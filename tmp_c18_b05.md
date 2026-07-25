### 17.7 绑定工作流 #8：LiteLLM 路由器配置

绑定交付物是生产系统的真实 LiteLLM 配置。示例是 Helios 的简化版，说明成本感知回退链、每租户预算钩子和提供商故障检测。

    # litellm_config.yaml
    model_list:
      - model_name: helios-easy-tier
        litellm_params:
          model: openai/gpt-4o-mini
          api_key: os.environ/OPENAI_API_KEY
          max_tokens: 1024
          timeout: 15
        model_info:
          tier: easy
          cost_per_input_1m: 0.15
          cost_per_output_1m: 0.60

      - model_name: helios-easy-tier
        litellm_params:
          model: gemini/gemini-2.5-flash
          api_key: os.environ/GOOGLE_API_KEY
          max_tokens: 1024
          timeout: 20
        model_info:
          tier: easy
          cost_per_input_1m: 0.10
          cost_per_output_1m: 0.40

      - model_name: helios-standard-tier
        litellm_params:
          model: anthropic/claude-haiku-4-20250630
          api_key: os.environ/ANTHROPIC_API_KEY
          max_tokens: 2048
          timeout: 25
        model_info:
          tier: standard
          cost_per_input_1m: 0.80
          cost_per_output_1m: 4.00

      - model_name: helios-standard-tier
        litellm_params:
          model: openai/gpt-4o
          api_key: os.environ/OPENAI_API_KEY
          max_tokens: 2048
          timeout: 25
        model_info:
          tier: standard
          cost_per_input_1m: 2.50
          cost_per_output_1m: 10.00

      - model_name: helios-hard-tier
        litellm_params:
          model: anthropic/claude-sonnet-4-20260315
          api_key: os.environ/ANTHROPIC_API_KEY
          max_tokens: 4096
          timeout: 30
        model_info:
          tier: hard
          cost_per_input_1m: 3.00
          cost_per_output_1m: 15.00

      - model_name: helios-hard-tier
        litellm_params:
          model: openai/gpt-4o
          api_key: os.environ/OPENAI_API_KEY
          max_tokens: 4096
          timeout: 30
        model_info:
          tier: hard
          cost_per_input_1m: 2.50
          cost_per_output_1m: 10.00

    router_settings:
      routing_strategy: simple-shuffle  # 在一层内，跨提供商分配
      fallback_models:
        helios-easy-tier:
          - helios-standard-tier  # 如简单层失败，升级而非降级
        helios-standard-tier:
          - helios-hard-tier
        helios-hard-tier: []  # 无进一步回退；困难层是天花板
      num_retries: 2
      retry_after: 5
      cooldown_time: 60  # 如模型反复失败，冷却 60 秒
      timeout: 35

    callbacks:
      - litellm.success_callback: ["langfuse"]
      - litellm.failure_callback: ["langfuse", "datadog"]
      - litellm.budget_callback: ["helios_tenant_budget_check"]

    general_settings:
      master_key: os.environ/LITELLM_MASTER_KEY
      database_url: os.environ/LITELLM_DB_URL  # 用于预算追踪、密钥管理
      alerting:
        - slack
        - pagerduty

    litellm_settings:
      drop_params: true  # 静默丢弃提供商不兼容的参数而非报错
      set_verbose: false
      enable_pre_call_hooks:
        - helios_tenant_budget_check
        - helios_safety_input_check
      enable_post_call_hooks:
        - helios_cost_record
        - helios_output_audit


此配置的内容：
