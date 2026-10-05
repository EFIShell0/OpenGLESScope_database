from pathlib import Path
import hashlib,sys
ROOT=Path(__file__).resolve().parents[1]
app=(ROOT/'assets/app.v3030.js').read_text(encoding='utf-8')
experience=(ROOT/'assets/experience.v3030.js').read_text(encoding='utf-8')
css=(ROOT/'assets/site.v3030.css').read_text(encoding='utf-8')
rules=(ROOT/'rules/PROJECT_RULES.md').read_text(encoding='utf-8')
repair=(ROOT/'tools/repair_repository.py').read_text(encoding='utf-8')

def fail(msg):
    print('test_3_0_29_cache_release_integrity: FAIL\n - '+msg)
    sys.exit(1)
def require(ok,msg):
    if not ok: fail(msg)

normalized=app.replace("const DATABASE_VERSION='3.0.30'","const DATABASE_VERSION='3.0.27'",1).replace('M6 9l6 6 6-6','M6 9l6 6-6 6',1)
expected='34089760a8cecbe4e2cce3450c3833392911ca6427e53108cdfbd0a9060d736f'
require(hashlib.sha256(normalized.encode()).hexdigest()==expected,'app cache/runtime implementation diverged from 3.0.27 beyond the release literal')
for token in [
    "manifest=await preloadJson('./data/preload/manifest.json','no-cache')",
    "catch{manifest=await preloadJson('./data/preload/manifest.json','force-cache')}",
    "preloadJson(`./data/preload/${part.file}`,'force-cache',part.byteLength,part.sha256)",
    "crypto.subtle.digest('SHA-256',buffer)",
    "if(loaded!==manifest.reportCount||details.size!==byId.size)throw Error('Incomplete cached report set')",
    "state.cachedReportLoads=state.details.size",
]: require(token in app,'required cache-first invariant missing: '+token)
ready=experience[experience.find("document.addEventListener('openglesscope:ready'"):experience.find("document.addEventListener('openglesscope:new-reports'")]
require('isVerifiedOffline' not in ready,'verified cache startup must not arm reconnect state')
require('max-height:150px' not in css,'late mobile banner override returned')
require("'app':'app.v3030.js'" in repair and "'site':'site.v3030.css'" in repair,'repair tool must recognize only current v3030 browser assets')
require('## Release 3.0.29 — cache-preservation and release-preflight recovery' in rules,'3.0.29 release rule missing')
print('test_3_0_29_cache_release_integrity: PASS')
