### 7.3 `instructor`：Pydantic 类型的结构化输出

`instructor` 是一个 Python 库，包装主要 provider API 并让你将输出 schema 指定为 Pydantic 模型。库将 Pydantic schema 转换为 provider 的 JSON schema 格式，发起调用，验证响应，并返回类型化 Python 对象。

    from typing import Literal
    from pydantic import BaseModel, Field
    import instructor
    from anthropic import Anthropic

    class CodeReviewItem(BaseModel):
        severity: Literal["critical", "major", "minor"]
        file: str
        line: int = Field(ge=1, description="行号，1 索引")
        issue: str
        suggested_fix: str

    class CodeReview(BaseModel):
        overall_assessment: str
        items: list[CodeReviewItem]

    client = instructor.from_anthropic(Anthropic())

    review = client.messages.create(
        model="claude-sonnet-4-20260315",
        max_tokens=1024,
        response_model=CodeReview,
        messages=[{"role": "user", "content": diff_text}],
    )

    # review 是类型化 CodeReview 对象；review.items 是 list[CodeReviewItem]


`instructor` 相比原生 JSON schema 模式给你的：

1. **Pydantic v2 验证**。超越 schema 一致性，Pydantic 验证类型、约束（`ge=1`、`min_length=1`）和自定义验证器。声明为 `Literal["critical", "major", "minor"]` 的字段被验证为这三个字符串之一；`line: int = Field(ge=1)` 被验证为至少 1。
2. **类型化 Python 对象**。返回值是类型化对象，非字典。你的 IDE 知道字段；重构安全；字典键访问中的拼写错误 bug 消失。
3. **自动 schema 生成**。你写 Pydantic 模型；库生成 JSON schema。Schema 和代码保持同步。
4. **Provider 抽象**。相同 Pydantic 模型以一行变更对 Anthropic、OpenAI、Google 工作。在你可能切换 provider 或在生产中运行多 provider 时有用。
5. **验证失败时内置重试**。如果模型产生符合 schema 但未通过 Pydantic 验证的 JSON（例如 `line` 是 0 而非 ≥1），库以验证错误作为消息反馈重试。可配置重试次数。

库足够小可审计；生产力增益足够大值得推荐。2026 年，大多数寻求 Pydantic 类型结构化输出的 Python 团队选择 `instructor`。
