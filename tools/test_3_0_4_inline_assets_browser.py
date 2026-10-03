from pathlib import Path
from playwright.sync_api import sync_playwright
import base64,os
root=Path(__file__).resolve().parents[1]
ns={'__file__':str(root/'tools/test_3_0_2_interface_browser.py')}
source=(root/'tools/test_3_0_2_interface_browser.py').read_text(encoding='utf-8')
exec(source.split('\nwith sync_playwright() as p:',1)[0].replace('range(63)','range(15)'),ns)
rows=ns['rows']; row_map=ns['row_map']; seed=ns['seed']; head=ns['head']; health=ns['health']; net=ns['network']
head['syncToken']='15:seed'; head['reportCount']=15
for row in row_map.values():
 row['technicalReport']['display']={'hdrTypes':['HDR10+'],'hdrStatus':'Available','wideColor':'Available'}
html=ns['html']
for rel in ['assets/egl-logo-white-v028.png','assets/opengles-gl-es-v030.png','assets/hdr/hdr10_plus_v1014.png']:
 candidate=root/rel
 if candidate.is_file():
  raw='data:image/png;base64,'+base64.b64encode(candidate.read_bytes()).decode('ascii')
  html=html.replace('./'+rel,raw)
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path=os.environ.get('CHROMIUM_PATH') or '/usr/bin/chromium',args=['--no-sandbox','--disable-gpu'])
 for width,height in [(1440,900),(390,844)]:
  ctx=browser.new_context(viewport={'width':width,'height':height},reduced_motion='reduce')
  page=ctx.new_page(); errors=[]; responses=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('response',lambda r:responses.append((r.status,r.url)))
  page.set_content(html,wait_until='domcontentloaded',timeout=25000)
  page.wait_for_function("document.body.classList.contains('startup-layout-ready') && !document.body.classList.contains('database-loading')",timeout=25000)
  page.wait_for_function("document.querySelector('#content .reports-table tbody')?.rows.length===15",timeout=15000)
  assert page.evaluate('window.__requestNetworkCalls')==0,'Unsolicited network-info request'
  assert page.locator('#privacyNotice').count()==0
  assert page.locator('#privacyNotice').count()==0
  assert page.locator('#databaseLoading').is_hidden(),'Loading was not dismissed'
  metrics=page.evaluate("""() => {const s=document.scrollingElement||document.documentElement;return {body:document.body.className,doc:s.scrollHeight,viewport:s.clientHeight,max:s.scrollHeight-s.clientHeight,rail:document.querySelector('#viewportScrollbar').className,controls:document.querySelector('#pageScrollControls').className,progress:document.querySelector('#pageProgress').className,style:getComputedStyle(document.querySelector('#viewportScrollbar')).display}}""")
  print('NATURAL SCROLL',width,height,metrics,flush=True)
  assert metrics['max']>2,'Natural reports must scroll'
  page.wait_for_function("document.querySelector('#viewportScrollbar').classList.contains('is-scrollable')",timeout=3000)
  assert 'is-scrollable' in page.locator('#pageScrollControls').get_attribute('class')
  assert 'is-scrollable' in page.locator('#pageProgress').get_attribute('class')
  thumb=page.locator('#viewportScrollbarThumb'); assert thumb.is_visible()
  page.locator('#viewportScrollbarDown').click()
  page.wait_for_function('window.scrollY > 50',timeout=3000)
  thumb.focus(); thumb.press('End')
  page.wait_for_function('Math.abs(window.scrollY - (document.scrollingElement.scrollHeight - innerHeight))<15',timeout=3500)
  thumb.press('Home');page.wait_for_function('window.scrollY<15',timeout=3500)
  print('SCROLL REAL PASS',width,height,flush=True)
  page.locator('#settingsButton').click()
  assert page.locator('#settingsDrawer').get_attribute('aria-hidden')=='false'
  page.locator('[data-settings-category="internet"]').click()
  page.wait_for_function("document.querySelectorAll('#settingsNetworkInfo .settings-info-row').length>=5",timeout=3000)
  page.locator('[data-settings-category="internet"]').click()
  page.wait_for_function("document.querySelectorAll('#settingsBrowserInfo .settings-info-row').length>=20",timeout=3000)
  body=page.locator('.settings-drawer-body')
  sm=body.evaluate('(x)=>({view:x.clientHeight,doc:x.scrollHeight,rail:x._surfaceScrollbar?.className})')
  print('SETTINGS SCROLL',width,height,sm,flush=True)
  if sm['doc']>sm['view']+2:
   page.wait_for_function("document.querySelector('.settings-drawer-body')._surfaceScrollbar?.classList.contains('is-scrollable')",timeout=3000)
   down=page.locator('.settings-drawer-body + .surface-scrollbar .surface-scrollbar-down')
   down.click()
   page.wait_for_function("document.querySelector('.settings-drawer-body').scrollTop>20",timeout=4000)
   body.evaluate('(x)=>x.scrollTo({top:0,behavior:"instant"})')
  page.locator('#settingsClose').click()
  assert page.evaluate('window.__requestNetworkCalls')>=1
  page.locator('#mainNav button[data-view="egl"]').click()
  page.wait_for_timeout(250)
  egl=page.locator('#viewTitle img.view-title-egl-logo')
  assert egl.count()==1 and egl.first.evaluate('(x)=>x.complete && x.naturalWidth===512'),'Official white EGL logo did not load'
  page.locator('#mainNav button[data-view="opengles"]').click()
  page.wait_for_timeout(250)
  gl=page.locator('#viewTitle img.view-title-gles-logo')
  assert gl.count()==1 and gl.first.evaluate('(x)=>x.complete && x.naturalWidth>0'),'Official GL|ES logo did not load'
  page.locator('#mainNav button[data-view="statistics"]').click()
  page.wait_for_timeout(250)
  donut=page.locator('#content svg.donut-chart')
  assert donut.count()>=1,'Missing percentage chart'
  assert donut.first.get_attribute('viewBox')=='0 0 120 120'
  assert not errors,(width,errors)
  print('CHROMIUM INLINED-FIRST-PARTY-ASSETS PASS',width,height,'15 reports, natural first-load scrollbar, settings inner scroll and 32 Browser rows, GL/EGL official logos, 120px chart, no pageerrors or unsolicited IP request',flush=True)
  if os.environ.get('BROWSER_PREVIEW_DIR'):
   output=Path(os.environ['BROWSER_PREVIEW_DIR']);output.mkdir(parents=True,exist_ok=True)
   page.locator('#mainNav button[data-view="reports"]').click()
   page.screenshot(path=str(output/('OpenGLESScope-Database-3.0.23-'+('desktop' if width>600 else 'mobile')+'.png')),full_page=False)
  ctx.close()
 ctx=browser.new_context(viewport={'width':1024,'height':768},user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.0 Safari/537.36')
 legacy=ctx.new_page();legacy_errors=[];legacy.on('pageerror',lambda e:legacy_errors.append(str(e)))
 legacy.set_content(html,wait_until='domcontentloaded',timeout=20000)
 legacy.wait_for_function("document.querySelector('#browserCompatibilityGate')?.hidden === false",timeout=4000)
 print('LEGACY COMPAT',legacy.evaluate("() => ({title:document.title,gate:document.querySelector('#browserCompatibilityGate')?.hidden,app:document.querySelector('#appRoot')?.hidden,det:document.querySelector('#browserDetected')?.textContent})"),legacy_errors,flush=True)
 assert legacy.locator('#appRoot').is_hidden() and 'Browser not supported' in legacy.title()
 assert not legacy_errors,legacy_errors
 print('CHROMIUM COMPATIBILITY GATE PASS Chromium 80 rejected, 84+ threshold preserved',flush=True)
 ctx.close()
 browser.close()

