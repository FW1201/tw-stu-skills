#!/usr/bin/env python3
"""Capacity-constrained local schedules; no Calendar mutation."""
from datetime import datetime,timedelta,timezone
from zoneinfo import ZoneInfo
from hashlib import sha256
from io_utils import run,number

def fold(s):
    # RFC5545 75-octet physical lines, with continuation space.
    lines=[];line=''
    for c in s:
        if len((line+c).encode())>75:lines.append(line);line=' '+c
        else:line+=c
    return '\r\n'.join(lines+[line])
def escape(s):return s.replace('\\','\\\\').replace('\n','\\n').replace(';','\\;').replace(',','\\,')

def plan(d):
    tz=ZoneInfo(d['timezone']);buffer=number(d.get('buffer_fraction',.15));chunk=d.get('chunk_minutes',25)
    if not 0<=buffer<1 or type(chunk)is not int or chunk<=0:raise ValueError('invalid buffer or chunk')
    tasks=d['tasks'];ids=[x['id'] for x in tasks]
    if len(set(ids))!=len(ids) or any(not isinstance(x,str) or not x for x in ids):raise ValueError('unique nonempty task ids required')
    for x in tasks:
        if type(x['minutes'])is not int or x['minutes']<=0 or not x['title'].strip():raise ValueError('positive integer minutes and title required')
    def dt(s):
        t=datetime.fromisoformat(s)
        if t.tzinfo is None:raise ValueError('explicit UTC offset required')
        return t.astimezone(tz)
    slots=sorted([(dt(x['start']),dt(x['end'])) for x in d['slots']])
    if any(a>=b for a,b in slots) or any(slots[i][1]>slots[i+1][0] for i in range(len(slots)-1)):raise ValueError('invalid or overlapping availability')
    blocked=[(dt(x['start']),dt(x['end'])) for x in d.get('blocked',[])]
    if any(a>=b for a,b in blocked):raise ValueError('invalid blocked interval')
    for bs,be in blocked:
        parts=[]
        for s,e in slots:
            if be<=s or bs>=e:parts.append((s,e))
            else:
                if s<bs:parts.append((s,min(bs,e)))
                if be<e:parts.append((max(be,s),e))
        slots=parts
    remain={t['id']:t['minutes'] for t in tasks};segments={x:0 for x in ids};events=[];capacity=0
    for start,end in slots:
        budget=int((end-start).total_seconds()/60*(1-buffer));capacity+=budget;cursor=start
        for t in tasks:
            deadline=dt(t['deadline']) if t.get('deadline') else None
            while remain[t['id']]>0 and budget>0:
                amount=min(remain[t['id']],chunk,budget)
                if deadline and cursor+timedelta(minutes=amount)>deadline:break
                finish=cursor+timedelta(minutes=amount);index=segments[t['id']];uid=sha256((d['plan_id']+'|'+t['id']+'|'+str(index)).encode()).hexdigest()[:32]+'@local-study'
                events.append({'task_id':t['id'],'title':t['title'],'start':cursor.isoformat(),'end':finish.isoformat(),'minutes':amount,'uid':uid});segments[t['id']]+=1;remain[t['id']]-=amount;budget-=amount;cursor=finish
    stamp=d.get('generated_at')
    if not stamp:raise ValueError('generated_at required for reproducible ICS')
    dtstamp=dt(stamp).astimezone(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    lines=['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//TW STUDY//Local plan//ZH-TW','CALSCALE:GREGORIAN']
    for e in events:
        lines+=['BEGIN:VEVENT','UID:'+e['uid'],'DTSTAMP:'+dtstamp,'DTSTART:'+dt(e['start']).astimezone(timezone.utc).strftime('%Y%m%dT%H%M%SZ'),'DTEND:'+dt(e['end']).astimezone(timezone.utc).strftime('%Y%m%dT%H%M%SZ'),'SUMMARY:'+escape(e['title']),'END:VEVENT']
    lines+=['END:VCALENDAR'];markdown='# 學習計畫\n\n'+ '\n'.join(f"- {e['start']}–{e['end']}：{e['title']}（{e['minutes']} 分）" for e in events)
    return {'plan_id':d['plan_id'],'timezone':d['timezone'],'capacity_minutes':capacity,'scheduled_minutes':sum(e['minutes'] for e in events),'unscheduled':[{'task_id':k,'minutes':v} for k,v in remain.items() if v],'events':events,'markdown':markdown,'ics':'\r\n'.join(fold(x) for x in lines)+'\r\n','limitations':['僅本機日程內容；尚未寫入 Calendar。重排時以 plan_id/task_id/segment UID 對照，刪除旧多餘事件需另確認。']}
if __name__=='__main__':run(plan)
