from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
w=(R/'worker/src/index.js').read_text(encoding='utf-8')
g=(R/'worker/tests/contract.mjs').read_text(encoding='utf-8')
release=json.loads((R/'data/release.json').read_text(encoding='utf-8'))
assert release=={'schemaVersion':2,'databaseVersion':'3.0.25','releaseReady':False,'appAsset':'assets/app.v3025.js','cacheKey':'3025'}
assert "const DATABASE_VERSION='3.0.25'" in w
assert "p.application.version!=='3.0.5'||p.application.versionCode!==3005" in w
assert 'requiredVersionCode:3005},403' in w
assert "currentProducer:'OpenGLESScope 3.0.5'" in w
for v,code in [('3.0.0',3000),('3.0.1',3001),('3.0.2',3002),('3.0.3',3003),('3.0.4',3004)]:
 assert "(p.application.version===\'{}\'&&p.application.versionCode==={})".format(v,code) in w
assert "function makePayload(version='3.0.5',versionCode=3005" in g
assert 'reject complete previous 3.0.3 on 3.0.4 POST gate' in g
assert 'DELETE FROM reports' not in w and 'UPDATE reports SET' not in w
print('Database 3.0.25 exact current-only 3.0.5/3005 POST, historical-read contract: PASS')
