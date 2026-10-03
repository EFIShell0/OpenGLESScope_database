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
    for w,h in [(1440,900),(900,390),(390,844),(320,700)]:
        context=browser.new_context(viewport={'width':w,'height':h},reduced_motion='reduce')
        page=context.new_page(); errors=[]
        page.on('pageerror',lambda error:errors.append(str(error)))
        page.set_content(html,wait_until='domcontentloaded',timeout=25000)
        page.wait_for_function("document.body.classList.contains('startup-layout-ready')",timeout=20000)
        for repeat in range(2):
            page.locator('#mainNav button[data-view="encyclopedia"]').click()
            page.locator('#registrySearch').wait_for(state='visible',timeout=15000)
            search=page.locator('#registrySearch')
            search.fill('eglInitialize')
            page.wait_for_timeout(180)
            clear=page.locator('.encyclopedia-search-shell > .search-clear-button')
            assert clear.count()==1,(w,h,'duplicate X buttons',clear.count())
            assert page.locator('.encyclopedia-search-shell .og-search-clear').count()==0,(w,h,'enhancer injected duplicate')
            assert clear.first.get_attribute('id')=='registrySearchClear'
            assert clear.first.is_visible(),(w,h,'missing X button')
            clear.first.click()
            assert search.input_value()=='',(w,h,'clear failed')
            assert page.evaluate('document.activeElement?.id')=='registrySearch',(w,h,'focus lost')
            assert clear.count()==1,(w,h,'X count changed on clear')
            page.wait_for_function("document.getElementById('registrySearchClear')?.getAttribute('aria-hidden')==='true'",timeout=3000)
            assert clear.first.get_attribute('aria-hidden')=='true',(w,h,'empty-input X still active')
            assert not errors,(w,h,errors)
            page.locator('#mainNav button[data-view="reports"]').click()
        print(f'CHROMIUM PASS {w}x{h}: exactly one X after typing, clearing, route re-entry; focus retained',flush=True)
        context.close()
    browser.close()
