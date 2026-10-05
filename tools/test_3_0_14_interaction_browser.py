from pathlib import Path
from playwright.sync_api import sync_playwright
import os
R=Path(__file__).resolve().parents[1]
src=(R/'tools/test_3_0_0_live_browser.py').read_text(encoding='utf-8')
ns={'__file__':str(R/'tools/test_3_0_0_live_browser.py')}
exec(src.split('with sync_playwright() as p:')[0],ns)
html=ns['html']
with sync_playwright() as playwright:
 browser=playwright.chromium.launch(headless=True,executable_path=os.environ.get('CHROMIUM_PATH') or '/usr/bin/chromium',args=['--no-sandbox','--disable-gpu'])
 for w,h in ((1440,900),(390,844),(320,700)):
  ctx=browser.new_context(viewport={'width':w,'height':h},reduced_motion='reduce');page=ctx.new_page();errors=[]
  page.on('pageerror',lambda error:errors.append(str(error)))
  page.set_content(html,wait_until='domcontentloaded',timeout=30000)
  page.wait_for_function("document.body.classList.contains('startup-layout-ready')",timeout=20000)
  page.locator('#settingsButton').click();page.locator('[data-settings-category="information"]').click()
  info=page.locator('[data-settings-panel="information"]')
  assert info.inner_text().count('Release, runtime and dependency information for this OpenGLESScope Database build.')==1
  assert info.inner_text().count('OpenGLESScope is not affiliated with the Khronos Group')==1
  page.locator('#settingsClose').click()
  page.evaluate("document.dispatchEvent(new Event('openglesscope:release-transition'))")
  assert page.locator('#networkStatusShell').get_attribute('data-state')=='checking'
  assert page.locator('#networkStatusShell').get_attribute('aria-hidden')=='true'
  assert not page.locator('body').evaluate('(e)=>e.classList.contains("network-banner-visible")')
  page.locator('#mainNav button[data-view="encyclopedia"]').click()
  page.wait_for_selector('#registrySearch',timeout=10000)
  search=page.locator('#registrySearch');search.fill('GL_');page.wait_for_timeout(230)
  assert search.input_value()=='GL_' and page.evaluate('document.activeElement?.id')=='registrySearch'
  assert page.locator('.registry-entry').count()==24
  assert page.locator('.registry-workspace.encyclopedia-workspace').count()==1
  assert page.locator('.registry-list.encyclopedia-grid').count()==1
  search.fill('EGL_');page.wait_for_timeout(230)
  assert search.input_value()=='EGL_' and page.evaluate('document.activeElement?.id')=='registrySearch'
  assert 0<page.locator('.registry-entry').count()<=24
  assert not errors,(w,errors)
  print('CHROMIUM 3.0.30 INFORMATION / TRANSIENT STATUS / REGISTRY SEARCH PASS',w,h)
  ctx.close()
 browser.close()
