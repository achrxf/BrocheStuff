import sys
R=[
('''(()=>{const LS=NS+"toolmanager.ui.rz",SEL="table.lt,table.tt";''','''(()=>{const LS=NS+"toolmanager.ui.rz",SEL="table.lt";'''),
('''  // saved widths are stretched to fill a wider page, never squeezed
  const fit=(tb,w)=>{const box=tb.parentElement?tb.parentElement.clientWidth:0,sum=w.reduce((a,b)=>a+b,0);if(!box||sum>=box-2)return w.slice();
    const k=box/sum,o=w.map(x=>Math.floor(x*k));o[o.length-1]+=box-o.reduce((a,b)=>a+b,0);return o};''','''  // saved widths are stretched to fill a wider page, and squeezed (down to a readable minimum) on a narrower one
  const fit=(tb,w)=>{const box=tb.parentElement?tb.parentElement.clientWidth:0,sum=w.reduce((a,b)=>a+b,0);if(!box||Math.abs(sum-box)<=2)return w.slice();
    if(sum>box){const MINW=44,fl=w.map(x=>Math.max(0,x-MINW)),room=fl.reduce((a,b)=>a+b,0),over=sum-box;if(room<=0)return w.slice();
      const f=Math.min(1,over/room),o=w.map((x,i)=>Math.max(MINW,Math.round(x-fl[i]*f)));return o}
    const k=box/sum,o=w.map(x=>Math.floor(x*k));o[o.length-1]+=box-o.reduce((a,b)=>a+b,0);return o};'''),
('''  const view=document.getElementById("view");
  new MutationObserver(ms=>{''','''  const view=document.getElementById("view");
  // a window that changes size: the saved widths fit it again
  let rzT=0;window.addEventListener("resize",()=>{clearTimeout(rzT);rzT=setTimeout(()=>view.querySelectorAll("table.lt.rzfix").forEach(apply),120)});
  new MutationObserver(ms=>{'''),
]
for f in sys.argv[1:]:
  s=open(f).read()
  for a,b in R:
    assert s.count(a)==1,(f,s.count(a),a[:80]);s=s.replace(a,b)
  open(f,'w').write(s);print("patched",f)
# also: apply() trims leftover overflow from the widest column after fit
