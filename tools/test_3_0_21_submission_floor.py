from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
w=(R/'worker/src/index.js').read_text(encoding='utf-8')
g=(R/'worker/tests/contract.mjs').read_text(encoding='utf-8')
release=json.loads((R/'data/release.json').read_text(encoding='utf-8'))
assert release=={'schemaVersion':2,'databaseVersion':'3.0.27','releaseReady':False,'appAsset':'assets/app.v3027.js','cacheKey':'3027'}
assert "const DATABASE_VERSION='3.0.27'" in w
assert "p.application.version!=='3.0.7'||p.application.versionCode!==3007" in w
assert 'requiredVersionCode:3007},403' in w
assert "currentProducer:'OpenGLESScope 3.0.7'" in w
for v,code in [('3.0.0',3000),('3.0.1',3001),('3.0.2',3002),('3.0.3',3003),('3.0.4',3004)]:
 assert "(p.application.version===\'{}\'&&p.application.versionCode==={})".format(v,code) in w
assert "function makePayload(version='3.0.7',versionCode=3007" in g
assert 'reject complete previous 3.0.3 on 3.0.4 POST gate' in g
assert 'DELETE FROM reports' not in w and 'UPDATE reports SET' not in w
print('Database 3.0.27 exact current-only 3.0.7/3007 POST, historical-read contract: PASS')
