import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

root=Path(__file__).resolve().parents[1]
required=['data/registry-catalog.v2000.json','tools/verify_1_1_0_rules.py','tools/test_live_index.py','tools/verify_published_snapshot.py','rules/PROJECT_RULES.md','rules/VULKANSCOPE_DATABASE_1.4.12_PROJECT_RULES_REFERENCE.md','rules/vulkanscope_database_1_4_12_rule_applicability.json','assets/app.v3002.js','assets/site.v3002.css','index.html','worker/src/index.js','.github/workflows/pages.yml','tools/pages.workflow.yml']
mutations=[
 ('alter immutable reference','rules/VULKANSCOPE_DATABASE_1.4.12_PROJECT_RULES_REFERENCE.md',lambda s:s+'\nunauthorized reference mutation\n'),
 ('drop Vulkan methodology heading','rules/vulkanscope_database_1_4_12_rule_applicability.json',lambda s:s.replace('"headingCount": 116','"headingCount": 115',1)),
 ('alter locked GL/EGL catalog count','data/registry-catalog.v2000.json',lambda s:s.replace('\"entries\":5261','\"entries\":5260',1)),
 ('remove live sync path','worker/src/index.js',lambda s:s.replace("'/v1/sync'","'/v1/not-synced'")),
 ('remove live accessibility announcement','index.html',lambda s:s.replace('aria-live="polite" id="liveStatus" role="status"','aria-live="off" id="liveStatus" role="status"',1)),
 ('remove publication verification','tools/pages.workflow.yml',lambda s:s.replace('python tools/verify_published_snapshot.py','python tools/not_verified.py',1))
]
with tempfile.TemporaryDirectory(prefix='gl1100-mutations-') as base:
    tmp=Path(base)
    for file in required:
        dst=tmp/file
        dst.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(root/file,dst)
    command=[sys.executable,'-B',str(tmp/'tools/verify_1_1_0_rules.py')]
    good=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    assert good.returncode==0,good.stdout+good.stderr
    for label,rel,mutate in mutations:
        item=tmp/rel
        original=item.read_text(encoding='utf-8')
        changed=mutate(original)
        assert changed!=original,label
        item.write_text(changed,encoding='utf-8')
        r=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        assert r.returncode!=0,'Negative mutation escaped verifier: '+label
        item.write_text(original,encoding='utf-8')
    print('OpenGLESScope Database 3.0.2 immutable rules/Worker/UI/publication negative mutations: ALL PASS')
