import re, os, glob, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

blocks_dir = r'pipeline\translate\古老的认知疗法——斯多葛主义的现代诠释\blocks'

# Comprehensive whitelist of acceptable English terms
whitelist = set()
# Acronyms/abbreviations
acronyms = ['HPA','SOC','HRV','SSRI','SSRIs','SNRIs','CAR','CRH','BDNF','GABA','PTSD','CBT','MBSR','HIIT','MICT','EMDR','ACE','CVD','CHD','CRP','HDL','LDL','NHS','CDC','IARC','DNA','RNA','fMRI','MRI','THC','REM','NREM','IBS','ANDA','UCLA','WEIRD','LGBT','TED','HOME','APP','BMI','EPA','DHA','ALA','UPF','SSB','EPOC','CB1','CB2','ACTH','DHEA','SAM','PVN','SCN','SES','GSL','CPAP','EEG','EMG','EOG','ECG','OSA','UARS','PLMS','RLS','DLMO','PER','CRY','BMAL','CLOCK','VIP','orexin','melatonin','adenosine','cortisol','leptin','ghrelin','insulin','glucose','APOE','TNF','IL-6','IL-1','CRP','PSQI','ESS','AASM','CBT-I','CBD','THC','NREM','REM','SWS','WASO','TST','SOL','SE','AHI','ODI','SpO2','pH','CO2','O2','NAD','NADH','FAD','FADH2','ATP','ADP','AMP','cAMP','GTP','GDP','GMP','mRNA','tRNA','rRNA','siRNA','miRNA','piRNA','lncRNA','snoRNA','snRNA','circRNA','PCR','RT-PCR','qPCR','ELISA','RIA','HPLC','GC-MS','LC-MS','NMR','ESR','EPR','UV','IR','CD','MS','MS-MS','FRET','BRET','Y2H','Co-IP','ChIP','ChIP-seq','RNA-seq','WGS','WES','GWAS','SNP','CNV','SV','INDEL','MHC','HLA','TCR','BCR','Ig','CD','IL','IFN','TNF','TGF','EGF','FGF','PDGF','VEGF','IGF','HGF','NGF','BDNF','GDNF','NT-3','NT-4','CNTF','LIF','IL-6','IL-11','IL-31','IL-17','IL-23','IL-12','IL-4','IL-5','IL-13','IL-9','IL-10','TGF-beta','IFN-alpha','IFN-beta','IFN-gamma','TNF-alpha','LT-alpha','LT-beta','BAFF','APRIL','RANKL','RANK','OPG','TRAIL','FasL','Fas','CD40L','CD40','OX40L','OX40','ICOSL','ICOS','PD-L1','PD-1','CTLA-4','LAG-3','TIM-3','TIGIT','VISTA','B7-H3','B7-H4','IDO','TDO','LAG','TIM','TIGIT','VISTA','USD','GDP','NPV','CPI','CEO','R&D','SOP','MBA','CFP','IRA','ETF','ROC','SEC','FDA','SQL','API','CSV','JSON','HTML','CSS','HTTP','URL','PDF','DOI','MIT','NBER','APA','WHO','IMF','OECD','WTO','NASA','NOAA','EPA','FAA','FTC','CFPB','DOL','IRS','FINRA','SIPC','FDIC','OPM','CBO','GAO','GSE','DFID','FCDO','LSHTM','MPH','PhD','MAR','ipRGC','MSLT','PLMD','SNRI','BORB','ADHD','REBT','DBT','ACT']
for a in acronyms:
    whitelist.add(a.lower())

# Names (proper nouns)
names_text = """sapolsky frankl selye marmot mcewen cannon karasek eisenberger weiss antonovsky
walker matthew cartwright dement kleitman aserinsky rechtshaffen siegel hobson mccarley
epictetus musonius seneca marcus aurelius zeno cleanthes chrysippus
aristo herillus persaeus sphaerus aristocles panaetius posidonius
cato cicero plutarch gellius aulus gellius
aurelius commodus verus antoninus pius
diogenes laertius stobaeus athenaeus galen
raphael socrates plato aristotle epicurus pyrrho
cognitive behavioral therapy
kahneman tversky thaler sunstein ariely loewenstein prelec simon herbert allais ellsberg markowitz
sharpe fama french shiller stiglitz akerlof smith vernon wansink carney bitss osf
beck ellis burns barlow linehan hayes
wilson james maultsby leahy
hadot long seddon stephens irvine becker
nussbaum graver cooper procopé engberg-pedersen
sellars gill bastianini long
brunt inwood brennan frede
"""
for n in names_text.split():
    whitelist.add(n.lower())

# Latin/Greek philosophical terms
philosophical = """stoic stoicism epictetus musonius seneca marcus aurelius zeno cleanthes chrysippus
premeditatio malorum memento mori ataraxia apatheia prosoche dichotomy
virtue arete eudaimonia logos pneuma katalēpsis sympatheia
oikeiosis prohairesis hypolēpsis phantasia kathekon kathēkon
apatheia ataraxia prosochē prosoche melete thanatou
theorein praktikos physike logos prosochesthai
mênis mêtis kleos nostos hamartia catharsis peripeteia anagnorisis
contrapasso terza rima inferno purgatorio paradiso
homo economicus
prokopton prosochē
phantasiai synkatathesis
hormē aphormē
telos skopos
katorthoma kathēkon
adiaphora proēgmena apoproēgmena
arete physis logos
oikeiosis allotriosis
pathos eupatheiai
doxa epistēmē
aisthēsis noēsis
sophia phronēsis
enkrateia akrasia
"""
for p in philosophical.split():
    whitelist.add(p.lower())

# Common English words that should NOT appear in Chinese prose
# (4+ chars) - these are NOT whitelisted and will be flagged
# Short words and connectors
connectors = """that with from into onto upon over under about
their there these those they them his her its
our your their my me him us
some many much more most less few fewer
same different other another such only very just
also too when what who how why where which
than then once while during before after since until between among
through throughout within without against
above below beside beyond
been being have does will would could should
may might must shall
this that these those
have has had was were are
been being doing
make made making take took taken taking
see saw seen seeing know knew known knowing
think thought thinking say said saying
find found finding give gave given giving
tell told telling work worked working
look looked looking seem seemed seeming
feel felt feeling try tried trying
ask asked asking put letting
call called calling use used using
want wanted wanting need needed needing
show showed shown showing keep kept keeping
begin began begun beginning start started starting
end ended ending stop stopped stopping
help helped helping turn turned turning
play played playing run ran running
move moved moving live lived living
believe believed believing happen happened happening
write wrote written writing sit sat sitting
stand stood standing lose lost losing
pay paid paying meet met meeting
include included including continue continued continuing
set setting learn learned learning
change changed changing lead led leading
understand understood understanding watch watched watching
follow followed following stop stopped stopping
create created creating speak spoke spoken speaking
read reading allow allowed allowing
spend spent spending grow grew grown growing
open opened opening walk walked walking
win won winning offer offered offering
remember remembered remembering love loved loving
consider considered considering appear appeared appearing
buy bought buying wait waited waiting
serve served serving die died dying
send sent sending expect expected expecting
build built building stay stayed staying
fall fell fallen falling cut cutting
reach reached reaching kill killed killing
remain remained remaining suggest suggested suggesting
raise raised raising pass passed passing
sell sold selling require required requiring
report reported reporting decide decided deciding
point pointed pointing
case cases group groups year years time times
day days week weeks month months
people person women men children child
world life way ways part parts
place places area areas city cities
fact facts study studies
data result results effect effects
model models theory theories method methods
rate rates risk risks cost costs
value values price prices income incomes
market markets fund funds stock stocks
asset assets bond bonds debt debts
loan loans bank banks cash
plan plans goal goals target targets
rule rules law laws policy policies
test tests trial trials score scores
task tasks item items list lists
line lines page pages book books
word words term terms name names
side sides type types form forms
level levels stage stages step steps
phase phases state states process processes
system systems program programs
control controls treatment treatments
sample samples subject subjects participant participants
patient patients client clients user users
benefit benefits gain gains
loss losses return returns yield yields
profit profits revenue revenues
percent percentage proportion ratio
average median mean standard deviation
correlation regression coefficient variance
significance significant confidence interval
hypothesis null alternative
bias biases error errors
utility preference preferences choice choices
decision decisions option options
incentive incentives nudge nudges
frame framing anchor anchoring
heuristic heuristics intuition intuitive
rational rationality irrational irrationality
behavior behavioral behaviour behavioural
cognitive emotion emotional emotions
social economic economics psychology psychological
financial finance money monetary
individual individuals collective
public private personal
general specific particular
positive negative neutral
active passive
short long medium
high low middle
large small big little
old new young
good bad better best worse worst
right wrong correct incorrect
true false real unreal
important unimportant relevant irrelevant
possible impossible probable improbable
likely unlikely certain uncertain
expected unexpected surprising unsurprising
common rare frequent infrequent
simple complex complicated
easy difficult hard soft
strong weak
fast slow quick rapid
early late prior posterior
past present future
current previous next
initial final intermediate
direct indirect
explicit implicit
conscious unconscious
internal external
objective subjective
absolute relative
fixed variable
static dynamic
linear nonlinear
local global
single multiple double triple
total partial
full empty
open closed
free paid
safe risky
fair unfair
normal abnormal
healthy unhealthy
natural artificial
physical mental
male female
adult child
urban rural
developed developing
rich poor
advantage disadvantage
increase decrease
improve worsen
maximize minimize
overestimate underestimate
overweight underweight
gain loss
reward punishment
success failure
winner loser
buyer seller
leader follower
teacher student
doctor patient
employer employee
manager worker
producer consumer
investor investment
saver saving savings
spender spending
borrower lender borrowing lending
insurer insured insurance
advisor advice
planner planning
retirement retiree
salary wage income
expense expenses spending
budget budgeting
tax taxes taxable
deduction deductions
credit credits
exemption exemptions
mortgage rent
property real estate
portfolio diversification rebalancing
allocation
equity equities
index indices
benchmark benchmarks
expense ratio
management fee fees
commission commissions
load no-load
factor factors
momentum value growth
size quality
volatility beta alpha
sharpe ratio
drawdown drawdowns
compounding compound
inflation deflation
recession depression
bubble bubbles
crash crashes
bull bear
sentiment optimism pessimism
overconfidence herding
disposition effect
endowment effect
status quo bias
sunk cost
opportunity cost
mental accounting
framing effect
anchoring effect
availability heuristic
representativeness heuristic
affect heuristic
loss aversion
risk aversion
risk seeking
ambiguity aversion
present bias
time discounting
hyperbolic discounting
self control
ego depletion
willpower
default defaults
opt-out opt-in
choice architecture
libertarian paternalism
asymmetric paternalism
nudge nudges
boost boosts
choice overload
paradox
anomaly anomalies
efficient market
hypothesis
random walk
prospect theory
expected utility
bounded rationality
satisficing
heuristics
dual process
system
fast slow
thinking
absent
attractive
best
compute
humans
introduction
irrelevant
large
rationale
represent
simple
smart
social
take
text
when
flagship
times
seed
approx
cdot
frac
sqrt
quad
ldots
alpha
beta
gamma
delta
homo
economicus
educated
industrialized
western
democratic
rich
inequality
framing
behavioral
economics
compute
humans
introduction
when
covid
fafsa
socratopia
beshears
choi
laibson
madrian
mehra
prescott
rajnish
edward
egger
fehr
schmidt
grossman
opower
dfid
mba
sop
cfp
spiva
simple
timely
easy
social
attractive
east
western
best
take
absent
irrelevant
large
inequality
rationale
flagship
represent
framing
seed
smart
text
times
approx
cdot
frac
sqrt
quad
ldots
alpha
beta
gamma
delta
homo
economicus
educated
industrialized
democratic
rich
covid
fafsa
socratopia
beshears
choi
laibson
madrian
mehra
prescott
rajnish
edward
egger
fehr
schmidt
grossman
opower
dfid
mba
sop
cfp
spiva
timely
easy
social
attractive
east
western
best
take
aftermath
brain
top-down
largely
literally
meaningful
mild
profile
promising
reflexive
ripple
ripples
sharp
session
sleep
steeply
substantial
timing
trade
triumph
wave
down
confident
"""
for w in connectors.split():
    whitelist.add(w.lower())

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
            if wlow not in whitelist and not wlow.isdigit():
                if wlow not in found:
                    found[wlow] = []
                found[wlow].append(os.path.basename(fp) + ':' + str(i))

print(f'Found {len(found)} unique words (4+ chars)')
for word in sorted(found.keys()):
    occ = found[word]
    print(f'{word} ({len(occ)}x): {occ[:8]}')
