"""3.0.32: strict Pages verification, fail-closed cache-first startup, display marks."""
from pathlib import Path
from unittest.mock import patch
import importlib.util
import io
import json
import urllib.error

ROOT=Path(__file__).resolve().parents[1]
app=(ROOT/'assets/app.v3032.js').read_text(encoding='utf-8')
workflow=(ROOT/'tools/pages.workflow.yml').read_text(encoding='utf-8')
html=(ROOT/'index.html').read_text(encoding='utf-8')
spec=importlib.util.spec_from_file_location('snapshot_verifier',ROOT/'tools/verify_published_snapshot.py')
verifier=importlib.util.module_from_spec(spec);spec.loader.exec_module(verifier)
assert workflow==(ROOT/'.github/workflows/pages.yml').read_text(encoding='utf-8')
assert workflow.count('steps.deployment.outputs.page_url')==4
assert workflow.count('--base-url "$PAGE_URL"')==2
assert 'include-hidden-files: true' not in workflow
assert 'if(cached){preloadVerified=true;' in app
assert 'if(!preloadVerified&&state.summaries.length&&' in app
assert "Published cache update pending: refusing full per-report download" in app
assert 'Loading the authoritative live report set; published preload will be checked on the next visit.' not in app
assert 'Published report cache temporarily unavailable' in app
assert 'OpenGL® ES™ Hardware Database' in html and 'EGL™ APIs' in html and 'Khronos® Group' in html
assert "x.api==='OpenGL ES'" in app and "x.api==='EGL'" in app
assert "section==='EGL CONFIGS'" in app
assert "glVersion.match(/^OpenGL ES\\s+" in app

class Response(io.BytesIO):
    def __init__(self, data):super().__init__(data)
    @property
    def headers(self):return {'content-length':str(len(self.getvalue()))}
    def __enter__(self):return self
    def __exit__(self,*_):self.close()

base='https://github-pages.example.invalid/project/'
index={'databaseVersion':'3.0.32','reports':[],'schemaVersion':2}
manifest={'databaseVersion':'3.0.32','schemaVersion':1,'reports':[],'chunks':[],'reportCount':0}

def simulate(request, timeout=25):
    url=request.full_url
    if '/data/index.json?' in url:return Response(json.dumps(index).encode())
    if '/data/preload/manifest.json?' in url:return Response(json.dumps(manifest).encode())
    raise urllib.error.HTTPError(url,404,'Not Found',{},None)

with patch.object(verifier.urllib.request,'urlopen',side_effect=simulate):
    assert verifier.verify_preload(1,0,base)

def missing(request, timeout=25):
    if '/data/index.json?' in request.full_url:return Response(json.dumps(index).encode())
    raise urllib.error.HTTPError(request.full_url,404,'Not Found',{},None)
with patch.object(verifier.urllib.request,'urlopen',side_effect=missing):
    try:verifier.verify_preload(1,0,base)
    except RuntimeError as e:
        assert 'HTTP 404' in str(e) and '/project/data/preload/manifest.json' in str(e),str(e)
    else:raise AssertionError('missing published cache was accepted')
print('3.0.32 PUBLISHED-CACHE: real Pages URL, 404-path diagnostics, complete empty cache, branding and raw API identity PASS')
