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
 ['node','--check','assets/app.v3021.js'],
 ['node','--check','assets/experience.v3021.js'],
 ['node','--check','assets/browser-compat.v3021.js'],
 ['node','--check','assets/release-bootstrap.v3021.js'],
 ['node','--check','assets/scroll-system.v3021.js'],
 ['python3','tools/test_3_0_1_scroll_parity.py'],
 ['python3','tools/test_3_0_4_visual_parity.py'],
 ['python3','tools/test_3_0_6_settings_filter_contract.py'],
 ['python3','tools/test_3_0_7_shell_contract.py'],
 ['python3','tools/test_3_0_10_parity_contract.py'],
 ['python3','tools/test_3_0_12_overview_contract.py'],
 ['python3','tools/test_3_0_12_angle_contract.py'],
 ['python3','tools/test_3_0_13_behavior_contract.py'],
 ['python3','tools/test_3_0_14_parity_contract.py'],
 ['python3','tools/test_3_0_15_pairing_contract.py'],
 ['python3','tools/test_3_0_19_submission_floor.py'],
 ['python3','tools/test_3_0_20_submission_floor.py'],
 ['python3','tools/test_3_0_21_submission_floor.py'],
 ['python3','tools/test_3_0_16_regional_encyclopedia_contract.py'],
 ['node','tools/test_3_0_17_angle_egl.mjs'],
 ['node','tools/test_3_0_18_encyclopedia_clear.mjs'],
 ['python3','tools/test_3_0_0_experience.py'],
 ['node','tools/test_3_0_3_publication_parity.mjs'],
 ['node','tools/test_3_0_5_interaction_contract.mjs'],
 ['node','--check','worker/src/index.js'],
 ['python3','tools/test_2_0_5_release_handshake.py'],
 ['python3','tools/test_2_0_5_official_brand.py'],
 ['node','tools/test_routes.mjs'],
 ['node','tools/test_compare_contract.mjs'],
 ['node','tools/test_statistics_filters.mjs'],
 ['node','tools/test_ui_parity.mjs'],
 ['node','tools/test_2_0_2_interface.mjs'],
 ['python3','tools/test_2_0_5_vulkan_ui_parity.py'],
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
