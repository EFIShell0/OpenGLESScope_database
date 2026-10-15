from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
app=(ROOT/'assets/app.v3031.js').read_text(encoding='utf-8')
css=(ROOT/'assets/site.v3031.css').read_text(encoding='utf-8')
rules=(ROOT/'rules/PROJECT_RULES.md').read_text(encoding='utf-8')
GOOD='M6 9l6 6 6-6'
BAD='M6 9l6 6-6 6'
assert BAD not in app,'malformed/skewed filter chevron returned'
assert app.count(f'<path d="{GOOD}"/>')>=1,'VulkanScope filter chevron path missing'
assert '.custom-select-chevron{width:17px;height:17px;flex:0 0 17px;fill:none;stroke:var(--muted);stroke-width:2;stroke-linecap:round;stroke-linejoin:round;transition:transform .16s ease}' in css
assert '.custom-select.open .custom-select-chevron{transform:rotate(180deg)}' in css
assert '.filters .custom-select-chevron{width:14px;height:14px;flex-basis:14px}' in css
assert 'M6 9l6 6 6-6' in rules and 'M6 9l6 6-6 6' in rules
import hashlib
cache=app[app.index('async function preloadJson'):app.index('async function ensureAllDetails')]
expected='c5bcb4e7fe67693066072e82b5e1247a744e80fb03fd0b1728042155f54b2d3e'
assert hashlib.sha256(cache.encode()).hexdigest()==expected,'cache-first implementation changed during UI parity work'
assert 'const technicalCoverage=' in app and 'const technicalStateNumber=' in app
print('OpenGLESScope Database 3.0.31 VulkanScope filter-chevron parity and cache-preservation: PASS')
