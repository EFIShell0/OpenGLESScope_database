from pathlib import Path
from hashlib import sha256
import re
r=Path(__file__).resolve().parents[1]
app=(r/'assets/app.v3014.js').read_text(encoding='utf-8')
css=(r/'assets/site.v3014.css').read_text(encoding='utf-8')
html=(r/'index.html').read_text(encoding='utf-8')
ref=(r/'rules/SHARED_UI_1_4_12_REFERENCE.css').read_bytes()
assert sha256((r/'assets/egl-logo-white-v028.png').read_bytes()).hexdigest()=='fbda474cfe9043d5907b70b9ccdb8964bc3d3fa78f707d3eccacb57042a8e01f'
assert 'egl-logo-white-v030.png' not in app and not (r/'assets/egl-logo-white-v030.png').exists()
assert app.count('eglLogo(')>=3 and app.count('glEsLogo(')>=3
assert "'hdr10_plus_v1014.png','hdr-logo-hdr10plus'" in app
assert (r/'assets/hdr/hdr10_plus_v1014.png').is_file()
assert 'ANDROID_APP_FILTER_ICON=`<svg' in app and 'fill="#3DDC84"' in app
assert sha256(re.search(r'const ANDROID_APP_FILTER_ICON=(`.*?`);',app).group(1).encode('utf-8')).hexdigest()=='035bb9b70d7ef57365a304a9eeb110b139acb51561f04cad7460617d0313824c'
assert sha256((r/'assets/hdr/hdr10_plus_v1014.png').read_bytes()).hexdigest()=='8c38222517cd48357da8a93623e3c40aa06cccc7046e806b89cf81350907aba8'
assert "key==='android'?ANDROID_APP_FILTER_ICON" in app
assert "androidFilter:'android'" in app and "const semantic={vendorFilter:'vendor',gpuFilter:'gpu'" in app
assert 'viewBox="0 0 120 120"' in app and 'stroke-dashoffset=' in app and 'class="coverage-bar"' in app
assert "document.body.classList.remove('startup-layout-hold','database-loading')" in app
assert "if(document.body?.classList.contains('database-loading'))" in (r/'assets/scroll-system.v3014.js').read_text(encoding='utf-8')
assert "try{return window.sessionStorage?'Available':'Unavailable'}catch{return'Blocked / unavailable'}" in app
assert 'if(window.__OPENGLESSCOPE_COMPATIBLE__===false)return;' in app
assert 'settings-info-grid' in app and 'settings-browser-grid' in app and 'settings-network-summary' in app
assert 'OpenGLESScope Database could not validate' in html and 'does not send browser identity to OpenGLESScope' in html
assert 'VulkanScope' not in html
for code in (400,401,403,404,405,408,409,413,415,429,500,502,503,504):
 error=(r/f'{code}.html').read_text(encoding='utf-8')
 assert '<main class="shell error-page"><section class="hero error-hero">' in error
 assert f'HTTP {code}' in error and 'OpenGLESScope Database' in error
 assert 'Open Reports' in error and 'OpenGLESScope on GitHub' in error
 assert 'VulkanScope' not in error and 'site.v3014.css?v=3014' in error
assert '.viewport-scrollbar.is-scrollable' in css and '.surface-scrollbar.is-scrollable' in css
assert (r/'assets/browser-compat.v3014.js').read_text(encoding='utf-8').replace('OPENGLESSCOPE','VULKANSCOPE').replace('OpenGLESScope','VulkanScope')==(r/'rules/SHARED_BROWSER_COMPAT_1_4_12_REFERENCE.js').read_text(encoding='utf-8') if (r/'rules/SHARED_BROWSER_COMPAT_1_4_12_REFERENCE.js').exists() else True
print('OpenGLESScope Database 3.0.14 real scroll completion, white EGL, Android, HDR10+, coverage and Settings: PASS')
