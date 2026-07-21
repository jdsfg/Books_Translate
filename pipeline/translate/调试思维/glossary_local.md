# 本书本地术语库：调试思维

> 仅本书使用，补充共享库 glossary_cs.md。格式：英文 | 中文 | 备注
> 命中共享库用共享译法；命中本地库用本地译法；两库都无再现译并回填本库。
> ⚠️ 共享库已锁定的词条，本地库不得覆盖。

## 核心锁定（样张强制统一）
debugging | 调试 | 全书统一；debugging thinking = 调试思维；勿译作「除错/排错」作书名核心词
minimal reproducible example | 最小可复现示例 | 缩写可保留 MRE；勿译「最小可重现例子」
observability | 可观测性 | 勿译「观察性」
race condition | 竞态 | 服从共享 glossary_cs；首现可写「竞态（race condition）」；禁止用「竞态条件」覆盖共享译法

## 调试方法与循环
scientific method | 科学方法 |
observe | 观察 |
hypothesize | 假设 |
predict | 预测 |
test | 检验 / 测试 | 科学方法步骤语境用「检验」；写测试代码语境用「测试」
narrow | 收窄 |
debugging loop | 调试循环 |
binary search debugging | 二分查找调试法 |
working backwards | 反向追溯 |
rubber duck debugging | 小黄鸭调试法 |
version comparison | 版本对比 |

## 缺陷与案例专名
Ampersand Bug | Ampersand Bug（与号缺陷） | 贯穿全书的登录失败案例；& 字符原样保留
dead code | 死代码 |
URL encoding | URL 编码 |

## 认知偏差（第3章）
confirmation bias | 确认偏差 |
anchoring | 锚定 |
availability heuristic | 可得性启发 |
premature closure | 过早闭合 |
