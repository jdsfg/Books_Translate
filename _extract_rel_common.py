import re

with open('_issues_relationships.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Clearly proper nouns / book title words / tech acronyms - skip these
skip_words = {
    # People names
    'gottman', 'coan', 'karen', 'hrdy', 'david', 'finkel', 'perel', 'fisher',
    'marcus', 'tanya', 'waldinger', 'ethan', 'lin', 'vaillant', 'james',
    'johnson', 'helen', 'robert', 'sarah', 'sue', 'putnam', 'john', 'eli',
    'alex', 'sofia', 'esther', 'diamond', 'holt', 'lunstad', 'maya',
    'margaret', 'bowlby', 'ainsworth', 'chapman', 'knee', 'lisa', 'reis',
    'williams', 'murthy', 'nagoski', 'coleman', 'hazan', 'shaver', 'ted',
    'kolk', 'der', 'van', 'park', 'gable', 'bancroft', 'emily', 'janssen',
    'chen', 'patel', 'reyes', 'whitfield', 'mia', 'vivek', 'raymond',
    'wayne', 'gary', 'harry', 'porges', 'wallace', 'julianne', 'ben',
    'bessel', 'mary', 'george', 'hooton', 'kim', 'shelly', 'aron', 'sis',
    'vasquez', 'austin', 'socratopia', 'glueck', 'marc', 'schulz', 'stan',
    'tatkin', 'erick', 'cindy', 'phillip', 'stephen', 'daniel', 'siegel',
    'eleanor', 'sheldon', 'arthur', 'coontz', 'stephanie', 'elena', 'julie',
    'aaliyah', 'jaden', 'lydia', 'robin', 'antonio', 'denworth', 'dunbar',
    'lucilius', 'christian',
    # Place names
    'brooklyn', 'seattle', 'harvard', 'san',
    # Tech acronyms
    'cbct', 'dpa', 'cbt', 'ptsd', 'emdr', 'mri', 'intj', 'ses', 'psycho',
    # Book title words (in italicized titles)
    'love', 'five', 'languages', 'making', 'marriage', 'principles', 'seven',
    'lab', 'body', 'keeps', 'secure', 'earnest', 'good', 'hold', 'mind',
    'tight', 'cure', 'work', 'fail', 'wired', 'affairs', 'captivity',
    'come', 'mating', 'gap', 'history', 'alone', 'bowling', 'mother',
    'mothers', 'nature', 'others', 'bond', 'friends', 'friendship', 'kids',
    'relationships', 'why', 'experience', 'triumphs', 'phubbing', 'anatomy',
    'eros', 'philia', 'agape', 'succeed', 'marriages', 'life', 'relationship',
    'scholar', 'stoic',
}

# Extract sections for words NOT in skip set
pattern = r'=== (\w+) \((\d+) occurrences\) ===\n(.*?)(?=\n=== |\Z)'
matches = re.findall(pattern, content, re.DOTALL)

print(f'需要检查上下文的普通词（非人名/非书名）：')
print()
for word, count, body in matches:
    if word.lower() not in skip_words:
        print(f'=== {word} ({count} occurrences) ===')
        print(body.strip())
        print()
