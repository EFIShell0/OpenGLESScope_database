from pathlib import Path
from playwright.sync_api import sync_playwright
import os
ROOT=Path(__file__).resolve().parents[1]
ns={'__file__':str(ROOT/'tools/test_3_0_0_live_browser.py')}
src=(ROOT/'tools/test_3_0_0_live_browser.py').read_text(encoding='utf-8')
exec(src.split('with sync_playwright() as p:')[0],ns)
html=ns['html']
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path=os.environ.get('CHROMIUM_PATH') or '/usr/bin/chromium',args=['--no-sandbox','--disable-gpu'])
 for width,height in [(1440,900),(390,844),(320,700)]:
  ctx=browser.new_context(locale='en-TR',timezone_id='Europe/Istanbul',viewport={'width':width,'height':height},reduced_motion='reduce')
  page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  def route_flag(route):
   name=route.request.url.split('/')[-1];p=ROOT/'assets/country-flags'/name
   route.fulfill(status=200,content_type='image/png',body=p.read_bytes()) if p.is_file() else route.fulfill(status=404)
  page.set_content(html,wait_until='domcontentloaded',timeout=25000)
  page.wait_for_function("document.body.classList.contains('startup-layout-ready')",timeout=18000)
  page.locator('#settingsButton').click();page.locator('[data-settings-category="preferences"]').click()
  assert page.locator('#settingsRegionalCountry option').count()==251
  auto=page.locator('#settingsRegionalCountry option').first.inner_text()
  assert 'TR' in auto and 'Browser / system region' in auto,(width,auto)
  assert 'Europe/Istanbul' in page.locator('#settingsRegionalTimeZone option').first.inner_text()
  preview=page.locator('#settingsRegionalPreview').inner_text()
  assert 'TR' in preview and 'Standard / winter offset' in preview and 'Daylight / summer offset' in preview,(width,preview)
  page.locator('#settingsRegionalMode').select_option('country')
  sel=page.locator('#settingsRegionalCountry').locator('xpath=..');sel.locator('.custom-select-button').click()
  assert sel.locator('.custom-select-option').count()==50
  imgs=sel.locator('.custom-select-option img.filter-country-flag')
  assert imgs.count()==50,(width,imgs.count())
  first=imgs.first;first.wait_for(state='attached')
  assert first.get_attribute('src').endswith('.png')
  assert all((ROOT/x.get_attribute('src').replace('./','')).is_file() for x in imgs.all())
  scroll=sel.locator('.custom-select-scroll');scroll.hover();page.mouse.wheel(0,240);page.wait_for_timeout(130)
  assert sel.locator('.custom-select-menu').is_visible(),(width,'closed on wheel')
  bbox=scroll.bounding_box();assert bbox,bbox
  x=bbox['x']+bbox['width']-3;y=bbox['y']+min(45,bbox['height']/3)
  page.mouse.move(x,y);page.mouse.down();page.mouse.move(x,y+min(65,bbox['height']/3),steps=6);page.mouse.up();page.wait_for_timeout(110)
  assert sel.locator('.custom-select-menu').is_visible(),(width,'closed on drag release')
  sel.locator('.custom-select-page-next').click()
  assert sel.locator('.page-jump-input').input_value()=='2'
  sel.locator('.custom-select-search').fill('TR')
  assert 0<sel.locator('.custom-select-option').count()<=50
  sel.locator('.custom-select-search-clear').click()
  assert sel.locator('.custom-select-option').count()==50
  page.locator('#settingsClose').click()
  page.locator('#mainNav button[data-view="encyclopedia"]').click()
  page.wait_for_selector('.registry-workspace .encyclopedia-stat-strip',timeout=12000)
  assert page.locator('.encyclopedia-category').count()==8
  assert page.locator('.registry-entry').count()==24
  assert page.locator('.encyclopedia-stat-strip strong').all_text_contents()==['1233','3430','70','517','11']
  search=page.locator('#registrySearch');search.fill('eglInitialize');page.wait_for_timeout(180)
  assert page.evaluate('document.activeElement?.id')=='registrySearch'
  assert page.locator('.registry-entry').first.locator('h3').inner_text()=='eglInitialize'
  page.locator('.encyclopedia-category',has_text='EGL').click()
  assert page.locator('.registry-entry').first.locator('h3').inner_text()=='eglInitialize'
  search.fill('GL_MAX_TEXTURE_SIZE');page.wait_for_timeout(170)
  page.locator('.encyclopedia-category',has_text='Tokens').click()
  assert any('GL_MAX_TEXTURE_SIZE' in t for t in page.locator('.registry-entry h3').all_text_contents())
  if width<500:assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 3'),(width,page.evaluate('[document.documentElement.scrollWidth,innerWidth]'))
  assert not errors,(width,errors)
  print('CHROMIUM 3.0.25 REGION + FLAG + MENU WHEEL/DRAG + ENCYCLOPEDIA PASS',width,height,flush=True)
  ctx.close()
 browser.close()
