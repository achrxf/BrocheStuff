import sys
# 2.25.0: operations. The sheet can hold one line per operation (same T several times) with Operation, Time and Tool life;
# Saisie / PDF / Excel modes: the PDF shows one line per tool (times and tool life added up), the Excel every operation
# with a total, or the same list as the PDF. Sorting only changes the PDF (and the Excel if asked). Old sheets work as before.
BLOCK=r'''/* ---------- 2.25: operations (same T several times), Saisie / PDF / Excel modes ---------- */
Object.assign(I18N.en,{colOp:"Operation",colTime:"Time",colLife:"Tool life",fOp:"Operation",fTime:"Time",fLife:"Tool life",
  nOps:n=>`${n} operation${n>1?"s":""}`,addOpT:"Add an operation for this tool (same T, tool data copied)",opGrp:(k,n)=>`${k} is used for ${n} operations: one line on the PDF`,
  opConf:(k,s)=>`${k}: not the same tool on every line (${s}). The PDF takes the first line.`,durBad:"Type a time like 12:30 (min:s) or 02:54:12 (h:min:s)",
  mSaisie:"Saisie",mSaisieT:"Everything you type, one line per operation",mPdfT:"How the PDF shows it",mXlT:"How the Excel shows it",
  mpGroup:"One line per tool: lines with the same T are combined (times and tool life added up)",mpOrder:"Order",mpOrderSaisie:"As typed",mpCols:"Columns",
  mpPdfN:(t,o)=>`${t} tool${t>1?"s":""} on the PDF`+(o>t?` (from ${o} operations)`:""),mpConf:"Same T, different tool:",
  mxRows:"Lines",mxOps:"Every operation, with the total at the end",mxPdf:"One line per tool (like the PDF)",mxOrder:"Order",mxOrderSaisie:"As typed",mxOrderPdf:"Like the PDF",
  mxN:n=>`${n} line${n>1?"s":""} in the Excel`,opsBtn:"+ Operation columns",opsBtnT:"Show Operation, Time and Tool life on this sheet, to type one line per operation",opsOff:"Hide operation columns",
  mTotal:"TOTAL",opsHint:"Add an operation: + on the tool's line. The same T on several lines is one tool on the PDF."});
Object.assign(I18N.fr,{colOp:"Opération",colTime:"Temps",colLife:"Vie outil",fOp:"Opération",fTime:"Temps",fLife:"Vie outil",
  nOps:n=>`${n} opération${n>1?"s":""}`,addOpT:"Ajouter une opération pour cet outil (même T, données de l’outil copiées)",opGrp:(k,n)=>`${k} sert à ${n} opérations : une seule ligne sur le PDF`,
  opConf:(k,s)=>`${k} : pas le même outil sur toutes les lignes (${s}). Le PDF prend la première ligne.`,durBad:"Tapez un temps comme 12:30 (min:s) ou 02:54:12 (h:min:s)",
  mSaisie:"Saisie",mSaisieT:"Tout ce que vous tapez, une ligne par opération",mPdfT:"Ce que montre le PDF",mXlT:"Ce que montre l’Excel",
  mpGroup:"Une ligne par outil : les lignes avec le même T sont regroupées (temps et vie outil additionnés)",mpOrder:"Ordre",mpOrderSaisie:"Ordre de saisie",mpCols:"Colonnes",
  mpPdfN:(t,o)=>`${t} outil${t>1?"s":""} sur le PDF`+(o>t?` (à partir de ${o} opérations)`:""),mpConf:"Même T, outil différent :",
  mxRows:"Lignes",mxOps:"Toutes les opérations, avec le total à la fin",mxPdf:"Une ligne par outil (comme le PDF)",mxOrder:"Ordre",mxOrderSaisie:"Ordre de saisie",mxOrderPdf:"Comme le PDF",
  mxN:n=>`${n} ligne${n>1?"s":""} dans l’Excel`,opsBtn:"+ Colonnes d’opération",opsBtnT:"Afficher Opération, Temps et Vie outil sur cette fiche, pour taper une ligne par opération",opsOff:"Masquer les colonnes d’opération",
  mTotal:"TOTAL",opsHint:"Ajouter une opération : + sur la ligne de l’outil. Le même T sur plusieurs lignes = un seul outil sur le PDF."});
try{Object.assign(SYN,{op:["operation","op","operation name","nom operation","usinage","phase usinage","toolpath","parcours"],
  time:["time","temps","duree","temps usinage","machining time","cycle time","temps operation","temps cycle","duration"],
  life:["tool life","vie outil","duree de vie","duree vie","life","usure","durabilite","durability","vie"]})}catch(e){}
const OPK=["op","time","life"],IDK=["type","diameter","ra","insert","ls","oal","z","holder","code","corrH","corrD"];
// times: 12:30 = 12 min 30 s, 02:54:12 = 2 h 54 min 12 s, a plain number = minutes
const durS=v=>{v=clean(v).replace(",",".");if(!v)return null;let m=v.match(/^(\d+):(\d{1,2}):(\d{1,2})$/);if(m)return +m[1]*3600+ +m[2]*60+ +m[3];
  m=v.match(/^(\d+):(\d{1,2})$/);if(m)return +m[1]*60+ +m[2];m=v.match(/^\d+(\.\d+)?$/);if(m)return Math.round(parseFloat(v)*60);return null};
const durF=s=>{if(s==null)return "";s=Math.round(s);const h=Math.floor(s/3600),m=Math.floor(s%3600/60),x=s%60,p=n=>String(n).padStart(2,"0");return h?`${p(h)}:${p(m)}:${p(x)}`:`${p(m)}:${p(x)}`};
const durSum=vals=>{let tot=0,any=0;vals.forEach(v=>linesOf_(v).forEach(l=>{const s=durS(l);if(s!=null){tot+=s;any=1}}));return any?durF(tot):""};
// lines with the same T are one tool
function opsGroups(tools){const G=[],by=new Map();realTools(tools).forEach(x=>{const k=clean(x.t)?normT(x.t):"";if(!k){G.push([x]);return}if(by.has(k))by.get(k).push(x);else{const g=[x];by.set(k,g);G.push(g)}});return G}
function opsMerge(tools){return opsGroups(tools).map(g=>{if(g.length===1)return g[0];const r={...g[0]};
  g.slice(1).forEach(x=>Object.keys(x).forEach(f=>{if(!clean(r[f])&&clean(x[f]))r[f]=x[f]}));
  r.time=durSum(g.map(x=>x.time));r.life=durSum(g.map(x=>x.life));r.op=[...new Set(g.map(x=>clean(x.op)).filter(Boolean))].join(" · ");return r})}
const cmpV=(f,v)=>{v=clean(v);if(!v)return "";if(f==="diameter")return normDia(v);if(f==="ra"){const r=normRA(v);return r.kind+r.val}return v.toUpperCase().replace(/\s+/g," ")};
function opsConflicts(tools){const out=[];opsGroups(tools).forEach(g=>{if(g.length<2)return;const k=normT(g[0].t);
  const diff=IDK.filter(f=>new Set(g.map(x=>cmpV(f,x[f])).filter(Boolean)).size>1);
  if(diff.length)out.push({t:k,fields:diff,txt:diff.map(f=>`${f==="corrH"?"H":f==="corrD"?"D":colLabel(f==="corrH"||f==="corrD"?"corr":f)} ${[...new Set(g.map(x=>clean(x[f])).filter(Boolean))].join(" / ")}`).join(" · ")})});return out}
// the PDF list and the Excel list
function sortList(L,k){const f=SORTK[k];if(!f)return L;
  const cmp=(a,b)=>{if(a.v==null&&b.v==null)return a.i-b.i;if(a.v==null)return 1;if(b.v==null)return -1;
    const c=typeof a.v==="number"&&typeof b.v==="number"?a.v-b.v:String(a.v).localeCompare(String(b.v),undefined,{numeric:true});return c||(tNum(a.x.t)??1e9)-(tNum(b.x.t)??1e9)||a.i-b.i};
  return L.map((x,i)=>({x,i,v:f(x)})).sort(cmp).map(o=>o.x)}
function pdfRowsOf(art){let L=realTools(art.tools);if(art.pdfGroup!==false)L=opsMerge(L);return sortList(L,art.pdfSort)}
function xlRowsOf(art){if(art.xlRows==="pdf")return pdfRowsOf(art);let L=realTools(art.tools);if(art.xlSort==="pdf")L=sortList(L,art.pdfSort);
  const T=durSum(L.map(x=>x.time)),F=durSum(L.map(x=>x.life));return L.length&&(T||F)?[...L,{t:t("mTotal"),time:T,life:F,_total:1}]:L}
// the Excel can have its own columns (by default the PDF's; Operation is in it when every operation is listed)
function prOnX(art,k,cfg){const P=(art&&art.prx)||{};if(Object.prototype.hasOwnProperty.call(P,k))return !!P[k];if(k==="op")return (art&&art.xlRows)!=="pdf";return prOn(art,k,cfg)}
function printCfgX(cfg,art){if(!cfg)return cfg;const keys=[...LABK.filter(k=>k!=="t"),...(cfg.extra||[]).map(x=>xKey(x.id))].filter(k=>!prOnX(art,k,cfg));
  if(!keys.length)return cfg;const hidden=[...new Set([...(cfg.hidden||[]),...keys])],joinTo={};
  Object.entries(cfg.joinTo||{}).forEach(([k,to])=>{if(!hidden.includes(k)&&!hidden.includes(to))joinTo[k]=to});return{...cfg,hidden,joinTo,join:Object.keys(joinTo)}}
// operation columns: hidden in layouts unless shown, or switched on for one sheet
const opsCfg=(cfg,art)=>art&&art.ops&&cfg?{...cfg,hidden:cfg.hidden.filter(k=>!OPK.includes(k))}:cfg;
{const c0=cfgOf;cfgOf=function(art){return opsCfg(c0(art),art)};const c1=cfgXlOf;cfgXlOf=function(art){return opsCfg(c1(art),art)}}
const opsVis=()=>!!cur&&edCols(sheetCfg()).some(k=>OPK.includes(k));
function toolCountTxt(){const real=realTools(cur.tools),n=opsGroups(cur.tools).length;return t("nTools",n)+(real.length>n?" · "+t("nOps",real.length):"")}
// same T on several lines: a dot on the T (blue), red when the tool data differ; later lines dimmed
function tDupMark(){if(!cur)return;const G=new Map();cur.tools.forEach((x,i)=>{const k=normT(x.t);if(clean(x.t)&&realTools([x]).length){if(!G.has(k))G.set(k,[]);G.get(k).push(i)}});
  const CF=new Map(opsConflicts(cur.tools).map(c=>[c.t,c]));
  document.querySelectorAll("#rows tr[data-i]").forEach(tr=>{const i=+tr.dataset.i,x=cur.tools[i],el=tr.querySelector('input[data-k="t"]');if(!x||!el)return;
    const k=normT(x.t),g=G.get(k)||[],n=g.length,cf=CF.get(k);el.classList.remove("warn");el.classList.toggle("opg",n>1&&!cf);el.classList.toggle("opbad",n>1&&!!cf);
    tr.classList.toggle("oprow",n>1&&g[0]!==i);el.title=n>1?(cf?t("opConf",k,cf.txt):t("opGrp",k,n)):""})}
// times typed: 12:3 -> 12:03, 90 -> 01:30:00 (minutes), wrong ones marked
document.addEventListener("change",e=>{const i=e.target;if(!i||!i.matches||!i.matches('#rows input[data-k="time"],#rows input[data-k="life"]'))return;const v=clean(i.value);
  if(!v){i.classList.remove("bad");return}const s=durS(v);i.classList.toggle("bad",s==null);i.title=s==null?t("durBad"):"";if(s!=null&&durF(s)!==v){i.value=durF(s);i.dispatchEvent(new Event("input",{bubbles:true}))}},true);
// modes
let edMode=lsGet("bs.edmode");if(!["saisie","pdf","excel"].includes(edMode))edMode="saisie";
const modeTabs=()=>`<span class="modetabs" role="tablist">${[["saisie",t("mSaisie"),t("mSaisieT")],["pdf","PDF",t("mPdfT")],["excel","Excel",t("mXlT")]].map(([m,l,tt])=>`<button type="button" role="tab" data-edm="${m}" title="${esc(tt)}" aria-selected="${edMode===m}">${esc(l)}</button>`).join("")}</span>`;
function setEdMode(m){edMode=m;lsSet("bs.edmode",m);const ed=$("#ed");if(ed)ed.dataset.mode=m;document.querySelectorAll("[data-edm]").forEach(b=>b.setAttribute("aria-selected",b.dataset.edm===m));
  if(m!=="saisie"){const pv=m==="excel"?"xlsx":"pdf";if(pvMode!==pv){const b=document.querySelector(`[data-pvm="${pv}"]`);if(b)b.click()}}
  drawModePanel();if(m==="saisie")requestAnimationFrame(()=>{try{ttFit()}catch(_){}})}
document.addEventListener("click",e=>{const b=e.target.closest&&e.target.closest("[data-edm]");if(b){e.preventDefault();setEdMode(b.dataset.edm)}});
function mpVal(x,k,cfg){if(k==="corr"){const h=corrV(x.corrH),d=corrV(x.corrD);return h||d?`H${h||"—"} D${d||"—"}`:""}if(k==="diameter"){const d=normDia(x.diameter);return d?"Ø"+d:""}
  if(k==="ra")return raLabel(x.ra);return linesOf_(x[k]).join(" · ")}
function drawModePanel(){const P=$("#modepanel");if(!P||!cur)return;P.hidden=edMode==="saisie";if(edMode==="saisie"){P.innerHTML="";return}
  const art=cur,pdf=edMode==="pdf",cfg=pdf?sheetCfg(art):cfgXlOf(art),keys=visCols(cfg).filter(k=>k!=="t"),on=k=>pdf?prOn(art,k):prOnX(art,k);
  const rows=withLoc(pdf?pdfRowsOf(art):xlRowsOf(art),cfg),shown=keys.filter(on),nOps=realTools(art.tools).length,nT=opsGroups(art.tools).length,CF=opsConflicts(art.tools);
  const sortSel=(id,val,first)=>`<select id="${id}">${first}${Object.entries(t("sortBy")).map(([k,l])=>`<option value="${k}" ${val===k?"selected":""}>${esc(l)}</option>`).join("")}</select>`;
  const set=pdf?`<div class="mpset"><label class="chk"><input type="checkbox" id="mp-group" ${art.pdfGroup!==false?"checked":""}> ${esc(t("mpGroup"))}</label>
      <label class="laysel"><span>${esc(t("mpOrder"))}</span>${sortSel("mp-sort",art.pdfSort||"",`<option value="">${esc(t("mpOrderSaisie"))}</option>`)}</label></div>`
    :`<div class="mpset"><div class="seg2" role="radiogroup" aria-label="${esc(t("mxRows"))}"><label class="chk"><input type="radio" name="mx-rows" value="ops" ${art.xlRows!=="pdf"?"checked":""}> ${esc(t("mxOps"))}</label><label class="chk"><input type="radio" name="mx-rows" value="pdf" ${art.xlRows==="pdf"?"checked":""}> ${esc(t("mxPdf"))}</label></div>
      ${art.xlRows!=="pdf"?`<label class="laysel"><span>${esc(t("mxOrder"))}</span><select id="mx-sort"><option value="">${esc(t("mxOrderSaisie"))}</option><option value="pdf" ${art.xlSort==="pdf"?"selected":""}>${esc(t("mxOrderPdf"))}</option></select></label>`:""}</div>`;
  P.innerHTML=`${set}
    <div class="mpcols"><span class="mplab">${esc(t("mpCols"))}</span>${keys.map(k=>`<label class="mpchip${on(k)?" on":""}"><input type="checkbox" data-mpk="${k}" ${on(k)?"checked":""}>${esc(colLabel(k,cfg))}</label>`).join("")}</div>
    ${CF.length?`<div class="warnline mpconf"><b>${esc(t("mpConf"))}</b> ${CF.map(c=>`<span>${esc(c.t)} — ${esc(c.txt)}</span>`).join("")}</div>`:""}
    <p class="note mpn">${esc(pdf?t("mpPdfN",art.pdfGroup!==false?nT:nOps,nOps):t("mxN",rows.filter(r=>!r._total).length))}</p>
    <div class="list mplist"><table class="lt mpt"><thead><tr><th>T</th>${shown.map(k=>`<th>${esc(colLabel(k,cfg))}</th>`).join("")}</tr></thead><tbody>
      ${rows.map(x=>`<tr class="${x._total?"tot":""}"><td class="m b">${esc(x._total?x.t:normT(x.t))}</td>${shown.map(k=>`<td class="${/^(time|life|ls|oal|z|diameter|ra|code|asm|corr)$/.test(k)?"m":""}${(k==="time"||k==="life")&&x._total?" b":""}">${esc(mpVal(x,k,cfg))}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`;
  const ch=()=>{edited();pvLastKey="";schedulePreview(30);drawModePanel()};
  if(pdf){$("#mp-group").onchange=e=>{art.pdfGroup=e.target.checked;ch()};$("#mp-sort").onchange=e=>{art.pdfSort=e.target.value||"";ch()}}
  else{P.querySelectorAll('[name="mx-rows"]').forEach(r=>r.onchange=()=>{art.xlRows=r.value==="pdf"?"pdf":"ops";ch()});const xs=$("#mx-sort");if(xs)xs.onchange=e=>{art.xlSort=e.target.value||"";ch()}}
  if(art.status==="done")P.querySelectorAll("input,select").forEach(i=>i.disabled=true);
  P.querySelectorAll("[data-mpk]").forEach(c=>c.onchange=()=>{const k=c.dataset.mpk;if(pdf){art.pr=art.pr||{};art.pr[k]=c.checked;try{prStyle()}catch(_){}document.querySelectorAll(`.tt [data-pr="${k}"]`).forEach(b=>b.checked=c.checked)}else{art.prx=art.prx||{};art.prx[k]=c.checked}ch()})}
{const r0=renderEditor;renderEditor=function(art){r0.apply(this,arguments);const ed=$("#ed");if(ed)ed.dataset.mode=edMode;drawModePanel();
  if(cur&&cur.status==="done")setTimeout(()=>{const P=$("#modepanel");if(P)P.querySelectorAll("input,select").forEach(i=>i.disabled=true)},0)}}
// "+ operation columns" on one sheet
document.addEventListener("click",e=>{const b=e.target.closest&&e.target.closest("#b-ops");if(!b||!cur)return;cur.ops=!cur.ops;edited();try{refreshCols(cur)}catch(_){}renderEditor(cur)});

'''
CSS=r'''
/* 2.25 operations */
.modetabs{display:inline-flex;gap:2px;margin-left:12px;padding:3px;border-radius:10px;background:var(--fill);border:1px solid var(--hair);vertical-align:middle}
.modetabs button{border:0;background:transparent;padding:5px 12px;border-radius:7px;font:600 13px/1 var(--body);letter-spacing:0;text-transform:none;color:var(--mid);cursor:pointer}
.modetabs button[aria-selected="true"]{background:var(--paper);color:var(--ink);box-shadow:0 1px 2px rgba(0,0,0,.12)}
.ed[data-mode="pdf"] .card .tw,.ed[data-mode="excel"] .card .tw,.ed[data-mode="pdf"] .tdiag.wide,.ed[data-mode="excel"] .tdiag.wide,
.ed[data-mode="pdf"] .rowbar .rbg:first-child,.ed[data-mode="excel"] .rowbar .rbg:first-child,.ed[data-mode="pdf"] .rowbar>.note,.ed[data-mode="excel"] .rowbar>.note,.ed[data-mode="pdf"] .opshint,.ed[data-mode="excel"] .opshint{display:none!important}
.ed[data-mode="pdf"] .tdtog,.ed[data-mode="excel"] .tdtog{display:none}
.sortsel{display:none!important}
#modepanel{display:flex;flex-direction:column;gap:12px;margin-bottom:12px}#modepanel[hidden]{display:none}
.mpset{display:flex;flex-wrap:wrap;gap:10px 20px;align-items:center}.mpset .chk{font-size:14px}.seg2{display:flex;flex-direction:column;gap:6px}
.mpcols{display:flex;flex-wrap:wrap;gap:6px;align-items:center}.mplab{font:600 11px/1 var(--body);text-transform:uppercase;letter-spacing:.06em;color:var(--mid);margin-right:4px}
.mpchip{display:inline-flex;align-items:center;gap:6px;padding:5px 10px 5px 8px;border:1px solid var(--hair);border-radius:999px;font-size:13px;cursor:pointer;color:var(--mid);background:var(--paper)}
.mpchip.on{border-color:var(--ink);color:var(--ink)}.mpchip input{accent-color:var(--ink);margin:0}
.mpconf{display:flex;flex-wrap:wrap;gap:4px 14px}.mpn{margin:0}
.mplist{max-height:min(560px,62vh);overflow:auto}.mpt td,.mpt th{white-space:nowrap}.mpt tr.tot td{border-top:2px solid var(--ink);font-weight:700}
.tt input[data-k="t"].opg{background-image:radial-gradient(circle at calc(100% - 7px) 50%,#2563eb 3px,transparent 3.6px)!important}
.tt input[data-k="t"].opbad{background-image:radial-gradient(circle at calc(100% - 7px) 50%,var(--red) 3.4px,transparent 4px)!important}
.tt tr.oprow td:not([data-col="t"]):not([data-col="op"]):not([data-col="time"]):not([data-col="life"]):not(.act):not([data-col^="x_"]) input{opacity:.42}
.tt td.durcell input{font-family:var(--mono)}.tt input.bad{outline:2px solid var(--red);outline-offset:-2px}
.tt .act .ib.op{font-weight:700;color:#2563eb}
.opshint{margin-left:auto}
'''
R=[
('''const off=visCols(sheetCfg()).filter(k=>k!=="t"&&!prOn(cur,k));''','''const off=visCols(sheetCfg()).filter(k=>k!=="t"&&k!=="op"&&!prOn(cur,k));'''),
('''const BASEK=["t","asm","corrH","corrD","type","diameter","ra","insert","ls","oal","z","holder","code"];''','''const BASEK=["t","asm","corrH","corrD","op","type","diameter","ra","insert","ls","oal","z","holder","code","time","life"];'''),
('''const LABK=["t","asm","corr","type","diameter","ra","insert","ls","oal","z","holder","code","loc"];''','''const LABK=["t","asm","corr","op","type","diameter","ra","insert","ls","oal","z","holder","code","loc","time","life"];'''),
('''const JOINORD=["t","asm","corr","type","diameter","ra","insert","ls","oal","z","holder","code","loc"];''','''const JOINORD=["t","asm","corr","op","type","diameter","ra","insert","ls","oal","z","holder","code","loc","time","life"];'''),
('''const STDHIDE=["oal","z"]''','''const STDHIDE=["oal","z","op","time","life"]'''),
('''hidden:c?((c.hidden)||[]).filter(k=>k!=="t"&&LABK.includes(k)):[...STDHIDE]''','''hidden:c?[...new Set([...((c.hidden)||[]).filter(k=>k!=="t"&&LABK.includes(k)),...(c.opsV?[]:["op","time","life"])])]:[...STDHIDE],opsV:1'''),
('''noprint:[...new Set(buf.noprint||[])].filter(k=>k!=="t")});''','''noprint:[...new Set(buf.noprint||[])].filter(k=>k!=="t"),opsV:1});'''),
('''noprint:c.noprint,asmOwn:c.asmOwn,locOwn:c.locOwn}''','''noprint:c.noprint,asmOwn:c.asmOwn,locOwn:c.locOwn,opsV:1}''',2),
('''else if(k==="loc"&&out.includes("code"))out.splice(out.indexOf("code")+1,0,k);''','''else if(k==="loc"&&out.includes("code"))out.splice(out.indexOf("code")+1,0,k);else if(k==="op"&&out.includes("corr"))out.splice(out.indexOf("corr")+1,0,k);'''),
('''holder:t("colHolder"),code:t("colCode"),loc:t("colLoc")}''','''holder:t("colHolder"),code:t("colCode"),loc:t("colLoc"),op:t("colOp"),time:t("colTime"),life:t("colLife")}'''),
('''const DEFW={loc:110,''','''const DEFW={op:150,time:84,life:84,loc:110,'''),
('''const MIN={type:140,holder:100,insert:76,loc:72}''','''const MIN={type:140,holder:100,insert:76,loc:72,op:90}'''),
('''["holder","fHolder"],["code","fCode"]];''','''["holder","fHolder"],["code","fCode"],["op","fOp"],["time","fTime"],["life","fLife"]];'''),
('''const prDef=(cfg,k)=>!((cfg&&cfg.noprint)||["asm"]).includes(k);''','''const prDef=(cfg,k)=>k==="op"?false:!((cfg&&cfg.noprint)||["asm"]).includes(k);'''),
# PDF / Excel lists
('''tools:withLoc(art.tools,cfg),cols:printCfg(cfg,art)''','''tools:withLoc(pdfRowsOf(art),cfg),cols:printCfg(cfg,art)'''),
('''function xlData(art){const d=sheetData(art),X=printCfg(cfgXlOf(art),art);''','''function xlData(art){const d=sheetData(art),X=printCfgX(cfgXlOf(art),art);d.tools=withLoc(xlRowsOf(art),cfgXlOf(art));'''),
(''',tools=realTools(withLoc(art.tools,cfgXlOf(art))),done=art.status==="done"''',''',tools=realTools(withLoc(xlRowsOf(art),cfgXlOf(art))),done=art.status==="done"'''),
('''["corrD",EN?"D offset":"Corr. D"],''','''["corrD",EN?"D offset":"Corr. D"],["op",lb("op",EN?"Operation":"Opération")],'''),
('''["code",lb("code",EN?"Tool code":"Code outil")],''','''["code",lb("code",EN?"Tool code":"Code outil")],["time",lb("time",EN?"Time":"Temps")],["life",lb("life",EN?"Tool life":"Vie outil")],'''),
# PDF drawing
('''ORD=["t","asm","corr","type","diameter","ra","insert","ls","oal","z","holder","code","loc",''','''ORD=["t","asm","corr","op","type","diameter","ra","insert","ls","oal","z","holder","code","loc","time","life",'''),
('''.concat([["loc",24]]).filter(''','''.concat([["loc",24],["op",26],["time",14],["life",14]]).filter('''),
('''["holder",42],["code",21],["loc",24],["chk",10],''','''["holder",42],["code",21],["loc",24],["op",26],["time",14],["life",14],["chk",10],'''),
('''loc:lab("loc",LANG==="fr"?"Emplacement":"Location"),chk:''','''loc:lab("loc",LANG==="fr"?"Emplacement":"Location"),op:lab("op",LANG==="fr"?"Opération":"Operation"),time:lab("time",LANG==="fr"?"Temps":"Time"),life:lab("life",LANG==="fr"?"Vie outil":"Tool life"),chk:'''),
('''// your own columns
    EXTRA.forEach''','''OPK.forEach(k=>{if(KI[k]==null)return;at(k);useK(k);const v=linesOf(t[k]);if(v.length)stack(v,X_(k)+1.6,W_(k)-2.8,k==="op"?"Plex5":"Mono5",k==="op"?8.4:9.4,4.8,"left");else if(k!=="op")dash(X_(k)+1.8);under(k)});
    // your own columns
    EXTRA.forEach'''),
('''else if(k.startsWith("x_")||k==="loc"){const x=EXTRA.find(e=>"x_"+e.id===k),hd=k==="loc"?lab("loc",LANG==="fr"?"Emplacement":"Location"):(x?x.label:"")''','''else if(k.startsWith("x_")||k==="loc"||OPK.includes(k)){const x=EXTRA.find(e=>"x_"+e.id===k),hd=k==="loc"?lab("loc",LANG==="fr"?"Emplacement":"Location"):OPK.includes(k)?lab(k,{op:LANG==="fr"?"Opération":"Operation",time:LANG==="fr"?"Temps":"Time",life:LANG==="fr"?"Vie outil":"Tool life"}[k]):(x?x.label:"")'''),
# editor
('''function countTools(){$("#count").textContent=t("nTools",realTools(cur.tools).length);''','''function countTools(){$("#count").textContent=toolCountTxt();'''),
('''$("#count").textContent=t("nTools",realTools(cur.tools).length);drawStatus()})}''','''$("#count").textContent=toolCountTxt();drawStatus();tDupMark()})}'''),
('''k.startsWith("x_")?"xcell":k==="holder"?"holdcell":k==="code"?"codecell":""''','''k.startsWith("x_")?"xcell":k==="holder"?"holdcell":k==="code"?"codecell":k==="time"||k==="life"?"durcell":""'''),
('''<td class="act"><button class="ib" data-r="up"''','''<td class="act">${opsVis()?`<button class="ib op" data-r="addop" title="${esc(t("addOpT"))}" tabindex="-1">+</button>`:""}<button class="ib" data-r="up"'''),
('''if(b.dataset.r==="del"){T.splice(i,1);if(!T.length)T.push({t:"T01"})}''','''if(b.dataset.r==="del"){T.splice(i,1);if(!T.length)T.push({t:"T01"})}
    if(b.dataset.r==="addop"){const s=T[i],n={};["t","asm","corrH","corrD",...IDK].forEach(k=>{if(clean(s[k]))n[k]=s[k]});const j=i+1;T.splice(j,0,n);
      setTimeout(()=>{const r=document.querySelector(`#rows tr[data-i="${j}"]`),el=r&&(r.querySelector('input[data-k="op"]')||r.querySelector('input[data-k="time"]'));if(el)el.focus()},40)}'''),
('''<h2>${esc(t("tools"))} <span class="hint" id="count"></span>${tdBtn()}</h2>''','''<h2>${esc(t("tools"))}${modeTabs()} <span class="hint" id="count"></span>${tdBtn()}</h2><div id="modepanel" hidden></div>'''),
('''<label class="laysel sortsel" title="${esc(t("sortT"))}">''','''<button class="btn ghost" id="b-ops" title="${esc(t("opsBtnT"))}">${esc(art.ops?t("opsOff"):t("opsBtn"))}</button><label class="laysel sortsel" title="${esc(t("sortT"))}">'''),
# the read-only view and the tool prep show one line per tool
('''const rows=realTools(art.tools),AC=sheetCfg(art);''','''const rows=pdfRowsOf(art),AC=sheetCfg(art);'''),
('''const rows=prepSort(realTools(art.tools).filter(x=>clean(x.code)),art);''','''const rows=prepSort(opsMerge(realTools(art.tools)).filter(x=>clean(x.code)),art);'''),
('''const rows=prepSort(realTools(art.tools).filter(x=>clean(x.code)),art),A0''','''const rows=prepSort(opsMerge(realTools(art.tools)).filter(x=>clean(x.code)),art),A0'''),
('''/* ---------- which columns go on the PDF and the Excel ----------''',BLOCK+'''/* ---------- which columns go on the PDF and the Excel ----------'''),
('''.tt .colrs{right:0;width:8px}.tt .colrs::after{left:6px}''','''.tt .colrs{right:0;width:8px}.tt .colrs::after{left:6px}'''+CSS),
]
for f in sys.argv[1:]:
  s=open(f).read()
  for r in R:
    a,b=r[0],r[1];n=r[2] if len(r)>2 else 1
    assert s.count(a)==n,(f,s.count(a),a[:90]);s=s.replace(a,b)
  open(f,'w').write(s);print("patched",f)
