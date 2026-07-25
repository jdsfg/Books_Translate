### 3.6 API key 管理：不要提交到仓库

Aiyana 在 Beacon Health AI 的第一个 PR 实际上是三个 PR 的伪装：一个将 CodeReview Bot 连接到 Anthropic，一个将 API key 添加到开发环境，一个为 staging 和生产环境添加单独的 key。key 是 bearer credential——任何拥有 key 的人都可以花公司的钱——围绕处理它的纪律在她第一周内就建立了。

纪律，按照 Beacon 团队写下的顺序：

永远不要将 key 提交到版本控制。key 存活在 secrets manager（HashiCorp Vault、AWS Secrets Manager、GCP Secret Manager）或平台的等效物中，代码在启动时从那里读取它。一个最终进入 `git log` 的 key 是一个必须立即轮换的 key，以及一个必须运行的预算上限审计。

为开发、staging 和生产使用单独的 key。不同的消费预算，不同的审计轨迹，撤销一个不会破坏其他。Beacon 的生产 key 有一个覆盖其典型流量十倍的月度上限；他们的开发 key 上限为每个工程师每月 200 美元，这足够实验且不至于让人失眠。

每季度轮换，或在任何疑似泄露时。季度是保守的；如果你的代码库从 secrets manager 读取，运营成本很小（轮换是一行配置变更）。

使用 provider 的组织功能将 key 限定到项目。Anthropic、OpenAI、Google 都支持子组织 API key 作用域；作用域在你第一次需要调试按项目消费时就会得到回报。

为本地开发使用每个开发者单独的 key，每个有小预算上限，这样凌晨 2 点的失误花费 50 美元而非 50,000 美元。上限是安全网；不运行无速率限制的昂贵实验的纪律才是真正的防御。

按 key 监控消费。一个突然消耗其通常流量 10 倍的 key 要么被泄露要么被误用。对其告警。

Aiyana 的团队持续运行的 canary：一个一行 CLI 脚本从 secrets manager 读取 API key 并发送一个 `Hello, world` 请求。如果 key 损坏或 secrets manager 配置错误，canary 在几秒内告诉你，而非在生产部署之后。
