from pathlib import Path
import hashlib,tempfile,zipfile,sys
ROOT=Path(__file__).resolve().parents[1]
EXCLUDED={'.git','__pycache__','node_modules','.wrangler','_site'}
LOCAL_CHECKOUT_ONLY={'.gitattributes','worker/package-lock.json','rules/0.2.6_OPENGLESSCOPE_0.3.3_FULL_DATABASE_AUDIT.md'}
def package_files(root):
    out=[]
    for p in root.rglob('*'):
        if not p.is_file(): continue
        rel=p.relative_to(root)
        if rel.as_posix() in LOCAL_CHECKOUT_ONLY: continue
        if any(part in EXCLUDED for part in rel.parts): continue
        if p.suffix in {'.pyc','.pyo'}: continue
        out.append(rel.as_posix())
    return sorted(out)
def make_zip(root,dest):
    with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for rel in package_files(root):
            info=zipfile.ZipInfo(rel,(2026,9,16,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=(0o755 if rel.startswith('tools/') else 0o644)<<16
            z.writestr(info,(root/rel).read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
def fail(msg): print('verify_package_reproducibility: FAIL\n - '+msg);sys.exit(1)
manifest=ROOT/'files.txt'
if not manifest.is_file(): fail('files.txt package manifest missing')
expected=[x for x in manifest.read_text().splitlines() if x];actual=package_files(ROOT)
if expected!=actual: fail('files.txt does not exactly match clean source package')
if len(expected)!=len(set(expected)): fail('files.txt contains duplicates')
with tempfile.TemporaryDirectory(prefix='oglesdb-repro-') as td:
    a=Path(td)/'a.zip';b=Path(td)/'b.zip';make_zip(ROOT,a);make_zip(ROOT,b)
    if hashlib.sha256(a.read_bytes()).digest()!=hashlib.sha256(b.read_bytes()).digest(): fail('deterministic ZIP reproduction failed')
print('verify_package_reproducibility: PASS')
