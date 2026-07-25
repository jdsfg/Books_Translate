import re

with open('_issues_relationships.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Check specific words
check = ['bug', 'contemplative', 'developing', 'stoic', 'christian', 'mom', 'tip', 'force', 'agape', 'philia', 'eros']
pattern = r'=== (\w+) \((\d+) occurrences\) ===\n(.*?)(?=\n=== |\Z)'
matches = re.findall(pattern, content, re.DOTALL)

for word, count, body in matches:
    if word.lower() in check:
        print(f'=== {word} ({count} occurrences) ===')
        print(body.strip())
        print()
