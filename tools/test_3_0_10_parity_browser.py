"""VulkanScope-aligned mobile filter, pager, opt-in persistence, compatibility UI smoke test."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import os
root=Path(__file__).resolve().parents[1]
source=(root/'tools/test_3_0_2_interface_browser.py').read_text(encoding='utf-8')
ns={'__file__':str(root/'tools/test_3_0_2_interface_browser.py')}
exec(source.split('\nwith sync_playwright() as p:',1)[0],ns)
html=ns['html']
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path=os.getenv('CHROMIUM_PATH','/usr/bin/chromium'),args=['--no-sandbox','--disable-gpu'])
 for width,height in [(1440,900),(390,844),(320,700)]:
  ctx=browser.new_context(viewport={'width':width,'height':height},reduced_motion='reduce')
  page=ctx.new_page();errors=[];page.on('pageerror',lambda e: errors.append(str(e)))
  page.evaluate("""() => {const values=new Map();Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem:k=>values.has(k)?values.get(k):null,setItem:(k,v)=>values.set(String(k),String(v)),removeItem:k=>values.delete(k),clear:()=>values.clear()}})}""")
  page.set_content(html,wait_until='domcontentloaded',timeout=30000)
  page.wait_for_function("document.body.classList.contains('startup-layout-ready')",timeout=20000)
  assert page.locator('#privacyNotice').count()==0
  assert page.evaluate("localStorage.getItem('openglesscopeDatabaseRememberLocalState.v1')") is None
  page.locator('#reportNext').click()
  assert page.locator('#reportPageInput').input_value()=='2'
  pager=page.locator('#content .reports-pagination').first
  assert pager.locator('.page-jump-go').count()==1
  page.locator('#reportPageInput').fill('3')
  pager.locator('.page-jump-go').click()
  assert page.locator('#reportPageInput').input_value()=='3'
  page.locator('#reportPageInput').fill('999')
  page.locator('#reportPageInput').press('Enter')
  assert page.locator('#reportPageInput').input_value()=='3'
  page.locator('#content .report-favorite').first.click()
  before=page.locator('#content .report-favorite').first.get_attribute('aria-pressed')
  assert before=='true'
  assert page.evaluate("localStorage.getItem('openglesscopeDatabaseFavorites.v1')") is None
  page.set_content(html,wait_until='domcontentloaded',timeout=30000)
  page.wait_for_function("document.body.classList.contains('startup-layout-ready')",timeout=20000)
  assert page.locator('#content .report-favorite').first.get_attribute('aria-pressed')=='false'
  page.locator('#settingsButton').click()
  page.locator('[data-settings-category="preferences"]').click()
  box=page.locator('#rememberDevice')
  assert not box.is_checked()
  page.locator('label.settings-toggle-prominent').click()
  assert box.is_checked()
  assert page.evaluate("localStorage.getItem('openglesscopeDatabaseRememberLocalState.v1')")=='1'
  page.locator('#settingsRegionalMode').select_option('country')
  country=page.locator('#settingsRegionalCountry').locator('xpath=..')
  country.locator('.custom-select-button').click()
  assert country.locator('.custom-select-option').count()==50
  country.locator('.custom-select-page-next').click()
  assert country.locator('.page-jump-input').input_value()=='2'
  assert country.locator('.page-jump-go').count()==1
  country.locator('.page-jump-input').fill('3')
  country.locator('.page-jump-go').click()
  assert country.locator('.page-jump-input').input_value()=='3'
  country.locator('.custom-select-search').fill('United')
  assert country.locator('.custom-select-option').count()>=1
  assert country.locator('.page-jump-input').input_value()=='1'
  country.locator('.custom-select-search-clear').click()
  assert country.locator('.custom-select-option').count()==50
  page.locator('#settingsClose').click()
  page.locator('#reportPageSize').select_option('50')
  assert page.locator('#reportPageSize').input_value()=='50'
  page.locator('#content .report-favorite').first.click()
  assert page.locator('#content .report-favorite').first.get_attribute('aria-pressed')=='true'
  page.set_content(html,wait_until='domcontentloaded',timeout=30000)
  page.wait_for_function("document.body.classList.contains('startup-layout-ready')",timeout=20000)
  assert page.locator('#content .report-favorite').first.get_attribute('aria-pressed')=='true'
  assert page.locator('#reportPageSize').input_value()=='50'
  page.locator('#settingsButton').click()
  page.locator('[data-settings-category="preferences"]').click()
  box=page.locator('#rememberDevice');assert box.is_checked();page.locator('label.settings-toggle-prominent').click()
  assert page.evaluate("localStorage.getItem('openglesscopeDatabaseRememberLocalState.v1')") is None
  page.evaluate("() => {localStorage.setItem=()=>{throw new DOMException('Blocked','SecurityError')}; return true}")
  page.locator('label.settings-toggle-prominent').click()
  assert not box.is_checked()
  assert 'blocked' in page.locator('#settingsStorageStatus').inner_text().lower()
  page.locator('#settingsClose').click()
  if width<500:
   assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 3'),page.evaluate('[document.documentElement.scrollWidth,innerWidth]')
  assert not errors,(width,errors)
  print('BROWSER PARITY PASS',width,height,'50/filter page; search X; direct Go; remember opt-in/reload/forget; no startup consent')
  ctx.close()
 for ua,expected in [('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36','Chromium'),('Mozilla/5.0 (Windows NT 10.0; rv:80.0) Gecko/20100101 Firefox/80.0','Firefox'),('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15','Safari')]:
  ctx=browser.new_context(user_agent=ua,viewport={'width':390,'height':844})
  page=ctx.new_page();page.set_content(html,wait_until='domcontentloaded',timeout=30000)
  assert page.evaluate('window.__OPENGLESSCOPE_COMPATIBLE__') is False,(expected,page.evaluate('window.__OPENGLESSCOPE_BROWSER_INFO__'))
  assert page.locator('#browserCompatibilityGate').is_visible(),expected
  assert page.locator('#appRoot').is_hidden(),expected
  requirement={'Chromium':'84','Firefox':'86','Safari':'14.1'}[expected]
  assert requirement in page.locator('#browserRequirement').inner_text(),(expected,page.locator('#browserRequirement').inner_text())
  print('UNSUPPORTED BROWSER PASS',expected)
  ctx.close()
 browser.close()
