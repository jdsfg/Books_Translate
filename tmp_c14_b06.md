### 13.5 绑定工作流 #6：沙箱代码执行

代码执行是典型的 _危险工具_：LLM 发出代码；应用运行它；代码可以做运行时允许的任何事。生产代码执行需要 **沙箱**：一个隔离运行时，LLM 的代码可在其中运行而无权访问你的生产系统。

2026 年主导沙箱选项：

**E2B**：提供 Python、Node 等的按调用沙箱运行时的 SaaS。每次 LLM 生成代码执行在全新容器中运行；容器在调用后销毁。卖点：即用型沙箱代码执行。

**Modal**：带沙箱能力的无服务器计算平台。比 E2B 更灵活；你定义沙箱镜像、库、资源限制。适合已在 Modal 上的团队。

**自托管**：Docker 容器、gVisor、Firecracker microVM、Kubernetes Jobs。最大控制；最大运维负担。适合需要特定隔离保证或有数据敏感性约束的团队。

绑定工作流使用 E2B 作为工作示例（模式泛化）：


    from e2b import Sandbox
    from anthropic import Anthropic

    ANTHROPIC = Anthropic()

    CODE_EXEC_TOOL = {
        "name": "execute_python",
        "description": "在沙箱环境中执行 Python 代码。沙箱可访问 numpy、pandas、"
        "matplotlib 和标准库。返回 stdout、stderr 和任何产物。"
        "沙箱在每次调用后销毁；状态不持久化。",
        "input_schema": {
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "要执行的 Python 代码"},
                "timeout_seconds": {"type": "integer", "minimum": 1, "maximum": 60,
                                    "default": 10},
            },
            "required": ["code"],
        },
    }

    def execute_python_in_sandbox(code: str, timeout_seconds: int = 10) -> dict:
        """在隔离沙箱中执行 LLM 生成的代码。"""
        with Sandbox(template="python-3.12") as sandbox:
            result = sandbox.run_code(code, timeout=timeout_seconds)
            return {
                "stdout": result.stdout[-4000:],  # 截断到安全大小用于 LLM 上下文
                "stderr": result.stderr[-2000:],
                "exit_code": result.exit_code,
                "artifacts": [a.name for a in result.artifacts],
            }


沙箱保证：

* **隔离**：代码在容器中运行；无法访问主机文件系统、网络（可配置）或其他沙箱。
* **资源限制**：CPU、内存、超时。失控循环被杀死。
* **临时状态**：每次调用全新；无持久状态意味无跨调用攻击面。
* **有界输出**：结果在返回 LLM 上下文前截断（保留上下文预算）。
