# 自动化翻译审校工作流

这套流程把“用户在多个窗口之间复制报告”改成“所有结果汇总到 GitHub PR”。

## 自动执行的机械闸门

`.github/workflows/translation-quality-gate.yml` 会在翻译 PR 更新时：

1. 从 PR diff 识别受影响书目；
2. 读取该书 `checkpoint.json` 和正式 `blocks/*.md`；
3. 在临时目录运行 assemble；
4. 使用共享及本地 glossary 运行 verify；
5. 检查 checkpoint/source/output 哈希、完成进度和 DONE flag；
6. 检查 Q 编号、列表数量、占位符、相邻块重复、普通英文候选及禁止提交的临时文件；
7. 创建或更新 PR 中唯一一条 `Translation quality gate` 评论；
8. 有机械阻断项时让 GitHub check 失败。

自动评论只更新原评论，不会在每次 push 后重复刷屏。完整 Markdown/JSON 报告作为
workflow artifact 保存 30 天。

## 自动化不能替代语义审校

`ERROR=0` 无法发现漏译、反义误译、生硬直译或作者限定语被改变。最终完成的书仍需
独立 Agent 做源译对照。`.cursor/BUGBOT.md` 已提供仓库级审查规则，但 Bugbot 只能
作为辅助。

建议在 Cursor 网页端只创建一次 PR 更新 Automation：

```text
当 Books_Translate 仓库的 pull request 被创建或更新，且改动包含
pipeline/translate/<书名>/blocks/ 时，执行独立、只读翻译审校。

读取 HANDOFF_CONTROL_MODEL.md、CLOUD_AGENT.md、
pipeline/translate/review_config.json、对应 style、共享 glossary、本地 glossary、
checkpoint 和源书。先读取 GitHub Translation quality gate 评论，不信任作者的
DONE 自述，也不把 ERROR=0 当作语义通过。

若书未完成，只审查本次改动块及相邻块；若 done==total，另选至少一早一晚两个完整
章节做源译对照。检查漏译、重复、块错位、Q题干、列表、公式、数字、章节回指、
普通英文残留、术语和中文可读性。技术书至少抽查一章公式密集内容。

在同一 PR 发布或更新一条带标记
<!-- translation-semantic-review -->
的评论。结论只能是 PASS、BLOCK 或 IN PROGRESS。BLOCK 必须列出块ID并引用源文和
译文证据。全程不得修改文件、提交、推送、合并或改变 PR 状态。
```

不要开启“发现 BLOCK 后自动修改同一分支”，否则可能与仍在运行的翻译 Agent 并发
推送。修复应由该书原 Agent 读取 PR 评论后执行；原 Agent 停止后，才可使用
Fix in Web。

## 新增书目

新书初始化并锁定标题后，只需在 `review_config.json` 增加：

- 中文书名；
- `sources/<书名>.md`；
- style 文件；
- 共享/本地 glossary；
- 是否启用阿拉伯数字审计。

不需要为每本书复制 workflow。

## 现有长期分支

GitHub 的 `pull_request` workflow 来自 PR 的分支历史。此工作流合入 `main` 后，
已有 `translate/*` 长期分支需要各同步一次 `main`，后续建立的任务 PR 才会自动
运行机械闸门。新书分支应始终从最新 `main` 创建。

## 最终合并条件

只有以下项目全部满足才能从 `translate/<slug>` 合入 `main`：

- 机械闸门 PASS；
- 独立语义审校 PASS；
- `done == total`；
- verify `ERROR=0`；
- WARN 逐条解释；
- DONE flag 位于本书目录；
- PR 未包含生成的 `.zh.md`、临时文件、日志或共享资产误改。
