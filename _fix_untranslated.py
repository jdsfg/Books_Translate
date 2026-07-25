import re, os, glob, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

blocks_dir = r'pipeline\translate\软件工程匠艺\blocks'

# (file_pattern, old_text, new_text, note)
# Only replace in prose context, never in code blocks or inline code.
# Each replacement is specific enough to avoid false positives.

replacements = [
    # --- c20_b06.md ---
    (r'c20_b06\.md$',
     'mentoring 他们错过的模式',
     '指导他们错过的模式',
     'mentoring→指导'),

    # --- c20_b07.md ---
    (r'c20_b07\.md$',
     '不是偶尔 episodic。',
     '不是偶尔的。',
     'episodic→偶尔的'),

    # --- c21_b03.md ---
    (r'c21_b03\.md$',
     '保留作为 fallback。',
     '保留作为备用。',
     'fallback→备用'),

    # --- c22_b05.md ---
    (r'c22_b05\.md$',
     '哪些只是 vestigial。',
     '哪些只是残留的。',
     'vestigial→残留的'),
    (r'c22_b05\.md$',
     '是 load-bearing、',
     '是承重的、',
     'load-bearing→承重的'),

    # --- c23_b03.md ---
    (r'c23_b03\.md$',
     '窄版本 risky。',
     '窄版本有风险。',
     'risky→有风险'),

    # --- c23_b05.md ---
    (r'c23_b05\.md$',
     'AI  surface 战术问题',
     'AI 浮现战术问题',
     'surface→浮现'),
    (r'c23_b05\.md$',
     '一致性 issues。',
     '一致性问题。',
     'issues→问题'),

    # --- c23_b06.md ---
    (r'c23_b06\.md$',
     '第二稿 reliably 更好。',
     '第二稿可靠地更好。',
     'reliably→可靠地'),

    # --- c23_b08.md ---
    (r'c23_b08\.md$',
     'subtle off-by-one',
     '微妙的差一错误',
     'subtle off-by-one→微妙的差一错误'),
    (r'c23_b08\.md$',
     '在 payments 模块加了变异测试',
     '在支付模块加了变异测试',
     'payments→支付'),

    # --- c23_b12.md ---
    (r'c23_b12\.md$',
     '提示驱动更 fuzzy；',
     '提示驱动更模糊；',
     'fuzzy→模糊'),
    (r'c23_b12\.md$',
     '把 money 从 float 迁移到 Decimal',
     '把金额从 float 迁移到 Decimal',
     'money→金额'),
    (r'c23_b12\.md$',
     '新工程师 onboarding。',
     '新工程师入职。',
     'onboarding→入职'),
    (r'c23_b12\.md$',
     '团队的 standing context',
     '团队的常驻上下文',
     'standing context→常驻上下文'),
    (r'c23_b12\.md$',
     '工程师 A 的 lore',
     '工程师 A 的传说',
     'lore→传说'),

    # --- c24_b02.md ---
    (r'c24_b02\.md$',
     '需要更深 rework。',
     '需要更深返工。',
     'rework→返工'),
    (r'c24_b02\.md$',
     '每个 load-bearing 注释处',
     '每个承重注释处',
     'load-bearing→承重'),
    (r'c24_b02\.md$',
     '兼容 shim 的代码',
     '兼容垫片的代码',
     'shim→垫片'),

    # --- c24_b06.md ---
    (r'c24_b06\.md$',
     '能 sustain 代码库',
     '能维持代码库',
     'sustain→维持'),
    (r'c24_b06\.md$',
     '写 happy-path 测试',
     '写正常路径测试',
     'happy-path→正常路径'),

    # --- c25_b04.md ---
    (r'c25_b04\.md$',
     '文档化 turnaround 时间',
     '文档化周转时间',
     'turnaround→周转'),
    (r'c25_b04\.md$',
     '在 enable 团队速度。',
     '在使能团队速度。',
     'enable→使能'),
    (r'c25_b04\.md$',
     '代码库特定 gotcha。',
     '代码库特定陷阱。',
     'gotcha→陷阱'),

    # --- c25_b05.md ---
    (r'c25_b05\.md$',
     'shipped 的代码尚未匹配',
     '已发布的代码尚未匹配',
     'shipped→已发布的'),
    (r'c25_b05\.md$',
     '允许代码 ship 后处于未激活状态',
     '允许代码发布后处于未激活状态',
     'ship→发布'),

    # --- c25_b09.md ---
    (r'c25_b09\.md$',
     '微妙的 off-by-one',
     '微妙的差一',
     'off-by-one→差一'),
    (r'c25_b09\.md$',
     'mentally trace 代码',
     '心理上跟踪代码',
     'mentally trace→心理上跟踪'),
    (r'c25_b09\.md$',
     'typosquat 包名',
     '抢注包名',
     'typosquat→抢注'),

    # --- c25_b11.md ---
    (r'c25_b11\.md$',
     '覆盖 happy path',
     '覆盖正常路径',
     'happy path→正常路径'),

    # --- c16_b05.md ---
    (r'c16_b05\.md$',
     'AI 生成代码 routinely 包含安全错误',
     'AI 生成代码惯常包含安全错误',
     'routinely→惯常'),
    (r'c16_b05\.md$',
     '把 secrets 嵌入代码',
     '把密钥嵌入代码',
     'secrets→密钥'),
    (r'c16_b05\.md$',
     'canonical 库但解析到 typosquatted 包',
     '正规库但解析到抢注包',
     'canonical→正规, typosquatted→抢注'),
    (r'c16_b05\.md$',
     'mentally 用恰好在边界',
     '心理上用恰好在边界',
     'mentally→心理上'),

    # --- c16_b06.md ---
    (r'c16_b06\.md$',
     '人类要 triage 更多问题',
     '人类要分诊更多问题',
     'triage→分诊'),

    # --- c16_b10.md ---
    (r'c16_b10\.md$',
     '品味或 bikeshedding；',
     '品味或钻牛角尖；',
     'bikeshedding→钻牛角尖'),
    (r'c16_b10\.md$',
     '1 个 praise。',
     '1 个表扬。',
     'praise→表扬'),
    (r'c16_b10\.md$',
     '每条评论至少要 ack',
     '每条评论至少要确认',
     'ack→确认'),

    # --- c17_b09.md ---
    (r'c17_b09\.md$',
     'auth 模块 session 处理重构',
     'auth 模块会话处理重构',
     'session→会话'),
    (r'c17_b09\.md$',
     '工作 straightforward。',
     '工作直截了当。',
     'straightforward→直截了当'),
    (r'c17_b09\.md$',
     '何时是 overhead？',
     '何时是开销？',
     'overhead→开销'),
    (r'c17_b09\.md$',
     '是 overhead：',
     '是开销：',
     'overhead→开销'),

    # --- c19_b05.md ---
    (r'c19_b05\.md$',
     '也返回 inactive 客户',
     '也返回不活跃客户',
     'inactive→不活跃'),
    (r'c19_b05\.md$',
     'collectively 它们改变',
     '集体地它们改变',
     'collectively→集体地'),

    # --- c22_b04.md ---
    (r'c22_b04\.md$',
     '如果你 tempted 提议重写',
     '如果你心动提议重写',
     'tempted→心动'),
    (r'c22_b04\.md$',
     '改进可衡量且 substantial 吗',
     '改进可衡量且大量吗',
     'substantial→大量'),

    # --- c16_b05.md (additional) ---
    (r'c16_b05\.md$',
     '硬编码 secrets、token 或凭证',
     '硬编码密钥、token 或凭证',
     'secrets→密钥'),

    # --- c23_b05.md (additional) ---
    (r'c23_b05\.md$',
     'pattern-tax PR',
     '模式税 PR',
     'pattern-tax→模式税'),

    # --- c22_b07.md ---
    (r'c22_b07\.md$',
     'inventory 模块代码包',
     '库存模块代码包',
     'inventory→库存'),

    # --- c24_b06.md (additional) ---
    (r'c24_b06\.md$',
     '杠杆加深。',
     '杠杆加深。',  # no change needed - already Chinese
     'skip'),

    # --- c16_b10.md (additional) ---
    (r'c16_b10\.md$',
     'blocking 逻辑关切',
     '阻塞逻辑关切',
     'blocking→阻塞'),

    # --- c17_b09.md (additional) ---
    (r'c17_b09\.md$',
     '1 个架构建议、1 个范围问题、1 个 praise',
     '1 个架构建议、1 个范围问题、1 个表扬',
     'praise→表扬'),

    # --- c25_b09.md (additional) ---
    (r'c25_b09\.md$',
     '不同 import。',
     '不同导入。',
     'import→导入'),

    # --- c19_b05.md (additional) ---
    (r'c19_b05\.md$',
     'redirect 从泛化名字',
     '重定向从泛化名字',
     'redirect→重定向'),

    # --- c22_b04.md (additional) ---
    (r'c22_b04\.md$',
     'load-bearing 的。',
     '承重的。',
     'load-bearing→承重'),
]

files = sorted(glob.glob(os.path.join(blocks_dir, '*.md')))
changed = 0
skipped = 0

for fp in files:
    fname = os.path.basename(fp)
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    for pattern, old, new, note in replacements:
        if re.search(pattern, fname):
            if old in content:
                content = content.replace(old, new, 1)  # replace first occurrence only
                print(f'  [{fname}] {note}: "{old[:40]}" -> "{new[:40]}"')

    if content != original:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)
        changed += 1
        print(f'  >> Wrote {fname}')

print(f'\nDone. {changed} files changed.')
