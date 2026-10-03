from pathlib import Path
import argparse
import shutil
import sys
from datetime import datetime

root=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
g=parser.add_mutually_exclusive_group(required=True)
g.add_argument('--apply',action='store_true')
g.add_argument('--check',action='store_true')
args=parser.parse_args()
current_assets={
    'app':'app.v3027.js',
    'site':'site.v3027.css',
    'browser-compat':'browser-compat.v3027.js',
    'experience':'experience.v3027.js',
    'release-bootstrap':'release-bootstrap.v3027.js',
    'scroll-system':'scroll-system.v3027.js'
}
workflow_template=(root/'tools/pages.workflow.yml').read_text(encoding='utf-8')
issues=[]
for stem,current in current_assets.items():
    suffix='css' if stem=='site' else 'js'
    for p in (root/'assets').glob(f'{stem}.v*.{suffix}'):
        if p.name!=current: issues.append(p)
workflow_dir=root/'.github/workflows'
for p in workflow_dir.glob('*'):
    if p.is_file() and p.name!='pages.yml': issues.append(p)
pages=workflow_dir/'pages.yml'
workflow_wrong=not pages.is_file() or pages.read_text(encoding='utf-8')!=workflow_template
manifest_path=root/'files.txt'
manifest=set(manifest_path.read_text(encoding='utf-8').splitlines()) if manifest_path.is_file() else set()
stale_tool_sources=[p for p in (root/'tools').glob('*.py') if p.relative_to(root).as_posix() not in manifest]
transient=[]
for name in ['node_modules','.wrangler','__pycache__','.gradle','build','.idea']:
    transient.extend(p for p in root.rglob(name) if p.is_dir())
for rel in ['README.md','release.md']:
    p=root/rel
    if p.exists(): transient.append(p)
if args.apply:
    if stale_tool_sources:
        quarantine=root.parent/('OpenGLESScope_database_3.0.27_stale_tools_'+datetime.now().strftime('%Y%m%d_%H%M%S'))
        for p in stale_tool_sources:
            dest=quarantine/p.relative_to(root)
            dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.move(str(p),str(dest))
            print('QUARANTINED obsolete source:',p.relative_to(root))
    for p in issues:
        if p.is_dir(): shutil.rmtree(p)
        else: p.unlink(missing_ok=True)
    for p in sorted(set(transient),key=lambda x:len(x.parts),reverse=True):
        if p.is_dir(): shutil.rmtree(p,ignore_errors=True)
        else: p.unlink(missing_ok=True)
    workflow_dir.mkdir(parents=True,exist_ok=True)
    pages.write_bytes((root/'tools/pages.workflow.yml').read_bytes())
    print('OpenGLESScope Database 3.0.27 repository repair: APPLIED')
    sys.exit(0)
if issues or workflow_wrong or transient or stale_tool_sources:
    print('OpenGLESScope Database 3.0.27 repository repair: CHANGES REQUIRED')
    for p in issues: print(p.relative_to(root))
    for p in stale_tool_sources: print(p.relative_to(root))
    for p in transient: print(p.relative_to(root))
    if workflow_wrong: print('.github/workflows/pages.yml')
    sys.exit(1)
print('OpenGLESScope Database 3.0.27 repository repair: CLEAN')
