**答案：**


    import logging
    import time
    from dataclasses import dataclass
    from e2b import Sandbox, SandboxException
    from tenacity import retry, stop_after_attempt, retry_if_exception_type, wait_exponential

    logger = logging.getLogger("agent.code_exec")

    @dataclass
    class CodeExecResult:
        status: str  # "success" | "code_error" | "timeout" | "infrastructure_error"
        stdout: str
        stderr: str
        exit_code: int | None
        duration_ms: int
        cost_cents: float

    class InfrastructureError(Exception):
        pass

    @retry(
        retry=retry_if_exception_type(InfrastructureError),
        stop=stop_after_attempt(2),
        wait=wait_exponential(multiplier=1, min=1, max=4),
        reraise=False,
    )
    def _execute_with_retry(code: str, timeout_seconds: int) -> dict:
        try:
            t0 = time.monotonic()
            with Sandbox(template="python-3.12") as sandbox:
                result = sandbox.run_code(code, timeout=timeout_seconds)
            duration_ms = int((time.monotonic() - t0) * 1000)
            return {
                "stdout": result.stdout[-4000:],
                "stderr": result.stderr[-2000:],
                "exit_code": result.exit_code,
                "duration_ms": duration_ms,
            }
        except SandboxException as e:
            if "infrastructure" in str(e).lower() or "transient" in str(e).lower():
                raise InfrastructureError(str(e))
            raise

    def execute_python_safe(code: str, timeout_seconds: int = 10,
                            request_id: str = "") -> CodeExecResult:
        """执行 LLM 生成的 Python 代码；返回结构化结果用于 LLM 上下文。"""
        if not 1 <= timeout_seconds <= 60:
            return CodeExecResult(
                status="code_error",
                stdout="",
                stderr=f"timeout_seconds 必须在 1-60 之间，得到 {timeout_seconds}",
                exit_code=None,
                duration_ms=0,
                cost_cents=0,
            )

        try:
            result = _execute_with_retry(code, timeout_seconds)
            cost_cents = 0.5 + result["duration_ms"] * 0.0001  # E2B 每沙箱分钟定价近似
            outcome = CodeExecResult(
                status="success" if result["exit_code"] == 0 else "code_error",
                stdout=result["stdout"],
                stderr=result["stderr"],
                exit_code=result["exit_code"],
                duration_ms=result["duration_ms"],
                cost_cents=cost_cents,
            )
        except InfrastructureError as e:
            outcome = CodeExecResult(
                status="infrastructure_error",
                stdout="",
                stderr="沙箱基础设施故障；请尝试不同方法。",
                exit_code=None,
                duration_ms=0,
                cost_cents=0,
            )
        except Exception as e:
            if "timeout" in str(e).lower():
                outcome = CodeExecResult(
                    status="timeout",
                    stdout="",
                    stderr=f"代码执行超过 {timeout_seconds}s 超时。",
                    exit_code=None,
                    duration_ms=timeout_seconds * 1000,
                    cost_cents=0.5,
                )
            else:
                logger.exception("意外错误", extra={"request_id": request_id})
                outcome = CodeExecResult(
                    status="infrastructure_error",
                    stdout="",
                    stderr="代码执行内部错误。",
                    exit_code=None,
                    duration_ms=0,
                    cost_cents=0,
                )

        logger.info(
            "code_exec.complete",
            extra={
                "request_id": request_id,
                "status": outcome.status,
                "duration_ms": outcome.duration_ms,
                "cost_cents": outcome.cost_cents,
                "code_chars": len(code),
            },
        )
        cost_counter.increment(request_id, outcome.cost_cents)
        return outcome
