"""Run only examples/. Never execute snippets/ or pseudocode/."""
from pathlib import Path
import subprocess, sys, os
base=Path(__file__).resolve().parents[1]
paths=sorted((base/'chapters').glob('chapter_*/examples/*.py'))
if not paths: raise SystemExit('ERROR: no examples')
failed=[]
for path in paths:
    env=os.environ.copy()
    env['MPLBACKEND']='Agg'
    env['PYTHONDONTWRITEBYTECODE']='1'
    try:
        p=subprocess.run([sys.executable,path.name],cwd=path.parent,env=env,capture_output=True,text=True,timeout=60)
        ok=(p.returncode==0)
        if not ok: failed.append((str(path),p.stderr[-700:]))
    except Exception as exc:
        ok=False;failed.append((str(path),str(exc)))
    print(('PASS' if ok else 'FAIL'),path.relative_to(base))
if failed:
    for path,why in failed:print(path,why,file=sys.stderr)
    raise SystemExit(1)
print(f'PASS: {len(paths)} example files')
