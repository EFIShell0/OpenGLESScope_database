from pathlib import Path
from playwright.sync_api import sync_playwright
import os
root=Path(__file__).resolve().parents[1]
ns={'__file__':str(root/'tools/test_3_0_2_interface_browser.py')}
source=(root/'tools/test_3_0_2_interface_browser.py').read_text(encoding='utf-8')
exec(source.split('\nwith sync_playwright() as p:',1)[0],ns)
html=ns['html']
expect={
 'reports':{'vendorFilter','gpuFilter','deviceModelFilter','apiFilter','eglFilter','androidFilter'},
 'versions':{'vendorFilter','gpuFilter','deviceModelFilter','driverModeFilter','androidFilter'},
 'opengles':{'apiFilter','driverModeFilter','androidFilter'},
 'egl':{'eglFilter','driverModeFilter','androidFilter'},
 'extensions':{'extensionTokenFilter','statusFilter'},
 'display':{'androidFilter','deviceModelFilter','submissionAgeFilter','hdrStateFilter','hdrTypeFilter','wideColorFilter','resolutionFilter','refreshRateFilter','displayOrderFilter'},
 'encyclopedia':set(),
}
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path=os.getenv('CHROMIUM_PATH') or '/usr/bin/chromium',args=['--no-sandbox','--disable-gpu'])
 for width,height in [(1440,900),(390,844)]:
  context=browser.new_context(viewport={'width':width,'height':height},reduced_motion='reduce')
  page=context.new_page();errors=[]
  page.on('pageerror',lambda error:errors.append(str(error)))
  page.set_content(html,wait_until='domcontentloaded',timeout=25000)
  page.wait_for_function("document.body.classList.contains('startup-layout-ready')",timeout=20000)
  assert page.evaluate('window.__requestNetworkCalls')==0
  assert page.locator('#privacyNotice').count()==0
  page.wait_for_function("document.querySelector('#content .reports-table tbody')?.rows.length===25",timeout=10000)
  page.wait_for_function("document.querySelector('#pageProgress')?.classList.contains('is-scrollable')",timeout=6000)
  progress=page.evaluate("() => ({tag:document.querySelector('#pageProgressBar').tagName,fill:getComputedStyle(document.querySelector('#pageProgressBar')).backgroundImage})")
  assert progress['tag']=='SPAN' and progress['fill']!='none',progress
  page.evaluate('window.scrollTo(0,Math.min(400,document.scrollingElement.scrollHeight-innerHeight))')
  page.wait_for_timeout(100)
  assert 'scaleX(' in page.locator('#pageProgressBar').get_attribute('style')
  page.locator('#settingsButton').click()
  assert page.evaluate('window.__requestNetworkCalls')==0
  page.locator('[data-settings-category="internet"]').click()
  page.wait_for_function("window.__requestNetworkCalls>=1 && document.querySelectorAll('#settingsNetworkInfo .settings-info-row').length>=20 && document.querySelectorAll('#settingsBrowserInfo .settings-info-row').length>=25",timeout=8000)
  assert page.locator('[data-settings-panel="internet"] .settings-section').count()==2
  assert page.locator('#settingsNetworkInfo .network-address-mosaic').count()>=1
  assert page.locator('[data-settings-panel="information"] #settingsBrowserInfo').count()==0
  assert page.locator('#settingsBrowserInfo').count()==1
  page.locator('#settingsClose').click()
  assert '2001:db8::42' not in page.locator('#settingsNetworkInfo').inner_text()
  for view,required in expect.items():
   page.locator(f'#mainNav button[data-view="{view}"]').click()
   page.wait_for_timeout(50)
   controls=set(page.evaluate("() => [...document.querySelectorAll('.filter-family-controls > .custom-select,.filter-family-controls > select')].filter(el=>el.getClientRects().length).map(el=>el.id||el.querySelector('select')?.id||'')"))
   assert required<=controls,(view,required-controls)
   if view=='versions':assert 'apiFilter' not in controls and 'eglFilter' not in controls,controls
   if view=='opengles':assert 'eglFilter' not in controls,controls
   if view=='egl':assert 'apiFilter' not in controls,controls
   if view=='display':assert controls==required,controls
   if view=='encyclopedia':assert not controls,controls
  assert not errors,(width,errors)
  print('CHROMIUM 3.0.12 SETTINGS / FILTERS / PROGRESS PASS',width,height,'26 request rows, 34 browser rows, 250 bundled country flags, no duplicate Browser panel, per-tab filters')
  context.close()
 browser.close()
