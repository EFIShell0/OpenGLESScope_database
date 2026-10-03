from pathlib import Path
R=Path(__file__).resolve().parents[1]
w=(R/'worker/src/index.js').read_text(encoding='utf-8')
g=(R/'worker/tests/contract.mjs').read_text(encoding='utf-8')
rel=(R/'data/release.json').read_text(encoding='utf-8')
assert "const DATABASE_VERSION='3.0.22'" in w
assert "p.application.version!=='3.0.4'||p.application.versionCode!==3004" in w
assert 'requiredVersionCode:3004},403' in w
assert "(p.application.version==='3.0.2'&&p.application.versionCode===3002)" in w
assert "(p.application.version==='3.0.3'&&p.application.versionCode===3003)||(p.application.version==='3.0.4'&&p.application.versionCode===3004)" in w
assert "currentProducer:'OpenGLESScope 3.0.4'" in w
assert "function makePayload(version='3.0.4',versionCode=3004" in g
assert "'3.0.2'" in g and "'3.0.3'" in g
assert 'DELETE FROM reports' not in w and 'UPDATE reports SET' not in w
assert '"databaseVersion":"3.0.22"' in rel
print('Database 3.0.22 exact new POST 3.0.4/3004, old 3.0.2 GET-only: PASS')
