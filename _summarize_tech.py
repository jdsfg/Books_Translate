import re

for fname, label in [('_issues_systemdesign.txt', '系统设计思维'), ('_issues_distributed.txt', '分布式系统')]:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = r'=== (\w+) \((\d+) occurrences\) ==='
    matches = re.findall(pattern, content)
    
    print(f'\n{label} — 全部 {len(matches)} 个词：')
    # Only show words with >= 3 occurrences for brevity
    for word, count in matches:
        if int(count) >= 3:
            print(f'  {word}: {count}')
    print(f'  ... (仅显示 ≥3 次的词，共 {len([w for w,c in matches if int(c)>=3])} 个)')
