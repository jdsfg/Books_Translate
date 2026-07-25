原则——永远不要在应用进程中执行 LLM 生成代码——是持久的。实现演化；原则不。到 2030 年，_不沙箱_ 将是教科书反模式，如同 2026 年的 _SQL 字符串插值_。

**Q3.** _复杂有状态操作的工具 schema 设计_。本章展示的工具模式（lookup_order、process_refund、read_file）大多无状态：每次调用独立。许多生产任务涉及有状态操作：启动多步工作流、检查进度、完成或中止。考虑操作：_供应新客户环境_（在多个下游系统中创建账户、生成凭证、配置权限、发送欢迎邮件；端到端约 30 秒；可能部分失败）。设计此有状态操作的工具 schema。解决：agent 如何发起操作；如何检查进度；如何处理部分失败；操作应暴露为一个工具还是多个；什么纪律防止 LLM 通过误用破坏状态。

**讨论：**

第一个设计问题：_一个工具还是多个？_ 诱惑是一个 `provision_customer(name, plan, ...)` 工具做一切。这错误有几个原因：

1. **长时间运行操作不适合工具调用超时**。工具调用有实际延迟预算（秒到低十秒级）；30 秒操作要么阻塞 agent 循环要么在完成前返回。
2. **部分失败难以在单个响应中表达**。如账户创建成功但邮件发送失败，工具返回什么？成功还是失败？两个答案都误导。
3. **LLM 无法对中间状态反应**。如 agent 能看到进度（账户已创建；权限待定），它可决定等待、升级或中止；单一全有或全无调用否认此。

正确设计：**为不同有状态动作分离工具**，带显式状态模型。

    - name: start_customer_provisioning
      description: |
        发起供应新客户环境。返回可用于检查状态或中止的 workflow_id。
        操作在应用侧异步运行。
      input_schema:
        customer_name: string
        plan: enum [starter, professional, enterprise]
        contact_email: string

    - name: check_provisioning_status
      description: |
        检查进行中供应工作流的状态。返回当前阶段、每阶段结果和总体状态。
      input_schema:
        workflow_id: string

    - name: abort_provisioning
      description: |
        取消进行中的供应工作流。已完成的阶段在可能时回滚；
        检查响应了解哪些回滚成功。
      input_schema:
        workflow_id: string
        reason: string


状态模型在应用侧持有：`provisioning_workflows` 表含 workflow_id、customer_name、plan、current_stage、stage_outcomes（JSON）、overall_status（pending / in_progress / succeeded / partially_succeeded / failed / aborted）、created_at、updated_at。

**部分失败如何处理**：
