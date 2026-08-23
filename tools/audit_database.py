from pathlib import Path
import json,re,subprocess,sys,shutil
root=Path(__file__).resolve().parents[1]
errors=[]
required=['index.html','config.js','report.schema.json','assets/app.v041.js','assets/site.v036.css','assets/egl-logo-white-v029.png','assets/opengles-gl-es-v028.png','assets/openglesscope_logo_horizontal-v017.png','assets/favicon-v017.png','assets/favicon-v017.ico','assets/apple-touch-icon-v017.png','worker/src/index.js','worker/tests/contract.mjs','worker/migrations/0001_init.sql','worker/migrations/0002_report_cursor_index.sql','worker/migrations/0003_application_version_summary.sql','worker/scripts/verify-cloudflare-account.mjs','worker/wrangler.jsonc','worker/package.json','rules/PROJECT_RULES.md','rules/0.1.20_RESPONSIVE_TABLE_AUDIT.md','rules/0.1.21_FULL_PARITY_SECURITY_SPEC_AUDIT.md','rules/0.1.22_FULL_PRODUCER_TAB_PARITY_AUDIT.md','rules/0.1.23_REPORTS_TABLE_PARITY_AUDIT.md','rules/0.1.24_UI_PARITY_FIX_AUDIT.md','rules/0.1.25_REPORT_VENDOR_TABLE_SCROLL_PARITY_AUDIT.md','rules/0.1.26_FULL_UI_SECURITY_SPEC_AUDIT.md','rules/0.2.0_FULL_DATABASE_COMPATIBILITY_SECURITY_SPEC_AUDIT.md','rules/0.2.2_ANDROID_SECURITY_PATCH_END_TO_END_AUDIT.md','rules/0.2.4_TECHNICAL_COMPARE_FILTER_AUDIT.md','rules/0.2.5_OPENGLESSCOPE_0.3.2_COMPATIBILITY_AUDIT.md','rules/0.2.7_OPENGLESSCOPE_0.3.3_FULL_DATABASE_AUDIT.md','SECURITY.md','README.md','release.md','BUILD_AUDIT.md','.github/workflows/pages.yml']
for x in required:
    if not (root/x).is_file(): errors.append(f'missing {x}')
for x in ['report.schema.json','worker/package.json','data/index.json']:
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
source_files=[root/'assets/app.v041.js',root/'assets/site.v036.css',root/'worker/src/index.js',root/'worker/tests/contract.mjs',root/'worker/scripts/verify-cloudflare-account.mjs',root/'tools/build_index.py',root/'tools/audit_database.py']
for f in source_files:
    t=f.read_text(encoding='utf-8')
    block='/'+'*'
    bad=block in t or bool(re.search(r'(?m)^\s*//',t))
    if f.suffix=='.py': bad=bool(bad or re.search(r'(?m)^\s*#(?!\!)',t))
    if bad: errors.append(f'source-comment {f.relative_to(root)}')
idx=(root/'index.html').read_text(encoding='utf-8')
for token in ['assets/site.v036.css','assets/app.v041.js','config.js?v=040','OpenGLESScope Database <strong>0.2.7</strong>','displayOrderFilter','nav-edge-left','nav-edge-right','repo-icon','repo-arrow']:
    if token not in idx: errors.append(f'missing-index-token {token}')
for token in ['assets/app.js','assets/site.css','app.v035.js" defer','config.js?v=035','OpenGLESScope Database <strong>0.1.25</strong>']:
    if token in idx: errors.append(f'stale-index-token {token}')
for f in root.glob('*.html'):
    if f.name!='index.html' and 'assets/site.v036.css' not in f.read_text(encoding='utf-8'): errors.append(f'error-css {f.name}')
worker=(root/'worker/src/index.js').read_text(encoding='utf-8')
worker_tokens=["DATABASE_VERSION='0.2.7'","NORMALIZER_VERSION=9","compatibleProducer:'OpenGLESScope 0.1.17+ within 0.x schema 2 / technical report 1'","currentProducer:'OpenGLESScope 0.3.3'","publishedOpenGlesSpec:'OpenGL ES 3.2 (May 5, 2022)'","publishedGlslEsSpec:'GLSL ES 3.20 (August 14, 2023)'","publishedEglSpec:'EGL 1.5 (August 27, 2014)'","registryAuditDate:'2026-08-24'",'MAX_BODY=2*1024*1024','replace(/[^a-z0-9]/g','const TOP_KEYS=new Set','const DIAGNOSTIC_STATES=new Set','sameDisplay(t.display,p.display)',"text.startsWith('OpenGLESScope report\\n')","text.startsWith(`OpenGLESScope ${p.application.version}\\n`)",'runtimeMetadata=p=>','securityPatch','Android security patch','Security patch','Application ABI','Supported device ABIs','text.length<1000','currentProducerEvidence=p=>','unique(t.limits','unique(t.queryDiagnostics','enumerationEvidenceValid','GL_TIME_ELAPSED_EXT_QUERY_COUNTER_BITS','GL_TIMESTAMP_EXT_QUERY_COUNTER_BITS','GL_MAX_DEBUG_MESSAGE_LENGTH','dm.get(x.name)?.status!==\'Available\'','countHeader(text,label,count)','preflight=(origin)=>','content-security-policy','Submission JSON nesting is too deep','Content-Type must be application/json','Stored report payload is invalid','Both cursor fields are required','Method not allowed']
for token in worker_tokens:
    if token not in worker: errors.append(f'missing-worker-token {token}')
for token in ['producerVersion=p=>','producerAtLeast=(p,minor,patch)=>','supportedProducer=p=>','luminanceTextMatches=(text,label,value)=>','Unsupported OpenGLESScope producer version','current producer versionCode mismatch']:
    if token not in worker and token!='current producer versionCode mismatch': errors.append(f'missing-0.2-worker-token {token}')
for token in ["p.application.version==='0.3.3'&&p.application.versionCode!==303","`Core version: ${p.opengles.major}.${p.opengles.minor}`","reportLine(text,'Core version provenance')",'Direct GL_MAJOR_VERSION / GL_MINOR_VERSION query','Parsed from GL_VERSION runtime string']:
    if token not in worker: errors.append(f'missing-0.2.7-worker-token {token}')

js=(root/'assets/app.v041.js').read_text(encoding='utf-8')
js_tokens=['updateTableScroller','enhanceTableScroller','thumb.style.width','thumb.style.transform','role="scrollbar"','aria-valuenow','setPointerCapture','ArrowLeft','ArrowRight','table-edge-left','table-edge-right','egl-logo-white-v029.png','opengles-gl-es-v028.png','failedReportLoads','Report load failures','reportSearchText','runtimeMeta','reportPlatform','reportSupportedAbis','reportOs','securityPatch','Patch ${esc(runtimeMeta(p).securityPatch)}','Application ABI','Supported device ABIs','Platform / ABI',"table(['Submitted','Device','Logo','Vendor','Driver','OpenGL ES','EGL','Android','OpenGLESScope','Platform / ABI','Report ID']",'state.details.get(r.id)',"['driver-asc','Driver — A to Z']",'Repeated report cursor','Response exceeds 4 MiB','Database request timed out','aria-busy','detailTransitionToken','prefersReducedMotion()?',"display:[['available','HDR available'],['unavailable','HDR unavailable'],['unknown','HDR unknown']]",'diagnosticIndex','enumEvidence','LIMIT_DIAGNOSTIC_EXCLUSIONS','isLimitDiagnosticName','isPrecisionDiagnosticName','Enumeration query evidence','Not listed','Compressed texture','shaderBinaryFormats','programBinaryFormats','available values','State coverage','detail-metrics','Extensions (${n.extensions.length+n.eglExtensions.length+n.eglClientExtensions.length})','Limits (${n.limits.length})','Formats (${n.compressedFormats.length+n.shaderBinaryFormats.length+n.programBinaryFormats.length})','Precision (${n.precision.length})','EGL Configs (${n.eglConfigs.length})','Diagnostics (${n.diagnostics.length})','Modes','Min luminance','Avg luminance','Max luminance','coverage-progress','value(d.desiredMaxLuminance,\' cd/m²\')','value(d.desiredMaxAverageLuminance,\' cd/m²\')','value(d.desiredMinLuminance,\' cd/m²\')']
for token in ['glEglVersionChip','class=\"gl-egl-version-chip mono\"','class=\"report-id-cell\"','Device','OpenGL ES','EGL']:
    if token not in js: errors.append(f'missing-reports-parity-token {token}')
for token in js_tokens:
    if token not in js: errors.append(f'missing-frontend-token {token}')
for token in ['./data/index.json','state.summaries=staticIndex',"fetch('./data/index.json",'eval(', 'new Function', 'document.write(', 'javascript:','style="']:
    if token in js: errors.append(f'forbidden-frontend-token {token}')
css=(root/'assets/site.v036.css').read_text(encoding='utf-8')
if '\\n' in css: errors.append('literal-escaped-newline-css')
for token in ['th,td{text-align:left;vertical-align:top;padding:10px 12px;border-bottom:1px solid #28282c}','th{position:sticky;top:0;background:#151518;color:#cbcad0;font-size:12px;font-weight:700;line-height:1.35;z-index:2}']:
    if token not in css: errors.append(f'global-table-parity {token}')
for token in ['.table-edge{','.table-edge.visible{','.table-scroll-shell.scrollable .table-scroll-controls{','.table-scroll-track:focus-visible{','.table-scroll-thumb{','.coverage-progress{','.query-evidence{','.detail-metrics{','.reports-table th{','.gl-egl-version-chip{','.report-id-cell{','@media(prefers-reduced-motion:reduce)']:
    if token not in css: errors.append(f'missing-style-token {token}')
schema=json.loads((root/'report.schema.json').read_text(encoding='utf-8'))
sp=schema.get('properties',{})
app_props=sp.get('application',{}).get('properties',{})
if app_props.get('versionCode',{}).get('minimum')!=117: errors.append('schema-version-floor')
if app_props.get('version',{}).get('pattern')!=r'^0\.(?:1\.(?:1[7-9]|[2-9][0-9]|[1-9][0-9]{2,})|(?:[2-9]|[1-9][0-9]+)\.[0-9]+)$': errors.append('schema-version-pattern')
tr=sp.get('technicalReport',{}).get('properties',{})
if tr.get('limits',{}).get('maxItems')!=8192: errors.append('schema-limit-bound')
if tr.get('queryDiagnostics',{}).get('maxItems')!=16384: errors.append('schema-diagnostic-bound')
if set(tr.get('queryDiagnostics',{}).get('items',{}).get('properties',{}).get('status',{}).get('enum',[]))!={'Available','Unavailable','Not applicable','Unknown'}: errors.append('schema-diagnostic-states')
dev=sp.get('device',{});security_patch=dev.get('properties',{}).get('securityPatch',{});
if security_patch.get('pattern')!=r'^\d{4}-\d{2}-\d{2}$' or 'securityPatch' in dev.get('required',[]): errors.append('schema-security-patch-optional')
wr=json.loads((root/'worker/wrangler.jsonc').read_text(encoding='utf-8'))
if wr.get('compatibility_date')!='2026-08-23': errors.append('worker-compatibility-date')
if wr.get('account_id')!='6881527e6e0b9bc4a0c009473428d1bc': errors.append('cloudflare-account-pin')
dbs=wr.get('d1_databases',[])
if not dbs or dbs[0].get('binding')!='DB' or dbs[0].get('database_id')!='2c945dda-e320-4b3a-9fac-a086373db17c': errors.append('d1-pin')
pkg=json.loads((root/'worker/package.json').read_text(encoding='utf-8'))
if pkg.get('version')!='0.2.7': errors.append('worker-package-version')
if pkg.get('devDependencies',{}).get('wrangler')!='4.124.0': errors.append('wrangler-pin')
for key in ['predeploy','premigrate','premigrations:list','pred1:count']:
    if 'verify:account' not in pkg.get('scripts',{}).get(key,''): errors.append(f'account-guard {key}')
static=json.loads((root/'data/index.json').read_text(encoding='utf-8'))
for key,val in [('databaseVersion','0.2.7'),('normalizerVersion',9),('currentProducer','OpenGLESScope 0.3.3')]:
    if static.get(key)!=val: errors.append(f'static-index-{key}')

for token in ['Technical differences only','technicalCompareEntry','Application/Version','Application/Version code','Collection/Status','Collection/Complete','Collection/Source']:
    if token not in js: errors.append(f'technical-compare {token}')
for token in ['function compareCell(x)','showStatus','diagStatus','wideColor','hdrTypes','Not reported']:
    if token not in js: errors.append(f'compare-semantic-state {token}')
if "${esc(x?.value??'Unknown')} ${x?badge(x.status,x.status)" in js: errors.append('compare-redundant-badge-renderer')
workflow=(root/'.github/workflows/pages.yml').read_text(encoding='utf-8')
for token in ['actions/checkout@v6','actions/setup-python@v6','python tools/build_index.py','python tools/audit_database.py','node --check assets/app.v041.js','node --check worker/src/index.js','node worker/tests/contract.mjs','actions/configure-pages@v5','actions/upload-pages-artifact@v4','actions/deploy-pages@v4','cancel-in-progress: false']:
    if token not in workflow: errors.append(f'workflow-quality {token}')
node=shutil.which('node')
if node:
    for f in [root/'assets/app.v041.js',root/'worker/src/index.js',root/'worker/tests/contract.mjs']:
        r=subprocess.run([node,'--check',str(f)],capture_output=True,text=True)
        if r.returncode: errors.append(f'node-check {f.relative_to(root)}: {r.stderr.strip()}')
    r=subprocess.run([node,str(root/'worker/tests/contract.mjs')],capture_output=True,text=True,cwd=root/'worker')
    if r.returncode: errors.append(f'worker-contract: {r.stdout.strip()} {r.stderr.strip()}')
if errors:
    print('\n'.join(errors));sys.exit(1)
print('OpenGLESScope Database 0.2.7 audit PASS')
