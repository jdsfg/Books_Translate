import subprocess, re, collections

cwd = r'd:\HuaweiMoveData\Users\淡水海边\Desktop\Postgraduate\项目\MySelf\Books_Translate'

books = [
    ('origin/translate/relationships-science', '看见彼此——亲密关系的科学', '_issues_relationships.txt'),
    ('origin/translate/system-design', '系统设计思维：大规模软件的架构之道', '_issues_systemdesign.txt'),
    ('origin/translate/distributed-systems', '分布式系统', '_issues_distributed.txt'),
    ('origin/translate/training-science-2', '训练的科学·卷二：耐力与整体表现', '_issues_training2.txt'),
]

# Common OK: people names, tech acronyms, product names that appear across books
common_ok = {
    'app', 'apps', 'kpi', 'kpis', 'ui', 'ux', 'api', 'rss', 'pdf', 'url',
    'ceo', 'cfo', 'coo', 'cto', 'hr', 'adhd', 'fmri', 'bpm',
    'instagram', 'facebook', 'twitter', 'tiktok', 'whatsapp', 'snapchat',
    'youtube', 'google', 'apple', 'android', 'ios', 'chrome', 'safari', 'firefox',
    'redis', 'postgresql', 'postgres', 'mongodb', 'cassandra', 'cockroachdb',
    'spanner', 'kafka', 'docker', 'kubernetes', 'grpc', 'protobuf', 'json', 'xml', 'yaml',
    'cap', 'acid', 'base', 'slo', 'sli', 'sla', 'ttl', 'jwt', 'cdn', 'dns',
    'raft', 'paxos', 'bft', 'crdt', 'hlc', 'lww', 'mvcc', 'lsm',
    'ntp', 'utc', 'gps', 'sql', 'tcp', 'udp', 'http', 'https', 'rpc',
    'vllm', 'newsql', 'oltp', 'olap', 'truetime',
    'the', 'and', 'for', 'with', 'from', 'that', 'this', 'are', 'was', 'were',
    'has', 'had', 'have', 'not', 'but', 'all', 'can', 'will', 'one', 'two',
    'zone', 'kcal', 'met', 'epoc', 'atp', 'hrmax', 'hrr', 'vo',
    'sat', 'act', 'gre', 'cps', 'acs',
    'gdp', 'gni', 'isei', 'oecd', 'nber',
    'pew', 'gallup', 'norc', 'gss', 'psid', 'nlsy', 'nces',
    'naep', 'pisa', 'timss',
    'cdc', 'fda', 'nih', 'irs', 'cbo',
    'ncaa', 'mlb', 'nba', 'nfl',
    'ppr', 'eft',
}

for branch, book, outfile in books:
    blocks_path = f'pipeline/translate/{book}/blocks/'
    r = subprocess.run(
        ['git', '-c', 'core.quotepath=false', 'ls-tree', '--name-only', f'{branch}:{blocks_path}'],
        capture_output=True, cwd=cwd
    )
    files = [f.strip() for f in r.stdout.decode('utf-8').splitlines() if f.strip().endswith('.md')]
    
    all_issues = {}
    for fname in files:
        full_path = f'{branch}:{blocks_path}{fname}'
        r2 = subprocess.run(
            ['git', '-c', 'core.quotepath=false', 'show', full_path],
            capture_output=True, cwd=cwd
        )
        text = r2.stdout.decode('utf-8', 'replace')
        
        clean = text
        clean = re.sub(r'```[^`]*```', '', clean, flags=re.DOTALL)
        clean = re.sub(r'`[^`]*`', '', clean)
        clean = re.sub(r'^>.*$', '', clean, flags=re.MULTILINE)
        clean = re.sub(r'https?://\S+', '', clean)
        clean = re.sub(r'（[^）]*）', '', clean)
        clean = re.sub(r'\([^)]*\)', '', clean)
        clean = re.sub(r'\*+', '', clean)
        clean = re.sub(r'^[a-zA-Z\s,.!?;:\-\'"()]+$', '', clean, flags=re.MULTILINE)
        
        words = re.findall(r'[a-zA-Z]{3,}', clean)
        real_issues = [w for w in words if w.lower() not in common_ok]
        
        if real_issues:
            for w in sorted(set(real_issues)):
                wl = w.lower()
                if wl not in all_issues:
                    all_issues[wl] = []
                for m in re.finditer(r'\b' + re.escape(w) + r'\b', text, re.IGNORECASE):
                    start = max(0, m.start()-60)
                    end = min(len(text), m.end()+60)
                    ctx = text[start:end].replace('\n', ' ').strip()
                    before = text[max(0,m.start()-5):m.start()]
                    if '（' in before or '(' in before:
                        continue
                    all_issues[wl].append((fname, ctx))
    
    with open(outfile, 'w', encoding='utf-8') as f:
        f.write(f'{book} — 全量残留英文词扫描\n')
        f.write(f'总块数: {len(files)}\n')
        f.write(f'独立词: {len(all_issues)}\n')
        f.write(f'总出现: {sum(len(v) for v in all_issues.values())}\n\n')
        for w in sorted(all_issues.keys(), key=lambda x: -len(all_issues[x])):
            contexts = all_issues[w]
            f.write(f'=== {w} ({len(contexts)} occurrences) ===\n')
            for fname, ctx in contexts:
                f.write(f'  {fname}: ...{ctx}...\n')
            f.write('\n')
    
    print(f'{book}: {len(all_issues)} words, {sum(len(v) for v in all_issues.values())} occurrences → {outfile}')
