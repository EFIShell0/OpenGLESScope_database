"""Shared VulkanScope 1.4.12 contract translated to OpenGL ES/EGL, with privacy negative assertions."""
from pathlib import Path
import re
root=Path(__file__).resolve().parents[1]
app=(root/'assets/app.v3021.js').read_text()
css=(root/'assets/site.v3021.css').read_text()
ux=(root/'assets/experience.v3021.js').read_text()
html=(root/'index.html').read_text()
compat=(root/'assets/browser-compat.v3021.js').read_text()
ref_compat=(root/'rules/SHARED_BROWSER_COMPAT_1_4_12_REFERENCE.js').read_text()
assert compat.replace('OPENGLESSCOPE','VULKANSCOPE').replace('OpenGLESScope','VulkanScope')==ref_compat, 'Unsupported-browser algorithm differs from reference'
assert 'id="browserCompatibilityGate"' in html and 'Chromium 84+ · Firefox 86+ · Safari 14.1+' in html
assert 'id="privacyNotice"' not in html and 'privacy()' not in ux and 'localStorage.setItem' not in ux
assert 'Cookie and storage policy' in ux and 'Remember on this device' in html
assert "rememberKey='openglesscopeDatabaseRememberLocalState.v1'" in app
assert 'safeLocal(\'get\',rememberKey)' in app and 'favorites.size<500' in app
assert 'return safeLocal(\'get\',rememberKey)===\'1\'' in app
assert 'Local storage is unavailable or blocked.' in app
for term in ["const validPageJumpValue=",'const pageJumpMarkup=','function syncPageJumpUi','function bindPageJump','function enhanceSelect(sel)','function enhanceLegacyPageJumps','matches.slice(start,start+50)','custom-select-search-clear','custom-select-page-jump','page-jump-go','PageDown','PageUp','MutationObserver(refresh)','enhanceLegacyPageJumps(document)']:
 assert term in app,term
assert 'document.cookie=' not in app+ux
assert '.custom-select-menu.is-searchable .custom-select-scroll' in css and '.og-page-jump' in css
assert '@media(max-width:760px)' in css and '@media(max-width:430px)' in css and '@media(prefers-reduced-motion:reduce)' in css
assert all(x in app for x in ['[10,25,50]','renderPrecision()','renderEncyclopedia()','bindCohort('])
assert 'CURRENT_PRODUCER' not in ux
print('OpenGLESScope Database 3.0.21 compatibility, complete filter pager, reduced-motion, opt-in storage negative contract: PASS')
