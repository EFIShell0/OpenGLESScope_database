from pathlib import Path
import argparse
import shutil
import sys

root=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
g=parser.add_mutually_exclusive_group(required=True)
g.add_argument('--apply',action='store_true')
g.add_argument('--check',action='store_true')
args=parser.parse_args()
current_app='app.v070.js'
current_css='site.v070.css'
workflow_template=(root/'tools/pages.workflow.yml').read_text(encoding='utf-8')
issues=[]
for p in (root/'assets').glob('app.v*.js'):
    if p.name!=current_app: issues.append(p)
for p in (root/'assets').glob('site.v*.css'):
    if p.name!=current_css: issues.append(p)
workflow_dir=root/'.github/workflows'
for p in workflow_dir.glob('*'):
    if p.is_file() and p.name!='pages.yml': issues.append(p)
pages=workflow_dir/'pages.yml'
workflow_wrong=not pages.is_file() or pages.read_text(encoding='utf-8')!=workflow_template
if args.apply:
    for p in issues: p.unlink(missing_ok=True)
    workflow_dir.mkdir(parents=True,exist_ok=True)
    pages.write_text(workflow_template,encoding='utf-8')
    for name in ['__pycache__']:
        for p in root.rglob(name):
            if p.is_dir(): shutil.rmtree(p)
    print('OpenGLESScope Database 0.7.0 repository repair: APPLIED')
    sys.exit(0)
if issues or workflow_wrong:
    print('OpenGLESScope Database 0.7.0 repository repair: CHANGES REQUIRED')
    for p in issues: print(p.relative_to(root))
    if workflow_wrong: print('.github/workflows/pages.yml')
    sys.exit(1)
print('OpenGLESScope Database 0.7.0 repository repair: CLEAN')
