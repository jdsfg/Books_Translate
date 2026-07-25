2. **`confidence_aligned_with_unclear`**：强制低整体置信度需要至少一个不确定性标志（`medications_unclear` 等）。没有这个验证器，模型可以产生 _低置信度_ 摘要而不标记任何特定不确定性，这是不连贯的（如果你不确定，你具体不确定什么？）。验证器强制模型表达不确定性位置，这对临床医生审查更有用。

第三个判别变体（`HumanReviewSummary`）介于完全成功和不可解析之间：模型可以提取一些信息但标记需人工审查。这种三路分支比成功/失败更细致，是真实临床工作流通常想要的。

**AI 协作子问题**：你会如何请 LLM 帮助完成这个练习，你会在它的回答中验证什么？

**答案：** 有用的 prompt：_设计一个 Pydantic 判别联合 schema 用于临床摘要，三个变体：成功、需人工审查、不可解析。包含强制非显而易见约束的字段级验证器。_ 你验证 (a) 验证器在边缘案例上正确运行（为每个验证器写带有效和无效输入的测试），以及 (b) 判别器覆盖模型将遇到的所有真实案例（通过你的 eval 运行 schema；检查模型产生不适合任何变体的输出的案例）。

**Q2.** _实现带验证反馈的重试_。以下是一个朴素实现；重写以使用 `instructor` 的内置重试，三次重试尝试和验证失败的结构化日志。

    def extract(text: str) -> CodeReview:
        response = anthropic.messages.create(
            model="claude-sonnet-4-20260315",
            messages=[{"role": "user", "content": text}],
            max_tokens=1024,
        )
        return CodeReview.model_validate_json(response.content[0].text)


**答案：**


    import logging
    import instructor
    from anthropic import Anthropic
    from pydantic import ValidationError

    logger = logging.getLogger("review.extract")
    client = instructor.from_anthropic(Anthropic())

    def extract(text: str, request_id: str) -> CodeReview:
        try:
            review = client.messages.create(
                model="claude-sonnet-4-20260315",
                max_tokens=1024,
                response_model=CodeReview,
                messages=[{"role": "user", "content": text}],
                max_retries=3,  # instructor 在 ValidationError 上重试并反馈错误
            )
            return review
        except ValidationError as e:
            logger.error(
                "extract.validation_failed_after_retries",
                extra={
                    "request_id": request_id,
                    "errors": e.errors(),
                },
            )
            raise


与朴素版本的区别：
