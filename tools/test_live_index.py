import importlib.util
import json
from pathlib import Path
from unittest.mock import patch

root=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('build_live_index',root/'tools/build_live_index.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
a='a'*64
b='b'*64
summary=lambda id,time:{'id':id,'submitted_at':time,'schema_version':2,'gpu_name':'GL fixture','vendor':'fixture','opengles_version':'OpenGL ES 3.2','egl_version':'1.5','manufacturer':'fixture','model':'fixture','application_version':'2.2.22','application_version_code':2222}
first={'schemaVersion':2,'databaseVersion':'2.0.2','currentProducer':'OpenGLESScope 2.2.22','normalizerVersion':16,'reports':[summary(a,'2026-10-01T12:00:00.000Z')],'nextCursor':{'submittedAt':'2026-10-01T12:00:00.000Z','id':a}}
second={'schemaVersion':2,'databaseVersion':'2.0.2','currentProducer':'OpenGLESScope 2.2.22','normalizerVersion':16,'reports':[summary(b,'2026-09-30T12:00:00.000Z')],'nextCursor':None}
with patch.object(module,'fetch',side_effect=[first,second]) as fetch:
    result=module.build('https://test.example',b)
    assert result['reportCount']==2
    assert [r['id'] for r in result['reports']]==[a,b]
    assert result['normalizerVersion']==16
    assert result['databaseVersion']=='2.0.2'
    assert 'beforeSubmittedAt=' in fetch.call_args.args[0]
    assert list(result['reports'][0])==[x for x in module.ALLOWED if x in first['reports'][0]]
with patch.object(module,'fetch',return_value={'schemaVersion':2,'databaseVersion':'2.0.2','currentProducer':'OpenGLESScope 2.2.22','normalizerVersion':16,'reports':[summary(a,'now')],'nextCursor':None}):
    try: module.build('https://test.example',b)
    except ValueError as e: assert 'Expected accepted report' in str(e)
    else: raise AssertionError('missing trigger ID must abort snapshot')
with patch.object(module,'fetch',return_value={'schemaVersion':2,'databaseVersion':'2.0.2','currentProducer':'OpenGLESScope 2.2.22','normalizerVersion':16,'reports':[dict(summary(a,'now'),token='private')],'nextCursor':None}):
    try: module.build('https://test.example','')
    except ValueError as e: assert 'private report summary' in str(e)
    else: raise AssertionError('unreviewed summary keys must fail')
with patch.object(module,'fetch',return_value={'schemaVersion':2,'databaseVersion':'2.0.2','currentProducer':'OpenGLESScope 2.2.22','normalizerVersion':16,'reports':[summary(a,'now'),summary(a,'now')],'nextCursor':None}):
    try: module.build('https://test.example','')
    except ValueError as e: assert 'Duplicate' in str(e)
    else: raise AssertionError('duplicate IDs must fail')
with patch.object(module,'fetch',return_value={'schemaVersion':2,'databaseVersion':'2.0.2','currentProducer':'OpenGLESScope 2.2.22','normalizerVersion':16,'reports':[summary(a,'now')],'nextCursor':{'submittedAt':'now','id':a}}):
    try: module.build('https://test.example','')
    except ValueError as e: assert 'repeated Worker cursor' in str(e) or 'Duplicate' in str(e)
    else: raise AssertionError('cursor replay must fail')
for api in ['http://example.test','file:///tmp/file']:
    try:module.build(api,'')
    except ValueError:pass
    else: raise AssertionError('non-HTTPS API must fail')
print('OpenGLESScope Database deterministic live snapshot positive/negative tests: ALL PASS')

with patch.object(module,'fetch',return_value={'schemaVersion':2,'databaseVersion':'1.0.16','currentProducer':'OpenGLESScope 2.2.1','normalizerVersion':16,'reports':[],'nextCursor':None}):
    try:module.build('https://test.example','')
    except ValueError as e:assert 'Incompatible report index schema' in str(e)
    else:raise AssertionError('old deployed Worker must block current Pages release')
import importlib.util
verify_spec=importlib.util.spec_from_file_location('verify_published_snapshot',root/'tools/verify_published_snapshot.py')
published=importlib.util.module_from_spec(verify_spec)
verify_spec.loader.exec_module(published)
with patch.object(published,'fetch',side_effect=[False,True]),patch.object(published.time,'sleep') as sleeping:
    assert published.verify(a,attempts=3,interval=0) is True
    assert sleeping.call_count==1
with patch.object(published,'fetch',return_value=False),patch.object(published.time,'sleep'):
    try:published.verify(a,attempts=2,interval=0)
    except RuntimeError as e:assert 'verification failed' in str(e)
    else:raise AssertionError('missing published report cannot pass')
try:published.verify('not-an-id',attempts=1,interval=0)
except ValueError:pass
else:raise AssertionError('invalid published report ID cannot pass')
print('OpenGLESScope Database published accepted-report verifier: ALL PASS')
