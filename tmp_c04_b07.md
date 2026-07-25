### 3.5 速率限制与 429

每个 provider 都对 _每分钟请求数_（RPM）和 _每分钟 token 数_（TPM）进行速率限制。2026 年的默认层级很紧：Anthropic 的免费层级从约 50 RPM / 50K TPM 开始；OpenAI 类似。付费层级（通常从 tier 1 到 tier 5，以总消费为门槛）扩展到数千 RPM 和数百万 TPM。

当你超过限制时，API 返回 HTTP **429 Too Many Requests**。响应包含一个 `retry-after` 头（或等效物）告诉你等待多久。标准做法：

    import time
    from anthropic import APIError

    def call_with_retry(client, max_attempts=5, **kwargs):
        for attempt in range(max_attempts):
            try:
                return client.messages.create(**kwargs)
            except APIError as e:
                if e.status_code == 429:
                    wait = float(e.response.headers.get("retry-after", 2 ** attempt))
                    time.sleep(wait)
                    continue
                raise
        raise RuntimeError("Exceeded max retry attempts on 429.")


这是最小模式。生产代码做更多：

* **在每个响应上读取速率限制头，而非仅在 429 上**，并在剩余预算降到阈值以下时主动退避。
* **添加抖动** 到重试等待中，以避免来自一群 worker 的惊群重试。
* **区分 429（速率限制）、529（过载，Anthropic 特有）和 503（服务不可用）**。重试行为类似但退避间隔不同。
* **有每个用户/每个租户的显式预算**，在你的网关层执行，在请求甚至到达 provider 之前。这是 Helios 使用的 _每租户成本治理_ 模式（第 17 章、第 18 章）。

生产级重试库（Python 中 `tenacity` 是标准选择）封装了所有这些。用一个；不要在上面的最小模式之外自己造。
