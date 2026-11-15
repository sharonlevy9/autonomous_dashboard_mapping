import math, json, sys
OUT = sys.argv[1]
# kind, name, role, count_in_tool, dims
import lists
P = lists.TOOL if sys.argv[2]=="tool" else lists.STATION
TITLE = "כלי" if sys.argv[2]=="tool" else "עמדה (רותם), בנפרד מהכלי"
S = 3.0  # font mm
def f(x):
    s=('%.2f'%x).rstrip('0').rstrip('.'); return s
def rect(x,y,w,h,cls="cut"): return f'<rect x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}" class="{cls}"/>'
def lab(x,y,w,h,t):
    if w>=11 and h>=5: return f'<text x="{x+w/2:.3f}" y="{y+h/2+1:.3f}" class="d" text-anchor="middle">{t}</text>'
    return ''
TAB=5
def box(L,W,H):
    # cross net: column of L-wide faces: H, W, H, W ; side flaps H x W beside 2nd face
    w=L+2*H+0; h=2*W+2*H
    x0=H; e=[]
    y=0
    faces=[(x0,0,L,H),(x0,H,L,W),(x0,H+W,L,H),(x0,2*H+W,L,W),(0,H,H,W),(x0+L,H,H,W)]
    # tabs (gray) on side flaps top/bottom edges
    tabs=[]
    for (fx,fy,fw,fh) in faces[4:]:
        t=min(TAB,fh/2,fw/2) if False else min(TAB,max(1.5,min(fw,fh)/2))
        tabs.append(f'<polygon class="tab" points="{fx:.3f},{fy:.3f} {fx+fw:.3f},{fy:.3f} {fx+fw-min(t,fw/3):.3f},{fy-t:.3f} {fx+min(t,fw/3):.3f},{fy-t:.3f}"/>')
        tabs.append(f'<polygon class="tab" points="{fx:.3f},{fy+fh:.3f} {fx+fw:.3f},{fy+fh:.3f} {fx+fw-min(t,fw/3):.3f},{fy+fh+t:.3f} {fx+min(t,fw/3):.3f},{fy+fh+t:.3f}"/>')
    # tab on last face bottom
    fx,fy,fw,fh=faces[3]; t=min(TAB,max(1.5,fw/3))
    tabs.append(f'<polygon class="tab" points="{fx:.3f},{fy+fh:.3f} {fx+fw:.3f},{fy+fh:.3f} {fx+fw-t:.3f},{fy+fh+t:.3f} {fx+t:.3f},{fy+fh+t:.3f}"/>')
    labs={0:(L,H),1:(L,W),2:(L,H),3:(L,W),4:(H,W),5:(H,W)}
    for i,(fx,fy,fw,fh) in enumerate(faces):
        e.append(rect(fx,fy,fw,fh)); a,b=labs[i]; e.append(lab(fx,fy,fw,fh,f'{f(a)}×{f(b)}'))
    return w,h+TAB,''.join(tabs+e), f'קופסה: {f(L)} × {f(W)} × {f(H)}', 5
def cyl(D,H):
    C=math.pi*D; e=[]
    e.append(f'<polygon class="tab" points="{C:.3f},0 {C+TAB:.3f},{min(TAB,H/3):.3f} {C+TAB:.3f},{H-min(TAB,H/3):.3f} {C:.3f},{H:.3f}"/>')
    e.append(rect(0,0,C,H)); e.append(lab(0,0,C,H,f'{f(C)}×{f(H)} (עוטף)'))
    r=D/2; gy=H+4
    for k in range(2):
        cx=r+k*(D+6); cy=gy+r
        e.append(f'<circle cx="{cx:.3f}" cy="{cy:.3f}" r="{r:.3f}" class="cut"/>')
        e.append(f'<circle cx="{cx:.3f}" cy="{cy:.3f}" r="0.6" class="pt"/>')
        if D>=14: e.append(f'<text x="{cx:.3f}" y="{cy+r/2+1:.3f}" class="d" text-anchor="middle">Ø{f(D)} r{f(r)}</text>')
    w=max(C+TAB,2*D+6); h=gy+D
    return w,h,''.join(e), f'גליל: קוטר {f(D)}, גובה {f(H)} · מלבן עוטף {f(C)} × {f(H)} + 2 עיגולים ברדיוס {f(r)}', 3
items=[]
for kind,name,role,n,d in P:
    w,h,svg,dims,per = (box(*d) if kind=="box" else cyl(*d))
    cut = n if kind=="box" else n
    pieces = 'קופסה אחת מקופלת' if kind=='box' else 'מלבן אחד + 2 עיגולים'
    items.append(dict(name=name,role=role,n=n,w=w,h=h,svg=svg,dims=dims,pieces=pieces))
# shelf pack A3 297x420, margin 10, header 17mm, footer 18mm
PW,PH,M=297,420,10; HEAD=18; GAP=8; TOP=16; BOT=22
pages=[[]]; x=M; y=M+TOP; rowh=0
import textwrap
def fw(it):
    t=max(len(it['name'])*2.0, len(it['dims'])*1.5, 60)
    return min(max(it['w'], min(t,140)), 277)
def lines(it):
    W=fw(it); n=max(20,int(W/1.5))
    L=[('hd',it['name'])]
    for t,c in [('תפקיד: '+it['role'],'rl'),(f"בכלי: {it['n']} · לחתוך: {it['n']} · {it['pieces']}",'ct'),(it['dims'],'ct')]:
        for p in textwrap.wrap(t,n): L.append((c,p))
    return L
order=sorted(range(len(items)), key=lambda i:-items[i]['h'])
order=list(range(len(items)))
for i in order:
    it=items[i]; W=fw(it); Hh=it['h']+4+3.7*len(lines(it))
    if x+W>PW-M: x=M; y+=rowh+GAP; rowh=0
    if y+Hh>PH-M-BOT: pages.append([]); x=M; y=M+TOP; rowh=0
    pages[-1].append((i,x,y)); x+=W+GAP; rowh=max(rowh,Hh)
np=len(pages); html=['''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><style>
@page{size:297mm 420mm;margin:0} body{margin:0;font-family:"Liberation Sans",Arial,sans-serif}
.pg{width:297mm;height:420mm;position:relative;page-break-after:always;overflow:hidden}
svg{position:absolute;left:0;top:0}
.cut{fill:none;stroke:#000;stroke-width:0.35} .tab{fill:#ddd;stroke:#888;stroke-width:0.25}
.pt{fill:#000} .d{font-size:2.8px;fill:#d00;font-weight:bold;direction:ltr}
.hd{font-size:3.4px;font-weight:bold} .rl{font-size:2.6px} .ct{font-size:2.6px;fill:#333} .sm{font-size:2.6px}
</style></head><body>''']
for pi,pg in enumerate(pages):
    s=[f'<div class="pg"><svg width="297mm" height="420mm" viewBox="0 0 297 420" xmlns="http://www.w3.org/2000/svg">']
    s.append(f'<text x="{PW-M}" y="{M+5}" class="hd" text-anchor="start" direction="rtl">פריסות מידות כוללות 1:1 · {TITLE} · עמוד {pi+1} מתוך {np} · כל המידות במ״מ · עודכן 14.11.2026</text>')
    for (i,x,y) in pg:
        it=items[i]; W=fw(it); xr=PW-x  # mirror: RTL layout from right
        left=PW-x-W
        LL=lines(it)
        for k,(c,t) in enumerate(LL):
            s.append(f'<text x="{left+W:.2f}" y="{y+4+3.7*k:.2f}" class="{c}" direction="rtl">{t}</text>')
        ox=left+W-it['w']
        s.append(f'<g transform="translate({ox:.3f},{y+3.7*len(LL)+4:.3f})">{it["svg"]}</g>')
    fy=PH-M-8
    s.append(f'<line x1="{M}" y1="{fy}" x2="{M+50}" y2="{fy}" stroke="#000" stroke-width="0.6"/><line x1="{M}" y1="{fy-2}" x2="{M}" y2="{fy+2}" stroke="#000" stroke-width="0.4"/><line x1="{M+50}" y1="{fy-2}" x2="{M+50}" y2="{fy+2}" stroke="#000" stroke-width="0.4"/>')
    s.append(f'<text x="{M+25}" y="{fy+5}" class="sm" text-anchor="middle" direction="rtl">בדיקה: 50 מ״מ</text>')
    s.append(f'<text x="{PW-M}" y="{fy+5}" class="sm" direction="rtl">מספר אדום: מידות הפאה. קו שחור: לחתוך. אפור: לשונית הדבקה. בעיגול: הקוטר, ואחריו הרדיוס למחוגה. אלה צורות כלליות לחיתוך, לא שרטוט מדויק.</text>')
    s.append('</svg></div>'); html.append(''.join(s))
html.append('</body></html>')
open(OUT+'.html','w').write(''.join(html))
json.dump([dict(name=it['name'],role=it['role'],n=it['n'],dims=it['dims'],pieces=it['pieces']) for it in items],open(OUT+'.json','w'),ensure_ascii=False,indent=0)
print('pages',np,'items',len(items))
