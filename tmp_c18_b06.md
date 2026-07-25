* **三个层级**（简单、标准、困难）各有多个提供商在 shuffle 分配中（在层内跨提供商负载均衡）。
* **跨层回退**（简单层失败 → 升级到标准层；标准层失败 → 升级到困难层）。团队选择 _失败时升级_ 而非 _同层换提供商_ 因为生产数据显示主层失败通常因能力限制，非提供商问题——升级到更强模型解决了更多案例。
* **按模型重试和冷却**：失败模型重试两次，然后冷却 60 秒以避免重试风暴。
* **可观测性和预算回调**：每次调用的成功/失败记录到 Langfuse 和 Datadog；调用前钩子检查租户预算；调用后钩子记录实际成本。

配置是真实生产级的。核心约 90 行；Helios 的完整配置约 600 行覆盖 12 种租户类型、7 个层级、4 个提供商和各种特殊路由规则。

应用代码变得简单：


    from litellm import Router

    router = Router(config_file="litellm_config.yaml")

    response = router.completion(
        model="helios-standard-tier",
        messages=[...],
        metadata={"tenant_id": "tenant_abc", "feature": "customer_support_agent"},
    )


应用代码命名 _层级_；路由器处理提供商选择、回退、可观测性、预算。应用不知道实际调用的是哪个提供商；它不需要知道。
