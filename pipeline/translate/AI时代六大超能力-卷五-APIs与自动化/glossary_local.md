# 本书本地术语库：AI时代六大超能力-卷五-APIs与自动化

> 仅本书使用，补充共享库 glossary_cs.md。格式：英文 | 中文 | 备注
> 命中共享库用共享译法；命中本地库用本地译法；两库都无再现译并回填本库。

## API 与接口
API | API | 保留英文；全称 Application Programming Interface 可注「应用程序接口」
endpoint | 端点 | 服务对外暴露的具体地址/入口
counter window | 柜台窗口 | 本书核心隐喻：API 是给机器开的侧门/柜台
side door | 侧门 | 与柜台窗口同系隐喻
request | 请求 |
response | 响应 |
HTTP | HTTP | 保留
GET | GET | 保留方法名
POST | POST | 保留方法名
PUT | PUT | 保留方法名
PATCH | PATCH | 保留方法名
DELETE | DELETE | 保留方法名
status code | 状态码 |
header | 请求头 / 响应头 | 视上下文；也可说 header
payload | 载荷 | 请求/响应体内容
query parameter | 查询参数 |
path parameter | 路径参数 |
rate limit | 速率限制 | 亦可「限流」
webhook | Webhook | 保留英文；可注「网络钩子/门铃」；本书用门铃隐喻
callback | 回调 |

## 数据格式
JSON | JSON | 保留英文；全称 JavaScript Object Notation 可注
key | 键 | JSON 字段名语境
value | 值 | JSON 字段值语境
object | 对象 | JSON 对象
array | 数组 | JSON 数组
field | 字段 |
schema | 模式 / 结构 | API 文档中的数据结构说明

## 密钥与身份（勿与 JSON 的 key 混淆）
API key | API 密钥 | 机器身份凭证；持有者即「你」
key | 密钥 | **身份/鉴权语境**；区别于 JSON 的「键」
secret | 机密 / 密钥 | 视上下文；secret key 作「密钥」
token | 令牌 | 鉴权令牌；OAuth access token 等
credential | 凭证 |
authentication | 身份认证 |
authorization | 授权 |
identity | 身份 |
permission | 权限 |
scope | 权限范围 | OAuth scope
least privilege | 最小权限 |
read-only | 只读 |
write access | 写入权限 |

## 读与写 / 可逆性（安全判断，不可弱化）
read | 读取 | 廉价、通常可逆
send | 发送 | 常不可逆，需人手把关
write | 写入 |
irreversible | 不可逆 |
reversible | 可逆 |
side effect | 副作用 |
destructive | 破坏性 / 不可逆的 |
dry run | 干跑 / 试运行 | 不产生真实副作用的预演

## 自动化与智能体
automation | 自动化 |
pipeline | 流水线 / 管道 | 本书「管道」隐喻与 plumbing 呼应时可译「管道」
plumbing | 管道 / 管件 | 本书核心隐喻：人在工具之间充当连接
agent | 智能体 | 与 glossary_ai 一致；AI agent
AI assistant | AI 助手 |
trigger | 触发器 / 触发条件 |
action | 动作 |
workflow | 工作流 |
cron | cron | 保留；可注定时任务
polling | 轮询 |
event | 事件 |
misfire | 误触发 / 走火 | 自动化在无人值守时出错

## 工具与平台（专有名保留）
curl | curl | 保留
Zapier | Zapier | 保留
Make | Make | 保留（原 Integromat）
n8n | n8n | 保留
GitHub Actions | GitHub Actions | 保留
OAuth | OAuth | 保留
REST | REST | 保留
GraphQL | GraphQL | 保留

## 本书叙事锚点
Mara | Mara | 陶工角色名保留
Socratopia | Socratopia | 平台名保留
map | 地图 | 相对「手册」；概念地图，非地理
manual | 手册 | 与地图对立：死记硬背的说明书
territory | 疆域 | 综合项目隐喻
capstone | 综合项目 |
