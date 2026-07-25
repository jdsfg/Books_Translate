import re, os, glob, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

books = {
    '营养的逻辑': r'pipeline\translate\营养的逻辑\blocks',
    '压力的科学': r'pipeline\translate\压力的科学\blocks',
    '情绪的科学': r'pipeline\translate\情绪的科学：识别、调节、不被绑架\blocks',
}

# Whitelist of technical terms / proper names / acronyms that are OK in Chinese prose
whitelist = {
    'bmi','rda','rdi','ldl','hdl','gi','gl','kcal','dna','rna','who','fda','usda',
    'hpa','acth','cortisol','ace','ptsd','fmri','cbt','dbt','act','eft','apa','dsm','bps',
    'api','git','github','ci','cd','tdd','bdd','solid','dry','kiss','yagni','pr','mvp',
    'sdk','cli','ide','repl','oop','fp','frp','ddd','e2e','sut','mock','stub','spy',
    'cap','acid','base','crud','grpc','cdn','dns','ttl','lru','fifo','qps',
    'redis','kafka','docker','kubernetes','nginx',
    'gpa','gre','toefl','ielts','sat','common','mba','phd','cv','sop',
    'bold','heuristics','bias','selye','sapolsky','frankl','pronin','mercier','sperber',
    'amygdala','cortisol','prefrontal','hippocampus','norepinephrine','epinephrine',
    'glucose','insulin','leptin','ghrelin','metabolism','microbiome','probiotic',
    'carbohydrate','protein','fat','fiber','vitamin','mineral','calcium','iron',
    'cholesterol','triglyceride','lipoprotein','macronutrient','micronutrient',
    'ketogenic','glycemic','saturated','unsaturated','trans','omega',
    'placebo','random','controlled','trial','meta','cohort','epidemiological',
    'cognitive','dissonance','confirmation','motivated','reasoning','blind','spot',
    'tribal','epistemic','pre','post','mortem','commitment',
    'stochastic','deterministic','asymptotic','polynomial','exponential',
    'throughput','latency','bottleneck','scalability','replication','sharding',
    'refactoring','coverage','snapshot','property','mutation','fixture',
    'hexagonal','imperative','repository','doubles',
    'the','and','for','not','but','with','from','that','this','are','was','were',
    'have','has','had','will','would','could','should','may','might','can',
    'about','into','than','then','them','they','their','there','where','which',
    'while','when','what','who','how','why','more','most','some','any','all',
    'one','two','three','first','second','third','last','next','only','very',
    'also','just','like','such','each','both','other','same','different','new',
    'old','good','bad','big','small','high','low','long','short','fast','slow',
    'true','false','real','fake','right','wrong','yes','ok','out','off','back',
    'over','under','again','once','here','there','now','still','yet','even',
    'too','so','no','nor','not','don','isn','wasn','aren','weren','hasn','haven',
    'hadn','won','wouldn','shouldn','couldn','mightn','mustn','needn','daren',
    'let','let\'s','going','being','having','doing','saying','making','taking',
    'getting','putting','coming','going','looking','seeming','feeling','trying',
    'asking','leaving','calling','keeping','setting','finding','turning','giving',
    'showing','bringing','playing','running','moving','living','growing','holding',
    'standing','spending','falling','cutting','breaking','hitting','wearing',
    'meeting','talking','working','sitting','reading','watching','eating',
    'drinking','sleeping','waking','walking','driving','flying','riding',
    'swimming','climbing','jumping','throwing','catching','kicking','punching',
}

for book_name, blocks_dir in books.items():
    full = os.path.join(r'd:\HuaweiMoveData\Users\淡水海边\Desktop\Postgraduate\项目\MySelf\Books_Translate', blocks_dir)
    if not os.path.exists(full):
        print(f'\n=== {book_name}: directory not found ===')
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
            clean = re.sub(r'`[^`]*`', '', line)
            clean = re.sub(r'（[A-Za-z\s\-\.]+）', '', clean)
            clean = re.sub(r'\([A-Za-z\s\-\.]+\)', '', clean)
            clean = re.sub(r'https?://\S+', '', clean)
            clean = re.sub(r'<[^>]+>', '', clean)
            # Find English words (3+ letters) adjacent to Chinese characters
            matches = re.findall(r'([\u4e00-\u9fff])\s*([a-zA-Z]{3,})\s*([\u4e00-\u9fff])', clean)
            matches += re.findall(r'([a-zA-Z]{3,})\s*([\u4e00-\u9fff])', clean)
            matches += re.findall(r'([\u4e00-\u9fff])\s*([a-zA-Z]{3,})', clean)
            all_words = [(m[1] if len(m)==3 else m[0]) for m in matches] + [m[1] for m in matches]
            for w in all_words:
                wl = w.lower()
                if wl not in whitelist:
                    issues.append((os.path.basename(fp), i+1, w, line.strip()[:150]))

    print(f'\n=== {book_name}: {len(issues)} potential issues ===')
    if issues:
        seen = set()
        for fn, ln, w, ctx in issues:
            key = (fn, ln, w.lower())
            if key not in seen:
                seen.add(key)
                print(f'  {fn}:{ln} [{w}] {ctx}')
    else:
        print('  No untranslated English words found in Chinese prose.')
