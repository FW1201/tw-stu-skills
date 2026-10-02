"""Portable JSON CLI IO, provenance and atomic result writes."""
import argparse,hashlib,json,os,sys,tempfile,math
from pathlib import Path

def load(path):
    data=json.loads(Path(path).read_text(encoding='utf-8'),parse_constant=lambda x: (_ for _ in ()).throw(ValueError('nonfinite '+x)))
    if not isinstance(data,dict):raise ValueError('input must be an object')
    return data

def write(path,data):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    text=json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False)+'\n'
    fd,tmp=tempfile.mkstemp(dir=path.parent,prefix='.'+path.name)
    try:
        with os.fdopen(fd,'w',encoding='utf-8') as f:f.write(text)
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)

def run(fn):
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path);p.add_argument('--validate-only',action='store_true');a=p.parse_args()
    try:
        data=load(a.input);result=fn(data)
        result['input_sha256']=hashlib.sha256(a.input.read_bytes()).hexdigest();result['schema_version']='1.0'
        if a.validate_only: print('PASS input and computation');return
        if not a.output:raise ValueError('--output required unless --validate-only')
        write(a.output,result);print(a.output)
    except (ValueError,TypeError,KeyError,OSError,ImportError) as e:p.exit(2,str(e)+'\n')

def number(x):
    if isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x):raise ValueError('expected finite number')
    return float(x)
