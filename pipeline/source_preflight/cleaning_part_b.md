# 待入库源稿清洗 Part B

## 范围

仅处理指定的 11 份 `sources/pending/*.md`；未修改 `SOURCE_INTAKE.md`、其他书稿或共享流水线脚本；未移动/init/lock-titles/翻译。

## 汇总

- CLEAN_PASS：**8**
- CLEAN_WITH_REMAINDERS：**3**
- BLOCK：**0**

## 逐书结果

| # | 书名 | 修复前问题数 | 修复后问题数 | 状态 |  diff +/- |
|---:|---|---:|---:|---|---|
| 1 | 机器学习：从数据到智能 | 2 | 1 | **CLEAN_WITH_REMAINDERS** | +1135/-1135 |
| 2 | 被讲述的自己——自欺背后的脑科学 | 2 | 0 | **CLEAN_PASS** | +1/-23 |
| 3 | 情绪的科学：识别、调节、不被绑架 | 1 | 0 | **CLEAN_PASS** | +3/-3 |
| 4 | 压力的科学 | 2 | 0 | **CLEAN_PASS** | +5/-27 |
| 5 | 说服性写作 | 2 | 0 | **CLEAN_PASS** | +3/-3 |
| 6 | 计算机网络 | 3 | 1 | **CLEAN_WITH_REMAINDERS** | +17/-94 |
| 7 | 细听：古典音乐欣赏指南 | 3 | 0 | **CLEAN_PASS** | +3/-411 |
| 8 | 软件工程匠艺 | 2 | 0 | **CLEAN_PASS** | +1/-6 |
| 9 | 看见彼此——亲密关系的科学 | 1 | 0 | **CLEAN_PASS** | +0/-39 |
| 10 | 睡眠的科学 | 1 | 0 | **CLEAN_PASS** | +2/-41 |
| 11 | 细听：勃拉姆斯 | 1 | 1 | **CLEAN_WITH_REMAINDERS** | +3/-1 |

## 明细

### 机器学习：从数据到智能 — CLEAN_WITH_REMAINDERS

- 路径：`sources/pending/机器学习：从数据到智能.md`
- 字节/行数：635072 / 7532
- 修复前问题数：2
  - systemic_formula_multiple_renderings (~775 latex-command hits)
  - table_cells_corrupted_by_dollar_math_parsing (L2657–2660, L7505–7511)
- 修复后问题数：1
- 修改 hunk 数：1015
- 主要 diff 行范围（旧→新）：
  - L1 → L1
  - L9 → L9
  - L37 → L37
  - L71 → L71
  - L119 → L119
  - L149 → L149
  - L153-L155 → L153-L155
  - L161 → L161
  - L221 → L221
  - L258 → L258
  - L313 → L313
  - L315 → L315
- 处理决定：
  - `formula`：Applied verified local patterns (letter triples, \mathbf wraps, \mathbb powers, assignments, P(·) wraps) plus explicit high-frequency U+L+U replacements and ASCII-safe generic matches; prefer closed LaTeX.
  - `table`：Restored RMSE comparison tables: removed corrupted (/) amount wrappers; normalized headers including Test $R^2$; amounts as 34,500 without $ currency delimiters.（approx L2657–2660 and epilogue L7505–7511）
- 复扫：
  - 伪 H2 表头：无
  - 数学定界外残余 `\command` 行数：684
  - H2 数：28；最终 `---`：True
- 未解决问题：
  - [BLOCKER] `SOURCE_CONFLICT` lines=[313, 315, 353, 359, 367, 371, 379, 391, 393, 401, 403, 407, 413, 415, 421] — Asymmetric unicode/LaTeX triples remain (e.g. pmatrix rows, sum index order differs left vs right).; Cannot safely auto-dedupe without guessing; retain original until human formula pass.; 建议：Manual formula normalization pass before init; do not guess missing braces/subscripts.

### 被讲述的自己——自欺背后的脑科学 — CLEAN_PASS

- 路径：`sources/pending/被讲述的自己——自欺背后的脑科学.md`
- 字节/行数：1098815 / 5282
- 修复前问题数：2
  - table_header_misparsed_as_h2 (L4878)
  - duplicate_long_section (L5109–5129 / L5131–5151)
- 修复后问题数：0
- 修改 hunk 数：2
- 主要 diff 行范围（旧→新）：
  - L4878 → L4878
  - L5110-L5131 → L5109
- 处理决定：
  - `table`：Removed ## from application table header; kept GFM table.（former L4878）
  - `duplicate`：Deleted second copy of closing observations+letter; kept one * * * before Coda.（former L5131–5151）
- 复扫：
  - 伪 H2 表头：无
  - 数学定界外残余 `\command` 行数：0
  - H2 数：16；最终 `---`：True
- 未解决问题：无

### 情绪的科学：识别、调节、不被绑架 — CLEAN_PASS

- 路径：`sources/pending/情绪的科学：识别、调节、不被绑架.md`
- 字节/行数：938480 / 5792
- 修复前问题数：1
  - table_headers_misparsed_as_h2 (L359, L5034, L5047)
- 修复后问题数：0
- 修改 hunk 数：3
- 主要 diff 行范围（旧→新）：
  - L359 → L359
  - L5034 → L5034
  - L5047 → L5047
- 处理决定：
  - `table`：Removed ## from three Move/Emotion table headers; separators/columns intact.（former L359/5034/5047）
- 复扫：
  - 伪 H2 表头：无
  - 数学定界外残余 `\command` 行数：0
  - H2 数：25；最终 `---`：True
- 未解决问题：无

### 压力的科学 — CLEAN_PASS

- 路径：`sources/pending/压力的科学.md`
- 字节/行数：828766 / 6089
- 修复前问题数：2
  - chapter_heading_glued_and_toc_gap (L16, L4141)
  - duplicate_tail_section (L6057–6081 / L6083–6107)
- 修复后问题数：0
- 修改 hunk 数：3
- 主要 diff 行范围（旧→新）：
  - L15 → L16
  - L4141 → L4142-L4145
  - L6060-L6085 → L6063
- 处理决定：
  - `toc`：Inserted Chapter 11 TOC entry between Ch10 and Ch12 from real H2 title.（TOC ~L16）
  - `heading`：Split glued '# Chapter 11...' into ## Chapter 11 heading.（former L4141）
  - `duplicate`：Deleted second closing diagnostic+Chapter Summary; kept single ending.（former L6083–6107）
- 复扫：
  - 伪 H2 表头：无
  - 数学定界外残余 `\command` 行数：0
  - H2 数：16；最终 `---`：True
- 未解决问题：无

### 说服性写作 — CLEAN_PASS

- 路径：`sources/pending/说服性写作.md`
- 字节/行数：586620 / 5422
- 修复前问题数：2
  - table_header_misparsed_as_h2 (L415)
  - table_column_mismatch (L4525–4526)
- 修复后问题数：0
- 修改 hunk 数：2
- 主要 diff 行范围（旧→新）：
  - L415 → L415
  - L4525-L4526 → L4525-L4526
- 处理决定：
  - `table`：Removed ## from 6 Moves table header.（former L415）
  - `table`：Added blank Layer cells for Heart Test / Restrained Connection rows (4 columns).（L4525–4526）
- 复扫：
  - 伪 H2 表头：无
  - 数学定界外残余 `\command` 行数：0
  - H2 数：19；最终 `---`：True
- 未解决问题：无

### 计算机网络 — CLEAN_WITH_REMAINDERS

- 路径：`sources/pending/计算机网络.md`
- 字节/行数：1178444 / 11357
- 修复前问题数：3
  - toc_corruption (L36 fake Chapter 1 / missing Appendix D)
  - duplicate_long_section (L9957–10033 / L10035–10111)
  - table_header_misparsed_as_h2 + column mismatch (L11411)
- 修复后问题数：1
- 修改 hunk 数：5
- 主要 diff 行范围（旧→新）：
  - L36 → L36
  - L66 → L66
  - L72 → L72
  - L10035-L10111 → L10034
  - L11411-L11424 → L11334-L11347
- 处理决定：
  - `toc`：Replaced fake '- Chapter 1: Annotated ping Trace' with Appendix D from real H2.（L36）
  - `duplicate`：Deleted exact duplicate L10035–10111 of Ch27 closing; kept one summary before Appendix A.（former L10035–10111）
  - `table`：Normalized workflows table to | # | Workflow | Chapter | without ##.（Appendix D workflows）
  - `heading`：Promoted Introduction H4 subsections to H3.（Who This Book Is For / What This Book Is Not）
- 复扫：
  - 伪 H2 表头：无
  - 数学定界外残余 `\command` 行数：20
  - H2 数：33；最终 `---`：True
- 未解决问题：
  - [LOW] `intentional_tbd_cell` lines=['~1305'] — Table cell 'TBD' for planned 1.6 Tbps standard; Preflight WARNING; likely intentional pending-standard marker.; 建议：Confirm with control model; no structural block.

### 细听：古典音乐欣赏指南 — CLEAN_PASS

- 路径：`sources/pending/细听：古典音乐欣赏指南.md`
- 字节/行数：1070002 / 6952
- 修复前问题数：3
  - toc_duplicate (L5)
  - editing_scaffold_in_body (L103–454)
  - duplicate_tail_section (L7252–7303 / L7305–7356)
- 修复后问题数：0
- 修改 hunk 数：6
- 主要 diff 行范围（旧→新）：
  - L5 → L4
  - L64 → L63
  - L72 → L71
  - L89 → L88
  - L99-L453 → L97
  - L7305-L7356 → L6948
- 处理决定：
  - `toc`：Deleted corrupted duplicate Chapter 1 TOC entry with stray **.（former L5）
  - `scaffolding`：Removed generation metadata/outline/threading plan between Introduction and Chapter 1; kept formal ## Introduction.（former L103–454）
  - `duplicate`：Deleted second closing cousin-list through _Go listen._（former second closing block）
  - `heading`：Promoted Introduction H4 to H3; cleaned extra * * * before Chapter 1.（Introduction / Chapter 1 boundary）
- 复扫：
  - 伪 H2 表头：无
  - 数学定界外残余 `\command` 行数：0
  - H2 数：29；最终 `---`：True
- 未解决问题：无

### 软件工程匠艺 — CLEAN_PASS

- 路径：`sources/pending/软件工程匠艺.md`
- 字节/行数：891890 / 10988
- 修复前问题数：2
  - toc_duplicate Introduction (L5/L29)
  - table_header_misparsed_as_h2 (L10606)
- 修复后问题数：0
- 修改 hunk 数：3
- 主要 diff 行范围（旧→新）：
  - L29 → L28
  - L10606 → L10605
  - L10989-L10992 → L10987
- 处理决定：
  - `toc`：Removed duplicate trailing '- Introduction' TOC entry.（former L29）
  - `table`：Removed ## from Appendix B table header.（former L10606）
  - `separator`：Collapsed excess * * * to one chapter end + final ---.（file end）
- 复扫：
  - 伪 H2 表头：无
  - 数学定界外残余 `\command` 行数：3
  - H2 数：26；最终 `---`：True
- 未解决问题：无

### 看见彼此——亲密关系的科学 — CLEAN_PASS

- 路径：`sources/pending/看见彼此——亲密关系的科学.md`
- 字节/行数：871100 / 3838
- 修复前问题数：1
  - duplicate_tail_section (L3719–3756 / L3758–3795)
- 修复后问题数：0
- 修改 hunk 数：1
- 主要 diff 行范围（旧→新）：
  - L3724-L3762 → L3723
- 处理决定：
  - `duplicate`：Deleted second Think Deeper/Summary/Begin/For deeper reading block; kept one before Appendix.（former L3758–3795）
- 复扫：
  - 伪 H2 表头：无
  - 数学定界外残余 `\command` 行数：0
  - H2 数：17；最终 `---`：True
- 未解决问题：无

### 睡眠的科学 — CLEAN_PASS

- 路径：`sources/pending/睡眠的科学.md`
- 字节/行数：794209 / 7091
- 修复前问题数：1
  - duplicate_tail_section (L7050–7087 / L7089–7126)
- 修复后问题数：0
- 修改 hunk 数：3
- 主要 diff 行范围（旧→新）：
  - L55 → L55
  - L67 → L67
  - L7060-L7098 → L7059
- 处理决定：
  - `duplicate`：Deleted second closing argument+Summary+Diary instruction; kept one ending.（former L7089–7126）
  - `heading`：Promoted Introduction H4 to H3.（What This Book Is/Not）
- 复扫：
  - 伪 H2 表头：无
  - 数学定界外残余 `\command` 行数：0
  - H2 数：16；最终 `---`：True
- 未解决问题：无

### 细听：勃拉姆斯 — CLEAN_WITH_REMAINDERS

- 路径：`sources/pending/细听：勃拉姆斯.md`
- 字节/行数：480178 / 2817
- 修复前问题数：1
  - body_misparsed_as_h3 Read item (L2807–2815)
- 修复后问题数：1
- 修改 hunk 数：1
- 主要 diff 行范围（旧→新）：
  - L2813 → L2813-L2815
- 处理决定：
  - `heading`：Changed ### **Read** to plain **Read** paragraph under Going Deeper.（former ~L2813）
  - `separator`：Ensured * * * + --- final separators.（file end）
- 复扫：
  - 伪 H2 表头：无
  - 数学定界外残余 `\command` 行数：0
  - H2 数：24；最终 `---`：True
- 未解决问题：
  - [LOW] `opaque_cross_volume_ref` lines=[43, 45] — B159 Close Listening internal id; Preflight WARNING; opaque series code.; 建议：Optionally expand to full volume title on next edit pass.

## 说明

- `CLEAN_PASS`：报告登记的阻断项已修复，复扫无伪 H2/重复尾/目录损坏。
- `CLEAN_WITH_REMAINDERS`：可晋升登记，但仍有 SOURCE_CONFLICT 或低优先级 WARNING。
- `BLOCK`：仍存在会污染 init/锁标题的结构问题。
- 《机器学习》公式：禁止猜测；不对左右 unicode 不一致的三重渲染做盲替换；金额表已修复。
