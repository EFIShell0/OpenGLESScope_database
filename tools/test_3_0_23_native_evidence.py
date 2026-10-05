from pathlib import Path
root=Path(__file__).resolve().parents[1]
w=(root/'worker/src/index.js').read_text(encoding='utf-8')
t=(root/'worker/tests/contract.mjs').read_text(encoding='utf-8')
r=(root/'rules/PROJECT_RULES.md').read_text(encoding='utf-8')
required=('Query counter bits: GL_TIME_ELAPSED_EXT','Query counter bits: GL_TIMESTAMP_EXT')
line=w.split('const TIMER_LIMITS=',1)[1].split(';',1)[0]
for name in required:
 assert name in line,name
 assert name in t,name
 assert name in r,name
for fake in ('GL_TIME_ELAPSED_EXT_QUERY_COUNTER_BITS','GL_TIMESTAMP_EXT_QUERY_COUNTER_BITS'):
 assert fake not in line,'Native provenance regressed to invented identifier: '+fake
assert 'TIMER_QUERY_PROVENANCE' in w and 'errorCode:code' in w
assert 'real native timer query names accepted' in t and 'reject fabricated timer diagnostic identifiers' in t
print('3.0.30 native timer evidence and safe failure taxonomy: PASS')
