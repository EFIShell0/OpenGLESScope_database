"""New GL-only precision, full filter pagination and regional time browser coverage."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import os,json
root=Path(__file__).resolve().parents[1]
source=(root/'tools/test_3_0_2_interface_browser.py').read_text(encoding='utf8')
ns={'__file__':str(root/'tools/test_3_0_2_interface_browser.py')}
exec(source.split('\nwith sync_playwright() as p:',1)[0],ns)
precision=[{'shader':f'GL_{shader}_SHADER','type':f'GL_{level}_{kind}','rangeMin':-126,'rangeMax':127,'precision':23 if kind=='FLOAT' else 0} for shader in ('VERTEX','FRAGMENT') for kind in ('FLOAT','INT') for level in ('LOW','MEDIUM','HIGH')]
html=ns['html'].replace('"precision": []','"precision": '+json.dumps(precision))
assert html.count('"precision": []')==0 and html.count('"precision": [{')==63
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path=os.getenv('CHROMIUM_PATH') or '/usr/bin/chromium',args=['--no-sandbox','--disable-gpu'])
 for width,height in [(1440,900),(390,844)]:
  ctx=browser.new_context(viewport={'width':width,'height':height},reduced_motion='reduce')
  page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.set_content(html,wait_until='domcontentloaded',timeout=30000)
  page.wait_for_function("document.body.classList.contains('startup-layout-ready')",timeout=25000)
  assert page.locator('#privacyNotice').count()==0
  page.locator('#mainNav button[data-view="precision"]').click()
  page.wait_for_selector('#precisionTypeFilter',timeout=25000)
  assert page.locator('#content .precision-workspace h3').inner_text()=='Shader Precision'
  assert page.locator('#subGroup option').all_text_contents()==['All shader stages','Vertex shader','Fragment shader']
  assert page.locator('#content .precision-results tbody tr').count()==12
  page.locator('#subGroup').select_option('fragment')
  page.wait_for_function("document.querySelectorAll('#content .precision-results tbody tr').length === 6",timeout=25000)
  assert 'VERTEX' not in page.locator('#content .precision-results tbody').inner_text()
  page.locator('#precisionTypeFilter').select_option('float')
  page.wait_for_function("document.querySelectorAll('#content .precision-results tbody tr').length === 3",timeout=25000)
  assert 'INT' not in page.locator('#content .precision-results tbody').inner_text()
  page.locator('#precisionRowSearch').fill('HIGH')
  page.wait_for_function("document.querySelectorAll('#content .precision-results tbody tr').length === 1",timeout=25000)
  assert 'HIGH_FLOAT' in page.locator('#content .precision-results tbody').inner_text()
  page.locator('#precisionPageInput').fill('999')
  page.locator('#precisionPageInput').press('Enter')
  assert page.locator('#precisionPageInput').input_value()=='1'
  page.locator('#settingsButton').click()
  page.locator('[data-settings-category="preferences"]').click()
  assert page.locator('#settingsRegionalPreview').count()==1
  preview=page.locator('#settingsRegionalPreview').inner_text()
  assert 'Standard' in preview and 'Daylight' in preview,(width,preview)
  page.locator('#settingsRegionalMode').select_option('country')
  country=page.locator('#settingsRegionalCountry')
  assert country.locator('option').count()>200
  wrap=country.locator('xpath=..')
  wrap.locator('.custom-select-button').click()
  assert wrap.locator('.custom-select-option').count()==50
  assert wrap.locator('.custom-select-page-jump .page-jump-input').input_value()=='1'
  wrap.locator('.custom-select-page-next').click()
  assert wrap.locator('.custom-select-page-jump .page-jump-input').input_value()=='2'
  assert wrap.locator('.custom-select-option').count()==50
  wrap.locator('.custom-select-search').fill('Turkey')
  assert wrap.locator('.custom-select-page-jump .page-jump-input').input_value()=='1'
  assert wrap.locator('.custom-select-option').count()<=50
  wrap.locator('.custom-select-search-clear').click()
  assert wrap.locator('.custom-select-option').count()==50
  page.locator('#settingsClose').click()
  page.evaluate("""() => {window.__previousWorkerFetch=window.fetch;window.fetch=async (input,opts)=>String(input).includes('/v1/health?_probe=')?new Response(JSON.stringify({status:'ok',databaseVersion:'3.0.27'}),{status:200,headers:{'content-type':'application/json'}}):window.__previousWorkerFetch(input,opts)}""")
  page.evaluate("document.dispatchEvent(new Event('openglesscope:connection-error'))")
  page.wait_for_function("document.querySelector('#networkStatusShell')?.dataset.state==='checking'",timeout=7000)
  page.evaluate("document.dispatchEvent(new Event('openglesscope:connection-ok'))")
  page.wait_for_timeout(100)
  assert page.locator('#networkStatusShell').get_attribute('data-state')=='checking'
  assert not errors,(width,errors)
  print('CHROMIUM 3.0.27 SHADER/FILTER/TIME PASS',width,height,'12 queried GL precision types; 50/page full native filter; regional offsets')
  ctx.close()
 browser.close()
