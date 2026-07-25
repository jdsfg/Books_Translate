import re, os, glob, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

blocks_dir = sys.argv[1] if len(sys.argv) > 1 else r'pipeline\translate\理性之外：行为经济学\blocks'

whitelist = set()
acronyms = '''HPA SOC HRV SSRI SNRIs CAR CRH BDNF GABA PTSD CBT MBSR HIIT EPOC ACE CVD CHD CRP HDL LDL
NHS CDC DNA RNA fMRI MRI THC REM NREM UCLA WEIRD LGBT TED BMI EPA DHA ALA UPF SSB CB1 CB2 ACTH DHEA SAM
PVN SCN SES GSL USD GDP NPV CPI CEO R&D SOP MBA CFP IRA ETF ROC SEC FDA SQL API CSV JSON HTML CSS HTTP
URL PDF DOI MIT NBER APA WHO IMF OECD WTO NASA NOAA EPA FAA FTC CFPB DOL IRS FINRA SIPC FDIC OPM CBO GAO
GSE Fannie Freddie Vanguard BlackRock SPIVA Opower Oracle Utilities DFID FCDO LSHTM MPH PhD MAR
Sapolsky Frankl Selye Marmot McEwen Cannon Karasek Eisenberger Weiss Antonovsky
Kahneman Tversky Thaler Sunstein Ariely Loewenstein Prelec Simon Herbert Allais Ellsberg Markowitz
Sharpe Fama French Shiller Stiglitz Akerlof Smith Vernon Wansink Carney BITSS OSF
Achilles Priam Oedipus Antigone Medea Dante Virgil Homer Sophocles Aeschylus Euripides Kleos Mênis Mêtis
Nostos Hamartia Catharsis Terza Rima Contrapasso Inferno Purgatorio Paradiso
Stoic Stoicism Epictetus Musonius Seneca Marcus Aurelius Zeno Cleanthes Chrysippus
Memento Mori Premeditatio Malorum Dichotomy Control Prosoche Ataraxia Apatheia
'''
for a in acronyms.split():
    whitelist.add(a.lower())

# Also whitelist common short English words that might appear in markdown formatting
# or are part of valid bilingual annotations
extra_ok = {'etc', 'vs', 'cf', 'ie', 'eg', 'pp', 'ed', 'eds', 'vol', 'no', 'ch', 'fig', 'tab',
            'app', 'eq', 'n', 'p', 't', 'f', 'r', 'x', 'y', 'z', 'q', 'a', 'b', 'c', 'd', 'e',
            'ann', 'ref', 'refs', 'max', 'min', 'avg', 'std', 'var', 'pdf', 'log', 'exp', 'sin',
            'cos', 'tan', 'lim', 'inf', 'nan', 'null', 'true', 'false', 'none', 'self', 'this',
            'the', 'and', 'for', 'not', 'but', 'all', 'any', 'can', 'has', 'had', 'was', 'are',
            'been', 'have', 'does', 'will', 'would', 'could', 'should', 'may', 'might', 'must',
            'shall', 'than', 'then', 'when', 'what', 'who', 'how', 'why', 'where', 'which',
            'that', 'with', 'from', 'into', 'onto', 'upon', 'over', 'under', 'about',
            'their', 'there', 'these', 'those', 'they', 'them', 'his', 'her', 'its',
            'our', 'your', 'their', 'my', 'me', 'him', 'us',
            'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten',
            'first', 'second', 'third', 'last', 'next', 'prev', 'both', 'each', 'every',
            'some', 'many', 'much', 'more', 'most', 'less', 'few', 'fewer',
            'same', 'different', 'other', 'another', 'such', 'only', 'very', 'just',
            'also', 'too', 'so', 'as', 'at', 'by', 'if', 'or', 'on', 'up', 'out', 'off',
            'down', 'back', 'away', 'here', 'now', 'still', 'yet', 'again',
            'while', 'during', 'before', 'after', 'since', 'until', 'between', 'among',
            'through', 'throughout', 'within', 'without', 'against',
            'about', 'above', 'below', 'beside', 'beyond',
            'is', 'am', 'are', 'be', 'been', 'being', 'do', 'did', 'done', 'doing',
            'get', 'got', 'go', 'went', 'gone', 'going', 'come', 'came', 'coming',
            'make', 'made', 'making', 'take', 'took', 'taken', 'taking',
            'see', 'saw', 'seen', 'seeing', 'know', 'knew', 'known', 'knowing',
            'think', 'thought', 'thinking', 'say', 'said', 'saying',
            'find', 'found', 'finding', 'give', 'gave', 'given', 'giving',
            'tell', 'told', 'telling', 'work', 'worked', 'working',
            'look', 'looked', 'looking', 'seem', 'seemed', 'seeming',
            'feel', 'felt', 'feeling', 'try', 'tried', 'trying',
            'ask', 'asked', 'asking', 'put', 'putting', 'let', 'letting',
            'call', 'called', 'calling', 'use', 'used', 'using',
            'want', 'wanted', 'wanting', 'need', 'needed', 'needing',
            'show', 'showed', 'shown', 'showing', 'keep', 'kept', 'keeping',
            'begin', 'began', 'begun', 'beginning', 'start', 'started', 'starting',
            'end', 'ended', 'ending', 'stop', 'stopped', 'stopping',
            'help', 'helped', 'helping', 'turn', 'turned', 'turning',
            'play', 'played', 'playing', 'run', 'ran', 'running',
            'move', 'moved', 'moving', 'live', 'lived', 'living',
            'believe', 'believed', 'believing', 'happen', 'happened', 'happening',
            'write', 'wrote', 'written', 'writing', 'sit', 'sat', 'sitting',
            'stand', 'stood', 'standing', 'lose', 'lost', 'losing',
            'pay', 'paid', 'paying', 'meet', 'met', 'meeting',
            'include', 'included', 'including', 'continue', 'continued', 'continuing',
            'set', 'setting', 'learn', 'learned', 'learning',
            'change', 'changed', 'changing', 'lead', 'led', 'leading',
            'understand', 'understood', 'understanding', 'watch', 'watched', 'watching',
            'follow', 'followed', 'following', 'stop', 'stopped', 'stopping',
            'create', 'created', 'creating', 'speak', 'spoke', 'spoken', 'speaking',
            'read', 'reading', 'allow', 'allowed', 'allowing',
            'spend', 'spent', 'spending', 'grow', 'grew', 'grown', 'growing',
            'open', 'opened', 'opening', 'walk', 'walked', 'walking',
            'win', 'won', 'winning', 'offer', 'offered', 'offering',
            'remember', 'remembered', 'remembering', 'love', 'loved', 'loving',
            'consider', 'considered', 'considering', 'appear', 'appeared', 'appearing',
            'buy', 'bought', 'buying', 'wait', 'waited', 'waiting',
            'serve', 'served', 'serving', 'die', 'died', 'dying',
            'send', 'sent', 'sending', 'expect', 'expected', 'expecting',
            'build', 'built', 'building', 'stay', 'stayed', 'staying',
            'fall', 'fell', 'fallen', 'falling', 'cut', 'cutting',
            'reach', 'reached', 'reaching', 'kill', 'killed', 'killing',
            'remain', 'remained', 'remaining', 'suggest', 'suggested', 'suggesting',
            'raise', 'raised', 'raising', 'pass', 'passed', 'passing',
            'sell', 'sold', 'selling', 'require', 'required', 'requiring',
            'report', 'reported', 'reporting', 'decide', 'decided', 'deciding',
            'point', 'pointed', 'pointing',
            'case', 'cases', 'group', 'groups', 'year', 'years', 'time', 'times',
            'day', 'days', 'week', 'weeks', 'month', 'months',
            'people', 'person', 'women', 'men', 'children', 'child',
            'world', 'life', 'way', 'ways', 'part', 'parts',
            'place', 'places', 'area', 'areas', 'city', 'cities',
            'fact', 'facts', 'case', 'cases', 'study', 'studies',
            'data', 'result', 'results', 'effect', 'effects',
            'model', 'models', 'theory', 'theories', 'method', 'methods',
            'rate', 'rates', 'risk', 'risks', 'cost', 'costs',
            'value', 'values', 'price', 'prices', 'income', 'incomes',
            'market', 'markets', 'fund', 'funds', 'stock', 'stocks',
            'asset', 'assets', 'bond', 'bonds', 'debt', 'debts',
            'loan', 'loans', 'bank', 'banks', 'cash',
            'plan', 'plans', 'goal', 'goals', 'target', 'targets',
            'rule', 'rules', 'law', 'laws', 'policy', 'policies',
            'test', 'tests', 'trial', 'trials', 'score', 'scores',
            'task', 'tasks', 'item', 'items', 'list', 'lists',
            'line', 'lines', 'page', 'pages', 'book', 'books',
            'word', 'words', 'term', 'terms', 'name', 'names',
            'side', 'sides', 'type', 'types', 'form', 'forms',
            'level', 'levels', 'stage', 'stages', 'step', 'steps',
            'phase', 'phases', 'state', 'states', 'process', 'processes',
            'system', 'systems', 'program', 'programs',
            'control', 'controls', 'treatment', 'treatments',
            'sample', 'samples', 'subject', 'subjects', 'participant', 'participants',
            'patient', 'patients', 'client', 'clients', 'user', 'users',
            'benefit', 'benefits', 'cost', 'costs', 'gain', 'gains',
            'loss', 'losses', 'return', 'returns', 'yield', 'yields',
            'profit', 'profits', 'revenue', 'revenues',
            'percent', 'percentage', 'proportion', 'ratio',
            'average', 'median', 'mean', 'standard', 'deviation',
            'correlation', 'regression', 'coefficient', 'variance',
            'significance', 'significant', 'confidence', 'interval',
            'hypothesis', 'null', 'alternative',
            'bias', 'biases', 'error', 'errors',
            'utility', 'preference', 'preferences', 'choice', 'choices',
            'decision', 'decisions', 'option', 'options',
            'incentive', 'incentives', 'nudge', 'nudges',
            'frame', 'framing', 'anchor', 'anchoring',
            'heuristic', 'heuristics', 'intuition', 'intuitive',
            'rational', 'rationality', 'irrational', 'irrationality',
            'behavior', 'behavioral', 'behaviour', 'behavioural',
            'cognitive', 'emotion', 'emotional', 'emotions',
            'social', 'economic', 'economics', 'psychology', 'psychological',
            'financial', 'finance', 'money', 'monetary',
            'individual', 'individuals', 'collective',
            'public', 'private', 'personal',
            'general', 'specific', 'particular',
            'positive', 'negative', 'neutral',
            'active', 'passive',
            'short', 'long', 'medium',
            'high', 'low', 'middle',
            'large', 'small', 'big', 'little',
            'old', 'new', 'young',
            'good', 'bad', 'better', 'best', 'worse', 'worst',
            'right', 'wrong', 'correct', 'incorrect',
            'true', 'false', 'real', 'unreal',
            'important', 'unimportant', 'relevant', 'irrelevant',
            'possible', 'impossible', 'probable', 'improbable',
            'likely', 'unlikely', 'certain', 'uncertain',
            'expected', 'unexpected', 'surprising', 'unsurprising',
            'common', 'rare', 'frequent', 'infrequent',
            'simple', 'complex', 'complicated',
            'easy', 'difficult', 'hard', 'soft',
            'strong', 'weak',
            'fast', 'slow', 'quick', 'rapid',
            'early', 'late', 'prior', 'posterior',
            'past', 'present', 'future',
            'current', 'previous', 'next',
            'initial', 'final', 'intermediate',
            'direct', 'indirect',
            'explicit', 'implicit',
            'conscious', 'unconscious',
            'internal', 'external',
            'objective', 'subjective',
            'absolute', 'relative',
            'fixed', 'variable',
            'static', 'dynamic',
            'linear', 'nonlinear',
            'local', 'global',
            'single', 'multiple', 'double', 'triple',
            'total', 'partial',
            'full', 'empty',
            'open', 'closed',
            'free', 'paid',
            'safe', 'risky',
            'fair', 'unfair',
            'normal', 'abnormal',
            'healthy', 'unhealthy',
            'natural', 'artificial',
            'physical', 'mental',
            'male', 'female',
            'adult', 'child',
            'urban', 'rural',
            'developed', 'developing',
            'rich', 'poor',
            'advantage', 'disadvantage',
            'increase', 'decrease',
            'improve', 'worsen',
            'maximize', 'minimize',
            'overestimate', 'underestimate',
            'overweight', 'underweight',
            'gain', 'loss',
            'reward', 'punishment',
            'success', 'failure',
            'winner', 'loser',
            'buyer', 'seller',
            'leader', 'follower',
            'teacher', 'student',
            'doctor', 'patient',
            'employer', 'employee',
            'manager', 'worker',
            'producer', 'consumer',
            'investor', 'investment',
            'saver', 'saving', 'savings',
            'spender', 'spending',
            'borrower', 'lender', 'borrowing', 'lending',
            'insurer', 'insured', 'insurance',
            'advisor', 'adviser', 'advice',
            'planner', 'planning',
            'retirement', 'retiree',
            'salary', 'wage', 'income',
            'expense', 'expenses', 'spending',
            'budget', 'budgeting',
            'tax', 'taxes', 'taxable',
            'deduction', 'deductions',
            'credit', 'credits',
            'exemption', 'exemptions',
            'mortgage', 'rent',
            'property', 'real', 'estate',
            'portfolio', 'diversification', 'rebalancing',
            'allocation', 'allocation',
            'equity', 'equities',
            'fixed', 'income',
            'index', 'indices',
            'benchmark', 'benchmarks',
            'expense', 'ratio',
            'management', 'fee', 'fees',
            'commission', 'commissions',
            'load', 'no-load',
            'active', 'passive',
            'factor', 'factors',
            'momentum', 'value', 'growth',
            'size', 'quality',
            'volatility', 'beta', 'alpha',
            'sharpe', 'ratio',
            'drawdown', 'drawdowns',
            'compounding', 'compound',
            'inflation', 'deflation',
            'recession', 'depression',
            'bubble', 'bubbles',
            'crash', 'crashes',
            'bull', 'bear',
            'sentiment', 'optimism', 'pessimism',
            'overconfidence', 'herding',
            'disposition', 'effect',
            'endowment', 'effect',
            'status', 'quo', 'bias',
            'sunk', 'cost',
            'opportunity', 'cost',
            'mental', 'accounting',
            'framing', 'effect',
            'anchoring', 'effect',
            'availability', 'heuristic',
            'representativeness', 'heuristic',
            'affect', 'heuristic',
            'loss', 'aversion',
            'risk', 'aversion',
            'risk', 'seeking',
            'ambiguity', 'aversion',
            'present', 'bias',
            'time', 'discounting',
            'hyperbolic', 'discounting',
            'self', 'control',
            'ego', 'depletion',
            'willpower',
            'default', 'defaults',
            'opt-out', 'opt-in',
            'choice', 'architecture',
            'libertarian', 'paternalism',
            'asymmetric', 'paternalism',
            'nudge', 'nudges',
            'boost', 'boosts',
            'choice', 'overload',
            'paradox',
            'anomaly', 'anomalies',
            'efficient', 'market',
            'hypothesis',
            'random', 'walk',
            'prospect', 'theory',
            'expected', 'utility',
            'bounded', 'rationality',
            'satisficing',
            'heuristics',
            'dual', 'process',
            'system',
            'fast', 'slow',
            'thinking',
            '''
for w in extra_ok.split():
    whitelist.add(w.lower())

files = sorted(glob.glob(os.path.join(blocks_dir, '*.md')))
found = {}
for fp in files:
    with open(fp, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    in_code = False
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith('```'):
            in_code = not in_code
            continue
        if in_code:
            continue
        
        # Remove inline code
        line = re.sub(r'`[^`]*`', '', line)
        # Remove URLs
        line = re.sub(r'https?://\S+', '', line)
        # Remove parenthetical content (中文（English）or (English))
        line = re.sub(r'[（(][^)）]*[)）]', '', line)
        # Remove HTML tags
        line = re.sub(r'<[^>]+>', '', line)
        # Remove italic/bold markers but keep content
        line = re.sub(r'\*+', '', line)
        line = re.sub(r'_+', '', line)
        
        # Find English words
        words = re.findall(r'[a-zA-Z]{4,}', line)
        for w in words:
            wl = w.lower()
            if wl not in whitelist and not wl.isdigit():
                key = wl
                if key not in found:
                    found[key] = []
                found[key].append(f'{os.path.basename(fp)}:{i}')

print(f'Found {len(found)} unique words (4+ chars)')
for word in sorted(found.keys()):
    occurrences = found[word]
    print(f'{word} ({len(occurrences)}x): {occurrences[:8]}')
