### 7.9 绑定工作流 #3：生产 Pydantic + instructor + JSON schema + tenacity

交付物是一个真实生产模块。示例是 Beacon 的临床笔记摘要器，简化为重要的结构。

首先是导入和模块级日志器；重试原语前置列出使后面的装饰器块读起来干净：

    """beacon_clinical/summarizer.py - 生产级结构化摘要。"""

    import os
    import logging
    import time
    from typing import Literal, Annotated, Union
    from pydantic import BaseModel, Field, field_validator
    import instructor
    from anthropic import Anthropic, APIError
    from tenacity import (
        retry,
        stop_after_attempt,
        wait_exponential,
        retry_if_exception_type,
        before_sleep_log,
    )

    logger = logging.getLogger("beacon.summarizer")


接下来是 schema：嵌套的 `Medication`、带字段约束加拒绝编造标签验证器的 `SuccessSummary`、闭集 `ErrorSummary`，以及包装在信封中的判别联合使调用者在 `kind` 上分支而非捕获异常：

    # --- Schema ------------------------------------------------------------------

    class Medication(BaseModel):
        name: str = Field(min_length=1)
        dosage: str | None = None
        frequency: str | None = None

    class SuccessSummary(BaseModel):
        kind: Literal["success"]
        chief_complaint: str = Field(min_length=1)
        history_of_present_illness: str
        examination_findings: list[str] = Field(default_factory=list)
        medications: list[Medication] = Field(default_factory=list)
        plan: str
        confidence: float = Field(ge=0.0, le=1.0)
        unclear_elements: list[str] = Field(default_factory=list)

        @field_validator("chief_complaint")
        @classmethod
        def no_fabricated_placeholder(cls, v: str) -> str:
            forbidden = ["[fabricated]", "[hallucinated]", "(made up)"]
            for tag in forbidden:
                if tag.lower() in v.lower():
                    raise ValueError(f"chief_complaint contains forbidden tag: {tag}")
            return v

    class ErrorSummary(BaseModel):
        kind: Literal["error"]
        reason: Literal["unparseable", "incomplete", "policy_violation", "low_confidence"]
        detail: str = Field(min_length=1)

    Summary = Annotated[Union[SuccessSummary, ErrorSummary], Field(discriminator="kind")]

    class SummaryEnvelope(BaseModel):
        result: Summary
