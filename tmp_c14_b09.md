### 13.7 Helios Customer AI：生产规模的工具目录

Helios 的客户支持 agent 在 2026 年有约 40 个工具，按类别组织：

**信息工具**（只读）：

* `search_knowledge_base(query)`
* `lookup_order(order_id)`
* `get_customer_history(customer_id, days)`
* `check_inventory(product_id)`
* `get_shipping_status(tracking_number)`

**计算工具**：

* `calculate_eligibility(customer_id, policy_id)`：对照客户数据运行业务逻辑
* `estimate_shipping_cost(...)`：包装确定性库

**操作工具**（状态变更，带策略门控）：

* `process_refund(order_id, amount, reason)`：门控金额 ≤ 租户限制；记录日志
* `create_support_ticket(customer_id, summary)`：始终允许
* `assign_to_human(ticket_id, queue)`：始终允许
* `update_customer_record(customer_id, field, value)`：门控字段允许列表
* `send_email(customer_id, template_id, args)`：门控模板 ID 允许列表

**升级工具**：

* `escalate_to_supervisor(ticket_id, reason)`：呼叫人工；agent 的退出坡道
* `flag_for_review(ticket_id, reason)`：标记但不立即升级

**诊断工具**：

* `run_account_diagnostic(customer_id)`：包装内部诊断
* `check_known_issues(symptom)`：搜索已知问题数据库

目录的组织是有意的。模型的 prompt 命名类别；这帮助模型在选择特定工具前选对类别。目录也版本化：`v3` 包含特定工具；`v4` 添加新工具并可能废弃旧的；生产 agent 固定到特定目录版本。

运维纪律：

* **工具定义在中央注册表中**（类似第 6 章的 prompt 注册表），版本化，eval 门控。
* **工具使用可观测**（第 19 章）：每次工具调用被追踪，含参数、输出、延迟和结果。
* **每工具成本跟踪**：一些工具昂贵（知识库搜索有小成本；全面客户历史查询可能更贵）。成本按租户按工具分配。

纪律将 Helios 从 5 工具原型 agent 扩展到服务每月 1000 万工单的 40 工具生产 agent。没有它，工具目录将变得不可维护。

#### 常见误解

_更多工具更好_的直觉听起来对但错了。有 40 个工具的模型比有 8 个的更难引导；工具选择错误上升；延迟随模型考虑更多选项而攀升。正确工具数是 _足够覆盖任务领域，不多_。无纪律增长工具目录的生产团队最终遇到质量悬崖——agent 开始错误路由——不得不重构。正确纪律：每个新工具的价值在加入生产前对照 eval 测量。
