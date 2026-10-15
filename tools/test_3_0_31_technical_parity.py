from pathlib import Path
import hashlib
ROOT=Path(__file__).resolve().parents[1]
app=(ROOT/'assets/app.v3032.js').read_text(encoding='utf-8')
css=(ROOT/'assets/site.v3032.css').read_text(encoding='utf-8')
html=(ROOT/'index.html').read_text(encoding='utf-8')
worker=(ROOT/'worker/src/index.js').read_text(encoding='utf-8')
cache=app[app.index('async function preloadJson'):app.index('async function ensureAllDetails')]
assert hashlib.sha256(cache.encode()).hexdigest()=='54383f3b3f069c1f6f0d5e7e8d1ee93f62bf10a398513b57c9ac49481e24e5ae'
assert "const DATABASE_VERSION='3.0.32'" in app
assert "$('#contentView').dataset.mainView=state.view" in app
assert 'const technicalCoverage=' in app and 'const technicalStateNumber=' in app
assert 'ratio*100' in app and 'count===total?0:1' in app
assert 'statusClass(status).replace(/-/g' in app
for view in ['Extensions','Limits','Formats','Precision']:
 assert ('async function render'+view+'()') in app,view
 assert f'[data-main-view="{view.lower()}"]' in css,view
for pattern in ['technicalCounts(','technicalCoverage(counts[1],rs.length','technicalHeads(labels)','precision-pagination','bindSubSearch(\'precisionRowSearch\'','not-applicable','Not listed','isLimitDiagnosticName','isPrecisionDiagnosticName','renderGeneration']:
 assert pattern in app,pattern
for label in ['Query available','Query unavailable','Unavailable %','Value distribution','Available ranges / precision','NV sample properties']:
 assert label in app,label
assert '.coverage-bar{height:7px;' in css and '.coverage-value{min-width:42px;' in css
assert '.subfilters{display:grid;grid-template-columns:repeat(auto-fit,minmax(205px,1fr))' in css
assert 'site.v3032.css?v=3032' in html and 'app.v3032.js?v=3032' in html
assert "const DATABASE_VERSION='3.0.32'" in worker
assert 'versionCode===3007' in worker or 'versionCode' in worker and '3007' in worker
print('3.0.32 TECHNICAL_COVERAGE_AND_PARITY: PASS')
