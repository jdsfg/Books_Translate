### 6.4 Prompt 注册表：prompt 作为版本化制品

大多数团队的第一个 prompt 作为 Python 字符串存在于函数中。六个月后，他们在 30 个函数中有 30 个 prompt，没有一个被独立测试，没有一个可跨版本比较，而 _这个客户的调用使用的是哪个 prompt？_ 这个问题无法回答。

**prompt 注册表**模式解决了这个。Prompt 是一等制品：存储在各自文件中、独立版本化、独立评估、用自己的发布流程部署。

最小 prompt 注册表：


    prompts/
    ├── clinical_summary/
    │   ├── v1.md
    │   ├── v2.md
    │   ├── v3.md       # 当前生产
    │   └── README.md
    ├── code_review/
    │   ├── v1.md
    │   └── v2.md       # 当前生产
    └── manifest.yaml   # 哪个版本是当前的


每个 prompt 文件包含 prompt 文本加 front-matter：


    ---
    prompt_name: clinical_summary
    version: 3
    model: claude-sonnet-4-20260315
    temperature: 0
    max_tokens: 1024
    created_at: 2026-02-14
    created_by: aiyana@beacon
    eval_baseline_score: 9.4
    ---

    你是 Beacon Health AI 的临床笔记摘要器。
    给定口述笔记，产生结构化摘要，包含：
    - 主诉
    - 现病史
    - 检查发现
    - 计划

    约束：
    - 绝不编造药物、剂量或诊断
    - 使用系统文档中描述的 EHR schema
    - 用"[不确定]"显式标记不确定性而非猜测


清单固定每个环境中哪个版本是当前的：


    # manifest.yaml
    production:
      clinical_summary: v3
      code_review: v2
    staging:
      clinical_summary: v4-candidate
      code_review: v2


代码通过注册表加载 prompt：


    from prompts import registry

    prompt = registry.load("clinical_summary")  # 读取清单，返回当前版本
    response = client.messages.create(
        model=prompt.model,
        max_tokens=prompt.max_tokens,
        system=prompt.text,
        messages=[{"role": "user", "content": note}],
        temperature=prompt.temperature,
    )


这产生的纪律：

* **每个 prompt 有版本。** 变更是对 prompt 文件的提交；版本号升级；历史在 git 中。
* **每个 prompt 有 eval 基线。** 当 prompt 版本创建时，其在 golden set 上的 eval 分数记录在 front-matter 中。新版本获得对基线的 delta。
* **每个 prompt 有部署清单。** 生产/预发布环境使用特定版本。提升新版本是清单更新；回滚是恢复清单。
* **Prompt 可以被其他代码加载而无需耦合到内联字符串。** 重构 prompt 不再需要重构每个使用它的代码路径。
