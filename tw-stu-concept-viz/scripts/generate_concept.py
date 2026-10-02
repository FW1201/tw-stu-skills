#!/usr/bin/env python3
import argparse,json,html
from pathlib import Path

def render(d):
    nodes=d['nodes'];ids=[x['id'] for x in nodes]
    if not nodes or len(set(ids))!=len(ids) or any(not isinstance(x,str) or not x for x in ids):raise ValueError('unique nonempty node IDs required')
    if any(e['from'] not in ids or e['to'] not in ids for e in d['edges']):raise ValueError('unknown edge')
    if not d.get('questions') or any(not x.get('prompt') or not x.get('answer') for x in d['questions']):raise ValueError('understanding questions and answers required')
    model=d.get('linear')
    if model:
        import math
        for k in ['a','b','min','max','step']:
            if type(model[k])not in [int,float] or not math.isfinite(model[k]):raise ValueError('finite linear model parameters required')
        if model['min']>=model['max'] or model['step']<=0:raise ValueError('invalid slider range')
    def esc(x):return html.escape(str(x))
    buttons=''.join(f'<button type="button" data-node="{esc(n["id"])}">{esc(n["label"])}</button>' for n in nodes)
    alternative=''.join(f'<li><strong>{esc(n["label"])}</strong>：{esc(n["description"])}</li>' for n in nodes)
    relationships=''.join(f'<li>{esc(e["from"])} → {esc(e["to"])}：{esc(e["label"])}</li>' for e in d['edges'])
    questions=''.join(f'<details><summary>{esc(q["prompt"])}</summary><p>{esc(q["answer"])}</p></details>' for q in d['questions'])
    data=json.dumps(d,ensure_ascii=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    slider='<svg id="chart" viewBox="0 0 500 320" role="img" aria-label="一次函數圖形與目前輸入的位置" style="width:100%;max-width:650px"></svg><label for="x">改變 x</label><input id="x" type="range"><output id="result" aria-live="polite"></output>' if model else ''
    return '''<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'''+esc(d['title'])+'''</title><style>body{max-width:850px;margin:auto;padding:24px;font:18px/1.6 sans-serif;color:#17354a}button{font:inherit;margin:8px;padding:12px}button:focus-visible{outline:3px solid #b04800}summary{cursor:pointer}output{display:block}</style><main><h1>'''+esc(d['title'])+'''</h1><nav aria-label="概念節點">'''+buttons+'''</nav><p id="detail" aria-live="polite">選擇一個概念查看說明。</p>'''+slider+'''<h2>文字替代</h2><ul>'''+alternative+'''</ul><h2>關係</h2><ul>'''+relationships+'''</ul><h2>理解與遷移</h2>'''+questions+'''</main><script type="application/json" id="data">'''+data+'''</script><script>const d=JSON.parse(document.getElementById('data').textContent);document.querySelectorAll('[data-node]').forEach(b=>b.addEventListener('click',()=>{const n=d.nodes.find(n=>n.id===b.dataset.node);document.getElementById('detail').textContent=n.label+'：'+n.description}));if(d.linear){const x=document.getElementById('x');for(const k of ['min','max','step'])x[k]=d.linear[k];x.value=d.linear.min;const update=()=>{const y=d.linear.a*Number(x.value)+d.linear.b;document.getElementById('result').textContent='x='+x.value+'，y='+Number(y.toFixed(8));const lo=Math.min(0,d.linear.a*d.linear.min+d.linear.b,d.linear.a*d.linear.max+d.linear.b),hi=Math.max(0,d.linear.a*d.linear.min+d.linear.b,d.linear.a*d.linear.max+d.linear.b),span=hi-lo||1;const px=v=>50+400*(v-d.linear.min)/(d.linear.max-d.linear.min),py=v=>270-220*(v-lo)/span;document.getElementById('chart').innerHTML='<path d="M50 50V270H450" fill="none" stroke="#17354a"/><line x1="50" y1="'+py(d.linear.a*d.linear.min+d.linear.b)+'" x2="450" y2="'+py(d.linear.a*d.linear.max+d.linear.b)+'" stroke="#17354a" stroke-width="3"/><circle cx="'+px(Number(x.value))+'" cy="'+py(y)+'" r="7" fill="#b04800"/><text x="455" y="290">x</text><text x="25" y="40">y</text>'};x.addEventListener('input',update);update()}</script></html>'''
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path);p.add_argument('--validate-only',action='store_true');a=p.parse_args()
    try:
        content=render(json.loads(a.input.read_text()))
        if not a.validate_only:
            if not a.output:raise ValueError('--output required')
            a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(content)
    except (ValueError,KeyError,TypeError,OSError) as e:p.exit(2,str(e)+'\n')
