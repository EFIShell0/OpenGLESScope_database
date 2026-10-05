from pathlib import Path
r=Path(__file__).resolve().parents[1]
s=(r/'assets/app.v3028.js').read_text()
h=(r/'index.html').read_text()
assert 'gpuIdentity=(vendor,renderer)' in s
assert "rawVendor.replace(/^Google Inc\\.(?=\\s|$)/i,'Google LLC')" in s
assert "OGS_SOFTWARE_RENDERER.test(rawRenderer)" in s
assert 'gpuView=gpuIdentity' in s
assert '<div class="v">${esc(v??\'Unknown\')}</div>' in s
assert "['GL_RENDERER (reported)',p.gpu?.name]" in s
assert "['GL_VENDOR (reported)',p.gpu?.vendor]" in s
assert "['ANGLE backend',gpuIdentity" in s
assert 'OpenGL® ES™' in s+h and 'EGL™' in s+h
assert 'GL_RENDERER' in s and 'GL_VENDOR' in s
assert 'ANGLE display labels are derived' in s
print('3.0.28 ANGLE/branding source contract: PASS')
