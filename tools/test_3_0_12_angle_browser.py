from pathlib import Path
from playwright.sync_api import sync_playwright
import base64,os
root=Path(__file__).resolve().parents[1]
source=(root/'tools/test_3_0_2_interface_browser.py').read_text(encoding='utf8')
renderer='ANGLE (Qualcomm, Vulkan 1.3.284 (Adreno (TM) 710 (0x07010000)), Qualcomm Technologies Inc. Adreno Vulkan Driver-512.800.70)'
patch="""selected=rows[59];selected['gpu_name']=RENDERER;selected['vendor']='Google Inc. (Qualcomm)';selected['driver_version']='Unavailable (OpenGL ES does not expose a standardized driver-version query)';selected['opengles_version']='OpenGL ES 3.1.0 (ANGLE 2.1 git hash: 1166eec4c0b125e9e945196acfc549983ef72b18)';chosen=row_map[selected['id']];chosen['gpu']={'name':selected['gpu_name'],'vendor':selected['vendor']};chosen['driver']={'mode':'System OpenGL ES/EGL','version':selected['driver_version']};chosen['opengles']['version']=selected['opengles_version'];chosen['egl']['initializedVersion']='1.5'\n""".replace('RENDERER',repr(renderer))
patch+="software=rows[58];software['gpu_name']='ANGLE (Google, Vulkan 1.3.284 (Google SwiftShader Device))';software['vendor']='Google Inc. (Google SwiftShader)';row_map[software['id']]['gpu']={'name':software['gpu_name'],'vendor':software['vendor']}\n"
source=source.replace("seed={'schemaVersion':2",patch+"seed={'schemaVersion':2",1)
ns={'__file__':str(root/'tools/test_3_0_2_interface_browser.py')}
exec(source.split('\nwith sync_playwright() as p:',1)[0],ns)
html=ns['html'];report_id=f'{60:064x}'
for name in ('opengles-gl-es-v030.png','egl-logo-white-v028.png'):
 data='data:image/png;base64,'+base64.b64encode((root/'assets'/name).read_bytes()).decode('ascii')
 html=html.replace('./assets/'+name,data)
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path=os.environ.get('CHROMIUM_PATH') or '/usr/bin/chromium',args=['--no-sandbox','--disable-gpu'])
 for width,height in ((1440,900),(390,844),(320,700)):
  ctx=browser.new_context(viewport={'width':width,'height':height},reduced_motion='reduce')
  page=ctx.new_page();errors=[];page.on('pageerror',lambda x:errors.append(str(x)))
  page.set_content(html,wait_until='domcontentloaded',timeout=30000)
  page.wait_for_function("document.body.classList.contains('startup-layout-ready')",timeout=25000)
  row=page.locator(f'#content .report-row[data-id="{report_id}"]')
  assert row.count()==1,('row',width)
  software=page.locator(f'#content .report-row[data-id=\"{59:064x}\"]')
  assert software.locator('.gpu-logo-cell img').get_attribute('src').endswith('gpu_vendor_unknown.png')
  assert 'Adreno (TM) 710' in row.locator('.gpu-name-text').inner_text()
  assert row.locator('.gpu-logo-cell img').get_attribute('src').endswith('gpu_vendor_qualcomm.png')
  row.click()
  page.wait_for_selector('#detailTabBody .detail-overview-grid',timeout=10000)
  assert page.locator('.detail-hero h1').inner_text()=='Adreno (TM) 710'
  assert page.locator('.detail-hero .eyebrow').inner_text()=='Google LLC (Qualcomm)'
  assert 'ANGLE · Vulkan 1.3.284 backend' in page.locator('.detail-hero-chips').inner_text()
  assert page.locator('.detail-identity-card').nth(2).locator('strong').inner_text()=='Unavailable'
  assert 'OpenGL ES 3.1.0' in page.locator('.detail-identity-card').nth(3).locator('strong').inner_text()
  overview=page.locator('#detailTabBody').inner_text()
  assert 'GL_VENDOR (REPORTED)' in overview and 'Google Inc. (Qualcomm)' in overview,(width,overview[:2200])
  assert 'GL_RENDERER (REPORTED)' in overview and renderer in overview
  assert 'ANGLE BACKEND' in overview and 'Vulkan 1.3.284' in overview
  assert page.locator('#detailTabBody .detail-overview-section .kv .v').first.evaluate('(e)=>getComputedStyle(e).fontFamily').lower().find('mono')>=0
  assert page.locator('#mainNav button[data-view="opengles"]').inner_text()=='OpenGL® ES™'
  assert page.locator('#mainNav button[data-view="egl"]').inner_text()=='EGL™'
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+3'),('overflow',width)
  page.locator('.detail-tabs button[data-tab="opengles"]').click()
  page.wait_for_timeout(80)
  assert renderer in page.locator('#detailTabBody').inner_text()
  assert 'Google Inc. (Qualcomm)' in page.locator('#detailTabBody').inner_text()
  assert not errors,(width,errors)
  print('ANGLE OVERVIEW CHROMIUM PASS',width,height,'Qualcomm logo, Google LLC derived display, raw GL strings, Vulkan backend, restored trademarks, matched font')
  ctx.close()
 browser.close()
