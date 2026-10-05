from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
js=(ROOT/'assets/experience.v3030.js').read_text(encoding='utf-8')
css=(ROOT/'assets/site.v3030.css').read_text(encoding='utf-8')
ref=(ROOT/'rules/SHARED_UI_1_4_12_REFERENCE.css').read_text(encoding='utf-8')
rules=(ROOT/'rules/PROJECT_RULES.md').read_text(encoding='utf-8')

def fail(msg):
    print('test_3_0_28_network_banner_parity: FAIL\n - '+msg)
    sys.exit(1)

def require(ok,msg):
    if not ok: fail(msg)

require("const show=!!copy;" in js,'checking/restored banner visibility must use the canonical state copy')
require("next==='checking'&&reachable()" not in js,'checking must not be hidden just because navigator.onLine is true')
start=js.find("document.addEventListener('openglesscope:ready'")
end=js.find("document.addEventListener('openglesscope:new-reports'",start)
require(start>=0 and end>start,'ready lifecycle handler missing')
ready=js[start:end]
require('isVerifiedOffline' not in ready,'verified cache-first startup must not arm the reconnect latch')
require("if(!reachable()){interrupted=true;banner('offline')}else{markOnline();void sync(true)}" in ready,'ready lifecycle must distinguish only real browser offline from normal online startup')
require("const recheck=()=>{if(!reachable()){interrupted=true;banner('offline');return}interrupted=true;banner('checking');void releases();void sync(true)}" in js,'real reconnect must retain offline/checking/live recheck lifecycle')
require("window.addEventListener('online',recheck" in js,'browser online event must trigger real reconnect recheck')
require("document.addEventListener('openglesscope:connection-ok',markOnline)" in js,'successful live probe must resolve the reconnect lifecycle')

expected=[
    'body.network-banner-visible{--network-banner-offset:82px}',
    '.network-status-shell.is-visible{max-height:96px}',
    '.network-status-banner{min-height:82px;padding:8px 0;align-items:flex-start}',
    '.network-status-copy span{white-space:normal;line-height:1.3}',
    '.network-status-badge{min-width:68px}',
    '@media(max-width:470px){.network-status-badge{display:none}',
]
for fragment in expected:
    require(fragment in ref,'frozen VulkanScope reference missing expected geometry: '+fragment)
    require(fragment in css,'OpenGLESScope mobile geometry diverged from frozen reference: '+fragment)
require(css.count('.network-status-shell.is-visible{')==2,'common visible-shell geometry must exist only at base + 760px breakpoint')
require(css.count('.network-status-banner{')==2,'common banner geometry must exist only at base + 760px breakpoint')
require('max-height:150px' not in css,'late 150px OpenGLESScope override must not return')
require('## Release 3.0.28 — connection lifecycle and mobile network-banner parity' in rules,'3.0.28 engineering rule missing')
print('test_3_0_28_network_banner_parity: PASS')
