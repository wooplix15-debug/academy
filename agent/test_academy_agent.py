import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

spec=importlib.util.spec_from_file_location('academy_agent',Path(__file__).with_name('academy_agent.py'))
agent=importlib.util.module_from_spec(spec); spec.loader.exec_module(agent)

def result(path='materials/test_lesson.md'):
    return {'summary':'Synthetic test draft','assumptions':[],'review_required':True,'change_impact':[],
            'artifacts':[{'path':path,'content':'# Test Lesson\n\nSynthetic content.\n','outcome_mapping':['ZIM-M01'],'source_ids':['S02'],'review_notes':['Review source support.']}]}

class AgentTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.root=Path(self.temp.name)
        for folder in ('data','knowledge','materials','drafts','approved','archive'): (self.root/folder).mkdir()
        shutil.copy2(agent.ROOT/'data/catalog.json',self.root/'data/catalog.json')
        (self.root/'knowledge/note.md').write_text('# Verified reference\n')
        (self.root/'knowledge/manifest.json').write_text(json.dumps({'records':[{'id':'S02','status':'verified_public_reference','permission':'public','version':'1','path':'knowledge/note.md'},{'id':'PRIVATE','status':'approved','permission':'client_only','version':'1','path':'knowledge/note.md'}]}))
        self.request={'mode':'lesson','course_id':'ZIM','module_id':'ZIM-M01','source_ids':['S02'],'instructions':'Create an example'}
    def tearDown(self): self.temp.cleanup()
    def test_catalog_totals_and_weights(self):
        catalog=agent.validate_catalog(json.loads((self.root/'data/catalog.json').read_text()))
        self.assertEqual(len(catalog['programs']),4)
        catalog['programs'][0]['total_hours']+=1
        with self.assertRaises(ValueError): agent.validate_catalog(catalog)
    def test_prerequisite_order(self):
        catalog=json.loads((self.root/'data/catalog.json').read_text())
        catalog['programs'][0]['modules'][0]['depends_on']=['ZIM-M10']
        with self.assertRaises(ValueError): agent.validate_catalog(catalog)
    def test_selected_context(self):
        text,ids=agent.context_for(self.request,self.root)
        self.assertEqual(ids,{'S02'}); self.assertEqual(len(json.loads(text)['programs']),1)
    def test_restricted_source_blocked_before_model(self):
        request=dict(self.request,source_ids=['PRIVATE'])
        with self.assertRaises(ValueError): agent.context_for(request,self.root)
    def test_wrong_module_rejected(self):
        with self.assertRaises(ValueError): agent.context_for(dict(self.request,module_id='AAB-M01'),self.root)
    def test_traversal_and_disallowed_extension(self):
        for path in ('../escape.md','materials/../../escape.md','/tmp/escape.md','materials/tool.py','data/catalog.json','materials//file.md'):
            with self.subTest(path=path), self.assertRaises(ValueError): agent.validate_result(result(path),{'S02'})
    def test_symlink_rejected(self):
        (self.root/'materials/link').symlink_to(self.root/'knowledge',target_is_directory=True)
        with self.assertRaises(ValueError): agent.safe_path(self.root,'materials/link/file.md',roots={'materials'},suffix={'.md'})
    def test_unprovided_citation_rejected(self):
        data=result(); data['artifacts'][0]['source_ids']=['MADE_UP']
        with self.assertRaises(ValueError): agent.validate_result(data,{'S02'})
    def test_review_flag_required(self):
        data=result(); data['review_required']=False
        with self.assertRaises(ValueError): agent.validate_result(data,{'S02'})
    def test_duplicate_output_rejected(self):
        data=result(); data['artifacts'].append(dict(data['artifacts'][0]))
        with self.assertRaises(ValueError): agent.validate_result(data,{'S02'})
    def test_stage_and_selected_approval(self):
        data=result(); data['artifacts'].append(dict(data['artifacts'][0],path='materials/second.md'))
        run=agent.stage(data,self.request,{},self.root)
        agent.approve(run,'Test reviewer',['materials/test_lesson.md'],self.root)
        self.assertTrue((self.root/'approved/materials/test_lesson.md').exists())
        self.assertFalse((self.root/'approved/materials/second.md').exists())
        info=json.loads((self.root/f'drafts/{run}/run.json').read_text())
        self.assertEqual(info['status'],'partially_approved')
        with self.assertRaises(ValueError): agent.approve(run,'Test reviewer',['materials/test_lesson.md'],self.root)
    def test_edited_draft_rejected(self):
        run=agent.stage(result(),self.request,{},self.root)
        (self.root/f'drafts/{run}/materials/test_lesson.md').write_text('# Edited\n')
        with self.assertRaises(ValueError): agent.approve(run,'Test reviewer',['materials/test_lesson.md'],self.root)
    def test_approved_overwrite_has_backup(self):
        first=agent.stage(result(),self.request,{},self.root); agent.approve(first,'Reviewer',['materials/test_lesson.md'],self.root)
        data=result(); data['artifacts'][0]['content']='# New Lesson\n'
        second=agent.stage(data,self.request,{},self.root); agent.approve(second,'Reviewer',['materials/test_lesson.md'],self.root)
        self.assertEqual((self.root/f'archive/{second}/materials/test_lesson.md').read_text(),'# Test Lesson\n\nSynthetic content.\n')
    def test_api_payload_and_response(self):
        class MockResponse:
            def __enter__(self): return self
            def __exit__(self,*args): return False
            def read(self): return json.dumps({'status':'completed','output':[{'content':[{'type':'output_text','text':json.dumps(result())}]}],'usage':{'total_tokens':100}}).encode()
        with patch.object(agent.urllib.request,'urlopen',return_value=MockResponse()) as call:
            data,usage=agent.api_generate('{}','system','test-model','test-key',6000)
            payload=json.loads(call.call_args.args[0].data)
            self.assertFalse(payload['store']); self.assertNotIn('tools',payload)
            self.assertEqual(payload['text']['format']['type'],'json_schema')
            self.assertEqual(data['summary'],'Synthetic test draft')
    def test_incomplete_api_response_rejected(self):
        class MockResponse:
            def __enter__(self): return self
            def __exit__(self,*args): return False
            def read(self): return b'{"status":"incomplete","output":[]}'
        with patch.object(agent.urllib.request,'urlopen',return_value=MockResponse()), self.assertRaises(RuntimeError):
            agent.api_generate('{}','system','test-model','test-key',6000)

if __name__=='__main__': unittest.main(verbosity=2)
