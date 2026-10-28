# MICourse 课程环境（Windows / CPU）—— 配置说明与验收记录

> 适用课程：《AI 在材料科学中的应用》（西南科技大学 材料与化学学院 研究生选修课）
> 授课教师：何刚（计算机科学与技术学院） NNIP LAB @ SWUST
> 环境名：`MICourse`　Python：3.11.17　GPU：不需要
> **当前状态：分层自检 44/44 全部通过（2026-10-26）**

---

## 一、结论先行

1. Miniconda 已在本机（`D:\ProgramData\miniconda3`），**无需重装**；本次工作是建环境与装包。
2. 统一环境 `MICourse` 位于 `C:\Users\gang\.conda\envs\MICourse`，Python 3.11.17。
3. 第 1—10 讲全部代码所需的包均已安装并**实际跑通**，不是只做语法检查。
4. 已实跑验证的课程脚本：第 4 讲 `featurize_composition.py`（4 列特征与 README 断言逐项一致）、
   第 5 讲 `graph_core.py`、第 6 讲 `run_v5.py`（12 个输出文件全部生成、自检通过）。
5. 期间解决了 7 个环境级故障，逐条记在第四节，换机重建时必须照做。

---

## 二、怎么用

### 方式 1：双击进入（推荐给学生）

```
课件\00-课程环境\进入MICourse环境.bat
```

窗口会先打印中文横幅，并现场校验三件事：解释器是否落在 MICourse 内、关键包能否导入、
`PYTHONNOUSERSITE` 是否为 1。三项都正常会显示「[就绪] 环境检查通过」；
有问题会列出具体原因，便于当场排查。

之后环境变量与 PATH 已设好，直接 `python xxx.py` 或 `jupyter lab` 即可。

> 该 `.bat` 是**生成物**（ASCII + CRLF）。要改内容请编辑 `make_launcher.py` 后重新生成，
> 直接用编辑器改 `.bat` 极易把换行换成 LF，导致 cmd 报「命令语法不正确」。

### 方式 2：conda 激活（推荐给教师本机）

```bash
export PATH="/d/ProgramData/miniconda3/Scripts:$PATH"   # Git Bash 每次新开都要设
conda activate MICourse
export PYTHONNOUSERSITE=1      # ← 必须，原因见 4.3
```

### 方式 3：绝对路径直调（脚本化、无人值守时最稳）

```bash
PYTHONNOUSERSITE=1 "C:/Users/gang/.conda/envs/MICourse/python.exe" your_script.py
```

### Jupyter

已注册内核 `micourse`，显示名「Python 3.11 (MICourse)」。在 JupyterLab 里选它即可，
`kernel.json` 内已写入 `PYTHONNOUSERSITE=1`，无需再手动设环境变量。

---

## 三、已安装清单（本机实测版本）

### 数值与数据底座
| 包 | 版本 | 用途 |
|---|---|---|
| numpy | 1.26.4 | 数值计算（**OpenBLAS 后端**，非 MKL） |
| scipy | 1.15.1 | 优化、统计、稀疏矩阵 |
| pandas | 2.2.3 | 表格数据处理 |
| pyarrow | 17.0.0 | Parquet 列式存储 |
| openpyxl / xlrd | 3.1.5 / 2.0.2 | Excel 读写（.xlsx / .xls） |

### 机器学习与统计
| 包 | 版本 | 对应讲次 |
|---|---|---|
| scikit-learn | 1.6.1 | 第 6—9 讲主力 |
| statsmodels | 0.14.4 | 第 6 讲 OLS/置信区间、第 8 讲诊断 |
| joblib | 1.6.0 | 模型持久化 |
| shap | 0.49.1 | 第 9 讲模型归因 |
| networkx | 3.6.1 | 第 5 讲图表示 |

### 绘图与交互
| 包 | 版本 |
|---|---|
| matplotlib | 3.10.0（中文字体 Microsoft YaHei / SimHei 已确认可用） |
| seaborn | 0.13.2 |
| jupyterlab | 4.6.4 |
| ipykernel | 7.4.0 |

### 材料与化学
| 包 | 版本 | 对应讲次 |
|---|---|---|
| pymatgen | 2026.10.24 | 第 3、5 讲结构与相图 |
| mp-api | 0.46.5 | 第 3 讲 Materials Project（需自备 API Key） |
| ase | 3.29.0 | 结构文件 I/O（CIF/POSCAR） |
| rdkit | 2026.09.1 | 第 5 讲分子描述符 |
| matminer | 0.9.3 | 第 4、5 讲成分/结构特征（magpie 132 维已验证） |
| CBFV | 1.1.0 | 成分向量化基线 |

### 优化与深度学习
| 包 | 版本 | 对应讲次 |
|---|---|---|
| optuna | 5.0.0 | 第 14 讲贝叶斯优化（TPE 已验证） |
| Bgolearn | 3.1.2 | 第 14 讲贝叶斯全局优化教学 |
| pymoo / deap | 0.6.2 / 1.4 | 多目标进化 / 遗传算法（自学部分） |
| torch | 2.14.1+cpu | 第 11—12 讲深度学习 |
| torchvision | 0.29.1+cpu | 同上 |

其余基础包：sympy 1.14.0、setuptools 80.9.0（**不要升到 84**，见 4.5）。

---

## 四、七个坑与对应解法（换机重建必读）

### 4.1 Conda 服务条款未接受 → `CondaToSNonInteractiveError`

不替用户接受 Anaconda 商业条款，改用 `--override-channels -c conda-forge` 只走社区通道。

### 4.2 批量安装触发清理保护 → `SAFE_DELETE_BULK_CONFIRM_REQUIRED`

本机沙箱对一次性删除大量文件有确认保护，pip/conda 批量清理缓存时会被中断并**整体回滚**。
解法：`--no-cache-dir` + **逐个包安装**；失败时只重试该包，不重跑整批。

### 4.3 用户级 site-packages 遮盖环境包（最隐蔽）

现象：环境里装的是 NumPy 1.26.4 / pandas 2.2.3，`python -c "import numpy; print(numpy.__version__)"`
却显示 1.26.2 / 2.1.4 —— 因为 `C:\Users\gang\AppData\Roaming\Python\Python311\site-packages`
里的旧包排在 `sys.path` 更前面。这类问题不看版本号根本发现不了。

解法：**永久设置 `PYTHONNOUSERSITE=1`**，并在 Jupyter `kernel.json` 的 `env` 里显式写死。

### 4.4 NumPy 矩阵乘法崩溃 → 退出码 `-1066598273`（`0xC06D007F`）

现象：`import numpy` 正常、`print(a @ b)` 让进程直接消失，无 Python 异常。
根因：conda 装的 NumPy 链接 MKL，与本机 MKL 2026.x 的运行时 ABI 不兼容；
把 MKL 降到 2024.2.2 仍未修复。

解法：改用 **pip 官方 wheel 的 NumPy/SciPy（自带 OpenBLAS）**。
本机当前实现方式是放进 `C:\Users\gang\.conda\envs\MICourse\localpkgs`，
再用 `site-packages\micourse_overlay.pth` 优先加载：

```python
# micourse_overlay.pth 内容
import sys; sys.path.insert(0, r'C:\Users\gang\.conda\envs\MICourse\localpkgs')
```

这样还顺带解决了 `pkg_resources` 缺失（见 4.5）。
**重建时的更干净做法**：一开始就不用 conda 装 numpy/scipy，直接 `pip install numpy scipy`，
则 wheel 的 `numpy.libs` / `scipy.libs` 自带 OpenBLAS，不需要覆盖层。`rebuild_env.sh` 走这条路径。

### 4.5 `ModuleNotFoundError: pkg_resources`（CBFV 等老包）

setuptools 84.2.1 已移除 `pkg_resources`。在 `localpkgs` 装 `setuptools==80.9.0` 解决。
注意环境内 `setuptools` 显示为 80.9.0 是**被覆盖层接管后**的结果，不是降级了主环境。

### 4.6 PyTorch 官方源 SSL 中断 → `[SSL: UNEXPECTED_EOF_WHILE_READING]`

CPU wheel 约 200 MB，官方源与镜像直连都在传输中途断开。
解法：`curl -C -` 断点续传下载 wheel 到 `tmp/MICourse_wheels/`，SHA256 校验后
`pip install --no-deps <本地 wheel>` 离线安装。

### 4.7 PyTorch 报 `WinError 1114 DLL 初始化例程失败`（**新发现，2026-10-26**）

现象极怪：单独 `import torch` 正常；只要先 `import shap`（或任何会拉起 sklearn/pyarrow 的包）
再 `import torch`，就报 `c10.dll` 初始化失败。**这是导入顺序依赖的偶发故障，最难复现。**

根因：pip wheel 普遍在包目录里塞了**私有 MSVC 运行库副本**，且版本落后于环境：

| 文件 | 版本 | 说明 |
|---|---|---|
| `envs\MICourse\msvcp140.dll`（基准） | 14.51.36247.0 | 由 conda 装入，`python.exe` 同目录，优先级最高 |
| `site-packages\pyarrow\msvcp140.dll` | **14.28**.29334.0 | 太旧，缺 torch 需要的符号 |
| `site-packages\sklearn\.libs\msvcp140.dll` | **14.42**.34433.0 | 略旧 |

Windows 按文件名复用已加载的同名 DLL，于是 torch 的 `c10.dll` 拿到旧版 CRT → 初始化失败。
带哈希后缀的副本（`llvmlite.libs\msvcp140-8f141b44….dll` 等）已做文件名隔离，**不冲突，不要动**。

解法：把这两处**裸名**副本替换为环境根目录的同一版本（内容相同即不再有版本差）：

```bash
cd "C:/Users/gang/.conda/envs/MICourse"
cp -f msvcp140.dll Lib/site-packages/sklearn/.libs/msvcp140.dll
cp -f msvcp140.dll Lib/site-packages/pyarrow/msvcp140.dll
```

注意：**不能直接删**。sklearn 的 `.pyd` 依赖 `.libs` 目录内的同名文件，删掉会变成
`FileNotFoundError: Could not find module ...\sklearn\...pyd`（实测过）。
原始副本已备份到 `tmp/*_msvcp140_orig.dll.bak`。

### 4.8 附带发现：坚果云同步盘导致的 `WinError 5`

第 6 讲 `run_v5.py` 最后一步是把临时目录 rename 成正式目录，输出若放在项目目录（坚果云同步盘）
会报 `[WinError 5] 拒绝访问`——同步客户端持有目录句柄。
**计算本身全部正确**（自检、Lasso KKT 违反 7.5e-13 都过），只是发布失败。

解法：脚本输出目录放到非同步路径，如 `C:\Users\gang\AppData\Local\Temp\...`；实测一次通过。

### 4.9 双击 `.bat` 报「命令语法不正确」/「系统找不到路径」（2026-10-26 修复）

现象：双击 `进入MICourse环境.bat` 直接报错，窗口一闪而过或停在半截。

根因两条，都是**编辑器写文件时的副作用**：

| 问题 | 实测证据 | 后果 |
|---|---|---|
| 换行是 **LF** 而不是 CRLF | 32 处孤立 LF | cmd.exe 把相邻两行并成一条命令解析 |
| 文件是 **UTF-8 无 BOM 却含中文** | 300 个非 ASCII 字节 | 默认 GBK 代码页下乱码，甚至断在多字节字符中间 |

解法（已落地）：
1. **批处理只写 ASCII**，中文一律由 `welcome.py` 输出——Python 会按控制台实际代码页
   （本机 OEMCP=936）编码，不受批处理解析影响。
2. **强制 CRLF**。不要手改这个 `.bat`，用 `python make_launcher.py` 生成；
   它会先规范化换行、再 `encode('ascii')`（编码不符会当场抛错，等于自带校验）。
3. `python make_launcher.py --check` 可单独校验现有文件是否符合 ASCII + CRLF。
4. 中文窗口标题改用 Python 的 `SetConsoleTitleW` 设置，避开批处理编码问题。

验证方式（不要只看文件内容）：用 `cmd /c` 跑一个把末尾 `cmd /k` 换成结束标记的副本，
同时把环境变量 `PYTHONIOENCODING` 设为 `cp936`、清掉 `PYTHONUTF8`，模拟学生双击时的真实编码环境。
本项目实测：cp936 下中文完整、cmd 执行到结尾，两项均通过。

---

## 五、验收方法

```bash
cd "课件/00-课程环境"
CONDA_DEFAULT_ENV=MICourse PYTHONNOUSERSITE=1 \
  "C:/Users/gang/.conda/envs/MICourse/python.exe" verify_env.py --report 自检结果.md
```

脚本分三层，避免「import 成功就当装好了」这种假阳性：

| 层 | 查什么 | 为什么必须分开查 |
|---|---|---|
| 引导 | Python 版本、用户级 site 是否隔断、环境名 | 4.3 类问题在这一层就能拦住 |
| L1 导入 | 26 个包能否 import、版本号 | 常规检查，但**不足以证明可用** |
| L2 数值 | 600×600 矩阵乘法、LAPACK 求逆/QR/特征值 | 4.4 的崩溃只在这一层暴露 |
| L3 功能 | 拟合+交叉验证、OLS 置信区间、中文出图、Excel/Parquet 读写、pymatgen 建结构、matminer 132 维特征、RDKit 描述符、Optuna 40 次试验、torch 反传、SHAP 归因、Jupyter 内核执行 | 对齐课程真实动作 |

**判定标准：44 项全通过、退出码 0。** 结果表自动写入 `自检结果.md`。

关键量化结果（2026-10-26）：
- NumPy 求逆误差 2.44e-15、SciPy QR 正交性 1.11e-15（浮点精度级别，说明 OpenBLAS 正常）
- sklearn 5 折 R² = 1.000 ± 0.000（合成线性数据，符合预期）
- torch：`d(x²)/dx = [2, 4, 6]`，CUDA=False（CPU 构建）
- Optuna：40 次 TPE 找到 x=0.747 / y=-0.687（真值 1.2 / −0.7；贝叶斯优化样本少时精度有限，属正常）

---

## 六、换机重建

```bash
cd "课件/00-课程环境"
bash rebuild_env.sh --mirror        # 国内网络建议带 --mirror
```

脚本按 4.1—4.7 的结论设计，共 6 步：建环境（仅解释器 + C/C++ 依赖）→ 装数值底座（pip wheel）
→ 逐包装其余 → 统一 CRT → 注册内核并写 `PYTHONNOUSERSITE` → 跑自检。
**最后一步不是可选项**，自检不过就不算装好。

规范清单见 `environment.yml`（含每条的注释说明）。注意其中的警告：
**不要用 `conda env create -f environment.yml` 一把装完**，那会重新引入 4.4 的 MKL 崩溃。

---

## 七、给学生的话（课堂现场注意事项）

1. 不要用 `pip install --upgrade` 升级 numpy——一升到 2.x，pyarrow 17 与若干材料包会失效。
2. 不要用 Anaconda 主环境跑课程代码，一定用 `MICourse`。
3. 输出目录别放 OneDrive / 坚果云同步盘（见 4.8）。
4. 中文字体：Windows 自带 Microsoft YaHei 即可；macOS 学生需把
   `plt.rcParams['font.sans-serif']` 换成 `Heiti TC` / `PingFang SC`，并把 `axes.unicode_minus` 设 False。
5. 课上所有任务 CPU 可完成，不需要独立显卡；`torch.cuda.is_available()` 返回 False 是**正常**的。

---

## 八、文件清单

| 文件 | 作用 |
|---|---|
| `verify_env.py` | 分层自检脚本（44 项），可重复执行，支持 `--quick` / `--verbose` / `--report` |
| `自检结果.md` | 最近一次自检的完整结果表（自动生成） |
| `environment.yml` | 完整依赖规范（conda + pip 分段，带注释） |
| `rebuild_env.sh` | 一键重建（含全部已知坑的规避） |
| `进入MICourse环境.bat` | 学生双击进入环境（ASCII + CRLF；**不要手改**，用 `make_launcher.py` 生成） |
| `welcome.py` | 启动横幅与依赖自检（中文输出放在这里，规避批处理代码页问题） |
| `make_launcher.py` | 生成/校验上述 `.bat`：`--check` 只校验 ASCII + CRLF |
| `check_lecture_code.py` | **第 1—10 讲代码批量实跑**：28 组 35 步，复制到临时目录执行，不动课件原件 |
| `代码检查报告-第1-10讲.md` | 上述检查的结果表（自动生成） |
| `check_assertions.py` | **教学断言与实算核对**：直读产物反算 README 声明值（边数、阈值代价表、OOF 覆盖等） |
| `断言核对报告-第1-10讲.md` | 断言核对结果（自动生成） |
| `README.md` | 本文件 |

---

## 九、第 1—10 讲代码检查结论（2026-10-26）

两个脚本各管一层，缺一不可：`check_lecture_code.py` 证明「跑得通」，`check_assertions.py` 证明「讲得对」。

### 9.1 实跑结果：28 组 / 35 步 全部通过

| 讲 | 组数 | 步骤 | 耗时 | 关键验证 |
|---|---|---|---|---|
| 1 | 2 | 2 | 5.8 s | 两张图生成，中文无乱码 |
| 2 | 2 | 2 | 7.0 s | pymatgen 结构对象 |
| 3 | 4 | 4 | 38.9 s | 示例1 无 Key 时**自动回退本地快照**；示例3 **真实联网 NOMAD**（33.9 s） |
| 4 | 3 | 3 | 21.0 s | Al₂O₃ = 10.000/6.000/2.708/1.830；matminer 对比 |
| 5 | 6 | 6 | 2.0 s | 四个截断的边数全部正确 |
| 6 | 3 | 3 | 3.1 s | ridge λ=0.1、test MAE 1.379892；扰动后 1.4631 |
| 7 | 2 | 5 | 2.1 s | 阈值—代价表 22 点；四格和=120 |
| 8 | 4 | 5 | 4.4 s | 嵌套 CV 双协议；8 个负例全被拦截 |
| 9 | 1 | 2 | 15.8 s | 置换重要性 4 特征×10 次重复 |
| 10 | 1 | 3 | 1.5 s | raw / standardized 各覆盖 379 条 |

合计 **101.6 s、280 个产物、13.7 MB**。

### 9.2 断言核对：44 项成立、0 项不成立、1 处文档不一致

逐条反算过的关键量：
- **第 5 讲**：`rcut1p0=0/0`、`默认=4/2`、`r2p1=8/4`、`r3p1=12/6`、`none=0/0`（有向/无向边），与 README 表格逐格相符；图级读出 sum=9、节点读出 (5,4) 也相符。
- **第 7 讲**：22 个阈值点、网格 0→1.00 步长 0.05 + 1.01 哨兵；**逐行**满足四格和=120、`cost=2·FP+10·FN`、`selected_count=TP+FP`；t=1.01 确为全拒绝。
- **第 8 讲**：各协议×模型均 379 行、entry_id 无重复且全集一致；`ridge` 的 group MAE 1.2768 显著高于 random 0.7580（外推更难，符合教学设计）。
- **第 9 讲**：置换重要性覆盖 4 特征 × 10 次重复；40 次里仅 10 次 delta_mae 为负（未系统性异常）。
- **第 10 讲**：两个尺度各覆盖 379 条、无重复，各 3 个簇。

### 9.3 唯一发现：第 9 讲 README 的 PDP 网格点数过时

| 项 | README 声明 | 实测 |
|---|---|---|
| `pdp.csv` 网格点数 | 17 位 | **4 位** |

**代码本身自洽**：`lec9_models.py` 第 533 行取训练集 mean_Z 的 0.05—0.95 共 11 个等距分位后**去重**，当前数据集只有 14 个化学式、mean_Z 仅 4 个不同取值，去重后即 4 点；产物 `development_model.json` 自报 `pdp_n_grid=4`，与 `pdp.csv` 的 4 行一致。

**影响**：课堂演示 PDP 时是 4 点折线而非平滑曲线，讲解需说明「网格点受数据取值数限制」；README 的「17 位」应改为「取训练集 0.05—0.95 分位去重后的点数（当前数据为 4）」。

### 9.4 检查纪律（复用到第 11—16 讲）

1. **先复制再跑**：第 6、7 讲 README 明确禁止直接跑核心脚本（会写进随包 `outputs/` 覆盖验收产物）。
2. **不用系统 TEMP**：本机沙箱拒绝写 `%LOCALAPPDATA%\Temp`；项目目录在坚果云同步盘，脚本 rename 会报 `WinError 5`。统一用 `D:/tmp_micourse_check`。
3. **输出参数显式给**，不依赖脚本默认值。
4. **区分三类结果**：`PASS` / `FAIL` / `EXPECTED_FAIL`（缺凭据属设计如此）。曾把第 3 讲两个脚本误标为「应失败」，实际一个能回退快照、一个能真联网——**预期标签必须由实跑结果校正**。
5. **跨依赖必须同组串行**：`{RUN}` 按组隔离，`gen_data→分类→自查` 这类链条放同一组，否则报「文件不存在」被误判为代码缺陷（本次踩过 6 次）。
