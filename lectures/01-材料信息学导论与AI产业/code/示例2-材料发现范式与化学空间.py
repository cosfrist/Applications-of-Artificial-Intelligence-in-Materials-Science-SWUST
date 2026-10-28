# -*- coding: utf-8 -*-
"""
第 1 讲 课内示例代码（二）：材料发现四范式与化学空白区
============================================================

对应 PPT：第 14 页（10¹² 化学空白区）、第 30 页（Stookey 碎玻璃）
          第 32–35 页（四种范式）、第 37 页（GNoME）
对应讲义：第三章「材料是如何被发现的」

本脚本的三个目的：
    ① 用可计算的方式理解「化学空间 10¹²」是怎么来的
    ② 定量对比四种发现范式的成本结构——为什么试错注定赢不了
    ③ 用数据说明「什么是有效关系」，以及它为什么可以直接从数据学到

运行：python 示例2-材料发现范式与化学空间.py
"""

import itertools
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os
from matplotlib.patches import FancyArrowPatch

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 图表统一输出到脚本同级的「输出」目录
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '输出')
os.makedirs(OUT_DIR, exist_ok=True)


# ════════════════════════════════════════════════════════════════════
# 第一部分：化学空间到底有多大——亲手算一遍
# ════════════════════════════════════════════════════════════════════

print("=" * 70)
print("第一部分：亲手计算化学空间的大小")
print("=" * 70)

# 步骤 1：统计常见元素数量
# 周期表中金属 + 类金属 + 非金属，约90 种在材料中被关注的元素
N_ELEMENTS = 89
print(f"\n考虑的元素种类数 N = {N_ELEMENTS}")

# 步骤 2：四元体系 A_a B_b C_c D_d
# 原讲义的条件：各组分质量分数 > 3%（忽略掺杂）
# 这意味着在一个体系中，最多只有 33 种组分能各占 3% 以上
MAX_COMPONENTS = int(100 / 3)   # = 33
print(f"每个体系中各组分质量分数 > 3%，故组分数上限 ≈ {MAX_COMPONENTS}")

# 步骤 3：估计可能的化学式数量（简化估算）
# 思路：先选 4 种元素，再考虑每个化学式中包含几种元素
combos_4 = itertools.combinations(range(N_ELEMENTS), 4)
n_4elem = sum(1 for _ in combos_4)
print(f"\n四元体系（恰好4 种元素）的组合数 C({N_ELEMENTS}, 4) = {n_4elem:,}")

# 但实际材料常含 1-6 种元素，覆盖多种元数
total = 0
print(f"\n按元数累加（每个体系内元素数可为 1 ~ 10）：")
for k in range(1, 11):
    n_k = 1
    for i in range(k):
        n_k *= (N_ELEMENTS - i)
    n_k //= k  # 去掉排列重复
    total += n_k
    print(f"  {k} 元体系：{n_k:>18,}")
print(f"\n合计（仅元素组合，不含配比）：{total:,}")

print(f"""
【重要说明】
上面算的是「元素组合数」，与讲义中 10^12 的口径不同。两者差别在于：

  · 讲义口径：四元化合物 AₐBᵦCᴄD₅，4 种元素各自取不同原子数，
    在「各组分 > 3%」约束下的相空间体积估计 ≈ 10^12
  · 本脚本口径：89 种元素中选 1~10 种的【组合数】，
    不含化学计量比，也不含晶体结构

注意本脚本累加到 10 元时结果已达 {total:.1e}（约 10^18），
远超讲义的 10^12——原因很简单：元素种类数一放开，
组合数按阶乘增长，10 元体系一家就占了 98% 以上。

这恰好说明问题的两面：
  · 即使用【最保守】的 10^12 口径，也已不可能枚举穷尽
  · 一旦放宽元数上限，实际规模还要再大好几个数量级

结论不变：这是一个【不可能靠枚举穷尽】的规模。
""")


# ════════════════════════════════════════════════════════════════════
# 第二部分：四种范式的成本结构——为什么试错赢不了
# ════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("第二部分：四种范式的成本结构")
print("=" * 70)

# 假设：要搜索 1% 的化学空间
SEARCH_TARGET = 1e12 * 0.01
print(f"\n假设目标：覆盖 1% 的化学空间 = {SEARCH_TARGET:.0e} 个候选\n")

# 参数：一次实验的成本（人时）
COST_PER_EXPERIMENT = 20          # 20 人时/次
SUCCESS_RATE_TRADITIONAL = 0.05   # 经验试错的成功率
SUCCESS_RATE_COMPUTATIONAL = 0.30 # 计算筛选的命中率

# 各个范式的「加速比」（相对纯实验）
paradigms = [
    {
        'name': '范式一：经验试错',
        'detail': '串行，命中即止',
        'throughput': 1.0,                    # 相对速度
        'hit_rate': SUCCESS_RATE_TRADITIONAL,
        'note': '速度最慢，成功率最低'
    },
    {
        'name': '范式二：理论计算',
        'detail': 'DFT 筛选后再实验',
        'throughput': 200.0,                  # DFT 比实验快约 200 倍
        'hit_rate': SUCCESS_RATE_COMPUTATIONAL,
        'note': '可解释，但算力昂贵'
    },
    {
        'name': '范式三：数据驱动',
        'detail': '模型直接预测，秒级',
        'throughput': 100000.0,               # 模型预测接近瞬时
        'hit_rate': SUCCESS_RATE_COMPUTATIONAL,
        'note': '覆盖能力最强，可解释性最弱'
    },
    {
        'name': '范式四：自主发现',
        'detail': 'BO 主动选点',
        'throughput': 5000.0,                 # 仍需真实实验，但每次实验信息量更高
        'hit_rate': 0.45,
        'note': '实验次数最少，但依赖自动化'
    },
]

print(f"{'范式':<20}{'相对速度':<14}{'命中率':<12}{'所需实验次数':<18}{'耗时(人时)'}")
print("-" * 80)
for p in paradigms:
    # 需要的「评估次数」= 目标 / (速度 × 命中率)
    n_eval = SEARCH_TARGET / (p['throughput'] * p['hit_rate'])
    # 真正需要的「成功实验数」近似为 1（找到目标为止）
    # 这里用「达到同等覆盖度所需的评估次数 × 单次成本」作为粗略对比
    total_hours = n_eval * (COST_PER_EXPERIMENT / 1000)  # 机器执行折算
    print(f"{p['name']:<22}{p['throughput']:>10,.0f}×{p['hit_rate']:>12.2f}"
          f"{n_eval:>16,.0f}{total_hours:>16,.0f}")

print(f"""
【解读】
注意最后两列的量级差异：
  · 范式三在「速度」上碾压其他三者
  · 但它不是要取代前两者，而是给它们加上「覆盖能力」

范式四的价值不在速度，而在【每次实验的信息量更大】：
  贝叶斯优化通过采集函数，有目的地选择信息量最大的实验点，
  而不是像随机采样那样盲目探索。
  → 这就是第 14 讲要讲的核心。
""")


# ════════════════════════════════════════════════════════════════════
# 第三部分：什么是「有效关系」——为什么可以直接从数据学到
# ════════════════════════════════════════════════════════════════════

print("=" * 70)
print("第三部分：数据能学到什么，学不到什么")
print("=" * 70)

# 演示一个经典的材料关系：带隙 vs 元素电负性
# 这是「有用但尚无简洁理论表述」的典型关系
print("\n【演示】带隙与平均电负性的关系")

data = {
    'formula':    ['Si', 'Ge', 'GaAs', 'GaN', 'ZnO', 'CdTe', 'CdS', 'InP', 'AlP', 'SiC'],
    'bandgap':    [1.12, 0.67, 1.42, 3.40, 3.37, 1.47, 2.42, 1.35, 2.45, 3.26],
    'electroneg': [2.20, 2.01, 2.45, 2.60, 2.30, 2.55, 2.50, 2.45, 2.20, 2.55],
}

print(f"{'化学式':<10}{'带隙(eV)':<12}{'平均电负性':<14}")
print("-" * 40)
for i in range(len(data['formula'])):
    print(f"{data['formula'][i]:<12}{data['bandgap'][i]:<14.2f}{data['electroneg'][i]:.2f}")

# 计算相关系数
x = np.array(data['electroneg'])
y = np.array(data['bandgap'])
r = np.corrcoef(x, y)[0, 1]
print(f"\nPearson 相关系数 r = {r:.3f}")
print(f"R² = {r**2:.3f}   ← 注意：这个值并不高，反而印证了下面的论点")

print(f"""
【这张图要说明什么】
带隙与平均电负性的整体相关性很弱（r={r:.3f}，R² 仅 {r**2:.2f}），
但它【不是一个通用规律】。

关键观察：
  · SiC (3.26 eV) 与 AlP (2.45 eV) 电负性几乎相同 (2.55 vs 2.20)，带隙却差很多
  · GaN (3.40) 和 GaAs (1.42) 平均电负性接近 (2.60 vs 2.45)，带隙差 2 倍

这说明：单一标量特征无法解释带隙。
必须引入更多维度：化学键性质、晶体对称性、能带结构路径……

这正是本课程第 4–5 讲要做的：
  从「一个特征」到「一组精心设计的特征」。
""")


# ════════════════════════════════════════════════════════════════════
# 第四部分：可视化——把上述结论画出来
# ════════════════════════════════════════════════════════════════════

fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle('第 1 讲：材料发现范式与化学空间（示意图）', fontsize=16,
             fontweight='bold', y=1.02)

# 图1：化学空间的数量级（对数轴）
ax = axes[0]
# 注：微软雅黑缺少上标数字的字形，直接写 10⁶ 会渲染成方框，
#     因此刻度标签统一用「10^n」形式，靠柱顶的 1e+06 标注给出精确量级。
scales = ['已知化合物', '元素组合数', '10^2 目标', '10^6', '10^9', '化学空间']
values = [3e6, 5e11, 1e2, 1e6, 1e9, 1e12]
colors = ['#2E7D32', '#6E9BDB', '#C3D5EE', '#C3D5EE', '#C3D5EE', '#C62828']
bars = ax.bar(range(len(scales)), values, color=colors, edgecolor='#0E3F8C')
ax.set_yscale('log')
ax.set_xticks(range(len(scales)))
ax.set_xticklabels(scales, rotation=30, ha='right', fontsize=9)
ax.set_ylabel('数量（对数刻度）', fontsize=11)
ax.set_title('① 化学空间：已知量只是极小一角', fontsize=13)
for b, v in zip(bars, values):
    ax.text(b.get_x() + b.get_width()/2, v*1.5, f'{v:.0e}',
            ha='center', fontsize=8, fontweight='bold')

# 图2：四范式的相对速度
ax = axes[1]
names = ['经验试错', '第一性原理', '数据驱动', '自主发现']
speeds = [1, 200, 100000, 5000]
colors2 = ['#B8C4D4', '#6E9BDB', '#0E3F8C', '#1E4FA8']
bars2 = ax.barh(names, speeds, color=colors2, edgecolor='#0E3F8C')
ax.set_xscale('log')
ax.set_xlabel('相对评估速度（对数刻度）', fontsize=11)
ax.set_title('② 相对速度对比', fontsize=13)
for b, v in zip(bars2, speeds):
    ax.text(v*1.3, b.get_y()+b.get_height()/2, f'{v:,}×',
            va='center', fontsize=9, fontweight='bold')

# 图3：带隙 vs 电负性——展示「单一特征不够」
ax = axes[2]
for i, f in enumerate(data['formula']):
    ax.scatter(data['electroneg'][i], data['bandgap'][i], s=80, color='#0E3F8C')
    ax.annotate(f, (data['electroneg'][i], data['bandgap'][i]),
                textcoords='offset points', xytext=(6, 4), fontsize=9)
z = np.polyfit(x, y, 1)
xs = np.linspace(1.9, 2.7, 50)
ax.plot(xs, np.polyval(z, xs), '--', color='#C62828', linewidth=2,
        label=f'线性拟合 R²={np.corrcoef(x,y)[0,1]**2:.2f}')
ax.set_xlabel('平均电负性', fontsize=11)
ax.set_ylabel('带隙 (eV)', fontsize=11)
ax.set_title('③ 单一特征的解释力有限', fontsize=13)
ax.legend(fontsize=9)

plt.tight_layout()
_out = os.path.join(OUT_DIR, 'lec01_paradigms.png')
plt.savefig(_out, dpi=150, bbox_inches='tight')
print(f"\n图表已保存为 {_out}")

if not matplotlib.get_backend().lower().startswith('agg'):
    plt.show()
else:
    plt.close()


# ════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("本讲要点回顾（第二部分）")
print("=" * 70)
print("""
1. 化学空间约 10¹²，已知化合物只是 10⁶ 量级——覆盖不了，穷举无望
2. 试错的成本结构决定了它注定无法主导发现过程
3. 第一性原理有解释力但算力昂贵
4. 数据驱动的价值是「覆盖能力」，不是取代其他三者
5. 自主发现（贝叶斯优化）的价值是「每次实验的信息量更大」
6. 单一标量特征解释力有限，必须构造多维特征——第 4–5 讲的核心任务

配套材料：
  · 本讲 PPT 第 30 页：Stookey 与碎玻璃的故事（发现常来自意外）
  · 本讲 PPT 第 35 页：四范式演进总览（叠加而非替代）
  · 讲义第三章：完整的范式对比与 GNoME 案例
""")


print("\n✅ 第 1 讲示例代码（二）运行完成")
print(f"   图表输出目录：{OUT_DIR}")