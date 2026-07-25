**AI 协作子问题**：你会如何请 LLM 帮助完成这个练习，你会在它的回答中验证什么？

**答案：** 有用的 prompt：_我们的 agent 在应调用 lookup_order 处理订单特定问题时调用了 search_knowledge_base。诊断并提出三个修复。_ 你验证 (a) 提议的修复针对实际诊断（工具描述、prompt、分类）而非通用"让模型更聪明"建议，以及 (b) 提议的修复顺序匹配工程成本 vs 影响（最便宜先）。

**Q5.** _设计带确认的退款工具_。你的客户支持 agent 需要发退款。按 §13.4，LLM 提议应用处置；按 §13.9 原则 3，高风险操作需要显式确认。设计 `issue_refund` 的工具架构。指定：(a) 工具 schema；(b) 确认流程（什么触发它、谁确认）；(c) 应用层策略门控；(d) LLM 在每条路径（提议、确认、拒绝）中看到的结构化响应格式；(e) 审计轨迹。

提示

确认是单独工具调用，非参数。为什么？

**答案：**

(a) **工具 schema**：


    name: issue_refund
    description: |
      为特定订单发出退款。此操作需要先通过 confirm_refund_intent 工具
      捕获的显式客户确认。除非 confirm_refund_intent 已在同一轨迹中
      调用并返回成功，否则不要调用此工具。
    input_schema:
      order_id: string（必须匹配当前客户的现有订单）
      amount_cents: integer（不得超过订单总额；必须 > 0）
      reason: string（10-500 字符；必填）
      confirmation_token: string（由 confirm_refund_intent 返回；必填）


单独的 `confirm_refund_intent` 工具有自己的 schema：


    name: confirm_refund_intent
    description: |
      请求客户对退款的显式确认。在调用 issue_refund 之前使用此工具。
      工具在聊天 UI 中向客户展示退款详情；客户的响应（是/否）
      被捕获，如确认则返回 confirmation_token。
    input_schema:
      order_id: string
      amount_cents: integer
      reason: string


(b) **确认流程**：

1. Agent 决定退款合理；用提议详情调用 `confirm_refund_intent`。
2. 应用向客户渲染确认 UI："我们即将为订单 #12345 发出 50.00 美元退款，因为商品损坏。确认或取消？"
3. 客户点击"确认"或"取消"。应用捕获响应。
4. 如确认：应用生成短期 `confirmation_token`（UUID，约 5 分钟 TTL）绑定到 (order_id, amount_cents, reason) 元组。token 在工具响应中返回给 LLM。
5. agent 然后用匹配参数加 `confirmation_token` 调用 `issue_refund`。应用层策略验证 token，执行退款，返回确认。

分离重要：LLM 无法伪造 `confirmation_token` 因为 token 是服务端生成并绑定到特定参数；50 美元退款的 `confirmation_token` 不能重用于 500 美元退款。

(c) **应用层策略门控**（按 §13.9）：
