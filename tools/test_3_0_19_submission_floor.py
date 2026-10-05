from pathlib import Path
R=Path(__file__).resolve().parents[1]
w=(R/'worker/src/index.js').read_text(encoding='utf-8')
assert "const DATABASE_VERSION='3.0.30'" in w
assert "p.application.version!=='3.0.7'||p.application.versionCode!==3007" in w
assert 'requiredVersionCode:3007},403' in w
assert "(p.application.version==='3.0.1'&&p.application.versionCode===3001)" in w,'historical producer must remain parseable, but forbidden at POST gate'
assert "(p.application.version==='3.0.2'&&p.application.versionCode===3002)" in w
assert "(p.application.version==='3.0.3'&&p.application.versionCode===3003)||(p.application.version==='3.0.4'&&p.application.versionCode===3004)" in w
assert 'SELECT payload_json,submitted_at,id FROM reports WHERE id=?' in w
assert 'DELETE FROM reports' not in w and 'UPDATE reports SET' not in w
assert "currentProducer:'OpenGLESScope 3.0.7'" in w
print('3.0.30 producer floor exact 3.0.3/3003, historical read-only integrity: PASS')
