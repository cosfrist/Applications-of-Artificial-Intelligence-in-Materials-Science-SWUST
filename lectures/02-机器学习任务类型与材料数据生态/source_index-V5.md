# 第 2 讲 源清单（V5）

> **2026-11-06 文件信息更新**：当前教师PPT为 **60页**，5,268,177 B，SHA256 `0b0e2d0369c2ae08219b9f96f071a7c1bfb2f0fbc1c2d5fdafb33c52132b42d3`。
> 当前60页可见文字和备注与仓库上版相同；本轮P7/P12为图片或版式XML变化。讲义/路线保留。学生副本和ZIP未更新。
> 本次只核对主件字节、结构、页码和文件记录；未重新进行整讲科学/原生逐页视觉验收，旧包与旧验收结论不代表当前主件。

> 当前手动课件的逐页来源；历史图片处理记录保留作溯源，实际嵌入身份与尺寸见末节。本次未重做论文来源或版权核验。

## 一、版本与基线

| 项 | 值 |
|---|---|
| V4 课件（冻结） | `85c588042520f843d666381d890c1530746ba186cba8b301f1834a7b9c6f5b8c`（60 页，2 800 026 B） |
| 旧长讲义（未改） | `aee9ee8c15ffd63781855b337d59d8c310f70d04b5c85b35ad6493b48ded00b6`（38 076 B） |
| 当前V5课件 | `0b0e2d0369c2ae08219b9f96f071a7c1bfb2f0fbc1c2d5fdafb33c52132b42d3`（60页；当前手动版） |
| 第1讲当前入口 | 见课程总交付索引；原50c86eb3…接受属于历史字节，不作为当前手动版接受 |
| 第 3 讲快照（包外） | `课件/第3讲 数据获取处理与剖析/code/mp_be_snapshot.csv`，379 行 7 列 |

## 二、逐页来源

| 页 | 类型 | 文字依据 | 图片 |
|---|---|---|---|
| P1 | 必讲·封面 | 课程信息：1012680110，2学分/32学时，16讲；V5授课计划第2讲（G1/G2，实践20分钟）；仓库URL依当前封面。 | 页眉Logo、课程二维码/仓库入口以实际嵌入元数据为准 |
| P2 | 必讲·导航 | 页码按本地 PDF 实核：ISLP §2.1.4 PDF39（印刷25）、§2.1.5 PDF41（p27）、§2.2.1 PDF42 起（p28—30/PDF42—44）；Zhang §11.1 PDF374（p364）。论文：Jain, A.; Ong, S. P.; Hautier, G.; Chen, W.; Richards, W. D.; Dacek, S.; Cholia, S.; Gunter, D.; Skinner, D.; Ceder, G.; Persson, K. A. "Commentary: The Materials Project: A materials genome approach to accelerating materials innovation", APL Materials 1, 011002 (2013), DOI 10.1063/1.4812323；机构公开 PDF https://escholarship.org/content/qt3h26p692/qt3h26p692.pdf（13 页含封面；Fig.1 在 PDF 第 4 页 / 论文 011002-2）。MP 官方：https://docs.materialsproject.org/downloading-data/using-the-api/querying-data 与 https://docs.materialsproject.org/frequently-asked-questions（数据许可 CC BY 4.0，版本/日期以查询当日为准）。 | —（仅页眉 Logo） |
| P3 | 必讲·路线 | V5 授课计划第 2 讲：15 讲授 + 20 实践 + 25 选源 + 20 异构 + 10 基线 = 90；必讲 24 页，其余为补充/课后阅读。 | —（仅页眉 Logo） |
| P4 | 必讲 | 课程自编任务卡模板；示例阈值（按批次留出 20%、MAE ≤ 1.5 个百分点）为教学约定，不是材料学通用阈值；PCE 协议写明 AM1.5G、温度、面积与 MPP 稳态口径；工艺前时点的可得/不可得见 P50。 | —（仅页眉 Logo） |
| P5 | 补充 | 课程自编；经典经验规律为教科书内容。图取自原课程沿用的犹他大学 MSE5540/6640 讲义（历史素材）。 | —（仅页眉 Logo） |
| P6 | 补充 | 拟合图为犹他大学 MSE5540/6640 讲义 7 的历史示意（原始数据与拟合参数未在本轮复核）；带隙—电负性“没有通用解析模型”指缺少跨体系通用式，特定体系仍有经验式。 | 1 张（419×372，历史讲义示意） |
| P7 | 必讲 | 分类树为犹他大学课程讲义历史图；文字按 Settles/Levine 等通行定义改写，离线强化学习参考 Levine et al. (2020), arXiv:2005.01643。 | 1 张（577×247，历史分类树） |
| P8 | 必讲 | 课程自编；指标定义为教科书内容；ISLP §2.1.5（p27/PDF41）用于区分回归与分类。 | —（仅页眉 Logo） |
| P9 | 必讲 | 课程自编对照表；“工艺参数是决策变量”按优化问题定义改写；光谱反演按输入—输出口径改写。 | —（仅页眉 Logo） |
| P10 | 补充 | 课程自编；方法定义为教科书内容。 | —（仅页眉 Logo） |
| P11 | 补充 | 聚类、密度、投影三图取自 MaterialsInformatics/course_notes/7. Machine learning tasks and types.pdf 第 9 页（Utah MSE5540/6640 课程讲义；原图可能为第三方，版权未核）；本轮从该页重裁三个完整面板，替换 V4 中裁切不全的版本；KMeans 三迭代图沿用 V4（完整，来源未逐页核）。 | 4 张（本轮重裁 cluster / density / projection，KMeans 沿用） |
| P12 | 补充 | 截图为 Machine Learning Mastery 博文（J. Brownlee, 2019-11-11, https://machinelearningmastery.com/types-of-learning-in-machine-learning/）；本地原课程讲义 7 第 8 页含完整版（至第 14 项 Ensemble Learning）；版权未核，课程内使用，对外公开或录制前需替换或取得许可。 | 1 张（本轮重裁完整十四类截图，已去底部半截 URL） |
| P13 | 补充 | 组合数 ΣC(89,k), k=1..10 = 5 798 786 177 163（本机标准库复算）；代价为量级估计，随体系、机时与测试条件变化，不作实测统计。 | —（仅页眉 Logo） |
| P14 | 补充 | 课程自编归纳；方法名按教科书与 scikit-learn 官方术语。 | 1 张（595×397，八种补救全景） |
| P15 | 补充 | 课程自编；离线 RL 参考 Levine et al. (2020), arXiv:2005.01643；材料实例为公开研究方向，不引用具体性能数字。 | 2 张（217×203 / 289×203） |
| P16 | 补充 | 定义按 scikit-learn 官方说明 https://scikit-learn.org/stable/modules/semi_supervised.html；半监督算法流程图为犹他大学讲义 7 历史素材。 | 1 张（287×410，半监督流程图） |
| P17 | 补充 | 课程自编；条件生成的自监督判定按“目标是否由输入构造”这一标准改写；预训练—微调范式见第 12 讲。 | 1 张（552×202，自监督循环图） |
| P18 | 补充 | 课程自编；MIL 定义与 OR 假设参考 Ilse, Tomczak & Welling (2018), PMLR 80。 | —（仅页眉 Logo） |
| P19 | 补充 | 课程自编；三分类为统计学习通行的认识论划分；右图为 stacking 集成示意，中图为训练集规模示意，均不当作演绎推理或归纳机制图；直推边界按“可用目标域未标注 X、不得看目标 y”限定。 | 3 张（左：三类推理三角图，已清理页边；中：训练集规模；右：stacking 集成示意） |
| P20 | 补充 | 策略命名按 Settles 报告 §3 https://burrsettles.com/pub/settles.activelearning.pdf；“本讲不跑代码”为 V5 限定。 | 1 张（485×262，主动学习闭环） |
| P21 | 补充 | 课程自编；两维度对照为课程归纳，漂移只是可能情形。 | —（仅页眉 Logo） |
| P22 | 补充 | 课程自编；左图为公开计算库与单一任务样本的量级示意（历史图，口径不同，不引用具体条数）。 | 2 张（245×235 / 232×235） |
| P23 | 补充 | 课程自编；方法定义为教科书内容。 | —（仅页眉 Logo） |
| P24 | 补充 | 课程自编；偏差—方差为教科书内容。 | 1 张（496×401，集成组合图） |
| P25 | 分隔 | 课程自编。 | —（仅页眉 Logo） |
| P26 | 必讲 | 课程自编；与 V5 大纲“数据语义与可信评估”一致。 | —（仅页眉 Logo） |
| P27 | 必讲 | MP Querying Data（material_id / band_gap / structure / origins / run_type）https://docs.materialsproject.org/downloading-data/using-the-api/querying-data；NOMAD glossary https://docs.nomad-lab.eu/reference/glossary.html；各仓库公开文档；条目数不声称当前规模，也不以某一快照日期为依据。 | —（仅页眉 Logo） |
| P28 | 必讲 | 课程自编；尺度划分为材料科学通行框架。 | —（仅页眉 Logo） |
| P29 | 必讲 | 组合数同 P13（5 798 786 177 163）；“失败→MNAR”改为需检验的条件判断；组合数与记录数相除只说明口径错误，不当作探索程度。 | —（仅页眉 Logo） |
| P30 | 必讲 | Rubin (1976), Biometrika 63(3), 581—592, DOI 10.1093/biomet/63.3.581（缺失机制定义）；MCAR/MAR/MNAR 为教科书内容；不把“未测”直接判为 MCAR、不把“失败”直接判为 MNAR。 | —（仅页眉 Logo） |
| P31 | 必讲 | 课程自编；泛函与带隙类型为教科书内容；教学标签偏移为示例设定。 | —（仅页眉 Logo） |
| P32 | 补充 | 课程自编；三条红线与第 8 讲分组验证衔接；不建立“材料比图像/文本更难”的领域难度二分。 | —（仅页眉 Logo） |
| P33 | 分隔 | 课程自编。 | —（仅页眉 Logo） |
| P34 | 补充 | 课程自编；历史叙述为概述；图为原课程历史素材。 | 2 张（476×268 / 464×268，历史照片） |
| P35 | 补充 | 图为犹他大学讲义 5 历史素材；分类说明为课程归纳。 | 1 张（1084×506，八门类图） |
| P36 | 必讲 | 课程自编；FAIR 原则为公开框架。 | 1 张（671×328，六问图） |
| P37 | 必讲 | 课程自编；NOMAD 条款 https://about.nomad-lab.eu/terms.html（内容 CC BY 4.0、元数据 CC0）；Matbench 仓库 https://github.com/materialsproject/matbench 与 Dunn et al. (2020) DOI 10.1038/s41524-020-00406-3；COD https://www.crystallography.net/cod（CC0）；各库许可以官方文档为准。 | —（仅页眉 Logo） |
| P38 | 补充 | 课程自编；标准名与用途为公开文档概述。 | 1 张（560×241，互操作标准） |
| P39 | 补充 | 图为犹他大学讲义 5 历史素材；开放性与覆盖为图示信息，不代表当前各库状态。 | 2 张（545×258，开放性与覆盖对比） |
| P40 | 必讲 | MP Querying Data 与 FAQ；Matbench 仓库 https://github.com/materialsproject/matbench 与 Dunn et al. (2020), DOI 10.1038/s41524-020-00406-3；不引用具体条数。 | —（仅页眉 Logo） |
| P41 | 补充 | 图为犹他大学讲义 5 历史素材；具体访问与许可逐库核对（见 P42）。 | 1 张（1071×506，资源清单图） |
| P42 | 必讲 | MP Querying Data 与 FAQ（CC BY 4.0）；Jain et al. (2013), APL Materials 1, 011002, DOI 10.1063/1.4812323；COD https://www.crystallography.net/cod（CC0）；NOMAD 条款 https://about.nomad-lab.eu/terms.html；Matbench 仓库与 Dunn et al. (2020) DOI 10.1038/s41524-020-00406-3；其余逐库官方来源，未核处明确标注。 | —（仅页眉 Logo） |
| P43 | 补充 | 课程自编；API/批处理为通行工程实践，不引用具体限额。 | —（仅页眉 Logo） |
| P44 | 分隔 | 课程自编。 | —（仅页眉 Logo） |
| P45 | 补充 | pymatgen 官方 Structure 序列化接口（https://pymatgen.org/pymatgen.core.html 的 Structure.as_dict/from_dict）；分工原则为课程方案。 | —（仅页眉 Logo） |
| P46 | 补充 | pymatgen 官方文档（https://pymatgen.org）；表述按“常用/事实标准”限定。 | 1 张（397×293，pymatgen 文档首页） |
| P47 | 必讲 | pymatgen 官方对象定义：https://pymatgen.org/pymatgen.core.html（Composition / Lattice / Structure）；空间群与基元关系为晶体学教科书内容；图模型表述按课程方案限定。 | —（仅页眉 Logo） |
| P48 | 分隔 | 课程自编。 | —（仅页眉 Logo） |
| P49 | 补充 | 课程自编教学案例；结构图为通用 ABX3 示意；不引用未核的带隙窗口数字。 | 1 张（320×296，ABX3 结构示意） |
| P50 | 必讲 | 课程自编；PCE 协议与测试条件为领域通行描述，不引用具体器件数据；时点定义与 P4 一致；光伏效率与测量口径参考 NREL https://www.nrel.gov/pv/cell-efficiency.html。 | —（仅页眉 Logo） |
| P51 | 必讲 | 课程自编；PCE 定义为光伏领域通行式（Pin 为入射辐照功率密度，面积基准须与 Jsc 一致）；稳态 MPP 与扫描 J–V 是两套协议，分别记录；NREL https://www.nrel.gov/pv/cell-efficiency.html。 | —（仅页眉 Logo） |
| P52 | 分隔 | 课程自编。 | —（仅页眉 Logo） |
| P53 | 补充 | 课程自编；与 P3—P31 一致；“优先级”为课程建议，不是领域排名。 | —（仅页眉 Logo） |
| P54 | 补充 | 课程自编；与 P26—P31 对应。 | —（仅页眉 Logo） |
| P55 | 必讲 | 第 3 讲 code/mp_be_snapshot.csv 实测 379 行 7 列；band_gap 单位 eV、density 单位 g/cm³；MP Querying Data；Matbench 仓库 https://github.com/materialsproject/matbench 与 Dunn et al. (2020) DOI 10.1038/s41524-020-00406-3；COD https://www.crystallography.net/cod（CC0）；许可以原数据为准，课程分发不改变原数据许可。 | —（仅页眉 Logo） |
| P56 | 补充 | 课程术语表；定义按教科书与 scikit-learn 官方术语；直推边界按本讲 P19 口径限定。 | —（仅页眉 Logo） |
| P57 | 补充 | 课程术语表；FAIR 与 MCAR/MAR/MNAR 为公开框架/教科书定义。 | —（仅页眉 Logo） |
| P58 | 必讲·实践 | 课程自编；V5 授课计划第 2 讲 20 分钟独立实践；任务卡模板见 P4。 | —（仅页眉 Logo） |
| P59 | 必讲 | 课程自编；数据泄漏与管线见 scikit-learn 官方文档；第 8 讲系统展开分组验证。 | —（仅页眉 Logo） |
| P60 | 必讲·小结 | 课程自编；节点：HW1 第 3 讲发布、第 6 讲截止；项目第 8 讲立项；本讲只登记选题意向。 | —（仅页眉 Logo） |

## 三、图片处理与许可状态

| 图 | 本轮处理 | 来源（本地页） | 新文件 SHA256 |
|---|---|---|---|
| P11 聚类 | 重裁完整面板（含标题与右侧 Cluster 1—4） | `MaterialsInformatics/course_notes/7. Machine learning tasks and types.pdf` p9 | `5af65340beada4630a93ca6a5e8e12c21b45c93c777a9721001d3bc6c75b8848` |
| P11 密度 | 重裁完整面板（含标题、色标、坐标轴） | 同上 p9 | `ca3d378b448ed9539ae3c9b94ff5be78332f8f6956b46a934ae49f09b432f8fd` |
| P11 投影 | 重裁完整面板（含 Projection 标题） | 同上 p9 | `51dee4938f7e3ec74ecafcebf0ebda0998e6dfc3290d1a947abdeaa6104fe082` |
| P12 十四类 | 重裁完整截图（至第 14 项 Ensemble Learning），去掉底部半截 URL | 同上 p8（网页截图，原博文 2019-11-11） | `3c567a55467033e42a41c9ae802094ac776a2a47eb8eca884b056281b0d8510f` |
| P19 左图 | 清理顶部青色页边与底部相邻面板 A/B 图标，保留完整归纳/演绎/直推三角图 | 原 V4 课程图（历史素材，原图可能为第三方） | `11c4448cba7acc7e47d3326bc1d2823ef70417a0f981e50361843a1884cc5f8a` |

- P11 的 KMeans 三迭代图与除 P19 左图外的其余页图片沿用 V4，未替换、未拉伸、未裁切。
- 历史图来自原课程沿用的 Utah MSE5540/6640 讲义与网页截图，未核到具体馆藏与许可；课程内使用，**对外公开或录制课程前需替换或取得许可**。
- P12 截图原博文：https://machinelearningmastery.com/types-of-learning-in-machine-learning/ （J. Brownlee, 2019-11-11）；本地只保存重裁图，不分发原文。

## 四、本讲已核事实

| 项 | 核验方式 |
|---|---|
| ISLP §2.1.4 / §2.1.5 / §2.2.1 位置 | 本地 PDF 实读：PDF39（印刷25）、PDF41（p27）、PDF42 起（p28—30/PDF42—44） |
| Zhang §11.1 位置 | 本地 PDF 实读：PDF374（p364）开头 |
| Jain 2013 题名/作者/卷/文章号/DOI | 出版者页面与 DOI 实核：APL Materials 1, 011002, 10.1063/1.4812323；机构 PDF 13 页含封面、Fig.1 在 PDF4 / 011002-2 按任务书核验记录；本机 curl 该机构 PDF 返回 403，未作本地视觉复核 |
| MP 数据许可 | 官网 Terms/Citing：CC BY 4.0；版本/日期以查询当日为准 |
| MP 字段与泛函 | Querying Data：material_id / band_gap / structure / origins / run_type；summary 一行是材料汇总 |
| NOMAD 条款 | https://about.nomad-lab.eu/terms.html：内容 CC BY 4.0，元数据 CC0 |
| COD 许可 | https://www.crystallography.net/cod：数据与数据库 CC0，使用时致谢原始作者 |
| Matbench | https://github.com/materialsproject/matbench；Dunn et al. (2020), DOI 10.1038/s41524-020-00406-3；标签按任务定义，并非统一重算 |
| pymatgen 对象 | https://pymatgen.org/pymatgen.core.html（Composition / Lattice / Structure） |
| 缺失机制 | Rubin (1976), Biometrika 63(3), 581—592, DOI 10.1093/biomet/63.3.581 |
| 化学空间组合数 | 标准库复算 ΣC(89,k), k=1..10 = 5 798 786 177 163 ≈ 5.80×10¹² |
| 第 3 讲快照 | `mp_be_snapshot.csv`：379 行 7 列（formula/band_gap/density/energy_above_hull/symmetry/spg_number/entry_id） |

## 五、未核与限制

- 历史图未逐张核版权与原始数据；不作为当前规模或实测结论。P11/P12 只重裁本地讲义已有页面，不重画科学图。
- 本讲不引用各仓库当前条数：规模随版本变化，以查询当日官网为准。
- Jain 机构 PDF 本机下载 403；13 页/Fig.1 位置按任务书与 Codex 核验记录写入，未声称本地视觉核。
- 器件 PCE 的示例阈值与协议为教学约定，不是材料学通用标准；不引用具体器件效率数据。
- 旧示例脚本与旧输出为历史材料，不在 V5 包内；其缺陷与修订史只留私有 diff 与 `code/README.md` 短入口，不作为当前科学结论。

## 六 当前主文件嵌入元数据

当前课件有91个图片对象、32个唯一媒体SHA；其中60个高频页眉/标识对象另计。下表仅为嵌入文件元数据，不代表新增事实、出处或许可核验。

|页|实际嵌入part|SHA256前12位|像素|显示尺寸(in)|裁切srcRect|
|---|---|---|---|---|---|
|P1|`ppt/media/image2.jpeg`|`536b0c218d68`|1260×2344|3.240×4.488|{}|
|P1|`ppt/media/image3.png`|`9ee0f2472136`|1700×619|3.241×1.181|{}|
|P6|`ppt/media/image4.png`|`32efd34c42f7`|419×372|4.365×3.875|{}|
|P7|`ppt/media/image5.png`|`c9e7d38ae01d`|3464×1451|7.046×2.951|{}|
|P11|`ppt/media/image6.png`|`de5bc6f5a88f`|446×158|4.646×1.646|{}|
|P11|`ppt/media/image7.png`|`5af65340bead`|1312×956|2.000×1.458|{}|
|P11|`ppt/media/image8.png`|`ca3d378b448e`|1080×956|1.646×1.458|{}|
|P11|`ppt/media/image9.png`|`51dee4938f7e`|936×984|1.385×1.458|{}|
|P12|`ppt/media/image10.png`|`3c567a554670`|3728×1784|8.927×4.271|{}|
|P14|`ppt/media/image11.png`|`387aa1485136`|595×397|6.198×4.135|{}|
|P15|`ppt/media/image12.png`|`ff2f32474d74`|216×202|2.260×2.115|{"l": "15", "r": "15"}|
|P15|`ppt/media/image13.png`|`fd4385e01258`|288×202|3.010×2.115|{"l": "73", "r": "73"}|
|P16|`ppt/media/image14.png`|`03283c5b5164`|287×410|2.990×4.271|{}|
|P17|`ppt/media/image15.png`|`82cde977c486`|551×202|5.750×2.104|{"t": "90", "b": "90"}|
|P19|`ppt/media/image16.png`|`36b01b00c824`|280×271|2.927×2.833|{"l": "5", "r": "5"}|
|P19|`ppt/media/image17.png`|`698220ad834a`|288×272|3.000×2.833|{}|
|P19|`ppt/media/image18.png`|`11c4448cba7a`|325×271|3.396×2.833|{}|
|P20|`ppt/media/image19.png`|`accc5502e283`|484×261|5.052×2.729|{"l": "87", "r": "87"}|
|P22|`ppt/media/image20.png`|`8a1ca8f65690`|244×234|2.552×2.448|{"l": "8", "r": "8"}|
|P22|`ppt/media/image21.png`|`aa1ad3112c73`|232×234|2.417×2.448|{"l": "212", "r": "212"}|
|P24|`ppt/media/image22.png`|`5b95f80c55e0`|496×401|5.167×4.177|{}|
|P34|`ppt/media/image23.png`|`801960e27e6b`|475×267|4.958×2.792|{"l": "81", "r": "81"}|
|P34|`ppt/media/image24.png`|`34bff08f20ea`|463×267|4.833×2.792|{"l": "78", "r": "78"}|
|P35|`ppt/media/image25.png`|`9767595a5ab6`|1084×506|11.292×5.271|{}|
|P36|`ppt/media/image26.png`|`028af8fb9894`|671×328|6.990×3.417|{}|
|P38|`ppt/media/image27.png`|`11068465df6a`|806×396|5.833×2.510|{"t": "6203", "b": "6203"}|
|P39|`ppt/media/image28.png`|`446c1938d9fa`|544×258|5.677×2.688|{"t": "91", "b": "91"}|
|P39|`ppt/media/image29.png`|`738848adc43d`|544×258|5.677×2.688|{"t": "91", "b": "91"}|
|P41|`ppt/media/image30.png`|`e21d161cdf62`|1069×505|11.156×5.271|{"l": "5", "r": "5"}|
|P46|`ppt/media/image31.png`|`8b9c75bf78b0`|397×293|4.135×3.052|{}|
|P49|`ppt/media/image32.png`|`4898f68af884`|319×295|3.333×3.083|{"l": "12", "r": "12"}|
