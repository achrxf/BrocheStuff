/* ===================== 2.26 ATELIER: skin switch, day/night, motion, cabinet map ===================== */
Object.assign(I18N.fr,{skinAt:"Nouvelle interface (Atelier)",skinCl:"Interface classique",skinAtT:"Passer à la nouvelle interface Atelier",skinClT:"Revenir à l’ancienne interface (rien n’est perdu, vous pouvez revenir)",
  skinToAt:"Nouvelle interface Atelier",skinToCl:"Interface classique",dnDay:"Jour",dnNight:"Nuit",dnT:"Mode jour ou nuit",
  planList:"Liste",planMap:"Plan des armoires",planMapT:"Voir le magasin comme il est rangé : chaque armoire et ses tiroirs",
  planDrawer:"Tiroir",planContent:"Contenu",planN:n=>`${n} outil${n>1?"s":""}`,planPrint:"Imprimer l’étiquette",planShowList:"Voir dans la liste",
  planNoLoc:"Sans emplacement",planNoLocT:"Cliquez un code pour lui donner un emplacement",planEmpty:"Aucun outil n’a encore d’emplacement. Donnez un emplacement à vos outils (« + emplacement ») et le plan des armoires se dessine ici.",
  planLow:n=>`▼ ${n} tiroir${n>1?"s":""} à recompléter`,planOk:"Stock complet",planHint:"Cliquez un tiroir pour voir ce qu’il contient.",
  planSum:(c,d)=>`Vue de face · ${c} armoire${c>1?"s":""} · ${d} tiroir${d>1?"s":""}`,planStock:(s,m)=>`${s} / min ${m}`,planNoMatch:"Aucun tiroir ne correspond au filtre."});
Object.assign(I18N.en,{skinAt:"New look (Atelier)",skinCl:"Classic look",skinAtT:"Switch to the new Atelier look",skinClT:"Go back to the old look (nothing is lost, you can come back)",
  skinToAt:"New Atelier look",skinToCl:"Classic look",dnDay:"Day",dnNight:"Night",dnT:"Day or night mode",
  planList:"List",planMap:"Cabinet map",planMapT:"See the crib the way it is stored: every cabinet and its drawers",
  planDrawer:"Drawer",planContent:"Contents",planN:n=>`${n} tool${n>1?"s":""}`,planPrint:"Print the label",planShowList:"Show in the list",
  planNoLoc:"No location",planNoLocT:"Click a code to give it a location",planEmpty:"No tool has a location yet. Give your tools a location (“+ location”) and the cabinet map draws itself here.",
  planLow:n=>`▼ ${n} drawer${n>1?"s":""} to refill`,planOk:"Stock complete",planHint:"Click a drawer to see what is in it.",
  planSum:(c,d)=>`Front view · ${c} cabinet${c>1?"s":""} · ${d} drawer${d>1?"s":""}`,planStock:(s,m)=>`${s} / min ${m}`,planNoMatch:"No drawer matches the filter."});

const SKINKEY="bs.skin";
const isAt=()=>document.documentElement.classList.contains("at");
const atRM=()=>{try{return matchMedia("(prefers-reduced-motion: reduce)").matches}catch(_){return false}};
function drawSkinBtn(){const b=$("#b-skin");if(!b)return;const at=isAt();
  b.innerHTML=`<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${at?'<path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5"/>':'<path d="M12 3l2.6 5.6L20 9.3l-4 4.1.9 5.6L12 16.4 7.1 19l.9-5.6-4-4.1 5.4-.7z"/>'}</svg><span class="lbl">${esc(at?t("skinCl"):t("skinAt"))}</span>`;
  b.title=at?t("skinClT"):t("skinAtT")}
function setSkin(at){const r=document.documentElement;try{localStorage.setItem(SKINKEY,at?"at":"classic")}catch(_){}
  r.classList.toggle("at",at);r.classList.add("skinning");setTimeout(()=>r.classList.remove("skinning"),500);
  drawSkinBtn();drawDayNight();try{if(route&&route.view==="article")render();else if(window.__rzApply)window.__rzApply()}catch(_){}requestAnimationFrame(navMark);toast(at?t("skinToAt"):t("skinToCl"))}
function drawDayNight(){const w=$("#b-dn");if(!w)return;const dark=curTheme()==="dark";
  w.title=t("dnT");w.setAttribute("aria-label",t("dnT"));
  w.innerHTML=`<button type="button" data-dn="light" aria-pressed="${!dark}" aria-label="${esc(t("dnDay"))}" title="${esc(t("dnDay"))}">${sunIcon}<span>${esc(t("dnDay"))}</span></button><button type="button" data-dn="dark" aria-pressed="${dark}" aria-label="${esc(t("dnNight"))}" title="${esc(t("dnNight"))}">${moonIcon}<span>${esc(t("dnNight"))}</span></button>`}
function setDayNight(th){if(th===curTheme())return;const r=document.documentElement;r.classList.add("theming");lsSet(THEMEKEY,th);applyTheme(th);drawDayNight();setTimeout(()=>r.classList.remove("theming"),420)}
// header: skin button (goes in the ⋯ menu with the other settings) and the day/night switch
(function(){const top=$("header.top");if(!top)return;
  if(!$("#b-skin")){const b=document.createElement("button");b.className="tb";b.id="b-skin";b.type="button";const a=$("#b-theme");a?a.after(b):top.appendChild(b);b.onclick=()=>setSkin(!isAt())}
  if(!$("#b-dn")){const w=document.createElement("div");w.className="daynight";w.id="b-dn";w.setAttribute("role","group");const f=$("#b-find");(f||$("#tbar")).after(w);
    w.onclick=e=>{const b=e.target.closest("[data-dn]");if(b)setDayNight(b.dataset.dn)}}
  drawSkinBtn();drawDayNight()})();
{const c0=chrome;chrome=function(){c0.apply(this,arguments);drawSkinBtn();drawDayNight()}}
{const a0=applyTheme;applyTheme=function(){a0.apply(this,arguments);drawDayNight()}}
try{matchMedia("(prefers-color-scheme: dark)").addEventListener("change",()=>drawDayNight())}catch(_){}

/* sliding red underline under the current page in the main menu */
function navMark(){const nav=$(".mainnav");if(!nav)return;const b=nav.querySelector('button[aria-current="true"]:not([hidden])');
  if(!b||!b.offsetWidth){nav.style.setProperty("--no","0");return}
  nav.style.setProperty("--nx",b.offsetLeft+8+"px");nav.style.setProperty("--nw",Math.max(0,b.offsetWidth-16)+"px");nav.style.setProperty("--no","1")}
addEventListener("resize",()=>navMark());

/* page entrance: rows, cards and gauges come in once when you change page (not on every small redraw) */
let navinT=null;
function countUp(){if(atRM())return;document.querySelectorAll(".tile4 b,.ov-n b,.mc .ct b,.bigstock").forEach(el=>{
  const txt=el.textContent.trim();if(!/^\d{1,5}$/.test(txt))return;const to=+txt;if(to<2)return;const t0=performance.now(),D=Math.min(700,260+to*2);
  const step=now=>{const k=Math.min(1,(now-t0)/D),e=1-Math.pow(1-k,3);el.textContent=String(Math.round(to*e));if(k<1&&el.isConnected)requestAnimationFrame(step);else el.textContent=txt};requestAnimationFrame(step)})}
function navIn(){const r=document.documentElement;navMark();if(!isAt()||atRM())return;
  r.classList.remove("navin");void r.offsetWidth;r.classList.add("navin");clearTimeout(navinT);navinT=setTimeout(()=>r.classList.remove("navin"),1100);countUp()}
addEventListener("hashchange",()=>setTimeout(navIn,0));
setTimeout(navIn,0);
{const r0=render;render=function(){r0.apply(this,arguments);navMark()}}

/* stock buttons: the number jumps when it changes */
{const f0=refreshCribRow;refreshCribRow=function(c){f0.apply(this,arguments);try{const sp=document.querySelector(`#crows tr[data-code="${CSS.escape(c.code)}"] .stepper span`);if(sp){sp.classList.remove("bump");void sp.offsetWidth;sp.classList.add("bump")}}catch(_){}}}

/* ---------- plan des armoires (tool crib) ---------- */
let cribView=(()=>{try{return localStorage.getItem("bs.cribview")==="plan"?"plan":"list"}catch(_){return"list"}})();
let planSel=null;
const pnCmp=(a,b)=>String(a).localeCompare(String(b),undefined,{numeric:true,sensitivity:"base"});
function splitLoc(loc){const s=clean(loc);if(!s)return null;
  const m=s.match(/^(.*\S)\s*[-–—\/|:·>]\s*([^-–—\/|:·>]+)$/);if(m&&m[1].trim()&&m[2].trim())return{c:m[1].trim(),d:m[2].trim()};
  const m2=s.match(/^(.*\S)\s+(\d+[A-Za-z]?|[A-Za-z]\d+)$/);if(m2)return{c:m2[1].trim(),d:m2[2]};
  return{c:s,d:"—"}}
function planModel(){const C=new Map(),noloc=[];
  (db.catalog||[]).forEach(c=>{const p=splitLoc(c.location);if(!p){noloc.push(c);return}
    const ck=p.c.toUpperCase();if(!C.has(ck))C.set(ck,{name:p.c,dr:new Map()});const cab=C.get(ck);const dk=p.d.toUpperCase();
    if(!cab.dr.has(dk))cab.dr.set(dk,{id:p.d,items:[]});cab.dr.get(dk).items.push(c)});
  const cabs=[...C.values()].sort((a,b)=>pnCmp(a.name,b.name)).map(cab=>{const drs=[...cab.dr.values()].sort((a,b)=>pnCmp(a.id,b.id));
    const rc=drs.every(d=>/^\d+\s*[A-Za-z]$/.test(d.id));let cols,place=null;
    if(rc&&drs.length>1){const L=[...new Set(drs.map(d=>d.id.slice(-1).toUpperCase()))].sort(),R=[...new Set(drs.map(d=>parseInt(d.id)))].sort((a,b)=>a-b);
      if(L.length<=4&&R.length<=12){cols=L.length;place=d=>({r:R.indexOf(parseInt(d.id))+1,c:L.indexOf(d.id.slice(-1).toUpperCase())+1});
        cab.slots=R.length*L.length}}
    if(!cols)cols=drs.length<=3?Math.max(1,drs.length):drs.length<=10?2:3;
    return{name:cab.name,drs,cols,place,total:drs.reduce((a,d)=>a+d.items.length,0)}});
  return{cabs,noloc}}
function planMatch(){const q=(cribQ||"").trim().toLowerCase().replace(/^ø/,""),terms=q.split(/\s+/).filter(Boolean);
  const f=cribF;const active=f!=="all"||terms.length>0;
  const ok=c=>(f==="all"||(f==="noloc"?!clean(c.location):stockState(c)===f))&&terms.every(w=>[c.code,c.type,c.diameter,"ø"+c.diameter,c.ref,c.location,c.supplier,c.family].join(" ").toLowerCase().includes(w));
  return{active,ok}}
function ticksHTML(s,m){const N=Math.max(6,Math.min(10,Math.max(m*2,s)));let h="";for(let i=0;i<N;i++)h+=`<i class="${i<s?"f":""}${m>0&&i===m-1?" m":""}"></i>`;return `<span class="ticks" aria-hidden="true">${h}</span>`}
function drawPlan(){const box=$("#cres");if(!box)return;box.querySelectorAll(":scope > .list, :scope > .empty, :scope > .note, :scope > .plan").forEach(e=>e.remove());
  const M=planModel(),{active,ok}=planMatch();
  if(!M.cabs.length){const d=document.createElement("div");d.className="plan";d.innerHTML=`<div class="empty2" style="flex:1">${esc(t("planEmpty"))}</div>${M.noloc.length?nolocHTML(M.noloc,ok):""}`;box.appendChild(d);bindNoloc(d);return}
  const allDr=[];M.cabs.forEach(c=>c.drs.forEach(d=>allDr.push({cab:c,d})));
  const hits=allDr.filter(x=>x.d.items.some(ok));
  if(!planSel||!allDr.some(x=>x.cab.name+"\u0001"+x.d.id===planSel)||(active&&!hits.some(x=>x.cab.name+"\u0001"+x.d.id===planSel))){const first=(active?hits[0]:null)||allDr[0];planSel=first?first.cab.name+"\u0001"+first.d.id:null}
  const cabHTML=M.cabs.map(c=>{const any=c.drs.some(d=>d.items.some(ok)),lowN=c.drs.filter(d=>d.items.some(x=>/^(low|out)$/.test(stockState(x)))).length;
    const cells=c.drs.map(d=>{const key=c.name+"\u0001"+d.id,h=d.items.some(ok),low=d.items.some(x=>/^(low|out)$/.test(stockState(x)));
      const pos=c.place?`grid-row:${c.place(d).r};grid-column:${c.place(d).c}`:"";
      return `<button type="button" class="drw${key===planSel?" on":""}${active?(h?" hit":" miss"):""}" data-dk="${esc(key)}" style="${pos}" aria-pressed="${key===planSel}" aria-label="${esc(c.name+" · "+d.id+" · "+t("planN",d.items.length))}"><span>${esc(d.id)}</span><small>${d.items.length}</small>${low?'<span class="lowm" aria-hidden="true">▼</span>':""}</button>`}).join("");
    return `<div class="cab${active&&!any?" dim":""}"><div class="chd"><span title="${esc(c.name)}">${esc(c.name)}</span><b>${c.drs.length}</b></div><div class="cbody" style="grid-template-columns:repeat(${c.cols},minmax(64px,1fr))">${cells}</div><div class="feet"><i></i><i></i></div><div class="cdim">${esc(t("planN",c.total))}</div><div class="clow" style="${lowN?"":"color:var(--done)"}">${esc(lowN?t("planLow",lowN):t("planOk"))}</div></div>`}).join("");
  const nd=allDr.length;
  const wrap=document.createElement("div");wrap.className="plan";
  wrap.innerHTML=`<div class="cabs" role="group" aria-label="${esc(t("planMap"))}">${active&&!hits.length?`<div class="empty2" style="flex-basis:100%">${esc(t("planNoMatch"))}</div>`:""}${cabHTML}${M.noloc.length&&(cribF==="all"||cribF==="noloc"||active)?nolocHTML(M.noloc,ok):""}<div style="flex-basis:100%;font:400 11.5px var(--mono);color:var(--soft)">${esc(t("planSum",M.cabs.length,nd))} · ${esc(t("planHint"))}</div></div><aside class="side" aria-live="polite" id="planside"></aside>`;
  box.appendChild(wrap);drawPlanSide(M);
  wrap.querySelector(".cabs").onclick=e=>{const b=e.target.closest("[data-dk]");if(!b)return;planSel=b.dataset.dk;
    wrap.querySelectorAll(".drw.on").forEach(x=>{x.classList.remove("on");x.setAttribute("aria-pressed","false")});b.classList.add("on");b.setAttribute("aria-pressed","true");drawPlanSide(M)};
  bindNoloc(wrap)}
function nolocHTML(list,ok){const L=list.filter(ok).sort((a,b)=>pnCmp(a.code,b.code)),MAX=40;if(!L.length)return"";
  return `<div class="noloc"><span class="cap">${esc(t("planNoLoc"))} · ${L.length}</span>${L.slice(0,MAX).map(c=>`<button type="button" data-nl="${esc(c.code)}" title="${esc(t("planNoLocT"))}">${esc(c.code)}</button>`).join("")}${L.length>MAX?`<span style="font:400 12px var(--mono);color:var(--soft)">+${L.length-MAX}</span>`:""}</div>`}
function bindNoloc(root){root.querySelectorAll("[data-nl]").forEach(b=>b.onclick=()=>{if(hasRight("cribEdit"))locDialog(b.dataset.nl);else go("#c-"+encodeURIComponent(b.dataset.nl))})}
function drawPlanSide(M){const side=$("#planside");if(!side)return;let cab=null,dr=null;
  M.cabs.forEach(c=>c.drs.forEach(d=>{if(c.name+"\u0001"+d.id===planSel){cab=c;dr=d}}));
  if(!dr){side.innerHTML=`<div class="empty2">${esc(t("planHint"))}</div>`;return}
  const {ok,active}=planMatch();const items=dr.items.slice().sort((a,b)=>(active?(ok(b)-ok(a)):0)||pnCmp(a.code,b.code));
  side.innerHTML=`<div class="sh"><div style="min-width:0"><span class="cap">${esc(t("planDrawer"))}</span><span class="bin"><b>${esc(cab.name.toUpperCase())}</b><span>${esc(dr.id)}</span></span></div><div style="text-align:right;flex:none"><span class="cap">${esc(t("planContent"))}</span><span style="font:600 15px var(--mono)">${esc(t("planN",dr.items.length))}</span></div></div>
    <div class="its">${items.map(c=>{const s=stockState(c),low=s==="low"||s==="out",st=+c.stock||0,mn=+c.min||0;
      return `<div class="it${active&&!ok(c)?" off":""}"><button type="button" class="cd" data-go="${esc(c.code)}">${esc(c.code)}</button><span class="tx"><b>${esc(c.type||"—")}${c.diameter?` <span style="font:400 12.5px var(--mono);color:var(--mid)">Ø${esc(normDia(c.diameter))}</span>`:""}</b><i>${esc(c.ref||"")}</i></span><span class="sk${low?" low":""}"><span>${esc(t("planStock",st,mn))}</span>${ticksHTML(st,mn)}</span></div>`}).join("")}</div>
    <div class="sfoot"><button type="button" class="btn" id="pl-print">${pinIcon}${esc(t("planPrint"))}</button><button type="button" class="btn ghost" id="pl-list">${esc(t("planShowList"))}</button></div>`;
  side.querySelectorAll("[data-go]").forEach(b=>b.onclick=()=>go("#c-"+encodeURIComponent(b.dataset.go)));
  const loc=dr.items[0]&&clean(dr.items[0].location);
  side.querySelector("#pl-list").onclick=()=>{setCribView("list");cribQ=loc||"";const q=$("#q");if(q)q.value=cribQ;drawCrib()};
  side.querySelector("#pl-print").onclick=()=>{const G=locGroups().filter(g=>splitLoc(g.loc)&&splitLoc(g.loc).c.toUpperCase()===cab.name.toUpperCase()&&splitLoc(g.loc).d.toUpperCase()===dr.id.toUpperCase());
    const css=`body{font:10px/1.3 "Segoe UI",Arial,sans-serif;color:#111;padding:8mm}.lb{border:1.5px solid #111;padding:4mm 5mm;width:90mm}.lb h2{font-size:22px;margin:0 0 3mm;border-bottom:1px solid #111;padding-bottom:2mm}.it{display:flex;gap:3mm;padding:.6mm 0}.it b{font-family:Consolas,"Courier New",monospace;min-width:14mm}.it span{color:#333}`;
    printHTML({css,body:G.map(g=>`<div class="lb"><h2>${esc(g.loc)}</h2>${g.items.map(it=>`<div class="it"><b>${esc(it.code)}</b><span>${esc(it.txt)}</span></div>`).join("")}</div>`).join("")},false)}}
function setCribView(v){cribView=v;try{localStorage.setItem("bs.cribview",v)}catch(_){}document.querySelectorAll("[data-cview]").forEach(b=>b.setAttribute("aria-pressed",b.dataset.cview===v))}
{const d0=drawCrib;drawCrib=function(){d0.apply(this,arguments);if(cribView==="plan"&&cribF!=="missing"&&$("#cres"))drawPlan()}}
{const r0=renderCrib;renderCrib=function(){r0.apply(this,arguments);const ph=$("#view .ph"),anchor=$("#b-labels")||$("#b-newcode");if(!ph||!anchor||$("#cview"))return;
  const seg=document.createElement("div");seg.className="viewseg";seg.id="cview";seg.setAttribute("role","group");seg.title=t("planMapT");
  seg.innerHTML=`<button type="button" data-cview="list" aria-pressed="${cribView==="list"}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/></svg>${esc(t("planList"))}</button><button type="button" data-cview="plan" aria-pressed="${cribView==="plan"}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><path d="M4 3h7v18H4zM13 3h7v18h-7zM4 9h7M4 15h7M13 9h7M13 15h7"/></svg>${esc(t("planMap"))}</button>`;
  anchor.before(seg);seg.onclick=e=>{const b=e.target.closest("[data-cview]");if(!b||b.dataset.cview===cribView)return;setCribView(b.dataset.cview);drawCrib();if(isAt()&&!atRM()){const p=$("#cres .plan, #cres .list");if(p)p.animate([{opacity:0,transform:"translateY(8px)"},{opacity:1,transform:"none"}],{duration:320,easing:"cubic-bezier(.2,.8,.2,1)"})}}}}
{const a0=afterLoc;afterLoc=function(){a0.apply(this,arguments);try{if($("#cres .plan"))drawCrib()}catch(_){}}}
