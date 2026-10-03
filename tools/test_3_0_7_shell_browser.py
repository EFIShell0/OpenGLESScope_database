"""Real Chromium regressions for report Overview, Back visibility and motion shell."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import os
root=Path(__file__).resolve().parents[1]
source=(root/'tools/test_3_0_2_interface_browser.py').read_text(encoding='utf8')
ns={'__file__':str(root/'tools/test_3_0_2_interface_browser.py')}
exec(source.split('\nwith sync_playwright() as p:',1)[0],ns)
html=ns['html']
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path=os.getenv('CHROMIUM_PATH') or '/usr/bin/chromium',args=['--no-sandbox','--disable-gpu'])
 for width,height in [(1440,900),(390,844),(320,760)]:
  context=browser.new_context(viewport={'width':width,'height':height},reduced_motion='no-preference',accept_downloads=True)
  page=context.new_page();errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
  page.set_content(html,wait_until='domcontentloaded',timeout=30000)
  page.wait_for_function("document.body.classList.contains('startup-layout-ready')",timeout=20000)
  assert page.locator('#databaseLoading').is_hidden()
  assert not page.locator('body').evaluate("e=>e.classList.contains('database-loading')")
  assert page.locator('#privacyNotice').count()==0
  page.wait_for_function("document.querySelector('#content .reports-table tbody')?.rows.length===25",timeout=10000)
  page.locator('#content .report-row').first.scroll_into_view_if_needed()
  before=page.evaluate('window.scrollY')
  page.locator('#content .report-row').first.click()
  page.wait_for_selector('#detailTabBody .detail-overview-grid',timeout=10000)
  assert page.locator('#detailContent .detail-tabs [data-tab]').count()==11
  assert page.locator('#detailContent .detail-tabs [data-tab="overview"]').inner_text()=='Overview'
  assert page.locator('#detailTabBody .detail-overview-section').count()==6
  assert page.locator('#detailContent .detail-hero .detail-actions').count()==1
  for action in ['detailFavorite','shareReport','copyReportLink','downloadReportJson']:
   assert page.locator('#detailContent .detail-hero #'+action).count()==1,action
  assert page.locator('#detailContent .detail-hero #downloadRawReport').count()==0
  assert page.locator('#detailFavorite svg').count()==1
  pos=page.evaluate("""() => {const head=document.querySelector('.topbar').getBoundingClientRect(),back=document.querySelector('#detailBack').getBoundingClientRect();return {headTop:head.top,headHeight:head.height,backY:back.top,backBottom:back.bottom,rootOverflow:getComputedStyle(document.documentElement).overflowX}}""")
  assert abs(pos['headTop'])<2,pos
  assert pos['backY']>=pos['headHeight']-5 and pos['backBottom']<height-30,pos
  assert pos['rootOverflow']=='clip',pos
  page.locator('#detailFavorite').click()
  assert page.locator('#detailFavorite').get_attribute('aria-pressed')=='true'
  assert page.locator('#detailFavorite path').get_attribute('fill')=='currentColor'
  page.locator('#detailFavorite').click()
  assert page.locator('#detailFavorite').get_attribute('aria-pressed')=='false'
  for tab in ['opengles','egl','extensions','limits','formats','precision','eglconfigs','display','diagnostics','raw','overview']:
   page.locator('#detailContent .detail-tabs [data-tab="'+tab+'"]').click()
   assert page.locator('#detailContent .detail-tabs [data-tab="'+tab+'"]').get_attribute('aria-selected')=='true',tab
   if tab=='raw':page.wait_for_selector('#downloadRawTabReport',timeout=5000)
  page.locator('#detailBack').click()
  page.wait_for_function("document.querySelector('#contentView')?.classList.contains('active') && !document.querySelector('#detailView')?.classList.contains('active')",timeout=7000)
  page.wait_for_timeout(200)
  assert page.evaluate('Math.abs(window.scrollY-'+str(before)+')')<35,(width,before,page.evaluate('window.scrollY'))
  assert not errors,(width,errors)
  print('CHROMIUM 3.0.17 OVERVIEW / BACK / HERO ACTIONS / STARTUP / ROUTE SCROLL PASS',width,height,'11 tabs, six sections, correct sticky header')
  context.close()
 browser.close()
