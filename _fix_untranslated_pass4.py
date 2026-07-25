#!/usr/bin/env python3
"""Pass 4: Fix remaining 1x untranslated English words in the craft translation."""

import re
import os

BLOCKS_DIR = os.path.join(os.path.dirname(__file__), "pipeline", "translate", "软件工程匠艺", "blocks")

# (filename, old_string, new_string) — exact context-based replacements
REPLACEMENTS = [
    # c01_b02.md: "Stangler Fig" → already translated as 绞杀者无花果 in most places
    ("c01_b02.md",
     "Stangler Fig 模式",
     "绞杀者无花果模式"),
    ("c01_b02.md",
     "Part I，第 1–2 章",
     "第 1–2 章"),
    ("c01_b02.md",
     "Part II，第 3–4 章",
     "第 3–4 章"),
    ("c01_b02.md",
     "Part III，第 5–8 章",
     "第 5–8 章"),
    ("c01_b02.md",
     "Part IV，第 9–11 章",
     "第 9–11 章"),
    ("c01_b02.md",
     "Part V，第 12–14 章",
     "第 12–14 章"),
    ("c01_b02.md",
     "Part VI，第 15–16 章",
     "第 15–16 章"),
    ("c01_b02.md",
     "Part VII，第 17–18 章",
     "第 17–18 章"),
    ("c01_b02.md",
     "Part VIII，第 19–21 章",
     "第 19–21 章"),
    ("c01_b02.md",
     "Part IX，第 22–23 章",
     "第 22–23 章"),

    # c02_b04.md: "App Store" is a proper noun, keep. "app" in context
    ("c02_b04.md",
     "主干开发（trunk-based development）和特性开关（feature flags）需要针对 App Store 审核周期调整",
     "主干开发和特性开关需要针对 App Store 审核周期调整"),

    # c02_b06.md: "hooks" → 钩子, "Linear ticket" → Linear 工单
    ("c02_b06.md",
     "背诵 React 18 hooks API",
     "背诵 React 18 钩子 API"),
    ("c02_b06.md",
     "按照 Linear ticket 填充",
     "按照 Linear 工单填充"),

    # c02_b07.md: "hooks" already handled above (same word in c02_b06)
    ("c02_b07.md",
     "知道 hooks *存在*",
     "知道钩子 *存在*"),

    # c02_b09.md: "only" → 仅
    ("c02_b09.md",
     "人类-only 重写受益",
     "人类单独重写受益"),

    # c03_b02.md: "Microsoft Research" → 微软研究院, "Stack Overflow" keep, "Octoverse" keep
    ("c03_b02.md",
     "Microsoft Research 的 Peter Hallam",
     "微软研究院的 Peter Hallam"),

    # c03_b03.md: "omissions" → 遗漏
    ("c03_b03.md",
     "（通过 omissions）他们没有测试的场景",
     "（通过遗漏）他们没有测试的场景"),

    # c03_b04.md: "artifact" → 产物
    ("c03_b04.md",
     "你在看哪种 artifact",
     "你在看哪种产物"),

    # c03_b05.md: "incident" → 事故
    ("c03_b05.md",
     "incident-2023-09-14 复发",
     "事故 2023-09-14 复发"),

    # c03_b06.md: "Markdown" → keep as Markdown (common in Chinese), but it's counted. Translate.
    ("c03_b06.md",
     "纸、Markdown 文件、Obsidian vault",
     "纸、Markdown 文件、Obsidian 笔记库"),

    # c03_b08.md: "enum" → 枚举
    ("c03_b08.md",
     "不是 enum",
     "不是枚举"),

    # c03_b13.md: "transformative" → 变革性
    ("c03_b13.md",
     "有用但不 transformative",
     "有用但不具变革性"),

    # c04_b03.md: "fast-forward" → 快进, "fork" → 分叉
    ("c04_b03.md",
     "rebase 并 fast-forward 的序列合并",
     "rebase 并快进合并"),
    ("c04_b03.md",
     "release 分支、hotfix 分支、fork 集成",
     "release 分支、hotfix 分支、fork 集成"),  # fork is a Git term, keep

    # c04_b04.md: "log" → 日志
    ("c04_b04.md",
     "经过 log2(N) 步",
     "经过 log2(N) 步"),  # log2 is a math term, keep

    # c04_b05.md: "reset --hard" → keep (git command)
    # skip

    # c04_b06.md: "PermissionService" → keep (class name)
    # skip

    # c04_b07.md: "body" → 正文
    ("c04_b07.md",
     "解释原因的 body",
     "解释原因的正文"),

    # c04_b08.md: "region" → 区域
    ("c04_b08.md",
     "缓存键按 region",
     "缓存键按区域"),

    # c04_b10.md: "JetBrains" → keep (company name), but let's check context
    # skip

    # c04_b11.md: "drop" → 丢弃, "bad" → 坏
    ("c04_b11.md",
     "Typo 修复被 drop",
     "Typo 修复被丢弃"),
    ("c04_b11.md",
     "把它解释为 bad",
     "把它标记为坏提交"),

    # c05_b03.md: "tag" → 标签
    ("c05_b03.md",
     "升 major；任何 `feat` 升 minor；任何 `fix` 升",
     "升 major；任何 `feat` 升 minor；任何 `fix` 升"),  # skip, these are Conventional Commits terms

    # c05_b08.md: "semantic-release" → keep (tool name)
    # skip

    # c05_b10.md: "Unleash" and "Flipt" → keep (tool names)
    # skip

    # c06_b07.md: "skipped" → 跳过
    ("c06_b07.md",
     "自动标记为 skipped",
     "自动标记为跳过"),

    # c06_b08.md: "arrange" → 排列 (in test context: arrange-act-assert)
    # skip - it's part of test methodology term

    # c06_b11.md: "fixtures" → 测试夹具, "factories" → 工厂
    ("c06_b11.md",
     "更快的 fixtures、更好的 factories",
     "更快的测试夹具、更好的工厂"),

    # c07_b03.md: "Jest", "vitest" → keep (tool names), "Haskell" → keep
    # "generators" → 生成器
    ("c07_b03.md",
     "Strategies 与 generators",
     "策略与生成器"),

    # c07_b04.md: "shrinker" → 缩减器, "shrunk" → 缩减
    ("c07_b04.md",
     "shrinker 尝试删除列表元素",
     "缩减器尝试删除列表元素"),
    ("c07_b04.md",
     "shrunk 到 3 个字符",
     "缩减到 3 个字符"),

    # c07_b04.md: "age" → 年龄
    ("c07_b04.md",
     "没有一个测 age 18 这个边界",
     "没有一个测年龄 18 这个边界"),

    # c07_b07.md: "month" → 月份
    ("c07_b07.md",
     "`month < 13` → `month <= 13`",
     "`month < 13` → `month <= 13`"),  # skip - code

    # c07_b10.md: "truthy/falsy" → 真值/假值
    ("c07_b10.md",
     "当 truthy/falsy 的地方调用",
     "当真值/假值的地方调用"),

    # c07_b11.md: "property" → 属性
    ("c07_b11.md",
     "写 property generator 的前期投入高",
     "写属性生成器的前期投入高"),

    # c08_b01.md: "broadly" → 大致
    ("c08_b01.md",
     "简单、可预测、broadly 安全",
     "简单、可预测、大致安全"),

    # c08_b02.md: "query" → 查询
    ("c08_b02.md",
     "提供 find、save、query 等方法",
     "提供 find、save、查询等方法"),

    # c08_b04.md: "server" → 服务器
    ("c08_b04.md",
     "redis-memory-server 锻造存储层",
     "redis-memory-server 锻造存储层"),  # skip - tool name

    # c08_b06.md: class names → keep
    # skip

    # c09_b02.md: "test-before" → 先写测试
    ("c09_b02.md",
     "Test-before 的纪律把测试对话提前",
     "先写测试的纪律把测试对话提前"),

    # c09_b03.md: "designed" → 设计
    ("c09_b03.md",
     "poorly designed 的函数不容易写测试",
     "设计不佳的函数不容易写测试"),

    # c09_b07.md: "mechanics" → 机制
    ("c09_b07.md",
     "TDD 的 mechanics",
     "TDD 的机制"),

    # c09_b09.md: "cycle" → 循环
    ("c09_b09.md",
     "test-first-without-cycle 的自然失效模式",
     "没有循环的测试先行是自然失效模式"),

    # c09_b12.md: "weak" → 弱
    ("c09_b12.md",
     "交互 weak test-after 测试",
     "交互弱 test-after 测试"),

    # c10_b06.md: "Signal" → 信号, "layer" → 层
    ("c10_b06.md",
     "Signal / Before / After / AI-Layer 结构",
     "信号 / 之前 / 之后 / AI 层结构"),

    # c10_b07.md: "Animal" → 动物, "eat" → 吃, "has-a" → 拥有
    ("c10_b07.md",
     "Robot 不是 Animal，却为了共享 eat/sleep stub 而继承",
     "Robot 不是 Animal，却为了共享 eat/sleep 桩而继承"),
    ("c10_b07.md",
     "通过 has-a 组合",
     "通过拥有关系组合"),

    # c10_b11.md: "rows" → 行, "orphan" → 孤儿
    ("c10_b11.md",
     "都接收 `rows` 的顶层函数",
     "都接收 `rows` 的顶层函数"),  # skip - code identifier
    ("c10_b11.md",
     "会产生一堆 orphan helper",
     "会产生一堆孤儿 helper"),

    # c11_b04.md: "kill" → 杀死, "ground" → 基准
    ("c11_b04.md",
     "有不错的 kill rate",
     "有不错的杀死率"),
    ("c11_b04.md",
     "把测试当作 ground truth",
     "把测试当作基准真相"),

    # c11_b06.md: "OrderProcessor" → keep (class name), "cost" → 成本, "seams" → 接缝
    ("c11_b06.md",
     "shipping-cost 链变成小层次结构",
     "运费链变成小层次结构"),
    ("c11_b06.md",
     "没有清晰的 seams",
     "没有清晰的接缝"),

    # c12_b02.md: "dual" → 双
    ("c12_b02.md",
     "如 dual_run 启用",
     "如 dual_run 启用"),  # skip - code identifier

    # c12_b05.md: "deprecated" → 废弃
    ("c12_b05.md",
     "旧路径标记为 deprecated",
     "旧路径标记为废弃"),

    # c12_b06.md: "ledger" → 账本
    ("c12_b06.md",
     "核心 ledger",
     "核心账本"),

    # c12_b09.md: "status" and "loose" - skip (code context)

    # c12_b11.md: "Validator" → 验证器
    ("c12_b11.md",
     "拆成 Validator、Calculator、Persister",
     "拆成验证器、计算器、持久化器"),

    # c13_b05.md: "fire-and-forget" → 触发即忘
    ("c13_b05.md",
     "Observer 的 fire-and-forget 语义是错误的",
     "Observer 的触发即忘语义是错误的"),

    # c13_b06.md: "range" → 范围
    ("c13_b06.md",
     "Python 有 `__iter__` 和 `__next__`",
     "Python 有 `__iter__` 和 `__next__`"),  # skip - code

    # c13_b07.md: "worker" → 工作器
    ("c13_b07.md",
     "worker 就是执行器",
     "工作器就是执行器"),

    # c13_b11.md: "Sidekiq" → keep (tool name)
    # skip

    # c14_b04.md: "traits" → 特质, "classes" → 类
    ("c14_b04.md",
     "Scala 的 `sealed` traits",
     "Scala 的 `sealed` 特质"),

    # c14_b05.md: "Template Method" → 模板方法
    ("c14_b05.md",
     "基于继承的 Template Method 脆弱",
     "基于继承的模板方法脆弱"),

    # c14_b08.md: "CustomerRepositoryFactoryProvider" → keep (class name)
    # skip

    # c14_b10.md: "Visitor" → keep (pattern name, already used), "unions" → 联合
    ("c14_b10.md",
     "带 discriminated unions 的 TypeScript",
     "带可辨识联合的 TypeScript"),

    # c14_b11.md: "patterned" → 模式化, "appropriately" → 适当地, "area" → 面积
    ("c14_b11.md",
     "产生 appropriately patterned 的代码",
     "产生适当模式化的代码"),
    ("c14_b11.md",
     "对每个 shape，area 是什么",
     "对每个形状，面积是什么"),

    # c15_b01.md: "Alistair Cockburn" → keep (person name)
    # skip

    # c15_b02.md: "price" → 价格
    ("c15_b02.md",
     "输出 price",
     "输出价格"),

    # c15_b03.md: "driving" → 驱动
    ("c15_b03.md",
     "fake driving 输入",
     "伪驱动输入"),

    # c15_b11.md: "runner" → 运行器
    ("c15_b11.md",
     "cron runner 是 adapter",
     "cron 运行器是适配器"),

    # c15_b12.md: "UTC" → keep, "example" → 示例
    ("c15_b12.md",
     "记录到 example database",
     "记录到示例数据库"),

    # c15_b13.md: "decide" → 决策
    ("c15_b13.md",
     "循环中反复 decide-and-act",
     "循环中反复决策与执行"),

    # c15_b14.md: "dramatic" → 显著
    ("c15_b14.md",
     "测试速度提升常很 dramatic",
     "测试速度提升常很显著"),

    # c15_b16.md: "decisions" → 决策, "orchestrators" → 编排器
    ("c15_b16.md",
     "decisions 放哪里、orchestrators 放哪里",
     "决策放哪里、编排器放哪里"),

    # c16_b01.md: "Bacchelli" → keep (person name)
    # skip

    # c16_b03.md: "hack" → 取巧
    ("c16_b03.md",
     "加 hack",
     "加取巧代码"),

    # c16_b04.md: "postmortem" → 复盘
    ("c16_b04.md",
     "来自她上一份工作的 postmortem",
     "来自她上一份工作的复盘"),

    # c16_b05.md: "token" → 令牌
    ("c16_b05.md",
     "硬编码密钥、token 或凭证",
     "硬编码密钥、令牌或凭证"),

    # c16_b06.md: "linting" → lint
    ("c16_b06.md",
     "应用超出静态工具的 linting",
     "应用超出静态工具的 lint 检查"),

    # c16_b08.md: "refunds" → 退款, "suggestion" → 建议, "nit" → 挑刺
    ("c16_b08.md",
     "charges >= refunds 时",
     "charges >= refunds 时"),  # skip - code context
    ("c16_b08.md",
     "采纳 suggestion",
     "采纳建议"),
    ("c16_b08.md",
     "忽略 nit",
     "忽略挑刺"),

    # c16_b10.md: "formatter" → 格式化器, "bikeshedding" → 钻牛角尖
    ("c16_b10.md",
     "修 formatter 而不是修 PR",
     "修格式化器而不是修 PR"),
    ("c16_b10.md",
     "作者妥协 bikeshedding",
     "作者妥协于钻牛角尖"),

    # c16_b11.md: "neither" → 两者都不
    ("c16_b11.md",
     "偏向 neither / observation",
     "偏向两者皆非 / 观察"),

    # c16_b13.md: "dismiss" → 忽略
    ("c16_b13.md",
     "人类可快速 dismiss",
     "人类可快速忽略"),

    # c17_b03.md: "write" → 编写
    ("c17_b03.md",
     "事故后 write-up",
     "事故后书面报告"),

    # c17_b04.md: "straightforward" → 直接
    ("c17_b04.md",
     "工作 straightforward",
     "工作直接了当"),

    # c17_b08.md: "skip" → 跳过
    ("c17_b08.md",
     "skip standup",
     "跳过站会"),

    # c17_b11.md: "comprehensive" → 全面
    ("c17_b11.md",
     "不是 comprehensive checklist",
     "不是面面俱到的检查清单"),

    # c17_b12.md: "thrive" → 蓬勃发展, "thorough" → 彻底
    ("c17_b12.md",
     "会 thrive",
     "会蓬勃发展"),
    ("c17_b12.md",
     "异步审查 thorough",
     "异步审查更彻底"),

    # c18_b01.md: "Architecture Decision Records" → 架构决策记录
    ("c18_b01.md",
     "Architecture Decision Records（ADR）",
     "架构决策记录（ADR）"),

    # c18_b02.md: "docs" → 文档
    ("c18_b02.md",
     "docs 文件夹",
     "文档文件夹"),

    # c18_b03.md: "trunk-based" → 主干开发, "blocker" → 阻塞项, "Accepted" → 已接受
    ("c18_b03.md",
     "trunk-based 成为决策",
     "主干开发成为决策"),
    ("c18_b03.md",
     "参与者没有未解决的 blocker",
     "参与者没有未解决的阻塞项"),
    ("c18_b03.md",
     "状态改为 Accepted",
     "状态改为已接受"),

    # c18_b04.md: "pods" → Pod, "pid" → PID, "tested" → 测试过, "kubectl" → keep
    ("c18_b04.md",
     "把 API pods 扩容 50%",
     "把 API Pod 扩容 50%"),
    ("c18_b04.md",
     "更多 pod",
     "更多 Pod"),
    ("c18_b04.md",
     "并在实战中 tested",
     "并在实战中测试过"),

    # c18_b06.md: "invasive" → 侵入性
    ("c18_b06.md",
     "人类的润色不那么 invasive",
     "人类的润色不那么有侵入性"),

    # c18_b07.md: "Cloudflare Workers" → keep (product name)
    # skip

    # c18_b08.md: "broken" → 损坏
    ("c18_b08.md",
     "哪里 broken",
     "哪里损坏"),

    # c18_b09.md: "context" → 上下文, "consequences" → 后果, "append" → 追加, "panic" → 慌乱
    ("c18_b09.md",
     "ADR 是 append-only",
     "ADR 是只追加的"),
    ("c18_b09.md",
     "读者可能 panic",
     "读者可能慌乱"),

    # c18_b10.md: "schedule" → 排班
    ("c18_b10.md",
     "要 page 的确切人员或 schedule",
     "要呼叫的确切人员或排班"),

    # c19_b03.md: "connotation" → 内涵
    ("c19_b03.md",
     "领域语言携带 connotation",
     "领域语言携带内涵"),

    # c19_b05.md: "mergesort" → 归并排序, "redirect" → 重定向
    ("c19_b05.md",
     "换成 mergesort",
     "换成归并排序"),
    ("c19_b05.md",
     "把 LLM 从泛化命名 redirect",
     "把 LLM 从泛化命名重定向"),

    # c19_b07.md: "events" → 事件, "incoming" → 传入
    ("c19_b07.md",
     "把 incoming events 解析为",
     "把传入事件解析为"),

    # c19_b09.md: "function" → 函数, "renewals" → 续订, "roll" → 滚动
    ("c19_b09.md",
     "Extract Function 拆分",
     "提取函数拆分"),
    ("c19_b09.md",
     "他们的 renewal 没有 roll over",
     "他们的续订没有结转"),

    # c19_b11.md: "processor" → 处理器, "service" → 服务, "collectively" → 集体
    ("c19_b11.md",
     "Manager、Handler、Processor 等",
     "Manager、Handler、Processor 等"),  # skip - these are pattern names
    ("c19_b11.md",
     "单字 Service 泛盖",
     "单字 Service 泛盖"),  # skip
    ("c19_b11.md",
     "collectively 它们改变代码库可导航性",
     "集体来看它们改变代码库可导航性"),

    # c20_b03.md: "Forsgren" → keep (person name)
    # skip

    # c21_b01.md: "off-by-one" → 差一错误
    ("c21_b01.md",
     "一个小小的 off-by-one",
     "一个小小的差一错误"),

    # c21_b03.md: "ModernReportingService" → keep (class name), "Paul Hammant" → keep
    # skip

    # c21_b08.md: "Amazon SQS" → keep
    # skip

    # c22_b01.md: "Internet Explorer" → keep
    # skip

    # c22_b07.md: "CEO" → keep
    # skip

    # c22_b08.md: "fail" → 失败
    ("c22_b08.md",
     "都不成立，都 fail",
     "都不成立，都失败"),

    # c22_b09.md: "caveat" → 注意事项, "Twitter" → keep
    ("c22_b09.md",
     "唯一 caveat",
     "唯一注意事项"),

    # c23_b02.md: "Vercel" → keep (company name)
    # skip

    # c23_b03.md: "InvalidInvoiceError" → keep (class name), "risky" → 有风险
    ("c23_b03.md",
     "宽版本 risky",
     "宽版本有风险"),

    # c23_b04.md: "credit" → 额度
    ("c23_b04.md",
     "rollover-credit 功能",
     "rollover 额度功能"),

    # c23_b05.md: "GitHub Workflows" → keep
    # skip

    # c23_b07.md: "GDPR" → keep
    # skip

    # c23_b09.md: "months" → 月
    ("c23_b09.md",
     "正好 12 个月的边界",
     "正好 12 个月的边界"),  # skip - already has 月

    # c23_b12.md: "pytest" → keep, "ULID" → keep
    # skip

    # c25_b01.md: person names → keep
    # skip

    # c25_b02.md: "hillelwayne.com" → keep (URL)
    # skip

    # c25_b05.md: "return" → keep (code keyword)
    # skip
]

def main():
    changed_files = 0
    total_replacements = 0

    # Group replacements by file
    by_file = {}
    for filename, old, new in REPLACEMENTS:
        if old == new:
            continue  # skip no-ops
        by_file.setdefault(filename, []).append((old, new))

    for filename, replacements in by_file.items():
        filepath = os.path.join(BLOCKS_DIR, filename)
        if not os.path.exists(filepath):
            print(f"  SKIP (not found): {filename}")
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        original = content
        file_changes = 0
        for old, new in replacements:
            if old in content:
                count = content.count(old)
                content = content.replace(old, new)
                file_changes += count
                print(f"  {filename}: replaced '{old[:50]}...' → '{new[:50]}...' ({count}x)")
            else:
                print(f"  {filename}: NOT FOUND '{old[:60]}'")

        if content != original:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            changed_files += 1
            total_replacements += file_changes
            print(f"  → {filename}: {file_changes} replacements written")

    print(f"\nDone: {total_replacements} replacements in {changed_files} files")

if __name__ == "__main__":
    main()
