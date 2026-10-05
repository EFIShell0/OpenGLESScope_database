from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
app=(ROOT/'assets/app.v3030.js').read_text(encoding='utf-8')
css=(ROOT/'assets/site.v3030.css').read_text(encoding='utf-8')
rules=(ROOT/'rules/PROJECT_RULES.md').read_text(encoding='utf-8')
GOOD='M6 9l6 6 6-6'
BAD='M6 9l6 6-6 6'
assert BAD not in app,'malformed/skewed filter chevron returned'
assert app.count(f'<path d="{GOOD}"/>')>=1,'VulkanScope filter chevron path missing'
assert '.custom-select-chevron{width:17px;height:17px;flex:0 0 17px;fill:none;stroke:var(--muted);stroke-width:2;stroke-linecap:round;stroke-linejoin:round;transition:transform .16s ease}' in css
assert '.custom-select.open .custom-select-chevron{transform:rotate(180deg)}' in css
assert '.filters .custom-select-chevron{width:14px;height:14px;flex-basis:14px}' in css
assert 'M6 9l6 6 6-6' in rules and 'M6 9l6 6-6 6' in rules
normalized=app.replace("const DATABASE_VERSION='3.0.30'","const DATABASE_VERSION='3.0.29'",1).replace(GOOD,BAD,1)
import hashlib
expected='fc47b7a5926c119bd7dbec0540bb60c630b01306ac8c73305f7210b063764a2f'
assert hashlib.sha256(normalized.encode()).hexdigest()==expected,'unexpected app/runtime mutation beyond release literal and chevron fix'
print('OpenGLESScope Database 3.0.30 VulkanScope filter-chevron parity and cache-preservation: PASS')
