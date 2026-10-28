#!/usr/bin/env bash
# =============================================================================
# MICourse 课程环境一键重建（Windows / Git Bash 或 WSL 的 bash）
#
# 用法：
#   bash rebuild_env.sh              # 用默认 pip 源
#   bash rebuild_env.sh --mirror     # 用阿里云 PyPI 镜像（国内网络更快）
#   bash rebuild_env.sh --env-name MICourse2   # 换个环境名做试验
#
# 设计原则（每一条都对应一个真实踩过的坑，不要随意简化）：
#   1. conda 只装解释器和纯 C/C++ 依赖；numpy/scipy 走 pip 官方 wheel（自带 OpenBLAS），
#      因为 Windows 上 conda 的 MKL 版 NumPy 与本机 MKL 2026.x 冲突，一算矩阵乘法就崩。
#   2. 每个 pip 包单独安装。批量安装会触发本机 pip 清理保护导致整体回滚。
#   3. 统一 MSVC 运行库版本。pyarrow 自带 msvcp140 14.28、sklearn 自带 14.42，
#      只要它们比 torch 先加载，torch 的 c10.dll 就报 WinError 1114。
#   4. 固化 PYTHONNOUSERSITE=1，隔断用户级 site-packages。
#   5. 最后必须跑 verify_env.py，44 项全过才算成功。
# =============================================================================
set -uo pipefail

ENV_NAME="MICourse"
PY_VER="3.11"
USE_MIRROR=0
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --mirror)   USE_MIRROR=1; shift ;;
    --env-name) ENV_NAME="$2"; shift 2 ;;
    -h|--help)  sed -n '2,22p' "$0"; exit 0 ;;
    *) echo "未知参数：$1"; exit 2 ;;
  esac
done

PIP_INDEX=()
if [[ $USE_MIRROR -eq 1 ]]; then
  PIP_INDEX=(-i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com)
fi

# ---------------------------------------------------------------- 0. 找 conda
find_conda() {
  if command -v conda >/dev/null 2>&1; then command -v conda; return; fi
  for c in \
    "/d/ProgramData/miniconda3/Scripts/conda.exe" \
    "/c/ProgramData/miniconda3/Scripts/conda.exe" \
    "$HOME/miniconda3/Scripts/conda.exe" \
    "$HOME/anaconda3/Scripts/conda.exe" \
    "/d/ProgramData/miniconda3/condabin/conda" ; do
    [[ -x "$c" ]] && { echo "$c"; return; }
  done
  return 1
}

CONDA_BIN="$(find_conda)" || { echo "[x] 找不到 conda，请先安装 Miniconda 或把它加进 PATH"; exit 1; }
CONDA_ROOT="$(cd "$(dirname "$CONDA_BIN")/.." && pwd)"
echo "[i] conda: $CONDA_BIN"
echo "[i] 目标环境: $ENV_NAME (Python $PY_VER)"

# ---------------------------------------------------------------- 1. 建环境
echo
echo "=== [1/6] 创建 conda 环境（只装解释器与 C/C++ 依赖）==="
if "$CONDA_BIN" env list | awk '{print $1}' | grep -qx "$ENV_NAME"; then
  echo "[i] 环境已存在，跳过创建。要重建请先 conda env remove -n $ENV_NAME"
else
  "$CONDA_BIN" create -y -n "$ENV_NAME" --override-channels -c conda-forge \
    "python=$PY_VER" pip rdkit openpyxl xlrd sympy jupyterlab ipykernel \
    || { echo "[x] 环境创建失败"; exit 1; }
fi

ENV_PREFIX="$("$CONDA_BIN" run -n "$ENV_NAME" python -c 'import sys; print(sys.prefix)' | tail -1)"
PY="$ENV_PREFIX/python.exe"
[[ -x "$PY" ]] || PY="$ENV_PREFIX/bin/python"
[[ -x "$PY" ]] || { echo "[x] 找不到环境内 python：$ENV_PREFIX"; exit 1; }
echo "[i] 环境路径: $ENV_PREFIX"

export PYTHONNOUSERSITE=1

# ---------------------------------------------------------------- 2. 数值底座
echo
echo "=== [2/6] 安装数值底座（pip 官方 wheel，自带 OpenBLAS）==="
for pkg in "numpy>=1.26,<2" "scipy>=1.11"; do
  echo "--- $pkg"
  "$PY" -m pip install --no-cache-dir --no-warn-script-location "${PIP_INDEX[@]}" "$pkg" \
    || { echo "[x] $pkg 安装失败"; exit 1; }
done

# ---------------------------------------------------------------- 3. 其余包
echo
echo "=== [3/6] 逐包装载其余依赖（单包安装，避免清理钩子回滚）==="
PKGS=(
  "pandas>=2.1"
  "matplotlib>=3.8"
  "seaborn>=0.13"
  "pyarrow>=15,<18"
  "statsmodels>=0.14"
  "scikit-learn>=1.4"
  "joblib>=1.3"
  "networkx>=3.2"
  "pymatgen>=2024.1"
  "ase>=3.22"
  "matminer>=0.9"
  "optuna>=3.5"
  "pymoo>=0.6"
  "deap>=1.4"
  "shap>=0.44"
  "mp-api>=0.41"
  "Bgolearn>=3.1"
  "CBFV>=1.0"
  "torch>=2.3"
  "torchvision>=0.18"
)
FAILED=()
for pkg in "${PKGS[@]}"; do
  printf '--- %-22s ' "$pkg"
  if "$PY" -m pip install --no-cache-dir --no-warn-script-location "${PIP_INDEX[@]}" "$pkg" >/tmp/micourse_pip.log 2>&1; then
    echo "ok"
  else
    echo "FAILED（详见 /tmp/micourse_pip.log）"
    FAILED+=("$pkg")
  fi
done
if [[ ${#FAILED[@]} -gt 0 ]]; then
  echo
  echo "[!] 以下包安装失败，可稍后单独重试："
  printf '    %s\n' "${FAILED[@]}"
fi

# ---------------------------------------------------------------- 4. 统一 CRT
echo
echo "=== [4/6] 统一 MSVC 运行库（修复 torch WinError 1114）==="
"$PY" - "$ENV_PREFIX" <<'PYEOF'
import sys, os, shutil, glob
prefix = sys.argv[1]
site = os.path.join(prefix, "Lib", "site-packages")
canon = None
for cand in (os.path.join(prefix, "msvcp140.dll"),
             os.path.join(prefix, "Library", "bin", "msvcp140.dll")):
    if os.path.exists(cand):
        canon = cand
        break
if canon is None:
    print("  [i] 环境内无 msvcp140.dll 基准副本，跳过（pip wheel 通常自带新版，一般无冲突）")
    sys.exit(0)

# 只处理「裸名」副本；带哈希后缀（如 msvcp140-8f141b44....dll）是重命名隔离的，不会被复用
pat = ["msvcp140.dll", "MSVCP140.dll"]
replaced = 0
for name in pat:
    for path in glob.glob(os.path.join(site, "**", name), recursive=True):
        d = os.path.dirname(path)
        if os.path.abspath(path) == os.path.abspath(canon):
            continue
        # 只替换包根目录或 .libs 目录下的副本
        if os.path.basename(d).lower() not in (".libs", "lib") and \
           os.path.dirname(d) != site:
            continue
        try:
            shutil.copy2(canon, path)
            replaced += 1
            print(f"  [ok] 替换 {os.path.relpath(path, prefix)}")
        except Exception as e:
            print(f"  [!] 无法替换 {path}: {e}")
print(f"  共替换 {replaced} 处私有 CRT 副本")
PYEOF

# ---------------------------------------------------------------- 5. 内核
echo
echo "=== [5/6] 注册 Jupyter 内核（含用户级 site 隔断）==="
"$PY" -m ipykernel install --user --name micourse --display-name "Python 3.11 (MICourse)" >/dev/null 2>&1 \
  && echo "[ok] 内核 micourse 已注册" || echo "[!] 内核注册失败，可手动执行 ipykernel install"

KDIR="$HOME/AppData/Roaming/jupyter/kernels/micourse"
[[ -d "$KDIR" ]] || KDIR="$HOME/.local/share/jupyter/kernels/micourse"
if [[ -f "$KDIR/kernel.json" ]]; then
  "$PY" - "$KDIR/kernel.json" <<'PYEOF'
import json, sys
p = sys.argv[1]
cfg = json.load(open(p, encoding="utf-8"))
cfg.setdefault("env", {})["PYTHONNOUSERSITE"] = "1"
json.dump(cfg, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(f"[ok] 已写入 PYTHONNOUSERSITE=1 → {p}")
PYEOF
fi

# ---------------------------------------------------------------- 6. 验收
echo
echo "=== [6/6] 分层自检（必须 44/44 通过）==="
CONDA_DEFAULT_ENV="$ENV_NAME" PYTHONNOUSERSITE=1 "$PY" "$SCRIPT_DIR/verify_env.py" \
  --report "$SCRIPT_DIR/自检结果.md"
RC=$?

echo
if [[ $RC -eq 0 ]]; then
  echo "=============================================="
  echo " 环境就绪。进入方式："
  echo "   conda activate $ENV_NAME"
  echo " 或直接：$PY"
  echo "=============================================="
else
  echo "=============================================="
  echo " 自检未全过（退出码 $RC），请查上面的失败明细。"
  echo "=============================================="
fi
exit $RC
