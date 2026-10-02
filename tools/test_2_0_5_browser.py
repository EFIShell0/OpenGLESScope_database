from pathlib import Path
import os,re,json,base64
from playwright.sync_api import sync_playwright
r=Path(__file__).resolve().parents[1]
health={'status':'ok','schemaVersion':2,'technicalReportSchema':5,'normalizerVersion':16,'currentProducer':'OpenGLESScope 2.2.22','databaseVersion':'3.0.2','compatibleProducer':'OpenGLESScope 2.2.22 (versionCode 2222) for new submissions only'}
index={'schemaVersion':2,'normalizerVersion':16,'databaseVersion':'3.0.2','currentProducer':'OpenGLESScope 2.2.22','reports':[],'nextCursor':None}
sync={'databaseReleaseVersion':'3.0.2','workerReleaseVersion':'3.0.2','reportCount':0,'latestReportId':'','latestSubmittedAt':'','syncToken':'0::'}
html=(r/'index.html').read_text()
html=re.sub(r'<meta[^>]*http-equiv="Content-Security-Policy"[^>]*>', '', html)
logo='data:image/png;base64,'+base64.b64encode((r/'assets/openglesscope_logo_horizontal-v017.png').read_bytes()).decode('ascii')
html=html.replace('src="./assets/openglesscope_logo_horizontal-v017.png"','src="'+logo+'"')
html=re.sub(r'<link\b[^>]*href="[^"]*site\.v3002\.css(?:\?[^\"]*)?"[^>]*>',lambda x:'<style>'+(r/'assets/site.v3002.css').read_text()+'</style>',html)
mock_script="""<script>window.OPENGLESSCOPE_DATABASE_API='https://openglesscope-database-api.openglesscope.workers.dev';window.__requestNetworkCalls=0;window.fetch=async function(input){const u=String(input);let x;if(u.includes('/v1/network-info')){window.__requestNetworkCalls++;x=MOCK_NETWORK;}else if(u.includes('/v1/health'))x=MOCK_HEALTH;else if(u.includes('/v1/sync'))x=MOCK_SYNC;else if(u.includes('/v1/reports'))x=MOCK_INDEX;else if(u.includes('registry-catalog'))x=MOCK_CATALOG;else if(u.includes('data/index.json'))x=MOCK_INDEX;else x={};return new Response(JSON.stringify(x),{status:200,headers:{'content-type':'application/json'}})}</script>"""
mock_script=mock_script.replace('MOCK_NETWORK',json.dumps({'networkInfoVersion':1,'accessFamily':'IPv6','activeAddress':'2001:db8::42','ipv4':{'address':'','status':'not_observed'},'ipv6':{'address':'2001:db8::42','status':'observed'},'country':'TR','region':'Istanbul','city':'Istanbul','timezone':'Europe/Istanbul','colo':'IST','asOrganization':'Test Network'})).replace('MOCK_HEALTH',json.dumps(health)).replace('MOCK_INDEX',json.dumps(index)).replace('MOCK_SYNC',json.dumps(sync)).replace('MOCK_CATALOG',(r/'data/registry-catalog.v2000.json').read_text())
html,n=re.subn(r'<script\b[^>]*src="[^"]*config\.js[^"]*"[^>]*>\s*</script>',lambda x:mock_script,html);assert n,n
html,n=re.subn(r'<script\b[^>]*src="[^"]*app\.v3002\.js[^"]*"[^>]*>\s*</script>',lambda x:'<script>'+(r/'assets/app.v3002.js').read_text()+'</script>',html);assert n,n
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-gpu'])
 for size in [(1440,900),(390,844)]:
  page=browser.new_page(viewport={'width':size[0],'height':size[1]},reduced_motion='reduce')
  errors=[];page.on('pageerror',lambda error:errors.append(error.stack or str(error)))
  page.set_content(html,wait_until='domcontentloaded',timeout=20000)
  page.wait_for_selector('#mainNav .nav-button',timeout=12000)
  print('SCREEN',size,'nav',page.locator('#mainNav .nav-button').count(),'errors',errors[:2])
  assert page.locator('#mainNav .nav-button').count()==16
  for view in ['devices','versions','trends','statistics','compare','encyclopedia','reports']:
   page.locator(f'#mainNav button[data-view="{view}"]').click();page.wait_for_timeout(45)
   assert page.locator('#mainNav button.active').get_attribute('data-view')==view,view
  page.locator('#mainNav button[data-view="encyclopedia"]').click();page.wait_for_selector('#registryPageInput',timeout=10000)
  print('entries',page.locator('.registry-entry').count())
  assert page.locator('.registry-entry').count()==50
  page.locator('#settingsButton').click();print('drawer',page.locator('#settingsDrawer').get_attribute('aria-hidden'))
  assert page.locator('#settingsDrawer').get_attribute('aria-hidden')=='false'
  page.locator('[data-settings-category="preferences"]').click()
  assert page.locator('#settingsRegionalMode').count()==1
  page.locator('#settingsRegionalMode').evaluate('(el)=>{el.value="country";el.dispatchEvent(new Event("change",{bubbles:true}))}')
  assert not page.locator('#settingsRegionalCountry').is_disabled()
  page.locator('#settingsRegionalCountry').evaluate('(el)=>{el.value="TR";el.dispatchEvent(new Event("change",{bubbles:true}))}')
  assert 'Istanbul' in page.locator('#settingsRegionalPreview').inner_text()
  page.locator('[data-settings-category="internet"]').click()
  assert page.evaluate('window.__requestNetworkCalls')==0
  page.locator('#settingsRequestNetwork').click();page.wait_for_function('window.__requestNetworkCalls===1');page.wait_for_function("document.querySelector('#settingsRequestNetworkResult').textContent.includes('2001:db8::42')")
  page.locator('#settingsClose').click()
  assert page.locator('#settingsRequestNetworkResult').get_attribute('hidden') is not None
  assert not errors,errors
  preview=os.environ.get('BROWSER_PREVIEW_DIR')
  if preview:
   dest=Path(preview);dest.mkdir(parents=True,exist_ok=True)
   page.locator('#mainNav button[data-view="reports"]').click()
   page.screenshot(path=str(dest/('openglesscope-3.0.2-' + ('desktop' if size[0]>600 else 'mobile') + '.png')),full_page=False)
  print('BROWSER PASS',size,'16 tabs, VulkanScope shared UI, 50-row catalog, Settings, explicit-only network privacy; errors=',errors)
  page.close()
 browser.close()
