from pathlib import Path
import subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1]
app=(ROOT/'assets/app.v3024.js').read_text(encoding='utf-8')
workflow=(ROOT/'.github/workflows/pages.yml').read_text(encoding='utf-8')
template=(ROOT/'tools/pages.workflow.yml').read_text(encoding='utf-8')
audit=(ROOT/'tools/audit_database.py').read_text(encoding='utf-8')
builder=(ROOT/'tools/build_preload_snapshot.py').read_text(encoding='utf-8')
verifier=(ROOT/'tools/verify_published_snapshot.py').read_text(encoding='utf-8')
rules=(ROOT/'rules/PROJECT_RULES.md').read_text(encoding='utf-8')
assert workflow==template
for term in ('async function loadLiveAtomically()', 'savedSummaries=state.summaries',
             'state.details=new Map(savedDetails)', 'current.submitted_at!==payload?.submittedAt',
             'await ensureAllDetails()', 'state.summaries=savedSummaries;state.details=savedDetails',
             'Preparing ${manifest.reportCount} cached reports', 'Preload integrity mismatch',
             "await preloadJson('./data/preload/manifest.json','force-cache')"):
    assert term in app,term
for term in ('--require-preload','--verify-preload','build_preload_snapshot.py'):
    assert term in workflow,term
assert workflow.count('audit_database.py --artifact-tree _site --require-preload')==2
assert 'if args.require_preload and not (preload/\'manifest.json\').is_file()' in audit
assert 'published report cache is missing' in audit
assert 'def verify_preload(' in verifier and "hashlib.sha256(raw).hexdigest()!=digest" in verifier
assert 'ThreadPoolExecutor' in builder and 'get_report' in builder
assert '3.0.24 — mandatory VulkanScope-style cache-first publication' in rules
with tempfile.TemporaryDirectory(prefix='ogs24-optional-cache-test-') as td:
    run=subprocess.run([sys.executable,'-B',str(ROOT/'tools/build_pages_artifact.py'),td],cwd=ROOT,capture_output=True,text=True)
    assert run.returncode==0,run.stdout+run.stderr
    failed=subprocess.run([sys.executable,'-B',str(ROOT/'tools/audit_database.py'),'--artifact-tree',td,'--require-preload'],cwd=ROOT,capture_output=True,text=True)
    assert failed.returncode!=0 and 'published report cache is missing' in failed.stdout,failed.stdout+failed.stderr
print('3.0.24 mandatory published cache, atomic cache-first synchronization, regression source contract: PASS')
