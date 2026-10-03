from pathlib import Path
from playwright.sync_api import sync_playwright
import os
root=Path(__file__).resolve().parents[1]
source=(root/'tools/test_3_0_2_interface_browser.py').read_text(encoding='utf-8')
ns={'__file__':str(root/'tools/test_3_0_2_interface_browser.py')}
exec(source.split('\nwith sync_playwright() as p:',1)[0],ns)
html=ns['html']
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path=os.getenv('CHROMIUM_PATH') or '/usr/bin/chromium',args=['--no-sandbox','--disable-gpu'])
 for width,height in [(1440,900),(390,844),(320,760)]:
  context=browser.new_context(viewport={'width':width,'height':height},reduced_motion='reduce')
  page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.set_content(html,wait_until='domcontentloaded',timeout=30000)
  page.wait_for_function("document.body.classList.contains('startup-layout-ready')",timeout=20000)
  page.locator('#settingsButton').click()
  page.locator('[data-settings-category="information"]').click()
  notice=page.locator('#settingsInformation')
  assert 'not affiliated with the Khronos Group' in notice.inner_text()
  assert 'official Khronos Group project' in notice.inner_text()
  assert '3.0.13' in notice.inner_text()
  assert '0 third-party runtime libraries' in notice.inner_text()
  assert 'Wrangler 4.146.0' in notice.inner_text()
  assert notice.locator('.settings-release-summary>div').count()==3
  assert notice.locator('.settings-library-card').count()>=9
  assert notice.locator('.settings-library-card dl>div').count()>=27
  assert notice.locator('[data-license-name="OpenGLESScope application"]').count()==1
  page.locator('[data-settings-category="favorites"]').click()
  assert 'Favorites are session-only' in page.locator('#settingsFavoritesPersistence').inner_text()
  assert 'No favorite reports yet.' in page.locator('#favoriteItems').inner_text()
  page.locator('#settingsClose').click()
  page.locator('#content .report-favorite').first.click()
  page.locator('#settingsButton').click()
  page.locator('[data-settings-category="favorites"]').click()
  assert page.locator('#favoriteItems .settings-favorite-item').count()==1
  assert page.locator('#favoriteItems .settings-favorite-open strong').count()==1
  assert page.locator('#favoriteItems .settings-favorite-open span').count()==1
  page.locator('#favoriteItems .settings-favorite-remove').click()
  assert 'No favorite reports yet.' in page.locator('#favoriteItems').inner_text()
  assert not errors,(width,errors)
  print('CHROMIUM 3.0.13 INFORMATION / KHRONOS / LICENSES / FAVORITES PASS',width,height)
  context.close()
 browser.close()
