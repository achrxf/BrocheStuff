import sys
FIT=r'''
/* ---------- the tool table fits the space it has (no sideways scrolling unless the window is really too small) ----------
   The wide text columns (type, holder, insert, your own columns) give up room down to a readable minimum;
   the widths you set by dragging stay as you set them when there is room. */
function ttFit(){const tw=document.querySelector(".ed .tw"),tb=tw&&tw.querySelector("table.tt");if(!tb||window.innerWidth<761)return;
  const avail=tw.clientWidth;if(!avail)return;const ths=[...tb.querySelectorAll("thead tr:first-child th[data-ck]")];if(!ths.length)return;
  const MIN={type:140,holder:100,insert:76},ACT=76;
  const C=ths.map(th=>{const k=th.dataset.ck;return{th,k,w:thW(k)||0,min:MIN[k]||(k.startsWith("x_")?64:null)}});
  const fixed=C.filter(c=>c.w).reduce((s,c)=>s+c.w,0)+ACT,typ=C.find(c=>c.k==="type"&&!c.w);
  // Type without its own width takes what is left; it still needs its minimum
  let need=fixed+(typ?MIN.type:0);
  // first the wide text columns, then (a little) the small ones
  const SMALL={t:52,asm:72,corr:54,diameter:46,ra:48,ls:42,oal:44,z:32,code:66};
  [c=>c.min,c=>c.min==null?SMALL[c.k]:null].forEach(minOf=>{if(need<=avail)return;let over=need-avail;
    const fl=C.filter(c=>c.w&&minOf(c)!=null&&c.w>minOf(c)),room=fl.reduce((s,c)=>s+(c.w-minOf(c)),0);
    if(room>0){const f=Math.min(1,over/room);fl.forEach(c=>c.w=Math.max(minOf(c),Math.round(c.w-(c.w-minOf(c))*f)))}
    need=C.filter(c=>c.w).reduce((s,c)=>s+c.w,0)+ACT+(typ?MIN.type:0)});
  C.forEach(c=>{c.th.style.width=c.w?c.w+"px":""});
  tb.style.minWidth=need>avail?need+"px":"0px";tb.style.width="100%"}
let ttRO=null;
function ttWatch(){const tw=document.querySelector(".ed .tw");if(!tw)return;if(ttRO)ttRO.disconnect();
  if(window.ResizeObserver){ttRO=new ResizeObserver(()=>{cancelAnimationFrame(ttWatch.r);ttWatch.r=requestAnimationFrame(ttFit)});ttRO.observe(tw)}ttFit()}

/* ---------- 4. reports ---------- */'''
R=[
('''
/* ---------- 4. reports ---------- */''',FIT),
# the table no longer asks for every column's full width
('''<div class="tw"><table class="tt" style="min-width:${edCols(sheetCfg()).reduce((n,k)=>n+(thW(k)||220),0)+80}px">''','''<div class="tw"><table class="tt">'''),
('''  renderRows();checkDup();prStyle();''','''  renderRows();checkDup();prStyle();setTimeout(ttWatch,0);'''),
# after a drag (or a double-click back to the automatic size), fit again
('''lsSet(CWKEY,JSON.stringify(m))};
    h.addEventListener("pointermove",mv);''','''lsSet(CWKEY,JSON.stringify(m));ttFit()};
    h.addEventListener("pointermove",mv);'''),
('''th.style.width=thW(k)?thW(k)+"px":"";table.style.minWidth=[...table.querySelectorAll("thead th[data-ck]")].reduce((n,x)=>n+(thW(x.dataset.ck)||220),0)+80+"px"}});''','''th.style.width=thW(k)?thW(k)+"px":"";ttFit()}});'''),
('''.tt{width:100%;border-collapse:collapse;min-width:780px}''','''.tt{width:100%;border-collapse:collapse}
@media (min-width:761px){.tt{table-layout:fixed}.tt td,.tt th{overflow:hidden}.tt th{text-overflow:ellipsis}}
@media (max-width:1500px) and (min-width:1051px){.ed:not(.nopv){grid-template-columns:minmax(480px,1fr) var(--pvw,minmax(360px,34%))}}'''),
]
for f in sys.argv[1:]:
  s=open(f).read()
  for a,b in R:
    assert s.count(a)==1,(f,s.count(a),a[:90]);s=s.replace(a,b)
  open(f,'w').write(s);print("patched",f)
# also: pvOn default closed below 1150px unless turned on
