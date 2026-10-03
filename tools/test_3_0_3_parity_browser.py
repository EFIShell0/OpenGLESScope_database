from pathlib import Path
from playwright.sync_api import sync_playwright
import json,os
root=Path(__file__).resolve().parents[1]
source=(root/'tools/test_3_0_2_interface_browser.py').read_text(encoding='utf-8')
exec(source.rsplit('\nwith sync_playwright() as p:',1)[0],globals())
new_id=f'{1000:064x}'
new_row={**rows[0],'id':new_id,'submitted_at':'2026-10-02T15:59:00.000Z','gpu_name':'New Live Reference GPU','model':'New Model'}
new_detail={**row_map[rows[0]['id']],**new_row,'gpu':{'name':new_row['gpu_name'],'vendor':new_row['vendor']}}
new_seed={**seed,'reports':[new_row,*rows]}
new_head={**head,'reportCount':64,'latestReportId':new_id,'latestSubmittedAt':new_row['submitted_at'],'syncToken':'64:new'}
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path=os.environ.get('CHROMIUM_PATH') or ('/usr/bin/chromium' if Path('/usr/bin/chromium').is_file() else None),args=['--no-sandbox','--disable-gpu'])
 for width,height in [(1440,900),(390,844)]:
  ctx=browser.new_context(viewport={'width':width,'height':height},reduced_motion='reduce')
  page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.set_content(html,wait_until='domcontentloaded',timeout=30000)
  page.wait_for_function("document.body.classList.contains('startup-layout-ready')",timeout=20000)
  assert page.locator('#privacyNotice').count()==0
  page.wait_for_function("document.querySelectorAll('#metrics .metric').length===6&&document.querySelector('#metrics .metric .value')?.textContent==='63'",timeout=10000)
  assert page.locator('#databaseLoading').is_hidden()
  page.locator('#content .report-row').first.click()
  page.wait_for_selector('#detailTabBody .detail-overview-grid',timeout=10000)
  detail_tabs=page.locator('#detailContent .detail-tabs [data-tab]')
  assert detail_tabs.count()==11
  for tab in ['overview','opengles','egl','extensions','limits','formats','precision','eglconfigs','display','diagnostics','raw']:
   page.locator(f'#detailContent .detail-tabs [data-tab="{tab}"]').click()
   if tab=='overview':
    assert page.locator('#detailTabBody .detail-overview-section').count()==6,(width,tab)
    assert page.locator('#detailTabBody .detail-section-intro').count()==0,(width,tab)
   else:
    assert page.locator('#detailTabBody .detail-section-intro').count()==1,(width,tab)
    assert page.locator('#detailTabBody .detail-evidence-panel').count()>=1,(width,tab)
   if tab=='eglconfigs':assert 'EGL' in page.locator('#detailTabBody').inner_text()
   if tab=='raw':assert 'OpenGL ES test report' in page.locator('#detailTabBody').inner_text()
  page.locator('#detailBack').click()
  page.locator('#mainNav button[data-view="compare"]').click()
  page.wait_for_selector('#compareBody .compare-overview',timeout=10000)
  for selector in ['#compareStickySentinel','#compareStickyShell','.compare-workspace','#compareAMeta','#compareBMeta','#swapCompare','#compareMiniBar','#compareMinimizeToggle','#compareFilters .compare-filter-controls','#shareCompare','#compareBody .compare-section']:
   assert page.locator(selector).count()>=(1 if selector=='#compareBody .compare-section' else 1),(width,selector)
  baseline=page.locator('#compareA').input_value();candidate=page.locator('#compareB').input_value()
  assert baseline!=candidate
  page.locator('#swapCompare').click()
  page.wait_for_function('(a)=>document.querySelector("#compareA")?.value===a',arg=candidate,timeout=5000)
  assert page.locator('#compareB').input_value()==baseline
  page.locator('#compareFieldSearch').fill('GL_RENDERER')
  page.wait_for_timeout(300)
  assert page.evaluate("document.activeElement?.id")=='compareFieldSearch',(width,'search focus')
  page.locator('#compareFieldSearch').fill('')
  page.wait_for_timeout(300)
  page.locator('label.compare-diff-toggle:has(#commonOnly)').click()
  assert page.locator('#commonOnly').is_checked()
  page.wait_for_timeout(150)
  assert page.locator('#compareBody .compare-overview').count()==1
  page.locator('label.compare-diff-toggle:has(#commonOnly)').click()
  assert not page.locator('#commonOnly').is_checked()
  page.evaluate("window.scrollTo({top:document.documentElement.scrollHeight,behavior:'instant'})")
  page.wait_for_timeout(160)
  if page.evaluate('window.scrollY')>40:
   page.wait_for_function("document.querySelector('#compareStickyShell')?.classList.contains('is-pinned')",timeout=2500)
   page.locator('#compareMinimizeToggle').click()
   assert page.locator('#compareMinimizeToggle').get_attribute('aria-expanded')=='false'
   assert page.locator('#compareMiniBar').get_attribute('aria-hidden')=='false'
  page.locator('#mainNav button[data-view="reports"]').click()
  page.evaluate('''(payload)=>{const prior=window.fetch;window.fetch=async(input,options)=>{const u=String(input);if(u.includes('/v1/sync'))return new Response(JSON.stringify(payload.head),{status:200,headers:{'content-type':'application/json'}});if(u.includes('/v1/reports?'))return new Response(JSON.stringify(payload.seed),{status:200,headers:{'content-type':'application/json'}});if(u.includes('/v1/reports/'+payload.id))return new Response(JSON.stringify(payload.detail),{status:200,headers:{'content-type':'application/json'}});return prior(input,options)}}''',{'seed':new_seed,'head':new_head,'detail':new_detail,'id':new_id})
  assert page.evaluate('window.__OGS30__.refreshLive()') is True
  page.wait_for_function("window.__OGS30__.getCount()===64&&document.querySelector('#metrics .metric .value')?.textContent==='64'",timeout=13000)
  page.wait_for_function("document.querySelector('#newReportToast .new-report-toast-title')?.textContent==='1 new report added'",timeout=5000)
  assert 'New Live Reference GPU' in page.locator('#content').inner_text()
  assert not errors,(width,errors)
  print('CHROMIUM 3.0.17 PARITY PASS',width,height,'6 hero metrics, 11 evidence tabs, A/B compare swap/filter/pin/minimize, 64th live report+toast')
  ctx.close()
 browser.close()
