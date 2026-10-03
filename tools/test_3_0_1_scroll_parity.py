from pathlib import Path
import hashlib,json,re
from html.parser import HTMLParser
root=Path(__file__).resolve().parents[1]
app=(root/'assets/app.v3023.js').read_text()
css=(root/'assets/site.v3023.css').read_text()
scroll=(root/'assets/scroll-system.v3023.js').read_text()
html=(root/'index.html').read_text()
vk_scroll=(root/'rules/SHARED_SCROLL_1_4_12_REFERENCE.js').read_text()
assert hashlib.sha256(vk_scroll.encode()).hexdigest()==(root/'rules/SHARED_SCROLL_1_4_12_SHA256.txt').read_text().strip()
assert vk_scroll.strip() in scroll,'Reference viewport and surface scrollbar logic mutated'
for key in ['syncViewportScrollbar','initViewportScrollbar','syncSurfaceScrollbar','enhanceKnownSurfaceScrollbars','queueAllSurfaceScrollbars','viewportScrollMetrics','ResizeObserver','MutationObserver','pointerdown','pointermove','pointercancel','ArrowUp','PageDown','Home','End','is-scrollable']:
 assert key in scroll,key
assert "window.OGSScroll301=Object.freeze" in scroll
assert "const smooth=()=>prefersReducedMotion()?'auto':'smooth';const up=()=>window.scrollTo({top:0" not in app,'conflicting legacy scrollbar handlers returned'
for token in ['id="navScrollLeft"','id="navScrollRight"','id="viewportScrollbarThumb"','id="pageScrollUp"','id="pageScrollDown"','id="viewportScrollbarTrack"','scroll-system.v3023.js?v=3023']:
 assert token in html,token
assert 'id="navLeft"' not in html and 'id="navRight"' not in html
for token in ['html.viewport-scrollbar-mounted','surface-scroll-host','.viewport-scrollbar.is-scrollable','.surface-scrollbar.is-scrollable','.table-scroll-shell','.table-scroll-controls','.page-scroll-controls.is-scrollable']:
 assert token in css,token
assert '.page-scroll-controls.is-scrollable:not(.is-active){visibility:hidden;opacity:0;pointer-events:none' not in css
assert '--accent:#ba2a8d' in css and '--red:#ff8f98' in css and '--green:#74e2a6' in css
assert '.coverage.unsupported{--coverage-spray:var(--red);--coverage-spray-soft:rgba(255,143,152,.42)}' in css
assert 'rgba(255,143,220,.42)' not in css and 'rgba(255,143,220,.22)' not in css
ref=json.loads((root/'rules/SHARED_ICON_1_4_12_REFERENCE.json').read_text())
def icons(s):
 raw=s.split('const ICON_PATHS={',1)[1].split('};',1)[0]
 return dict(re.findall(r"(\w+):'([^']*)'",raw))
current=icons(app)
for key in set(current)&set(ref):
 assert current[key]==ref[key],f'Shared SVG path mismatch: {key}'
assert len(set(current)&set(ref))>=10
for token in ['bounded-table-pagination','page-jump-input','bounded-page-size','aria-live','rows[i].hidden','pageSize=25','pageSize=[10,25,50]','valid=v=>','paint(-1)','paint(1)','!prefersReducedMotion()']:
 assert token in scroll,token
assert 'technicalReportSchema:5' in (root/'worker/src/index.js').read_text()
assert "p.application.version!=='3.0.4'||p.application.versionCode!==3004" in (root/'worker/src/index.js').read_text()
def source_ok(value):
 return vk_scroll.strip() in value and 'initViewportScrollbar();' in value and 'window.OGSScroll301=' in value
assert source_ok(scroll)
assert not source_ok(scroll.replace('initViewportScrollbar();','',1))
assert not source_ok(scroll.replace('const syncViewportScrollbar=','const brokenViewport=',1))
print('OpenGLESScope Database 3.0.23 exact reference-scroll, neutral-semantic-color, common SVG and bounded-table gates: ALL PASS')
