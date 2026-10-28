# 课程环境 MICourse

> 环境名 `MICourse` ｜ Python 3.11.17 ｜ Windows / CPU，**不需要 GPU**
> 统一环境，后续各讲在此环境上扩展，不要为每讲单独建环境。

## 三步走

### 1. 建环境

```bash
conda create -n MICourse python=3.11 -y
conda activate MICourse
# 路线 A：按锁定清单整体安装（推荐，版本一次到位）
conda install -n MICourse -c conda-forge --file environment.yml -y
```

或按小节手工装（见 [`README-教师构建记录.md`](README-教师构建记录.md) 第三节的已安装清单）。

> 国内网络下若 conda 解析失败，用 `--override-channels -c conda-forge` 只走社区通道；不要替他人接受商业条款。

### 2. 必须设的环境变量

```bash
export PYTHONNOUSERSITE=1          # Git Bash / Linux
```

```powershell
$env:PYTHONNOUSERSITE = "1"        # PowerShell
```

**这条不是可选项**：不设的话，用户级 site-packages 里的旧 numpy / pandas 会盖掉环境内的包，出现"版本明明装对了却报错"的怪现象。

### 3. 自检（必须 44 项全过）

```bash
python environment/verify_env.py
```

分层自检覆盖：解释器归属 → 数值底座 → 机器学习 → 绘图 → 材料化学 → 优化与深度学习。任一项失败按输出提示修，修完重跑。

## 三种进入方式

| 方式 | 适合 | 命令 |
|---|---|---|
| 双击启动器 | 课堂、Windows 学生 | `进入MICourse环境.bat`（先校验解释器、关键包与 `PYTHONNOUSERSITE`，通过后打印「[就绪]」） |
| conda 激活 | 通用 | `conda activate MICourse` 后设 `PYTHONNOUSERSITE=1` |
| 绝对路径直调 | 脚本化、无人值守 | `PYTHONNOUSERSITE=1 python your_script.py` |

Jupyter：环境内已注册内核 `micourse`（显示名「Python 3.11 (MICourse)」），`kernel.json` 内已写入 `PYTHONNOUSERSITE=1`，在 JupyterLab 里直接选它即可。

## 目录里有什么

| 文件 | 用途 |
|---|---|
| `environment.yml` | 锁定版本清单，重建环境用 |
| `rebuild_env.sh` | 一键重建（含本项目已知坑的处理顺序） |
| `verify_env.py` | 44 项分层自检，交付与开课前必跑 |
| `进入MICourse环境.bat` | Windows 启动器（**生成物**，改内容请改 `make_launcher.py` 后重新生成） |
| `welcome.py` | 环境就绪欢迎页 |
| `check_lecture_code.py` / `check_assertions.py` | 逐讲代码可用性与教学断言核对 |
| `自检结果.md` | 2026-10-26 的验收快照（44/44） |
| `代码检查报告-第1-10讲.md` / `断言核对报告-第1-10讲.md` | 逐讲实跑记录 |
| `README-教师构建记录.md` | 教师侧完整构建过程、七个环境级故障与解法（换机重建必读） |

## 常见问题

| 现象 | 原因 | 处理 |
|---|---|---|
| 明明装了包却导入旧版本 | 用户级 site-packages 抢占 | 设 `PYTHONNOUSERSITE=1` |
| 矩阵乘法直接崩（`0xC06D007F`） | conda 的 MKL 版 numpy/scipy 与本机 MKL 冲突 | 用 pip 的 OpenBLAS wheel 覆盖，**不要用 conda 装 numpy/scipy** |
| 导入 torch 报 `WinError 1114` | pip wheel 自带的旧 `msvcp140.dll` 先于 torch 加载 | 用环境根目录的新版 CRT **覆盖**（不能删） |
| `CBFV` 导入失败 | setuptools ≥84 移除了 `pkg_resources` | 固定 `setuptools==80.9.0` |
| conda 批量安装被中断并回滚 | 清理缓存触发批量删除保护 | `--no-cache-dir` + 逐个包安装 |
| 脚本输出写入同步盘报 `WinError 5` | 云同步盘发布阶段 rename 失败 | 输出目录改到本地非同步路径 |

更完整的成因、验证过程与命令见 [`README-教师构建记录.md`](README-教师构建记录.md)。
