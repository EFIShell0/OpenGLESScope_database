from pathlib import Path
import os,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1]
ENV={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
commands=[
 ['python3','tools/repair_repository.py','--check'],
 ['python3','tools/test_audit_hygiene.py'],
 ['python3','tools/verify_1_1_0_rules.py'],
 ['python3','tools/test_1_1_0_negative_mutations.py'],
 ['python3','tools/test_live_index.py'],
 ['python3','tools/test_2_0_2_snapshot_security.py'],
 ['node','worker/scripts/security-audit.mjs'],
 ['node','--check','assets/app.v2004.js'],
 ['node','--check','worker/src/index.js'],
 ['python3','tools/test_2_0_4_release_handshake.py'],
 ['python3','tools/test_2_0_4_official_brand.py'],
 ['node','tools/test_routes.mjs'],
 ['node','tools/test_compare_contract.mjs'],
 ['node','tools/test_statistics_filters.mjs'],
 ['node','tools/test_ui_parity.mjs'],
 ['node','tools/test_2_0_2_interface.mjs'],
 ['python3','tools/test_2_0_4_vulkan_ui_parity.py'],
 ['node','worker/tests/contract.mjs'],
 ['python3','tools/audit_database.py','--source-tree','.'],
 ['python3','tools/verify_release_docs.py'],
 ['python3','tools/verify_package_reproducibility.py']]
for cmd in commands:
    r=subprocess.run(cmd,cwd=ROOT,env=ENV)
    if r.returncode: print('QUALITY_GATE: FAIL · '+' '.join(cmd));sys.exit(r.returncode)
with tempfile.TemporaryDirectory(prefix='oglesdb-pages-') as td:
    r=subprocess.run(['python3','tools/build_pages_artifact.py',td],cwd=ROOT,env=ENV)
    if r.returncode: print('QUALITY_GATE: FAIL · Pages staging');sys.exit(r.returncode)
    r=subprocess.run(['python3','tools/audit_database.py','--artifact-tree',td],cwd=ROOT,env=ENV)
    if r.returncode: print('QUALITY_GATE: FAIL · Pages artifact audit');sys.exit(r.returncode)
print('QUALITY_GATE: PASS')
