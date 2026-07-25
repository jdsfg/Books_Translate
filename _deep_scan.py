import re, os, glob, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

blocks_dir = r'pipeline\translate\理性之外：行为经济学\blocks'

# Comprehensive whitelist of acceptable English terms
whitelist = set()
# Acronyms/abbreviations
acronyms = ['HPA','SOC','HRV','SSRI','SSRIs','SNRIs','CAR','CRH','BDNF','GABA','PTSD','CBT','MBSR','HIIT','MICT','EMDR','ACE','CVD','CHD','CRP','HDL','LDL','NHS','CDC','IARC','DNA','RNA','fMRI','MRI','THC','REM','NREM','IBS','ANDA','UCLA','WEIRD','LGBT','TED','HOME','APP','BMI','EPA','DHA','ALA','UPF','SSB','EPOC','CB1','CB2','ACTH','DHEA','SAM','PVN','SCN','SES','GSL']
for a in acronyms:
    whitelist.add(a.lower())

# Names (proper nouns)
names_text = """sapolsky frankl selye marmot mcewen cannon karasek eisenberger weiss antonovsky
felitti lunstad holt robert bruce hans michael marshall warren barry robin victor aaron george
elisabeth ross paul daniel joseph lisa barbara nicholas alan harris friedman marcia losada dacher
keltner bren brown david buss carol tavris brad bushman todd kashdan james gross matthew lieberman
wegner william frey maria gendron ekman maclean allport tomkins arnold moreau lindquist wager kober
bliss sokal wagenmakers christakis fowler hatfield jamieson crum kross emmons lewis inbar cacioppo
bonanno damasio ledoux siegel kahneman gawande sacks tangney rozin mayo whitehall mcgill kaiser
permanente maya andrea rimonabant anandamide ananda adrenaline epinephrine cortisol corticotropin
endocrinologist allostatic suprachiasmatic neocortex triune broaden build framework fight flight
freeze fawn reappraisal self distancing body state labeling affect accumbens amygdala hippocampus
prefrontal cortex medial striatum anglo saxon helicobacter pylori socratopia library stress eustress
strain allostasis homeostasis perceived control decision latitude demand control support
vagal tone parasympathetic sympathetic nervous system hpa axis crh acth cortisol adrenaline
noradrenaline norepinephrine dopamine serotonin glutamate endorphin endocannabinoid cannabinoid
cb1 cb2 receptor antagonist agonist inflammation interleukin cytokine crp fibrinogen
cholesterol ldl hdl triglyceride blood pressure hypertension atherosclerosis
metabolic syndrome insulin resistance glucose tolerance diabetes type
cardiovascular morbidity mortality epidemiology longitudinal cross-sectional
randomized controlled trial rct meta-analysis systematic review
effect size confidence interval statistical significance p-value
correlation causation confounder covariate adjustment regression
hierarchical multiple regression odds ratio hazard ratio relative risk
incidence prevalence etiology pathophysiology mechanism pathway
acute chronic stressor stress response adaptation allostasis load overload
wear and tear weathering cumulative cost
sleep architecture rem nrem slow wave deep sleep circadian rhythm
melatonin cortisol awakening response car
exercise aerobic resistance high intensity interval training hiit mict
moderate intensity continuous training
mindfulness meditation mbsr mbct mindful based stress reduction
cognitive behavioral therapy cbt acceptance commitment act
dialectical behavior dbt
eye movement desensitization reprocessing emdr
polyvagal theory vagal tone heart rate variability hrv
social support buffering hypothesis direct indirect effects
perceived control mastery decision latitude job strain
effort reward imbalance eri demand control support model
sense of coherence soc coherence comprehensibility manageability meaningfulness
meaning purpose logotherapy viktor frankl existential
attachment theory secure anxious avoidant disorganized
adverse childhood experiences ace study kaiser permanente cdc
felitti anda childhood trauma questionnaire
social determinants health sdoh structural
individual intervention structural intervention
population level public health prevention treatment
diary assessment self-monitoring ecological momentary
qualitative quantitative mixed methods
biological marker biomarker physiological measure
salivary cortisol hair cortisol glucocorticoid
hpa axis functioning dysregulation hyper hypo
amygdala prefrontal cortex hippocampus
top-down bottom-up regulation inhibition excitation
neuroplasticity neurogenesis synaptogenesis pruning
bdnf brain derived neurotrophic factor
inflammation immune system pro-inflammatory anti-inflammatory
autoimmune disease rheumatoid arthritis lupus
gastrointestinal ibs ulcer helicobacter pylori
cardiovascular disease coronary heart disease chd stroke
metabolic syndrome obesity diabetes insulin resistance
cancer tumor oncology iarc classification carcinogen
sleep disorder insomnia apnea
mental health depression anxiety ptsd burnout
pharmacotherapy ssri snri benzodiazepine
psychotherapy cbt act dbt mbsr emdr
lifestyle intervention exercise diet sleep stress management
social connection loneliness isolation social support
meaning purpose coherence control
childhood adversity trauma resilience vulnerability
structural poverty inequality discrimination
workplace job strain effort reward control autonomy
public health prevention policy intervention"""
for n in names_text.split():
    whitelist.add(n.lower())

found = {}
files = sorted(glob.glob(os.path.join(blocks_dir, '*.md')))
for fp in files:
    with open(fp, 'r', encoding='utf-8') as f:
        text = f.read()
    # Remove code blocks
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    # Remove inline code
    text = re.sub(r'`[^`]+`', '', text)
    # Remove URLs
    text = re.sub(r'https?://\S+', '', text)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove parenthetical English
    text = re.sub(r'（[^）]*[A-Za-z][^）]*）', '', text)
    text = re.sub(r'\([^\)]*[A-Za-z][^\)]*\)', '', text)
    # Remove italic/bold markers
    text = re.sub(r'\*+', '', text)
    text = re.sub(r'_+', '', text)
    
    lines = text.split('\n')
    for i, line in enumerate(lines):
        # Find English words embedded in Chinese prose
        # Pattern: Chinese char followed by English word followed by Chinese char
        matches = re.findall(r'[\u4e00-\u9fff]([a-zA-Z]{2,})[\u4e00-\u9fff]', line)
        matches += re.findall(r'[\u4e00-\u9fff]([a-zA-Z]{2,})\s', line)
        matches += re.findall(r'\s([a-zA-Z]{2,})[\u4e00-\u9fff]', line)
        for m in matches:
            w = m.lower()
            if w not in whitelist and len(w) > 2:
                if w not in found:
                    found[w] = []
                found[w].append(f'{os.path.basename(fp)}:{i+1}')

for w in sorted(found.keys()):
    locs = found[w]
    print(f'{w} ({len(locs)}x): {locs[:5]}')
