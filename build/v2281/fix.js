/* ===================== 2.28.1 · one scrollbar, no sideways bar, the sheet uses the screen ===================== */
// the demo's tutorial button goes at the end of the sheet instead of under it (it made a second scrollbar)
function edFootIn(){const v=$("#view");if(!v)return;const f=v.querySelector(":scope > .guidefoot"),fm=v.querySelector(".ed > .form");if(f&&fm)fm.appendChild(f)}
{const r0=render;render=function(){const r=r0.apply(this,arguments);try{edFootIn()}catch(_){}return r}}
new MutationObserver(()=>{try{edFootIn()}catch(_){}}).observe(document.getElementById("view")||document.body,{childList:true});
// a wide table: the room Type doesn't need goes to the boxes that are cut (holder, insert, code, location, your columns)
function ttGive(){const tw=document.querySelector(".ed .tw"),tb=tw&&tw.querySelector("table.tt");if(!tb||window.innerWidth<761)return;
  const ths=[...tb.querySelectorAll("thead tr:first-child th[data-ck]")],typ=ths.find(th=>th.dataset.ck==="type");if(!typ||typ.style.width)return;
  const idx=th=>[...th.parentElement.children].indexOf(th),rows=[...tb.querySelectorAll("tbody tr[data-i]")].slice(0,80);
  const need=th=>{const i=idx(th);let m=0;rows.forEach(tr=>{const td=tr.children[i];if(!td)return;td.querySelectorAll("input,textarea,.loctag span,.cellv").forEach(el=>{m=Math.max(m,el.scrollWidth-el.clientWidth>0?el.scrollWidth+(el.closest(".loctag")?34:0):0)})});return m};
  let spare=Math.round(typ.getBoundingClientRect().width)-Math.max(160,need(typ)+30);if(spare<20)return;
  const CAP={holder:340,insert:220,code:220,loc:220};
  ths.filter(th=>/^(holder|insert|code|loc)$|^x_/.test(th.dataset.ck)).forEach(th=>{if(spare<10)return;const cur=Math.round(th.getBoundingClientRect().width),n=need(th);if(!n)return;
    const want=Math.min(CAP[th.dataset.ck]||200,n+22)-cur;if(want<=0)return;const g=Math.min(want,spare);th.style.width=(cur+g)+"px";spare-=g})}
{const f0=ttFit;ttFit=function(){const r=f0.apply(this,arguments);try{ttGive()}catch(_){}return r}}
