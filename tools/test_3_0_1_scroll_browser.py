from pathlib import Path
from playwright.sync_api import sync_playwright
import re
root=Path(__file__).resolve().parents[1]
source=(root/'tools/test_3_0_0_live_browser.py').read_text()
exec(source.split('with sync_playwright() as p:')[0],globals())
for name in ['scroll-system.v3020.js']:
 content='<script>'+(root/'assets'/name).read_text()+'</script>'
 html,n=re.subn(r'<script\b[^>]*src="[^\"]*'+re.escape(name)+r'(?:\?[^\"]*)?"[^>]*>\s*</script>',lambda _:content,html)
 assert n==1,(name,n)
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-gpu'])
 for width,height in [(1440,900),(390,844)]:
  ctx=browser.new_context(viewport={'width':width,'height':height},reduced_motion='reduce')
  page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.set_content(html,wait_until='domcontentloaded',timeout=20000)
  page.wait_for_function("document.body.classList.contains('startup-layout-ready')",timeout=16000)
  assert page.locator('#privacyNotice').count()==0
  page.evaluate("""() => {
    const block=document.createElement('section'); block.id='scrollProbe';block.style.minHeight='1900px';
    block.textContent='Viewport scrollbar height probe';document.querySelector('#content').appendChild(block);
  }""")
  page.wait_for_function("document.querySelector('#viewportScrollbar')?.classList.contains('is-scrollable')",timeout=8000)
  rail=page.locator('#viewportScrollbar')
  assert rail.is_visible(),f'Viewport rail hidden: {width}'
  assert rail.locator('#viewportScrollbarThumb').evaluate('(e)=>e.offsetHeight')>=40
  assert page.evaluate('document.documentElement.classList.contains("viewport-scrollbar-mounted")')
  page.locator('#viewportScrollbarDown').click()
  page.wait_for_function('window.scrollY>100',timeout=4000)
  start=page.evaluate('scrollY')
  thumb=page.locator('#viewportScrollbarThumb');thumb.focus();thumb.press('PageDown')
  page.wait_for_function('(previous)=>scrollY>previous+100',arg=start,timeout=4000)
  thumb.press('End')
  page.wait_for_function('() => Math.abs(scrollY - (document.scrollingElement.scrollHeight-innerHeight))<5',timeout=4000)
  thumb.press('Home')
  page.wait_for_function('scrollY<5',timeout=4000)
  thumb_box=thumb.bounding_box()
  assert thumb_box,(width,'Missing scroll thumb bounds')
  drag_x=thumb_box['x']+thumb_box['width']/2
  drag_y=thumb_box['y']+thumb_box['height']/2
  page.mouse.move(drag_x,drag_y)
  page.mouse.down()
  page.mouse.move(drag_x,min(height-48,drag_y+190),steps=8)
  page.mouse.up()
  page.wait_for_function('scrollY>70',timeout=4000)
  thumb.press('Home')
  page.wait_for_function('scrollY<5',timeout=4000)
  page.evaluate("""() => {
   const probe=document.querySelector('#scrollProbe');
   probe.innerHTML=`<div class="section-card" id="tableProbe"><div class="table-wrap" style="max-width:100%;overflow-x:auto">
      <table style="min-width:1450px"><thead><tr><th>Evidence</th><th>Field</th></tr></thead><tbody>
      ${Array.from({length:63},(_,i)=>`<tr><td>Row ${i+1}</td><td>Canonical GL/EGL source evidence ${i+1}</td></tr>`).join('')}
      </tbody></table></div></div>`;
  }""")
  page.wait_for_function("document.querySelector('#tableProbe .bounded-table-pagination') !== null",timeout=7000)
  assert page.locator('#tableProbe tbody tr:not([hidden])').count()==25
  assert page.locator('#tableProbe tbody tr').count()==63
  page.locator('#tableProbe .bounded-next').click()
  assert page.locator('#tableProbe .page-jump-input').input_value()=='2'
  assert page.locator('#tableProbe tbody tr:not([hidden])').count()==25
  page.locator('#tableProbe .page-jump-input').fill('3')
  page.locator('#tableProbe .page-jump-input').press('Enter')
  assert page.locator('#tableProbe tbody tr:not([hidden])').count()==13
  assert page.locator('#tableProbe .page-jump-input').input_value()=='3'
  page.locator('#tableProbe .page-jump-input').fill('999')
  page.locator('#tableProbe .page-jump-input').press('Enter')
  assert page.locator('#tableProbe .page-jump-input').input_value()=='3'
  page.locator('#tableProbe .bounded-page-size select').select_option('50')
  assert page.locator('#tableProbe tbody tr:not([hidden])').count()==50
  assert page.locator('#tableProbe .page-jump-input').input_value()=='1'
  page.wait_for_function("document.querySelector('#tableProbe .table-scroll-shell')?.classList.contains('scrollable')",timeout=7000)
  page.locator('#tableProbe .table-scroll-right').click()
  page.wait_for_function("document.querySelector('#tableProbe .table-wrap').scrollLeft>0",timeout=4000)
  page.locator('#settingsButton').click()
  page.wait_for_function("document.querySelector('.settings-drawer-body')?.dataset.surfaceScrollEnhanced==='1'",timeout=5000)
  if width<500:
   probe=page.evaluate("""() => {const h=document.querySelector('.settings-drawer-body');return {scrollHeight:h.scrollHeight,clientHeight:h.clientHeight};}""")
   assert probe['scrollHeight']>=probe['clientHeight']
   page.evaluate("""() => {const host=document.querySelector('.settings-drawer-body');const child=document.createElement('div');child.id='settingsOverflowProbe';child.style.cssText='height:1200px;min-height:1200px;flex:none';host.append(child);window.OGSScroll301.refresh();}""")
   page.wait_for_function("document.querySelector('#settingsDrawer .surface-scrollbar')?.classList.contains('is-scrollable')",timeout=5000)
   page.locator('#settingsDrawer .surface-scrollbar-down').click()
   page.wait_for_function("document.querySelector('.settings-drawer-body')?.scrollTop>25",timeout=4000)
  page.locator('#settingsClose').click()
  assert not errors,(width,errors)
  print('CHROMIUM SCROLL PASS',width,height,'viewport pointer-drag keyboard endpoints, 63-row 25/50 pagination, horizontal table scroll, settings surface')
  ctx.close()
 browser.close()
