from pathlib import Path
import json,re,sys
root=Path(__file__).resolve().parents[1]
required=['index.html','config.js','report.schema.json','assets/app.v024.js','assets/site.v024.css','assets/openglesscope_logo_horizontal-v017.png','assets/favicon-v017.png','assets/favicon-v017.ico','assets/apple-touch-icon-v017.png','worker/src/index.js','worker/migrations/0002_report_cursor_index.sql','worker/migrations/0003_application_version_summary.sql','rules/PROJECT_RULES.md']
errors=[]
for x in required:
    if not (root/x).is_file(): errors.append(f'missing {x}')
for x in ['report.schema.json','worker/package.json']:
    try: json.loads((root/x).read_text(encoding='utf-8'))
    except Exception as e: errors.append(f'json {x}: {e}')
try: json.loads(re.sub(r'(?m)^\s*//.*$','',(root/'worker/wrangler.jsonc').read_text(encoding='utf-8')))
except Exception as e: errors.append(f'jsonc worker/wrangler.jsonc: {e}')
for f in root.glob('*.html'):
    text=f.read_text(encoding='utf-8')
    if 'Content-Security-Policy' not in text: errors.append(f'csp {f.name}')
    for ref in re.findall(r'(?:src|href)="([^"]+)"',text):
        if ref.startswith(('http://','https://','#')): continue
        target=(f.parent/ref.split('?',1)[0]).resolve()
        try: target.relative_to(root.resolve())
        except ValueError: errors.append(f'outside-ref {f.name} {ref}');continue
        if not target.exists(): errors.append(f'broken-ref {f.name} {ref}')
for f in [root/'assets/app.v024.js',root/'assets/site.v024.css',root/'worker/src/index.js',root/'tools/build_index.py']:
    t=f.read_text(encoding='utf-8')
    bad='/*' in t or re.search(r'(?m)^\s*//',t)
    if f.suffix=='.py': bad=bool(bad or re.search(r'(?m)^\s*#(?!\!)',t))
    if bad: errors.append(f'source-comment {f.relative_to(root)}')
idx=(root/'index.html').read_text(encoding='utf-8')
for ref in ['assets/app.js','assets/site.css','assets/openglesscope_logo_horizontal.png','assets/favicon.png','v015','app.v023.js','site.v023.css']:
    if ref in idx: errors.append(f'stale-or-unversioned-index-ref {ref}')
for token in ['displayOrderFilter','nav-edge-left','nav-edge-right','repo-icon','repo-arrow','OpenGLESScope Database <strong>0.1.14</strong>']:
    if token not in idx: errors.append(f'missing-ui-token {token}')
worker=(root/'worker/src/index.js').read_text(encoding='utf-8')
for token in ["databaseVersion:'0.1.14'","normalizerVersion:3",'application_version','application_version_code','MAX_BODY=2*1024*1024']:
    if token not in worker: errors.append(f'missing-worker-token {token}')
if errors:
    print('\n'.join(errors));sys.exit(1)
print('OpenGLESScope Database audit PASS')
