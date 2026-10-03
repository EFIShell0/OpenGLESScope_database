from pathlib import Path
import json,re
R=Path(__file__).resolve().parents[1]
w=(R/'worker/src/index.js').read_text(encoding='utf-8')
a=(R/'assets/app.v3017.js').read_text(encoding='utf-8')
h=(R/'index.html').read_text(encoding='utf-8')
release=json.loads((R/'data/release.json').read_text(encoding='utf-8'))
assert release=={'schemaVersion':2,'databaseVersion':'3.0.17','releaseReady':False,'appAsset':'assets/app.v3017.js','cacheKey':'3017'}
assert "const DATABASE_VERSION='3.0.17'" in w and "const NORMALIZER_VERSION=16" in w
assert "p.application.version!=='3.0.1'||p.application.versionCode!==3001" in w
assert 'requiredVersionCode:3001},403' in w
assert "(p.application.version==='3.0.0'&&p.application.versionCode===3000)" in w
assert "(p.application.version==='3.0.1'&&p.application.versionCode===3001)" in w
assert 'if(producerAtLeastVersion(p,3,0,0)){if(t.schemaVersion!==5||!validGlRuntimeV5' in w
assert 'Existing historic reports remain available for reading.' in w
assert 'SELECT id,submitted_at,schema_version,gpu_name,vendor,opengles_version,egl_version,manufacturer,model,application_version,application_version_code FROM reports' in w
assert 'DELETE FROM reports' not in w and 'UPDATE reports SET' not in w
assert "compatibleProducer:'OpenGLESScope 3.0.1 (versionCode 3001) for new submissions only; existing earlier reports remain readable'" in w
assert 'OpenGLESScope 3.0.1' in a
assert "+metric('Producer/query baseline',baseline)+metric('Compatible producers',state.health?.compatibleProducer" in a
assert a.count("metric('Compatible producers'")==1
assert '.hero-v127 .metrics{margin-top:0!important;grid-template-columns:repeat(6,minmax(0,1fr))' in (R/'assets/site.v3017.css').read_text(encoding='utf-8')
assert 'site.v3017.css' in h and 'app.v3017.js' in h
assert sorted(x.name for x in (R/'worker/migrations').glob('*.sql'))==['0001_init.sql','0002_report_cursor_index.sql','0003_application_version_summary.sql','0004_payload_chunks.sql']
print('3.0.17 exact producer floor, six hero cards, historical reads, D1 stability and app pairing: PASS')
