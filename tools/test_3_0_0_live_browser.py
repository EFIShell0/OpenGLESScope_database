from pathlib import Path
from playwright.sync_api import sync_playwright
import json,re,base64,os
root=Path(__file__).resolve().parents[1]
health={'status':'ok','schemaVersion':2,'technicalReportSchema':5,'normalizerVersion':16,'currentProducer':'OpenGLESScope 2.2.22','databaseVersion':'3.0.1','compatibleProducer':'OpenGLESScope 2.2.22 (versionCode 2222) for new submissions only'}
idx={'schemaVersion':2,'normalizerVersion':16,'databaseVersion':'3.0.1','currentProducer':'OpenGLESScope 2.2.22','reports':[],'nextCursor':None}
sync={'databaseReleaseVersion':'3.0.1','workerReleaseVersion':'3.0.1','reportCount':0,'latestReportId':'','latestSubmittedAt':'','syncToken':'0::'}
network={'networkInfoVersion':1,'accessFamily':'IPv6','activeAddress':'2001:db8::42','ipv4':{'address':'','status':'not_observed'},'ipv6':{'address':'2001:db8::42','status':'observed'},'country':'TR','region':'Istanbul','city':'Istanbul','timezone':'Europe/Istanbul','colo':'IST','asOrganization':'Test Network'}
html=(root/'index.html').read_text()
def inline_art(match):
 file=root/match.group(1)
 if not file.is_file():return match.group(0)
 media='image/png' if file.suffix=='.png' else 'image/svg+xml' if file.suffix=='.svg' else 'image/jpeg'
 return 'src="data:'+media+';base64,'+base64.b64encode(file.read_bytes()).decode('ascii')+'"'
html=re.sub(r'src="\./(assets/[^"]+\.(?:png|svg|jpg))"',inline_art,html)

html=re.sub(r'<meta[^>]*http-equiv="Content-Security-Policy"[^>]*>','',html)
html=re.sub(r'<link\b[^>]*href="[^"]*site\.v3001\.css[^"]*"[^>]*>',lambda _: '<style>'+(root/'assets/site.v3001.css').read_text()+'</style>',html)
mock="""<script>window.OPENGLESSCOPE_DATABASE_API='https://openglesscope-database-api.openglesscope.workers.dev';window.__requestNetworkCalls=0;window.fetch=async function(input){const u=String(input);let x;if(u.includes('/v1/network-info')){window.__requestNetworkCalls++;x=MOCK_NETWORK;}else if(u.includes('/v1/health'))x=MOCK_HEALTH;else if(u.includes('/v1/sync'))x=MOCK_SYNC;else if(u.includes('/v1/reports'))x=MOCK_INDEX;else if(u.includes('registry-catalog'))x=MOCK_CATALOG;else if(u.includes('/licenses/')||u.includes('./licenses/'))return new Response(MOCK_LICENSE,{status:200,headers:{'content-type':'text/plain'}});else if(u.includes('data/release.json'))x=MOCK_RELEASE;else if(u.includes('data/index.json'))x=MOCK_INDEX;else x={};return new Response(JSON.stringify(x),{status:200,headers:{'content-type':'application/json'}})}</script>"""
for token,obj in [('MOCK_NETWORK',network),('MOCK_HEALTH',health),('MOCK_SYNC',sync),('MOCK_INDEX',idx),('MOCK_CATALOG',json.loads((root/'data/registry-catalog.v2000.json').read_text())),('MOCK_RELEASE',json.loads((root/'data/release.json').read_text())),('MOCK_LICENSE',(root/'licenses/openglesscope-application-mit.md').read_text())]:mock=mock.replace(token,json.dumps(obj))
for name in ['release-bootstrap.v3001.js','config.js','browser-compat.v3001.js','app.v3001.js','experience.v3001.js']:
 content=mock if name=='config.js' else '<script>'+(root/('assets/'+name)).read_text()+'</script>'
 html,n=re.subn(r'<script\b[^>]*src="[^"]*'+re.escape(name)+r'(?:\?[^\"]*)?"[^>]*>\s*</script>',lambda _,src=content:src,html)
 assert n==1,(name,n)
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-gpu'])
 for width,height in [(1440,900),(390,844)]:
  ctx=b.new_context(viewport={'width':width,'height':height},reduced_motion='reduce')
  page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.set_content(html,wait_until='domcontentloaded',timeout=20000)
  page.wait_for_function("document.body.classList.contains('startup-layout-ready')",timeout=15000)
  page.wait_for_selector('#privacyNotice',state='visible',timeout=6000)
  assert page.locator('#mainNav .nav-button').count()==16
  assert page.evaluate('window.__requestNetworkCalls')==0
  assert page.locator('#databaseLoading').is_hidden(),'Startup loading was not dismissed'
  assert not errors,errors
  page.locator('#privacyOpenLicense').click()
  page.wait_for_selector('#licenseViewerDialog',state='visible')
  page.locator('#licenseViewerClose').click()
  page.wait_for_selector('#privacyNotice',state='visible')
  page.locator('#privacySessionOnly').click()
  assert page.locator('#privacyNotice').is_hidden()
  page.locator('#settingsButton').click()
  assert page.locator('#settingsDrawer').get_attribute('aria-hidden')=='false'
  page.locator('[data-settings-category="information"]').click()
  assert page.locator('.legal-list .legal-card').count()==7
  page.get_by_role('button',name='Read local license (.md)').last.click()
  page.wait_for_selector('#licenseViewerDialog',state='visible',timeout=4000)
  page.wait_for_function("document.querySelector('#licenseViewerBody').textContent.includes('MIT')",timeout=5000)
  page.locator('#licenseViewerClose').click()
  page.wait_for_selector('#licenseViewerDialog',state='hidden')
  page.locator('#settingsClose').click()
  assert page.locator('#settingsDrawer').get_attribute('aria-hidden')=='true'
  for view in ['devices','versions','reports','encyclopedia','compare']:
   page.locator(f'#mainNav button[data-view="{view}"]').click(timeout=4000)
   assert page.locator('#mainNav button.active').get_attribute('data-view')==view
  assert not errors,errors
  if os.environ.get('BROWSER_PREVIEW_DIR'):
   output=Path(os.environ['BROWSER_PREVIEW_DIR']);output.mkdir(parents=True,exist_ok=True)
   page.locator('#mainNav button[data-view="reports"]').click()
   page.screenshot(path=str(output/('OpenGLESScope-Database-3.0.1-'+('desktop' if width>600 else 'mobile')+'.png')),full_page=False)
  print('CHROMIUM PASS:',width,'x',height,'startup, privacy choices, license modal, 16 tabs, settings, and no unsolicited IP queries')
  ctx.close()
 b.close()
