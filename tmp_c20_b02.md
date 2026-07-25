### 19.2 LLM 系统追踪是什么样的

一个完整的 LLM 系统追踪包括：

**每个 LLM 调用**：

* 时间戳
* 模型版本
* Prompt（系统 + 消息）
* 输出（文本内容 + 工具使用块）
* Token 计数（输入、输出、缓存创建、缓存读取）
* 成本（从 token × 模型费率计算）
* 延迟分解（首 token 时间；总挂钟时间）
* 停止原因

**每个工具调用**（适用时）：

* 工具名称
* 参数
* 结果（为大小脱敏；为隐私标记）
* 持续时间
* 成本（如工具本身有成本）

**每个轨迹**（多调用）：

* 所有 LLM 调用和工具调用按序，带时序
* 总轨迹成本
* 总轨迹延迟
* 最终结果（成功 / 升级 / 失败 / 放弃）
* 元数据（user_id、session_id、feature_name、tenant_id、...）

**每个会话**（多轨迹会话）：

* 会话中的所有轨迹
* 跨轨迹状态（做出的决策；用户上下文）

追踪是结构化的：带嵌套 span 的类 JSON 文档（LLM 调用 → 工具调用 → LLM 续写 → ...）。结构镜像 agent 的实际执行。


    {
      "trace_id": "trace_abc",
      "trajectory_id": "traj_xyz",
      "session_id": "sess_123",
      "user_id": "user_456",
      "tenant_id": "tenant_789",
      "feature": "customer_support_agent",
      "started_at": "2026-05-20T14:30:00Z",
      "ended_at": "2026-05-20T14:30:04.2Z",
      "outcome": "success",
      "total_cost_cents": 18,
      "spans": [
        {
          "type": "llm_call",
          "model": "claude-haiku-4-20250630",
          "duration_ms": 800,
          "input_tokens": 1500,
          "output_tokens": 280,
          "cost_cents": 1,
          "system_prompt_redacted": "[1500 tokens]",
          "messages": [...],
          "response": {...}
        },
        {
          "type": "tool_call",
          "name": "lookup_order",
          "args": {"order_id": "ORD-1234567890"},
          "duration_ms": 80,
          "result": {...}
        },
        {
          "type": "llm_call",
          "model": "claude-haiku-4-20250630",
          "duration_ms": 700,
          "input_tokens": 1820,
          "output_tokens": 200,
          "cost_cents": 1,
          ...
        },
        ...
      ]
    }


追踪是调试产物。当生产中出问题时，团队打开追踪；他们看到 agent 做了什么、调用了什么工具、模型说了什么、成本是多少。调查是结构化的而非考古式的。
