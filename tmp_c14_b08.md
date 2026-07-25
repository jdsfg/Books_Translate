#### 数据库查询工具

查询结构化业务数据的工具。`get_customer(customer_id)`；`list_orders(customer_id, status=None)`；`get_inventory(product_id)`。这些是 _参数化的_；LLM 的参数验证决定数据库看到什么。

安全：永远不要允许 LLM 构造任意 SQL。工具应暴露特定的、参数化查询。如需要灵活查询工具（罕见），用约束操作的 SQL 构建器实现（只读；特定表；无禁止表连接）。

#### 操作工具

改变状态的工具。`create_ticket`、`assign_to_human`、`process_refund`、`send_notification`。这些需要 §13.4 原则 3 的确定性策略门控。

Helios 的模式：操作工具有 `dry_run: bool = false` 参数。确定性策略层首先以 dry-run 模式运行工具（返回会发生什么）；对照策略检查结果；如通过则真实运行；如失败则返回错误给 agent。

#### 计算工具

执行计算、统计、数据转换的工具。代码执行沙箱（§13.5）是最通用的；特定计算工具（`calculate_loan_payment`、`compute_summary_statistics`）将常见操作包装在安全、确定性实现中。

#### 时间和外部工具

依赖真实世界的工具：`current_time()`、`get_weather(location)`、`query_external_api(endpoint, params)`。这些有故障模式（网络、速率限制、API 变更）；其错误必须结构化以供模型处理。
