from pathlib import Path
import re,hashlib,json
R=Path(__file__).resolve().parents[1]
a=(R/'assets/app.v3021.js').read_text(encoding='utf-8')
c=(R/'assets/site.v3021.css').read_text(encoding='utf-8')
h=(R/'index.html').read_text(encoding='utf-8')
assert 'const COUNTRY_CODE_SET=new Set(COUNTRY_CODES)' in a
codes=re.search(r"const COUNTRY_CODES=Object.freeze\('([^']+)'\.split\(','\)\)",a).group(1).split(',')
assert len(codes)==250 and len(set(codes))==250
flags=R/'assets/country-flags'
assert {p.name for p in flags.glob('*.png')}=={x.lower()+'.png' for x in codes}
for p in flags.glob('*.png'):
 assert p.stat().st_size>60 and p.read_bytes()[:8]==b'\x89PNG\r\n\x1a\n',p
assert 'browserCountryLabel()' in a and 'countryFlagAsset(code)' in a
assert 'Browser / system time zone — ${browserZone()}' in a
assert 'new Option(`${name} (${code})`,code)' in a
assert 'menu.addEventListener(\'wheel\',e=>e.stopPropagation()' in a
assert 'menuPointerActive' in a and "if(e.target.closest('.custom-select.open'))return" in a
assert 'setRegionalPreviewContent(el,' in a and "regionalProfileRow('Country / region',country)" in a
assert 'registry-workspace encyclopedia-workspace' in a
for name in ['encyclopedia-workspace-head','encyclopedia-stat-strip','encyclopedia-search-zone','encyclopedia-categories','encyclopedia-guidance','encyclopedia-results-head','registry-list encyclopedia-grid']:
 assert name in a and all(('.'+token) in c for token in name.split()),name
assert len(json.loads((R/'data/registry-catalog.v2000.json').read_text(encoding='utf-8'))['entries'])==5261
assert "const size=24,pages=Math.max(1,Math.ceil(matches.length/size))" in a
assert 'new TextDecoder(\'utf-8\',{fatal:true})' in a
assert (R/'data/release.json').read_text(encoding='utf-8').find('"databaseVersion":"3.0.21"')>=0
print('3.0.21 region/country flags, viewport-safe menu, and reference encyclopedia contract: PASS (250 countries, 5,261 real registry entries)')
