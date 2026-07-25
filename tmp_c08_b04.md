### 7.4 判别联合：处理结构化分支

许多真实输出是联合：_模型应返回 `success` 响应或 `error` 响应，每种情况有不同字段_。朴素的联合处理产生歧义——验证器不知道用哪个变体。**判别联合**通过添加显式标识变体的 _判别字段_ 来解决这个。

    from pydantic import BaseModel, Field
    from typing import Literal, Annotated, Union

    class SuccessResponse(BaseModel):
        kind: Literal["success"]
        summary: str
        confidence: float = Field(ge=0.0, le=1.0)

    class ErrorResponse(BaseModel):
        kind: Literal["error"]
        reason: Literal["unparseable_input", "low_confidence", "policy_violation"]
        detail: str

    Response = Annotated[Union[SuccessResponse, ErrorResponse], Field(discriminator="kind")
]
    class WrappedResponse(BaseModel):
        result: Response


现在当模型产生输出时，`kind` 字段告诉验证器用哪个变体。下游代码做：

    result = call_llm(...).result
    if result.kind == "success":
        use_summary(result.summary, result.confidence)
    elif result.kind == "error":
        handle_error(result.reason, result.detail)


模式对任何非平凡输出至关重要。没有判别，模型的结构化输出在字段跨变体共享时变歧义；有判别，下游代码是类型安全的且验证器确定性地工作。

判别联合也是 _优雅失败模式_ 的基础：与其要求模型 _总是_ 产生成功答案，你给它一个结构化的 _错误_ 变体它可以在任务不可能时产生。模型有一个定义的退出坡道而非幻觉。Beacon 临床笔记摘要器使用这个模式：当口述不可解析时，模型产生 `{kind: "error", reason: "unparseable_input", detail: "..."}` 而非猜测。
