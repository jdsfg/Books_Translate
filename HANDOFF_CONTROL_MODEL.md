# 云端翻译项目交接：中转控制模型

## 1. 角色与目标

你是本项目的**中转控制模型**，负责统筹、派工、质量闸门和 Git 分支验收；不要把本项目当作普通编码任务。

目标是把仓库内英文 Markdown 书稿译为高质量中文。优先级固定为：**忠实完整 > 术语与数字准确 > Markdown/公式结构完整 > 中文可读性 > 速度**。

翻译 Agent 只负责其分支的一本书。控制模型只在需要时发出纠偏指令、审查结果、合并通过的 PR；不得让多 Agent 共用同一书目或同一分支。

## 2. 仓库与真源

- GitHub：`jdsfg/Books_Translate`，私有协作仓库。
- `sources/<书名>.md`：英文源书。
- `pipeline/translate/<书名>/checkpoint.json`：块进度真源。
- `pipeline/translate/<书名>/blocks/<块id>.md`：正式中文译块真源。
- `sources/<书名>.zh.md`：由 `assemble` 生成，属于派生输出，不提交。
- `pipeline/translate_book.py`：唯一允许用于状态、取块、提交和拼装的脚本。
- `pipeline/translate/verify_translation.py`：结构、数字和术语核验脚本。
- `CLOUD_AGENT.md`、`STATUS.md`：云端执行合同与当前迁移状态。

当前已初始化的 `sources/` 根目录包含以下六本完整英文书稿：信息论：从香农到 AI、复杂性科学入门、AI时代的统计思维、明智决策：不确定世界中的理性思考、进化心理学、身体这台机器：随身硬件巡礼。章节结构与结尾显示它们是完整书稿，不是节选。另有 48 份英语占主导的待入库书稿已上传至 `sources/pending/`；清单见 `SOURCE_INTAKE.md`。它们尚未预检、初始化、锁标题或分配分支，任何 Agent 不得直接翻译。

不要提交 `_tmp_*`、日志、缓存、调试脚本、根目录译文副本、临时 `.zh.md` 文件或无关项目文件。

## 3. 当前迁移状态

| 书目 | 分支 | 块进度 | 状态 |
|---|---|---:|---|
| 信息论：从香农到 AI | `translate/info-theory` | 134 / 282 | 先返修，禁止继续堆量 |
| 复杂性科学入门 | `translate/complexity-science` | 350 / 350 | 块已完成，待最终验收 |
| AI时代的统计思维 | `translate/ai-statistics` | 180 / 380 | 可续翻 |
| 明智决策：不确定世界中的理性思考 | `translate/decision-making` | 30 / 285 | 可续翻 |
| 进化心理学 | `translate/evolutionary-psychology` | 29 / 184 | 可续翻 |
| 身体这台机器：随身硬件巡礼 | `translate/body-machine` | 8 / 151 | 可续翻 |

所有六本书**已经初始化且标题已锁定**。任何 Agent 均禁止执行 `init`、`lock-titles` 或重新切块。

### 信息论风险

信息论源稿本身存在公式三重渲染等提取问题；译文不得把 LaTex、Unicode 渲染式和纯文本公式三份叠加。现有译文已出现公式重复/粘连、`0.90.90.9` 等数字变形、`XXX/YYY` 残留、标题层级遗漏、表格缺失。最近一次全书核验至少出现 `ERROR=18`、`WARN=83`。此分支的首个任务是逐块修复既有问题；`verify` 达到 `ERROR=0` 前，不得继续翻新块。

### 复杂性科学

`350/350` 仅表示全部块已提交，不表示出版质量。英文源稿已确认存在重复段落；最终审校必须定位、记录并处理这些重复，而不能把重复源文直接当作合格中文内容。该分支必须完成全量核验、随机抽样源译对照、术语审查和 `DONE_*.flag` 后才能合并。

## 4. 云端 Agent 执行合同

每个 VM/容器/本地 Agent 都必须：

1. 克隆仓库并切换**唯一指定分支**。
2. 先读取 `CLOUD_AGENT.md`、`STATUS.md`、相关 `style_*.md`、`glossary_*.md` 和 `PITFALLS.md`。
3. 使用仓库相对路径；不要依赖 Windows 盘符或本地旧目录。
4. 运行 `status`，再运行 `next --ctx` 取得下一块。
5. 完整精翻一块，保留所有标题、列表、表格、代码块、公式、数字、单位、变量与脚注。
6. 只用 `commit --file` 提交块；每 3–5 块运行 `assemble`、`status`、`verify` 并提交 Git。
7. 推送自己的分支；绝不直接推送 `main`。
8. 有命令错误、标题/公式不确定、校验 `ERROR`、源文疑似损坏时停止并报告；禁止自造脚本或修改共享工具。

不要把 stderr 重定向到空设备。`status` 或 `verify` 没有输出不代表成功；应保留完整终端输出并检查退出码。

## 5. 标准命令骨架

在仓库根目录执行。将 `<书名>`、`<块id>`、`<风格术语库>` 替换为当前分支的实际值。

```powershell
python pipeline/translate_book.py status "sources\<书名>.md"
python pipeline/translate_book.py next "sources\<书名>.md" --ctx
python pipeline/translate_book.py commit "sources\<书名>.md" <块id> --file "<临时译文文件>.md"
python pipeline/translate_book.py assemble "sources\<书名>.md"
python pipeline/translate/verify_translation.py "sources\<书名>.md" --glossary "pipeline\translate\<风格术语库>.md"
```

技术书额外使用 `--force-arabic` 审计精确数字。科普/心理/社科书允许自然约数转中文，但精确数值、年份、百分比、公式、单位、统计与型号不得改写。

## 6. Git 与 PR 闸门

- 一书一分支；不同书互不共享工作目录。
- 每 3–5 块，或每次上下文即将结束前：`git add` 本书目录、`git commit`、`git push`。
- 提交信息必须含书目 slug 和块范围，例如 `translate(ai-statistics): c04_b01-c04_b05`。
- `main` 是迁移基线；不接受云端 Agent 直推。
- 只有符合下列所有条件的 PR 才能合并：
  - `done == total`
  - `verify` 的 `ERROR=0`
  - 剩余 `WARN` 已逐条解释
  - 随机抽检至少一章，覆盖公式/数字/标题或专业术语
  - 已写入 `DONE_<书名>.flag`

### 自动化审校

- `.github/workflows/translation-quality-gate.yml` 在翻译 PR 更新时运行机械闸门，并将结果直接更新到 PR 评论。
- `pipeline/translate/review_config.json` 是书目、风格、术语库与数字审计策略的统一配置；新增书目只需登记一次。
- `.cursor/BUGBOT.md` 提供 PR 翻译审查规则；完整设置见 `pipeline/translate/AUTOMATED_REVIEW.md`。
- 机械 `PASS` 不等于出版质量。最终合并仍必须有独立 Agent 的源译语义审校 `PASS`。
- 控制模型直接读取和发布 PR 审校评论，不再要求用户在多个窗口之间复制报告。

## 7. 平台与模型调度

CPU 不是本项目瓶颈。翻译、Markdown 处理和 Python 校验均为轻量工作；云端 VM 的价值是**会话隔离、稳定性、持久磁盘和 Git 分支协作**，不是算力。

- 高质量/高风险任务：使用 Cursor 中额度充足的高阶模型，尤其是信息论返修、统计与公式、最终质量审稿、术语决策、PR 验收。
- 常规连续翻译：可以使用 Devin 云端会话或容器，以单书单分支隔离执行；免费 SW 1.7 只能在通过样张试译后使用。
- 低风险任务：状态汇报、Git 操作、文件整理、重复性格式核验可用免费模型。
- 任何新模型先做盲测：同一源块让候选模型各译 2–3 块，由高阶模型或人工检查完整度、公式、术语和中文质量；不通过不得大规模铺量。

## 8. 后续批次规划

1. 第一批：修复/完成当前六本书，建立稳定的 PR 与质量闸门。
2. 第二批：按学科簇扩容，而不是随机开书：技术簇、社科心理簇、生命科学科普簇分别共享术语与风格。
3. 每批最多 4–6 本；先完成上批验收再导入新书。
4. 新书入库流程：将一份新的完整英文 Markdown 放入 `sources/` → **源稿预检与清洗** → `init` 与锁标题仅执行一次 → 建专属分支 → 通过 2–3 块样张试译 → 才允许批量翻译。
5. 源稿预检至少检查：章节标题连续性、结尾完整性、重复段落、公式/表格多重渲染、乱码/占位符、代码块闭合与脚注链接；问题必须在初始化前修复或明确登记。
6. 已初始化书目的源文不得被 Agent 静默改写。若必须修复源稿，先单独记录变更和受影响块，再由控制模型决定是否迁移检查点或重新初始化。
7. 不把 `PASS`、已生成 EPUB 或登记台账当作本仓库的翻译验收替代；本仓库一律以块进度、核验和抽检为准。

## 9. 给下一位控制模型的第一步

1. `git fetch --all --prune`，读取 `STATUS.md`。
2. 检查每个翻译分支最近提交、当前 `status` 和 `verify` 输出。
3. 优先派信息论返修；其次派复杂性科学最终审校；其余四本按分支续翻。
4. 每次派工明确：书名、分支、当前块进度、风格文件、术语库、验收条件。
5. 不确定时宁可暂停并报告，不要为了提升完成数接受结构损坏或偷译。
