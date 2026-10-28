# 第 1 讲 源清单（V5）

> 逐页记录文字依据与图片情况；图片为原课程讲义沿用的历史素材，本轮未替换、未逐张核到版权页。

## 一、版本与基线

| 项 | 值 |
|---|---|
| V4 课件（冻结） | `047c38fb691dfad572833f1fce8152c4861caaf40e1dc51914f2da8eee344b70`（60 页） |
| V5 课件 | 见 `SHA256-清单-V5.md` |
| 旧长讲义（历史） | `ef49d9dbfc2a6258399c400abe869c07a7475277b017a54749d07fd0c23ff4a5` |
| 课程导论（已验收，未改） | `e60c1027bed4f1e5f60de33a5d59eec688c979b46dd98f9dc32c67a6dbb5f11b` |
| V5 大纲 / 计划（已验收，未改） | `07de4ebf687f15af8f595c972574e6e1367a3d36903374f46224fb618902fecd` / `6e5e90f55b130a5be4eb9f38d45acb56e753d61d5b5d8897e7bb580bc300b1e6` |

## 二、逐页来源

| 页 | 类型 | 文字依据 | 图片 |
|---|---|---|---|
| P1 | 必讲·封面 | 课程信息：1012680110，2 学分 / 32 学时，8 周 × 每周 4 学时，16 讲；开课单位与授课教师按 V5 课程基本信息。 | —（仅页眉 Logo） |
| P2 | 必讲·导航 | ISLP 2023 Python 版页码按本地 PDF 目录核对（§2.1.1 PDF 31 起、§2.2.1 PDF 42 起、§2.3 PDF 54 起）；R1 = Zhang, The Elements of Machine Learning（英文版，2025/2026 订正）第 1 章；CGCNN：Tian Xie & Jeffrey C. Grossman (2018), “Crystal Graph Convolutional Neural Networks for an Accurate and Interpretable Prediction of Material Properties”, Phys. Rev. Lett. 120, 145301, DOI 10.1103/PhysRevLett.120.145301；GNoME：Merchant, Batzner, Schoenholz, Aykol, Cheon & Cubuk (2023), “Scaling deep learning for materials discovery”, Nature 624, 80–85, DOI 10.1038/s41586-023-06735-9。 | —（仅页眉 Logo） |
| P3 | 必讲·路线 | V5 授课计划第 1 讲（35/20/15/15/5 = 90）；详细必讲/补充页清单见《授课路线-V5.md》。 | —（仅页眉 Logo） |
| P4 | 分隔页（补充） | 课程自编。 | —（仅页眉 Logo） |
| P5 | 补充 | 课程自编；观点性对比，不引用具体影片或产品性能。 | 3 个图标（装饰） |
| P6 | 补充 | 课程自编；PINN 的损失构成见第 15 讲与 Raissi 等 2019 的框架（本讲不展开推导）；符号主义/学习主义的划分按教材通行说法，不把数值计算等同于符号推理。 | —（仅页眉 Logo） |
| P7 | 补充 | 课程自编；Google 翻译的规则系统到神经方法的演进作为公开常识举例，不引用具体指标。 | —（仅页眉 Logo） |
| P8 | 必讲 | Materials Informatics is data science applied to materials science —— Taylor D. Sparks, University of Utah（课程引用的定义）。 | —（仅页眉 Logo） |
| P9 | 必讲 | 材料科学通行的「结构—工艺—性质—性能」框架；课程自绘示意图。 | —（仅页眉 Logo） |
| P10 | 补充 | Krishna Rajan (2005), “Materials informatics”, Materials Today 8(10), 38–45, DOI 10.1016/S1369-7021(05)71123-8（出版者条目 https://www.sciencedirect.com/science/article/pii/S1369702105711238）；该文为 Review Feature（综述特稿），不宣称其亲自完成某个未核的金属玻璃发现；旧引文「Rajan et al., Comput. Mater. Sci. 2005」归属未核，已不再使用；Hall–Petch 式仅作对照。 | 1 张（187×200，原刊首页扫描） |
| P11 | 补充 | Gaultois et al. 2013 Chem. Mater.；Gaultois et al. 2016 APL Mater.；Ghadbeigi et al. 2016 Energy Environ. Sci.；Sparks et al. 2016 Scripta Mater.（原课程讲义引用，未逐篇核对全文，按历史示例处理）。 | —（仅页眉 Logo） |
| P12 | 补充 | Hall–Petch 关系为教科书内容；ZT 散点为原课程整理的历史数据（教学示意），本页不据此给新材料结论。 | 2 张（368×344 / 397×344） |
| P13 | 补充 | Materials Genome Initiative for Global Competitiveness, 2011（美国 NSTC 文件，公开文本）。 | 1 张（340×379） |
| P14 | 补充 | 课程自编；MGI 白皮书中「materials genome」的用法作为对照。 | —（仅页眉 Logo） |
| P15 | 补充 | 课程自编；成本结构为定性描述，不引用具体金额。 | —（仅页眉 Logo） |
| P16 | 补充 | 本页自算组合数（Σ_{k=1..10} C(89,k) = 5 798 786 177 163 ≈ 5.80×10¹²；标准库独立核验 sum(math.comb(89,k) for k in range(1,11))）；与 htwins.net/scale2 的 10¹² 口径不同，不混用、不相除。 | —（仅页眉 Logo） |
| P17 | 必讲 | Al 7075 为既有牌号（1943 年商业化，公开冶金史）；本页是教学回溯案例，不声称新发现。 | 1 张（281×250） |
| P18 | 补充 | 课程自编；不引用具体市场规模数字。 | 2 张（278×210 / 353×210） |
| P19 | 补充 | 原课程整理的历史统计（教学示意）；未核到单一原始数据源，按历史素材处理，不作当前结论。 | 1 张（320×400） |
| P20 | 分隔页（补充） | 课程自编。 | —（仅页眉 Logo） |
| P21 | 必讲 | 课程自编对照表；表中「10²—10³」指本课程聚焦的样本量级，不是全领域统计。 | —（仅页眉 Logo） |
| P22 | 必讲 | 课程自编；ISLP 第 2 章关于偏差—方差与样本量的讨论作为方法论背景。 | 1 张（285×240） |
| P23 | 必讲 | 课程自编；外推与验证协议的对应关系见第 8 讲。 | —（仅页眉 Logo） |
| P24 | 必讲 | 课程自编；第 3 讲会给出 MP/NOMAD 字段与单位对照的具体例子。 | —（仅页眉 Logo） |
| P25 | 必讲 | 课程自编；噪声与均值估计误差、模型不确定性的区分见第 13 讲（GP 后验与噪声项）。 | —（仅页眉 Logo） |
| P26 | 补充 | 课程自编；CBFV、周期图与图表示分别在第 4、5 讲；表示比较的同协议要求见第 8 讲。 | —（仅页眉 Logo） |
| P27 | 必讲 | 课程自编；SHAP/PDP 的边界见第 9 讲；PINN 的检验要求见第 15 讲。 | —（仅页眉 Logo） |
| P28 | 必讲 | 课程自编；LOCO = leave-one-cluster-out（留一簇），见第 8 讲；六维为课程组织口径，不作领域分类学。 | —（仅页眉 Logo） |
| P29 | 必讲 | 课程自编教学案例；不引用具体数据库条数；划分与应用目标的对应见第 8 讲。 | —（仅页眉 Logo） |
| P30 | 补充 | 课程自编示意图；不引用具体模型的精度数字；不把「学习必然牺牲可读性」当普遍结论。 | —（仅页眉 Logo） |
| P31 | 补充 | 课程自编；与 V5 大纲「内容结构」一致；原课程选用资源见《覆盖矩阵》，已按本课 16 讲重组。 | —（仅页眉 Logo） |
| P32 | 分隔页（补充） | 课程自编。 | —（仅页眉 Logo） |
| P33 | 补充 | Corning《The History of Corning Innovation》1952 年条目 https://www.corning.com/cala/en/innovation/culture-of-innovation/the-history-of-corning-innovation.html ；Corning《Glass Heroes》https://www.corning.com/worldwide/en/innovation/the-glass-age/inspiration/glass-heroes.html ；离子交换化学强化为另一项独立技术，不并入本页。 | 0 张（原肖像已移除；左卡为可编辑三步观察卡） |
| P34 | 补充 | Corning 官方创新史（1952 年条目）与公开材料史常识；页面不引用未核细节。 | 3 张历史照片（300×188 / 286×190 / 192×190） |
| P35 | 补充 | 课程自编分类；与页面五张卡一一对应。 | —（仅页眉 Logo） |
| P36 | 补充 | 课程自编；DFT 的适用范围与局限见第 15 讲。 | —（仅页眉 Logo） |
| P37 | 补充 | 课程自编；候选与验证的区分见第 8 讲与第 10 讲。 | —（仅页眉 Logo） |
| P38 | 补充 | 课程自编；BO 的采集函数与离线回放协议见第 14 讲；具体平台案例见第 15 讲与课程导论案例页。 | —（仅页眉 Logo） |
| P39 | 补充 | 课程自编；以第 15 讲的自驱动实验室讨论为准。 | 2 张（480×320） |
| P40 | 必讲 | 课程自编；与导论 P7—P16 十例的「证据层级」一致。 | —（仅页眉 Logo） |
| P41 | 补充 | DeepMind 官方博客《Highly accurate protein structure predictions with AlphaFold》（2020-11-30）；Jumper et al., Highly accurate protein structure prediction with AlphaFold, Nature 596, 583–589 (2021), DOI 10.1038/s41586-021-03819-2。 | 1 张（620×339） |
| P42 | 必讲 | 课程自编归纳；四例分别对应 AlphaFold2（结果 2020 / 论文 2021）、GNoME（2023）、MatterGen（2025）与自驱动实验室；GNoME 的候选口径见 P43 与原文。 | —（仅页眉 Logo） |
| P43 | 必讲 | Merchant et al., Scaling deep learning for materials discovery, Nature 624, 80–85 (2023), DOI 10.1038/s41586-023-06735-9；凸包与相图口径见 Materials Project 官方方法文档 https://docs.materialsproject.org/methodology/materials-methodology/thermodynamic-stability/phase-diagrams-pds 与 Bartel et al., Nat. Commun. 9, 4168 (2018), DOI 10.1038/s41467-018-06682-4。 | 1 张（368×245） |
| P44 | 补充 | 课程自编；历史叙述为概述，不引用未核史料。 | —（仅页眉 Logo） |
| P45 | 分隔页（补充） | 课程自编。 | —（仅页眉 Logo） |
| P46 | 补充 | 原课程整理的企业名单（历史素材，未逐家核实现状）；课堂按补充页处理。 | —（仅页眉 Logo） |
| P47 | 补充 | 课程自编；不引用具体融资额或市场规模。 | —（仅页眉 Logo） |
| P48 | 补充 | 课程自编概述；不指名具体企业产品性能。 | —（仅页眉 Logo） |
| P49 | 必讲 | 课程自编教学情景（假设），无企业数据；目标量为内应力/强度（见页面图注），不写「翘曲」。 | 1 张（253×250） |
| P50 | 补充 | 课程自编教学情景（假设）；分组验证见第 8 讲。 | 1 张（368×242） |
| P51 | 必讲 | 课程自编；与 V5 大纲「可信评估」要求一致。 | —（仅页眉 Logo） |
| P52 | 补充 | 课程自编。 | —（仅页眉 Logo） |
| P53 | 分隔页（补充） | 课程自编。 | —（仅页眉 Logo） |
| P54 | 补充 | V5 授课计划与教学大纲（模块学时 6/4/10/4/4/2/2）；本页与计划一致。 | —（仅页眉 Logo） |
| P55 | 补充 | V5 教学大纲「六、考核与评分」与「四次作业与阶段任务」。 | —（仅页眉 Logo） |
| P56 | 必讲 | V5 大纲「研究表达与诚信」与课程导论 P30 约定（不是本讲 P30 的可解释性页）；不虚构处分条款。 | —（仅页眉 Logo） |
| P57 | 补充 | V5 大纲「期末项目」「论文评议与课堂研讨」；节点为第 8/10/14/16 讲；讨论记录约 300 字。 | —（仅页眉 Logo） |
| P58 | 必讲·小结 | 课程自编；下讲内容见第 2 讲任务书与 V5 计划。 | —（仅页眉 Logo） |
| P59 | 必讲·实践 | code/环境验收/环境验收.py 实跑输出（Python 3.14.5 / Windows）；独立复算最大偏差 0.000638041261062483 eV。 | —（仅页眉 Logo） |
| P60 | 必讲·退出 | 课程自编模板；与 V5 大纲任务卡字段一致（输入/目标/样本单位/可用时点/验证）。 | —（仅页眉 Logo） |

## 三、图片处理与许可状态

- 除 P33 移除未核肖像外，其余图片沿用 V4 版面位置与比例（未拉伸、未裁切、未替换）；三轮修订只改文字与 P33 左卡版式，没有替换任何图片素材。
- **P33 肖像已移除**：源 DSL `gen_slides.py` 第 992 行用的是 `assets/edison_portrait.png`，却署「Donald Stookey（1915–2014）」；该图与 Corning 官方 Stookey 肖像不一致，身份未核。V5 不再使用这张图、不猜原图人物是谁，左卡改为可编辑的三步观察卡（炉温异常—观察析晶—检验性能），姓名与生卒年以文字保留。
- P34 的历史照片仍来自原课程讲义，未核到具体馆藏与许可；课程内使用，**对外公开或录制课程前需替换或取得许可**。
- P10 的图片是 Materials Today 2005 原刊首页扫描（历史课程配图），本轮未替换；图注标为「未核馆藏与许可」，不据此图给新引文背书。
- P41/P43 的论文示意图同样为历史素材；正文只讲任务边界，不把示意图当原始数据。

## 四、数值与事实核验

| 项 | 核验方式 |
|---|---|
| 12 行 × 5 列、bandgap_J 缺 6 行 | `环境验收.py --step read` 实跑（Python 3.14.5 / Windows） |
| 最大换算偏差 0.000638041261062483 eV | 独立读 CSV 复算（S05 MgO）；脚本显示为 0.0006 eV |
| ΣC(89,k) ≈ 5.80×10¹² | 本机复算（k=1..10，不计比例与结构） |
| Al 7075 回溯 | 按既有牌号（1943 年商业化）叙述，不称新发现 |
| Rajan 2005 文献 | Materials Today 8(10), 38–45, DOI 10.1016/S1369-7021(05)71123-8；出版者条目 PII S1369702105711238，类型 Review Feature |
| Stookey 玻璃陶瓷 | Corning 官方创新史 1952 年条目（感光玻璃 + 炉温失控 + 析晶乳白 + 落地不碎）；部分机构记 1953，页面统一写 20 世纪 50 年代 |
| GNoME 候选/实验 | 原文方法与边界；候选数按原论文口径，不写成已合成材料 |

## 五、未核与限制

- P11/P19 的早期工作年表与二十年曲线为原课程历史素材，未能逐条核到原始出处；按「历史示例」处理，不作为当前结论。
- P46 企业清单为历史名单，未逐家核实现状，仅作补充阅读。
- 旧引文「Rajan et al., Comput. Mater. Sci. 2005」与「该文用 ML 学金属玻璃形成能力」的归属未核，V5 已改为已核的 Materials Today 2005 综述条目；旧截图仅作历史课程配图。
- 原课程资源的份数/页数/论文篇数口径不同：讲义 38 份 PDF / 958 页；papers 目录 21 个 `.pdf` 扩展名文件中 17 个可解析（含 GP 专著）。V5 不在页面引用这些计数，统一以《覆盖矩阵》为准。
- 原 `code/README.md` 里写的「本讲实测通过」与具体版本号（Python 3.11.17 / numpy 2.4.6 等）缺绑定日志，已在 V5 入口改为「环境规范（非本机实测锁）」，不补造版本与结果。
