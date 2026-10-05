from pathlib import Path
from html.parser import HTMLParser
import hashlib,json,re
root=Path(__file__).resolve().parents[1]
html=(root/'index.html').read_text(encoding='utf-8')
css=(root/'assets/site.v3030.css').read_text(encoding='utf-8')
app=(root/'assets/app.v3030.js').read_text(encoding='utf-8')
ux=(root/'assets/experience.v3030.js').read_text(encoding='utf-8')
boot=(root/'assets/release-bootstrap.v3030.js').read_text(encoding='utf-8')
compat=(root/'assets/browser-compat.v3030.js').read_text(encoding='utf-8')
ref=(root/'rules/SHARED_UI_1_4_12_REFERENCE.css').read_text(encoding='utf-8')
source,branded=(root/'rules/SHARED_UI_BASE_SHA256.txt').read_text(encoding='utf-8').splitlines()
assert hashlib.sha256(ref.encode()).hexdigest()==source
assert css.find('\n\n.not-applicable')>0
base=css[:css.index('\n\n.not-applicable')]
assert hashlib.sha256(base.encode()).hexdigest()==branded
normalize=lambda s:re.sub(r'rgba?\([^)]*\)|#[0-9a-fA-F]{6}(?![0-9a-fA-F])','COLOR',s)
assert normalize(base)==normalize(ref),'Reference geometry was modified'
assert '--accent:#ba2a8d' in css and '#ff5c66' not in base
class Inspector(HTMLParser):
 def __init__(self):super().__init__();self.ids=[]
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if 'id' in d:self.ids.append(d['id'])
i=Inspector();i.feed(html)
assert len(i.ids)==len(set(i.ids)),'Duplicate HTML IDs'
for key in ['browserCompatibilityGate','appRoot','networkStatusShell','databaseLoading','settingsDrawer','settingsInformation','licenseViewerDialog','licenseViewerBackdrop','licenseViewerBody','databaseUpdateModal','databaseUpdateRefresh','new-report-toast-title','new-report-toast-copy']:
 if key.startswith('new-report-toast-'):assert key in ux
 else:assert key in i.ids,key
assert 'startup-layout-hold' in html and 'startup-layout-ready' in app and 'app.v3030.js?v=3030' in html
for asset in ['app.v3030.js','site.v3030.css','release-bootstrap.v3030.js','browser-compat.v3030.js','experience.v3030.js']:
 assert asset in html
assert 'https://openglesscope-database-api.openglesscope.workers.dev' in html
assert "const VERSION='3.0.30'" in ux and "const DATABASE_VERSION='3.0.30'" in app
assert "const LOCAL='3.0.30'" in boot and '__OPENGLESSCOPE_BROWSER_INFO__' in compat
for key in ['databaseReleaseVersion!==VERSION','setInterval(()=>void sync(false),3000)','setInterval(()=>void releases(),10000)','releaseReady===true','abortable','lastModalFocus','licenseFocus','licenseToken','ogdb-privacy-session-v1','ogdb-privacy-ack-v1','sessionStorage.setItem','openglesscope:new-reports','openglesscope:connection-error']:
 assert key in ux,key
assert 'document.cookie' not in ux and 'analytics' not in [x.strip().split('(')[0] for x in re.findall(r'\banalytics\s*\(',ux)]
assert 'id="privacyNotice"' not in html and 'privacy()' not in ux and '.license-viewer-dialog.open' in css and '.database-update-modal' in css
marker=json.loads((root/'data/release.json').read_text(encoding='utf-8'))
assert marker==dict(schemaVersion=2,databaseVersion='3.0.30',releaseReady=False,appAsset='assets/app.v3030.js',cacheKey='3030')
for name in ['openglesscope-application-mit.md','nodejs.md','python.md','workerd.md','wrangler.md','esbuild.md','sharp.md']:
 assert (root/'licenses'/name).is_file(),name
assert 'MIT License' in (root/'licenses/openglesscope-application-mit.md').read_text(encoding='utf-8')
assert '3.0.0' in (root/'worker/src/index.js').read_text(encoding='utf-8') and '3000' in (root/'worker/src/index.js').read_text(encoding='utf-8')
assert not list(root.glob('DEPLOY*.md'))
for candidate in [base.replace('--accent:#ba2a8d','--accent:#ff5c66',1),base.replace('border-radius:13px','border-radius:3px',1)]:
 try:assert hashlib.sha256(candidate.encode()).hexdigest()==branded
 except AssertionError:continue
 raise AssertionError('Visual negative mutation escaped')
print('OpenGLESScope Database 3.0.30 source geometry, brand, privacy, license, startup, live sync and version negative gates: ALL PASS')
