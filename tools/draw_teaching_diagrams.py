from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import html, math, textwrap

FONT='/System/Library/Fonts/Supplemental/Arial.ttf'
BOLD='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
W,H=1600,720
INK='#152E42'; TEAL='#087F8C'; BLUE='#E8F3F7'; GOLD='#FFEBBC'; RED='#FBE7E4'
class Diagram:
    def __init__(self,title):
        self.im=Image.new('RGB',(W,H),'white'); self.d=ImageDraw.Draw(self.im)
        self.svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="1600" height="720" fill="white"/>']
        self.text(45,30,title,43,bold=True)
    def text(self,x,y,text,size=29,bold=False,color=INK):
        font=ImageFont.truetype(BOLD if bold else FONT,size)
        for j,line in enumerate(text.split('\n')):
            yy=y+j*(size+10);self.d.text((x,yy),line,font=font,fill=color)
            self.svg.append(f'<text x="{x}" y="{yy+size}" font-family="Arial, sans-serif" font-size="{size}" font-weight="{"bold" if bold else "normal"}" fill="{color}">{html.escape(line)}</text>')
    def rect(self,x,y,w,h,fill=BLUE,stroke=TEAL):
        self.d.rounded_rectangle((x,y,x+w,y+h),radius=15,fill=fill,outline=stroke,width=3)
        self.svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="15" fill="{fill}" stroke="{stroke}" stroke-width="3"/>')
    def box(self,x,y,w,h,title,body='',fill=BLUE):
        self.rect(x,y,w,h,fill);self.text(x+18,y+16,title,32,True)
        if body:self.text(x+18,y+65,body,28)
    def line(self,x1,y1,x2,y2,color=TEAL,arrow=False):
        self.d.line((x1,y1,x2,y2),fill=color,width=4)
        self.svg.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="4"/>')
        if arrow:
            a=math.atan2(y2-y1,x2-x1); pts=[(x2,y2),(x2-18*math.cos(a-.5),y2-18*math.sin(a-.5)),(x2-18*math.cos(a+.5),y2-18*math.sin(a+.5))]
            self.d.polygon(pts,fill=color);self.svg.append('<polygon points="'+' '.join(f'{x},{y}' for x,y in pts)+f'" fill="{color}"/>')
    def note(self,text):self.text(45,645,text,27)
    def save(self,root,name):
        root.mkdir(parents=True,exist_ok=True); self.im.save(root/(name+'.png'));(root/(name+'.svg')).write_text('\n'.join(self.svg)+'</svg>')

def build(root):
    d=Diagram('Learn by predicting and testing')
    titles=['Explain','Predict','Build','Break','Recover']
    bodies=['State the rule','Choose input\nand output','Make the\nsmall change','Run a negative\ncase','Repair and\nretest']
    for i,(t,b) in enumerate(zip(titles,bodies)):
        x=45+i*308;d.box(x,140,270,190,t,b)
        if i<4:d.line(x+270,235,x+305,235,arrow=True)
    d.box(45,415,1500,150,'One portfolio across the course','Requirement ID -> design -> configuration or code -> tests -> handover',GOLD)
    d.note('Each week adds evidence to the capstone. Independent practice changes the scenario.');d.save(root,'01_learning_cycle')

    d=Diagram('CRM entities and stable identity')
    d.box(55,270,310,175,'Account A001','One company record\nStable account ID')
    d.box(530,110,310,175,'Contacts','C001 and C002\nMany per account')
    d.box(530,370,310,175,'Deals','D001 and D002\nMany per account')
    d.box(1080,370,425,175,'Delivery requests','NOVA-D001 unique key\nWork items link to request')
    d.line(365,330,530,220,arrow=True);d.text(365,175,'1 to many',26)
    d.line(365,400,530,455,arrow=True);d.text(380,505,'1 to many',26)
    d.line(840,455,1080,455,arrow=True);d.text(865,340,'0 or 1 per\nwon deal',26)
    d.note('Names can change or repeat. Relationships use record identity, not copied display names.');d.save(root,'02_crm_entities')

    d=Diagram('Test operations and record visibility separately')
    cols=[45,435,790,1140]; widths=[390,355,350,405]
    headers=['Training persona','Own-region read','Other-region read','Admin change']
    values=[['Sales West','Allow','Deny','Deny'],['Sales East','Allow','Deny','Deny'],['Manager','Allow','Allow','Deny']]
    for x,w,t in zip(cols,widths,headers):d.rect(x,135,w,85,GOLD);d.text(x+16,155,t,29,True)
    for j,row in enumerate(values):
        for x,w,t in zip(cols,widths,row):d.rect(x,235+j*100,w,90,BLUE if t!='Deny' else RED);d.text(x+16,262+j*100,t,31)
    d.text(45,565,'Proposed lab policy. Execute allowed and denied checks with the actual training personas.',29)
    d.note('Role, profile and sharing behavior must be verified in the selected Zoho edition.');d.save(root,'03_access_matrix')

    d=Diagram('Event automation and controlled transitions')
    d.text(45,125,'Workflow responds to an event',32,True)
    for x,t,b in [(45,'Lead created','Event'),(560,'Region is West','Condition'),(1080,'Assign West Sales','Action')]:d.box(x,185,450,150,t,b)
    d.line(495,260,560,260,arrow=True);d.line(1010,260,1080,260,arrow=True)
    d.text(45,375,'Transition controls a permitted state change',32,True)
    d.box(45,435,450,150,'Draft quote','Amount > INR 50000')
    d.box(560,435,450,150,'Manager review','Required decision',GOLD)
    d.box(1080,435,450,150,'Approved to send','Evidence recorded')
    d.line(495,510,560,510,arrow=True);d.line(1010,510,1080,510,arrow=True)
    d.note('Synthetic threshold. Rejection returns for correction; verify available approval features.');d.save(root,'04_workflow_transition')

    d=Diagram('A lost response creates an unknown outcome')
    for x,t in [(65,'Source worker'),(620,'Destination'),(1180,'Reconciler')]:d.box(x,105,350,85,t)
    for x in [240,795,1355]:d.line(x,200,x,585,color='#A0B5C0')
    d.line(240,260,795,260,arrow=True);d.text(275,210,'Write NOVA-D002 v1',28)
    d.text(805,288,'Commit unique key',28,True)
    d.line(795,370,240,370,color='#B94A3B',arrow=True);d.text(280,322,'Response lost after commit',28,color='#B94A3B')
    d.line(1355,450,795,450,arrow=True);d.text(865,400,'Read by business key',28)
    d.line(795,550,1355,550,arrow=True);d.text(830,495,'Existing v1 found; reconcile',28)
    d.note('Do not assume timeout means no write. Replay and side effects require separate tests.');d.save(root,'05_sync_recovery')

    d=Diagram('Filter eligible sources before assembling context')
    for x,t,b in [(45,'Source manifest','ID, status, version\npermission and owner'),(565,'Eligibility filter','Approved + current\nand allowed permission'),(1085,'Rank evidence','Search only the\neligible records')]:d.box(x,150,450,180,t,b)
    d.line(495,240,565,240,arrow=True);d.line(1015,240,1085,240,arrow=True)
    d.box(45,440,450,150,'Exclude restricted','Draft, stale or denied',RED)
    d.box(565,440,450,150,'Assemble context','Preserve source IDs')
    d.box(1085,440,450,150,'Answer or abstain','Check claim support',GOLD)
    d.line(1310,330,1310,385);d.line(1310,385,785,385);d.line(785,385,785,440,arrow=True)
    d.line(565,290,490,440,arrow=True);d.line(1015,515,1085,515,arrow=True)
    d.note('The local exercise uses lexical search. Live model quality needs separate evaluation.');d.save(root,'06_retrieval_permissions')

    d=Diagram('Review binds to the candidate content version')
    for x,t,b in [(45,'Request','Known module + scope'),(565,'Generate draft','Approved source context'),(1085,'Validate','Shape + teaching checks')]:d.box(x,150,450,150,t,b)
    d.line(495,225,565,225,arrow=True);d.line(1015,225,1085,225,arrow=True)
    for x,t,b,col in [(45,'Release decision','Separate destination access',GOLD),(565,'Local approval','Selected artifact + hash',BLUE),(1085,'Human review','Technical and teaching',GOLD)]:d.box(x,425,450,150,t,b,col)
    d.line(1310,300,1310,425,arrow=True);d.line(1085,500,1015,500,arrow=True);d.line(565,500,495,500,arrow=True)
    d.note('Changed hash returns to review. Local approval does not publish or connect to Zoho.');d.save(root,'07_agent_review')

    d=Diagram('Reconcile every source row before and after import')
    d.text(45,125,'50 source rows = 42 staging accepted + 5 rejected + 3 excluded',35,True)
    x=45
    for count,col,label in [(42,BLUE,'42 accepted'),(5,RED,'5 rejected'),(3,GOLD,'3 excluded')]:
        width=1500*count/50;d.rect(x,220,width,130,col);x+=width
    d.text(60,264,'84 percent accepted for the lab policy',32,True)
    d.box(45,425,450,150,'Accepted staging','42 rows ready for trial')
    d.box(565,425,450,150,'Target trial import','Record actual results',GOLD)
    d.box(1085,425,450,150,'Reconciliation','Created + updated\n+ failed + exceptions')
    d.line(495,500,565,500,arrow=True);d.line(1015,500,1085,500,arrow=True)
    d.note('Staging acceptance is not target success. Preserve source IDs and migration batch.');d.save(root,'08_migration_reconciliation')

    d=Diagram('Report task quality and critical failures separately')
    d.box(45,145,705,190,'Normal task checks','Evidence supports claims\nOutput fits schema and duration\nLearner task can be completed')
    d.box(835,145,705,190,'Critical boundary checks','No restricted source exposure\nNo unauthorized external write\nNo credentials in artifacts',RED)
    d.box(45,430,705,155,'Report denominators','Passed / executed, by category\nNot run remains visible')
    d.box(835,430,705,155,'Proposed release gate','No observed critical failure\nReviewer owns acceptance',GOLD)
    d.note('A high average cannot waive a critical failure. Mock tests are not live-model results.');d.save(root,'09_evaluation_gates')

    d=Diagram('Measure the entire assisted task')
    d.text(45,120,'Synthetic timing example in minutes per task',32)
    d.text(45,220,'Baseline',32,True);d.rect(300,200,1100,90,BLUE);d.text(330,225,'10 minutes active work',31)
    d.text(45,385,'Assisted',32,True);d.rect(300,365,220,90,GOLD);d.rect(520,365,440,90,BLUE)
    d.text(320,387,'Draft 2',29);d.text(545,387,'Review and correct 4',29)
    d.text(300,500,'Total assisted time 6. Difference 4 minutes = 40 percent in this example.',31)
    d.note('Illustrative arithmetic, not observed Wooplix savings. Record quality and actual sample size.');d.save(root,'10_pilot_timing')
    return 10

if __name__=='__main__':
    import sys
    dest=Path(sys.argv[1]); print('Diagrams generated:',build(dest))
