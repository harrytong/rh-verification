import json
from pathlib import Path
import tempfile
import subprocess
import sys
import unittest
from unittest.mock import patch
from test_driver import a,HERE

class SearchTests(unittest.TestCase):
    def text(self,rows):return '\n'.join('RH_STAGE3_SEARCH_JSON\t'+json.dumps(r) for r in rows)
    def row(self):
        return dict(event='search',target='A',binder='h',ordinal=0,status='found',path='root/app.arg',
          application=dict(application_path='root',function=dict(head_kind='constant',head='B',preceding_arguments=2,spine_truncated=False),
                           occurrence_branch='argument',selected_child_is_bvar=True),
          visited=2,node_limit=100000,depth_limit=600,omitted_annotation_roots=0,truncated=False)
    expected=[dict(target='A',binder='h')]
    def test_positive_application_context_is_not_necessity(self):
        r=a.validate_searches(self.text([self.row()]),self.expected)
        self.assertEqual(r['records'][0]['application']['function']['head'],'B')
        self.assertIn('necessity',r['not_established'])
        self.assertIn('hypothesis discharge',r['not_established'])
    def test_omitted_and_truncated_negative_never_claim_absence(self):
        for trunc in [False,True]:
            row=self.row();row.update(status='not-found-in-projection',path='',application=None,
                                      omitted_annotation_roots=1,truncated=trunc)
            r=a.validate_searches(self.text([row]),self.expected)
            self.assertIn('full-body absence',r['not_established'])
            self.assertEqual(r['any_search_truncated'],trunc)
    def test_found_with_prior_truncation_keeps_both(self):
        row=self.row();row['truncated']=True
        r=a.validate_searches(self.text([row]),self.expected)
        self.assertTrue(r['any_search_truncated']);self.assertEqual(r['records'][0]['status'],'found')
    def test_malformed_missing_duplicate_and_wrong_budget_rejected(self):
        good=self.row();badrows=[]
        for key,value in [('ordinal',256),('node_limit',2),('visited',100001),('depth_limit',2),
                          ('path',''),('truncated',0),('binder','other'),('omitted_annotation_roots',3)]:
            bad=json.loads(json.dumps(good));bad[key]=value;badrows.append([bad])
        bad=json.loads(json.dumps(good));bad['application']['function']['preceding_arguments']=True;badrows.append([bad])
        for rows in badrows+[[],[good,good],[dict(event='fixture',case='x',passed=True)]]:
            with self.assertRaises(RuntimeError):a.validate_searches(self.text(rows),self.expected)
        with self.assertRaises(RuntimeError):a.search_records('RH_STAGE3_SEARCH_JSON\t{')
    def fixture_rows(self):
        row=self.row();row.update(target='RHStage3SearchFixture.identity',path='root',application=None,visited=1)
        return [dict(event='fixture',case=c,passed=True) for c in a.SEARCH_CASES]+[row]
    def test_fixture_requires_all_cases_and_real_binder_result(self):
        good=self.fixture_rows()
        self.assertEqual(len(a.validate_search_fixture(self.text(good))['checks']),13)
        for rows in [good[1:],good[:-1],good+[good[-1]]]:
            with self.assertRaises(RuntimeError):a.validate_search_fixture(self.text(rows))
        bad=json.loads(json.dumps(good));bad[-1]['ordinal']=1
        with self.assertRaises(RuntimeError):a.validate_search_fixture(self.text(bad))
    def test_helpers_shared_bytewise_and_frozen_targets(self):
        for h in ['TargetSearchHelpers.lean.txt','ProvenanceHelpers.lean.txt']:
            source=(HERE/h).read_text()
            for filename in ['TargetSearchFixture.lean','Providers.lean']:
                self.assertEqual((HERE/filename).read_text().count(source),1)
        self.assertNotIn('import Main',(HERE/'TargetSearchFixture.lean').read_text())
        cfg=json.loads((HERE/'provider-targets.json').read_text());body=(HERE/'Providers.lean').read_text()
        self.assertEqual(len(cfg['targets']),8);self.assertEqual(len(cfg['searches']),5)
        self.assertEqual(cfg['targets'],json.loads((HERE/'chain-targets.json').read_text())['providers'])
        for r in cfg['searches']:
            self.assertIn('RHStage3Search.inspect env "'+r['target']+'" "'+r['binder']+'"',body)
    def test_search_fixture_failure_blocks_project_and_archives(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);project=p/'project';tc=p/'tc';out=p/'out'
            for x in [project,tc,out]:x.mkdir()
            calls=[]
            def logged(argv,logfile,cidfile,seconds):
                calls.append(logfile.stem)
                if logfile.stem=='positive':return 0,'RH_STAGE3_CONTEXT FIXTURE RH_STAGE3_POSITIVE_FIXTURE_END'
                if logfile.stem=='negative':return 1,'/audit/NegativeFixture.lean:1:0: error: Type mismatch'
                if logfile.stem=='provenance-fixture':return 0,'RH_STAGE3_PROVENANCE_FIXTURE_END'
                if logfile.stem=='search-fixture':return 0,'RH_STAGE3_SEARCH_FIXTURE_END'
                raise AssertionError('project must not start')
            args=['audit_stage3.py','--phase','providers','--project',str(project),'--toolchain',str(tc)]
            with patch.object(sys,'argv',args),patch.object(a,'package_files',return_value=[]),\
                patch.object(a,'validate',return_value={}),patch.object(a,'new_output',return_value=out),\
                patch.object(a,'check_resources',return_value={}),patch.object(a.subprocess,'run'),\
                patch.object(a,'command',return_value='sha256:test'),patch.object(a,'run_logged',side_effect=logged),\
                patch.object(a,'validate_provenance_fixture',return_value={}):
                self.assertEqual(a.main(),1)
            self.assertEqual(calls,['positive','negative','provenance-fixture','search-fixture'])
            self.assertTrue((out/'stage3-evidence.zip').is_file())
    def test_provider_source_priority_beats_alphabetical_cap(self):
        with tempfile.TemporaryDirectory() as d:
            project=Path(d)/'project';out=Path(d)/'out';out.mkdir()
            (project/'src/Development').mkdir(parents=True)
            for n in ['Owner','AUnrelated','ZClassSumPin']:(project/'src/Development'/f'{n}.lean').write_text('-- '+n+'\n')
            refs=[dict(name=n,module='Development.'+n,found=True) for n in ['AUnrelated','ZClassSumPin']]
            result=dict(records=[dict(event='target',module='Development.Owner'),dict(event='references',references=refs)],any_reference_truncated=False)
            cfg=dict(priority_module_fragments=['ClassSumPin'],source_import_depth=0,max_source_files=2,max_source_file_bytes=100,max_source_total_bytes=300)
            def git(args,**kw):return subprocess.CompletedProcess(args,0,(project/'src'/args[-1].split(':src/',1)[1]).read_bytes(),b'')
            with patch.object(a.subprocess,'run',side_effect=git):r=a.collect_provenance_sources(project,out,result,cfg)
            self.assertEqual([x['source'] for x in r['files']],['src/Development/Owner.lean','src/Development/ZClassSumPin.lean','src/Development/AUnrelated.lean'])
            self.assertEqual(r['files'][-1]['status'],'file-count-cap')

if __name__=='__main__':unittest.main()
