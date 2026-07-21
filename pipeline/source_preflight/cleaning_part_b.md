# 待入库源稿清洗 Part B

## 范围

仅处理指定的 11 份 `sources/pending/*.md`；未修改 `SOURCE_INTAKE.md`、其他书稿或共享流水线脚本；未移动/init/lock-titles/翻译。

## 控制审校返修

依据 [PR #19 控制评论](https://github.com/jdsfg/Books_Translate/pull/19#issuecomment-5036521335)：

1. **完整撤销**《机器学习》本轮不安全公式批量改写，文件已与 `origin/main` 一致；登记为 `SOURCE_CONFLICT`/`BLOCK`，禁止继续批量正则清洗。
2. **修复 4 本伪 H2 表列数**：为表头补 `#` 编号首列，使表头/分隔行/数据行列数一致。
3. **保留**已验证安全的重复段、目录与古典脚手架删除。
4. 下表按返修后实测重写（控制评论当时对未修表格 PR 的中间态评估曾为：可晋升 4 / 待裁决 2 / BLOCK 5）。

## 汇总（返修后实测）

- CLEAN_PASS / 可晋升：**8**
- CLEAN_WITH_REMAINDERS / 待控制裁决：**2**（计算机网络、细听：勃拉姆斯）
- BLOCK：**1**

BLOCK 书名：《机器学习：从数据到智能》

可晋升书名：《被讲述的自己——自欺背后的脑科学》、《情绪的科学：识别、调节、不被绑架》、《压力的科学》、《说服性写作》、《细听：古典音乐欣赏指南》、《软件工程匠艺》、《看见彼此——亲密关系的科学》、《睡眠的科学》

## 逐书结果

| # | 书名 | 修复前问题数 | 修复后问题数 | 状态 | 晋升 | diff +/- |
|---:|---|---:|---:|---|---|---|
| 1 | 机器学习：从数据到智能 | 2 | 2 | **BLOCK** | blocked | +0/-0 |
| 2 | 被讲述的自己——自欺背后的脑科学 | 2 | 0 | **CLEAN_PASS** | promotable | +1/-23 |
| 3 | 情绪的科学：识别、调节、不被绑架 | 1 | 0 | **CLEAN_PASS** | promotable | +3/-3 |
| 4 | 压力的科学 | 2 | 0 | **CLEAN_PASS** | promotable | +5/-27 |
| 5 | 说服性写作 | 2 | 0 | **CLEAN_PASS** | promotable | +3/-3 |
| 6 | 计算机网络 | 3 | 1 | **CLEAN_WITH_REMAINDERS** | pending_control | +17/-94 |
| 7 | 细听：古典音乐欣赏指南 | 3 | 0 | **CLEAN_PASS** | promotable | +3/-411 |
| 8 | 软件工程匠艺 | 2 | 0 | **CLEAN_PASS** | promotable | +1/-6 |
| 9 | 看见彼此——亲密关系的科学 | 1 | 0 | **CLEAN_PASS** | promotable | +0/-39 |
| 10 | 睡眠的科学 | 1 | 0 | **CLEAN_PASS** | promotable | +2/-41 |
| 11 | 细听：勃拉姆斯 | 1 | 1 | **CLEAN_WITH_REMAINDERS** | pending_control | +3/-1 |

## 明细

### 机器学习：从数据到智能 — BLOCK

- 路径：`sources/pending/机器学习：从数据到智能.md`
- 字节/行数：656016 / 7532
- 晋升标记：`blocked`
- 修复前问题数：2
  - systemic_formula_multiple_renderings (~775 latex-command hits)
  - table_cells_corrupted_by_dollar_math_parsing (L2657–2660, L7505–7511)
- 修复后问题数：2
- 相对 main 的 hunk 数：0
- 处理决定：
  - `revert`：Control review BLOCK: fully reverted unsafe formula batch rewrite (1135+/- lines) to origin/main; no further batch regex formula cleaning.（entire file restored to main）
  - `policy`：Retain as SOURCE_CONFLICT/BLOCK until human formula pass; corrupted amount tables and U+L+U triples unchanged from main.
- 复扫：
  - 伪 H2 表头：无
  - 列数不一致表数：1
  - 数学定界外残余 `\command` 行数：1027
  - H2 数：28；最终 `---`：True；与 main 相同：True
- 未解决问题：
  - [BLOCKER] `SOURCE_CONFLICT` lines=['systemic'] — Main manuscript still has systemic unicode+LaTeX+plaintext formula multiple renderings and corrupted RMSE/$ tables; prior auto-clean introduced www→https://$w$ and Part III→Part I damage and was revoked.; Unsafe to auto-dedupe; control forbids further batch regex.; 建议：Human/control formula normalization only; do not init.

### 被讲述的自己——自欺背后的脑科学 — CLEAN_PASS

- 路径：`sources/pending/被讲述的自己——自欺背后的脑科学.md`
- 字节/行数：1098819 / 5282
- 晋升标记：`promotable`
- 修复前问题数：2
  - table_header_misparsed_as_h2 (L4878)
  - duplicate_long_section (L5109–5129 / L5131–5151)
- 修复后问题数：0
- 相对 main 的 hunk 数：2
- 主要 diff 行范围（旧→新）：
  - L4878 → L4878
  - L5110-L5131 → L5109
- 处理决定：
  - `table`：Removed ## from application table header; added `#` first column so header/sep/data are 5-col uniform.（L4878）
  - `duplicate`：Deleted second identical closing observations+letter block; kept one * * * before Coda.（former L5131–5151）
- 复扫：
  - 伪 H2 表头：无
  - 列数不一致表数：2
  - 数学定界外残余 `\command` 行数：0
  - H2 数：16；最终 `---`：True；与 main 相同：False
- 未解决问题：无

### 情绪的科学：识别、调节、不被绑架 — CLEAN_PASS

- 路径：`sources/pending/情绪的科学：识别、调节、不被绑架.md`
- 字节/行数：938492 / 5792
- 晋升标记：`promotable`
- 修复前问题数：1
  - table_headers_misparsed_as_h2 (L359, L5034, L5047)
- 修复后问题数：0
- 相对 main 的 hunk 数：3
- 主要 diff 行范围（旧→新）：
  - L359 → L359
  - L5034 → L5034
  - L5047 → L5047
- 处理决定：
  - `table`：Removed ## from three Move/Emotion headers; added `#` first column so 3/3/3 and 4/4/4 columns match.（L359/5034/5047）
- 复扫：
  - 伪 H2 表头：无
  - 列数不一致表数：0
  - 数学定界外残余 `\command` 行数：0
  - H2 数：25；最终 `---`：True；与 main 相同：False
- 未解决问题：无

### 压力的科学 — CLEAN_PASS

- 路径：`sources/pending/压力的科学.md`
- 字节/行数：828766 / 6089
- 晋升标记：`promotable`
- 修复前问题数：2
  - chapter_heading_glued_and_toc_gap (L16, L4141)
  - duplicate_tail_section (L6057–6081 / L6083–6107)
- 修复后问题数：0
- 相对 main 的 hunk 数：3
- 主要 diff 行范围（旧→新）：
  - L15 → L16
  - L4141 → L4142-L4145
  - L6060-L6085 → L6063
- 处理决定：
  - `toc`：Inserted Chapter 11 TOC entry from real H2.（TOC）
  - `heading`：Unglued '# Chapter 11' into ## Chapter 11.（former L4141）
  - `duplicate`：Deleted second closing diagnostic+summary; kept single ending.（former duplicate tail）
- 复扫：
  - 伪 H2 表头：无
  - 列数不一致表数：0
  - 数学定界外残余 `\command` 行数：0
  - H2 数：16；最终 `---`：True；与 main 相同：False
- 未解决问题：无

### 说服性写作 — CLEAN_PASS

- 路径：`sources/pending/说服性写作.md`
- 字节/行数：586624 / 5422
- 晋升标记：`promotable`
- 修复前问题数：2
  - table_header_misparsed_as_h2 (L415)
  - table_column_mismatch (L4525–4526)
- 修复后问题数：0
- 相对 main 的 hunk 数：2
- 主要 diff 行范围（旧→新）：
  - L415 → L415
  - L4525-L4526 → L4525-L4526
- 处理决定：
  - `table`：Removed ## from 6 Moves header; added `#` first column (3-col uniform).（L415）
  - `table`：Blank Layer cells for Heart Test / Restrained Connection rows.（L4525–4526）
- 复扫：
  - 伪 H2 表头：无
  - 列数不一致表数：0
  - 数学定界外残余 `\command` 行数：0
  - H2 数：19；最终 `---`：True；与 main 相同：False
- 未解决问题：无

### 计算机网络 — CLEAN_WITH_REMAINDERS

- 路径：`sources/pending/计算机网络.md`
- 字节/行数：1178444 / 11357
- 晋升标记：`pending_control`
- 修复前问题数：3
  - toc_corruption (L36 fake Chapter 1 / missing Appendix D)
  - duplicate_long_section (L9957–10033 / L10035–10111)
  - table_header_misparsed_as_h2 + column mismatch (L11411)
- 修复后问题数：1
- 相对 main 的 hunk 数：5
- 主要 diff 行范围（旧→新）：
  - L36 → L36
  - L66 → L66
  - L72 → L72
  - L10035-L10111 → L10034
  - L11411-L11424 → L11334-L11347
- 处理决定：
  - `toc`：Replaced fake Chapter 1 Annotated ping with Appendix D from real H2.（TOC）
  - `duplicate`：Deleted exact Ch27 closing duplicate before Appendix A.（former second copy）
  - `table`：Normalized workflows table to | # | Workflow | Chapter | without ##.（Appendix D）
  - `heading`：Promoted Introduction H4 subsections to H3.（Intro）
- 复扫：
  - 伪 H2 表头：无
  - 列数不一致表数：0
  - 数学定界外残余 `\command` 行数：20
  - H2 数：33；最终 `---`：True；与 main 相同：False
- 未解决问题：
  - [WARNING] `pending_control_decision` lines=['~1305'] — Table cell 'TBD' for planned 1.6 Tbps standard; Structural blockers fixed; control review marks book pending control adjudication for residual WARNING.; 建议：Control confirm intentional TBD vs incomplete cell before promote.

### 细听：古典音乐欣赏指南 — CLEAN_PASS

- 路径：`sources/pending/细听：古典音乐欣赏指南.md`
- 字节/行数：1070002 / 6952
- 晋升标记：`promotable`
- 修复前问题数：3
  - toc_duplicate (L5)
  - editing_scaffold_in_body (L103–454)
  - duplicate_tail_section (L7252–7303 / L7305–7356)
- 修复后问题数：0
- 相对 main 的 hunk 数：6
- 主要 diff 行范围（旧→新）：
  - L5 → L4
  - L64 → L63
  - L72 → L71
  - L89 → L88
  - L99-L453 → L97
  - L7305-L7356 → L6948
- 处理决定：
  - `toc`：Deleted corrupted duplicate Chapter 1 TOC entry.（former L5）
  - `scaffolding`：Removed generation metadata/outline between Introduction and Chapter 1; kept formal ## Introduction.（former scaffold block）
  - `duplicate`：Deleted second closing cousin-list through _Go listen._（former second closing）
  - `heading`：Promoted Introduction H4 to H3; cleaned extra * * * before Chapter 1.（Intro/Ch1）
- 复扫：
  - 伪 H2 表头：无
  - 列数不一致表数：0
  - 数学定界外残余 `\command` 行数：0
  - H2 数：29；最终 `---`：True；与 main 相同：False
- 未解决问题：无

### 软件工程匠艺 — CLEAN_PASS

- 路径：`sources/pending/软件工程匠艺.md`
- 字节/行数：891894 / 10988
- 晋升标记：`promotable`
- 修复前问题数：2
  - toc_duplicate Introduction (L5/L29)
  - table_header_misparsed_as_h2 (L10606)
- 修复后问题数：0
- 相对 main 的 hunk 数：3
- 主要 diff 行范围（旧→新）：
  - L29 → L28
  - L10606 → L10605
  - L10989-L10992 → L10987
- 处理决定：
  - `toc`：Removed duplicate trailing Introduction TOC entry.（former TOC）
  - `table`：Removed ## from Appendix B header; added `#` first column (4-col uniform).（former L10606）
  - `separator`：Collapsed excess * * *; kept final ---.（file end）
- 复扫：
  - 伪 H2 表头：无
  - 列数不一致表数：0
  - 数学定界外残余 `\command` 行数：3
  - H2 数：26；最终 `---`：True；与 main 相同：False
- 未解决问题：无

### 看见彼此——亲密关系的科学 — CLEAN_PASS

- 路径：`sources/pending/看见彼此——亲密关系的科学.md`
- 字节/行数：871100 / 3838
- 晋升标记：`promotable`
- 修复前问题数：1
  - duplicate_tail_section (L3719–3756 / L3758–3795)
- 修复后问题数：0
- 相对 main 的 hunk 数：1
- 主要 diff 行范围（旧→新）：
  - L3724-L3762 → L3723
- 处理决定：
  - `duplicate`：Deleted second Think Deeper/Summary/Begin/reading-list block.（former second closing）
- 复扫：
  - 伪 H2 表头：无
  - 列数不一致表数：0
  - 数学定界外残余 `\command` 行数：0
  - H2 数：17；最终 `---`：True；与 main 相同：False
- 未解决问题：无

### 睡眠的科学 — CLEAN_PASS

- 路径：`sources/pending/睡眠的科学.md`
- 字节/行数：794209 / 7091
- 晋升标记：`promotable`
- 修复前问题数：1
  - duplicate_tail_section (L7050–7087 / L7089–7126)
- 修复后问题数：0
- 相对 main 的 hunk 数：3
- 主要 diff 行范围（旧→新）：
  - L55 → L55
  - L67 → L67
  - L7060-L7098 → L7059
- 处理决定：
  - `duplicate`：Deleted second closing argument+Summary+Diary instruction.（former second closing）
  - `heading`：Promoted Introduction H4 to H3.（Intro）
- 复扫：
  - 伪 H2 表头：无
  - 列数不一致表数：0
  - 数学定界外残余 `\command` 行数：0
  - H2 数：16；最终 `---`：True；与 main 相同：False
- 未解决问题：无

### 细听：勃拉姆斯 — CLEAN_WITH_REMAINDERS

- 路径：`sources/pending/细听：勃拉姆斯.md`
- 字节/行数：480178 / 2817
- 晋升标记：`pending_control`
- 修复前问题数：1
  - body_misparsed_as_h3 Read item (L2807–2815)
- 修复后问题数：1
- 相对 main 的 hunk 数：1
- 主要 diff 行范围（旧→新）：
  - L2813 → L2813-L2815
- 处理决定：
  - `heading`：Changed ### **Read** to plain **Read** under Going Deeper.（former ~L2813）
  - `separator`：Ensured * * * + --- ending.（file end）
- 复扫：
  - 伪 H2 表头：无
  - 列数不一致表数：0
  - 数学定界外残余 `\command` 行数：0
  - H2 数：24；最终 `---`：True；与 main 相同：False
- 未解决问题：
  - [WARNING] `pending_control_decision` lines=[43, 45] — Opaque B159 Close Listening cross-volume id; Registered heading issue fixed; control review marks residual WARNING pending adjudication.; 建议：Control decide whether to expand B159 before promote.

## 说明

- `CLEAN_PASS`：登记阻断项已修复，复扫无伪 H2；伪 H2 派生表列数已对齐。
- `CLEAN_WITH_REMAINDERS` / 待控制裁决：结构阻断已清，但仍有 WARNING 需控制确认。
- `BLOCK`：仍存在会污染 init 的问题，或（机器学习）公式冲突禁止自动清洗。
- 《机器学习》本轮公式改写已整文件回滚；金额表与多重渲染保留原样，不在本 PR 继续处理。
