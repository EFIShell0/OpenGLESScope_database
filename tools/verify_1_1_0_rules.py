import hashlib
import json
import re
from pathlib import Path
root=Path(__file__).resolve().parents[1]
reference=(root/'rules/VULKANSCOPE_DATABASE_1.4.12_PROJECT_RULES_REFERENCE.md').read_bytes()
manifest=json.loads((root/'rules/vulkanscope_database_1_4_12_rule_applicability.json').read_text(encoding='utf-8'))
headings=re.findall(r'^## (.+)$',reference.decode('utf-8'),re.M)
assert hashlib.sha256(reference).hexdigest()==manifest['sourceSha256']=='cc9b75a9f923cc1a3a59cf66ee104e22f1ef175cfde85fb5df4554c9a1226fac'
assert len(headings)==manifest['headingCount']==116
assert [x['heading'] for x in manifest['headings']]==headings
assert all(x['applicability'] in {'adopted','adapted','historical_methodology_reference','api_specific_reference'} and x['interpretation'].strip() for x in manifest['headings'])
rules=(root/'rules/PROJECT_RULES.md').read_text(encoding='utf-8')
for phrase in ['## Release 1.1.0 VulkanScope Database 1.4.12 methodology adaptation','exact semantic-version/versionCode binding','SNAPSHOT_GITHUB_TOKEN','GET /v1/sync','fatal UTF-8 validation','clean-extract full-gate']:
    assert phrase in rules,phrase
app=(root/'assets/app.v3013.js').read_text(encoding='utf-8')
html=(root/'index.html').read_text(encoding='utf-8')
css=(root/'assets/site.v3013.css').read_text(encoding='utf-8')
for term in ['refreshLive','announceLive','aria-busy','/v1/sync','loadSnapshotFallback','Offline public snapshot','out.length>100000','offlineSnapshot','Incompatible Worker report index']:
    assert term in app
for term in ['id="refreshLive"','aria-live="polite" id="liveStatus" role="status"','type="button"']:
    assert term in html
for term in ['.live-strip','.live-refresh:focus-visible','prefers-reduced-motion']:
    assert term in css
worker=(root/'worker/src/index.js').read_text(encoding='utf-8')
for term in ['getReader()','fatal:true','MAX_BODY','/v1/sync','insertResult?.meta?.changes','SNAPSHOT_GITHUB_TOKEN','ctx?.waitUntil']:
    assert term in worker
assert (root/'tools/test_live_index.py').is_file()
assert (root/'tools/verify_published_snapshot.py').is_file()
workflow=(root/'.github/workflows/pages.yml').read_text(encoding='utf-8')
assert workflow==(root/'tools/pages.workflow.yml').read_text(encoding='utf-8')
for term in ['group: pages','cancel-in-progress: false','Refresh authoritative live index','verify_published_snapshot.py']:
    assert term in workflow
for token in ['devices','versions','trends','encyclopedia','renderEncyclopedia','initParityFeatures','favoriteKey','fetchRegistry','finishStartup']:
    assert token in app,token
for token in ['id="settingsDrawer"','id="settingsButton"','id="pageScrollControls"','id="viewportScrollbar"','id="databaseLoading"','id="heroWorkspaceTitle"']:
    assert token in html,token
assert '.settings-drawer' in css and '.viewport-scrollbar' in css and '@media(prefers-reduced-motion:reduce)' in css
registry=json.loads((root/'data/registry-catalog.v2000.json').read_text(encoding='utf-8'))
assert registry['schema']=='OpenGLESScopeRegistryCatalog1' and len(registry['entries'])==registry['counts']['entries']==5261
assert all(x.get('api') in {'OpenGL ES','EGL'} for x in registry['entries'])
print('OpenGLESScope Database immutable Vulkan rules reference, GL/EGL applicability, and 2.0.0 interface: PASS')
