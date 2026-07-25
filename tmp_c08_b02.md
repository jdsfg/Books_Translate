### 7.2 现代技术栈：原生 JSON schema 模式

2026 年，主要 provider 提供 **原生 JSON schema 模式**。你提供 JSON schema；API 强制模型输出符合它。在底层，provider 使用 _约束解码_——在每个 token 生成步骤，模型的输出分布被限制为使输出保持为 schema 有效延续的 token。

实现各异：

* **Anthropic** 通过工具使用机制提供结构化输出。你用想要的 schema 定义工具；你设置 `tool_choice` 强制工具；模型输出是工具调用参数，符合 schema。
* **OpenAI** 提供直接接受 JSON schema 的 `response_format` 参数。结构化输出模式（在特定模型版本后）保证 schema 一致性。
* **Google Gemini** 支持类似的响应 schema 参数。

三者都支持相同的基本语义：_模型输出是验证通过你的 schema 的 JSON；API 做强制；如果 schema 无法满足，API 返回错误而非格式错误的输出。_

#### 定义：约束解码

一种 token 生成策略，其中 LLM 的下一 token 概率分布在每步被掩码以仅允许产生所需输出结构（JSON schema、正则表达式、上下文无关文法）有效延续的 token。模型的表达选择被机械地约束；模型不能发出无效输出即使其自然分布会。

用通俗语言：模型通常选任何 token。有约束解码时，选择器被过滤——仅保持输出有效的 token 被允许。结果是 _保证_ 有效的结构，其中 _保证_ 指语法有效性（输出可解析）而非语义正确性（输出可能解析为无意义）。

2026 年默认：**对任何结构化输出使用原生 JSON schema 模式，在任何支持它的 provider 上**。库包装器（`instructor`、`outlines`）在其上添加人体工程学改进。
