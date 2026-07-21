# 待入库英文源稿预检 Part 1
## 范围与方法
本报告仅检查任务指定的 24 份 `sources/pending/*.md` 英文源稿；未翻译、未执行 `init`/`lock-titles`、未移动源稿、未修改 `SOURCE_INTAKE.md`。检查使用 Python 标准库全量逐行扫描，并对全部候选回到原文人工复核；未使用长度比判断完整性。
覆盖项：UTF-8 与语言占比、H1–H4/章节编号/目录对应、开头与结尾、长段和小节重复、LaTeX 定界与多重渲染、表格列与管道、代码围栏/标签/缩进、脚注/链接/本地资源、乱码/HTML/占位符、章节回指/附录/术语表/最终分隔线。
## 汇总
- PASS：**10**
- PASS_WITH_WARNINGS：**4**
- BLOCK：**10**
- BLOCK 书名：《AI 工程：用 LLM 构建生产系统》、《系统设计思维：大规模软件的架构之道》、《被讲述的自己——自欺背后的脑科学》、《AI 科学 II：大语言模型》、《情绪的科学：识别、调节、不被绑架》、《数据库系统》、《压力的科学》、《理性之外：行为经济学》、《机器学习：从数据到智能》、《说服性写作》

全局核验：24/24 文件可读、UTF-8 正常且英语占主导；24 本均无 H1，正文统一以 H2 承载 Introduction/Chapter/Appendix，H3/H4 承载小节。所有显式 LaTeX 定界符计数闭合，所有代码围栏闭合，未发现真实缺失脚注定义或本地资源；自动扫描的金额 `$`、正则、HTML/编码教学示例、数学变量 `xxx/fff/nnn` 等均已人工排除。24 本结尾均经正文语义复核并有最终 `---`；BLOCK 来自结构污染、重复内容或公式/表格损坏，不来自篇幅。
## 逐书结论
| # | 书名 | 字节数 | 行数 | H1/H2/H3/H4 | 状态 | 结构与完整性 |
|---:|---|---:|---:|---|---|---|
| 1 | AI 工程：用 LLM 构建生产系统 | 1820312 | 19424 | 0/32/321/228 | **BLOCK** | Introduction、Chapter 1–25、Appendix A–D；末附录完整收束。 |
| 2 | 古老的认知疗法——斯多葛主义的现代诠释 | 1199601 | 7008 | 0/17/137/305 | **PASS_WITH_WARNINGS** | Chapter 1–14、Appendix A–G；正文与附录结尾完整。 |
| 3 | 系统设计思维：大规模软件的架构之道 | 1161018 | 12263 | 0/29/268/445 | **BLOCK** | Chapter 1–28 连续；Chapter 28 有 Summary 和完整收束句。 |
| 4 | 被讲述的自己——自欺背后的脑科学 | 1104947 | 5304 | 0/17/110/117 | **BLOCK** | Chapter 1–12、Coda、Further Reading；书目说明完整结束。 |
| 5 | AI 科学 II：大语言模型 | 974314 | 10742 | 0/25/243/304 | **BLOCK** | Chapter 1–24 连续；24.9 答案及末尾完整。 |
| 6 | 情绪的科学：识别、调节、不被绑架 | 938489 | 5792 | 0/28/228/129 | **BLOCK** | Chapter 1–18、Appendix A–F；最终附录完整收束。 |
| 7 | 数据库系统 | 884261 | 12151 | 0/25/292/673 | **BLOCK** | Introduction、Chapter 1–23；末章总结完整，但末段重复。 |
| 8 | 压力的科学 | 833222 | 6111 | 0/15/108/55 | **BLOCK** | Introduction、Chapter 1–14；Chapter 11 正文存在但标题粘连，末章收束后重复。 |
| 9 | 理性之外：行为经济学 | 757814 | 5311 | 0/23/168/219 | **BLOCK** | Chapter 1–22 连续；末章练习、答案和总结完整。 |
| 10 | 细听：巴赫 | 755611 | 4259 | 0/24/163/262 | **PASS** | Chapter 1–23 连续；Closing Handoff 和系列提示完整。 |
| 11 | 学术写作：从论文到研究计划 | 722745 | 5361 | 0/19/196/174 | **PASS** | Chapter 1–18 连续；末章总结和收束引语完整。 |
| 12 | 机器学习：从数据到智能 | 656016 | 7532 | 0/28/207/311 | **BLOCK** | Introduction、Chapter 1–26、Epilogue；结尾“The search continues.”完整。 |
| 13 | 社会学的想象力 | 623719 | 2819 | 0/23/148/114 | **PASS_WITH_WARNINGS** | Introduction、Chapter 1–21；末章总结和收束完整。 |
| 14 | 说服性写作 | 586617 | 5422 | 0/20/199/270 | **BLOCK** | Introduction、Chapter 1–17；结尾“Write that one.”完整。 |
| 15 | 细品大师：卡拉瓦乔 | 576689 | 3438 | 0/27/199/225 | **PASS** | Introduction、Chapter 1–25；终章回收 six moves / three threads。 |
| 16 | 社会心理学 | 547841 | 2366 | 0/23/135/102 | **PASS** | Introduction、Chapter 1–21；Open Verdict 和 Summary 完整。 |
| 17 | 细读世界文学·卷一：史诗与悲剧 | 525389 | 2705 | 0/28/143/148 | **PASS** | Introduction、Chapter 1–26；明确声明 volume complete。 |
| 18 | 调试思维 | 484366 | 5633 | 0/19/158/161 | **PASS** | Chapter 1–18；结尾“Happy debugging.”完整。 |
| 19 | 细品大师：伦勃朗 | 473204 | 2633 | 0/22/193/130 | **PASS_WITH_WARNINGS** | 目录列 Introduction，正文前言无 H2；Chapter 1–22 连续，终章完整。 |
| 20 | 细品大师：莫奈 | 428905 | 2301 | 0/26/139/136 | **PASS_WITH_WARNINGS** | Introduction、Chapter 1–24；终章 Orangerie 收束完整。 |
| 21 | 细读世界文学·卷三：小说的艺术 | 408382 | 2755 | 0/26/136/147 | **PASS** | Introduction、Chapter 1–24；系列终卷声明完整。 |
| 22 | AI时代六大超能力-卷一-Git与GitHub | 356303 | 2415 | 0/18/103/95 | **PASS** | Introduction、Chapter 1–16；终章指向下一卷并完整收束。 |
| 23 | 细品大师：维米尔 | 262078 | 1623 | 0/26/143/72 | **PASS** | Introduction、Chapter 1–24；终章和系列声明完整。 |
| 24 | AI时代六大超能力-卷六-你的第二大脑 | 195770 | 1358 | 0/16/81/57 | **PASS** | Introduction、Chapter 1–14；明确声明系列终卷并完整收束。 |

## 问题明细
### AI 工程：用 LLM 构建生产系统 — BLOCK
#### Issue 1
- 严重级别：`BLOCKER`
- 问题类型：`duplicate_long_section`
- 文件名：`sources/pending/AI 工程：用 LLM 构建生产系统.md`
- 行号：L18386–L18409（first copy）；L18411–L18434（second copy）
- 原文证据：“Add the discipline to the team's recurring meeting agenda…”至“…years beyond this book's publication.”整段连续复现。
- 风险：同一长段会被切块并重复翻译，形成实质内容重复。
- 建议处理：初始化前删除第二份 L18411–L18434，并人工确认段落衔接。
#### Issue 2
- 严重级别：`BLOCKER`
- 问题类型：`table_header_misparsed_as_h2`
- 文件名：`sources/pending/AI 工程：用 LLM 构建生产系统.md`
- 行号：L19285–L19293
- 原文证据：L19285 为“## | Anti-pattern | The kill criterion | Anchor failure | Chapter(s)”。
- 风险：表头被写成 H2，初始化会把速查表误当成独立章节并污染标题锁。
- 建议处理：初始化前删除表头前的“## ”，保留普通 Markdown 表格。
#### Issue 3
- 严重级别：`MEDIUM`
- 问题类型：`toc_duplicate_and_omission`
- 文件名：`sources/pending/AI 工程：用 LLM 构建生产系统.md`
- 行号：L31–L34
- 原文证据：Chapter 25 后连续出现四行“- Introduction”，且目录未列 Appendix A–D。
- 风险：目录与正文不对应，读者导航和后续目录审计会产生误报。
- 建议处理：去除重复 Introduction；按正文补列 Appendix A–D，或登记为目录裁剪决定。
### 古老的认知疗法——斯多葛主义的现代诠释 — PASS_WITH_WARNINGS
#### Issue 4
- 严重级别：`MEDIUM`
- 问题类型：`toc_corruption`
- 文件名：`sources/pending/古老的认知疗法——斯多葛主义的现代诠释.md`
- 行号：L20
- 原文证据：目录末项为“- Appendix C: _prosochē_).”，正文实际包含 Appendix A–G。
- 风险：目录条目明显残缺且不能代表正文附录结构。
- 建议处理：更正附录目录为 A–G，或由控制模型登记目录不参与标题锁。
### 系统设计思维：大规模软件的架构之道 — BLOCK
#### Issue 5
- 严重级别：`BLOCKER`
- 问题类型：`formula_multiple_renderings`
- 文件名：`sources/pending/系统设计思维：大规模软件的架构之道.md`
- 行号：L684；L692；L694；L696；L1114；L1116；L1124；L1128；L1132；L2711；L3265；L3269；L3514；L10383；L10407
- 原文证据：L684：“Combined availability=…\text{Combined availability} = …Combined availability=…”；L696：“99.95%99.95\%99.95%”。
- 风险：同一公式以 Unicode/LaTeX/纯文本二至三重粘连，共 15 行；会导致重复翻译和数字变形。
- 建议处理：初始化前逐行归一为一种公式表示，并复核计算值。
### 被讲述的自己——自欺背后的脑科学 — BLOCK
#### Issue 6
- 严重级别：`BLOCKER`
- 问题类型：`table_header_misparsed_as_h2`
- 文件名：`sources/pending/被讲述的自己——自欺背后的脑科学.md`
- 行号：L4878–L4893
- 原文证据：L4878 为“## | Action | Line 2 (inner reason) | …”。
- 风险：应用题表格被识别为 H2 章节，污染切块和标题锁。
- 建议处理：初始化前删除表头前的“## ”。
#### Issue 7
- 严重级别：`BLOCKER`
- 问题类型：`duplicate_long_section`
- 文件名：`sources/pending/被讲述的自己——自欺背后的脑科学.md`
- 行号：L5109–L5129（first copy）；L5131–L5151（second copy）
- 原文证据：“A third observation…”至“Tonight, before sleep, write the brief letter…”整块连续重复。
- 风险：重复内容会进入两个翻译块并破坏章末到 Coda 的衔接。
- 建议处理：删除第二份 L5131–L5151，并确认保留一次分隔线。
### AI 科学 II：大语言模型 — BLOCK
#### Issue 8
- 严重级别：`BLOCKER`
- 问题类型：`systemic_formula_multiple_renderings`
- 文件名：`sources/pending/AI 科学 II：大语言模型.md`
- 行号：L77；L222–L224；L2008–L2012；L2070；L10612
- 原文证据：L77 将 underbrace 的可视式、LaTeX 和可视式粘为一行；L222–L224 出现“ELMo_k…ELMok”及“jjj/kkk”；L2070 出现“Y=AK…Y=AK”与“YYY/KKK/LLL”。
- 风险：全书 602 行命中 LaTeX 命令与重复渲染特征，变量和上下标被重复，属于系统性源稿损坏。
- 建议处理：禁止初始化；先全书清洗为单一公式形式，再由控制模型复核公式与变量。
#### Issue 9
- 严重级别：`HIGH`
- 问题类型：`table_shape_inconsistent`
- 文件名：`sources/pending/AI 科学 II：大语言模型.md`
- 行号：L2539–L2543；L10486–L10503
- 原文证据：L2539 表头只有“Kaplan | Chinchilla”，数据行却有指标名 + 两值；L10489 起后续行省略 Category 列，列数少于四列表头。
- 风险：表格列语义错位，转换或翻译时可能丢失首列归属。
- 建议处理：补齐空白/指标表头并使每行列数一致。
### 情绪的科学：识别、调节、不被绑架 — BLOCK
#### Issue 10
- 严重级别：`BLOCKER`
- 问题类型：`table_headers_misparsed_as_h2`
- 文件名：`sources/pending/情绪的科学：识别、调节、不被绑架.md`
- 行号：L359–L366；L5033–L5041；L5047–L5060
- 原文证据：三处表头分别以“## | Move | …”和“## | Emotion | …”开头。
- 风险：三张表会被初始化为伪章节，章节数和标题锁均被污染。
- 建议处理：初始化前删除三处表头前的“## ”，并复核表格列数。
### 数据库系统 — BLOCK
#### Issue 11
- 严重级别：`BLOCKER`
- 问题类型：`systemic_formula_multiple_renderings`
- 文件名：`sources/pending/数据库系统.md`
- 行号：L286；L329；L2810–L2812；L10525–L10527
- 原文证据：L286：“10−2/(3×10−10)…\frac{10^{-2}}{3 \times 10^{-10}}…10−2…”；L2810：“XXX…YYY…X→Y\,X \rightarrow Y\,X→Y…RRR”。
- 风险：195 行命中重复公式特征，函数依赖变量出现 XXX/YYY/RRR 三写，数学和关系代数内容不可直接入翻译流水线。
- 建议处理：禁止初始化；全书归一公式并核对变量、上下标和运算符。
#### Issue 12
- 严重级别：`BLOCKER`
- 问题类型：`duplicate_tail_section`
- 文件名：`sources/pending/数据库系统.md`
- 行号：L12061–L12103（first copy）；L12105–L12147（second copy）
- 原文证据：Think Deeper 15–20、Hints、Chapter Summary 和“That is what a database engineer does.”整体重复。
- 风险：末章将产生重复问题、答案和总结。
- 建议处理：删除第二份 L12105–L12147，保留单次总结与终分隔线。
#### Issue 13
- 严重级别：`HIGH`
- 问题类型：`table_header_missing_row_label`
- 文件名：`sources/pending/数据库系统.md`
- 行号：L7616–L7622
- 原文证据：锁兼容矩阵表头为“| IS | IX | S | SIX | X”，正文行还含行标签 IS/IX/S/SIX/X。
- 风险：表头比数据行少一列，首列行标签没有表头，渲染和语义映射可能错位。
- 建议处理：在表头增加空白或“Lock type”首列，并统一列数。
### 压力的科学 — BLOCK
#### Issue 14
- 严重级别：`BLOCKER`
- 问题类型：`chapter_heading_glued_and_toc_gap`
- 文件名：`sources/pending/压力的科学.md`
- 行号：L16（TOC gap）；L4141（glued Chapter 11 heading）
- 原文证据：目录由 Chapter 10 直接跳到 Chapter 12；L4141 在正文句末粘入“# Chapter 11: Childhood — ACEs and Biological Embedding”。
- 风险：Chapter 11 正文存在但不是独立 H2，初始化会把整章并入 Chapter 10，且目录漏章。
- 建议处理：在 L4141 前断行并改为“## Chapter 11: …”，同时补目录 Chapter 11。
#### Issue 15
- 严重级别：`BLOCKER`
- 问题类型：`duplicate_tail_section`
- 文件名：`sources/pending/压力的科学.md`
- 行号：L6057–L6081（first copy）；L6083–L6107（second copy）
- 原文证据：“Most readers cannot tell…”后的诊断段、Chapter Summary 和“The framework is yours now.”重复。
- 风险：终章收束被整段复制，翻译后会出现双重结尾。
- 建议处理：删除第二份 L6083–L6107，保留单次总结。
### 理性之外：行为经济学 — BLOCK
#### Issue 16
- 严重级别：`BLOCKER`
- 问题类型：`formula_multiple_renderings`
- 文件名：`sources/pending/理性之外：行为经济学.md`
- 行号：L267–L467；L529–L533；L2164–L2165；L2238–L2248
- 原文证据：L303–L317 出现“CECECE”“RP=…RP = …RP=…”；L529–L533 出现“xxx”“+x+x+x”和同一不等式三重表示。
- 风险：56 行公式/变量重复，损坏集中在效用、前景理论等核心数学段，直接翻译会保留错误变量和多重公式。
- 建议处理：初始化前将 56 个命中行归一为单一公式，复核变量 x、CE、RP、EU。
### 机器学习：从数据到智能 — BLOCK
#### Issue 17
- 严重级别：`BLOCKER`
- 问题类型：`systemic_formula_multiple_renderings`
- 文件名：`sources/pending/机器学习：从数据到智能.md`
- 行号：L149–L154；L341–L399；L6977–L7051；L7465
- 原文证据：L149：“xxx…yyy…fff…f(x)≈y\,f(x) \approx y\,f(x)≈y”；L153 出现“y∈{0,1}”三重表示。
- 风险：775 行命中重复公式特征，变量、集合、上下标和函数在全书范围内损坏。
- 建议处理：禁止初始化；系统清洗后全量复扫公式和变量。
#### Issue 18
- 严重级别：`BLOCKER`
- 问题类型：`table_cells_corrupted_by_dollar_math_parsing`
- 文件名：`sources/pending/机器学习：从数据到智能.md`
- 行号：L2657–L2660；L7505–L7511
- 原文证据：RMSE 值交替变成“(34,500”“)31,200”“(27,100”“)23,800”，原货币美元符号/定界被破坏。
- 风险：两张模型比较表的数值含义和 Markdown 列内容已损坏。
- 建议处理：从可信来源恢复金额/数值表示并统一转义美元符号。
### 社会学的想象力 — PASS_WITH_WARNINGS
#### Issue 19
- 严重级别：`LOW`
- 问题类型：`markdown_emphasis_corruption`
- 文件名：`sources/pending/社会学的想象力.md`
- 行号：L2815
- 原文证据：“_This is the end of_ The Sociological Imagination*, the gateway volume of* The Sociological Eye*…means.*”
- 风险：斜体起止混乱，结尾书名与句子会被错误渲染。
- 建议处理：整理该行斜体边界；不影响章节完整性，可登记后晋升。
### 说服性写作 — BLOCK
#### Issue 20
- 严重级别：`BLOCKER`
- 问题类型：`table_header_misparsed_as_h2`
- 文件名：`sources/pending/说服性写作.md`
- 行号：L415–L422
- 原文证据：L415 为“## | Move | Diagnostic question”。
- 风险：六步表被当成 H2，初始化会创建伪章节并污染锁定标题。
- 建议处理：初始化前删除表头前的“## ”。
#### Issue 21
- 严重级别：`HIGH`
- 问题类型：`table_column_mismatch`
- 文件名：`sources/pending/说服性写作.md`
- 行号：L4520–L4529
- 原文证据：四列表头“Layer | Tool | What it does | Where introduced”下，The Heart Test 与 The Restrained Connection 两行仅三列。
- 风险：两行缺少 Layer 单元格，渲染后各列错位。
- 建议处理：显式补空白 Layer 单元格或重复“Tests”，使每行保持四列。
### 细品大师：伦勃朗 — PASS_WITH_WARNINGS
#### Issue 22
- 严重级别：`MEDIUM`
- 问题类型：`toc_heading_mismatch`
- 文件名：`sources/pending/细品大师：伦勃朗.md`
- 行号：L5（TOC）；L31–L53（unheaded introduction）
- 原文证据：目录列“- Introduction”，但正文前言从“There is a particular kind of helplessness…”开始，直到 L55 才出现首个 H2 Chapter 1。
- 风险：目录锚点与正文标题树不一致；当前解析器会把该段作为 intro，内容不会丢失。
- 建议处理：补“## Introduction”，或删目录该项并明确保留无标题前言；可登记后晋升。
### 细品大师：莫奈 — PASS_WITH_WARNINGS
#### Issue 23
- 严重级别：`LOW`
- 问题类型：`heading_level_jump`
- 文件名：`sources/pending/细品大师：莫奈.md`
- 行号：L50；L60
- 原文证据：“## Introduction”后首个子标题直接为“#### How this book teaches”，跳过 H3。
- 风险：标题层级不规范，但不影响章节连续性或正文完整性。
- 建议处理：将 L60 改为 H3，或登记为前言体例后晋升。
## 无登记问题的 PASS 书目
- 《细听：巴赫》：Chapter 1–23 连续；Closing Handoff 和系列提示完整。 未发现章节缺口、突然截断、真实长段重复、公式/表格/围栏/脚注/链接或占位符阻断问题。
- 《学术写作：从论文到研究计划》：Chapter 1–18 连续；末章总结和收束引语完整。 未发现章节缺口、突然截断、真实长段重复、公式/表格/围栏/脚注/链接或占位符阻断问题。
- 《细品大师：卡拉瓦乔》：Introduction、Chapter 1–25；终章回收 six moves / three threads。 未发现章节缺口、突然截断、真实长段重复、公式/表格/围栏/脚注/链接或占位符阻断问题。
- 《社会心理学》：Introduction、Chapter 1–21；Open Verdict 和 Summary 完整。 未发现章节缺口、突然截断、真实长段重复、公式/表格/围栏/脚注/链接或占位符阻断问题。
- 《细读世界文学·卷一：史诗与悲剧》：Introduction、Chapter 1–26；明确声明 volume complete。 未发现章节缺口、突然截断、真实长段重复、公式/表格/围栏/脚注/链接或占位符阻断问题。
- 《调试思维》：Chapter 1–18；结尾“Happy debugging.”完整。 未发现章节缺口、突然截断、真实长段重复、公式/表格/围栏/脚注/链接或占位符阻断问题。
- 《细读世界文学·卷三：小说的艺术》：Introduction、Chapter 1–24；系列终卷声明完整。 未发现章节缺口、突然截断、真实长段重复、公式/表格/围栏/脚注/链接或占位符阻断问题。
- 《AI时代六大超能力-卷一-Git与GitHub》：Introduction、Chapter 1–16；终章指向下一卷并完整收束。 未发现章节缺口、突然截断、真实长段重复、公式/表格/围栏/脚注/链接或占位符阻断问题。
- 《细品大师：维米尔》：Introduction、Chapter 1–24；终章和系列声明完整。 未发现章节缺口、突然截断、真实长段重复、公式/表格/围栏/脚注/链接或占位符阻断问题。
- 《AI时代六大超能力-卷六-你的第二大脑》：Introduction、Chapter 1–14；明确声明系列终卷并完整收束。 未发现章节缺口、突然截断、真实长段重复、公式/表格/围栏/脚注/链接或占位符阻断问题。
## 判定说明
- `BLOCK`：问题会改变 H2 标题树、复制实质内容，或使公式/表格语义不可直接进入翻译流水线；必须在初始化前修复，或由控制模型明确裁决。
- `PASS_WITH_WARNINGS`：目录、强调或层级存在局部异常，但解析不会丢正文且可登记后晋升。
- `PASS`：本轮检查未发现需登记的问题。
