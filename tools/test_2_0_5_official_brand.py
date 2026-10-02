from pathlib import Path
from hashlib import sha256
r=Path(__file__).resolve().parents[1]
EXPECTED={'opengles-gl-es-v030.png':'70d46d2ae6ce8392f01afdf548c4d486406a163053d135b42efe4ce3d420f952','egl-logo-white-v030.png':'945b590aebc7f48abb6a9d6cad16fe1e479568ec16d3ea8519f92f8698024b3e'}
for name,digest in EXPECTED.items():
 p=r/'assets'/name
 assert p.is_file() and sha256(p.read_bytes()).hexdigest()==digest,'OpenGLESScope 2.2.22 official artwork mismatch: '+name
h=(r/'index.html').read_text()
assert 'aria-label="OpenGL® ES™ Hardware Database"' in h
assert '<h1 aria-label="OpenGL® ES™ Hardware Database" class="hero-v127-brand-heading">OpenGL® ES™ Hardware Database</h1>' in h
js=(r/'assets/app.v3000.js').read_text()
assert "['opengles','OpenGL® ES™']" in js and "['egl','EGL™']" in js
assert 'src="./assets/opengles-gl-es-v030.png"' in js and 'src="./assets/egl-logo-white-v030.png"' in js
assert 'OPENGL® ES™ / EGL™ CAPABILITY INTELLIGENCE' in h
assert 'Complete OpenGL® ES™ and EGL™ capability evidence' in h
print('OpenGLESScope 2.2.22 exact official GL|ES and EGL artwork/typography: PASS')
