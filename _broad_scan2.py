import re, os, glob, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

blocks_dir = sys.argv[1] if len(sys.argv) > 1 else r'pipeline\translate\理性之外：行为经济学\blocks'

# Whitelist: acronyms, proper names, technical terms
wl = set()
for a in """HPA SOC HRV SSRI SNRIs CAR CRH BDNF GABA PTSD CBT MBSR HIIT EPOC ACE CVD CHD CRP HDL LDL
NHS CDC DNA RNA fMRI MRI THC REM NREM UCLA WEIRD LGBT TED BMI EPA DHA ALA UPF SSB CB1 CB2 ACTH DHEA SAM
PVN SCN SES GSL USD GDP NPV CPI CEO R&D SOP MBA CFP IRA ETF ROC SEC FDA SQL API CSV JSON HTML CSS HTTP
URL PDF DOI MIT NBER APA WHO IMF OECD WTO NASA NOAA FAA FTC CFPB DOL IRS FINRA SIPC FDIC OPM CBO GAO
GSE Fannie Freddie Vanguard BlackRock SPIVA Opower Oracle Utilities DFID FCDO LSHTM MPH PhD MAR
Sapolsky Frankl Selye Marmot McEwen Cannon Karasek Eisenberger Weiss Antonovsky
Kahneman Tversky Thaler Sunstein Ariely Loewenstein Prelec Simon Herbert Allais Ellsberg Markowitz
Sharpe Fama French Shiller Stiglitz Akerlof Smith Vernon Wansink Carney BITSS OSF
Achilles Priam Oedipus Antigone Medea Dante Virgil Homer Sophocles Aeschylus Euripides Kleos
Nostos Hamartia Catharsis Contrapasso Inferno Purgatorio Paradiso
Stoic Stoicism Epictetus Musonius Seneca Marcus Aurelius Zeno Cleanthes Chrysippus
Premeditatio Ataraxia Apatheia Prosoche""".split():
    wl.add(a.lower())

files = sorted(glob.glob(os.path.join(blocks_dir, '*.md')))
found = {}
for fp in files:
    with open(fp, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    in_code = False
    for i, line in enumerate(lines, 1):
        s = line.strip()
        if s.startswith('```'):
            in_code = not in_code
            continue
        if in_code:
            continue
        # Remove inline code, URLs, parenthetical, HTML, emphasis
        line2 = re.sub(r'`[^`]*`', '', line)
        line2 = re.sub(r'https?://\S+', '', line2)
        line2 = re.sub(r'[（(][^)）]*[)）]', '', line2)
        line2 = re.sub(r'<[^>]+>', '', line2)
        line2 = re.sub(r'\*+', '', line2)
        line2 = re.sub(r'_+', '', line2)
        # Find English words 4+ chars
        for w in re.findall(r'[a-zA-Z]{4,}', line2):
            wlow = w.lower()
            if wlow not in wl and not wlow.isdigit():
                if wlow not in found:
                    found[wlow] = []
                found[wlow].append(os.path.basename(fp) + ':' + str(i))

print(f'Found {len(found)} unique words (4+ chars)')
for word in sorted(found.keys()):
    occ = found[word]
    print(f'{word} ({len(occ)}x): {occ[:8]}')
