from pathlib import Path
import re
R=Path(__file__).resolve().parents[1]
w=(R/'worker/src/index.js').read_text(encoding='utf-8')
t=(R/'worker/tests/contract.mjs').read_text(encoding='utf-8')
assert "const DATABASE_VERSION='3.0.25'" in w
assert "p.application.version!=='3.0.5'||p.application.versionCode!==3005" in w
assert "function makePayload(version='3.0.5',versionCode=3005" in t
assert 'validCurrentConfigText(text,p.technicalReport?.eglConfigs)' in w
assert 'currentPbufferTextValid(text)' in w
for key in ('recordableAndroid','framebufferTargetAndroid','colorComponentTypeExt','unavailableAttributes'):
 assert f"'{key}'" in w and f'{key}=' in t
for label in ('config ID','GL colorspace','VG alpha format','VG colorspace','horizontal resolution','largest pbuffer','pixel aspect ratio','vertical resolution'):
 assert f"'Pbuffer {label}:'" in w and f'Pbuffer {label}:' in t
assert 'TXT_PBUFFER_FIELDS' in w and 'TXT_EGL_CONFIG_FORMAT' in w
for stale in ('GL_TIME_ELAPSED_EXT_QUERY_COUNTER_BITS','GL_TIMESTAMP_EXT_QUERY_COUNTER_BITS'):
 assert stale not in w and stale in t  # Explicit negative test must retain the fabricated string as an attack case
for native in ('Query counter bits: GL_TIME_ELAPSED_EXT','Query counter bits: GL_TIMESTAMP_EXT'):
 assert native in w and native in t
for case in ('accept 3.0.5 Android canonical TXT','reject absent app pbuffer evidence fields','reject synthetic non-native EGL config separator','accept legitimately empty EGL-config enumeration','reject forged EGL-config header count'):
 assert case in t
print('3.0.25 canonical app TXT/JSON + GL/EGL native labels: PASS')
