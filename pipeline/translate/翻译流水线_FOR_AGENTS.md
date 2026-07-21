> ## 📌 文件名铁律（最高频踩坑点 · 先读这一段）
> 本流水线有两套文件名，**极易混淆，务必分清**：
> - **块级译文** = `translate/<书名>/blocks/<块id>.md`（**注意：不带 `.zh`！**）。这是 `commit` 实际写入的文件（见 `translate_book.py` 第241行 `(self.work/'blocks'/f"{bid}.md")`）。你翻译的每一块最终都落在这里。
> - **临时译文文件** = 你先 `write_to_file` 写成 `<块id>.md`（同样**不带 `.zh`**），再用 `commit ... --file` 喂给它。
> - **最终成稿** = `成稿存档/<书名>.zh.md`（**这个带 `.zh`**），是 `assemble` 产物（不要手改）。
> ⚠️ 本文其余处若出现 `blocks/<块id>.zh.md` 字样，一律是笔误，就是指 `blocks/<块id>.md`；只有成稿的 `<书名>.zh.md` 才带 `.zh`。务必别自己另建目录（如 `_src/`、`_tmp_*`）或把译文写到工作目录根，所有译文只走 `commit` 落进 `blocks/`。
>
# 翻译流水线 · 智能体自助合同（FOR_AGENTS）

> 你是被派去翻译**一本书**的 agent。本文件是你开工前**必须通读**的唯一合同。读完后立即读同级 `PITFALLS.md`（那里有会让你卡死/假死的坑，先避开）。然后严格按 §2 固定序列执行。
> 配套脚本：`translate_book.py`、`verify_translation.py`（在 `..\` 即 `书库抓取工具\` 下）。方案总纲：`..\翻译总体方案.md`。风格简报：`style_<系列>.md`。术语库：`glossary_<领域>.md`。

---

## 🔥 质量铁律（最高优先级 · 压倒一切）

- **质量优先，不省 token。** 翻译这门活 user 明确：宁可多花轮次、多消耗 token，也绝不偷工减料。token 不封顶，别为省 token 压缩输出。
- **逐块精翻，不跳段、不摘要式翻译。** 每块原文都要完整、忠实、可读地译出；**严禁**用「以下略」「详见原文」「概括为」式偷懒；严禁整段跳过或只译大意。
- **长文不怕多轮。** 一块太长就分多轮译完再 `commit`；术语拿不准就查 `glossary_<领域>.md` / 网络确认，不要瞎猜硬翻。
- **质量 > 速度。** 中转监控平台（编排者）会抽章审文气/精度；质量不达标打回重译，没有「先交差再补」的余地。
- 这条铁律优先于一切「快进」冲动。其余 § 是流程纪律，这条是价值观底线。

---

## §0 总览与你的边界

- 你只负责**一本书**。别的书由别的 agent 负责，你们**共享只读资产**（脚本 / 风格简报 / 术语库 / PITFALLS），但**各自工作目录互不相干**。
- 你的工作目录：`translate\<书名>\`；块级检查点在 `translate\<书名>\blocks\<bid>.zh.md`。
- **绝不修改** `books_registry.md`（那是台账，由编排者统一合并）。你完工后只写一个 `DONE_<书名>.flag` 文件。
- **绝不手改** `成稿存档\<书名>.zh.md`（那是 assemble 产物，会被覆盖）。所有译文改动只走 `commit`。

---

## §1 开工前必读（顺序）

1. 本文件（合同）。
2. 同级 `PITFALLS.md`（坑 1 / 坑 2 会卡死或假死，必看）。
3. 本书对应的 `style_<系列>.md`（体裁质量标准）。
4. 本书对应的 `glossary_<领域>.md`（术语锁定译法）。

---

## §2 固定执行序列（铁律，照抄命令）

设变量（PowerShell，路径用绝对路径）：

```powershell
$env:TB="D:\HuaweiMoveData\Users\淡水海边\Desktop\Postgraduate\项目\MySelf\Archive\书库抓取工具\translate_book.py"
$env:VT="D:\HuaweiMoveData\Users\淡水海边\Desktop\Postgraduate\项目\MySelf\Archive\书库抓取工具\verify_translation.py"
$env:SRC="D:\HuaweiMoveData\Users\淡水海边\Desktop\Postgraduate\项目\MySelf\Archive\成稿存档\<书名>.md"
$env:WD="D:\HuaweiMoveData\Users\淡水海边\Desktop\Postgraduate\项目\MySelf\Archive\书库抓取工具\translate\<书名>"
$env:STYLE="D:\HuaweiMoveData\Users\淡水海边\Desktop\Postgraduate\项目\MySelf\Archive\书库抓取工具\translate\style_<系列>.md"
$env:GLOS="D:\HuaweiMoveData\Users\淡水海边\Desktop\Postgraduate\项目\MySelf\Archive\书库抓取工具\translate\glossary_<领域>.md"
$env:PY="D:\Python\python.exe"   # 系统 python；若不在 PATH 用绝对路径
```

步骤：

1. **初始化**：`python $env:TB init $env:SRC` —— 建工作目录 + 切块。
2. **生成并锁标题**（不锁不准翻，`titles_zh.json` 需你亲手造，init 不会生成它）：
   - a) 列出全部英文章题：`python $env:TB titles $env:SRC`（输出 `章号<TAB>英文题<TAB>中文题`，中文列初始为空）。
   - b) 你按 `style_<系列>.md` 的「标题/术语处理」+ `glossary_<领域>.md` 统一翻译**全部**标题。
   - c) 在 `$env:WD` 手写 `titles_zh.json`，格式：`{"c01": "第1章 …", "c02": "第2章 …", "intro": "导读"}`（键用步骤 a 输出的章号，值为你的中文题）。
   - d) 锁定：`python $env:TB lock-titles $env:SRC "$env:WD\titles_zh.json"`。
   - ⚠️ **编号偏移**：`## Introduction` 会成为 `c01`，于是 Chapter 1 = `c02`、Chapter 2 = `c03`……以此类推，对标题时以步骤 a 的实际输出为准，别按直觉编号。
   - ⚠️ **已有中文导读**：部分书（如《明智决策》）先前补写过中文 `## 导读`，会并入 `intro` 块——该块**已是中文，next 取到后照抄 commit 即可，不要再翻**。
3. **粗扫本书术语（两遍法第一遍）**：锁标题后，通读本书源文一遍，抽出本书高频/易歧义术语，连同你定的中文译法写进**本书工作目录内**的 `$env:WD\glossary_local.md`（与共享库同格式 `en | zh`）。
   - ⚠️ **共享 `glossary_<领域>.md` 只读，严禁追加**（多窗口并行写会冲突）。新术语一律进 `glossary_local.md`。
   - 翻译时**两库并用**：命中共享库用共享译法，命中本地库用本地译法，两库都没有再现译并回填本地库。
   - 完工后编排者会把有共用价值的本地条目合并回系列库。
4. **逐块循环**：
   - 取块：`python $env:TB next $env:SRC`（裸跑，不过滤）
   - 你翻译该块 → 写成临时文件 `<块id>.zh.md`（**严格保留**代码/公式/表格/脚注/Markdown 层级，只译散文；遵循 `style_<系列>.md` 质量标准；命中 `glossary_<领域>.md` 的术语用锁定译法）。
   - 落盘：`python $env:TB commit $env:SRC <块id> --file "$env:WD\<块id>.md"` —— **必须 `--file`**，否则直接报错退出（坑 1）。
   - 每译若干块跑一次：`python $env:TB assemble $env:SRC`（裸跑）。
5. **全部块 commit 后**：`python $env:TB assemble $env:SRC` + `python $env:VT $env:SRC --force-arabic --glossary $env:GLOS`（如有本地术语库可再加 `--glossary $env:WD\glossary_local.md` 跑一遍）。
   - verify 须 `ERROR=0` 才算过（中文在 GBK 控制台显乱码属正常，看 EXIT 码与 ERROR 数）。
   - **WARN 不必清零**：术语类 WARN 可能是术语库子串/惯例差异导致的合理保留，**把剩余 WARN 逐条抄进 `DONE_<书名>.flag` 交编排者裁决**，不要为消 WARN 硬改译文。
   - 若 ERROR：按报错块 `next --show` 复查，重写对应 `blocks/<块id>.zh.md` 再 `commit` + `assemble` + `verify`。

---

## §3 分体裁定质量标准（浓缩自 翻译总体方案 §2.3 + 首章审查意见）

- **人文书**（文学细读 / 艺术细品 / 音乐细听 / 哲学 / 心理自助叙事）：**保住文气与思辨纹理**是核心验收项。赏析口吻、隐喻与节奏、论证推进的语气、引文处理须还原；不压平成说明书体。术语首次出现可加注原文。
- **技术 / 科学书**（CS / ML / 数据 / 复杂性 / 工程 / AI）：以**准确 + 通顺 + 领域惯例**为主 bar，内容精度 > 文采。被动语态可保留，代码注释照译，公式/符号原样，术语不加注或按需加注。
- **数字规则（重要，曾踩坑）**：
  - 科普散文：约整数 / 顺口数词可用中文（十万、六十到一百）；但**精确测量值 / 单位 / 百分比 / 频率 / 统计 / 日期 / 编号 / 公式数 → 仍保留阿拉伯数字 + 原单位**。
  - 技术 / 统计 / 金融 / 会计 / 理科书：**所有数字强制阿拉伯数字 + 原单位**，中文数词约化零容忍。`--force-arabic` 校验源块阿拉伯数字集须在译块基本一致。
- **结构保全**：代码块 ```` ``` ````、LaTeX `$` / `$$`、表格 `|`、脚注、标题层级必须原样保留，只译散文。
- **禁忌译法**：见 `style_<系列>.md` 的「禁忌译法」小节（如 music 的 movement = 乐章 而非 运动；ML 的 training = 训练 而非 练习）。

---

## §4 防坑摘要（详看 PITFALLS.md）

- **坑 1**：`commit` 必须 `--file`，否则 stdin 常开管道永久阻塞超时（最严重）。
- **坑 2**：`status` / `assemble` / `next` 裸跑，**绝不要**套 `Select-String -NotMatch`（会吞掉正常输出假死）。只看 `2>$null` 压 oh-my-posh 噪声。
- **坑 3**：`.zh.md` 禁手改，只走 `commit`。
- **坑 4**：翻译前必 `lock-titles`。
- **坑 5**：`assemble` 须晚于 `commit`。
- **坑 6**：中文路径用绝对路径即可。
- **verify 章级 h3/h4 比对**：差异若是 legacy 切块把 `###` 切在边界造成的伪差会自动降级；若真丢失会报 ERROR。已修过 `chap_src → true_chap` 崩溃，现可稳定运行。

---

## §5 你不做什么（红线）

- 不碰 `books_registry.md`（台账）。
- 不手改 `成稿存档\<书名>.zh.md`。
- 不用「长度比」判异常（EN→ZH 字符比天然 0.2–0.35，会误报）。
- 不自行改 `translate_book.py` / `verify_translation.py`（共享只读资产）。

---

## §6 交付判据（完工动作）

满足全部：

1. `status` → `done == total`。
2. `verify_translation.py` → `ERROR=0`（WARN 允许保留，须逐条列出）。
3. 抽 1 章自审文气（人文书）或精度（技术书）过关。

→ 在 `$env:WD` 写 `DONE_<书名>.flag`（内容含：书名 / 总章 / done-total / verify 结果 `ERROR=x WARN=y` / **剩余 WARN 逐条清单** / 术语合规率 / 文气自评），并向编排者回报上述四项。

---

## §7 一键检查（不踩坑姿势）

```powershell
python $env:TB status $env:SRC 2>$null
python $env:TB next $env:SRC 2>$null
python $env:TB commit $env:SRC c02_b01 --file "$env:WD\c02_b01.md" 2>$null
python $env:TB assemble $env:SRC 2>$null
python $env:VT $env:SRC --force-arabic --glossary $env:GLOS 2>$null
```

---

_最后更新：2026-07-19。本文件为并行翻译的"失忆 agent 自助合同"，配合 PITFALLS.md 使用；任何新开窗口的翻译 agent 开工第一件事即读这两份。_
