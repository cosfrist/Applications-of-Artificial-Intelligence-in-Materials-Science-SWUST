# -*- coding: utf-8 -*-
"""
第 1 讲 课内示例代码（一）：材料信息学的数据起点
==================================================

对应 PPT：第 5讲（银幕 vs 实验室）、第 8 讲（MI 定义）、第 9 讲（材料科学四面体）
对应讲义：第一章「什么是材料信息学」

本脚本的目的不是讲语法，而是让你亲眼看到：
    ① 材料数据的真实形态——它长什么样、有多少、有多脏
    ② 为什么「直接丢给模型」是行不通的
    ③ 材料信息学与通用机器学习的第一个分岔点在哪里

运行前准备：
    pip install pymatgen pandas numpy matplotlib
    （若要访问 Materials Project 联网 API，还需 pip install mp-api 并申请 API key）
"""

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import os
from collections import Counter

# 中文显示设置（若报错可注释掉，不影响代码逻辑）
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 图表统一输出到脚本同级的「输出」目录，避免污染源码目录
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '输出')
os.makedirs(OUT_DIR, exist_ok=True)


# ════════════════════════════════════════════════════════════════════
# 第一部分：用一个真实的小数据集认识「材料数据是什么」
# ════════════════════════════════════════════════════════════════════

print("=" * 70)
print("第一部分：材料数据的真实形态")
print("=" * 70)

# 这是一个公开的、带隙数据小样本（可在讲义配套数据中替换为自己的数据）
# 字段说明：
#   formula  —— 化学式
#   bandgap  —— 带隙（eV），这是我们想预测的「性质」
#   nelem    —— 含有的元素种类数
#   volume   —— 晶胞体积（Å³）
#   spacegroup —— 空间群编号（对称性的编码方式）
data = pd.DataFrame({
    'formula':   ['Si', 'Ge', 'GaAs', 'GaN', 'ZnO', 'CdTe', 'CdS', 'InAs',
                  'AlP', 'AlAs', 'GaP', 'InP', 'SiC', 'TiO2', 'ZnS', 'CdSe'],
    'bandgap':   [1.12, 0.67, 1.42, 3.40, 3.37, 1.47, 2.42, 0.36,
                  2.45, 2.16, 2.24, 1.35, 3.26, 3.00, 3.60, 1.74],
    'nelem':     [1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    'volume':    [40.9, 82.0, 181.0, 46.6, 47.6, 68.7, 56.3, 79.3,
                  49.9, 57.2, 52.9, 61.3, 21.0, 62.5, 83.5, 84.1],
    'spacegroup':[227, 227, 216, 186, 186, 216, 216, 216,
                  216, 216, 216, 216, 186, 136, 216, 216]
})

print(f"\n数据集规模：{len(data)} 条样本")
print("\n—— 请注意这个数字 ——")
print("材料信息学的数据集通常 n < 1000，很多时候只有几十条。")
print("深度学习在这个量级几乎无法工作。\n")

print("前5 行预览：")
print(data.head().to_string(index=False))
print("\n各列的数据类型：")
print(data.dtypes.to_string())


# ════════════════════════════════════════════════════════════════════
# 第二部分：材料数据的「脏」——为什么不能直接丢给模型
# ════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("第二部分：材料数据为什么是「脏」的")
print("=" * 70)

# 问题 1：化学式是字符串，模型不认识它
print("\n【问题1】化学式是字符串")
print("'GaAs' 这样的字符串，模型无法直接计算。")
print("必须把它转成数字向量 —— 这个过程叫【特征化】，是第 4 讲的内容。")
print(f"  化学式示例：{data['formula'].iloc[0]}  （类型：{type(data['formula'].iloc[0]).__name__}）")

# 问题 2：缺失值在材料数据中极为常见
print("\n【问题2】缺失值")
missing_data = data.copy()
missing_data.loc[2, 'bandgap'] = np.nan      # 带隙缺失
missing_data.loc[5, 'volume'] = np.nan      # 体积缺失
print(f"  缺失值统计：\n{missing_data.isnull().sum().to_string()}")
print("材料数据的缺失往往有原因：")
print("  · 某些性质的计算本身就容易失败（收敛问题）")
print("  · 某些体系不适合用某种方法表征")
print("  · 实验数据因为仪器问题没测出来")
print("  → 缺失往往【不是随机的】，直接删除会引入偏差")

# 问题 3：异常值可能是最有价值的数据
print("\n【问题3】异常值")
print("在通用机器学习里，异常值通常当噪声删掉。")
print("但在材料场景中，异常值恰恰可能是【新材料】所在之处。")
outlier_idx = data['bandgap'].idxmax()
print(f"  带隙最大的样本：{data.loc[outlier_idx, 'formula']}"
      f"（{data.loc[outlier_idx, 'bandgap']} eV）")
print("  它是噪声吗？不一定。它可能正是我们要找的材料。")

# 问题 4：量纲与尺度不一致
print("\n【问题4】量纲问题")
print(f"  带隙范围：{data['bandgap'].min()} – {data['bandgap'].max()} eV")
print(f"  体积范围：{data['volume'].min()} – {data['volume'].max()} Å³")
print("  体积比带隙大两个数量级。若不缩放，模型会被体积主导。")
print("  → 这就是为什么第 8 讲讲指标时，R² 在跨量纲问题上会骗人")


# ════════════════════════════════════════════════════════════════════
# 第三部分：可视化先行——本课程的固有方法论
# ════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("第三部分：可视化先行")
print("=" * 70)
print("本课程的方法论第一条：任何算法上桌之前，先把数据画出来看。\n")

fig, axes = plt.subplots(2, 2, figsize=(13, 9))
fig.suptitle('第 1 讲：材料数据长什么样（示例数据集 n=16）',
             fontsize=16, fontweight='bold', y=0.98)

# 图1：带隙分布——观察是否长尾、是否有异常
ax = axes[0, 0]
ax.hist(data['bandgap'], bins=8, color='#8FB4E4', edgecolor='#0E3F8C')
ax.axvline(data['bandgap'].mean(), color='#C62828', linestyle='--',
           label=f"均值 {data['bandgap'].mean():.2f}")
ax.set_xlabel('带隙 (eV)', fontsize=12)
ax.set_ylabel('样本数', fontsize=12)
ax.set_title('① 带隙分布：半导体集中在两个「甜区」，中间是禁区', fontsize=13)
ax.legend(fontsize=10)
print("""
  从这张分布能读出一条真实的材料规律：
  带隙并非连续分布，而是在1.0 eV 附近与 3.5 eV 附近形成两个聚集区，
  中间 1.5–2.5 eV 一带明显稀疏。
  · 1.0 eV 附近：直接带隙半导体，适合光伏吸收
  · 3.5 eV 附近：宽禁带半导体，适合紫外探测、功率器件
  · 中间地带反而少有稳定材料
  这不是采样偏差，而是化学成键的物理后果——
  它也意味着「造一个带隙 2.0 eV 的稳定材料」本身就是难题。
""")

# 图2：带隙 vs 体积——看是否有物理关联
ax = axes[0, 1]
for _, row in data.iterrows():
    c = '#C62828' if row['nelem'] == 1 else '#0E3F8C'
    m = 'o' if row['nelem'] == 1 else 's'
    ax.scatter(row['volume'], row['bandgap'], c=c, marker=m, s=70)
ax.set_xlabel('晶胞体积 (Å³)', fontsize=12)
ax.set_ylabel('带隙 (eV)', fontsize=12)
ax.set_title('② 带隙 vs 体积：红圆=单质，蓝方=化合物', fontsize=13)

# 图3：元素种类数——材料数据的「异质性」直观体现
ax = axes[1, 0]
nelem_counts = Counter(data['nelem'])
ax.bar(list(nelem_counts.keys()), list(nelem_counts.values()),
       color='#6E9BDB', edgecolor='#0E3F8C')
ax.set_xlabel('含元素种类数', fontsize=12)
ax.set_ylabel('样本数', fontsize=12)
ax.set_title('③ 元素种类分布：材料数据的分组天然不均衡', fontsize=13)
ax.set_xticks(list(nelem_counts.keys()))

# 图4：特征相关性——注意只有 3 个数值特征可用
ax = axes[1, 1]
corr = data[['bandgap', 'nelem', 'volume', 'spacegroup']].corr()
im = ax.imshow(corr, cmap='RdBu_r', vmin=-1, vmax=1)
ax.set_xticks(range(len(corr)))
ax.set_yticks(range(len(corr)))
ax.set_xticklabels(corr.columns, rotation=45, ha='right', fontsize=9)
ax.set_yticklabels(corr.columns, fontsize=9)
for i in range(len(corr)):
    for j in range(len(corr)):
        ax.text(j, i, f'{corr.iloc[i, j]:.2f}', ha='center', va='center', fontsize=9)
ax.set_title('④ 特征相关性矩阵（可用的数值特征太少）', fontsize=13)
plt.colorbar(im, ax=ax, fraction=0.046)

plt.tight_layout()
_out = os.path.join(OUT_DIR, 'lec01_data_overview.png')
plt.savefig(_out, dpi=150, bbox_inches='tight')
print(f"\n图表已保存为 {_out}")

if not matplotlib.get_backend().lower().startswith('agg'):
    plt.show()
else:
    plt.close()


# ════════════════════════════════════════════════════════════════════
# 第四部分：特征化的必要性——把化学式变成向量
# ════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("第四部分：为什么必须做特征化")
print("=" * 70)

import re

ELEMENTS = ['H', 'B', 'C', 'N', 'O', 'F', 'Al', 'Si', 'P', 'S',
            'Ti', 'Ga', 'Ge', 'As', 'Se', 'Zn', 'Cd', 'In', 'Sn', 'Te']

# 把化学式按「元素符号 + 可选数字」解析成真实的元素列表。
# 注意：不能直接用 `el in formula` 做子串匹配——
#   'S' in 'Si'为真（Si 里并没有 S）
#   'C' in 'CdTe' 为真（CdTe 里并没有 C）
# 那是字符串包含判断，不是化学式解析。
def parse_formula(formula):
    """返回化学式中出现的元素符号列表，如 'CdTe' -> ['Cd', 'Te']。"""
    return re.findall(r'([A-Z][a-z]?)', formula)


def formula_to_simple_features(formula):
    """
    把化学式转成一个【最简单】的数值向量。
    这不是 CBFV（第 4 讲的内容），只用来演示「字符串→数字」的必要性与基本思路。

    思路：统计该化合物中含有哪些预设元素（存在性指示变量）。
    """
    present = set(parse_formula(formula))
    return [1.0 if el in present else 0.0 for el in ELEMENTS]


# 先自检解析逻辑，避免「子串匹配」这类隐蔽错误混进教学
_CASES = {'Si': {'Si'}, 'CdTe': {'Cd', 'Te'}, 'GaAs': {'Ga', 'As'},
          'SiC': {'Si', 'C'}, 'TiO2': {'Ti', 'O'}, 'AlP': {'Al', 'P'}}
for _f, _want in _CASES.items():
    _got = set(parse_formula(_f))
    assert _got == _want, f'化学式解析错误: {_f} -> {_got}（应为 {_want}）'
print("化学式解析自检通过（6/6）")

print("\n最简单的特征化：元素存在性向量（20 维）")
print("这个方法很粗糙——它无法区分 NaCl 和 KCl，但足以说明问题。")
print("为便于阅读，下面只列出每个样本【命中的元素编号】及其向量维度：\n")

X_simple = np.array([formula_to_simple_features(f) for f in data['formula']])

print(f"{'化学式':<10}{'命中元素':<22}{'1 的个数':<10}{'向量维度'}")
print("-" * 70)
for i in range(len(data)):
    hit = [f"{ELEMENTS[j]}({j})"
           for j, v in enumerate(X_simple[i]) if v == 1.0]
    print(f"{data['formula'].iloc[i]:<10}{', '.join(hit):<22}"
          f"{int(X_simple[i].sum()):<10}{len(X_simple[i])}")

print("\n现在数据可以被模型处理了：X 的形状 =", X_simple.shape)
print(f"  {X_simple.shape[0]} 个样本 × {X_simple.shape[1]} 个特征")

# 绝大多数维度都是 0——稀疏性问题
density = X_simple.mean()
print(f"\n  注意特征矩阵的密度（0 的占比）：仅 {density*100:.1f}% 的位置是 1，"
      f"{100-density*100:.1f}% 是 0。")
print("  16 个样本要撑起 20 维特征空间，每个样本平均只提供 "
      f"{X_simple.sum(axis=1).mean():.1f} 个非零信息。")
print("  → 维度数已经超过样本量，这是小数据场景的典型困境。")

# 但这个特征化有个严重问题——演示一下
print("\n【警告】这种特征化有个致命缺陷：")
print("  Si（硅）与 Ge（锗）在这个表示下都是「只含一个元素」——")
print("  向量长度相同、都只有一个 1，模型看不出任何差别；")
print("  但两者带隙差别巨大（1.12 vs 0.67 eV）。")
print("  原因：这个表示只记录【有没有】，不记录【元素的性质】。")
print("\n  → 解决方案：CBFV、oliynyk 描述符、mat2vec 嵌入")
print("  → 这正是第 4 讲要解决的问题。")


# ════════════════════════════════════════════════════════════════════
# 第五部分：小数据的真实困境——演示随机划分的陷阱
# ════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("第五部分：小数据的真实困境")
print("=" * 70)

from sklearn.model_selection import train_test_split, LeaveOneOut, KFold
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error

# 用随机森林做一次最简单的预测，只为演示评估问题，不追求效果
y = data['bandgap'].values
X_full = np.column_stack([X_simple, data[['nelem', 'volume', 'spacegroup']].values])

print(f"\n数据规模 n = {len(y)}")

# ── 陷阱演示：单次划分的结果完全取决于运气 ──
print("\n【演示】同一个模型、同一个数据，单次划分的结果波动极大：")
print(f"{'随机种子':<10}{'训练集R²':<12}{'测试集 R²':<12}{'测试集MAE'}")
print("-" * 50)
test_r2 = []
for seed in [0, 1, 2, 42, 123]:
    X_tr, X_te, y_tr, y_te = train_test_split(
        X_full, y, test_size=0.25, random_state=seed)
    model = RandomForestRegressor(n_estimators=50, random_state=0)
    model.fit(X_tr, y_tr)
    pred = model.predict(X_te)
    test_r2.append(r2_score(y_te, pred))
    print(f"{seed:<12}{r2_score(y_tr, model.predict(X_tr)):<14.3f}"
          f"{r2_score(y_te, pred):<14.3f}{mean_absolute_error(y_te, pred):.3f}")

print(f"\n  → 测试集 R² 在 {min(test_r2):.2f} 到 {max(test_r2):.2f} 之间波动，跨度 {max(test_r2)-min(test_r2):.2f}。")
print("  → 同一份数据、同一套特征，换个随机种子就可能得到「很好」或「比瞎猜还差」的结果。")
print("  → 结论：在 n<30 时，单次划分的结果【没有任何参考价值】。")

# ── 正确做法：交叉验证 ──
print("\n【正确做法】用留一交叉验证（LOO-CV）替代单次划分：")
loo = LeaveOneOut()
loo_scores = []
for tr, te in loo.split(X_full):
    m = RandomForestRegressor(n_estimators=30, random_state=0)
    m.fit(X_full[tr], y[tr])
    loo_scores.append(y[te][0] - m.predict(X_full[te])[0])
loo_errors = np.array(loo_scores)

print(f"  LOO-CV 平均绝对误差 MAE = {np.abs(loo_errors).mean():.3f} eV")
print(f"  误差标准差 = {np.abs(loo_errors).std():.3f} eV")
print(f"  最大单点误差 = {np.abs(loo_errors).max():.3f} eV")
print(f"  最小单点误差 = {np.abs(loo_errors).min():.3f} eV")
print("\n  → 这才是可信的评估。注意误差的标准差与均值同量级，")
print("    说明【单点预测的不确定性很大】，这在材料场景是常态。")

# 找出预测最差的样本
worst = np.argmax(np.abs(loo_errors))
print(f"\n  预测最差的样本：{data['formula'].iloc[worst]}"
      f"（真实 {y[worst]:.2f} eV，预测 {y[worst] - loo_errors[worst]:.2f} eV）")
print("  → 为什么会差？提示：看第 2 讲的数据模态选择。")

print("\n" + "=" * 70)
print("本讲要点回顾")
print("=" * 70)
print("""
本脚本演示的五件事，对应本讲的核心论断：

1. 材料数据规模小（n<1000），深度学习不适用
2. 材料数据是「脏」的：缺失有原因，异常值可能是目标
3. 化学式是字符串，必须特征化才能进入模型
4. 粗糙的特征化会丢信息（Si vs Ge 的例子）
5. 单次划分的结果完全不可信，必须用交叉验证

这五条共同指向一个结论：材料信息学不是「把ML 用到材料上」，
它需要的是一套针对小数据、异质模态、重外推场景的完整方法论——
这正是本课程 16 讲要交付的东西。

下一讲预告：机器学习任务类型与材料数据生态
""")


print("\n✅ 第 1 讲示例代码（一）运行完成")
print(f"   图表输出目录：{OUT_DIR}")