#!/usr/bin/env python3
"""Self-contained manifest validation, reproducible packaging and transactional install."""
import argparse,ast,hashlib,json,os,re,shutil,tempfile,zipfile
from pathlib import Path
from urllib.parse import unquote
import yaml
ROOT=Path(__file__).resolve().parents[1]

def files(base):
    return [p for p in sorted(base.rglob('*')) if p.is_file() and not p.is_symlink() and '__pycache__' not in p.parts and p.suffix!='.pyc']
def hashes(base):return {str(p.relative_to(base)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files(base)}
def skill_path(row):return ROOT/row.get('path',row['name'])
def validate():
    m=json.loads((ROOT/'skills-manifest.json').read_text());rows=m['skills'];names=[x['name'] for x in rows]
    if len(names)!=len(set(names)):raise ValueError('duplicate manifest names')
    expected={str(skill_path(x).relative_to(ROOT)) for x in rows};actual={str(p.parent.relative_to(ROOT)) for p in ROOT.glob('*/SKILL.md')}|{str(p.parent.relative_to(ROOT)) for p in ROOT.glob('skills/*/SKILL.md')}
    if actual!=expected:raise ValueError('manifest differs from installable directories')
    for row in rows:
        base=skill_path(row);text=(base/'SKILL.md').read_text();meta=yaml.safe_load(text.split('---',2)[1])
        if meta['name']!=row['name'] or str(meta.get('version',meta.get('metadata',{}).get('version')))!=row['version']:raise ValueError('metadata mismatch '+row['name'])
        if not meta.get('description'):raise ValueError('missing description')
        for ref in re.findall(r'\]\(([^)]+)\)',text):
            if '://' in ref or ref.startswith('#'):continue
            p=(base/unquote(ref.split('#')[0])).resolve()
            if not p.is_relative_to(base.resolve()) or not p.is_file():raise ValueError('unsafe/missing resource '+row['name']+':'+ref)
        for ref in row.get('required_resources',[])+row.get('entrypoints',[]):
            p=(base/ref).resolve()
            if not p.is_relative_to(base.resolve()) or not p.is_file():raise ValueError('missing manifest resource '+str(p))
        for p in files(base):
            if p.suffix=='.py':ast.parse(p.read_text())
    return m

def install(m,dest):
    dest=Path(dest).absolute()
    for p in [dest,*dest.parents]:
        if p.is_symlink():raise ValueError('symlink install ancestor refused')
    dest.mkdir(parents=True,exist_ok=True);receipt={};completed=[];active=None
    with tempfile.TemporaryDirectory(prefix='.skills-upgrade-',dir=dest) as temp:
        temp=Path(temp)
        try:
            # Stage and hash all packages before any replacement.
            for row in m['skills']:
                src=skill_path(row);stage=temp/(row['name']+'-new');shutil.copytree(src,stage,ignore=shutil.ignore_patterns('__pycache__','*.pyc'));expected=hashes(src)
                if hashes(stage)!=expected:raise ValueError('staging readback mismatch')
                target=dest/row['name'];old=temp/(row['name']+'-old')
                if target.is_symlink():raise ValueError('symlink target refused')
                if target.exists():
                    text=(target/'SKILL.md').read_text();meta=yaml.safe_load(text.split('---',2)[1])
                    if meta.get('name')!=row['name']:raise ValueError('target ownership mismatch')
            for row in m['skills']:
                target=dest/row['name'];old=temp/(row['name']+'-old');stage=temp/(row['name']+'-new');active=(target,old)
                if target.exists():os.replace(target,old)
                os.replace(stage,target);completed.append((target,old));active=None
                if hashes(target)!=hashes(skill_path(row)):raise ValueError('installed readback mismatch')
                receipt[row['name']]={'version':row['version'],'files':hashes(target)}
        except BaseException:
            if active and active[1].exists():
                if active[0].exists():shutil.rmtree(active[0])
                os.replace(active[1],active[0])
            for target,old in reversed(completed):
                if target.exists():shutil.rmtree(target)
                if old.exists():os.replace(old,target)
            raise
    (dest/('.'+ROOT.name+'-receipt.json')).write_text(json.dumps({'suite_version':m['version'],'skills':receipt},ensure_ascii=False,indent=2)+'\n')
    return receipt

def package(m,output):
    output=Path(output);output.mkdir(parents=True,exist_ok=True);archives=[]
    def archive(path,members):
        with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED) as z:
            for label,p in sorted(members):
                zi=zipfile.ZipInfo(label,(2026,1,1,0,0,0));zi.external_attr=0o100644<<16;zi.compress_type=zipfile.ZIP_DEFLATED;z.writestr(zi,p.read_bytes())
        with zipfile.ZipFile(path) as z:
            if len(z.namelist())!=len(set(z.namelist())):raise ValueError('duplicate archive members')
            for label,p in members:
                if z.read(label)!=p.read_bytes():raise ValueError('archive readback mismatch')
        archives.append(path)
    whole=[]
    for row in m['skills']:
        members=[(row['name']+'/'+str(p.relative_to(skill_path(row))),p) for p in files(skill_path(row))];whole+=members;archive(output/f"{row['name']}-{row['version']}.zip",members)
    metadata=[ROOT/'skills-manifest.json',ROOT/'README.md',ROOT/'CHANGELOG.md',ROOT/'MIGRATION.md',ROOT/'scripts/release.py']
    if (ROOT/'LICENSE').is_file():metadata.append(ROOT/'LICENSE')
    # Aggregate installer paths must match the flattened archive layout.
    packaged_manifest=json.loads(json.dumps(m))
    for row in packaged_manifest['skills']:row.pop('path',None)
    with tempfile.TemporaryDirectory() as temp:
        mp=Path(temp)/'skills-manifest.json';mp.write_text(json.dumps(packaged_manifest,ensure_ascii=False,indent=2)+'\n');members=whole+[(str(p.relative_to(ROOT)),p) for p in metadata if p.name!='skills-manifest.json']+[('skills-manifest.json',mp)]
        archive(output/f'{ROOT.name}-{m["version"]}.zip',members)
    (output/'SHA256SUMS').write_text(''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n' for p in archives));return len(archives)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--package',type=Path);p.add_argument('--install',type=Path);a=p.parse_args()
    try:
        m=validate()
        if a.package:print('Packaged',package(m,a.package))
        if a.install:print('Installed/read back',len(install(m,a.install)))
        print('PASS',len(m['skills']),'independent skills')
    except (ValueError,KeyError,TypeError,OSError,SyntaxError) as e:p.exit(2,str(e)+'\n')
