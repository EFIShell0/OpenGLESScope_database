from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess
import sys
import shutil
ROOT=Path(__file__).resolve().parents[1]
with TemporaryDirectory(prefix='oglesdb326-repair-') as td:
    root=Path(td)/'work'
    (root/'tools').mkdir(parents=True)
    (root/'.github/workflows').mkdir(parents=True)
    (root/'tools/repair_repository.py').write_bytes((ROOT/'tools/repair_repository.py').read_bytes())
    (root/'tools/pages.workflow.yml').write_bytes((ROOT/'tools/pages.workflow.yml').read_bytes())
    (root/'.github/workflows/pages.yml').write_bytes((ROOT/'tools/pages.workflow.yml').read_bytes())
    (root/'files.txt').write_text('files.txt\ntools/pages.workflow.yml\ntools/repair_repository.py\n.github/workflows/pages.yml\n',encoding='utf-8')
    old=root/'tools/verify_2_2_18_state_and_evidence.py'
    old.write_text('# obsolete source comment\nraise RuntimeError("stale")\n',encoding='utf-8')
    def run(mode):
        return subprocess.run([sys.executable,'-B',str(root/'tools/repair_repository.py'),mode],cwd=root,capture_output=True,text=True)
    before=run('--check')
    assert before.returncode!=0 and old.name in before.stdout,(before.returncode,before.stdout,before.stderr)
    fixed=run('--apply')
    assert fixed.returncode==0 and not old.exists(),(fixed.returncode,fixed.stdout,fixed.stderr)
    archives=list(Path(td).glob('OpenGLESScope_database_3.0.28_stale_tools_*/tools/'+old.name))
    assert len(archives)==1 and archives[0].read_text().startswith('# obsolete source comment')
    final=run('--check')
    assert final.returncode==0,(final.returncode,final.stdout,final.stderr)
print('3.0.28 obsolete Python source quarantine: PASS (fails safely before repair; old source retained outside project)')
