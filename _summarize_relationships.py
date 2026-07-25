import re

# Read the file and extract word frequency summary
with open('_issues_relationships.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract all === word (N occurrences) === lines
pattern = r'=== (\w+) \((\d+) occurrences\) ==='
matches = re.findall(pattern, content)

print(f'看见彼此 — 全部 {len(matches)} 个词：')
for word, count in matches:
    print(f'  {word}: {count}')
