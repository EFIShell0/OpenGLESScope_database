from pathlib import Path
import hashlib,sys
ROOT=Path(__file__).resolve().parents[1]
app=(ROOT/'assets/app.v3032.js').read_text(encoding='utf-8')
experience=(ROOT/'assets/experience.v3032.js').read_text(encoding='utf-8')
css=(ROOT/'assets/site.v3032.css').read_text(encoding='utf-8')
rules=(ROOT/'rules/PROJECT_RULES.md').read_text(encoding='utf-8')
repair=(ROOT/'tools/repair_repository.py').read_text(encoding='utf-8')

def fail(msg):
    print('test_3_0_29_cache_release_integrity: FAIL\n - '+msg)
    sys.exit(1)
def require(ok,msg):
    if not ok: fail(msg)

cache=app[app.index('async function preloadJson'):app.index('async function ensureAllDetails')]
expected='54383f3b3f069c1f6f0d5e7e8d1ee93f62bf10a398513b57c9ac49481e24e5ae'
require(hashlib.sha256(cache.encode()).hexdigest()==expected,'cache-first preload and index implementation differs from preserved baseline')
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
require("'app':'app.v3032.js'" in repair and "'site':'site.v3032.css'" in repair,'repair tool must recognize only current v3032 browser assets')
require('## Release 3.0.29 — cache-preservation and release-preflight recovery' in rules,'3.0.29 release rule missing')
print('test_3_0_29_cache_release_integrity: PASS')
