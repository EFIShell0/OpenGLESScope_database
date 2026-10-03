from pathlib import Path
import re
r=Path(__file__).resolve().parents[1]
s=(r/'assets/app.v3023.js').read_text()
w=(r/'worker/src/index.js').read_text()
h=(r/'index.html').read_text()
d=(r/'data/index.json').read_text()
assert "const DATABASE_VERSION='3.0.23'" in s
assert "const DATABASE_VERSION='3.0.23'" in w
for t in ["x.databaseVersion!==DATABASE_VERSION","sync?.databaseReleaseVersion!==DATABASE_VERSION","currentHealth?.databaseVersion!==DATABASE_VERSION","head.value.databaseVersion!==DATABASE_VERSION"]:
 assert t in s,t
assert s.count('databaseVersion!==DATABASE_VERSION')>=3
assert 'No verified offline reports' in s
assert not re.search(r"database(?:Release)?Version\s*!==\s*['\"]2\.0\.[0-9]+['\"]",s),'hardcoded frontend release/version mismatch regression'
assert 'app.v3023.js' in h and 'site.v3023.css' in h and 'config.js?v=3023' in h
assert '"databaseVersion":"3.0.23"' in d
assert "p.application.version!=='3.0.4'||p.application.versionCode!==3004" in w
assert "requiredVersionCode:3004},403" in w
assert "compatibleProducer:'OpenGLESScope 3.0.4 (versionCode 3004) for new submissions only" in w
for source,changed in [(s,s.replace('currentHealth?.databaseVersion!==DATABASE_VERSION',"currentHealth?.databaseVersion!=='2.0.3'")),(s,s.replace('x.databaseVersion!==DATABASE_VERSION',"x.databaseVersion!=='2.0.3'",1)),(w,w.replace("p.application.version!=='3.0.4'||p.application.versionCode!==3004","p.application.version!=='2.2.22'||p.application.versionCode!==2222"))]:
 try:
  if source==w:
   assert "p.application.version!=='3.0.4'||p.application.versionCode!==3004" in changed
  else:
   assert not re.search(r"database(?:Release)?Version\s*!==\s*['\"]2\.0\.[0-9]+['\"]",changed)
 except AssertionError:
  continue
 raise AssertionError('Negative mutation escaped release/producer handshake')
print('OpenGLESScope Database 3.0.23 release handshake and current-only POST negative mutations: ALL PASS')
