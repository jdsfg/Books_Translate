#### 故障模式 1：schema 太刚性

Schema 约束太强以至于模型无法表示有效输出。我们在 §7.3 中写的 `severity: Literal["critical", "major", "minor"]` 字段本身就是一个例子：模型遇到不适合这三个层级的注释级问题，它必须要么 (a) 误分类（强制使用可用层级之一，即使都不适合），或 (b) 拒绝产生输出。两者都不好。

缓解措施：设计带 **显式兜底选项** 的 schema 用于长尾。§7.3 schema 的修复是将 severity 扩展为 `Literal["critical", "major", "minor", "informational"]` 并让模型对不值得真正严重性层级的项目使用 `"informational"`。兜底不必常见；它必须存在。其他字段的相同模式：在模型需要出口的地方添加 `unspecified` 枚举值。

#### 故障模式 2：schema 太宽松

相反。Schema 在应约束的地方允许任意字符串。模型产生验证通过但包含下游代码无法使用的自由格式文本的 JSON。例子：字段定义为 `category: str` 而非 `category: Literal["A", "B", "C"]`；模型产生 `"category": "kind-of-A-but-also-B"` 并破坏下游 switch 语句。

缓解措施：**尽可能紧地约束字段类型以匹配下游代码的期望**。对有限分类集用 `Literal`；对格式约束字符串用 `Field(pattern=...)`；对数值范围用 `Field(ge=..., le=...)`。验证器强制约束；下游代码可以信任它。

#### 故障模式 3：语义但非语法错误

输出是有效 JSON，符合 schema，但错了。模型对拼写修复说 `severity: critical`；模型列出 diff 中不存在的 `file`；模型编造不适用的 `suggested_fix`。验证不捕获这个；只有 eval 能。

缓解措施：**结构验证不够；需要量表或 LLM 作为评判者 eval 对照语义正确性**。第 4 章的 eval 纪律在此适用。发布结构化输出但没有 eval 层的团队在发布一个验证错误答案的解析器。
