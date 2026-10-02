import importlib.util,json,subprocess,sys,zipfile,shutil
from pathlib import Path
from unittest.mock import patch
import pytest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('release',ROOT/'scripts/release.py');release=importlib.util.module_from_spec(spec);spec.loader.exec_module(release)

def test_individual_aggregate_archive_readback_and_install(tmp_path):
 m=release.validate();dest=tmp_path/'packages';release.package(m,dest)
 with zipfile.ZipFile(dest/(ROOT.name+'-'+m['version']+'.zip')) as z:z.extractall(tmp_path/'aggregate')
 install=tmp_path/'install';r=subprocess.run([sys.executable,str(tmp_path/'aggregate/scripts/release.py'),'--install',str(install)],cwd=tmp_path,capture_output=True,text=True);assert r.returncode==0,r.stderr
 for row in m['skills']:
  assert release.hashes(install/row['name'])==release.hashes(release.skill_path(row))
  with zipfile.ZipFile(dest/(row['name']+'-'+row['version']+'.zip')) as z:
   z.extractall(tmp_path/'single')
   assert all(x.startswith(row['name']+'/') for x in z.namelist())
  assert release.hashes(tmp_path/'single'/row['name'])==release.hashes(release.skill_path(row))

def test_transaction_removes_old_files_and_rolls_back_failure(tmp_path):
 m=release.validate();dest=tmp_path/'installed';release.install(m,dest);first=dest/m['skills'][0]['name'];(first/'old.txt').write_text('old')
 release.install(m,dest);assert not (first/'old.txt').exists()
 before={r['name']:release.hashes(dest/r['name']) for r in m['skills']};real_replace=release.os.replace
 def fail(src,dst):
  if str(src).endswith('-new'):raise OSError('simulated swap failure')
  return real_replace(src,dst)
 with patch.object(release.os,'replace',side_effect=fail):
  with pytest.raises(OSError):release.install(m,dest)
 assert before=={r['name']:release.hashes(dest/r['name']) for r in m['skills']}
 assert not list(dest.glob('.skills-upgrade-*'))

def test_symlink_install_refused(tmp_path):
 (tmp_path/'real').mkdir();(tmp_path/'alias').symlink_to(tmp_path/'real',target_is_directory=True)
 with pytest.raises(ValueError):release.install(release.validate(),tmp_path/'alias')
