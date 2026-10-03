#!/usr/bin/env python3
"""Wooplix content drafting agent. Standard library only; never executes model code."""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import sys
import urllib.error
import urllib.request
import uuid

ROOT=Path(__file__).resolve().parents[1]
MODES={'curriculum','lesson','assessment','website','corporate','feedback','operations'}
MAX_CONTEXT=100_000
MAX_FILE=80_000
ARTIFACT_KEYS={'path','content','outcome_mapping','source_ids','review_notes'}
RESULT_KEYS={'summary','assumptions','review_required','change_impact','artifacts'}
SCHEMA={
 'type':'object','additionalProperties':False,
 'properties':{
  'summary':{'type':'string'},'assumptions':{'type':'array','items':{'type':'string'}},
  'review_required':{'type':'boolean'},'change_impact':{'type':'array','items':{'type':'string'}},
  'artifacts':{'type':'array','items':{'type':'object','additionalProperties':False,
   'properties':{key:({'type':'array','items':{'type':'string'}} if key in ('outcome_mapping','source_ids','review_notes') else {'type':'string'}) for key in sorted(ARTIFACT_KEYS)},
   'required':sorted(ARTIFACT_KEYS)}}},'required':sorted(RESULT_KEYS)}

def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def digest(content): return hashlib.sha256(content.encode('utf-8')).hexdigest()
def read_json(path): return json.loads(path.read_text(encoding='utf-8'))
def write_json(path,data): path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def safe_path(root, relative, roots=None, suffix=None):
    if not isinstance(relative,str) or not relative or '\\' in relative:
        raise ValueError('Invalid artifact path')
    p=PurePosixPath(relative)
    if p.is_absolute() or any(x in ('..','.') for x in p.parts) or str(p)!=relative:
        raise ValueError('Path must be a normalized relative path')
    if roots and (len(p.parts)<2 or p.parts[0] not in roots):
        raise ValueError('Path is outside the allowed content folders')
    if suffix and p.suffix not in suffix: raise ValueError('Artifact file extension is not allowed')
    target=root.joinpath(*p.parts)
    if not target.resolve().is_relative_to(root.resolve()): raise ValueError('Path escapes workspace through a link')
    # Reject symlinks even when they resolve within the workspace.
    cursor=root
    for part in p.parts:
        cursor=cursor/part
        if cursor.is_symlink(): raise ValueError('Symlink destinations are not supported')
    return target

def validate_catalog(catalog):
    ids=set()
    if not isinstance(catalog.get('programs'),list) or not catalog['programs']: raise ValueError('Catalog has no programs')
    for course in catalog['programs']:
        cid=course['id']
        if cid in ids: raise ValueError('Duplicate program ID')
        ids.add(cid); module_ids=set(); live=practice=0
        for module in course['modules']:
            mid=module['id']
            if mid in module_ids: raise ValueError('Duplicate module ID')
            for dep in module['depends_on']:
                if dep not in module_ids: raise ValueError('Invalid prerequisite ordering')
            module_ids.add(mid)
            for field in ('live_hours','practice_hours'):
                value=module[field]
                if isinstance(value,bool) or not isinstance(value,(int,float)) or value<0: raise ValueError('Invalid hour value')
            if not module['outcomes'] or not module['acceptance_checks']: raise ValueError('Missing outcomes or assessment checks')
            live+=module['live_hours']; practice+=module['practice_hours']
        if (live,practice,live+practice)!=(course['live_hours'],course['practice_hours'],course['total_hours']): raise ValueError('Hour totals do not match modules')
        if sum(course['assessment_weights'].values())!=100: raise ValueError('Assessment weights must sum to 100')
    return catalog

def context_for(request, root=ROOT):
    if request.get('mode') not in MODES: raise ValueError('Unsupported task mode')
    if not isinstance(request.get('instructions'),str) or not request['instructions'].strip(): raise ValueError('Request instructions are required')
    if len(request['instructions'])>20_000: raise ValueError('Request instructions are too long')
    catalog=validate_catalog(read_json(root/'data/catalog.json'))
    course_id=request.get('course_id')
    selected=[p for p in catalog['programs'] if course_id in (None,p['id'])]
    if not selected: raise ValueError('Unknown course ID')
    module=request.get('module_id')
    if module and not any(module==m['id'] for p in selected for m in p['modules']): raise ValueError('Unknown module for selected course')
    manifest=read_json(root/'knowledge/manifest.json'); allowed={r['id']:r for r in manifest['records']}
    records=[]
    for sid in request.get('source_ids',[]):
        record=allowed.get(sid)
        if not record or record['status'] not in ('approved','verified_public_reference') or record['permission']!='public':
            raise ValueError('Source is missing, unapproved or restricted: '+str(sid))
        source=safe_path(root,record['path'],roots={'knowledge'},suffix={'.md','.txt'})
        content=source.read_text(encoding='utf-8')
        if len(content)>MAX_FILE: raise ValueError('Knowledge file is too large')
        records.append({'id':sid,'status':record['status'],'version':record['version'],'content':content})
    assets=[]
    for rel in request.get('input_assets',[]):
        path=safe_path(root,rel,roots={'curriculum','materials','website','operations','team'},suffix={'.md','.csv','.json'})
        content=path.read_text(encoding='utf-8')
        if len(content)>MAX_FILE: raise ValueError('Input asset is too large')
        assets.append({'path':rel,'status':'working_draft_unless_individually_approved','content':content})
    context={'request':request,'catalog_status':catalog['status'],'programs':selected,'sources':records,'input_assets':assets}
    serialized=json.dumps(context,ensure_ascii=False)
    if len(serialized)>MAX_CONTEXT: raise ValueError('Context exceeds the local limit; select fewer sources or input assets')
    return serialized,{r['id'] for r in records}

def validate_result(result, source_ids):
    if not isinstance(result,dict) or set(result)!=RESULT_KEYS: raise ValueError('Invalid result fields')
    if result['review_required'] is not True: raise ValueError('Every generated result must require review')
    if not isinstance(result['summary'],str): raise ValueError('Missing summary')
    for key in ('assumptions','change_impact'):
        if not isinstance(result[key],list) or any(not isinstance(x,str) for x in result[key]): raise ValueError('Invalid list field')
    artifacts=result['artifacts']
    if not isinstance(artifacts,list) or not 1<=len(artifacts)<=12: raise ValueError('A result must contain one to twelve artifacts')
    paths=set()
    for artifact in artifacts:
        if not isinstance(artifact,dict) or set(artifact)!=ARTIFACT_KEYS: raise ValueError('Invalid artifact fields')
        rel=artifact['path']; safe_path(ROOT,rel,roots={'curriculum','materials','website','operations'},suffix={'.md'})
        if rel in paths: raise ValueError('Duplicate artifact path')
        paths.add(rel)
        content=artifact['content']
        if not isinstance(content,str) or not content.strip() or len(content)>MAX_FILE: raise ValueError('Empty or oversized artifact')
        if not content.lstrip().startswith('# '): raise ValueError('Artifact needs a Markdown title')
        for key in ('outcome_mapping','source_ids','review_notes'):
            if not isinstance(artifact[key],list) or any(not isinstance(x,str) for x in artifact[key]): raise ValueError('Invalid artifact metadata')
        if not artifact['review_notes']: raise ValueError('Review notes are required')
        if not set(artifact['source_ids'])<=source_ids: raise ValueError('Artifact cites a source not supplied to the model')
    return result

def api_generate(context, system, model, key, max_tokens):
    # No browsing, business tools, executable functions or alternative destinations.
    payload={'model':model,'instructions':system,'input':context,'store':False,
             'max_output_tokens':max_tokens,'text':{'format':{'type':'json_schema','name':'academy_draft','strict':True,'schema':SCHEMA}}}
    req=urllib.request.Request('https://api.openai.com/v1/responses',data=json.dumps(payload).encode(),method='POST',headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(req,timeout=180) as response: raw=json.load(response)
    except urllib.error.HTTPError as error:
        raise RuntimeError(f'Model service returned HTTP {error.code}; check model access, billing and the selected output format. No retry was made.') from None
    except urllib.error.URLError:
        raise RuntimeError('Cannot reach model service. No automatic retry was made.') from None
    if raw.get('status')!='completed': raise RuntimeError('Model response is incomplete. Reduce scope or increase the configured output budget.')
    text=[]
    for item in raw.get('output',[]):
        for part in item.get('content',[]):
            if part.get('type')=='refusal': raise RuntimeError('The model declined this request; no artifacts were staged.')
            if part.get('type')=='output_text': text.append(part['text'])
    if not text: raise RuntimeError('No structured text was returned')
    return json.loads(''.join(text)),raw.get('usage',{})

def stage(result, request, usage, root=ROOT):
    run_id=dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S')+'-'+uuid.uuid4().hex[:8]
    run=safe_path(root,'drafts/'+run_id,roots={'drafts'})
    run.mkdir(parents=True)
    # Prevalidate all destinations before writes.
    targets=[(a,safe_path(run,a['path'],roots={'curriculum','materials','website','operations'},suffix={'.md'})) for a in result['artifacts']]
    hashes={}
    for artifact,target in targets:
        target.parent.mkdir(parents=True,exist_ok=True); target.write_text(artifact['content'],encoding='utf-8')
        hashes[artifact['path']]=digest(artifact['content'])
    write_json(run/'result.json',result); write_json(run/'request.json',request)
    write_json(run/'run.json',{'run_id':run_id,'created_at':now(),'status':'pending_review','artifact_hashes':hashes,'approved_artifacts':{},'usage':usage})
    review='# Draft Review\n\n'+result['summary']+'\n\n## Assumptions\n\n'+'\n'.join('- '+x for x in result['assumptions'])+'\n\n## Change impact\n\n'+'\n'.join('- '+x for x in result['change_impact'])+'\n\n## Artifacts\n\n'
    for artifact in result['artifacts']:
        review+='### '+artifact['path']+'\n\n'+'\n'.join('- '+x for x in artifact['review_notes'])+'\n\n'
    review+='Check factual correctness, outcome alignment, workload, source support and active cohort impact before approving individual artifacts.\n'
    (run/'REVIEW.md').write_text(review,encoding='utf-8')
    return run_id

def approve(run_id, reviewer, artifacts, root=ROOT):
    if not re.fullmatch(r'\d{8}T\d{6}-[a-f0-9]{8}',run_id): raise ValueError('Invalid run ID')
    if not reviewer.strip() or not artifacts or len(set(artifacts))!=len(artifacts): raise ValueError('Reviewer and distinct selected artifacts are required')
    run=safe_path(root,'drafts/'+run_id,roots={'drafts'}); info=read_json(run/'run.json')
    selected=[]
    for rel in artifacts:
        if rel not in info['artifact_hashes']: raise ValueError('Artifact is not in this run')
        if rel in info['approved_artifacts']: raise ValueError('Artifact was already approved')
        src=safe_path(run,rel,roots={'curriculum','materials','website','operations'},suffix={'.md'})
        content=src.read_text(encoding='utf-8')
        if digest(content)!=info['artifact_hashes'][rel]: raise ValueError('Draft changed after staging; create a new reviewed draft')
        dest=safe_path(root,'approved/'+rel,roots={'approved'},suffix={'.md'})
        backup=safe_path(root,'archive/'+run_id+'/'+rel,roots={'archive'},suffix={'.md'})
        selected.append((rel,content,dest,backup))
    # This local operation is for a single operator; shared production approval requires locking and RBAC.
    for rel,content,dest,backup in selected:
        if dest.exists():
            backup.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(dest,backup)
        dest.parent.mkdir(parents=True,exist_ok=True); temporary=dest.with_name(dest.name+'.tmp')
        temporary.write_text(content,encoding='utf-8'); temporary.replace(dest)
        info['approved_artifacts'][rel]={'reviewer':reviewer,'approved_at':now(),'sha256':digest(content)}
    info['status']='approved' if len(info['approved_artifacts'])==len(info['artifact_hashes']) else 'partially_approved'
    write_json(run/'run.json',info)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    sub.add_parser('doctor',help='Offline catalog and knowledge checks')
    d=sub.add_parser('draft',help='Generate reviewable content; API usage is billable')
    d.add_argument('--request',required=True,type=Path); d.add_argument('--dry-run',action='store_true')
    d.add_argument('--max-output-tokens',type=int,default=6000)
    a=sub.add_parser('approve',help='Copy individually reviewed artifacts to the local approved folder')
    a.add_argument('--run-id',required=True); a.add_argument('--reviewer',required=True)
    a.add_argument('--artifact',action='append',required=True)
    args=parser.parse_args()
    try:
        if args.command=='doctor':
            catalog=validate_catalog(read_json(ROOT/'data/catalog.json'))
            manifest=read_json(ROOT/'knowledge/manifest.json')
            for record in manifest['records']: safe_path(ROOT,record['path'],roots={'knowledge'},suffix={'.md','.txt'}).read_text()
            print(f'Offline checks passed: {len(catalog["programs"])} courses, {sum(len(p["modules"]) for p in catalog["programs"])} modules. Live generation requires OPENAI_API_KEY and WOOPLIX_MODEL.')
        elif args.command=='draft':
            request=read_json(args.request); context,ids=context_for(request)
            if not 500<=args.max_output_tokens<=12000: raise ValueError('Output token budget must be between 500 and 12000')
            if args.dry_run:
                print(f'Request valid. Context characters: {len(context)}. Sources: {", ".join(sorted(ids)) or "none"}. No network request or draft write was made.'); return
            key=os.environ.get('OPENAI_API_KEY'); model=os.environ.get('WOOPLIX_MODEL')
            if not key or not model: raise ValueError('Set OPENAI_API_KEY and WOOPLIX_MODEL in your environment. Never save secrets in this workspace.')
            result,usage=api_generate(context,(ROOT/'agent/system_prompt.md').read_text(),model,key,args.max_output_tokens)
            validate_result(result,ids); run_id=stage(result,request,usage)
            print('Draft staged: '+run_id+'\nReview drafts/'+run_id+'/REVIEW.md and each artifact before approving.')
        else:
            approve(args.run_id,args.reviewer,args.artifact)
            print('Selected reviewed artifacts copied to approved. Catalog, handbook, website and LMS were not changed.')
    except (ValueError,KeyError,OSError,RuntimeError,json.JSONDecodeError) as error:
        print('Error: '+str(error),file=sys.stderr); sys.exit(1)

if __name__=='__main__': main()
