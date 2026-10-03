from pathlib import Path
from playwright.sync_api import sync_playwright
import base64,os
root=Path(__file__).resolve().parents[1]
ns={'__file__':str(root/'tools/test_3_0_2_interface_browser.py')}
source=(root/'tools/test_3_0_2_interface_browser.py').read_text(encoding='utf8')
exec(source.split('\nwith sync_playwright() as p:',1)[0],ns)
html=ns['html']
for name in ('opengles-gl-es-v030.png','egl-logo-white-v028.png'):
    data='data:image/png;base64,'+base64.b64encode((root/'assets'/name).read_bytes()).decode('ascii')
    html=html.replace('./assets/'+name,data)
with sync_playwright() as playwright:
    browser=playwright.chromium.launch(headless=True,executable_path=os.environ.get('CHROMIUM_PATH') or '/usr/bin/chromium',args=['--no-sandbox','--disable-gpu'])
    for width,height in ((1440,900),(390,844),(320,700)):
        context=browser.new_context(viewport={'width':width,'height':height},reduced_motion='reduce')
        page=context.new_page();errors=[]
        page.on('pageerror',lambda error:errors.append(str(error)))
        page.set_content(html,wait_until='domcontentloaded',timeout=30000)
        page.wait_for_function("document.body.classList.contains('startup-layout-ready')",timeout=20000)
        for tab,img,natural in [('opengles','.nav-gles-logo',144),('egl','.nav-egl-logo',512)]:
            logo=page.locator('#mainNav button[data-view="'+tab+'"] '+img)
            assert logo.count()==1,tab
            assert logo.evaluate('(e)=>e.complete && e.naturalWidth')==natural,(tab,width)
            assert logo.evaluate('(e)=>getComputedStyle(e).objectFit')=='contain'
            assert page.locator('#mainNav button[data-view="'+tab+'"]').inner_text() in ('OpenGL® ES™','EGL™')
        page.locator('#content .report-row').nth(7).scroll_into_view_if_needed()
        y=page.evaluate('window.scrollY')
        page.locator('#content .report-row').nth(7).click()
        page.wait_for_selector('#detailTabBody .detail-overview-grid',timeout=10000)
        assert page.locator('#detailTabBody .detail-section-intro').count()==0
        assert page.locator('#detailTabBody .detail-overview-section').count()==6
        assert page.locator('#detailTabBody').inner_text().find('Raw TXT')<0
        assert len(page.locator('.detail-hero .detail-report-id').inner_text())==64
        assert len(page.locator('.detail-overview-report-id .v').inner_text())==64
        size=page.evaluate('''() => {
          const hero=document.querySelector('.detail-hero .detail-report-id');
          const card=document.querySelector('.detail-overview-report-id .v');
          const h=hero.getBoundingClientRect(),c=card.getBoundingClientRect();
          const hp=hero.parentElement.getBoundingClientRect(),cp=card.parentElement.getBoundingClientRect();
          return {hero:h.right<=hp.right+2&&h.left>=hp.left-2&&hero.scrollWidth<=hero.clientWidth+2,
            card:c.right<=cp.right+2&&c.left>=cp.left-2&&card.scrollWidth<=card.clientWidth+2,
            page:document.documentElement.scrollWidth<=innerWidth+3};}''')
        assert all(size.values()),(width,size)
        back=page.locator('#detailBack')
        assert back.is_visible()
        back.click()
        page.wait_for_function("document.querySelector('#contentView')?.classList.contains('active') && !document.querySelector('#detailView')?.classList.contains('active')",timeout=7000)
        page.wait_for_timeout(110)
        assert abs(page.evaluate('window.scrollY')-y)<50,(width,y,page.evaluate('window.scrollY'))
        assert not errors,(width,errors)
        print('OVERVIEW 3.0.22 BROWSER PASS',width,height,'6 cards, canonical 64-digit ID, Back scroll, white navigation logos, no Raw TXT fallback')
        context.close()
    browser.close()
