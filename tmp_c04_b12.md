Aiyana 的六行调用（§3.1）是她新角色的 _Hello, world_。她实际第一周的工作是用生产代码需要的东西封装它。以下是那些封装的样子。

    import os
    import time
    import logging
    from anthropic import Anthropic, APIError

    logger = logging.getLogger("beacon.codereview")
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    SYSTEM_PROMPT = """You are the Beacon Health AI CodeReview Bot.
    Review the diff that follows. Output a structured review with:
    - Severity (critical/major/minor)
    - File and line
    - Issue
    - Suggested fix
    Flag any potential PHI exposure with severity=critical.
    Do not invent files or lines not present in the diff.
    """

    def review_diff(diff_text: str, request_id: str, max_attempts: int = 3) -> dict:
        for attempt in range(max_attempts):
            try:
                t0 = time.monotonic()
                response = client.messages.create(
                    model="claude-sonnet-4-20260315",
                    max_tokens=1024,
                    system=SYSTEM_PROMPT,
                    messages=[{"role": "user", "content": diff_text}],
                    temperature=0,
                    metadata={"user_id": request_id},
                )
                duration_ms = int((time.monotonic() - t0) * 1000)

                logger.info(
                    "codereview ok",
                    extra={
                        "request_id": request_id,
                        "anthropic_request_id": response.id,
                        "model": response.model,
                        "input_tokens": response.usage.input_tokens,
                        "output_tokens": response.usage.output_tokens,
                        "duration_ms": duration_ms,
                        "stop_reason": response.stop_reason,
                    },
                )

                return {
                    "text": response.content[0].text,
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens,
                    "duration_ms": duration_ms,
                    "anthropic_request_id": response.id,
                }

            except APIError as e:
                if e.status_code == 429:
                    wait = float(e.response.headers.get("retry-after", 2 ** attempt))
                    logger.warning(
                        "codereview rate limited",
                        extra={"request_id": request_id, "wait_seconds": wait, "attempt": a
ttempt},                                                                                                       )
                    time.sleep(wait)
                    continue
                elif e.status_code >= 500:
                    wait = 2 ** attempt
                    logger.warning(
                        "codereview server error",
                        extra={"request_id": request_id, "status": e.status_code, "wait_sec
onds": wait, "attempt": attempt},                                                                              )
                    time.sleep(wait)
                    continue
                else:
                    logger.error(
                        "codereview client error",
                        extra={"request_id": request_id, "status": e.status_code, "error": 
str(e)},                                                                                                       )
                    raise

        raise RuntimeError(f"codereview exceeded {max_attempts} attempts for {request_id}")
