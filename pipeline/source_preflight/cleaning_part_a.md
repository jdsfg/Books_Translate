# Source Cleaning Part A
- Generated: 2026-07-21T16:07:31.934723+00:00
- Scope: 11 pending manuscripts listed below.
- Summary: **CLEAN_PASS 3**; **CLEAN_WITH_REMAINDERS 8**; **BLOCK 0**.
- Method: per-book structural repairs + formula multi-render peel preferring closed LaTeX; no global blind regex deletes; unsafe peels reverted; ZWSP stripped.

## 汇总

| # | 书名 | 修复前估点 | 修复后估点 | 行数变化 | 状态 |
|---|------|-----------|-----------|----------|------|
| 1 | AI 科学 I：从神经网络到 Transformer | 685 | 406 | 13373→13373 | CLEAN_WITH_REMAINDERS |
| 2 | AI 科学 II：大语言模型 | 163 | 103 | 10742→10742 | CLEAN_WITH_REMAINDERS |
| 3 | AI 工程：用 LLM 构建生产系统 | 46 | 45 | 19424→19400 | CLEAN_PASS |
| 4 | 数据库系统 | 86 | 36 | 12151→12108 | CLEAN_WITH_REMAINDERS |
| 5 | 分布式系统 | 44 | 13 | 12195→12168 | CLEAN_WITH_REMAINDERS |
| 6 | 操作系统 | 15 | 13 | 8812→8812 | CLEAN_WITH_REMAINDERS |
| 7 | 系统设计思维：大规模软件的架构之道 | 7 | 2 | 12263→12271 | CLEAN_WITH_REMAINDERS |
| 8 | 理性之外：行为经济学 | 17 | 9 | 5311→5311 | CLEAN_WITH_REMAINDERS |
| 9 | 营养的逻辑 | 0 | 0 | 4891→4891 | CLEAN_PASS |
| 10 | 钱为我用 | 2 | 0 | 4501→4484 | CLEAN_PASS |
| 11 | 训练的科学·卷二：耐力与整体表现 | 14 | 5 | 1756→1759 | CLEAN_WITH_REMAINDERS |

## 逐书

### AI 科学 I：从神经网络到 Transformer — CLEAN_WITH_REMAINDERS

- 预检来源: `pending_part_2`（原状态 BLOCK）
- 问题计数（启发式）: 685 → 406
- 行数: 13373 → 13373; 变更行约 2656
- 主要变更行范围: `[[85, 85], [107, 107], [117, 117], [121, 123], [258, 258], [268, 270], [326, 328], [332, 333], [445, 445], [521, 527], [549, 549], [553, 553]]`
- 公式: Prefer closed LaTeX via ABA/island peel; ZWSP stripped; unsafe peels reverted. Spot-checked early/mid/late.
- 重复: n/a
- 目录: n/a
- 表格: Forward/Backward pass → 3-col GFM with stub first header cell.
- 未解决:
  - ~406 heuristic residual multi-render hits remain after safe cleaning.

### AI 科学 II：大语言模型 — CLEAN_WITH_REMAINDERS

- 预检来源: `pending_part_1`（原状态 BLOCK）
- 问题计数（启发式）: 163 → 103
- 行数: 10742 → 10742; 变更行约 906
- 主要变更行范围: `[[77, 77], [115, 121], [129, 129], [133, 133], [154, 154], [160, 160], [196, 200], [222, 224], [293, 297], [307, 307], [345, 345], [351, 353]]`
- 公式: Systemic peel + manual underbrace/ELMo; unsafe PPO peels restored from backup.
- 重复: n/a
- 目录: n/a
- 表格: Added Metric col to Kaplan/Chinchilla; filled Category on assessment table.
- 未解决:
  - ~103 heuristic residual multi-render hits remain after safe cleaning.
  - SOURCE_CONFLICT avoided: unclear PPO/π_θ inline peels left as backup text rather than guessed.

### AI 工程：用 LLM 构建生产系统 — CLEAN_PASS

- 预检来源: `pending_part_1`（原状态 BLOCK）
- 问题计数（启发式）: 46 → 45
- 行数: 19424 → 19400; 变更行约 566
- 主要变更行范围: `[{"lines_before": 19424, "lines_after": 19400}, [31, 34], [18411, 19400]]`
- 公式: n/a
- 重复: Removed duplicate Weeks 12–13 discipline block (kept one).
- 目录: Removed duplicate Introduction; listed Appendix A–D.
- 表格: Removed ## from Anti-pattern cheat-sheet header; normalized GFM.
- 未解决: 无

### 数据库系统 — CLEAN_WITH_REMAINDERS

- 预检来源: `pending_part_1`（原状态 BLOCK）
- 问题计数（启发式）: 86 → 36
- 行数: 12151 → 12108; 变更行约 318
- 主要变更行范围: `[{"lines_before": 12151, "lines_after": 12108}, [286, 286], [329, 329], [2810, 2812], [2822, 2825], [2829, 2831], [2835, 2837], [2845, 2849], [2853, 2855], [2867, 2867], [2885, 2887], [2891, 2891]]`
- 公式: Safe multi-render peel; clear FD X→Y examples normalized.
- 重复: Deleted second Think Deeper 15–20 / Summary tail.
- 目录: n/a
- 表格: Lock matrix: added Lock type header column.
- 未解决:
  - ~36 heuristic residual multi-render hits remain after safe cleaning.

### 分布式系统 — CLEAN_WITH_REMAINDERS

- 预检来源: `pending_part_2`（原状态 BLOCK）
- 问题计数（启发式）: 44 → 13
- 行数: 12195 → 12168; 变更行约 12090
- 主要变更行范围: `[{"lines_before": 12195, "lines_after": 12168}, [34, 12168]]`
- 公式: Arrow/parallel and ABA peels; some aaa/bbb prose triples remain.
- 重复: One 29.4/29.5 + one polish note; removed replay.
- 目录: Deleted ghost「第 30 章」.
- 表格: Removed ## from three tables; GFM normalized.
- 未解决:
  - ~13 heuristic residual multi-render hits remain after safe cleaning.

### 操作系统 — CLEAN_WITH_REMAINDERS

- 预检来源: `pending_part_2`（原状态 BLOCK）
- 问题计数（启发式）: 15 → 13
- 行数: 8812 → 8812; 变更行约 41
- 主要变更行范围: `[[14, 31], [61, 61], [73, 73], [1483, 1483], [1577, 1577], [1581, 1581], [1615, 1615], [1625, 1625], [1645, 1645], [1669, 1669], [1759, 1759], [1763, 1763]]`
- 公式: Ch5 Average turnaround triples → single $...$ each.
- 重复: n/a
- 目录: Rebuilt from H2 Introduction + Chapters 1–26.
- 表格: n/a
- 标题层级: Introduction children #### → ###.
- 未解决:
  - ~13 heuristic residual multi-render hits remain after safe cleaning.

### 系统设计思维：大规模软件的架构之道 — CLEAN_WITH_REMAINDERS

- 预检来源: `pending_part_1`（原状态 BLOCK）
- 问题计数（启发式）: 7 → 2
- 行数: 12263 → 12271; 变更行约 7511
- 主要变更行范围: `[{"lines_before": 12263, "lines_after": 12271}, [684, 684], [692, 696], [1114, 1803], [1807, 10493], [10497, 10501], [10505, 10799], [10803, 10807], [10811, 11109], [11113, 11117], [11121, 11404], [11408, 11412]]`
- 公式: Availability/QPS/HitRatio/PageRank → closed LaTeX; arithmetic checked.
- 重复: n/a
- 目录: n/a
- 表格: n/a
- 未解决:
  - ~2 heuristic residual multi-render hits remain.

### 理性之外：行为经济学 — CLEAN_WITH_REMAINDERS

- 预检来源: `pending_part_1`（原状态 BLOCK）
- 问题计数（启发式）: 17 → 9
- 行数: 5311 → 5311; 变更行约 119
- 主要变更行范围: `[[267, 267], [277, 279], [293, 293], [303, 303], [307, 307], [311, 317], [347, 349], [361, 361], [371, 371], [405, 411], [431, 431], [439, 439]]`
- 公式: CE/RP/β peels where safe; CE=25 example verified.
- 重复: n/a
- 目录: n/a
- 表格: n/a
- 未解决:
  - ~9 heuristic residual multi-render hits remain after safe cleaning.

### 营养的逻辑 — CLEAN_PASS

- 预检来源: `pending_part_2`（原状态 BLOCK）
- 问题计数（启发式）: 0 → 0
- 行数: 4891 → 4891; 变更行约 4
- 主要变更行范围: `[[430, 430], [434, 434], [438, 438], [2746, 2746]]`
- 公式: GL → closed $$\frac...$$; ZWSP removed; reversed unicode flank discarded.
- 重复: n/a
- 目录: n/a
- 表格: n/a
- 标题层级: 12.9 Exercises → 12.8 (no missing body for 12.8).
- 未解决: 无

### 钱为我用 — CLEAN_PASS

- 预检来源: `pending_part_2`（原状态 BLOCK）
- 问题计数（启发式）: 2 → 0
- 行数: 4501 → 4484; 变更行约 2538
- 主要变更行范围: `[{"lines_before": 4501, "lines_after": 4484}, [55, 55], [67, 67], [106, 4484]]`
- 公式: Wealth/savings-rate/Rule-of-72/runway/P/R closed LaTeX; (1.07)^{10} de-tripled.
- 重复: Removed glued Q3/Summary replay after Start today.
- 目录: n/a
- 表格: n/a
- 标题层级: Intro #### → ###.
- 未解决: 无

### 训练的科学·卷二：耐力与整体表现 — CLEAN_WITH_REMAINDERS

- 预检来源: `pending_part_2`（原状态 BLOCK）
- 问题计数（启发式）: 14 → 5
- 行数: 1756 → 1759; 变更行约 1571
- 主要变更行范围: `[{"lines_before": 1756, "lines_after": 1759}, [78, 78], [102, 102], [184, 1756]]`
- 公式: Q̇ + Karvonen → closed math; ZWSP stripped.
- 重复: n/a
- 目录: n/a
- 表格: Zone/Session outer pipes; cell formulas deduped.
- 标题层级: 1.2/1.4 H4→H3; list items 4–5 restored.
- 未解决:
  - ~5 heuristic residual multi-render hits remain.

## 约束遵循

- 仅修改上述 11 份 `sources/pending/` 源稿 + 本报告文件。
- 未修改 `SOURCE_INTAKE.md`、其他书稿、流水线脚本；未移动文件、未 init/lock-titles/翻译。
- 无法确定的公式未猜测；损坏剥皮不安全处回退原文。
