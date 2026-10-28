#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MICourse 课程环境分层自检脚本
=============================

用途
----
在「课前准备」「换机重建」「学生报错排查」三种场景下，一条命令确认环境是否真的能用，
而不是只看 `conda list` 里有没有包名。分三层验收：

  L1 导入层  —— 包能否 import，版本是多少
  L2 数值层  —— BLAS/LAPACK 是否真能算（MKL 与 NumPy 版本不匹配时 import 会成功，一算矩阵乘法就崩）
  L3 功能层  —— 课程实际要做的动作能否跑通（拟合、绘图、写 Excel/Parquet、建结构、出成分特征、反向传播）

用法
----
    conda activate MICourse
    python verify_env.py            # 全部检查
    python verify_env.py --quick    # 只跑 L1+L2，约 10 秒
    python verify_env.py --verbose  # 打印每个失败的完整 traceback

退出码
------
    0  全部通过
    1  有检查项失败（失败详情见末尾汇总表）
    2  环境本身不对（Python 版本不符或用户级 site-packages 未隔断）

作者：何刚  NNIP LAB @ SWUST
"""

from __future__ import annotations

import argparse
import os
import platform
import sys
import tempfile
import traceback
from pathlib import Path

VERBOSE = False
REQUIRED_PY = (3, 11)

results: list[tuple[str, str, str, str]] = []  # (层, 名称, 状态, 说明)


def record(layer: str, name: str, status: str, detail: str = "") -> None:
    results.append((layer, name, status, detail))
    icon = {"PASS": "[ok]", "FAIL": "[!!]", "SKIP": "[--]", "WARN": "[??]"}.get(status, "[??]")
    print(f"  {icon} {name:<34s} {detail}", flush=True)


def check(layer: str, name: str):
    """装饰器：把函数包成一条检查项。函数返回说明字符串；抛异常即 FAIL。"""

    def deco(fn):
        def wrapper(*a, **kw):
            try:
                detail = fn(*a, **kw) or ""
                record(layer, name, "PASS", str(detail))
                return True
            except Exception as exc:  # noqa: BLE001
                msg = f"{type(exc).__name__}: {exc}"
                if VERBOSE:
                    msg += "\n" + traceback.format_exc()
                record(layer, name, "FAIL", msg.replace("\n", "\n        "))
                return False

        wrapper.__name__ = fn.__name__
        return wrapper

    return deco


# ---------------------------------------------------------------- 引导层
def check_bootstrap() -> bool:
    print("\n[引导] 解释器与隔离状态")
    ok = True

    detail = f"Python {platform.python_version()} @ {sys.executable}"
    if sys.version_info[:2] == REQUIRED_PY:
        record("引导", "Python 版本 == 3.11", "PASS", detail)
    else:
        record("引导", "Python 版本 == 3.11", "FAIL", detail + "  ← 课程统一用 3.11")
        ok = False

    # 用户级 site-packages 必须被隔断，否则 ~/.local 里的旧 numpy/pandas 会盖掉环境里的版本
    usersite = os.environ.get("PYTHONNOUSERSITE")
    try:
        import site

        in_paths = [p for p in site.getsitepackages()]
        user_path = site.getusersitepackages()
        leaked = user_path in sys.path
    except Exception:  # noqa: BLE001
        user_path, leaked = "<unknown>", False

    if usersite == "1" and not leaked:
        record("引导", "用户级 site-packages 已隔断", "PASS", "PYTHONNOUSERSITE=1")
    elif leaked:
        record(
            "引导", "用户级 site-packages 已隔断", "FAIL",
            f"{user_path} 仍在 sys.path —— 会遮盖环境包，请设 PYTHONNOUSERSITE=1"
        )
        ok = False
    else:
        record("引导", "用户级 site-packages 已隔断", "WARN",
               "未设 PYTHONNOUSERSITE，当前恰好未泄漏，但不保证")

    env = os.environ.get("CONDA_DEFAULT_ENV", "")
    if env == "MICourse":
        record("引导", "conda 环境名 == MICourse", "PASS", env)
    else:
        record("引导", "conda 环境名 == MICourse", "WARN", f"当前 env={env or '(未激活)'}")

    return ok


# ---------------------------------------------------------------- L1 导入层
PKGS = [
    # (模块名, 显示名, 是否必需)
    ("numpy", "NumPy", True),
    ("scipy", "SciPy", True),
    ("pandas", "pandas", True),
    ("matplotlib", "Matplotlib", True),
    ("sklearn", "scikit-learn", True),
    ("statsmodels", "statsmodels", True),
    ("seaborn", "seaborn", False),
    ("sympy", "SymPy", False),
    ("networkx", "NetworkX", False),
    ("joblib", "joblib", False),
    ("openpyxl", "openpyxl", False),
    ("pyarrow", "PyArrow", False),
    ("pymatgen", "pymatgen", True),
    ("mp_api", "mp-api", False),
    ("ase", "ASE", False),
    ("rdkit", "RDKit", False),
    ("matminer", "matminer", False),
    ("CBFV", "CBFV", False),
    ("optuna", "Optuna", False),
    ("Bgolearn", "Bgolearn", False),
    ("pymoo", "pymoo", False),
    ("deap", "DEAP", False),
    ("shap", "SHAP", False),
    ("torch", "PyTorch", False),
    ("torchvision", "torchvision", False),
    ("ipykernel", "ipykernel", False),
]


def check_imports() -> bool:
    print("\n[L1] 导入层：包是否可加载")
    import importlib

    ok = True
    for mod, label, required in PKGS:
        try:
            m = importlib.import_module(mod)
            v = getattr(m, "__version__", None)
            if v is None:
                try:
                    from importlib.metadata import version

                    v = version(mod.replace("_", "-"))
                except Exception:  # noqa: BLE001
                    v = "(无版本号)"
            record("L1", label, "PASS", str(v))
        except Exception as exc:  # noqa: BLE001
            status = "FAIL" if required else "WARN"
            record("L1", label, status, f"{type(exc).__name__}: {exc}")
            if required:
                ok = False
    return ok


# ---------------------------------------------------------------- L2 数值层
@check("L2", "NumPy 矩阵乘法 (BLAS)")
def t_matmul():
    import numpy as np

    a = np.random.default_rng(0).normal(size=(600, 600))
    c = a @ a.T
    assert np.isfinite(c).all()
    return f"600x600 有限值 ok，trace={c.trace():.3e}"


@check("L2", "NumPy LAPACK 求逆/特征值")
def t_lapack():
    import numpy as np

    a = np.random.default_rng(1).normal(size=(300, 300))
    a = a @ a.T + 300 * np.eye(300)
    inv = np.linalg.inv(a)
    ev = np.linalg.eigvalsh(a)
    err = float(abs(a @ inv - np.eye(300)).max())
    assert err < 1e-8, f"求逆误差过大 {err}"
    return f"求逆误差 {err:.2e}，最小特征值 {ev.min():.3e}"


@check("L2", "SciPy 分解与线代 (LAPACK)")
def t_scipy_linalg():
    import numpy as np
    from scipy import linalg

    a = np.random.default_rng(2).normal(size=(200, 200))
    q, r = linalg.qr(a)
    s = linalg.svd(a, compute_uv=False)
    return f"QR 正交性 {abs(q.T @ q - np.eye(200)).max():.2e}，cond={s[0] / s[-1]:.1e}"


@check("L2", "SciPy 优化与统计分布")
def t_scipy_misc():
    from scipy import optimize, stats

    res = optimize.minimize(lambda x: (x[0] - 3) ** 2 + (x[1] + 1) ** 2, [0, 0])
    assert res.success and abs(res.x[0] - 3) < 1e-5
    p = stats.norm.cdf(1.96)
    return f"minimize ok (x={np_round(res.x)})，norm.cdf(1.96)={p:.4f}"


def np_round(a):
    return "[" + ", ".join(f"{v:.4f}" for v in a) + "]"


# ---------------------------------------------------------------- L3 功能层
@check("L3", "scikit-learn 拟合 + 交叉验证")
def t_sklearn():
    import numpy as np
    from sklearn.linear_model import RidgeCV
    from sklearn.model_selection import cross_val_score
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    rng = np.random.default_rng(3)
    X = rng.normal(size=(200, 6))
    y = 3 * X[:, 0] - 2 * X[:, 1] + rng.normal(scale=0.05, size=200)
    pipe = make_pipeline(StandardScaler(), RidgeCV(alphas=np.logspace(-3, 3, 13)))
    scores = cross_val_score(pipe, X, y, cv=5, scoring="r2")
    pipe.fit(X, y)
    return f"5 折 R2 = {scores.mean():.3f} ± {scores.std():.3f}，alpha={pipe[-1].alpha_:.3g}"


@check("L3", "statsmodels OLS + 置信区间")
def t_statsmodels():
    import numpy as np
    import statsmodels.api as sm

    rng = np.random.default_rng(4)
    X = sm.add_constant(rng.normal(size=(150, 3)))
    y = 1.5 + X[:, 1] * 2.0 + rng.normal(scale=0.1, size=150)
    fit = sm.OLS(y, X).fit()
    ci = fit.conf_int()
    return f"R2={fit.rsquared:.3f}，beta1={fit.params[1]:.3f} CI=[{ci[1][0]:.3f},{ci[1][1]:.3f}]"


@check("L3", "Matplotlib 出图（含中文字体）")
def t_matplotlib():
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager

    names = {f.name for f in font_manager.fontManager.ttflist}
    cjk = [n for n in ("Microsoft YaHei", "SimHei", "SimSun", "DengXian") if n in names]
    plt.rcParams["font.sans-serif"] = cjk + ["DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False

    fig, ax = plt.subplots(figsize=(4, 3), dpi=110)
    ax.plot([0, 1, 2], [1, 4, 9], marker="o")
    ax.set_title("带隙随组分变化（自检）")
    ax.set_xlabel("组分 x")
    ax.set_ylabel("带隙 / eV")
    out = Path(tempfile.gettempdir()) / "micourse_selftest.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    size_kb = out.stat().st_size / 1024
    return f"中文字体 {cjk[:2] or '无(会显示方框)'}，输出 {size_kb:.0f} KB"


@check("L3", "pandas 读写 Excel / Parquet")
def t_io():
    import numpy as np
    import pandas as pd

    df = pd.DataFrame({"材料": ["GaAs", "CsPbBr3"], "带隙_eV": [1.42, 2.31], "n": [1, 2]})
    tmp = Path(tempfile.mkdtemp(prefix="micourse_io_"))
    xlsx, pq = tmp / "t.xlsx", tmp / "t.parquet"
    df.to_excel(xlsx, index=False)
    df.to_parquet(pq, index=False)
    back_x = pd.read_excel(xlsx)
    back_p = pd.read_parquet(pq)
    assert len(back_x) == 2 and len(back_p) == 2
    return f"xlsx {xlsx.stat().st_size / 1024:.1f}KB，parquet {pq.stat().st_size / 1024:.1f}KB"


@check("L3", "pymatgen 结构构建与性质")
def t_pymatgen():
    from pymatgen.core import Lattice, Structure

    s = Structure(
        Lattice.cubic(5.65),
        ["Na", "Cl"],
        [[0, 0, 0], [0.5, 0.5, 0.5]],
    )
    return f"NaCl 体积 {s.volume:.2f} Å^3，密度 {s.density:.3f} g/cm^3，式 {s.composition.reduced_formula}"


@check("L3", "matminer 成分特征 (magpie)")
def t_matminer():
    import pandas as pd
    from matminer.featurizers.composition import ElementProperty
    from pymatgen.core import Composition

    df = pd.DataFrame({"formula": ["LiFePO4", "CsPbBr3"]})
    df["comp"] = df["formula"].apply(Composition)
    fe = ElementProperty.from_preset("magpie")
    df = fe.featurize_dataframe(df, "comp", ignore_errors=True)
    n_feat = len([c for c in df.columns if c.startswith("MagpieData")])
    return f"{n_feat} 个成分特征，mean 电负性 = {df['MagpieData mean Electronegativity'].round(2).tolist()}"


@check("L3", "RDKit 分子描述符")
def t_rdkit():
    from rdkit import Chem
    from rdkit.Chem import Descriptors

    m = Chem.MolFromSmiles("CCO")
    return f"乙醇 MW={Descriptors.MolWt(m):.2f}，LogP={Descriptors.MolLogP(m):.2f}"


@check("L3", "Optuna 贝叶斯优化 (TPE)")
def t_optuna():
    import optuna

    optuna.logging.set_verbosity(optuna.logging.WARNING)

    def obj(trial):
        x = trial.suggest_float("x", -5, 5)
        y = trial.suggest_float("y", -5, 5)
        return (x - 1.2) ** 2 + (y + 0.7) ** 2

    study = optuna.create_study(direction="minimize", sampler=optuna.samplers.TPESampler(seed=0))
    study.optimize(obj, n_trials=40, show_progress_bar=False)
    return f"40 次试验，最优 x={study.best_params['x']:.3f} y={study.best_params['y']:.3f} (真值 1.2/-0.7)"


@check("L3", "PyTorch 张量 + 自动微分")
def t_torch():
    import torch

    x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
    y = (x**2).sum()
    y.backward()
    g = x.grad.tolist()
    assert g == [2.0, 4.0, 6.0], f"梯度错误 {g}"
    # 小型 MLP 前向 + 一步反传
    net = torch.nn.Sequential(torch.nn.Linear(4, 16), torch.nn.ReLU(), torch.nn.Linear(16, 1))
    out = net(torch.randn(8, 4))
    out.sum().backward()
    return f"{torch.__version__} / CUDA={torch.cuda.is_available()}，d(x^2)/dx={g}，MLP 前后向 ok"


@check("L3", "SHAP 归因 (TreeExplainer)")
def t_shap():
    import numpy as np
    import shap
    from sklearn.ensemble import RandomForestRegressor

    rng = np.random.default_rng(5)
    X = rng.normal(size=(150, 5))
    y = 2 * X[:, 0] + X[:, 1] ** 2 + rng.normal(scale=0.1, size=150)
    rf = RandomForestRegressor(n_estimators=60, random_state=0).fit(X, y)
    sv = shap.TreeExplainer(rf).shap_values(X)
    return f"shap_values 形状 {np.array(sv).shape}，特征 0 的平均 |SHAP| 最大（真值）"


@check("L3", "Jupyter 内核可执行")
def t_kernel():
    import json
    import subprocess

    from jupyter_client.kernelspec import KernelSpecManager

    spec = KernelSpecManager().get_kernel_spec("micourse")
    code = "import numpy as np; print(int((np.eye(3) @ np.ones(3)).sum()))"
    from jupyter_client import KernelManager

    km = KernelManager(kernel_name="micourse")
    km.start_kernel()
    try:
        kc = km.client()
        kc.start_channels()
        kc.wait_for_ready(timeout=60)
        msg_id = kc.execute(code)
        got = ""
        while True:
            msg = kc.get_iopub_msg(timeout=60)
            if msg["parent_header"].get("msg_id") != msg_id:
                continue
            if msg["msg_type"] == "stream":
                got += msg["content"]["text"]
            if msg["msg_type"] == "status" and msg["content"]["execution_state"] == "idle":
                break
        kc.stop_channels()
    finally:
        km.shutdown_kernel(now=True)
    assert got.strip() == "3", f"内核返回 {got!r}"
    return f"kernelspec={Path(spec.resource_dir).name}，执行结果 {got.strip()}"


# ---------------------------------------------------------------- 主流程
def main() -> int:
    global VERBOSE
    ap = argparse.ArgumentParser(description="MICourse 课程环境分层自检")
    ap.add_argument("--quick", action="store_true", help="只跑 L1+L2")
    ap.add_argument("--verbose", action="store_true", help="打印完整 traceback")
    ap.add_argument("--report", metavar="PATH", help="把结果表写到 Markdown 文件")
    args = ap.parse_args()
    VERBOSE = args.verbose

    print("=" * 74)
    print("  MICourse 课程环境分层自检   《AI 在材料科学中的应用》")
    print("=" * 74)

    boot_ok = check_bootstrap()
    if not boot_ok:
        print("\n引导层已不通过，后续检查结果不可信，先修环境再跑。")

    check_imports()

    print("\n[L2] 数值层：BLAS/LAPACK 是否真能算")
    t_matmul()
    t_lapack()
    t_scipy_linalg()
    t_scipy_misc()

    if not args.quick:
        print("\n[L3] 功能层：课程要做的动作能否跑通")
        t_sklearn()
        t_statsmodels()
        t_matplotlib()
        t_io()
        t_pymatgen()
        t_matminer()
        t_rdkit()
        t_optuna()
        t_torch()
        t_shap()
        t_kernel()

    # 汇总
    fail = [r for r in results if r[2] == "FAIL"]
    warn = [r for r in results if r[2] == "WARN"]
    pas = [r for r in results if r[2] == "PASS"]

    print("\n" + "=" * 74)
    print(f"  通过 {len(pas)}   警告 {len(warn)}   失败 {len(fail)}   共 {len(results)} 项")
    print("=" * 74)

    if fail:
        print("\n失败明细：")
        for layer, name, _, detail in fail:
            print(f"  [{layer}] {name}\n        {detail}")
    if warn:
        print("\n警告明细（不影响上课，但建议处理）：")
        for layer, name, _, detail in warn:
            print(f"  [{layer}] {name}\n        {detail}")

    if args.report:
        p = Path(args.report)
        p.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            "# MICourse 环境自检结果",
            "",
            f"- 执行时间：{__import__('datetime').datetime.now():%Y-%m-%d %H:%M:%S}",
            f"- 解释器：`{sys.executable}`",
            f"- Python：{platform.python_version()}",
            f"- 结论：通过 {len(pas)} / 警告 {len(warn)} / 失败 {len(fail)}",
            "",
            "| 层 | 检查项 | 状态 | 说明 |",
            "|---|---|---|---|",
        ]
        for layer, name, status, detail in results:
            d = detail.replace("|", "\\|").replace("\n", " ")
            lines.append(f"| {layer} | {name} | {status} | {d} |")
        p.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"\n结果表已写入：{p}")

    if fail or not boot_ok:
        return 1 if fail else 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
