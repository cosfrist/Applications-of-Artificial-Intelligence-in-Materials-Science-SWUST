# -*- coding: utf-8 -*-
"""
第 2 讲 示例代码（二）：数据仓库选源六问 + pymatgen 结构对象入门
================================================================

对应 PPT：第 27、28、29、30、31、35、36 页
对应讲义：第三章「数据仓库与访问」、第四章「pymatgen 概览」

本脚本做三件事：
  1. 用「选源六问」给八个主流仓库建档，生成可比较的对照表
  2. 演示为什么结构数据不能只用 pandas 读：分数坐标 vs 笛卡尔坐标
  3. 若已安装 pymatgen，则用真实 API 对象演示 Composition / Lattice / Structure

说明：第 3 部分需要 pymatgen；未安装时脚本会自动跳过，不影响前两部分。
      课程标准环境中 pymatgen 于第 3 讲前安装。
================================================================
"""

import os
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '输出')
os.makedirs(OUT_DIR, exist_ok=True)

# =================================================================
# 第一部分　选源六问：给八个仓库建档
# =================================================================
print("=" * 78)
print("第一部分　选源六问：八个主流仓库建档")
print("=" * 78)

# 字段含义：
#   access      访问方式（REST / OPTIMADE / 客户端 / 下载 / 商业接口）
#   open        是否开放免费
#   curation    数据策展方式
#   scale       规模量级（条目数）
#   datatypes   提供的数据类型
#   fair        FAIR / 溯源支持程度（1-5）
#   cite        是否指定引用文献
REPOS = [
    dict(name="Materials Project", cn="材料项目", kind="DFT计算库",
         open="是（CC BY 4.0）", access="REST API + MPRester 客户端",
         curation="自动计算 + 人工校验 + 社区反馈", scale="~20 万条计算材料",
         datatypes="CIF/POSCAR、计算性质、计算参数", fair=4,
         cite="Jain et al., APL Mater 2013",
         fit="性质回归的主数据源", highlight=True),
    dict(name="NOMAD", cn="欧洲材料数据库", kind="DFT + 实验",
         open="是", access="OPTIMADE + REST API",
         curation="自动归档（原始计算输出文件）", scale=">1000 万条记录",
         datatypes="原始计算输出、结构、性质、实验数据", fair=5,
         cite="Knights et al., Sci. Data 2022",
         fit="需要可追溯性与原始文件时", highlight=True),
    dict(name="AFLOW", cn="AFLOW 数据库", kind="DFT计算库",
         open="是", access="REST API + 客户端",
         curation="自动计算 + 人工策展", scale="~400 万条",
         datatypes="结构、性质、ICSD 匹配标签", fair=4,
         cite="Curtarolo et al., Comput. Mater. Sci. 2012",
         fit="高温相、多元素体系", highlight=False),
    dict(name="JARVIS (D-ML)", cn="JARVIS 基准集", kind="DFT计算库 + 基准",
         open="是", access="数据下载 + API",
         curation="自动计算 + 统一预处理流水线", scale="~100 万条，56 个 Matbench 任务",
         datatypes="结构、性质、预训练模型", fair=3,
         cite="Choudhary et al., npj Comput. Mater. 2019",
         fit="算法对比与基准测试", highlight=True),
    dict(name="OQMD", cn="开放量子材料数据库", kind="DFT计算库",
         open="是", access="REST API",
         curation="自动计算 + 相图分析", scale="~150 万条",
         datatypes="结构、形成能、相稳定性", fair=4,
         cite="Saal et al., APL Mater. 2013",
         fit="相稳定性与凸包分析", highlight=False),
    dict(name="Materials Cloud", cn="材料云", kind="DFT + 工作流",
         open="是", access="API + 工作流服务",
         curation="强调工作流溯源（NoSQL 架构）", scale="快速增长中",
         datatypes="结构、计算、工作流溯源数据", fair=5,
         cite="Krug et al., Sci. Data 2019",
         fit="大规模工作流数据管理", highlight=False),
    dict(name="COD", cn="开放晶体结构库", kind="实验结构库",
         open="是（订阅免费）", access="REST API + CIF 下载",
         curation="**全部人工评审**", scale="~50 万条实测结构",
         datatypes="CIF、实测结构元数据", fair=4,
         cite="Kratythisakul et al., Sci. Data 2020",
         fit="补充实测结构数据", highlight=True),
    dict(name="ICSD / ICDD", cn="国际晶体结构数据库", kind="策展结构库",
         open="否（**收费订阅**）", access="商业接口 / CCDC",
         curation="专家评审（覆盖最广）", scale="~300 万条",
         datatypes="实测结构、专业元数据", fair=3,
         cite="各机构分别引用",
         fit="关键结构权威核查（不可批量）", highlight=False),
]

repos = pd.DataFrame(REPOS)

print(f"{'仓库':<22}{'类型':<14}{'开放':<16}{'FAIR':>5}")
print("-" * 78)
for _, r in repos.iterrows():
    mark = '★' if r.highlight else ' '
    print(f"{mark}{r['name']:<21}{r['kind']:<14}{r['open']:<16}{r['fair']:>5}")

print()
print("★ = 本课程建议重点掌握的仓库")
print()
print("【本课程默认取数组合】")
print("  · MP       —— 打底主数据源，社区与文档最成熟")
print("  · NOMAD    —— 需要原始计算输出与溯源时补充")
print("  · COD      —— 补充实测结构")
print("  · Matbench —— 做方法对比时的标准任务集")
print()
print("【选源六问自查】以Materials Project 为例：")
mp = repos[repos['name'] == 'Materials Project'].iloc[0]
for q, v in [("① 开放/混合/订阅", mp['open']),
             ("② 访问方式", mp['access']),
             ("③ 策展程度", mp['curation']),
             ("④ 规模与覆盖", mp['scale']),
             ("⑤ 数据类型", mp['datatypes']),
             ("⑥ 引用规范", mp['cite'])]:
    print(f"  {q:<16} → {v}")

print()
print("【与 JARVIS 对比，答案会怎么变】")
jb = repos[repos['name'] == 'JARVIS (D-ML)'].iloc[0]
print(f"  ② 访问方式      → {jb['access']}（以数据下载为主）")
print(f"  ③ 策展程度      → {jb['curation']}")
print(f"  ⑥ 引用规范      → {jb['cite']}")
print("  → 接口不同意味着【取数代码不能照搬】，这是换库时最实际的成本。")

# =================================================================
# 第二部分　为什么结构数据不能只用 pandas 读
# =================================================================
print()
print("=" * 78)
print("第二部分　分数坐标 vs 笛卡尔坐标：pandas 的盲区")
print("=" * 78)

# 一个立方晶胞，晶格常数 4.0 Å，晶格矢量与坐标轴平行
lattice_matrix = np.array([
    [4.0, 0.0, 0.0],
    [0.0, 4.0, 0.0],
    [0.0, 0.0, 4.0],
])

# 两个原子：一个在原点，一个在面心
species = ['Na', 'Cl']
frac_coords = np.array([
    [0.00, 0.00, 0.00],
    [0.50, 0.50, 0.50],
])

print("晶格矩阵（Å）：")
print(lattice_matrix)
print()
print("分数坐标（fractional）：")
for s, c in zip(species, frac_coords):
    print(f"  {s:<4}{c}")
print()
print("笛卡尔坐标 = 分数坐标 @ 晶格矩阵：")
cart = frac_coords @ lattice_matrix
for s, c in zip(species, cart):
    print(f"  {s:<4}{np.round(c, 3)}")

print()
print("→ 朴素做法 `df[['x','y','z']]` 拿到的是【分数坐标】，不是真实位置。")
print("→ 如果把晶格常数从 4.0 改成 4.4（真实 NaCl 为 5.64），")
print("   分数坐标【一个数字都不会变】，但所有原子间距和密度全都变了。")

print()
print("【密度验算】")
volume = abs(np.linalg.det(lattice_matrix))   # 晶胞体积
mass = (22.99 + 35.45) / 6.022e23            # 单个 NaCl 单元的摩尔质量
# NaCl 结构每晶胞含 4 个 NaCl
density = 4 * mass / (volume * 1e-24)
print(f"  晶胞体积 = {volume:.2f} Å³")
print(f"  晶胞质量 = {4 * mass:.3e} g")
print(f"  密度     = {density:.3f} g/cm³   （真实 NaCl 为 2.16 g/cm³）")

print()
print("→ 【关键结论】只用 pandas 存一串坐标数字，就丢掉了『坐标依赖于晶格』")
print("   这一本质关系。没有晶格信息的坐标，在物理上是无意义的。")

print()
print("【pandas 看不到的另外三件事】")
items = [
    ("对称性与空间群", "判断结构属于哪个空间群，需要专门算法，不是数原子个数"),
    ("周期性边界", "邻居搜索必须考虑跨晶胞边界的原子，否则会漏掉最近邻"),
    ("等价结构", "同一结构换个原点/换套晶格就是另一个表示，\n     直接当成两个样本会造成【数据泄漏式重复】"),
]
for k, v in items:
    print(f"  · {k}：{v}")

print()
print("→ 这正是引入 pymatgen 的原因：它把这些规则封装成对象方法。")

# =================================================================
# 第三部分　pymatgen 演示（未安装则跳过）
# =================================================================
print()
print("=" * 78)
print("第三部分　pymatgen 核心对象")
print("=" * 78)

try:
    from pymatgen.core import Composition, Structure, Lattice
    HAS_PYMATGEN = True
except ImportError:
    HAS_PYMATGEN = False
    print("!! 未检测到 pymatgen，跳过本部分。")
    print("   安装：conda install -n MICourse -y pymatgen")
    print("   （本课程将在第 3 讲前统一安装）")

if HAS_PYMATGEN:
    # ① Composition：只关心化学式与配比
    print("① Composition —— 只有组成，没有空间信息")
    print("-" * 78)
    for f in ["Fe2O3", "Ga0.5Al0.5N", "MAPbI3"]:
        c = Composition(f)
        print(f"  {f:<12} 约化式 = {c.reduced_formula:<10} "
              f"元素分数 = { {str(k): round(v, 4) for k, v in c.get_el_amt_dict().items()} }")
    print()
    print("  → get_el_amt_dict() 的输出正是第 4 讲 CBFV 特征化的输入。")

    # ② Lattice：晶格矢量
    print()
    print("② Lattice —— 三个晶格矢量，六维参数")
    print("-" * 78)
    lat = Lattice.cubic(4.0)
    print(f"  a = b = c = {lat.a:.2f} Å")
    print(f"  α = β = γ = {lat.alpha:.1f}°")
    print(f"  体积 = {lat.volume:.2f} Å³")
    print(f"  晶格矩阵 =\n{lat.matrix}")
    print()
    print("  → Lattice 自动校验合法性：三轴不可共线、体积非零。")
    print("  → 手工维护矩阵时，这些约束很容易被破坏。")

    # ③ Structure = Lattice + 分数坐标 + 元素
    print()
    print("③ Structure —— 晶格 + 原子坐标 + 元素")
    print("-" * 78)
    s = Structure(lattice=lat,
                  species=["Na", "Cl"],
                  coords=frac_coords)
    print(f"  组成        = {s.composition.reduced_formula}")
    print(f"  晶格常数a   = {s.lattice.a:.2f} Å")
    print(f"  体积        = {s.volume:.2f} Å³")
    print(f"  密度        = {s.density:.3f} g/cm³  （真实 NaCl = 2.165）")
    print(f"  原子数      = {len(s)}")
    print()
    print("  【坐标变换】同一个结构，换一套晶格，笛卡尔坐标随之改变：")
    for a in [4.0, 5.64]:
        s2 = Structure(lattice=Lattice.cubic(a), species=["Na", "Cl"],
                       coords=frac_coords)
        cart2 = frac_coords @ s2.lattice.matrix
        print(f"    a = {a:>4.2f} Å → 分数坐标不变，笛卡尔坐标 = "
              f"{np.round(cart2[1], 2)}，密度 = {s2.density:.3f} g/cm³")
    print()
    print("  → 这正是 pandas 无法表达的那层关系。")

    # ④ 对称性
    print()
    print("④ 对称性与最近邻 —— pymatgen 提供的现成能力")
    print("-" * 78)
    # 立方 NaCl 的正确构型（FCC 骨架）
    s_nacl = Structure(lattice=Lattice.cubic(5.64),
                       species=["Na", "Cl"],
                       coords=[[0, 0, 0], [0.5, 0.5, 0.5]])
    spg = s_nacl.get_space_group_info()
    print(f"  空间群 = {spg[0]}  ({spg[1]})")
    nn = s_nacl.get_neighbors(s_nacl[0], r=3.0)
    print(f"  Na的 3 Å 内邻居数 = {len(nn)}")
    print("  → 这些计算用 pandas + numpy 手写是极其困难的。")
    print("  → 第 5 讲的结构特征化（晶体图网络）正是建立在这些能力之上。")

    # ⑤ 结构匹配：识别等价结构
    print()
    print("⑤ StructureMatcher —— 判断两个结构是否本质相同")
    print("-" * 78)
    from pymatgen.analysis.structure_matcher import StructureMatcher
    sm = StructureMatcher()
    s_shift = Structure(lattice=Lattice.cubic(5.64),
                        species=["Cl", "Na"],
                        coords=[[0.5, 0.5, 0.5], [0.25, 0.25, 0.25]])
    s_rot = Structure(lattice=Lattice.cubic(5.64),
                      species=["Na", "Cl"],
                      coords=[[0.25, 0.25, 0.25], [0.5, 0.5, 0.5]])
    print(f"  结构A 与 结构B（原子互换+平移）是否匹配 = {sm.fit(s_nacl, s_shift)}")
    print(f"  结构A 与 结构C（仅平移）     是否匹配 = {sm.fit(s_nacl, s_rot)}")
    print()
    print("  → 不做这一步，同一材料会在你的数据集中出现多行【伪重复】，")
    print("    训练集与测试集相互污染，R² 会虚高。")

else:
    # 没有 pymatgen 时用纯 numpy 演示等价逻辑，保证脚本有教学输出
    print("（以下用纯 numpy 演示「等价结构」这一核心问题）")
    print()
    print("两个结构：原子顺序被交换，整体做了平移")
    A = np.array([[0.0, 0.0, 0.0], [0.5, 0.5, 0.5]])
    B = A[[1, 0]] + 0.25
    print(f"  A = {A.tolist()}")
    print(f"  B = {np.round(B, 3).tolist()}")
    print()
    print("  → 逐行比较：全不相同。")
    print("  → 但它们描述的是【同一个晶体】：只是原点和物种顺序不同。")
    print("  → pandas 眼中是两个样本，物理上是一个材料。")
    print("  → 这类伪重复会同时污染训练集与测试集，必须用StructureMatcher 处理。")

# =================================================================
# 第四部分　可视化：仓库对比 + 坐标变换
# =================================================================
print()
print("=" * 78)
print("第四部分　可视化")
print("=" * 78)

fig, axes = plt.subplots(1, 2, figsize=(14, 5.6))
fig.patch.set_facecolor('white')

# 图① 仓库多维对比雷达感：FAIR 得分 + 开放性
ax = axes[0]
short = ['MP', 'NOMAD', 'AFLOW', 'JARVIS', 'OQMD', 'MC', 'COD', 'ICSD']
fair_scores = [4, 5, 4, 3, 4, 5, 4, 3]
open_score = [5, 5, 5, 5, 5, 5, 5, 1]     # ICSD 收费→低
x = np.arange(len(short))
w = 0.38
ax.bar(x - w/2, fair_scores, w, label='FAIR / 溯源支持', color='#1E4FA8')
ax.bar(x + w/2, open_score, w, label='开放程度', color='#7FBF7F')
ax.set_xticks(x)
ax.set_xticklabels(short, fontsize=11)
ax.set_ylim(0, 6)
ax.set_ylabel('评分（1–5，定性评估）', fontsize=11)
ax.set_title('① 八个仓库的开放性与溯源能力', fontsize=13, fontweight='bold')
ax.legend(fontsize=9)
ax.grid(alpha=0.3, axis='y')
for xi, (f_, o_) in enumerate(zip(fair_scores, open_score)):
    ax.annotate(f'{f_}', (xi - w/2, f_), ha='center', va='bottom', fontsize=9)
    ax.annotate(f'{o_}', (xi + w/2, o_), ha='center', va='bottom', fontsize=9)

# 图② 晶格常数如何改变真实原子位置
ax = axes[1]
a_range = np.linspace(4.0, 6.2, 60)
dist = a_range * np.sqrt(3) / 2      # 体心对角线的一半
vol = a_range ** 3
dens = 4 * (22.99 + 35.45) / 6.022e23 / (vol * 1e-24)
ax.plot(a_range, dist, 'o-', color='#1E4FA8', linewidth=2, markersize=4,
        label='Na–Cl 距离 (Å)')
ax2 = ax.twinx()
ax2.plot(a_range, dens, 's--', color='#C62828', linewidth=2, markersize=4,
         label='密度 (g/cm³)')
ax.axvline(5.64, color='#2E7D32', linestyle=':', linewidth=2)
ax.annotate('真实 NaCl\na = 5.64 Å', (5.64, dist[np.argmin(np.abs(a_range - 5.64))]),
            fontsize=9, color='#2E7D32', xytext=(-58, 22),
            textcoords='offset points')
ax.set_xlabel('晶格常数 a (Å)', fontsize=11)
ax.set_ylabel('Na–Cl 距离 (Å)', fontsize=11, color='#1E4FA8')
ax2.set_ylabel('密度 (g/cm³)', fontsize=11, color='#C62828')
ax.set_title('② 分数坐标不变，物性随晶格完全改变', fontsize=13, fontweight='bold')
ax.grid(alpha=0.3)
h1, l1 = ax.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, fontsize=9, loc='lower right')

plt.tight_layout()
path2 = os.path.join(OUT_DIR, 'lec02_repos_and_structure.png')
plt.savefig(path2, dpi=150, bbox_inches='tight')
if os.environ.get('MPLBACKEND', '').lower() != 'agg':
    plt.show()   # 无头环境下自动跳过弹窗

print()
print("=" * 78)
print("第 2 讲示例（二）运行完成")
print("=" * 78)
print(f"图表已保存：{path2}")
if not HAS_PYMATGEN:
    print()
    print("提示：第三部分为纯 numpy 降级演示。安装 pymatgen 后重跑可看到")
    print("      真实的空间群、邻居搜索与 StructureMatcher 效果。")
print()
print("本讲要点回顾：")
print("  1. 选数据源要过『开放性 / 访问方式 / 策展 / 覆盖 / 类型 / FAIR』六问")
print("  2. 换库的直接成本是取数代码要重写——接口标准化的价值就在这里")
print("  3. 分数坐标离开晶格就没有物理意义，这是 pandas 的能力边界")
print("  4. 等价结构必须用 StructureMatcher 识别，否则训练集会自我泄漏")
