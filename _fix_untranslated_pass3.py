import re, os, glob, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

blocks_dir = r'pipeline\translate\软件工程匠艺\blocks'

replacements = [
    # --- c02_b06.md ---
    ('c02_b06.md', 'still 可维护', '仍然可维护', 'still→仍然'),

    # --- c02_b07.md ---
    ('c02_b07.md', 'leverage 很低', '杠杆很低', 'leverage→杠杆'),

    # --- c02_b12.md ---
    ('c02_b12.md', '更 impressive 的 diff', '更令人印象深刻的 diff', 'impressive→令人印象深刻的'),

    # --- c03_b03.md ---
    ('c03_b03.md', '为 inflate 覆盖率', '为膨胀覆盖率', 'inflate→膨胀'),

    # --- c03_b05.md ---
    ('c03_b05.md', 'supposedly 就已经', '据说就已经', 'supposedly→据说'),

    # --- c03_b06.md ---
    ('c03_b06.md', '有一个 caveat', '有一个注意事项', 'caveat→注意事项'),
    ('c03_b06.md', 'trailer，以恢复', '尾注，以恢复', 'trailer→尾注'),
    ('c03_b06.md', '学到更多后 revisit', '学到更多后回顾', 'revisit→回顾'),

    # --- c03_b07.md ---
    ('c03_b07.md', 'docstring 说的事', '文档字符串说的事', 'docstring→文档字符串'),

    # --- c03_b09.md ---
    ('c03_b09.md', 'Senior 更早', '高级工程师更早', 'Senior→高级工程师'),

    # --- c04_b02.md ---
    ('c04_b02.md', 'staging', '暂存', 'staging→暂存'),

    # --- c04_b04.md ---
    ('c04_b04.md', '这个 tag 没有', '这个标签没有', 'tag→标签'),

    # --- c04_b06.md ---
    ('c04_b06.md', 'fixup d4e5f6a', 'fixup d4e5f6a', 'skip-fixup in code'),

    # --- c04_b07.md ---
    ('c04_b07.md', 'ticket ID 的 footer', 'ticket ID 的页脚', 'footer→页脚'),

    # --- c04_b09.md ---
    ('c04_b09.md', '新 util 函数', '新工具函数', 'util→工具'),

    # --- c04_b11.md ---
    ('c04_b11.md', '标记 good 或 bad', '标记好或坏', 'good/bad→好/坏'),
    ('c04_b11.md', 'bisect 可能 inconclusive', 'bisect 可能无结论', 'inconclusive→无结论'),

    # --- c04_b12.md ---
    ('c04_b12.md', '进入 patch 模式', '进入补丁模式', 'patch→补丁'),

    # --- c05_b03.md ---
    ('c05_b03.md', '`feat` 升 minor', '`feat` 升次版本', 'minor→次版本'),
    ('c05_b03.md', '`fix` 升 patch', '`fix` 升补丁版本', 'patch→补丁版本'),
    ('c05_b03.md', '`BREAKING CHANGE` 升 major', '`BREAKING CHANGE` 升主版本', 'major→主版本'),

    # --- c05_b04.md ---
    ('c05_b04.md', '富 targeting 规则', '富定向规则', 'targeting→定向'),
    ('c05_b04.md', '专注的 sitting 内', '专注的坐定时间内', 'sitting→坐定时间'),

    # --- c05_b06.md ---
    ('c05_b06.md', '每天 shipping 10 个', '每天发布 10 个', 'shipping→发布'),

    # --- c06_b03.md ---
    ('c06_b03.md', '简单 getter 的测试', '简单获取器的测试', 'getter→获取器'),

    # --- c06_b05.md ---
    ('c06_b05.md', '快速 sanity 检查', '快速健全性检查', 'sanity→健全性'),
    ('c06_b05.md', '把 arrange 和 act 混', '把准备和执行混', 'arrange/act→准备/执行'),

    # --- c06_b07.md ---
    ('c06_b07.md', '标记为 skipped', '标记为跳过', 'skipped→跳过'),
    ('c06_b07.md', 'flake 超过 3 次', '抖动超过 3 次', 'flake→抖动'),

    # --- c07_b01.md ---
    ('c07_b01.md', '差一错误 round', '差一错误轮次', 'round→轮次'),

    # --- c07_b03.md ---
    ('c07_b03.md', '优秀的 shrinking', '优秀的缩减', 'shrinking→缩减'),
    ('c07_b03.md', '基于 macro 的', '基于宏的', 'macro→宏'),

    # --- c07_b04.md ---
    ('c07_b04.md', '删除 return 语句', '删除返回语句', 'return→返回'),

    # --- c07_b08.md ---
    ('c07_b08.md', '把 email 替换', '把电子邮件替换', 'email→电子邮件'),

    # --- c09_b04.md ---
    ('c09_b04.md', 'AI 的 compliance', 'AI 的合规性', 'compliance→合规性'),

    # --- c09_b08.md ---
    ('c09_b08.md', '负 paid 金额', '负已付金额', 'paid→已付'),

    # --- c09_b11.md ---
    ('c09_b11.md', '最 informative', '最有信息量', 'informative→有信息量'),
    ('c09_b11.md', '这里的 reasoning', '这里的推理', 'reasoning→推理'),

    # --- c10_b03.md ---
    ('c10_b03.md', 'Consolidate 成', '合并成', 'Consolidate→合并'),

    # --- c10_b12.md ---
    ('c10_b12.md', '顺手把 process', '顺手把 process', 'skip-code-id'),

    # --- c11_b09.md ---
    ('c11_b09.md', 'bootstrap 操作', '引导操作', 'bootstrap→引导'),

    # --- c12_b07.md ---
    ('c12_b07.md', '一个 metrics 服务', '一个指标服务', 'metrics→指标'),

    # --- c12_b09.md ---
    ('c12_b09.md', 'discrepancy', '差异', 'discrepancy→差异'),

    # --- c12_b13.md ---
    ('c12_b13.md', '以 explicit 业务', '以显式业务', 'explicit→显式'),

    # --- c12_b14.md ---
    ('c12_b14.md', 'upfront 规划', '前置规划', 'upfront→前置'),

    # --- c13_b09.md ---
    ('c13_b09.md', '一个 Protocol +', '一个协议 +', 'Protocol→协议'),

    # --- c14_b01.md ---
    ('c14_b01.md', '2026 年 hindsight', '2026 年的后见之明', 'hindsight→后见之明'),
    ('c14_b01.md', '没人想 debug', '没人想调试', 'debug→调试'),

    # --- c14_b05.md ---
    ('c14_b05.md', '用策略函数或 hook', '用策略函数或钩子', 'hook→钩子'),
    ('c14_b05.md', '显式 Memento', '显式备忘录', 'Memento→备忘录'),

    # --- c15_b11.md ---
    ('c15_b11.md', 'Handler 把 HTTP', '处理器把 HTTP', 'Handler→处理器'),

    # --- c15_b14.md ---
    ('c15_b14.md', 'decision 的 `total`', '决策的 `total`', 'decision→决策'),

    # --- c16_b08.md ---
    ('c16_b08.md', '返回费 LTV', '返回费 LTV', 'skip-context'),

    # --- c16_b12.md ---
    ('c16_b12.md', 'customer 或 order', 'customer 或 order', 'skip-code-ids'),

    # --- c16_b15.md ---
    ('c16_b15.md', '团队 wiki', '团队维基', 'wiki→维基'),

    # --- c17_b02.md ---
    ('c17_b02.md', 'commit message 遵循', '提交信息遵循', 'message→信息'),

    # --- c17_b04.md ---
    ('c17_b04.md', '没有 ego', '没有自我', 'ego→自我'),

    # --- c17_b07.md ---
    ('c17_b07.md', 'Data 负责人', '数据负责人', 'Data→数据'),
    ('c17_b07.md', 'threaded 进行', '线程化进行', 'threaded→线程化'),

    # --- c17_b11.md ---
    ('c17_b11.md', '更 productive', '更高产', 'productive→高产'),

    # --- c18_b01.md ---
    ('c18_b01.md', '三个链接：仓库根目录的 README', '三个链接：仓库根目录的 README', 'skip'),

    # --- c18_b03.md ---
    ('c18_b03.md', 'Trunk-Based Development', '主干开发', 'Trunk-Based Development→主干开发'),

    # --- c18_b04.md ---
    ('c18_b04.md', 'API pods 扩容', 'API pod 扩容', 'skip-pod-is-jargon'),

    # --- c18_b07.md ---
    ('c18_b07.md', 'Drizzle wrapper', 'Drizzle 包装器', 'wrapper→包装器'),

    # --- c18_b10.md ---
    ('c18_b10.md', 'page DBA on-call', '呼叫 DBA on-call', 'page→呼叫'),

    # --- c18_b11.md ---
    ('c18_b11.md', 'prefer 依赖注入', '偏好依赖注入', 'prefer→偏好'),
    ('c18_b11.md', 'prefer 模式匹配', '偏好模式匹配', 'prefer→偏好'),

    # --- c19_b13.md ---
    ('c19_b13.md', '最 distinctive', '最独特', 'distinctive→独特'),

    # --- c20_b03.md ---
    ('c20_b03.md', 'On-call 负担', '值班负担', 'On-call→值班'),
    ('c20_b03.md', 'on-call 事故', '值班事故', 'on-call→值班'),
    ('c20_b03.md', 'on-call 率', '值班率', 'on-call→值班'),

    # --- c21_b03.md ---
    ('c21_b03.md', 'Modern 服务', '现代服务', 'Modern→现代'),
    ('c21_b03.md', 'Legacy 服务', '遗留服务', 'Legacy→遗留'),

    # --- c21_b04.md ---
    ('c21_b04.md', 'Branch by Abstraction', '抽象分支', 'Branch by Abstraction→抽象分支'),
    ('c21_b04.md', 'flag flip', '标志翻转', 'flag flip→标志翻转'),

    # --- c22_b01.md ---
    ('c22_b01.md', 'Apple ', 'Apple ', 'skip-proper-noun'),

    # --- c22_b04.md ---
    ('c22_b04.md', '如果你心动提议重写', '如果你心动提议重写', 'skip-already-fixed'),

    # --- c23_b01.md ---
    ('c23_b01.md', '带 rollover credits', '带 rollover 额度', 'credits→额度'),

    # --- c23_b04.md ---
    ('c23_b04.md', '具体 gotcha', '具体陷阱', 'skip-already-fixed'),

    # --- c24_b06.md ---
    ('c24_b06.md', 'framing', '框架', 'framing→框架'),

    # --- c25_b01.md ---
    ('c25_b01.md', 'Andrew Hunt 与 David Thomas', 'Andrew Hunt 与 David Thomas', 'skip-names'),
]

files = sorted(glob.glob(os.path.join(blocks_dir, '*.md')))
changed = 0

for fp in files:
    fname = os.path.basename(fp)
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    for target_fname, old, new, note in replacements:
        if fname == target_fname:
            if note.startswith('skip'):
                continue
            if old in content:
                content = content.replace(old, new, 1)
                print(f'  [{fname}] {note}: "{old[:40]}" -> "{new[:40]}"')

    if content != original:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)
        changed += 1
        print(f'  >> Wrote {fname}')

print(f'\nDone. {changed} files changed.')
