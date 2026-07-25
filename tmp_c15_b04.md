### 14.4 有界性工程：核心美德

有界设计是 agent 最重要的工程纪律。_有界_ 意味着：agent 有结构约束防止失控行为，独立于 LLM 的推理质量。

四界模式：

**界 1：最大迭代**。轨迹不能超过 N 次迭代。通常 N=10 用于常规任务，N=20–30 用于复杂任务，N=50 仅需显式操作员批准。上限不可协商。

    def agent_loop(...) -> Result:
        for iteration in range(MAX_ITERATIONS):
            ...
        raise AgentBudgetExceeded("达到最大迭代次数")


**界 2：每调用 token 上限**。每次推理调用有 `max_tokens` 上限；长推理响应被裁剪。防止模型意外产生 50K token 输出。

**界 3：总轨迹预算**。累积 token 使用（跨所有迭代的输入 + 输出）被跟踪；当轨迹超过预算（比如 100K token），agent 停止并报告。

    trajectory_token_budget = 100_000
    tokens_used = 0
    for iteration in range(MAX_ITERATIONS):
        response = client.messages.create(...)
        tokens_used += response.usage.input_tokens + response.usage.output_tokens
        if tokens_used > trajectory_token_budget:
            raise AgentBudgetExceeded(f"轨迹超过 {trajectory_token_budget} token")
        ...


**界 4：每工具断路器**。如同一工具连续失败 N 次，或同一工具用相同参数调用 N 次，轨迹被停止。捕获 _工具错误上的重试循环_ 螺旋。

    tool_call_history = []  # (tool_name, args_hash)
    def execute_tool_with_circuit_breaker(name: str, args: dict) -> dict:
        args_hash = hash(json.dumps(args, sort_keys=True))
        tool_call_history.append((name, args_hash))
        if tool_call_history.count((name, args_hash)) >= 3:
            return {"status": "error", "error_kind": "circuit_breaker",
                    "message": "此确切工具调用已执行 3 次；循环似乎卡住。"}
        return execute_tool(name, args)


四界合在一起将无界循环转为有界。agent 要么在界内完成，要么以结构化失败干净停止。§14 开头的 52K 美元事件如有这些将限制到约 50 美元。有界工程的成本是真实的（几个工程师日）；_无界_ 的成本潜在无限。

### 14.5 Agent 记忆架构

记忆是跨迭代和（有时）跨会话持久化的东西。三层记忆重要。

#### 层 1：工作记忆（短期暂存区）

agent 在当前轨迹内的中间思考、工具调用和观察。存在于推理调用的消息历史中。轨迹结束时重置。

这是每个 agent 自动拥有的：轨迹的对话历史就是工作记忆。两个设计问题是如何结构化它（将用户目标与中间工具调用分离）和当它变长时如何摘要（第 8 章 §8.4）。
