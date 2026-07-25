### 7.8 带验证的重试

原生模式非常可靠但非万无一失。即使 99.5% 的 schema 一致性，每天 10 万次调用你会看到 500 次失败。正确模式是 **带验证错误反馈进 prompt 的重试**。

    from tenacity import retry, stop_after_attempt, retry_if_exception_type
    from pydantic import ValidationError

    @retry(
        stop=stop_after_attempt(3),
        retry=retry_if_exception_type(ValidationError),
        reraise=True,
    )
    def extract_review(diff_text: str) -> CodeReview:
        return client.messages.create(
            model="claude-sonnet-4-20260315",
            max_tokens=1024,
            response_model=CodeReview,
            messages=[{"role": "user", "content": diff_text}],
        )


`instructor` 的内置重试比直接用 `tenacity` 更干净：它捕获验证错误，将其作为助手消息 + 用户消息追加（"你之前的响应验证失败，错误如下：...请重试"），并重新调用。模型通常在重试时自我纠正。

两个要注意的：

1. **限制重试次数**。三次尝试是工作默认值。更多尝试增加成本而无比例成功。
2. **将重试记录为指标**。如果重试率超过 1%，prompt 或 schema 需要改进。如果超过 5%，你有结构性问题（schema 不匹配、指令歧义、模型不胜任该任务）。
