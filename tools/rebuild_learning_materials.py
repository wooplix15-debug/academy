"""Rebuild Word, PDF and standalone HTML from editable course and lesson sources."""
from pathlib import Path
import base64, csv, html, json, re
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parents[1]
# During task-local authoring the canonical source lives in the versioned workspace.
if ROOT.name=='re': ROOT=ROOT/'outputs/Wooplix_Academy_Workspace_V2'
catalog=json.loads((ROOT/'data/catalog.json').read_text()); labs=json.loads((ROOT/'data/practical_labs.json').read_text())
def parts(mid):
    text=(ROOT/f'materials/lesson_plans/{mid}.md').read_text()
    found={}
    for match in re.finditer(r'^## (.*?)\n(.*?)(?=^## |\Z)',text,re.M|re.S):found[match[1]]=match[2].strip()
    return text,found
for l in labs:
    raw,p=parts(l['id'])
    l['concept']=p.get('Explain the concept',l['concept']); l['demonstration']=p.get('Demonstration and sample input',l['demonstration'])
    l['steps']=[re.sub(r'^\d+\.\s*','',s).rstrip('.') for s in p.get('Guided lab','').splitlines() if re.match(r'^\d+\.',s)] or l['steps']
    for field,heading in [('expected','Expected result'),('negative','Negative test'),('recovery','Recovery test')]: l[field]=p.get(heading,l[field])
    independent=p.get('Independent practice',l['independent']).split('\n\nBudget:')[0];l['independent']=independent
    trainer=(ROOT/f'materials/trainer_keys/{l["id"]}.md').read_text()
    match=re.search(r'## Oral answer\nQuestion: (.*?)\n\n(.*?)(?=\n## |\Z)',trainer,re.S)
    if match:l['oral_question'],l['oral_answer']=match.groups()
    l['live_hours']=next(m['live_hours'] for c in catalog['programs'] for m in c['modules'] if m['id']==l['id'])
    l['practice_hours']=next(m['practice_hours'] for c in catalog['programs'] for m in c['modules'] if m['id']==l['id'])
    schedule=[]
    for line in p.get('Live teaching sequence','').splitlines():
        match=re.match(r'- (.*?): (\d+) minutes$',line)
        if match:schedule.append((match[1],int(match[2])))
    if not schedule or sum(minutes for _,minutes in schedule)!=l['live_hours']*60:
        raise ValueError('Update the timed lesson sequence to match catalog hours: '+l['id'])
    l['schedule']=schedule
    c=next(c for c in catalog['programs'] if c['id']==l['course_id'])
    l['sources']=c['sources']
    example={'ZDV-M03':'normalize_requests.deluge','ZDV-M04':'normalize_requests.deluge','ZDV-M08':'create_training_lead.deluge'}.get(l['id'])
    if example:l['code_example']=(ROOT/'materials/code_examples'/example).read_text()

CAPTIONS={
'01_learning_cycle':'Figure 1 Each lesson predicts behavior, builds a small change and tests recovery. Evidence accumulates in one capstone portfolio.',
'02_crm_entities':'Figure 2 A fictional CRM model stores account identity once and relates contacts, deals and delivery requests.',
'03_access_matrix':'Figure 3 Proposed lab access matrix. Verify record visibility and operation permissions through training-persona tests.',
'04_workflow_transition':'Figure 4 Event automation and controlled state transitions answer different business requirements. The threshold is synthetic.',
'05_sync_recovery':'Figure 5 A write may commit even when its response is lost. Reconciliation reads by business key before a retry decision.',
'06_retrieval_permissions':'Figure 6 Source eligibility precedes ranking and context. Restricted or stale sources do not enter the public context.',
'07_agent_review':'Figure 7 Draft generation, technical review, local approval and external release are separate decisions.',
'08_migration_reconciliation':'Figure 8 Source classification reconciles 50 rows. Target import results require their own observed reconciliation.',
'09_evaluation_gates':'Figure 9 Task success, critical failures and not-run cases need separate reporting.',
'10_pilot_timing':'Figure 10 Synthetic timing arithmetic includes generation, review and correction. It is not evidence of business savings.'}
MAP={'ZIM-M01':'01_learning_cycle','ZIM-M02':'02_crm_entities','ZIM-M03':'03_access_matrix','ZIM-M04':'04_workflow_transition','ZIM-M05':'04_workflow_transition','ZIM-M06':'08_migration_reconciliation','ZIM-M07':'05_sync_recovery','ZIM-M09':'09_evaluation_gates','ZDV-M01':'02_crm_entities','ZDV-M07':'07_agent_review','ZDV-M09':'05_sync_recovery','AAB-M03':'07_agent_review','AAB-M04':'06_retrieval_permissions','AAB-M05':'06_retrieval_permissions','AAB-M06':'07_agent_review','AAB-M07':'09_evaluation_gates','AAB-M08':'10_pilot_timing','AAB-M09':'07_agent_review','CAW-M01':'10_pilot_timing','CAW-M03':'07_agent_review','CAW-M04':'10_pilot_timing'}
sources={}
manifest=json.loads((ROOT/'knowledge/manifest.json').read_text())
for r in manifest['records']:
    text=(ROOT/r['path']).read_text(); url=re.search(r'https://\S+',text)
    sources[r['id']]=r['title']+(' — '+url.group() if url else '')
payload={'courses':catalog['programs'],'labs':labs,'diagram_for':MAP,'captions':CAPTIONS,'sources':sources,
         'images':{name:'data:image/png;base64,'+base64.b64encode((ROOT/f'materials/diagrams/{name}.png').read_bytes()).decode() for name in CAPTIONS},
         'lesson_markdown':{l['id']:parts(l['id'])[0] for l in labs}}
template=(ROOT/'tools/learning_studio_template.html').read_text()
(ROOT/'Wooplix_Learning_Studio.html').write_text(template.replace('__PAYLOAD__',json.dumps(payload,ensure_ascii=False).replace('</','<\\/')))

pages=[]
def page(title,*blocks):pages.append({'title':title,'blocks':list(blocks)})
def p(text):return ('p',text)
def h(text):return ('h',text)
def bullets(*items):return ('bullets',items)
def image(name):return ('image',name)
def table(headers,rows,widths=None):return ('table',(headers,rows,widths))
def code(text):return ('code',text)

page('Wooplix Academy Practical Teaching Guide',
 p('This guide prepares trainers and learners to build tested CRM implementations, service applications and bounded AI workflows. Use it to plan a cohort, demonstrate the difficult concepts, review practical evidence and maintain the curriculum with your team.'),
 p('Version 0.2 | 3 October 2026 | Prepared for Wooplix Academy'),
 h('Four courses with different purposes'),
 table(['Course','Learner and result','Hours'],[[c['id'],c['title'],str(c['total_hours'])] for c in catalog['programs']],[.12,.70,.18]),
 h('How to use the complete pack'),
 bullets('Read the course progression and case brief before choosing modules. Keep one portfolio from the first lesson to the final defense.',
         'Teach from the 36 full lesson files or the offline Learning Studio. This guide explains the curriculum, visual models and selected worked labs; it does not duplicate every full lesson.',
         'Use the separate trainer keys, 72 assessment questions, 9 CSV evidence templates and Python exercises to prepare demonstrations and mark work.',
         'Rehearse exact Zoho steps in the selected training edition. Replace the fictional examples with sanitized, reviewed examples from your experience.'),
 h('Reading path'),
 p('Teaching method -> four course syllabi -> CRM design and access -> migration and synchronization -> retrieval and agent review -> pilot measurement -> assessment, team operations and first-cohort readiness.'),
 p('Completion evidence supports a Wooplix Academy assessment decision. Official Zoho credentials, employment outcomes and business savings must never be implied by an academy exercise.'))

page('Teach through prediction practice and recovery',image('01_learning_cycle'),
 h('Before class'),p('Select the requirement and smallest useful sample input. Run the normal, negative and recovery cases yourself. Save expected outputs separately from actual results. Confirm product edition, metadata, API version and training access.'),
 h('During class'),p('Explain the rule, ask learners to predict an output, demonstrate one case, then let them build. Introduce a deliberate failure before showing recovery. Require the learner to explain why the repair works. Keep the stated break time in the lesson budget.'),
 h('After class'),p('Independent practice changes the scenario. Learners submit input IDs, expected and observed results, evidence and a short explanation. Trainers review the evidence, not only a working screen. Carry accepted artifacts into the next module and final portfolio.'),
 p('Each 4-hour class has 240 live minutes including a 15-minute break; its 2-hour practice allocation is separate. Workshop modules use 120 live minutes including a 10-minute break plus 60 practice minutes. Optional extensions replace an agreed activity or add clearly optional time.'))

for c in catalog['programs']:
    rows=[[m['id'].split('-')[1],m['title'],f'{m["live_hours"]}+{m["practice_hours"]}',m['evidence']] for m in c['modules']]
    page(c['title'],p(c['audience']+'. '+c['outcome']),
         p(f'{c["weeks"]} weeks | {c["live_hours"]} live hours + {c["practice_hours"]} practical hours = {c["total_hours"]} hours.'+(' Workshop delivery is two facilitated days, with four participant follow-through hours spread across two weeks.' if c['id']=='CAW' else ' The capstone is built progressively within these hours.')),
         h('Entry requirement'),p(c['prerequisites']),
         table(['Module','Teaching focus','Live plus practice','Portfolio evidence'],rows,[.11,.29,.12,.48]),
         h('Final demonstration'),p(c['capstone']+' '+c['tests']))

page('Design CRM records around business identity',image('02_crm_entities'),
 p('Start with the Nova Services case brief. The sales journey is inquiry, qualification, quote review, won deal and delivery handoff. Departments share customer identity while owning different parts of the journey.'),
 h('Guided design task'),bullets('Define account, contact, deal and delivery-request keys. Mark one-to-many relationships and optional links.',
 'Give each field a type, owner, sample value and reason for being required. Verify actual API names in the training organization.',
 'Map R01 through R08 to a feature, field or documented gap. Keep assumptions beside the decision instead of hiding them in configuration.'),
 h('Check understanding'),p('Two accounts can have the same display name. Renaming A001 should not break D001. Ask the learner to explain how identifiers preserve relationships, then add a recurring renewal without copying the account.'),
 p('Evidence: entity diagram, data dictionary and requirement-to-design mapping. See ZIM-M02 and ZDV-M01 for full tasks and trainer keys.'))

page('Prove access with training personas',image('03_access_matrix'),
 p('The matrix expresses a proposed business policy. Product configuration must be tested with the intended users. Roles, profiles and sharing choices affect different parts of access.'),
 h('Run allowed and denied tests'),bullets('Sales West reads and edits its own regional record. Sales East attempts to read that West-only record.',
 'The manager reviews records from both regions. Export and administrative changes have their own explicit tests.',
 'Record persona, operation, record ID, expected result, actual result, environment and evidence reference. Do not submit tokens or personal data.'),
 h('Failure and recovery'),p('Seed an overly broad sharing rule. Confirm the denial test fails, correct the rule and rerun all visibility tests it could affect. Retain the original failure evidence.'),
 p('If training licensing prevents additional personas, record a simulated matrix and the unexecuted live tests. A paper matrix is useful design evidence but cannot prove actual permission behavior.'))

page('Control events transitions and approvals',image('04_workflow_transition'),
 p('An event rule asks what should happen when a record is created or edited. A controlled transition asks what must be true before moving to the next business state. Quote approval also needs a decision owner and rejection route.'),
 h('Worked boundary test'),p('Synthetic policy: a quote greater than INR 50000 requires manager approval. Test 49999, 50000 and 50001. At 50001, an attempted move from Draft to Sent without review must be blocked by the chosen implementation.'),
 h('Repeated execution test'),p('Create one lead, then edit only its phone number twice. Count intended follow-up tasks and explain when the configured event is eligible. A unique proposed task key may require a supported feature, customization or monitoring gap.'),
 h('Recovery test'),p('Reject a quote, revise it and resubmit. Decide explicitly whether a changed amount invalidates earlier approval. Verify the actual Blueprint and approval features in the training edition.'),
 p('Evidence: event-condition-action register, state diagram, boundary results and rejection history. Full lessons: ZIM-M04 and ZIM-M05.'))

page('Migration lab input and procedure',image('08_migration_reconciliation'),
 p('The supplied leads_50.csv contains 50 synthetic rows with stable source IDs. The lab requires name, company and syntactically valid email. These are exercise rules; a real import must follow current organization and layout metadata.'),
 h('Predict before running'),p('Rows 43-47 have missing or invalid required values. Rows 48-50 repeat normalized emails from rows 1-3. The policy keeps the first valid occurrence. Predict 42 staging accepted, 5 rejected and 3 intentionally excluded.'),
 code('python3 practice/practice_lab.py migration --out practice/results'),
 h('Perform the trial'),p('Preserve the original file and hash. Inspect accepted.csv, rejected.csv and excluded.csv. Map staging fields to verified target fields and import only into the training organization. Retain source ID and batch ID to support reconciliation and recovery.'),
 p('Do not report offline acceptance as actual target creation. Target-side duplicates, constraints and errors must be observed separately.'))

page('Migration lab answer and recovery guide',
 table(['Classification','Expected count','Meaning'],[['Source','50','Every supplied row'],['Staging accepted','42','Passed the lab policy'],['Rejected','5','Invalid or missing values'],['Excluded','3','Later normalized-email duplicates']],[.30,.18,.52]),
 h('Inspect reasons'),p('L043 and L047 lack name, L044 lacks company, L045 has malformed email and L046 has blank email. L048-L050 duplicate L001-L003 after lowercase normalization. Blank region is valid for import under this lab policy and routes to Review Queue.'),
 h('Separate staging and destination reports'),p('After a real trial, record created, updated, failed and unresolved results against accepted source IDs. An import that updates an existing record needs different recovery evidence from a newly created record. Keep before-values for any permitted update.'),
 h('Recovery exercise'),p('Remove only records created by NOVA-TRAIN-01. Restore separately any records updated by the batch. Reconcile again and show no unrelated records were affected. Rehearse this procedure with training data before any business migration.'),
 h('Independent variation'),p('Permit a blank company while retaining the other rules. The local validator should now accept 43, reject 4 and exclude 3. Explain why the total remains 50 and how this rule differs from the actual product metadata.'),
 h('Trainer assessment'),p('Require classification reasons, batch identity, target actuals or clear not-run labels, and a recovery design. Reject a portfolio containing only an import success screen.'),
 p('Worksheet: migration_reconciliation.csv. Full lesson: ZIM-M06. Source refresh: the official planned mandatory-field notice S11 is not a deployed behavior claim.'))

page('Synchronization lab write replay and reconcile',image('05_sync_recovery'),
 p('The local destination uses a SQLite unique business key and transaction. This makes the simulator useful for reasoning about replay and version conflicts; it is not a Zoho API adapter.'),
 code('python3 practice/practice_lab.py sync --out practice/results'),
 h('Trace the sequence'),bullets('Create NOVA-D001 version 1 amount 1250, then replay the same operation.',
 'Create NOVA-D002 version 1 amount 800, but lose the response after commit. Query by business key to reconcile the unknown outcome.',
 'Update D001 to version 2 amount 1500. Attempt stale version 1, then a conflicting version 2 amount 9999.'),
 h('Expected result'),p('Two destination business records. D001 retains version 2 and amount 1500. Replay returns the existing record; stale and same-version conflicting writes are rejected. The lost response is reconciled from persisted state.'))

page('Synchronization lab answer and transfer to Zoho',
 table(['Input','Expected simulator status','Destination effect'],[['D001 v1 amount 1250','created','One D001 row'],['Repeat same key and payload','replayed','No extra row'],['D002 timeout after commit','timeout reconciled','D002 already exists'],['D001 v2 amount 1500','updated','Latest value retained'],['D001 v1 again','stale rejected','No downgrade'],['D001 v2 amount 9999','conflict rejected','No silent overwrite']],[.35,.30,.35]),
 h('Explain the controls'),p('Business identity constrains record creation. A version comparison prevents a stale writer from downgrading a record. Matching version with different content is a conflict, not an ordinary replay. These choices are explicit lab policies.'),
 h('Connected implementation design'),p('For a real CRM integration, verify supported duplicate-check or external-ID matching, conditional updates, field ownership and workflow triggers. The current Upsert reference S09 describes insert-or-update matching; it does not establish exactly-once downstream task execution.'),
 h('Failure decisions'),p('Authorization denial needs a reviewed configuration decision, not blind retries with broader access. Quota exhaustion pauses the run. An ambiguous timeout needs read-and-reconcile by identity before replay. Use bounded retries only for errors classified as retryable.'),
 h('Independent extension'),p('Use two workers against the same business key and propose destination uniqueness or transaction control. The included two-connection test is sequential; concurrent stress testing remains a separate extension.'),
 p('Full lesson: ZDV-M09. Worksheet: sync_contract.csv. Evidence must label local mocks and separately executed sandbox tests.'))

page('Prepare evidence before generating answers',image('06_retrieval_permissions'),
 p('A knowledge manifest carries source ID, owner, status, permission, version and date. Public retrieval excludes restricted or obsolete records before assembling context. Ranking considers only eligible evidence.'),
 h('Local retrieval exercise'),code('python3 practice/practice_lab.py retrieval --out practice/results'),
 p('K1 is approved public issuer guidance. K2 is a stale draft. K3 is client-only. K4 is a quarantined instruction attack. K5 and K6 are conflicting approved attendance policies. The local exercise uses word overlap and returns evidence; it does not invoke a model or use embeddings.'),
 h('Predict outputs'),bullets('Certificate issuer: evidence from K1.', 'Job guarantee and client secret: abstain under the eligible evidence set.', 'Attendance threshold: show conflict requiring owner review.'),
 p('Full lessons: AAB-M04 and AAB-M05. Never infer live model reliability from this deterministic retrieval test.'))

page('Retrieval lab answer and evidence review',
 h('When evidence is enough'),p('A supported answer states the source ID and the specific supporting claim. Source existence is only the first check; the cited content must support the exact assertion. A real citation may still be used incorrectly.'),
 h('When evidence is missing'),p('An unsupported question should produce a clear abstention or a request for an approved source. Do not promote a draft or restricted document because it is highly relevant. Empty retrieval is not permission to invent an answer.'),
 h('When evidence conflicts'),p('The fixture deliberately contains two current approved attendance policies. The correct output is conflict_review, not an arbitrary choice of the numerically higher threshold. The academy owner must choose the applicable policy and retire the conflicting record.'),
 h('Instruction attacks'),p('A document can contain text that tries to override the assistant instructions. Treat it as data. The quarantined fixture tests eligibility filtering; resistance to attacks inside an eligible document must be exercised with an actual configured model and tool workflow.'),
 h('Independent practice'),p('Write a paraphrased query that lexical overlap fails to retrieve. Explain what semantic retrieval might improve and why permission filtering is still required. Add one approved source and rerun a formerly unanswered case.'),
 h('Trainer marking'),p('Score relevance, exact claim support, appropriate abstention, conflict handling and access behavior separately. Record model name, prompt version, source versions, input, actual output and reviewer when running a live experiment.'),
 p('Twenty designed evaluation cases are supplied with blank actuals. Do not mark them passing without execution.'))

page('Use the Academy agent to draft reviewed changes',image('07_agent_review'),
 p('The included Python content agent can generate draft lessons, assessments, curriculum and website copy when configured with a model API key. It supports selected local artifact approval with version hashes and backups. It is not connected to Zoho, a shared drive or a live website.'),
 h('Start with an offline context check'),code('python3 agent/academy_agent.py draft '+chr(92)+'\n  --request requests/practical_lesson_ZDV_M09.json --dry-run'),
 p('Use the agent setup guide to configure OPENAI_API_KEY and WOOPLIX_MODEL when live generation is wanted. A dry run checks the selected catalog, sources and inputs; it does not generate or assess a live lesson.'),
 h('Review the candidate'),p('Require concrete sample input, expected result, negative and recovery tests, independent variation and trainer answers. Check impact on outcomes, hours, questions, capstone tests, website claims and active cohorts. Select the exact artifact for local approval only after review.'),
 p('The operator runner is local and single-user. Team author and reviewer assignments are registers, not authenticated multi-user access controls.'))

page('Evaluate quality and critical boundaries',image('09_evaluation_gates'),
 p('Use materials/agent_evaluation_20_cases.csv to record supported, missing, stale, conflicting, restricted, injection, malformed, tool-failure and operating-limit cases. Each has an expected behavior and critical flag; actual results start not run.'),
 h('Record what actually ran'),p('Use a separate environment label for deterministic mocks, connected product tests and live model tests. Report passed divided by executed cases within each category. Keep the count of unexecuted cases visible.'),
 h('Proposed acceptance gate'),p('No observed critical permission, credential or unauthorized-action failure is acceptable for release. A 95-percent task success rate with one restricted-source leak fails the gate. The reviewer also examines pedagogical usefulness and factual support.'),
 h('Repair and retest'),p('Preserve the failing input and output. Change the smallest relevant rule, then rerun that case and related boundary cases. Add new cases from sanitized, reviewed learner feedback.'))

page('Measure a corporate pilot through the whole task',image('10_pilot_timing'),
 p('The workshop chooses one small task, maps its baseline, tests assisted work, ranks opportunities and writes a two-week pilot brief. A training session alone does not authorize implementation access or consulting work.'),
 h('Worked timing exercise'),p('Synthetic baseline examples are 8, 10 and 12 active minutes, mean 10. An illustrative assisted task uses 2 minutes drafting and 4 reviewing or correcting, total 6. The 4-minute difference is 40 percent for this example; it is not an observed saving.'),
 h('Pilot acceptance hypothesis'),p('Propose 20 sanitized drafts with zero unsupported commitments after review and at least 20-percent lower median total task time. Record actual timing, quality, reviewer and sample size before deciding whether the hypothesis holds.'),
 h('Independent variation'),p('Repeat the design for support summaries. Separate customer statements from confirmed findings and include a quality measure beyond speed. Rejection returns the draft for correction; nothing is sent automatically.'))

page('Assess demonstrated competence',
 table(['Practical dimension','Points','Evidence'],[['Business fit and traceability','20','Requirement and design mapping'],['Correct behavior','30','Input and expected versus actual result'],['Failure and recovery','25','Negative case and successful retest'],['Evidence and handover','15','Environment, IDs and runbook'],['Independent explanation','10','New input and oral defense']],[.42,.13,.45]),
 h('Course result'),p('ZIM, ZDV and AAB combine quizzes 15 percent, module labs 35 percent, capstone 40 percent and defense 10 percent. Scores 80, 75, 85 and 70 yield 79.75 overall. Proposed pass policy requires overall at least 70, module-lab average and capstone each at least 70, attendance at least 80 percent, critical gates and reviewer acceptance.'),
 p('CAW combines pilot brief 70 percent and demonstration 30 percent. Both practical components must reach 70 under the proposed policy. Owner confirms policies and reassessment terms before enrollment.'),
 h('Calibrate marking'),p('Two trainers independently mark one strong, one borderline and one failed portfolio. Compare deductions and evidence expectations. Blank actuals remain not run. Give a specific correction and independent retest for a resubmission.'),
 h('Question bank'),p('The 72-question CSV maps two questions to every module: an oral explanation and a failure-and-recovery scenario. Answer guidance and rationale support trainer preparation. Self-review answers do not replace an independent defense.'))

page('Use worksheets to make evidence inspectable',
 table(['Template','Purpose'],[['requirements.csv','Owner, trigger, normal and exception criteria'],['data_dictionary.csv','Identity, type, owner and metadata checks'],['access_tests.csv','Allowed and denied persona operations'],['automation_register.csv','Trigger, condition, action and replay behavior'],['uat_log.csv','Expected versus actual, evidence and severity'],['migration_reconciliation.csv','Staging and target counts with recovery'],['sync_contract.csv','Field mapping, ownership and conflict rule'],['baseline_and_pilot.csv','Active timing, review effort and quality'],['change_request.csv','Hours, assessment and active-cohort impact']],[.43,.57]),
 h('Learner routine'),p('Copy the relevant template, record predictions, perform the task, then write observed results. Link evidence by module and requirement ID. Explain one failure, one repair and one remaining limitation in the portfolio workbook.'),
 h('Trainer routine'),p('Pick one submitted case and ask the learner to repeat it with a fresh input. Confirm that evidence includes the actual environment. Mark a mock path correctly without claiming an unexecuted connected-product result.'),
 h('Peer handover'),p('Give another learner the runbook and one pending item. They should identify owner, failure indicator, recovery and escalation without narration. Record the peer outcome and repair unclear instructions.'))

page('Maintain content with your team',
 h('Assign three responsibilities'),p('The author supplies a useful lesson and an impact report. The technical reviewer verifies current product behavior and rehearses every step. The teaching reviewer checks timing, independent practice, expected outputs, answer quality and accessibility. The academy owner accepts policy and public claims.'),
 h('Capture your experience'),p('Use team/EXPERTISE_INPUT.md to record a sanitized situation, original problem, constraints, choices, failure, repair and lesson learned. Identify what is a real reviewed case and what is proposed teaching content. Obtain relevant permission before using identifiable client examples.'),
 h('Track a change'),p('Assign change ID and version. Identify affected lesson, outcome, worksheet, question, capstone test, hours and public copy. Preserve the previous version and reviewer decision. If an active cohort is affected, prepare a correction or migration note before adopting the change.'),
 h('Keep generated formats aligned'),p('Markdown lessons and trainer keys are editable sources. Rebuild the studio and teaching guide with tools/rebuild_learning_materials.py, then inspect the new Word and PDF renders. A lesson edit does not automatically change website copy or existing enrollment terms.'),
 h('Review cadence'),p('Before every cohort, refresh official sources and rehearse product steps. After each module, review learner failures and timing. After a cohort, calibrate the assessments and approve the next version. These are proposed operating routines; assign dates and owners in the team register.'))

page('Prepare the first cohort',
 h('Admission diagnostic'),bullets('ZIM: inspect a sample CRM record, explain a basic workflow, cleanse five rows and describe a safe import. Use a bridge exercise for a small gap.',
 'ZDV: trace a map and conditional, normalize zero versus missing input, read JSON and explain an HTTP response. Require programming readiness for the coded track.',
 'AAB: separate deterministic calculations from generated language, explain a source-supported answer, and complete a coding bridge for the coded track.',
 'CAW: sponsor brings a bounded process, attendees, approved examples, baseline hypothesis and decision owner.'),
 h('Before opening enrollment'),bullets('Owner confirms target audience, course duration, schedule, price, support scope, refund terms and academy credential wording.',
 'Trainer verifies product editions, accounts, required features, mock alternatives and model budget. Rehearse all selected demonstrations.',
 'Assign technical and teaching reviewers. Confirm marking rubric, capstone evidence, critical gates and resubmission terms.',
 'Select the first course based on available expertise and trainer readiness. Keep the other offers editable; all four need not launch simultaneously.'),
 h('Start the first session'),p('Explain the portfolio, independent practice and honest evidence labels. Run the diagnostic, demonstrate one small case, then have learners predict and test an exception. Collect one question and one timing observation for the next revision.'),
 p('Website copy is included for your own site. Confirm every deliverable, claim, duration and policy before publishing it.'))

page('Official references and product refresh',
 p('The reference notes link to official documentation checked on 2 and 3 October 2026. Trainers should verify current product behavior before a live demonstration. Synthetic rules and simulator behavior are described as exercises rather than product guarantees.'),
 table(['ID','Reference'],[[sid,sources[sid].replace(' — ','\n')] for sid in sources],[.10,.90]),
 h('Planned changes require careful wording'),p('S11 describes a mandatory-field behavior change planned for the end of October 2026 and explicitly says it is not live yet at the check date. Do not teach it as deployed. Check the latest notice and actual layout or field metadata before the next cohort.'),
 h('Keep evidence current'),p('Record documentation date, product edition, account metadata and observed result. A documentation link supports the relevant product fact; the trainer still rehearses the procedure. Exact limits, prices and model availability belong in current configuration, not hardcoded course promises.'))

FONT=Path('/System/Library/Fonts/Supplemental')
if (FONT/'Arial.ttf').exists():
    regular=FONT/'Arial.ttf'; bold=FONT/'Arial Bold.ttf';italic=FONT/'Arial Italic.ttf'
else:
    regular=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf');bold=regular.with_name('DejaVuSans-Bold.ttf');italic=regular.with_name('DejaVuSans-Oblique.ttf')
for name,path in [('Academy',regular),('AcademyBold',bold),('AcademyItalic',italic)]:pdfmetrics.registerFont(TTFont(name,str(path)))
pdfmetrics.registerFontFamily('Academy',normal='Academy',bold='AcademyBold',italic='AcademyItalic',boldItalic='AcademyBold')
styles={'title':ParagraphStyle('Title',fontName='AcademyBold',fontSize=26,leading=31,spaceAfter=20,textColor=colors.black),
        'H1':ParagraphStyle('H1',fontName='AcademyBold',fontSize=19,leading=24,spaceAfter=15,textColor=colors.black),
        'H2':ParagraphStyle('H2',fontName='AcademyBold',fontSize=12,leading=16,spaceBefore=9,spaceAfter=6),
        'body':ParagraphStyle('body',fontName='Academy',fontSize=10.5,leading=14.2,spaceAfter=8),
        'cell':ParagraphStyle('cell',fontName='Academy',fontSize=9,leading=11.4,spaceAfter=0),
        'caption':ParagraphStyle('caption',fontName='AcademyItalic',fontSize=8.5,leading=11,spaceAfter=12),
        'code':ParagraphStyle('code',fontName='Courier',fontSize=9,leading=12,spaceBefore=5,spaceAfter=10,backColor=colors.HexColor('#eef4f6'),borderPadding=8)}
def clean(s):return s.replace(' — ',' - ').replace('→','->').replace('’',"'").replace('–','-')
def para(text,kind='body'):
    return Paragraph(html.escape(clean(text)).replace('\n','<br/>'),styles[kind])
def pdf_table(headers,rows,widths):
    w=A4[0]-108; widths=widths or [1/len(headers)]*len(headers)
    data=[[para(str(v),'cell') for v in row] for row in [headers]+rows]
    t=Table(data,colWidths=[w*x for x in widths],repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e8f3f7')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('LINEBELOW',(0,0),(-1,0),.6,colors.HexColor('#91adb8')),('LINEBELOW',(0,1),(-1,-1),.25,colors.HexColor('#dbe6ea'))]))
    return t
doc=Document(); sec=doc.sections[0];sec.page_width=Inches(8.2677);sec.page_height=Inches(11.6929)
sec.top_margin=sec.bottom_margin=Inches(.70);sec.left_margin=sec.right_margin=Inches(.75)
for name in ('Normal','Title','Heading 1','Heading 2','Caption'):
    st=doc.styles[name];st.font.name='Arial';st.font.color.rgb=RGBColor(0,0,0)
    if st.element.pPr is not None:
        for elem in list(st.element.pPr):
            if elem.tag==qn('w:pBdr'):st.element.pPr.remove(elem)
doc.styles['Normal'].font.size=Pt(10.5);doc.styles['Normal'].paragraph_format.space_after=Pt(7);doc.styles['Normal'].paragraph_format.line_spacing=1.08
for name,size in [('Title',26),('Heading 1',19),('Heading 2',12),('Caption',8.5)]:doc.styles[name].font.size=Pt(size)
doc.styles['Title'].font.bold=True;doc.styles['Heading 1'].font.bold=True;doc.styles['Heading 2'].font.bold=True
footer=sec.footer.paragraphs[0];footer.alignment=2
footer.add_run('Wooplix Academy  |  ')
field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGE');footer._p.append(field)
for r in footer.runs:r.font.size=Pt(8);r.font.color.rgb=RGBColor(73,97,111)
story=[]; markdown=[]
for i,pg in enumerate(pages):
    if i:doc.add_page_break();story.append(PageBreak())
    doc.add_paragraph(pg['title'],style='Title' if i==0 else 'Heading 1');story.append(para(pg['title'],'title' if i==0 else 'H1'));markdown.append('# '+pg['title'])
    for kind,value in pg['blocks']:
        if kind in ('p','h','code'):
            if kind=='h':d=doc.add_paragraph(value,style='Heading 2');story.append(para(value,'H2'))
            else:
                d=doc.add_paragraph(clean(value));story.append(para(value,'code' if kind=='code' else 'body'))
                if kind=='code':
                    for r in d.runs:r.font.name='Courier New';r.font.size=Pt(9)
            markdown.append(('## ' if kind=='h' else '')+value)
        elif kind=='bullets':
            for item in value:
                doc.add_paragraph(clean(item),style='List Bullet');story.append(para('- '+item));markdown.append('- '+item)
        elif kind=='image':
            img=ROOT/f'materials/diagrams/{value}.png';d=doc.add_paragraph();d.paragraph_format.keep_with_next=True
            run=d.add_run();pic=run.add_picture(str(img),width=Inches(6.70))
            pic._inline.docPr.set('descr',CAPTIONS[value]);doc.add_paragraph(CAPTIONS[value],style='Caption')
            story.extend([Image(str(img),width=A4[0]-108,height=(A4[0]-108)*720/1600),para(CAPTIONS[value],'caption')])
            markdown.append(f'![{CAPTIONS[value]}](materials/diagrams/{value}.png)')
        elif kind=='table':
            headers,rows,widths=value; t=doc.add_table(rows=1,cols=len(headers));t.autofit=False
            fractions=widths or [1/len(headers)]*len(headers)
            for column,fraction in zip(t.columns,fractions):column.width=Inches(6.77*fraction)
            for cell,fraction in zip(t.rows[0].cells,fractions):cell.width=Inches(6.77*fraction)
            for cell,text in zip(t.rows[0].cells,headers):cell.text=str(text)
            props=t.rows[0]._tr.get_or_add_trPr(); repeat=OxmlElement('w:tblHeader');props.append(repeat)
            for row in rows:
                cells=t.add_row().cells
                for cell,fraction,text in zip(cells,fractions,row):cell.width=Inches(6.77*fraction);cell.text=clean(str(text))
            for j,row in enumerate(t.rows):
                trpr=row._tr.get_or_add_trPr();cant=OxmlElement('w:cantSplit');trpr.append(cant)
                for cell in row.cells:
                    for par in cell.paragraphs:
                        par.paragraph_format.space_after=Pt(4);par.paragraph_format.space_before=Pt(3)
                        for run in par.runs:run.font.size=Pt(9);run.bold=(j==0)
                    if j==0:
                        shd=OxmlElement('w:shd');shd.set(qn('w:fill'),'E8F3F7');cell._tc.get_or_add_tcPr().append(shd)
            story.extend([pdf_table(headers,rows,widths),Spacer(1,10)])
            markdown.append('| '+' | '.join(headers)+' |\n| '+' | '.join('---' for _ in headers)+' |\n'+'\n'.join('| '+' | '.join(str(v).replace('\n',' ') for v in row)+' |' for row in rows))
doc.core_properties.title='Wooplix Academy Practical Teaching Guide';doc.core_properties.author='Wooplix Academy';doc.core_properties.subject='Curriculum practical labs and trainer operations'
docx=ROOT/'Wooplix_Academy_Practical_Teaching_Guide.docx';pdf=ROOT/'Wooplix_Academy_Practical_Teaching_Guide.pdf';doc.save(docx)
def footer_pdf(canvas,doc):
    canvas.setFont('Academy',8);canvas.setFillColor(colors.HexColor('#49616f'));canvas.drawRightString(A4[0]-54,30,'Wooplix Academy  |  '+str(doc.page))
SimpleDocTemplate(str(pdf),pagesize=A4,leftMargin=54,rightMargin=54,topMargin=50,bottomMargin=50,title='Wooplix Academy Practical Teaching Guide',author='Wooplix Academy').build(story,onFirstPage=footer_pdf,onLaterPages=footer_pdf)
(ROOT/'Wooplix_Academy_Practical_Teaching_Guide.md').write_text('\n\n'.join(markdown)+'\n')
print(json.dumps({'planned_sections':len(pages),'word':str(docx),'pdf':str(pdf),'studio_lessons':len(labs)}))
