import re, os, glob, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

books = {
    '系统设计思维': r'pipeline\translate\系统设计思维：大规模软件的架构之道\blocks',
    '分布式系统': r'pipeline\translate\分布式系统\blocks',
    '看见彼此': r'pipeline\translate\看见彼此——亲密关系的科学\blocks',
}

# Only flag English words DIRECTLY embedded in Chinese sentences.
# Pattern: Chinese char + space + English word + space + Chinese char
# This catches untranslated words in prose, not in code/tables/parentheses.

def scan_book(name, blocks_dir):
    files = sorted(glob.glob(os.path.join(blocks_dir, '*.md')))
    issues = {}
    for fp in files:
        with open(fp, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        in_code = False
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith('```'):
                in_code = not in_code
                continue
            if in_code:
                continue
            # Remove inline code
            clean = re.sub(r'`[^`]*`', '', line)
            # Remove parenthetical English annotations: （English）
            clean = re.sub(r'（[A-Za-z\s\-\.]+）', '', clean)
            # Remove English in parentheses: (English)
            clean = re.sub(r'\([A-Za-z\s\-\.]+\)', '', clean)
            # Remove URLs
            clean = re.sub(r'https?://\S+', '', clean)
            # Remove HTML tags
            clean = re.sub(r'<[^>]+>', '', clean)
            # Find English words adjacent to Chinese characters
            # Pattern: Chinese char followed by English word or vice versa
            matches = re.findall(r'([\u4e00-\u9fff])\s*([a-zA-Z]{3,})\s*([\u4e00-\u9fff])', clean)
            matches += re.findall(r'([a-zA-Z]{3,})\s*([\u4e00-\u9fff])', clean)
            matches2 = re.findall(r'([\u4e00-\u9fff])\s*([a-zA-Z]{3,})', clean)
            all_matches = [(m[1] if len(m)==3 else m[0]) for m in matches] + [m[1] for m in matches2]
            for w in all_matches:
                wl = w.lower()
                if wl not in issues:
                    issues[wl] = []
                issues[wl].append((os.path.basename(fp), i+1, line.strip()[:120]))
    return issues

for name, d in books.items():
    full = os.path.join(r'd:\HuaweiMoveData\Users\淡水海边\Desktop\Postgraduate\项目\MySelf\Books_Translate', d)
    if not os.path.exists(full):
        print(f'{name}: directory not found, skipping')
        continue
    result = scan_book(name, full)
    # Sort by frequency
    sorted_items = sorted(result.items(), key=lambda x: -len(x[1]))
    print(f'\n=== {name}: {len(sorted_items)} unique words embedded in Chinese prose ===')
    for word, occs in sorted_items:
        print(f'  {word} ({len(occs)}x): {occs[0][0]}:{occs[0][1]} {occs[0][2]}')
