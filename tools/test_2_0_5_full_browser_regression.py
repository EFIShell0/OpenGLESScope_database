from pathlib import Path
import os
import tempfile
import json
from playwright.sync_api import sync_playwright
r=Path(__file__).resolve().parents[1]
health={'status':'ok','schemaVersion':2,'technicalReportSchema':5,'normalizerVersion':16,'currentProducer':'OpenGLESScope 3.0.1','databaseVersion':'3.0.17','compatibleProducer':'OpenGLESScope 3.0.1 (versionCode 3001) for new submissions only'}
index={'schemaVersion':2,'normalizerVersion':16,'databaseVersion':'3.0.17','currentProducer':'OpenGLESScope 3.0.1','reports':[],'nextCursor':None}
sync={'databaseReleaseVersion':'3.0.17','workerReleaseVersion':'3.0.17','reportCount':0,'latestReportId':'','latestSubmittedAt':'','syncToken':'0::'}
import re
html=(r/'index.html').read_text()
html=re.sub(r'<meta[^>]*http-equiv="Content-Security-Policy"[^>]*>','',html)
html=re.sub(r'<link\b[^>]*href="[^"]*site\.v3017\.css(?:\?[^\"]*)?"[^>]*>',lambda x:'<style>'+(r/'assets/site.v3017.css').read_text()+'</style>',html)
mock_script="""<script>window.OPENGLESSCOPE_DATABASE_API='https://openglesscope-database-api.openglesscope.workers.dev';window.__requestNetworkCalls=0;window.fetch=async function(input){const u=String(input);let x;if(u.includes('/v1/network-info')){window.__requestNetworkCalls++;x=MOCK_NETWORK;}else if(u.includes('/v1/health'))x=MOCK_HEALTH;else if(u.includes('/v1/sync'))x=MOCK_SYNC;else if(u.includes('/v1/reports'))x=MOCK_INDEX;else if(u.includes('registry-catalog'))x=MOCK_CATALOG;else if(u.includes('data/index.json'))x=MOCK_INDEX;else x={};return new Response(JSON.stringify(x),{status:200,headers:{'content-type':'application/json'}})}</script>"""
mock_script=mock_script.replace('MOCK_NETWORK',json.dumps({'networkInfoVersion':1,'accessFamily':'IPv6','activeAddress':'2001:db8::42','ipv4':{'address':'','status':'not_observed'},'ipv6':{'address':'2001:db8::42','status':'observed'},'country':'TR','region':'Istanbul','city':'Istanbul','timezone':'Europe/Istanbul','colo':'IST','asOrganization':'Test Network'})).replace('MOCK_HEALTH',json.dumps(health)).replace('MOCK_INDEX',json.dumps(index)).replace('MOCK_SYNC',json.dumps(sync)).replace('MOCK_CATALOG',(r/'data/registry-catalog.v2000.json').read_text())
html,n=re.subn(r'<script\b[^>]*src="[^"]*config\.js[^"]*"[^>]*>\s*</script>',lambda x:mock_script,html);assert n==1,n
html,n=re.subn(r'<script\b[^>]*src="[^"]*app\.v3017\.js[^"]*"[^>]*>\s*</script>',lambda x:'<script>'+(r/'assets/app.v3017.js').read_text()+'</script>',html);assert n==1,n
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),args=['--no-sandbox','--disable-gpu'])
 for size in [(1440,900),(390,844)]:
  page=browser.new_page(viewport={'width':size[0],'height':size[1]},reduced_motion='reduce')
  errors=[];page.on('pageerror',lambda error:errors.append(error.stack or str(error)))
  page.set_content(html,wait_until='domcontentloaded',timeout=20000)
  page.wait_for_selector('#mainNav .nav-button',timeout=12000)
  page.wait_for_selector('#databaseLoading[hidden]',state='attached',timeout=12000)
  labels=page.locator('#mainNav .nav-button').count()
  assert labels==16,labels
  for view in ['devices','versions','trends','statistics','compare','encyclopedia','reports']:
   page.locator(f'#mainNav button[data-view="{view}"]').click()
   page.wait_for_timeout(140)
   assert page.locator('#mainNav button.active').get_attribute('data-view')==view,view
  page.locator('#mainNav button[data-view="encyclopedia"]').click()
  page.wait_for_selector('#registryPageInput',timeout=10000)
  assert page.locator('.registry-entry').count()==50
  page.locator('#registryPageInput').fill('0');page.locator('#registryPageInput').dispatch_event('change');page.wait_for_timeout(100)
  assert page.locator('#registryPageInput').input_value()=='1'
  page.locator('#registryPageInput').fill('999');page.locator('#registryPageInput').dispatch_event('change');page.wait_for_timeout(100)
  assert page.locator('#registryPageInput').input_value()=='1'
  page.locator('#registryPageInput').fill('106');page.locator('#registryPageInput').locator('xpath=..').locator('.page-jump-go').click()
  assert page.locator('#registryPageInput').input_value()=='106'
  page.locator('#settingsButton').click()
  assert page.locator('#settingsDrawer').get_attribute('aria-hidden')=='false'
  page.locator('[data-settings-category="preferences"]').click()
  assert page.locator('#settingsRegionalMode').count()==1
  page.locator('#settingsRegionalMode').evaluate('(el)=>{el.value="country";el.dispatchEvent(new Event("change",{bubbles:true}))}')
  assert not page.locator('#settingsRegionalCountry').is_disabled()
  cwrap=page.locator('#settingsRegionalCountry').locator('xpath=..')
  cwrap.locator('.custom-select-button').click()
  assert cwrap.locator('.custom-select-option').count() <= 50
  cwrap.locator('.custom-select-search').fill('Canada')
  assert cwrap.locator('.custom-select-option').count() > 0
  cwrap.locator('.custom-select-option').filter(has_text='Canada').first.click()
  assert page.locator('#settingsRegionalCountry').input_value()=='CA'
  assert 'Toronto' in page.locator('#settingsRegionalPreview').inner_text()
  page.locator('#settingsRegionalCountry').evaluate('(el)=>{el.value="TR";el.dispatchEvent(new Event("change",{bubbles:true}))}')
  assert 'Istanbul' in page.locator('#settingsRegionalPreview').inner_text()
  page.locator('#settingsRegionalMode').evaluate('(el)=>{el.value="manual";el.dispatchEvent(new Event("change",{bubbles:true}))}')
  assert page.locator('#settingsRegionalCountry').is_disabled()
  assert not page.locator('#settingsRegionalClock').is_disabled()
  page.locator('#settingsRegionalTimeZone').evaluate('(el)=>{el.value="UTC";el.dispatchEvent(new Event("change",{bubbles:true}))}')
  page.locator('#settingsRegionalSeason').evaluate('(el)=>{el.value="standard";el.dispatchEvent(new Event("change",{bubbles:true}))}')
  assert 'Forced standard / winter offset' in page.locator('#settingsRegionalPreview').inner_text()
  page.locator('label:has(#settingsSubmittedDefault)').click();assert page.locator('#settingsSubmittedDefault').is_checked()
  page.locator('label:has(#settingsVendorDefault)').click();assert page.locator('#settingsVendorDefault').is_checked()
  assert page.evaluate('window.__requestNetworkCalls')==0
  page.locator('[data-settings-category="internet"]').click()
  page.wait_for_function("window.__requestNetworkCalls>=1 && document.querySelectorAll('#settingsNetworkInfo .settings-info-row').length>=20 && document.querySelectorAll('#settingsBrowserInfo .settings-info-row').length>=25",timeout=8000)
  assert page.locator('#settingsNetworkInfo .network-address-mosaic').count()>=1
  assert page.locator('[data-settings-panel="information"] #settingsBrowserInfo').count()==0
  page.locator('#settingsClose').click()
  assert '2001:db8::42' not in page.locator('#settingsNetworkInfo').inner_text()

  assert page.locator('#settingsDrawer').get_attribute('aria-hidden')=='true'
  page.locator('#mainNav button[data-view="reports"]').click()
  page.wait_for_timeout(130)
  assert page.locator('#pageProgress').get_attribute('aria-valuenow') is not None
  assert not errors,errors
  if os.environ.get('BROWSER_PREVIEW_DIR'):
   dest=Path(os.environ['BROWSER_PREVIEW_DIR']);dest.mkdir(parents=True,exist_ok=True)
   page.screenshot(path=str(dest/('desktop-201.png' if size[0]>600 else 'mobile-201.png')),full_page=True)
  print('BROWSER PASS',size,'16 tabs, catalog pagination, user-opened request details, settings, column toggles, route, progress. errors=',errors)
  page.close()
 browser.close()
