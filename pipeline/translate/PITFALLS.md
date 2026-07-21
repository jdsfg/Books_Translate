> ## 📌 文件名铁律（最高频踩坑点 · 先读这一段）
> 本流水线有两套文件名，**极易混淆，务必分清**：
> - **块级译文** = `translate/<书名>/blocks/<块id>.md`（**注意：不带 `.zh`！**）。这是 `commit` 实际写入的文件（见 `translate_book.py` 第241行）。你翻译的每一块最终都落在这里。
> - **临时译文文件** = 你先 `write_to_file` 写成 `<块id>.md`（同样**不带 `.zh`**），再用 `commit ... --file` 喂给它。
> - **最终成稿** = `成稿存档/<书名>.zh.md`（**这个带 `.zh`**），是 `assemble` 产物（不要手改）。
> ⚠️ 本文其余处若出现 `blocks/<块id>.zh.md` 字样，一律是笔误，就是指 `blocks/<块id>.md`；只有成稿的 `<书名>.zh.md` 才带 `.zh`。务必别自己另建目录（如 `_src/`、`_tmp_*`）或把译文写到工作目录根，所有译文只走 `commit` 落进 `blocks/`。
>
# 翻译流水线 PITFALLS（坑位清单）

> 目的：把翻译执行中踩过的、会"卡很久 / 误报失败 / 重来"的坑集中在此。任何 agent 接手翻译前**先读此文件**，避免每回重踩拖慢推进。
> 配套脚本：`../translate_book.py`；方案：`../翻译总体方案.md`；风格简报：`style_*.md`；术语库：`glossary_*.md`。

---

## ⛔ 坑 1：`commit` 必须加 `--file`，否则永久阻塞超时（最严重，曾卡很久）

**现象**：早期 `commit` 支持从 stdin 读译文（`sys.stdin.read()`）。但工具调用命令时 stdin 是**常开管道**，`read()` 一直等 EOF 不来 → 整个命令卡到超时（分钟级），看起来像"卡死"。

**已修复**：`commit` 的 stdin 路径已**彻底废弃**，现在无 `--file` 直接报错退出（`sys.exit(2)`），不再阻塞。

**规则（铁律）**：
```
# ✅ 正确——永远从文件读译文
python translate_book.py commit <src.md> <bid> --file <译文文件.md>

# ❌ 错误——会直接报错退出
python translate_book.py commit <src.md> <bid>
python translate_book.py commit <src.md> <bid> < 某文件   # 也不走 stdin 了
```
译文一律先 `write_to_file` 写成 `<块id>.md` 临时文件（**不带 `.zh`**），再 `--file` 落盘。

---

## ⛔ 坑 2：PowerShell 里给 `status` / `assemble` 套 `Select-String -NotMatch` 会吞掉正常输出，误报"运行不了"

**现象**：为过滤 oh-my-posh 噪声，曾用 `... | Select-String -NotMatch "oh-my-posh"`。结果**正常输出也被一起吞掉**，工具误报 `Tool execution failed: No result found` / 看起来卡死。其实脚本早就跑完了。

**规则**：
- `status` / `assemble` / `next` 这类**查看类命令，裸跑，不要二次过滤**。
- 想要干净输出，只在命令**末尾加 `2>$null`** 压制 profile 噪声即可（oh-my-posh 那几行红字是 PowerShell 个人配置报错，无害，可无视）。
- 不要再用 `Select-String -NotMatch` 包裹——它会误伤。

```powershell
# ✅ 正确：裸跑或仅 2>$null
python translate_book.py status <src.md> 2>$null

# ❌ 错误：会吞输出假死
python translate_book.py status <src.md> 2>$null | Select-String -NotMatch "oh-my-posh"
```

---

## ⚠️ 坑 3：`.zh.md`（成稿存档里的译本）**禁止手改**，会被 `assemble` 覆盖

**现象**：`assemble` 每次都按 `blocks/<bid>.zh.md` 重新拼装中文 `.zh.md`。若直接在成稿存档的 `.zh.md` 上手改，下次 assemble 直接覆盖丢改动。

**规则**：所有译文改动**只走 `commit`**（写 `blocks/`，再 assemble）。要改某块就重写对应 `blocks/<bid>.zh.md` 再 commit。

---

## ⚠️ 坑 4：翻译前必须先 `lock-titles`，否则目录/章节标题没本地化

**现象**：`next` / `commit` 依赖已锁定的中文标题映射（`titles_zh.json`）。没 lock 就翻，目录和 `##` 标题仍是英文，后续要返工。

**规则**：每本新书流程第一步永远是 `init` → `lock-titles <src> <titles_zh.json>` → 才 `next`。标题锁定后一般不再改。

---

## ⚠️ 坑 5：`assemble` 必须晚于 `commit`，且依赖 `blocks/` 已落盘

**规则**：commit 若干块后，再跑 `assemble <src>` 才会把这些块拼进中文 `.zh.md`。只想看某块进度用 `status` / `next --show`，不要误以为 assemble 能凭空生成。

---

## ⚠️ 坑 6：中文路径 / 中文文件名在 Python 里正常，但命令里要写绝对路径

**已验证**：`D:\...\身体这台机器：随身硬件巡礼.md` 这类含中文+冒号的文件名，Python `read_text/write_text(encoding='utf-8')` 全正常；PowerShell 命令里也正常（用绝对路径即可）。

**注意**：Windows 文件名里允许 `：` 冒号（中文全角冒号 `：` 更没问题），但**不要把 md 当 PowerShell 脚本路径**（`.ps1`/`.bat` 非 ASCII 路径会乱码——属另一条线，翻译这里不涉及）。

---

## 🔁 失败块处理（设计项，已就位）

- 块级检查点在 `blocks/<bid>.zh.md`；`status` 看 `done/pending/failed`。
- 单块失败：写 `retry_queue` + `failures`；`fail` / `retry` 子命令管理。
- **自动循环（未来接）**：指数退避 + 失败块单独重试队列——检查点精确到**块**而非本，断点续翻不丢进度。

---

## ✅ 标准一键检查（不踩坑的姿势）

```powershell
$env:SRC="D:\HuaweiMoveData\Users\淡水海边\Desktop\Postgraduate\项目\MySelf\Archive\成稿存档\身体这台机器：随身硬件巡礼.md"
$env:WD="D:\HuaweiMoveData\Users\淡水海边\Desktop\Postgraduate\项目\MySelf\Archive\书库抓取工具\translate\身体这台机器：随身硬件巡礼"

# 看进度（裸跑）
python translate_book.py status $env:SRC 2>$null

# 取下一个待译块（看源文）
python translate_book.py next $env:SRC 2>$null

# 落盘一块译文（必须 --file）
python translate_book.py commit $env:SRC c02_b01 --file "$env:WD\c02_b01.md" 2>$null

# 拼装预览（裸跑）
python translate_book.py assemble $env:SRC 2>$null
```

---
_最后更新：2026-07-19。坑 1/坑 2 为本日"卡很久 / 运行不了"假象的根因，已固化修复 + 此文档。_

---

## 📌 数字规则按体裁分类（2026-07-19 Devin 审查 P1-1 · 已落地）

**坑**：曾把 "about 100,000 times a day" 译成"约十万次"——虽在**科普散文**可接受，但技术/统计/金融/会计书把 `100,000→十万`、`3.5%→百分之三点五` 会出事。

**规则（写进各系列 `style_*.md`）**：
- **科普散文**：约整数/顺口数词可用中文（十万、六十到一百）；但精确测量值/单位/百分比/频率/统计/日期/编号/公式数 → **仍保留阿拉伯数字 + 原单位**。
- **技术/统计/金融/会计/理科书**：**所有数字强制阿拉伯数字 + 原单位**，中文数词约化零容忍。

**校验**：理科/技术书翻完跑 `verify_translation.py <src> --force-arabic`，源块阿拉伯数字集必须在译块中基本一致，缺失会报 WARN（加 `--strict` 升 ERROR）。

---

## 📌 导读切块（P1-2 · 已落地）

**坑**：旧 `init` 把整段导读塞进单个 `intro` 块；导读长的书会产生超窗口巨块，翻译截断/降质。

**已修复**：`init` 现在对长导读跑 `split_blocks` → 切成 `intro_b01 / intro_b02 ...`（短导读仍单块 `intro`）。`assemble` 同时兼容 `intro` 与 `intro_bNN` 两种前缀；旧 checkpoint（单 `intro`）不受影响，回退逻辑保证一致。

---

## 📌 译文结构校验脚本（P1-3 · 已落地，勿回译兜底）

**脚本**：`translate/verify_translation.py`（轻量、便宜、可全量跑）。

**做什么**：逐块比对 源↔译 的 `###`/`####` 标题数、代码围栏 ```` ``` ```` 数、LaTeX `$`/`$$` 数、表格 `|` 行数、脚注数；不一致即报警。可选 `--force-arabic` 数字集校验、`--glossary <术语库.md>` 术语合规。

**铁律：不要用"长度比"判异常**。EN→ZH 字符比天然只有 0.2–0.35（本书实测 intro 0.34、c01_b01 0.22），同语种比例阈值会把每一块都误报。回译只留 ~5% 抽样兜底，主校验走结构比对。

```powershell
python verify_translation.py $env:SRC 2>$null
python verify_translation.py $env:SRC --force-arabic --glossary "$env:WD\..\glossary_xxx.md" 2>$null
```

---

## 📌 切块优先按标题边界（P2 · 已落地）

`split_blocks` 现在**先按 `##/###/####` 标题边界切段**，段内再按大小切。避免把子小节从中间劈开、伤上下文连贯与术语注入命中。旧 checkpoint 用 legacy 版回退，互不影响。

---

## 📌 EPUB 闸门（P2 · 纪律）

`assemble` 对未译章节会输出空的 `## 第X章` + 空行（进行中无害）。**构建 EPUB 前必须以 `status` 的 `done == total` 为闸门**——绝不把含空章的 `.zh.md` 送进 EPUB。

---

## 📌 临时文件清理（P2 · 纪律）

翻译流程收尾时清理 `translate/<书名>/_tmp_*.zh.md`（与 `blocks/<bid>.zh.md` 重复，属临时文件），避免和正式块混淆。正式块只在 `blocks/` 下。

---

## 📌 verify 章级标题总量比对陷阱（2026-07-19 深夜补 · 已修）

**坑**：`verify_translation.py` 做 h3/h4 块级比对时，要判定"块级差异是 legacy 切块把 `###` 从边界劈开造成的伪差"还是"真丢失"，需拿**整章源文标题总量**和**整章译文总量**比。

- 整章源文总量**必须来自 `tb.parse_source(src)` 重新整章统计**（变量 `true_chap`），**绝不能**累加每块 legacy 源（legacy 切块会把 `###` 标题切在块边界，导致"按块累加的源文标题数"被通胀，反而误报）。
- **曾因误写变量名 `chap_src`（未定义）→ 一旦某块 h3/h4 不匹配就 `NameError` 崩溃而非降级伪差**，已改为 `true_chap.get(c,{}).get(k,0) == chap_zh.get(c,{}).get(k,0)`。若日后动这块逻辑，变量名对照 `true_chap` / `chap_zh` 两字典，别再用不存在的 `chap_src`。

---

_最后更新：2026-07-19。坑 1/坑 2 为本日卡很久/运行不了假象根因；另按 Devin 审查落地 P1-1（数字分类）/P1-2（导读切块）/P1-3（结构校验脚本）+ P2（标题边界切块/EPUB闸门/临时文件清理）；深夜补 verify 章级比对变量名崩溃坑（已修）。_
