import re, os, glob, sys
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

books = {
    '营养的逻辑': r'pipeline\translate\营养的逻辑\blocks',
    '压力的科学': r'pipeline\translate\压力的科学\blocks',
    '情绪的科学': r'pipeline\translate\情绪的科学：识别、调节、不被绑架\blocks',
}

# Technical terms / acronyms OK to keep in English
whitelist = {
    'bmi','rda','rdi','ldl','hdl','gi','gl','kcal','dna','rna','who','fda','usda',
    'hpa','acth','ace','ptsd','fmri','cbt','dbt','act','eft','apa','dsm','bps',
    'api','git','github','tdd','bdd','solid','dry','kiss','yagni','mvp',
    'sdk','cli','ide','repl','oop','fp','frp','ddd','e2e','sut',
    'cap','acid','base','crud','grpc','cdn','dns','ttl','lru','fifo','qps',
    'gpa','gre','toefl','ielts','sat','mba','phd','cv','sop',
    'bold','rct','rcts','scfa','glp','predimed',
    'omega','ldls','hdls',
    'socratopia',
}

for book_name, blocks_dir in books.items():
    full = os.path.join(r'd:\HuaweiMoveData\Users\淡水海边\Desktop\Postgraduate\项目\MySelf\Books_Translate', blocks_dir)
    if not os.path.exists(full):
        print(f'\n=== {book_name}: directory not found, skipping ===')
        continue
    files = sorted(glob.glob(os.path.join(full, '*.md')))
    issues = []
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
            # Remove parenthetical English
            clean = re.sub(r'（[A-Za-z\s\-\.]+）', '', clean)
            clean = re.sub(r'\([A-Za-z\s\-\.]+\)', '', clean)
            # Remove URLs
            clean = re.sub(r'https?://\S+', '', clean)
            # Remove HTML tags
            clean = re.sub(r'<[^>]+>', '', clean)
            # Find English words (3+ letters) adjacent to Chinese
            m1 = re.findall(r'([\u4e00-\u9fff])\s*([a-zA-Z]{3,})\s*([\u4e00-\u9fff])', clean)
            m2 = re.findall(r'([a-zA-Z]{3,})\s*([\u4e00-\u9fff])', clean)
            m3 = re.findall(r'([\u4e00-\u9fff])\s*([a-zA-Z]{3,})', clean)
            all_words = [(m[1] if len(m)==3 else m[0]) for m in m1] + [m[0] for m in m2] + [m[1] for m in m3]
            for w in all_words:
                wl = w.lower()
                if wl not in whitelist:
                    issues.append((os.path.basename(fp), i+1, w, line.strip()[:120]))

    word_counts = Counter(w.lower() for _,_,w,_ in issues)
    print(f'\n=== {book_name}: {len(word_counts)} unique words, {len(issues)} total occurrences ===')
    for w, c in word_counts.most_common(60):
        locs = [(fn,ln) for fn,ln,wd,_ in issues if wd.lower()==w]
        sample = next(ctx for fn,ln,wd,ctx in issues if wd.lower()==w)
        print(f'  {w} ({c}x) first@{locs[0][0]}:{locs[0][1]} | {sample[:100]}')
