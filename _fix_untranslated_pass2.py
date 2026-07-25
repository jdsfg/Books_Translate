import re, os, glob, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

blocks_dir = r'pipeline\translate\软件工程匠艺\blocks'

replacements = [
    # --- c23_b04.md ---
    (r'c23_b04\.md$',
     '在实施前 refine。',
     '在实施前精炼。',
     'refine→精炼'),
    (r'c23_b04\.md$',
     '具体 gotcha',
     '具体陷阱',
     'gotcha→陷阱'),
    (r'c23_b04\.md$',
     'onboarding 文档',
     '入职文档',
     'onboarding→入职'),

    # --- c23_b06.md ---
    (r'c23_b06\.md$',
     'recurring API 成本承诺',
     '经常性的 API 成本承诺',
     'recurring→经常性的'),

    # --- c23_b07.md ---
    (r'c23_b07\.md$',
     '哪个 tier、哪些区域',
     '哪个层级、哪些区域',
     'tier→层级'),

    # --- c23_b08.md ---
    (r'c23_b08\.md$',
     '故事是 composite',
     '故事是组合的',
     'composite→组合的'),

    # --- c23_b09.md ---
    (r'c23_b09\.md$',
     '* Off-by-one：',
     '* 差一：',
     'Off-by-one→差一'),

    # --- c24_b03.md ---
    (r'c24_b03\.md$',
     '她的 label-first 约定',
     '她的标签优先约定',
     'label-first→标签优先'),

    # --- c24_b05.md ---
    (r'c24_b05\.md$',
     '只是 prettier',
     '只是更漂亮',
     'prettier→更漂亮'),
    (r'c24_b05\.md$',
     '能 survive 模型更替',
     '能存活模型更替',
     'survive→存活'),

    # --- c25_b03.md ---
    (r'c25_b03\.md$',
     '更新 imports；运行测试',
     '更新导入；运行测试',
     'imports→导入'),
    (r'c25_b03\.md$',
     '保留薄 facade',
     '保留薄门面',
     'facade→门面'),
    (r'c25_b03\.md$',
     '转成 comprehension、',
     '转成推导式、',
     'comprehension→推导式'),

    # --- c25_b04.md ---
    (r'c25_b04\.md$',
     'regression test（假设先前行为错误）',
     '回归测试（假设先前行为错误）',
     'regression test→回归测试'),
    (r'c25_b04\.md$',
     'unit test（断言预期行为）',
     '单元测试（断言预期行为）',
     'unit test→单元测试'),

    # --- c25_b08.md ---
    (r'c25_b08\.md$',
     'off-by-one / 边界错误',
     '差一 / 边界错误',
     'off-by-one→差一'),
    (r'c25_b08\.md$',
     'Happy-path 偏见',
     '正常路径偏见',
     'Happy-path→正常路径'),

    # --- c25_b11.md ---
    (r'c25_b11\.md$',
     '被 typosquat）',
     '被抢注）',
     'typosquat→抢注'),

    # --- c25_b12.md ---
    (r'c25_b12\.md$',
     'standing artifacts',
     '常驻产物',
     'standing artifacts→常驻产物'),
    (r'c25_b12\.md$',
     '代码库特定 gotcha',
     '代码库特定陷阱',
     'gotcha→陷阱'),
]

files = sorted(glob.glob(os.path.join(blocks_dir, '*.md')))
changed = 0

for fp in files:
    fname = os.path.basename(fp)
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    for pattern, old, new, note in replacements:
        if re.search(pattern, fname):
            if old in content:
                content = content.replace(old, new, 1)
                print(f'  [{fname}] {note}: "{old[:40]}" -> "{new[:40]}"')

    if content != original:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)
        changed += 1
        print(f'  >> Wrote {fname}')

print(f'\nDone. {changed} files changed.')
