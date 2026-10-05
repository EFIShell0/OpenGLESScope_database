from pathlib import Path
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from urllib.parse import urlsplit

parser=argparse.ArgumentParser(description='Audit OpenGLESScope Database source or staged Pages artifact')
parser.add_argument('--source-tree',type=Path)
parser.add_argument('--artifact-tree',type=Path)
parser.add_argument('--require-preload',action='store_true',help='Refuse to publish Pages without an exhaustive verified report cache')
parser.add_argument('--version',action='store_true')
args=parser.parse_args()
AUDIT_VERSION='3.0.30'
print(f'OpenGLESScope Database audit tool {AUDIT_VERSION}')
if args.version: sys.exit(0)

public_files={'.nojekyll','index.html','config.js','report.schema.json','400.html','401.html','403.html','404.html','405.html','408.html','409.html','413.html','415.html','429.html','500.html','502.html','503.html','504.html','error.html'}
public_assets={'app.v3030.js','site.v3030.css','experience.v3030.js','browser-compat.v3030.js','release-bootstrap.v3030.js','scroll-system.v3030.js','apple-touch-icon-v017.png','favicon-v017.ico','favicon-v017.png','egl-logo-v027.png','egl-logo-white-v028.png','opengles-gl-es-v030.png','openglesscope_logo_horizontal-v017.png','gpu-vendors/gpu_vendor_amd.png','gpu-vendors/gpu_vendor_arm.png','gpu-vendors/gpu_vendor_broadcom.png','gpu-vendors/gpu_vendor_huawei.png','gpu-vendors/gpu_vendor_imagination.png','gpu-vendors/gpu_vendor_intel.png','gpu-vendors/gpu_vendor_nvidia.png','gpu-vendors/gpu_vendor_qualcomm.png','gpu-vendors/gpu_vendor_samsung.png','gpu-vendors/gpu_vendor_unknown.png','gpu-vendors/gpu_vendor_vivante.png','gpu-vendors/gpu_vendor_vsi.png','hdr/dolby_vision.png','hdr/dolby_vision_2.png','hdr/hdr10.svg','hdr/hdr10_plus.png','hdr/hdr10_plus_v1014.png','hdr/hdr10_plus_advanced.png','hdr/hdr_vivid.webp'}

public_assets.update("country-flags/"+p.name for p in (Path(__file__).resolve().parents[1]/"assets/country-flags").glob("*.png"))

def local_ref_errors(root):
    out=[]
    pattern=re.compile(r'(?:href|src)=["\']([^"\']+)["\']',re.I)
    for html in root.glob('*.html'):
        body=html.read_text(encoding='utf-8')
        for ref in pattern.findall(body):
            if ref.startswith(('http://','https://','data:','#','mailto:','javascript:')): continue
            clean=urlsplit(ref).path
            if not clean or clean in {'.','./','/','/OpenGLESScope_database/'} or clean.endswith('/'): continue
            if clean.startswith('/OpenGLESScope_database/'):
                target=(root/clean[len('/OpenGLESScope_database/'):]).resolve()
            else:
                target=(html.parent/clean).resolve()
            try: target.relative_to(root.resolve())
            except ValueError:
                out.append(f'local asset escapes tree {html.name}: {ref}')
                continue
            if not target.is_file(): out.append(f'broken local asset {html.name}: {ref}')
    return out

def audit_artifact(root):
    root=root.resolve(); errors=[]
    if not root.is_dir(): errors.append(f'artifact tree missing: {root}')
    if errors:
        print('\n'.join(errors)); sys.exit(1)
    top={p.name for p in root.iterdir()}
    allowed=public_files|{'assets','data','licenses'}
    for x in sorted(top-allowed): errors.append(f'forbidden Pages artifact top-level entry {x}')
    for x in public_files: 
        if not (root/x).is_file(): errors.append(f'missing Pages artifact entry {x}')
    assets=root/'assets'
    data=root/'data'
    if not assets.is_dir(): errors.append('missing Pages artifact entry assets')
    if not data.is_dir(): errors.append('missing Pages artifact entry data')
    legal=root/'licenses'
    expected_legal={'openglesscope-application-mit.md','nodejs.md','python.md','workerd.md','wrangler.md','esbuild.md','sharp.md'}
    if not legal.is_dir() or {p.name for p in legal.iterdir() if p.is_file()}!=expected_legal: errors.append('missing or unexpected packaged legal notice')
    forbidden={'.git','.github','worker','tools','rules','.gradle','build','__pycache__','.idea','node_modules','.wrangler'}
    for p in root.rglob('*'):
        rel=p.relative_to(root)
        if any(part in forbidden for part in rel.parts): errors.append(f'forbidden Pages artifact {rel}')
        if rel.as_posix()!='.nojekyll' and any(part.startswith('.') for part in rel.parts): errors.append(f'forbidden hidden Pages artifact {rel}')
        if p.is_symlink(): errors.append(f'symlink not permitted in Pages artifact {rel}')
        if p.is_file() and rel.parts and rel.parts[0]=='assets':
            asset_rel=Path(*rel.parts[1:]).as_posix()
            if asset_rel not in public_assets: errors.append(f'unexpected/stale Pages asset {rel}')
        if p.is_file() and rel.parts and rel.parts[0]=='data' and p.suffix.lower()!='.json': errors.append(f'non-JSON Pages data {rel}')
    idx=root/'index.html'
    if idx.is_file():
        body=idx.read_text(encoding='utf-8')
        marker=json.loads((root/'data/release.json').read_text(encoding='utf-8'))
        if marker.get('releaseReady') is not True or marker.get('databaseVersion')!='3.0.30': errors.append('release marker not validated')
        for token in ['OpenGLESScope Database <strong>3.0.30</strong>','site.v3030.css','app.v3030.js','config.js?v=3030','experience.v3030.js','release-bootstrap.v3030.js','scroll-system.v3030.js','browser-compat.v3030.js']:
            if token not in body: errors.append(f'Pages artifact current reference missing {token}')
    preload=data/'preload'
    if args.require_preload and not (preload/'manifest.json').is_file(): errors.append('published report cache is missing: data/preload/manifest.json')
    if preload.exists():
        try:
            assert preload.is_dir() and not preload.is_symlink(), 'preload location is not a directory'
            manifest=json.loads((preload/'manifest.json').read_bytes())
            assert manifest.get('schemaVersion')==1 and manifest.get('databaseVersion')=='3.0.30', 'preload version mismatch'
            assert manifest.get('sourceSchemaVersion')==2 and manifest.get('normalizerVersion')==16, 'preload schema mismatch'
            summaries=manifest.get('reports'); chunks=manifest.get('chunks')
            count=manifest.get('reportCount')
            assert isinstance(summaries,list) and isinstance(chunks,list) and isinstance(count,int) and 0<=count<=100000 and len(summaries)==count, 'preload count invalid'
            ids={}; permitted={'manifest.json'}
            for row in summaries:
                rid=row.get('id') if isinstance(row,dict) else None
                assert isinstance(rid,str) and re.fullmatch(r'[0-9a-f]{64}',rid) and rid not in ids, 'invalid/duplicate preload summary ID'
                ids[rid]=row.get('submitted_at')
            observed={}
            for part in chunks:
                name=part.get('file') if isinstance(part,dict) else None
                digest=part.get('sha256') if isinstance(part,dict) else None
                assert isinstance(name,str) and re.fullmatch(r'reports\.[0-9a-f]{16}\.json',name) and name not in permitted, 'invalid/duplicate preload filename'
                assert isinstance(digest,str) and re.fullmatch(r'[0-9a-f]{64}',digest) and name=='reports.'+digest[:16]+'.json', 'preload hash/filename mismatch'
                permitted.add(name)
                content=(preload/name).read_bytes()
                assert isinstance(part.get('byteLength'),int) and 0<len(content)<=3*1024*1024 and len(content)==part['byteLength'], 'oversized/incorrect preload chunk length'
                assert hashlib.sha256(content).hexdigest()==digest, 'preload checksum failed'
                payload=json.loads(content)
                assert payload.get('schemaVersion')==1 and isinstance(payload.get('reports'),list) and len(payload['reports'])==part.get('reportCount'), 'preload chunk schema/count mismatch'
                for detail in payload['reports']:
                    rid=detail.get('id') if isinstance(detail,dict) else None
                    assert rid in ids and rid not in observed and detail.get('submittedAt')==ids[rid], 'preload detail ID/timestamp mismatch'
                    observed[rid]=1
            assert count==len(observed), 'preload missing report bodies'
            assert {p.name for p in preload.iterdir()}==permitted, 'extra unvalidated preload artifacts'
            published=json.loads((data/'index.json').read_bytes())
            assert published.get('databaseVersion')=='3.0.30' and published.get('reports')==summaries, 'preload manifest must match published authoritative index'
            assert published.get('reportCount',len(published['reports']))==count, 'preload must include the entire published report count'
        except (AssertionError,KeyError,TypeError,ValueError,OSError) as exc:
            errors.append(f'invalid Pages public-report preload: {exc}')
    errors.extend(local_ref_errors(root))
    if errors:
        print('\n'.join(errors)); sys.exit(1)
    print('OpenGLESScope Database 3.0.30 Pages artifact audit: PASS')
    sys.exit(0)

if args.artifact_tree: audit_artifact(args.artifact_tree)
root=(args.source_tree or Path(__file__).resolve().parents[1]).resolve()
errors=[]
def check(cond,msg):
    if not cond: errors.append(msg)
def read(rel): return (root/rel).read_text(encoding='utf-8')

for rel in ['index.html','assets/app.v3030.js','assets/site.v3030.css','worker/src/index.js','worker/package.json','worker/wrangler.jsonc','report.schema.json','data/index.json','rules/PROJECT_RULES.md','tools/pages.workflow.yml','.github/workflows/pages.yml','tools/test_statistics_filters.mjs','tools/test_ui_parity.mjs']:
    check((root/rel).is_file(),f'missing source file {rel}')
if errors:
    print('\n'.join(errors)); sys.exit(1)
check(json.loads(read('data/release.json')).get('releaseReady') is False,'source release marker must be unpublished')
index=read('index.html'); app=read('assets/app.v3030.js'); css=read('assets/site.v3030.css'); worker=read('worker/src/index.js'); rules=read('rules/PROJECT_RULES.md'); workflow=read('.github/workflows/pages.yml'); template=read('tools/pages.workflow.yml'); build_index=read('tools/build_index.py')
workflow_dir=root/'.github/workflows'
workflows=sorted(p.name for p in workflow_dir.iterdir() if p.is_file() and p.suffix.lower() in {'.yml','.yaml'})
check(workflows==['pages.yml'],f'exactly one GitHub Actions workflow is permitted; remove stale workflows: {workflows}')
check(workflow==template,'pages.yml must exactly match tools/pages.workflow.yml; run python tools/repair_repository.py --apply')
check((root/'tools/build_preload_snapshot.py').is_file(),'missing public-report preload builder')
check(workflow.count('python tools/build_preload_snapshot.py _site/data/preload')==2,'both release and accepted-snapshot builds must generate preload')
check('loadPreloadedSnapshot' in app and 'seedPreloadedReports' in app and 'enhanceSearchClear' in app and 'pulseUiLoading' in app,'shared cache/search interaction contract')
shared=root/'rules/VULKANSCOPE_DATABASE_1.4.12_PROJECT_RULES_REFERENCE.md'
shared_map=root/'rules/vulkanscope_database_1_4_12_rule_applicability.json'
check(shared.is_file() and shared_map.is_file(),'complete shared rule corpus and applicability map missing')
if shared.is_file() and shared_map.is_file():
    mapping=json.loads(shared_map.read_text(encoding='utf-8'))
    check(hashlib.sha256(shared.read_bytes()).hexdigest()==mapping.get('sourceSha256'),'shared rules reference hash mismatch')
    check(mapping.get('headingCount')==116 and len(mapping.get('headings',[]))==116,'shared rules must map all 116 reference sections')
check('## Release 3.0.9 complete shared-rule adoption' in rules and 'source zip and source-tree' in rules.lower(),'OpenGL ES/EGL-compatible shared rules and cache privacy missing')
check('OpenGLESScope Database <strong>3.0.30</strong>' in index,'index version')
check('site.v3030.css' in index and 'app.v3030.js' in index and 'config.js?v=3030' in index,'2.0.0 cache-busted asset refs')
check("connect-src 'self' https://openglesscope-database-api.openglesscope.workers.dev" in index,'CSP API pin')
check('Common evidence only' in app and 'Cross-producer comparison' in app,'compare producer/common-evidence controls')
for token in ['Common fields','One-sided fields','Visible differences','Unknown / Not reported','av!==bv||ac!==bc','compareStickySentinel','compareMinimizeToggle','swapCompare','compare-overview','compare-filter-controls']:
    check(token in app,f'compare contract token {token}')
check("parts.length===2||parts.length===3" in app and "#reports/${id}/${DETAIL_ROUTE" in app,'canonical report hash routes')
check("#compare/${a}/${b}" in app,'canonical compare hash route')
check("['trends','Trends']" in app and "['statistics','Statistics']" in app,'distinct statistics and trends destinations')
check('Submission statistics' in app and 'not device-population or market-share estimates' in app,'statistics evidence-scope disclaimer')
for token in ['statisticsSliceLimit','statisticsExtensionScope','statisticsExtensionNamespace','statisticsExtensionMinShare','statisticsExtensionSearch','data-stat-filter','Extension enumeration ranking','Submission timeline']:
    check(token in app,f'statistics/filter contract token {token}')
for token in ['eglVersion','driverMode','driverVersion','android','abi','appVersion','extensionToken','clearFilters']:
    check(token in app or token in index,f'cohort-filter token {token}')
check('FILTER_APPLICABILITY_GL' in app and "display:['androidFilter'" in app and "state.view==='display'" in app and 'filterIsApplicableGL' in app,'Display/HDR filter isolation contract')
for token in ['Share report','Copy permalink','Share comparison','routeReportUrl','routeCompareUrl','hashchange','popstate']:
    check(token in app,f'routing/share token {token}')
check('compareSection' in app and 'compareFieldSearch' in app,'Compare section and field filtering')
check('id="compareFilters" class="compare-filter-panel subfilters"' in app and 'compare-filter-controls' in app,'Compare secondary filter row hierarchy')
check('compare-diff-input' in css and '#contentView[data-main-view="compare"] .compare-picker' in css,'Reference compare control isolation')
check('compare-share-button' in app and 'compare-share-button' in css,'Compare share action separated from picker controls')
for token in ['#compareFilters', '.subfilters', '.nav-shell', '.hero-v127', '.cards', '.filter-clear-button[hidden]', '.settings-category-nav', '.viewport-scrollbar']:
    check(token in css,f'canonical visual component {token}')
check(css.startswith(':root{--bg:') and '/* GL/EGL-only existing components' not in css,'canonical stylesheet must be the FIRST common UI layer without stale GL defaults')
check('id="compareFilters" class="compare-filter-panel subfilters"' in app and "selectControl('compareSection','Section'" in app,'Compare dynamic subfilter hierarchy')
check("clear.hidden=!(active||String(state.query||'').trim())" in app,'inactive Clear filters must stay hidden')
for token in ['extensionRowSearch','limitRowSearch','formatRowSearch','precisionRowSearch']:
    check(token in app,f'view-scoped search token {token}')
for token in ['deviceModelFilter','submissionAgeFilter','resolutionFilter','refreshRateFilter','wideColorFilter','hdrStateFilter','hdrTypeFilter']:
    check(token in index,f'extended cohort/display filter {token}')

check('.distribution-grid{' in css and '.donut-chart{' in css and '.chart-filter-button{' in css,'first-party statistics chart styles')
check('https://' not in css and '@import' not in css,'CSS must not load remote chart/font resources')
check((root/'data/registry-catalog.v2000.json').is_file(),'local GL/EGL registry reference')
check(all(token in app for token in ['renderDevices()','renderVersions()','renderTrends()','renderEncyclopedia()','initParityFeatures()','favoriteKey','settingsCategory','finishStartup()']),'2.0.0 application workspace contract')
check(all(token in index for token in ['id="settingsDrawer"','id="pageScrollControls"','id="viewportScrollbar"','id="databaseLoading"','id="heroWorkspaceTitle"']),'2.0.0 index interface contract')

check('.notice{' in css and '.notice strong{' in css,'cross-producer notice style')
check("const DATABASE_VERSION='3.0.30'" in worker,'worker database version')
check("currentProducer:'OpenGLESScope 3.0.7'" in worker,'worker current producer')
check("p.application.versionCode!==2200+Number(p.application.version.split('.')[2])" in worker,'worker current producer versionCode gate')
check("'/v1/sync'" in worker and 'snapshotDispatchConfigured' in worker and 'dispatchSnapshotRefresh' in worker,'sync/snapshot Worker path')
check('MAX_BODY=2*1024*1024' in worker and 'MAX_REPORT_TEXT=2*1024*1024' in worker,'worker body/report bounds')
check("schemaVersion:2" in worker and "technicalReportSchema:5" in worker,'worker schema contract')
check('New report submissions require OpenGLESScope 3.0.7' in worker,'worker exact producer restriction')
check('TECH_KEYS_V3' in worker and 'INTERNAL_FORMAT_KEYS' in worker and 'validInternalFormat' in worker and 'EGL_RUNTIME_KEYS_V4' in worker and 'validEglRuntimeV4' in worker,'worker technical report 2 EGL runtime validation')
check('recordableAndroid' in worker and 'framebufferTargetAndroid' in worker and 'colorComponentTypeExt' in worker,'worker EGL config extension validation')
check("p.application.version!=='3.0.7'||p.application.versionCode!==3007" in worker,'exact producer and versionCode gate')
check('EGL runtime' in app and 'recordableAndroid' in app and 'unavailableAttributes' in app,'frontend EGL runtime/config detail coverage')
check(not any(x in app for x in ['0x5143','0x13B5','0x10DE','0x8086','0x1002','0x1010','0x14E4','0x19E5']),'frontend must not fabricate PCI/Vulkan-style vendor ids')
check('hasSensitive' in worker and 'stable(p)' in worker and 'sha(canonical)' in worker,'worker sensitive/canonical hash handling')
check('2026-09-30' in worker,'worker registry audit date')
check('## Release 0.7.4 full shared presentation parity and release-gate hardening' in rules,'rules 0.7.4 section')
check((root/'rules/0.7.4_FULL_SHARED_PRESENTATION_PARITY_AUDIT.md').is_file(),'0.7.4 audit rule file')
check('## Release 0.7.5 current EGL binding evidence compatibility' in rules,'rules 0.7.5 compatibility section')
check((root/'rules/0.7.5_CURRENT_EGL_BINDING_EVIDENCE_COMPATIBILITY_AUDIT.md').is_file(),'0.7.5 compatibility audit rule file')
check('## Release 0.7.6 OpenGLESScope 0.7.3 HDR provenance compatibility' in rules,'rules 0.7.6 section')
check((root/'rules/0.7.6_OPENGLESSCOPE_0.7.3_HDR_PROVENANCE_COMPATIBILITY_AUDIT.md').is_file(),'0.7.6 audit rule file')
check("dm.get('EGL current bindings').status!==(bindingsCurrent?'Available':'Unavailable')" in worker,'worker EGL binding diagnostic consistency gate')
check('Current EGL bindings: context=${e.currentContext}, display=${e.currentDisplay}, draw=${e.currentDrawSurface}, read=${e.currentReadSurface}' in worker,'worker EGL binding TXT consistency gate')
check('APPLICATION_KEYS_V2' in worker and 'applicationAbi' in worker and 'supportedDeviceAbis' in worker,'worker 0.7.2 application ABI metadata contract')
check('GL_NUM_WINDOW_RECTANGLES_EXT' not in worker and 'GL_MAX_SHADER_COMPILER_THREADS_KHR' not in worker,'worker must not require non-capability state/control queries')
check('## Release 0.7.7 OpenGLESScope 1.2.1 technicalReport-v3 end-to-end compatibility' in rules,'rules 0.7.7 section')
check((root/'rules/0.7.7_OPENGLESSCOPE_1.2.1_TECHNICAL_REPORT_3_AUDIT.md').is_file(),'0.7.7 audit rule file')
check('internalFormats' in worker and 'validInternalFormat' in worker and 'technicalReportSchema:5' in worker,'technical report v3 internal-format Worker contract')
check('## Release 0.9.0 OpenGLESScope 1.4.0 technicalReport-v4 EGL registry parity' in rules,'rules 0.9.0 section')
check((root/'rules/0.9.0_OPENGLESSCOPE_1.4.0_TECHNICAL_REPORT_4_EGL_REGISTRY_PARITY_AUDIT.md').is_file(),'0.9.0 audit rule file')
check('## Release 1.0.1 OpenGLESScope 1.5.1 compiler-hotfix compatibility' in rules,'rules 1.0.1 section')
check((root/'rules/1.0.1_OPENGLESSCOPE_1.5.1_COMPILER_HOTFIX_COMPATIBILITY_AUDIT.md').is_file(),'1.0.1 audit rule file')
check('## Release 1.0.3 OpenGLESScope 1.7.0 visual-interaction parity compatibility' in rules,'rules 1.0.3 section')
check('## Release 1.0.5 OpenGLESScope 1.9.0 UI/storage parity compatibility' in rules,'rules 1.0.5 section')
check('## Release 1.0.9 OpenGLESScope 2.0.0 VulkanScope-quality parity compatibility' in rules,'rules 1.0.9 section')
check((root/'rules/1.0.3_OPENGLESSCOPE_1.7.0_VISUAL_INTERACTION_PARITY_COMPATIBILITY_AUDIT.md').is_file(),'1.0.3 audit rule file')
check((root/'rules/1.0.5_OPENGLESSCOPE_1.9.0_UI_STORAGE_PARITY_COMPATIBILITY_AUDIT.md').is_file(),'1.0.5 audit rule file')
check((root/'rules/1.0.9_OPENGLESSCOPE_2.0.0_VULKANSCOPE_QUALITY_PARITY_COMPATIBILITY_AUDIT.md').is_file(),'1.0.9 audit rule file')
check('## Release 1.0.16 OpenGLESScope 2.2.1 compile-hotfix compatibility' in rules,'rules historical 1.0.16 section')
check((root/'rules/1.0.16_OPENGLESSCOPE_2.2.1_COMPILE_HOTFIX_COMPATIBILITY_AUDIT.md').is_file(),'historical 1.0.16 audit rule file')
check('TECH_KEYS_V4' in worker and 'EGL_CAPABILITY_KEYS' in worker and 'validEglCapability' in worker,'technical report v4 EGL capability Worker contract')
check('TECH_KEYS_V5' in worker and 'GL_RUNTIME_KEYS' in worker and 'EGL_RUNTIME_KEYS_V5' in worker and 'validGlRuntimeV5' in worker and 'validEglRuntimeV5' in worker,'technical report v5 GL/EGL runtime Worker contract')
check('eglCapabilities:n.eglCapabilities' in app and 'EGL capability queries' in app and "put('EGL capabilities'" in app,'frontend EGL capability normalization/presentation/compare coverage')
check('internalFormats:n.internalFormats' in app and 'Internal-format sample support' in app and "put('Internal formats'" in app,'frontend internal-format normalization/presentation/compare coverage')
check('producerAtLeastVersion' in worker and "p.application.version!=='1.2.1'||p.application.versionCode!==1201" in worker,'1.2.1 producer identity gate')
check("p.application.version!=='1.4.0'||p.application.versionCode!==1400" in worker,'1.4.0 producer identity gate')
check("p.application.version!=='1.4.1'||p.application.versionCode!==1401" in worker,'1.4.1 historical producer identity gate')
check("p.application.version!=='1.5.1'||p.application.versionCode!==1501" in worker,'1.5.1 producer identity gate')
check("p.application.version!=='1.7.0'||p.application.versionCode!==1700" in worker,'1.7.0 producer identity gate')
check("p.application.version!=='1.8.0'||p.application.versionCode!==1800" in worker,'1.8.0 historical producer identity gate')
check("p.application.version!=='1.9.3'||p.application.versionCode!==1903" in worker,'1.9.3 historical producer identity gate')
check("p.application.version!=='2.0.0'||p.application.versionCode!==2000" in worker,'2.0.0 historical producer identity gate')
check("p.application.version!=='2.1.1'||p.application.versionCode!==2101" in worker,'2.1.1 historical producer identity gate')
check("p.application.version!=='2.1.4'||p.application.versionCode!==2104" in worker,'2.1.4 historical producer identity gate')
check("p.application.version!=='2.2.0'||p.application.versionCode!==2200" in worker,'2.2.0 historical producer identity gate')
check("p.application.version!=='2.1.2'||p.application.versionCode!==2102" in worker,'2.1.2 historical producer identity gate')
check("p.application.version!=='1.9.1'||p.application.versionCode!==1901" in worker,'1.9.1 historical producer identity gate')
check('README.md files are forbidden' in rules,'README archive policy')
check(not any(p.is_file() and p.name.lower()=='readme.md' for p in root.rglob('*')),'README.md must be absent from source release')
forbidden_product=('caps'+'viewer').lower()
check(not any(forbidden_product in p.read_text(encoding='utf-8',errors='ignore').lower() for p in root.rglob('*') if p.is_file()),'forbidden third-party product name content')
check(not any(forbidden_product in str(p.relative_to(root)).lower() for p in root.rglob('*')),'forbidden third-party product name filename')
check(not any(p.is_dir() and p.name.lower()=='fastlane' for p in root.rglob('*')),'packaged store metadata forbidden')
check(not (root/'release.md').exists(),'root release.md forbidden')
app_assets=sorted(p.name for p in (root/'assets').glob('app.v*.js'))
css_assets=sorted(p.name for p in (root/'assets').glob('site.v*.css'))
check(app_assets==['app.v3030.js'],f'exactly one versioned frontend app asset is permitted: {app_assets}')
check(css_assets==['site.v3030.css'],f'exactly one versioned frontend css asset is permitted: {css_assets}')
static=json.loads(read('data/index.json'))
check(static.get('databaseVersion')=='3.0.30','static databaseVersion')
check(static.get('normalizerVersion')==16,'static normalizerVersion')
check(static.get('currentProducer')=='OpenGLESScope 3.0.7','static currentProducer')
check(static.get('registryAuditDate')=='2026-09-30','static registry audit date')
check('obj["databaseVersion"]="3.0.30"' in build_index,'static index builder database version')
check('obj["currentProducer"]="OpenGLESScope 3.0.7"' in build_index,'static index builder current producer')
pkg=json.loads(read('worker/package.json'))
check(pkg.get('version')=='3.0.30','worker package version')
check(pkg.get('devDependencies',{}).get('wrangler')=='4.146.0','wrangler pin')
wr=json.loads(read('worker/wrangler.jsonc'))
check(wr.get('compatibility_date')=='2026-08-23','Cloudflare accepted compatibility date pin')
check(wr.get('account_id')=='6881527e6e0b9bc4a0c009473428d1bc','Cloudflare account pin')
dbs=wr.get('d1_databases',[])
check(bool(dbs) and dbs[0].get('binding')=='DB' and dbs[0].get('database_id')=='2c945dda-e320-4b3a-9fac-a086373db17c','D1 identity pin')
schema=json.loads(read('report.schema.json'))
check(schema.get('properties',{}).get('technicalReport',{}).get('properties',{}).get('queryDiagnostics',{}).get('maxItems')==16384,'query diagnostic schema bound')
tech_props=schema.get('properties',{}).get('technicalReport',{}).get('properties',{})
check(tech_props.get('schemaVersion',{}).get('enum')==[1,2,3,4,5],'public schema technical report versions')
check('glRuntime' in tech_props and 'eglRuntime' in tech_props and 'unavailableAttributes' in tech_props.get('glRuntime',{}).get('properties',{}) and 'surfaceGlColorspace' in tech_props.get('eglRuntime',{}).get('properties',{}),'public schema v5 GL/EGL runtime coverage')
internal_props=tech_props.get('internalFormats',{}).get('items',{}).get('properties',{})
check(all(x in internal_props for x in ['target','internalFormat','status','detail','sampleCounts','nvSampleProperties']),'public schema internal-format v3 coverage')
egl_cap_props=tech_props.get('eglCapabilities',{}).get('items',{}).get('properties',{})
check(all(x in egl_cap_props for x in ['name','status','value','detail']),'public schema EGL capability v4 coverage')
config_props=tech_props.get('eglConfigs',{}).get('items',{}).get('properties',{})
check(all(x in config_props for x in ['recordableAndroid','framebufferTargetAndroid','colorComponentTypeExt','unavailableAttributes']),'public schema EGL config extension coverage')
display_props=schema.get('properties',{}).get('display',{}).get('properties',{})
display_required=schema.get('properties',{}).get('display',{}).get('required',[])
tech_display_props=tech_props.get('display',{}).get('properties',{})
tech_display_required=tech_props.get('display',{}).get('required',[])
check(display_props.get('hdrCapabilityStatus',{}).get('enum')==['available','unavailable','unknown'] and 'hdrCapabilityStatus' in display_required,'public schema top-level HDR status')
check(tech_display_props.get('hdrCapabilityStatus',{}).get('enum')==['available','unavailable','unknown'] and 'hdrCapabilityStatus' in tech_display_required,'public schema technical HDR status')
check('DISPLAY_KEYS_V2' in worker and "producerAtLeast(p,7,3)" in worker and "reportLine(text,'HDR capability status')" in worker,'0.7.3 HDR provenance Worker gates')
for token in ['actions/checkout@v7','persist-credentials: false','ref: main','actions/setup-python@v7','python tools/audit_database.py --source-tree .','python tools/repair_repository.py --check','python tools/quality_gate.py','python tools/build_pages_artifact.py _site','python tools/build_live_index.py _site/data/index.json','python tools/audit_database.py --artifact-tree _site','actions/upload-pages-artifact@v4','include-hidden-files: true','actions/configure-pages@v5','actions/deploy-pages@v4','path: _site','--expect-report-id "$REPORT_ID"','verify_published_snapshot.py']:
    check(token in workflow,f'workflow quality token {token}')
check('  release-publish:' in workflow and '  snapshot-refresh:' in workflow,'separate release and snapshot jobs')
release=workflow.split('  release-publish:',1)[-1].split('  snapshot-refresh:',1)[0]
snapshot=workflow.split('  snapshot-refresh:',1)[-1]
for label,section in [('release',release),('snapshot',snapshot)]:
    check(all(token in section for token in ['pages: write','id-token: write','group: pages-publication','cancel-in-progress: false','queue: max','python tools/quality_gate.py']),label+' security and serialization')
check(workflow.count('group: pages-publication')==2,'one shared deployment concurrency group')
errors.extend(local_ref_errors(root))
for p in root.rglob('*'):
    if not p.is_file(): continue
    if p.suffix in {'.js','.mjs'}:
        text=p.read_text(encoding='utf-8',errors='ignore')
        if re.search(r'(^|\s)//(?!/)',text,re.M) or '/*' in text: errors.append(f'source-code comments forbidden: {p.relative_to(root)}')
    if p.suffix=='.py':
        text=p.read_text(encoding='utf-8',errors='ignore')
        if re.search(r'^\s*#',text,re.M): errors.append(f'source-code comments forbidden: {p.relative_to(root)}')
for forbidden in ['.gradle','build','__pycache__','.idea','node_modules','.wrangler']:
    found=[p.relative_to(root) for p in root.rglob(forbidden)]
    if found: errors.append(f'transient source entries {forbidden}: {found[:5]}')
node=shutil.which('node')
if node:
    for rel in ['assets/app.v3030.js','worker/src/index.js','worker/tests/contract.mjs','tools/test_routes.mjs','tools/test_compare_contract.mjs','tools/test_statistics_filters.mjs','tools/test_ui_parity.mjs']:
        r=subprocess.run([node,'--check',str(root/rel)],capture_output=True,text=True)
        if r.returncode: errors.append(f'node syntax {rel}: {r.stderr.strip()}')
if errors:
    print('\n'.join(errors)); sys.exit(1)
print('OpenGLESScope Database 3.0.30 source audit: PASS')
print('producer=OpenGLESScope 3.0.7/3007 schema=2 technicalReport=5 normalizer=16')
