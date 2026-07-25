* _仅 prompt 变更_：拼写修复、指令调优。升级 prompt 版本，保持 schema 版本。常见。
* _仅 schema 变更_：收紧字段约束而不改指令。罕见但可能。升级 schema 版本，保持 prompt。
* _prompt 和 schema 变更_：添加新判别联合变体及相应指令。两者都升级。最常见的实质性变更。

清单条目固定 _目录_（即联合版本），非分离版本号；联合固定避免漂移情况。

**Eval 设计。** 每个版本的 `eval_baseline.json` 记录多轴量表（按第 4 章）分数加特定于 schema 的结构指标：

    {
      "version": "v3",
      "eval_set": "clinical_v3",
      "axes": {
        "accuracy": 0.91,
        "completeness": 0.86,
        "citation_grounding": 0.93,
        "tone": 0.88
      },
      "structural": {
        "schema_validation_pass_rate": 0.998,
        "human_review_variant_rate": 0.12,
        "unparseable_variant_rate": 0.03,
        "catch_all_field_usage_rate": 0.04
      }
    }


结构指标捕获 schema 太刚性和太宽松故障（按上面 Q6）。推广门要求两者：轴分数不比基线在噪声内差，结构指标在健康范围内。

**为什么此集成重要。** Prompt 和 schema 在生产中紧密耦合：改一个不测另一个产生静默回归。共版本化强制联合测试；注册表的部署纪律适用于两者。通过此循环运行 prompt 更新的团队自信地发布变更；不通过 schema 检查更新 prompt（或反之）的团队累积产生大意外的小漂移。

**AI 协作子问题**：你会如何请 LLM 帮助完成这个练习，你会在它的回答中验证什么？

**答案：** 有用的 prompt：_设计一个共版本化 prompt 和 Pydantic schema 的 prompt 注册表。文件布局、加载器代码、版本化规则和 eval 格式。交叉引用第 6 章的注册表模式。_ 你验证 (a) LLM 提议 _联合_ 版本化（每个联合版本一个目录）而非两个独立版本号（独立版本化产生漂移；LLM 偶尔提议它好像更简单），以及 (b) eval 格式包含 _结构指标_（schema 验证通过率、变体分布）而非仅标准轴分数；没有这些，schema 级回归不被检测。
