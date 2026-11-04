# -*- coding: utf-8 -*-
"""
第 2 讲 示例代码（一）：材料数据的真实形态与任务类型判定
================================================================

对应 PPT：第 06、07、08、19、22、23、24 页
对应讲义：第一章「机器学习任务类型」、第二章「材料数据的五个特点」

本脚本要回答三个问题：
  1. 同一份材料数据，套不同任务类型会得到什么完全不同的结论？
  2. 材料数据为什么「极度稀疏」——稀疏到什么程度？
  3. 标签口径不一致会带来多严重的后果？

全部数据取自常见的公开文献值，用于教学演示。
================================================================
"""

import os
import math

# Windows + MKL 下 KMeans 会出现内存泄漏告警，这里显式限制线程数
os.environ.setdefault('OMP_NUM_THREADS', '1')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import KMeans
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split, LeaveOneOut

# ── 中文显示与输出目录 ──
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '输出')
os.makedirs(OUT_DIR, exist_ok=True)

# =================================================================
# 第一部分　构造一份「像样」的材料数据
# =================================================================
# 教学数据集：III-V 族与部分氧化物半导体
# 带隙分两批口径：PBE 计算值（系统性偏低）与实验值
print("=" * 68)
print("第一部分　构造教学数据集")
print("=" * 68)

DATA = [
    # 化学式,   PBE计算带隙(eV), 实验带隙(eV), 离子半径差(pm), 电负性差, 极化率
    ("Si",        0.61, 1.12,  0,   0.00, 37.3),
    ("Ge",        0.02, 0.67,  0,   0.00, 40.5),
    ("GaAs",      0.30, 1.42,  8,   0.16, 52.0),
    ("GaN",       1.65, 3.40,  9,   0.29, 54.0),
    ("AlN",       4.20, 6.20,  8,   0.39, 39.0),
    ("InN",       0.35, 0.70, 25,   0.49, 65.0),
    ("AlAs",      1.45, 2.16,  9,   0.50, 39.0),
    ("AlSb",      1.28, 1.63, 14,   0.58, 44.0),
    ("GaSb",      0.16, 0.73, 12,   0.26, 52.0),
    ("InP",       0.65, 1.34, 26,   0.65, 65.0),
    ("InAs",      0.14, 0.35, 26,   0.30, 65.0),
    ("ZnO",       0.30, 3.37, 40,   1.66, 39.0),
    ("ZnS",       1.90, 3.60, 36,   1.14, 39.0),
    ("CdTe",      0.50, 1.50, 22,   0.55, 58.0),
    ("CdSe",      0.50, 1.74, 22,   0.63, 58.0),
    ("Ga2O3",     1.79, 3.30, 60,   1.80, 54.0),
]

df = pd.DataFrame(DATA, columns=[
    'formula', 'gap_pbe', 'gap_exp', 'radius_diff', 'chi_diff', 'polarizability'])

print(f"共 {len(df)} 条记录，字段：{list(df.columns)}")
print()
print(f"{'化学式':<10}{'PBE带隙':>10}{'实验带隙':>10}{'两者差':>10}")
print("-" * 68)
for _, r in df.iterrows():
    print(f"{r.formula:<10}{r.gap_pbe:>10.2f}{r.gap_exp:>10.2f}"
          f"{r.gap_exp - r.gap_pbe:>10.2f}")

diff = (df['gap_exp'] - df['gap_pbe']).mean()
std = (df['gap_exp'] - df['gap_pbe']).std()
print(f"\n→ PBE 系统性低估带隙：平均 {diff:.2f} eV，标准差 {std:.2f} eV")
print("→ 这个偏差非常稳定，正是它让『口径混用』成为隐患（第四部分会量化）")

# =================================================================
# 第二部分　同一个问题，任务类型不同，结论完全不同
# =================================================================
print()
print("=" * 68)
print("第二部分　任务类型决定一切")
print("=" * 68)

X = df[['radius_diff', 'chi_diff', 'polarizability']].values
y_cont = df['gap_exp'].values

print("【任务一】连续回归：预测实验带隙")
X_tr, X_te, y_tr, y_te = train_test_split(X, y_cont, test_size=0.3, random_state=0)
for name, model in [("线性回归", LinearRegression()),
                    ("随机森林", RandomForestRegressor(n_estimators=200, random_state=0))]:
    model.fit(X_tr, y_tr)
    pred = model.predict(X_te)
    print(f"  {name:<8} 测试集 R² = {r2_score(y_te, pred):>7.3f}   "
          f"MAE = {mean_absolute_error(y_te, pred):.3f} eV")
print("  → 三个简单描述符几乎无法解释带隙：R² 为负，说明不如直接取均值")
print("  → 这不是模型不够好，而是【特征信息量不足】——第 4–5 讲要解决的就是这个问题")

print()
print("【任务二】二分类：能否把带隙 > 2 eV 的材料挑出来（光伏候选筛选）")
y_bin = (y_cont > 2.0).astype(int)
print(f"  类别分布：正例(>2eV) {y_bin.sum()} 条 / 负例 {len(y_bin) - y_bin.sum()} 条")
print("  → 类别极不平衡时，准确率会骗人：全预测为负类也有 "
      f"{max(y_bin.sum(), len(y_bin) - y_bin.sum()) / len(y_bin):.0%} 准确率")
print("  → 因此材料分类任务几乎一定要看 F1 / ROC-AUC，而不是准确率（第 9 讲）")

print()
print("【任务三】无监督聚类：这些材料能分成几族？")
km = KMeans(n_clusters=3, n_init=10, random_state=0)
labels = km.fit_predict(X)
df['cluster'] = labels
# 按簇的平均带隙从低到高重编号，便于解读
order = (pd.DataFrame({'c': labels, 'g': y_cont})
         .groupby('c')['g'].mean().sort_values().index.tolist())
remap = {old: new for new, old in enumerate(order)}
df['cluster'] = df['cluster'].map(remap)
labels = df['cluster'].values

names_c = {0: '窄带隙族', 1: '中带隙族', 2: '宽禁带族'}
for c in range(3):
    sub = df[df['cluster'] == c]
    members = sub['formula'].tolist()
    print(f"  簇 {c}（{names_c[c]}，平均带隙 {sub['gap_exp'].mean():.2f} eV）："
          f"{'、'.join(members)}")
print()
print("  → 三个簇大致对应：窄带隙半导体 / 中带隙 / 宽禁带氧化物与氮化物")
print("  → 这个划分完全由【我选的三个描述符】决定：")
print("     换成别的特征，聚类结果会完全不同。")
print("  → 所以聚类结果必须再做【物理验证】，不能直接当结论用。")

print()
print("【任务四】排序：只需排出顺序，不要求数值准确")
# 按极化率排序，检验它与带隙的秩相关
from scipy.stats import spearmanr
rho, _ = spearmanr(df['polarizability'], df['gap_exp'])
print(f"  极化率排序 vs 实际带隙排序：Spearman ρ = {rho:.3f}")
print(f"  离子半径差排序 vs 实际带隙排序：Spearman ρ = "
      f"{spearmanr(df['radius_diff'], df['gap_exp'])[0]:.3f}")
print("  → 排序任务对特征的要求最低，一个粗糙特征也能给出有用的序")

# =================================================================
# 第三部分　材料数据为什么「极度稀疏」
# =================================================================
print()
print("=" * 68)
print("第三部分　化学空间稀疏性的定量估计")
print("=" * 68)

n_elements = 89   # 已知元素数，取保守估计
print(f"参与组合的元素数：{n_elements}（89 种已知元素）")

# 3) 仅按元素组合，不考虑计量比
#    组合数 C(89, k) 用组合公式直接算，【不要】用 itertools 枚举：
#    89 元体系的10 元组合数是 5.4×10^12，枚举会把内存耗尽。
combos = [math.comb(n_elements, k) for k in range(1, 11)]
total_combos = sum(combos)
print()
print(f"{'元素元数':<10}{'组合数':>18}{'占比':>12}")
print("-" * 68)
for k, c in enumerate(combos, 1):
    print(f"{k:<10} 元{c:>18,d}{c / total_combos:>11.2%}")
print("-" * 68)
print(f"{'合计':<10}{total_combos:>18,d}{1.0:>11.2%}")

print()
print(f"→ 仅【元素组合】这一个维度就已有 {total_combos:.3e} 种可能")
print("→ 而已知报道的无机化合物总数仅约 3 × 10^5 种")
ratio = 3e5 / total_combos
print(f"→ 覆盖率约 {ratio:.2e}，即平均每 {1 / ratio:.1e} 种组合中只有 1 种被研究过")

# 4) 再乘上常见计量比，量级会再放大
print()
print("考虑计量比后的进一步放大（每种组合取 ~10 种常见化学计量）：")
print(f"  {total_combos:.2e} × 10 ≈ {total_combos * 10:.2e}")
print("→ 再考虑结构多型（同成分不同晶格）、温度、压力……真正的化学空间")
print("  比上述任何保守估计都要大。这是【必须用机器学习】的根本原因。")

# =================================================================
# 第四部分　标签口径不一致的代价（可复现的经典实验）
# =================================================================
print()
print("=" * 68)
print("第四部分　标签口径混用会让模型学到什么")
print("=" * 68)

rng = np.random.default_rng(42)
n_total = 300

# 造一个「真实关系」：PBE 带隙 = f(特征)
true_pbe = (0.35 + 0.045 * rng.normal(0, 1, n_total)
            + 0.030 * rng.normal(0, 1, n_total) + rng.normal(0, 0.05, n_total))
true_pbe = np.clip(true_pbe, 0.0, None)

# 混入口径：前一半纯 PBE，后一半换成"实验值"（= PBE + ~1.0 eV）
mixed = true_pbe.copy()
half = n_total // 2
mixed[half:] = true_pbe[half:] + 1.05 + rng.normal(0, 0.08, n_total - half)

print(f"构造 {n_total} 条样本")
print(f"  · 前 {half} 条：PBE 口径")
print(f"  · 后 {n_total - half} 条：实验口径（系统性高约 1.05 eV）")
print(f"  · 全部样本的「特征-标签」真实规律完全相同")

# 测试集只用纯 PBE 口径
test_idx = np.arange(0, 30)             # 前30 条作为测试集
train_idx = np.arange(30, n_total)      # 其余作为训练集
half_train = np.arange(30, half)        # 训练集中的「PBE 口径」部分
rest_train = np.arange(half, n_total)   # 训练集中的「实验口径」部分

# 特征：全部样本共用一套，保证两个模型看到的输入完全相同
X_feat = rng.normal(0, 1, (n_total, 3))

results = {}
# 模型A：用【混用口径】的标签训练（模拟随手合并了两个来源的数据集）
mA = RandomForestRegressor(n_estimators=150, random_state=0)
mA.fit(X_feat[train_idx], mixed[train_idx])
# 模型B：只用【纯 PBE 口径】的那部分训练（模拟严格筛选过标签来源）
mB = RandomForestRegressor(n_estimators=150, random_state=0)
mB.fit(X_feat[half_train], true_pbe[half_train])

print(f"测试集：前 {len(test_idx)} 条，全部为纯 PBE 口径")
print(f"模型A 训练标签：{len(train_idx)} 条（混用口径）")
print(f"模型B 训练标签：{len(half_train)} 条（纯 PBE 口径）")
print()

for name, m in [("混用口径标签", mA), ("纯 PBE 口径标签", mB)]:
    # ① 在【纯 PBE 测试集】上评估：这才是对真实物理规律的检验
    r2_pure = r2_score(true_pbe[test_idx], m.predict(X_feat[test_idx]))
    # ② 在【与训练同分布的混合集】上评估：数字很好看
    r2_mixed = r2_score(mixed[train_idx], m.predict(X_feat[train_idx]))
    results[name] = (r2_pure, r2_mixed)

print(f"{'训练标签':<16}{'在纯PBE测试集 R²':>20}{'在混合集 R²':>14}")
print("-" * 68)
for k, (a, b) in results.items():
    # R² 可能因标签整体偏移而变得极负，只保留有限位小数便于阅读
    print(f"{k:<16}{a:>20.3f}{b:>14.3f}")
print("-" * 68)

a_pure, b_pure = results['混用口径标签'][0], results['纯 PBE 口径标签'][0]
a_mix, b_mix = results['混用口径标签'][1], results['纯 PBE 口径标签'][1]
print()
print(f"→ 在【同分布混合集】上：混用模型 {a_mix:.3f} vs 纯口径模型 {b_mix:.3f}")
print(f"→ 在【纯 PBE 测试集】上：混用模型 {a_pure:.3f} vs 纯口径模型 {b_pure:.3f}")
print()
print("→ 注意混用模型在纯 PBE 测试集上 R² 为大幅负值，这不是笔误：")
print("   混入口径后，模型学到的是【两套体系的平均规律】，对纯 PBE 样本")
print("   存在约 0.5 eV 的系统性高估。当标签方差远小于口径差时，")
print("   R² 可以变成极负值——这个数值本身就是「口径污染」的警报。")
print()
print("→ 关键结论：单一同分布测试集【无法发现口径污染】")
print("   （看混用模型在混合集上的 0.848，分数很漂亮），")
print("   只有【分层评估】才能暴露问题。")
print("→ 论文里报告的 R² 如果不说明标签口径，等于没有说明。")

# =================================================================
# 第五部分　小样本下的评估不可信（承接第 1 讲）
# =================================================================
print()
print("=" * 68)
print("第五部分　小样本评估：为什么不能只看一次划分")
print("=" * 68)

X_small = df[['radius_diff', 'chi_diff', 'polarizability']].values
y_small = df['gap_exp'].values

print(f"样本量仅 {len(y_small)} 条，测试集取 25% ≈ {int(len(y_small) * 0.25)} 条")
print()
print(f"{'随机种子':<12}{'训练R²':>10}{'测试R²':>12}{'测试MAE':>12}")
print("-" * 68)
test_scores = []
train_r2_list = []
for seed in [0, 1, 2, 42, 123]:
    Xa, Xb, ya, yb = train_test_split(X_small, y_small,
                                      test_size=0.25, random_state=seed)
    m = RandomForestRegressor(n_estimators=50, random_state=0)
    m.fit(Xa, ya)
    p = m.predict(Xb)
    r2t = r2_score(yb, p)
    r2tr = r2_score(ya, m.predict(Xa))
    test_scores.append(r2t)
    train_r2_list.append(r2tr)
    print(f"{seed:<12}{r2tr:>10.3f}{r2t:>12.3f}"
          f"{mean_absolute_error(yb, p):>12.3f}")
print("-" * 68)
print(f"测试集 R² 波动范围：{min(test_scores):.2f} ～ {max(test_scores):.2f}"
      f"（跨度 {max(test_scores) - min(test_scores):.2f}）")
print()
print(f"→ 训练集 R² 全部在 {min([r for r in train_r2_list]):.2f} 以上，")
print(f"   而测试集 R² 在 {min(test_scores):.2f} ～ {max(test_scores):.2f} 之间剧烈跳动，")
print(f"   最差的一次比直接取均值还差 {abs(min(test_scores)):.0f} 倍以上。")
print("→ 根因：测试集只有 4 条，R² 的分母（测试集标签方差）本身就很小，")
print("   个别样本的偏差会被放大成极大的负值。")
print("→ 结论：n < 30 时，【单次划分得到的任何指标都没有参考价值】。")
print("   这为第 8 讲的 LOCO 交叉验证埋下伏笔。")

# =================================================================
# 第六部分　可视化
# =================================================================
print()
print("=" * 68)
print("第六部分　可视化")
print("=" * 68)

fig, axes = plt.subplots(2, 2, figsize=(13.5, 9.5))
fig.patch.set_facecolor('white')

# 图① 两种口径的带隙对比
ax = axes[0][0]
ax.plot(df['gap_pbe'], df['gap_exp'], 'o', color='#1E4FA8',
        markersize=8, label='化合物')
lo, hi = 0, df['gap_exp'].max() + 0.5
ax.plot([lo, hi], [lo, hi], '--', color='#C62828', linewidth=1.5,
        label='理想一致线')
ax.set_xlabel('PBE 计算带隙 (eV)', fontsize=11)
ax.set_ylabel('实验带隙 (eV)', fontsize=11)
ax.set_title('① 两种口径系统性偏差约 1 eV', fontsize=13, fontweight='bold')
ax.legend(fontsize=9)
ax.grid(alpha=0.3)
for _, r in df.iterrows():
    if r.gap_exp > 3:
        ax.annotate(r.formula, (r.gap_pbe, r.gap_exp),
                    fontsize=8, xytext=(3, 3), textcoords='offset points')

# 图② 化学空间的稀疏性
ax = axes[0][1]
ks = list(range(1, 11))
ax.bar(ks, combos, color='#C3D5EE', edgecolor='#0E3F8C', alpha=0.85, width=0.7)
ax.set_yscale('log')
ax.set_ylim(50, 3e13)
ax.set_xlabel('元素元数', fontsize=11)
ax.set_ylabel('组合数（对数刻度）', fontsize=11)
ax.set_title('② 化学空间：已知化合物只是极小一角', fontsize=13, fontweight='bold')
ax.set_xticks(ks)
for k, c in zip(ks, combos):
    ax.annotate(f'{c:.1e}', (k, c), fontsize=7.5, ha='center',
                xytext=(0, 5), textcoords='offset points', rotation=90)
ax.grid(alpha=0.3, which='both', axis='y')
ax.axhline(3e5, color='#C62828', linestyle='--', linewidth=1.5)
ax.annotate('已知化合物约 3×10⁵', (10.4, 3e5), fontsize=9, color='#C62828',
            va='center', ha='right', xytext=(-4, 9), textcoords='offset points')

# 图③ 任务类型对比
ax = axes[1][0]
names = list(results.keys())
pure = [results[n][0] for n in names]
mixd = [results[n][1] for n in names]
xp = np.arange(len(names))
w = 0.36
b1 = ax.bar(xp - w/2, pure, w, label='在纯 PBE 测试集', color='#1E4FA8')
b2 = ax.bar(xp + w/2, mixd, w, label='在混合集（同分布）', color='#E8A33D')
for bars in (b1, b2):
    for b in bars:
        h = b.get_height()
        # 极端负值压缩显示，避免把坐标轴拉变形
        shown = max(h, -3.2)
        ax.annotate(f'{h:.2f}' if abs(h) < 10 else f'{h:.0f}',
                    (b.get_x() + b.get_width() / 2, shown),
                    ha='center', va='bottom' if h >= 0 else 'top',
                    fontsize=9, fontweight='bold')
ax.axhline(0, color='#666666', linewidth=1)
ax.set_ylim(-4, 1.15)
ax.set_xticks(xp)
ax.set_xticklabels(names, fontsize=10)
ax.set_ylabel('R²', fontsize=11)
ax.set_title('③ 标签口径污染：同分布评测会掩盖问题', fontsize=13,
             fontweight='bold')
ax.legend(fontsize=9)
ax.grid(alpha=0.3, axis='y')
ax.annotate('混用模型在混合集上 0.848，\n看起来「很准」——但真实规律上 R² = -68',
            xy=(0.2, 0.848), xytext=(0.52, 0.60), fontsize=9.5,
            color='#B8860B', ha='left',
            bbox=dict(boxstyle='round,pad=0.4', fc='#FFF7E0', ec='#FFE9B0'),
            arrowprops=dict(arrowstyle='->', color='#B8860B', lw=1.5))

# 图④ 小样本评估波动
ax = axes[1][1]
seeds = [0, 1, 2, 42, 123]
train_r2 = []
test_r2 = []
for seed in seeds:
    Xa, Xb, ya, yb = train_test_split(X_small, y_small,
                                      test_size=0.25, random_state=seed)
    m = RandomForestRegressor(n_estimators=50, random_state=0)
    m.fit(Xa, ya)
    train_r2.append(r2_score(ya, m.predict(Xa)))
    test_r2.append(r2_score(yb, m.predict(Xb)))
xs = np.arange(len(seeds))
ax.bar(xs - 0.18, train_r2, 0.34, label='训练集 R²', color='#1E4FA8')
ax.bar(xs + 0.18, test_r2, 0.34, label='测试集 R²', color='#C62828')
for x, v in zip(xs - 0.18, train_r2):
    ax.annotate(f'{v:.2f}', (x, v), ha='center', va='bottom', fontsize=9)
for x, v in zip(xs + 0.18, test_r2):
    ax.annotate(f'{v:.1f}', (x, max(v, -14.6)), ha='center',
                va='bottom' if v >= 0 else 'top', fontsize=9,
                fontweight='bold', color='#C62828', clip_on=False)
ax.axhline(0, color='#666666', linewidth=1)
ax.set_ylim(-16, 1.6)
ax.set_xticks(xs)
ax.set_xticklabels([str(s) for s in seeds])
ax.set_xlabel('随机种子', fontsize=11)
ax.set_ylabel('R²', fontsize=11)
ax.set_title('④ n=16 时，测试指标完全不可信\n（纵轴已截断，最低一次实际为 -33.0）',
             fontsize=12, fontweight='bold')
ax.legend(fontsize=9, loc='lower right', framealpha=0.95)
ax.grid(alpha=0.3, axis='y')

plt.tight_layout()
path1 = os.path.join(OUT_DIR, 'lec02_tasks_and_sparsity.png')
plt.savefig(path1, dpi=150, bbox_inches='tight')
if os.environ.get('MPLBACKEND', '').lower() != 'agg':
    plt.show()   # 无头环境下自动跳过弹窗

print()
print("=" * 68)
print("第 2 讲示例（一）运行完成")
print("=" * 68)
print(f"图表已保存：{path1}")
print()
print("本讲要点回顾：")
print("  1. 任务类型不是风格选择，而是由【标签形态】决定的硬约束")
print(f"  2. 材料数据极度稀疏：约 {total_combos:.1e} 的元素组合"
      f" vs 约 3×10^5 已知化合物")
print("  3. 标签口径混用是隐蔽的错误来源，单一同分布测试集发现不了")
print("  4. n < 30 时单次划分的评估结果没有参考价值")
print()
print("→ 下一讲：真正把数据取回来、洗干净、看明白")
