# code/环境验收/ · 冻结核心（只由保护入口调用）

本目录是第 1 讲课堂预检的**冻结科学核心**，三件字节固定：

| 文件 | 字节 | SHA256 |
|---|---:|---|
| `环境验收.py` | 6875 | `1e47550633f8742ab21e2a530beff7ce746b626988e551b3483586d1e70a05c0` |
| `带隙小样本.csv` | 475 | `b089f06ebde74ee9257c8a4b2d99d519407ea7ef18d727d4c5a1a315b71b74e0` |
| `输出/lec1_env_check.svg` | 5074 | `7685277e46c85811199a6e1b579db8d537c9545bb3f9cfc007ff053dee7f11d8` |

> 这三个文件**不要直接在本目录运行或覆盖**：`环境验收.py` 的 `summary/all` 在 Windows 默认 GBK
> 控制台会因 `↔` 触发编码错误；`--step figure` 会覆盖本目录既有的示例 SVG。
> 课堂统一使用包根的保护入口 `code/运行预检-V5.py`：它把核心与 CSV 复制到一个**全新输出目录**的
> `work/` 下再运行，源文件不改、旧输出不覆盖。

## 课堂入口（在包根执行，普通 python）

```bat
python "code/运行预检-V5.py" --out "学生运行/首次预检"
```

四步单跑（**每一步各用一个全新目录**）：

```bat
python "code/运行预检-V5.py" --out "学生运行/1-读取"   --step read
python "code/运行预检-V5.py" --out "学生运行/2-换算"   --step summary
python "code/运行预检-V5.py" --out "学生运行/3-结果图" --step figure
python "code/运行预检-V5.py" --out "学生运行/4-版本"   --step version
```

- 结果图在 `3-结果图/work/输出/lec1_env_check.svg`，不是本目录的 `输出/`。
- 只允许包根下全新目录；拒绝已存在目录、包根本身、`code/`、`课程导论/`、`assets/`、
  `学生分发-V5/` 与包外路径（exit 2）。
- 单步只核该步真实输出；`figure`/`all` 才核对新 SVG。冻结核心、CSV、既有示例 SVG 原字节不改。

## 它验证什么 / 不验证什么

- 验证：能读 CSV（12 行 × 5 列，`bandgap_J` 缺 6 行）、能核对 eV↔J（6 条，最大偏差约
  0.000638 eV）、能生成 SVG、能登记 Python 与平台版本。
- 不验证：numpy / pandas / scikit-learn / matplotlib / pymatgen 是否可用；课程依赖按
  《MICourse 课前环境清单》另行验收。本页预检不另加 2 分，正式过程任务卡 2 分在第 2 讲完整卡评价。

## 数据口径

`带隙小样本.csv` 的数值为教学取整样例，只用于检查「能读、能算、能存图、能记版本」，
不作数据引用，也不等同 NOMAD 的 379 条记录。图与脚本输出均带「教学取整数据，仅用于流程演示」。
