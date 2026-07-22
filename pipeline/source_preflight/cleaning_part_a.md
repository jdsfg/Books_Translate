# Source Cleaning Part A（复验返修）

- Generated: 2026-07-21T22:35:00Z
- Scope: 11 pending manuscripts（同 PR #20）
- Trigger: 控制审校评论要求撤销不安全公式批量改写，仅保留可验证结构修复。
- 第三轮复验返修：仅补《分布式系统》3 张表的 `#` 首列与列数对齐。

## 返修原则（已执行）

1. **从 `origin/main` 全量恢复** 11 份源稿，丢弃本轮不安全的公式批量剥皮/改写。
2. **仅重做可逐项验证的结构修复**：精确重复段、目录、伪 H2 表头、表格列数/空白首列、可核对的标题层级与列表拆分。
3. **公式多重渲染**：凡无法从当前源稿唯一恢复的，**保持原文**，登记 `SOURCE_CONFLICT`；状态记为 **BLOCK**（不得用 CLEAN_WITH_REMAINDERS 粉饰为可晋升）。
4. 未修改 `SOURCE_INTAKE.md`、其他书稿、流水线脚本；未移动文件、未 init/lock-titles/翻译。

## 汇总

| # | 书名 | 结构修复 | 公式处理 | 状态 |
|---|------|----------|----------|------|
| 1 | AI 科学 I：从神经网络到 Transformer | 表头 stub 列 | 已撤销批量改写，原文保留 | BLOCK |
| 2 | AI 科学 II：大语言模型 | Kaplan Metric 列；评估表 Category 填列 | 已撤销批量改写，原文保留 | BLOCK |
| 3 | AI 工程：用 LLM 构建生产系统 | TOC/重复段/伪H2→5列表 | L6559 RRF 三重渲染保留 | BLOCK |
| 4 | 数据库系统 | 锁矩阵首列；尾部重复删除 | 已撤销批量改写，原文保留 | BLOCK |
| 5 | 分布式系统 | 幽灵目录；收尾重复；3处伪H2；**第三轮补3表 `#` 首列** | 已撤销批量改写，原文保留 | BLOCK |
| 6 | 操作系统 | TOC 重建；Intro ####→### | 调度公式三重渲染保留 | BLOCK |
| 7 | 系统设计思维：大规模软件的架构之道 | 无（原 BLOCK 仅为公式） | 原文保留 | BLOCK |
| 8 | 理性之外：行为经济学 | 无（原 BLOCK 仅为公式） | 原文保留 | BLOCK |
| 9 | 营养的逻辑 | 12.9→12.8 重编号 | GL 三重渲染保留 | BLOCK |
| 10 | 钱为我用 | 结尾重复删除；Intro ####→###；**未删 Discussion 正文** | 公式原文保留 | BLOCK |
| 11 | 训练的科学·卷二：耐力与整体表现 | 1.2/1.4 层级；列表 4/5；表管道符/列对齐 | 单元格公式未盲洗 | BLOCK |

**状态汇总：BLOCK 11；CLEAN_PASS 0；CLEAN_WITH_REMAINDERS 0。**

## 逐书

### 1. AI 科学 I：从神经网络到 Transformer — BLOCK

- 修复前问题：系统性公式多重渲染 + Forward/Backward 表列数不一致（预检 Part 2）。
- 本轮结构：`| | Forward pass | Backward pass |` 与三列分隔行；数据行外管道规范化。
- 公式：抽样 L85/915/938/1034/7504/12688/13364 与 `main` **逐字一致**（批量改写已撤销）。
- 未解决：`SOURCE_CONFLICT` — 全书系统性 plain+LaTeX+unicode 粘连；需独立、可逐项核验的公式清洗轮，禁止正则盲洗。
- 修改行范围：约 L2021–2026（表）。

### 2. AI 科学 II：大语言模型 — BLOCK

- 结构：Kaplan/Chinchilla 增 `Metric` 列；评估表为省略 Category 的行回填当前类别。
- 公式：抽样 L77/129/222/5801/8571 与 `main` 一致。
- 未解决：`SOURCE_CONFLICT` — 系统性公式多重渲染（含 underbrace/ELMo/PPO 等）。
- 修改行范围：约 L2539–2543；L10486–10502。

### 3. AI 工程：用 LLM 构建生产系统 — BLOCK

- 结构：
  - TOC：删 Chapter 25 后重复 Introduction；补 Appendix A–D。
  - 删除第二份 discipline 长段（保留一份）。
  - 伪 H2 表改为 5 列：`| # | Anti-pattern | The kill criterion | Anchor failure | Chapter(s) |`（与数据列数一致）。
- 公式：L6559 RRF `1/(k+rank…)` 三重渲染 **未改**（无法唯一还原为单一形式时不猜测）。
- 未解决：`SOURCE_CONFLICT` — RRF 等多处公式粘连。
- 修改行范围：TOC L31–34；重复段约 L18411–18434；表约 L19261+。

### 4. 数据库系统 — BLOCK

- 结构：锁兼容矩阵表头补 `Lock type`；删除文末第二份 Think Deeper 15–20/Summary。
- 公式：与 `main` 一致（批量改写已撤销）。
- 未解决：`SOURCE_CONFLICT` — 系统性公式多重渲染。
- 修改行范围：约 L7616–7622；尾部约原 L12105–12147。

### 5. 分布式系统 — BLOCK

- 结构：删幽灵 `- 第 30 章`；保留一份 29.4/29.5 + 单条 polish note；三处 `## |` 表头去伪 H2。
- **第三轮复验（仅此书表）**：为 3 张缺编号首列表补 `#`，统一表头/分隔行/数据行列数与外管道：
  - L11276–L11289：Workflow 宽表 → 7 列（`#` + 原 6 列）
  - L11817–L11824：Six Lies → 4 列（`#` + 原 3 列）
  - L12103–L12129：Misconceptions → 4 列（`#` + 原 3 列）
- 公式：原文保留（L715/913 等内容仍在文件中，仅因上方删行导致行号偏移）。
- 未解决：`SOURCE_CONFLICT` — 公式/变量三重渲染（表结构缺口已清）。
- 修改行范围：TOC L34；收尾约原 L11664–11690；表 L11276+/L11817+/L12103+。

### 6. 操作系统 — BLOCK

- 结构：按正文 H2 重建 Introduction+Ch1–26 目录；`#### How the book is organized` / `Three threading plans` → `###`。
- 公式：Ch5 Average turnaround 等三重渲染 **未改**。
- 未解决：`SOURCE_CONFLICT` — 调度算术三重渲染。
- 修改行范围：TOC L3–33；Intro 子标题。

### 7. 系统设计思维：大规模软件的架构之道 — BLOCK

- 结构：无（预检 BLOCK 均为公式）。
- 公式：全文与 `main` 一致（未再改写）。
- 未解决：`SOURCE_CONFLICT` — Combined availability / Hit Ratio 等多重渲染。
- 修改行范围：无。

### 8. 理性之外：行为经济学 — BLOCK

- 结构：无。
- 公式：与 `main` 一致。
- 未解决：`SOURCE_CONFLICT` — CE/RP/x 等多重渲染。
- 修改行范围：无。

### 9. 营养的逻辑 — BLOCK

- 结构：`### 12.9 Exercises` → `### 12.8 Exercises`（12.7 后直接接习题，无缺失正文可恢复为 12.8）。
- 公式：L430/434/438 GL 三重渲染 + ZWSP **未改**。
- 未解决：`SOURCE_CONFLICT` — GL 公式多重渲染。
- 修改行范围：L2746。

### 10. 钱为我用 — BLOCK

- 结构：Intro `####`→`###`；删除 Summary 后粘连/重复的 Discussion+Summary；**保留** L506 Rule-of-72 Discussion 全文（约 114 词，含高利率讨论上下文；Q2 题干含 50%/100%）。
- 公式：未做批量改写；定界符/粘连数字保持源稿原样。
- 未解决：`SOURCE_CONFLICT` — 财富方程/Rule-of-72 等三重渲染。
- 修改行范围：L55/L67；结尾约 L4479–4497→单份收尾。

### 11. 训练的科学·卷二：耐力与整体表现 — BLOCK

- 结构：`#### 1.2/1.4`→`###`；氧级联第 4/5 项拆回独立列表行；Zone/Session/灰区表外管道与列数对齐（灰区表补空白首列表头以匹配 `Weekly total | …` 五行）。
- 公式：**未**对 Karvonen 单元格做盲洗；单元格内三重算式仍在。
- 未解决：`SOURCE_CONFLICT` — 公式多重渲染与部分表内粘连算式。
- 修改行范围：L78/102；L186–189；表 L598–605 / 737–745 / 759–761 一带。

## 审校点对账

| 审校证据 | 处理 |
|----------|------|
| AI工程 4列表头/5列数据 | 改为 5 列表头（含 `#`） |
| AI工程 L6559 RRF | 保留原文 + SOURCE_CONFLICT |
| 钱为我用 Discussion 误删 | 已从 main 恢复后仅做结构删重；L506 仍为 114 词 |
| AI科学I/II 公式截断/误删 | 已撤销；抽样与 main 一致 |
| 操作系统/分布式/训练公式或表 | 结构已修；公式未盲洗 |
| **第三轮**：分布式 3 表缺 stub 首列（6/7、3/4、3/4） | 均补 `#` 首列；表头/分隔/数据列数一致 |

## 结论

本轮 **11/11 BLOCK**（公式 `SOURCE_CONFLICT` 仍在）。第三轮仅清掉《分布式系统》3 张表的列数缺口；其余书未改。
