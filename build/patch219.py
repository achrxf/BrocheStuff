import sys
ASM_JS=r'''
/* ---------- assemblies: a tool with its holder, saved under a code (AS0001…) ----------
   They are made by themselves from the tool sheets (a row with a holder and a tool code, or a type and a Ø).
   Typing an assembly code in the Code box of a sheet fills the whole row. */
Object.assign(I18N.en,{navAsm:"Assemblies", asmT:"Assemblies", asmSub:"Each tool with its holder, saved under a code. Type the code in the Code box of a tool sheet and the whole row fills in.",
  asmQ:"Assembly code, type, Ø, holder, tool code…", asmNew:"+ New assembly", asmNone:"No assembly yet.", asmNoneP:"They are made by themselves from the tool sheets: a row with a holder and a tool code (or a type and a Ø) becomes an assembly.",
  asmFAll:"All", asmFUsed:"In a sheet", asmFFree:"In no sheet", asmFKept:"Kept",
  asmTh:["Assembly","Tool","LS / LT","Holder","Tool code","Used in",""], asmUsedN:n=>`${n} ${pl(n,"sheet","sheets")}`, asmNoUse:"No sheet", asmAuto:"From a sheet", asmManual:"Made by hand",
  asmFilled:c=>`Row filled from assembly ${c}`, asmUnknown:c=>`No assembly ${c}`, asmChipT:"Assembly code: type it in the Code box of another sheet to get this same row",
  asmEditT:c=>`Assembly ${c}`, asmNewT:"New assembly", asmName:"Name (optional)", asmKeep:"Keep it even when no sheet uses it", asmSave:"Save", asmDel:"Delete", asmDelQ:c=>`Delete assembly ${c}? The sheets keep their rows.`, asmDelOk:c=>`${c} deleted`,
  asmNeed:"Give the holder, and a tool code or a type with a Ø.", asmSame:c=>`The same assembly already exists: ${c}.`, asmSaved:c=>`${c} saved`, asmCopied:c=>`${c} copied`, asmCopyT:"Copy the code", asmMade:n=>`${n} new ${pl(n,"assembly","assemblies")}`,
  sortL:"Sort", sortT:"Put the rows in another order (the PDF follows)", sortBy:{t:"Tool number (T1, T2…)",corr:"Corrector number",type:"Type (A → Z)",dia:"Ø small → large",diaD:"Ø large → small",holder:"Holder",code:"Tool code",ls:"LS short → long"}, sorted:s=>`Sorted: ${s}`, unsort:"Undo"});
Object.assign(I18N.fr,{navAsm:"Assemblages", asmT:"Assemblages", asmSub:"Chaque outil avec son porte-outil, gardé sous un code. Tapez le code dans la case Code d’une fiche outils et toute la ligne se remplit.",
  asmQ:"Code d’assemblage, type, Ø, porte-outil, code outil…", asmNew:"+ Nouvel assemblage", asmNone:"Pas encore d’assemblage.", asmNoneP:"Ils se créent tout seuls à partir des fiches outils : une ligne avec un porte-outil et un code outil (ou un type et un Ø) devient un assemblage.",
  asmFAll:"Tous", asmFUsed:"Dans une fiche", asmFFree:"Dans aucune fiche", asmFKept:"Gardés",
  asmTh:["Assemblage","Outil","LS / LT","Porte-outil","Code outil","Utilisé dans",""], asmUsedN:n=>`${n} ${pl(n,"fiche","fiches")}`, asmNoUse:"Aucune fiche", asmAuto:"Venu d’une fiche", asmManual:"Fait à la main",
  asmFilled:c=>`Ligne remplie depuis l’assemblage ${c}`, asmUnknown:c=>`Pas d’assemblage ${c}`, asmChipT:"Code d’assemblage : tapez-le dans la case Code d’une autre fiche pour avoir cette même ligne",
  asmEditT:c=>`Assemblage ${c}`, asmNewT:"Nouvel assemblage", asmName:"Nom (facultatif)", asmKeep:"Le garder même si aucune fiche ne l’utilise", asmSave:"Enregistrer", asmDel:"Supprimer", asmDelQ:c=>`Supprimer l’assemblage ${c} ? Les fiches gardent leurs lignes.`, asmDelOk:c=>`${c} supprimé`,
  asmNeed:"Indiquez le porte-outil, et un code outil ou un type avec un Ø.", asmSame:c=>`Le même assemblage existe déjà : ${c}.`, asmSaved:c=>`${c} enregistré`, asmCopied:c=>`${c} copié`, asmCopyT:"Copier le code", asmMade:n=>`${n} ${pl(n,"nouvel assemblage","nouveaux assemblages")}`,
  sortL:"Trier", sortT:"Mettre les lignes dans un autre ordre (le PDF suit)", sortBy:{t:"Numéro d’outil (T1, T2…)",corr:"Numéro de correcteur",type:"Type (A → Z)",dia:"Ø du petit au grand",diaD:"Ø du grand au petit",holder:"Porte-outil",code:"Code outil",ls:"LS du court au long"}, sorted:s=>`Trié : ${s}`, unsort:"Annuler"});
const ASMF=["type","diameter","ra","insert","ls","oal","z","holder","code"];
const asmList=()=>Array.isArray(db.assemblies)?db.assemblies:(db.assemblies=[]);
const asmNv=v=>clean(v).toUpperCase().replace(/\s+/g," ");
const asmSig=x=>ASMF.map(k=>k==="diameter"?normDia(x[k]):k==="code"?normCode(x[k]):asmNv(x[k])).join("|");
const asmReady=x=>!!clean(x.holder)&&(!!clean(x.code)||(!!clean(x.type)&&!!clean(x.diameter)));
const asmKey=v=>{const m=/^\s*AS[\s-]*0*(\d{1,6})\s*$/i.exec(String(v||""));return m?"AS"+m[1].padStart(4,"0"):null};
const asmFind=v=>{const k=asmKey(v);return k?asmList().find(a=>a.code===k)||null:null};
const asmOfTool=x=>{if(!asmReady(x))return null;const s=asmSig(x);return asmList().find(a=>a.sig===s)||null};
function asmNext(){let n=0;asmList().forEach(a=>{const m=/^AS(\d+)$/.exec(a.code||"");if(m)n=Math.max(n,+m[1])});return "AS"+String(n+1).padStart(4,"0")}
function asmApply(x,a){ASMF.forEach(k=>{x[k]=a.tool[k]||""});a.usedAt=Date.now()}
function asmUses(){const U=new Map();db.articles.forEach(a=>realTools(a.tools).forEach(x=>{if(!asmReady(x))return;const s=asmSig(x);if(!U.has(s))U.set(s,[]);U.get(s).push(a)}));return U}
// a sheet's finished rows become assemblies; the ones made while a row was still being typed (no sheet uses them) go away
let asmTimer=null,asmDirty=false;
function asmSync(art){asmDirty=false;if(!art||!Array.isArray(art.tools))return 0;const L=asmList();let ch=0;
  // first drop this sheet's recent ones that no sheet uses any more, so their number is free again
  const U=asmUses();for(let i=L.length-1;i>=0;i--){const a=L[i];if(a.auto&&!a.keep&&a.src===art.id&&!U.has(a.sig)&&Date.now()-(a.createdAt||0)<36e5){L.splice(i,1);ch++}}
  const have=new Set(L.map(a=>a.sig));
  realTools(art.tools).forEach(x=>{if(!asmReady(x))return;const s=asmSig(x);if(have.has(s))return;
    const tool={};ASMF.forEach(k=>{if(clean(x[k]))tool[k]=String(x[k]).trim()});
    L.push({id:uid(),code:asmNext(),tool,sig:s,auto:1,src:art.id,createdAt:Date.now()});have.add(s);ch++});
  return ch}
function asmLater(){asmDirty=true;clearTimeout(asmTimer);asmTimer=setTimeout(()=>{if(cur&&asmDirty&&asmSync(cur)){saveDB();asmChips()}},2500)}
// first start with this version: the existing sheets fill the library
function asmBoot(){if(asmDirty&&cur){clearTimeout(asmTimer);if(asmSync(cur))saveDB()}
  if(db.asmSeeded||!Array.isArray(db.articles))return;let n=0;const L=asmList(),have=new Set(L.map(x=>x.sig));let nx=+asmNext().slice(2);
  [...db.articles].sort((a,b)=>(a.createdAt||0)-(b.createdAt||0)).forEach(a=>{
    realTools(a.tools).forEach(x=>{if(!asmReady(x))return;const s=asmSig(x);if(have.has(s))return;const tool={};ASMF.forEach(k=>{if(clean(x[k]))tool[k]=String(x[k]).trim()});
      L.push({id:uid(),code:"AS"+String(nx++).padStart(4,"0"),tool,sig:s,auto:1,src:a.id,createdAt:a.createdAt||Date.now()});have.add(s);n++})});
  db.asmSeeded=1;if(n||db.articles.length)saveDB()}
// two PCs that made the same code at the same time: the later one takes the next free code
function asmFix(){const L=asmList(),seen=new Set();[...L].sort((a,b)=>(a.createdAt||0)-(b.createdAt||0)).forEach(a=>{if(!a.sig)a.sig=asmSig(a.tool||{});if(!a.code||seen.has(a.code))a.code=asmNext();seen.add(a.code)})}
// the small assembly code under the T number of each row
function asmChipHTML(x){const a=asmOfTool(x);return `<button class="asmc" data-asm="${a?esc(a.code):""}" title="${esc(t("asmChipT"))}" tabindex="-1"${a?"":" hidden"}>${a?esc(a.code):""}</button>`}
function asmChips(){const R=$("#rows");if(!R||!cur)return;R.querySelectorAll("tr[data-i]").forEach(tr=>{const x=cur.tools[+tr.dataset.i],b=tr.querySelector(".asmc");if(!x||!b)return;const a=asmOfTool(x);b.hidden=!a;b.dataset.asm=a?a.code:"";b.textContent=a?a.code:""})}
function asmCodeOptions(){return asmList().map(a=>`<option value="${esc(a.code)}">${esc([a.tool.type,a.tool.diameter?"Ø"+normDia(a.tool.diameter):"",linesOf_(a.tool.holder)[0]].filter(Boolean).join(" · "))}</option>`).join("")}
const linesOf_=v=>String(v||"").split("\n").map(s=>s.trim()).filter(Boolean);
function asmCopy(code){try{navigator.clipboard.writeText(code)}catch(e){}toast(t("asmCopied",code))}

/* sorting the rows of a sheet */
const numOf=v=>{const m=/-?\d+(?:[.,]\d+)?/.exec(String(v||""));return m?parseFloat(m[0].replace(",",".")):null};
const SORTK={t:x=>tNum(x.t),corr:x=>numOf(x.corrH),type:x=>clean(x.type).toUpperCase()||null,dia:x=>numOf(normDia(x.diameter)),diaD:x=>{const v=numOf(normDia(x.diameter));return v==null?null:-v},
  holder:x=>clean(x.holder).toUpperCase()||null,code:x=>normCode(x.code)||null,ls:x=>numOf(x.ls)};
function sortRows(k){const f=SORTK[k];if(!f||!cur)return;flushEditor();const before=cur.tools.slice();
  const real=cur.tools.filter(x=>realTools([x]).length),empty=cur.tools.filter(x=>!realTools([x]).length);
  const cmp=(a,b)=>{if(a.v==null&&b.v==null)return a.i-b.i;if(a.v==null)return 1;if(b.v==null)return -1;
    const c=typeof a.v==="number"&&typeof b.v==="number"?a.v-b.v:String(a.v).localeCompare(String(b.v),undefined,{numeric:true});return c||(tNum(a.x.t)??1e9)-(tNum(b.x.t)??1e9)||a.i-b.i};
  cur.tools=[...real.map((x,i)=>({x,i,v:f(x)})).sort(cmp).map(o=>o.x),...empty];
  if(cur.tools.every((x,i)=>x===before[i])){toast(t("sorted",t("sortBy")[k]));return}
  renderRows();edited();const art=cur;
  toast(t("sorted",t("sortBy")[k]),{label:t("unsort"),fn:()=>{if(cur!==art)return;cur.tools=before;renderRows();edited()}})}

/* the page */
let asmQ="",asmF="all";
function renderAsm(){const ed=can("article");
  $("#view").innerHTML=`<div class="page asmp"><div class="ph"><div><h2>${esc(t("asmT"))}<b>.</b></h2><div class="sub">${esc(t("asmSub"))}</div></div><span class="sp"></span>${ed?`<button class="btn red" id="asm-new">${esc(t("asmNew"))}</button>`:""}</div>
    <div class="resbar"><div class="search">${searchIcon}<input id="asm-q" type="search" placeholder="${esc(t("asmQ"))}" value="${esc(asmQ)}" autocomplete="off"></div><div class="chips">
      ${[["all",t("asmFAll")],["used",t("asmFUsed")],["free",t("asmFFree")],["kept",t("asmFKept")]].map(([k,l])=>`<button class="chip" data-asf="${k}" aria-pressed="${asmF===k}">${esc(l)}<b id="asfn-${k}"></b></button>`).join("")}</div></div>
    <div id="asmres"></div></div>`;
  $("#asm-new")&&($("#asm-new").onclick=()=>asmDialog(null));
  const q=$("#asm-q");let qt;q.oninput=()=>{asmQ=q.value;clearTimeout(qt);qt=setTimeout(drawAsm,120)};
  $("#view").querySelectorAll("[data-asf]").forEach(b=>b.onclick=()=>{asmF=b.dataset.asf;$("#view").querySelectorAll("[data-asf]").forEach(x=>x.setAttribute("aria-pressed",x===b));drawAsm()});
  drawAsm()}
function drawAsm(){const box=$("#asmres");if(!box)return;const U=asmUses(),L=asmList().slice().sort((a,b)=>String(a.code).localeCompare(String(b.code),undefined,{numeric:true}));
  const used=a=>U.has(a.sig),cnt={all:L.length,used:L.filter(used).length,free:L.filter(a=>!used(a)).length,kept:L.filter(a=>a.keep).length};
  Object.entries(cnt).forEach(([k,n])=>{const e=$("#asfn-"+k);if(e)e.textContent=n});
  const terms=asmQ.toLowerCase().split(/\s+/).filter(Boolean),ed=can("article");
  const R=L.filter(a=>(asmF==="all"||(asmF==="used"?used(a):asmF==="free"?!used(a):a.keep))&&(!terms.length||terms.every(w=>[a.code,a.name,...ASMF.map(k=>a.tool[k]),...(U.get(a.sig)||[]).map(x=>x.article.number)].join(" ").toLowerCase().includes(w))));
  const LIM=150,open=a=>can("article")?"#a-"+a.id:"#v-"+a.id;
  box.innerHTML=!L.length?`<div class="empty"><h3>${esc(t("asmNone"))}</h3><p>${esc(t("asmNoneP"))}</p></div>`:R.length?`<div class="list"><table class="lt asmt"><thead><tr>${t("asmTh").map(h=>`<th>${esc(h)}</th>`).join("")}</tr></thead><tbody>
    ${R.slice(0,LIM).map(a=>{const T=a.tool,ra=normRA(T.ra),dims=[T.diameter?"Ø"+normDia(T.diameter):"",ra.kind==="R"?"R"+ra.val:ra.kind==="A"?ra.val+"°":""].filter(Boolean).join("  "),A2=[...new Set(U.get(a.sig)||[])];
      return `<tr class="row" data-asmid="${a.id}"><td><button class="asmcode" data-copy="${esc(a.code)}" title="${esc(t("asmCopyT"))}">${esc(a.code)}</button>${clean(a.name)||!a.auto||a.keep?`<div class="dim small">${esc(clean(a.name)||t(a.auto?"asmAuto":"asmManual"))}${a.keep?" · ★":""}</div>`:""}</td>
        <td><b class="asmty">${esc(T.type||"—")}</b>${dims?` <span class="m">${esc(dims)}</span>`:""}${T.insert?`<div class="dim small m">${esc(T.insert)}</div>`:""}</td>
        <td class="m">${esc(T.ls||"—")}${T.oal?` <span class="dim">/ ${esc(T.oal)}</span>`:""}</td>
        <td class="asmh">${linesOf_(T.holder).map((l,i)=>`<div class="${i?"dim small":""}">${esc(l)}</div>`).join("")||"—"}</td>
        <td><b class="m">${esc(normCode(T.code)||"—")}</b></td>
        <td>${A2.length?`<div class="asmuse">${A2.slice(0,4).map(x=>`<button class="mtag" data-go="${open(x)}">${esc(x.article.number||"?")} · ${esc(mShort(M(x.machineId)))}</button>`).join("")}${A2.length>4?`<span class="dim small">+${A2.length-4}</span>`:""}</div>`:`<span class="dim">${esc(t("asmNoUse"))}</span>`}</td>
        <td class="act">${ed?`<button class="btn sm ghost" data-asmed="${a.id}">${esc(t("edit"))}</button>`:""}</td></tr>`}).join("")}</tbody></table></div>${R.length>LIM?`<p class="note">${esc(t("pMore",R.length-LIM))}</p>`:""}`
    :`<div class="empty"><h3>${esc(t("pNone"))}</h3><p>${esc(t("pNoneP"))}</p></div>`;
  box.querySelectorAll("[data-go]").forEach(b=>b.onclick=e=>{e.stopPropagation();go(b.dataset.go)});
  box.querySelectorAll("[data-copy]").forEach(b=>b.onclick=e=>{e.stopPropagation();asmCopy(b.dataset.copy)});
  box.querySelectorAll("[data-asmed]").forEach(b=>b.onclick=e=>{e.stopPropagation();asmDialog(asmList().find(a=>a.id===b.dataset.asmed))});
  if(ed)box.querySelectorAll("tr[data-asmid]").forEach(tr=>tr.onclick=()=>asmDialog(asmList().find(a=>a.id===tr.dataset.asmid)))}
function asmDialog(a){const isNew=!a,T=a?a.tool:{};
  dialog(esc(isNew?t("asmNewT"):t("asmEditT",a.code)),`<div class="grid asmform">
    <label class="f c3">${esc(colLabel("type"))}<input data-af="type" class="up" list="types" value="${esc(T.type||"")}"></label>
    <label class="f c1">Ø<input data-af="diameter" class="m" value="${esc(T.diameter||"")}"></label>
    <label class="f c1">R / °<input data-af="ra" class="m" value="${esc(T.ra||"")}"></label>
    <label class="f c1">${esc(colLabel("code"))}<input data-af="code" class="m up" list="codes" value="${esc(T.code||"")}"></label>
    <label class="f c2">${esc(colLabel("insert"))}<input data-af="insert" class="m up" value="${esc(T.insert||"")}"></label>
    <label class="f c1">LS<input data-af="ls" class="m" value="${esc(T.ls||"")}"></label>
    <label class="f c1">LT<input data-af="oal" class="m" value="${esc(T.oal||"")}"></label>
    <label class="f c1">Z<input data-af="z" class="m" value="${esc(T.z||"")}"></label>
    <label class="f c1">${esc(t("asmName"))}<input id="as-name" value="${esc(a&&a.name||"")}"></label>
    <label class="f c6">${esc(colLabel("holder"))}<textarea data-af="holder" class="up" rows="2">${esc(T.holder||"")}</textarea></label>
    <label class="chk c6"><input type="checkbox" id="as-keep" ${!a||a.keep?"checked":""}> ${esc(t("asmKeep"))}</label>
    <p class="err c6" id="as-err" hidden></p></div>`,
    `${isNew?"":`<button class="btn ghost danger" id="as-del">${esc(t("asmDel"))}</button><span class="sp"></span>`}<button class="btn ghost" id="d-cancel">${esc(t("cancel"))}</button><button class="btn red" id="as-ok">${esc(t("asmSave"))}</button>`);
  $(".dlg").classList.add("wide");$("#d-cancel").onclick=closeDlg;
  $("#as-ok").onclick=()=>{const tool={};document.querySelectorAll("[data-af]").forEach(i=>{const v=String(i.value||"").replace(/\r/g,"").split("\n").map(s=>s.trim()).filter(Boolean).join("\n");if(v)tool[i.dataset.af]=i.dataset.af==="code"?normCode(v):v});
    const err=m=>{const e=$("#as-err");e.textContent=m;e.hidden=false};if(!asmReady(tool)){err(t("asmNeed"));return}
    const s=asmSig(tool),other=asmList().find(x=>x.sig===s&&x!==a);if(other){err(t("asmSame",other.code));return}
    const name=clean($("#as-name").value),keep=$("#as-keep").checked;
    if(isNew)asmList().push({id:uid(),code:asmNext(),tool,sig:s,name,keep:keep?1:0,auto:0,createdAt:Date.now()});
    else{a.tool=tool;a.sig=s;a.name=name;a.keep=keep?1:0;a.updatedAt=Date.now()}
    saveDB();closeDlg();drawAsm();toast(t("asmSaved",isNew?asmList()[asmList().length-1].code:a.code))};
  $("#as-del")&&($("#as-del").onclick=()=>{dialog(esc(t("asmDel")),`<p style="margin:0">${esc(t("asmDelQ",a.code))}</p>`,`<button class="btn ghost" id="d-cancel">${esc(t("cancel"))}</button><button class="btn red" id="as-delok">${esc(t("asmDel"))}</button>`);
    $("#d-cancel").onclick=closeDlg;$("#as-delok").onclick=()=>{const L=asmList(),i=L.indexOf(a);if(i>=0)L.splice(i,1);saveDB();closeDlg();drawAsm();toast(t("asmDelOk",a.code))}})}

/* ---------- 4. reports ---------- */'''

ASM_CSS=r'''
/* ---------- assemblies ---------- */
.asmc{display:block;margin:3px 0 0;padding:1px 5px;border:0;border-radius:4px;background:var(--fill);color:var(--mid);font:600 10.5px/1.5 var(--mono);letter-spacing:.02em;cursor:pointer;white-space:nowrap}
.asmc:hover{background:var(--hair);color:var(--ink)}
.asmt td{vertical-align:top;padding-top:11px;padding-bottom:11px}
.asmcode{border:1px solid var(--hair);background:var(--paper);color:var(--ink);font:700 14px/1 var(--mono);padding:7px 9px;border-radius:7px;cursor:copy}
.asmcode:hover{border-color:var(--ink)}
.asmty{font-family:var(--display6);font-size:15px;letter-spacing:.01em}
.asmh{max-width:320px}
.asmuse{display:flex;flex-wrap:wrap;gap:5px;align-items:center}
.asmuse .mtag{cursor:pointer;border:0}
.asmform{gap:10px 12px}
.asmform textarea{min-height:58px}
.dlg .ft .sp{flex:1}
.rowbar .laysel.sortsel select{min-width:0}

/* ---------- top bar: one size, one style ---------- */
.top .tb,.top .lang{height:36px;box-sizing:border-box}
.top .tb{min-width:36px;padding:0 10px;border:1px solid var(--top-bd);border-radius:8px;background:transparent;color:var(--top-ink);font:500 13.5px/1 var(--body);gap:7px;justify-content:center}
.top .tb:hover{background:var(--top-hover)}
.top .tb svg{width:17px;height:17px;flex:none}
.top .tb.menubtn{padding:0}
.top .tb.themetog,.top #b-logo,.top #b-backup,.top #b-restore,.top #b-getapp{width:36px;padding:0}
.top #b-role{padding:0 8px}
.top .lang{display:inline-flex;border-radius:8px;overflow:hidden}
.top .lang button{height:100%}
#tbar{display:inline-flex;align-items:center;gap:0;margin-right:4px}
#tbar:empty{display:none}
/* the sheet's actions: preview switch, then one joined group: print · PDF · Excel */
#tbar .tb{border-radius:0;margin-left:-1px}
#tbar .tb:first-child{border-radius:8px 0 0 8px;margin-left:0}
#tbar .tb:last-child{border-radius:0 8px 8px 0}
#tbar .tb:only-child{border-radius:8px}
#tbar .tb.pvtog{border-radius:8px;margin-right:8px}
#tbar .tb.pvtog+.tb{border-radius:8px 0 0 8px;margin-left:0}
#tbar .tb .lbl,#tbar .tb .lbl2{display:inline}
#tbar .tb.dl .lbl,#tbar .tb.pvtog .lbl{display:none}
#tbar #b-print .lbl{display:inline}
#tbar .tb.dl{position:relative;z-index:1;background:var(--red);border-color:var(--red);color:#fff;font-weight:600;padding:0 14px}
#tbar .tb.dl:hover{background:var(--red-l);border-color:var(--red-l)}
#tbar .tb.xl{color:var(--top-ink);border-color:var(--top-bd)}
#tbar .tb.xl .lbl2{display:inline}
#tbar .tb.xl svg{color:#2f9a5e}
#tbar .tb.xl:hover{background:var(--top-hover)}
:root[data-theme="dark"] #tbar .tb.xl{color:var(--top-ink);border-color:var(--top-bd)}
:root[data-theme="dark"] #tbar .tb.xl:hover{background:var(--top-hover)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) #tbar .tb.xl{color:var(--top-ink);border-color:var(--top-bd)}}
@media (max-width:1280px){#tbar #b-print .lbl{display:none}}
@media (max-width:1100px){#tbar .tb.xl .lbl2{display:none}}
.top .tb.getapp{border-color:var(--top-bd)!important;font-weight:500}
.top .tb.getapp:hover{background:var(--top-hover);color:var(--top-ink)}
.top #b-role{height:36px;padding:0 4px;min-width:36px}
.top .rolechip .gi{width:26px;height:26px;border-radius:6px;background:transparent;color:var(--red)}
:root[data-theme="dark"] .top .rolechip .gi{color:#ff6b6e}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .top .rolechip .gi{color:#ff6b6e}}
.top .rolechip .gi svg{width:18px;height:18px}
</style></head>'''

R=[
# module + page
('''
/* ---------- 4. reports ---------- */''',ASM_JS),
('''#wfs .wfserr{color:var(--red-tx,var(--red));font-weight:600}
</style></head>''','''#wfs .wfserr{color:var(--red-tx,var(--red));font-weight:600}'''+ASM_CSS),
# routing, menu, permissions
('''<button data-nav="#arts" id="nav-a"></button>''','''<button data-nav="#arts" id="nav-a"></button><button data-nav="#asm" id="nav-s"></button>'''),
('''  if(h==="reports")return{view:"reports"};''','''  if(h==="reports")return{view:"reports"};
  if(h==="asm")return{view:"asm"};'''),
('''reports:"#reports",admin:"#admin",arts:"#arts"}[route.view]??"#";''','''reports:"#reports",admin:"#admin",arts:"#arts",asm:"#asm"}[route.view]??"#";'''),
('''  else if(route.view==="arts"){cr.innerHTML="";renderArts()}''','''  else if(route.view==="arts"){cr.innerHTML="";renderArts()}
  else if(route.view==="asm"){cr.innerHTML="";renderAsm()}'''),
('''$("#nav-a").textContent=t("navArts");''','''$("#nav-a").textContent=t("navArts");$("#nav-s").textContent=t("navAsm");'''),
('''const NAV_ORDER=["#","#arts","#crib","#holders","#prod","#mags","#log","#reports"];''','''const NAV_ORDER=["#","#arts","#asm","#crib","#holders","#prod","#mags","#log","#reports"];'''),
('''  {k:"sheets",views:["article","aview"],rights:''','''  {k:"sheets",views:["article","aview","asm"],rights:'''),
('''P.nav=NAV_ORDER.filter(h=>P.admin||pg.some(p=>p.nav===h));''','''P.nav=NAV_ORDER.filter(h=>P.admin||pg.some(p=>p.nav===h)||(h==="#asm"&&pg.some(p=>p.k==="sheets")));'''),
('''  admin:{views:"*",nav:["#","#arts","#crib","#holders","#prod","#mags","#log","#reports"],''','''  admin:{views:"*",nav:["#","#arts","#asm","#crib","#holders","#prod","#mags","#log","#reports"],'''),
('''  methode:{views:["home","machine","article","mags","mag","arts","aview"],nav:["#","#arts","#mags"],''','''  methode:{views:["home","machine","article","mags","mag","arts","aview","asm"],nav:["#","#arts","#asm","#mags"],'''),
# data: merge between PCs, codes kept unique, first fill from the existing sheets
('''  out.artNotes=mergeList(b.artNotes||[],m.artNotes||[],t.artNotes||[],"num");if(!out.artNotes.length)delete out.artNotes;''','''  out.artNotes=mergeList(b.artNotes||[],m.artNotes||[],t.artNotes||[],"num");if(!out.artNotes.length)delete out.artNotes;
  out.assemblies=mergeList(b.assemblies||[],m.assemblies||[],t.assemblies||[],"id");out.asmSeeded=m.asmSeeded||t.asmSeeded;if(!out.asmSeeded)delete out.asmSeeded;'''),
('''  db.articles.forEach(a=>{if(!a.article)a.article={};if(!Array.isArray(a.tools))a.tools=[]});''','''  db.articles.forEach(a=>{if(!a.article)a.article={};if(!Array.isArray(a.tools))a.tools=[]});if(Array.isArray(db.assemblies)&&typeof asmFix==="function")asmFix();'''),
('''function render(){
  if(edTimer){clearTimeout(edTimer);edTimer=null;flushEditor()}''','''function render(){
  if(edTimer){clearTimeout(edTimer);edTimer=null;flushEditor()}
  if(ROLE&&typeof asmBoot==="function")asmBoot();'''),
# editor: make assemblies while typing, fill a row from its code, show the code, sort
('''function edited(){cur.updatedAt=Date.now();''','''function edited(){if(typeof asmLater==="function")asmLater();cur.updatedAt=Date.now();'''),
('''    if(fillFromCrib(i)){renderRows();edited();toast(t("filled",normCode(cur.tools[i].code)))}});''','''    const as0=asmFind(cur.tools[i].code);if(as0){asmApply(cur.tools[i],as0);renderRows();edited();toast(t("asmFilled",as0.code));return}
    if(asmKey(cur.tools[i].code)){toast(t("asmUnknown",asmKey(cur.tools[i].code)));return}
    if(fillFromCrib(i)){renderRows();edited();toast(t("filled",normCode(cur.tools[i].code)))}});
  rows.addEventListener("click",e=>{const b=e.target.closest(".asmc");if(b&&b.dataset.asm){e.stopPropagation();asmCopy(b.dataset.asm)}});'''),
('''    ${visCols(sheetCfg()).map(k=>k==="t"?`<td data-col="t"><input class="m b up" data-k="t" value="${v("t")}" placeholder="T${String(i+1).padStart(2,"0")}"></td>`''','''    ${visCols(sheetCfg()).map(k=>k==="t"?`<td data-col="t"><input class="m b up" data-k="t" value="${v("t")}" placeholder="T${String(i+1).padStart(2,"0")}">${asmChipHTML(x)}</td>`'''),
('''<button class="btn ghost" id="b-ncimp" title="${esc(t("impNCP"))}">${esc(t("ncFromProg"))}</button>''','''<button class="btn ghost" id="b-ncimp" title="${esc(t("impNCP"))}">${esc(t("ncFromProg"))}</button><label class="laysel sortsel" title="${esc(t("sortT"))}"><span>${esc(t("sortL"))}</span><select id="a-sort"><option value="">—</option>${Object.entries(t("sortBy")).map(([k,l])=>`<option value="${k}">${esc(l)}</option>`).join("")}</select></label>'''),
('''  edIndex0=cur.article.index||"";edBaseline();applyLock();drawHistory();
  $("#codes").innerHTML=(db.catalog||[]).map(c=>`<option value="${esc(c.code)}">${esc([c.type,c.diameter?"Ø"+c.diameter:""].filter(Boolean).join(" "))}</option>`).join("");''','''  edIndex0=cur.article.index||"";edBaseline();applyLock();drawHistory();
  $("#codes").innerHTML=(db.catalog||[]).map(c=>`<option value="${esc(c.code)}">${esc([c.type,c.diameter?"Ø"+c.diameter:""].filter(Boolean).join(" "))}</option>`).join("")+asmCodeOptions();
  $("#a-sort").onchange=e=>{const k=e.target.value;e.target.value="";if(k)sortRows(k)};'''),
# guide
('''["templates","Modèles Excel et import",''','''["asm","Assemblages",["Chaque outil avec son porte-outil est gardé sous un code (AS0001…), tout seul, dès qu’une ligne de fiche a un porte-outil et un code outil (ou un type et un Ø).","Le code s’affiche sous le numéro T de la ligne. Tapez-le dans la case Code d’une autre fiche : toute la ligne se remplit.","La page Assemblages les liste, montre les fiches qui les utilisent, et permet d’en créer, modifier ou supprimer."]],
   ["sort","Trier une fiche",["Sous le tableau des outils, « Trier » remet les lignes dans l’ordre voulu : numéro T, correcteur, type, Ø, porte-outil, code outil ou LS. Le PDF suit. « Annuler » revient à l’ordre d’avant."]],
   ["templates","Modèles Excel et import",'''),
('''["templates","Excel models and import",''','''["asm","Assemblies",["Each tool with its holder is kept under a code (AS0001…), by itself, as soon as a sheet row has a holder and a tool code (or a type and a Ø).","The code shows under the row’s T number. Type it in the Code box of another sheet: the whole row fills in.","The Assemblies page lists them, shows the sheets using each one, and lets you add, change or delete them."]],
   ["sort","Sorting a sheet",["Under the tools table, “Sort” puts the rows in the order you want: T number, corrector, type, Ø, holder, tool code or LS. The PDF follows. “Undo” goes back to the order before."]],
   ["templates","Excel models and import",'''),
]
for f in sys.argv[1:]:
  s=open(f).read()
  for a,b in R:
    assert s.count(a)==1,(f,s.count(a),a[:100])
    s=s.replace(a,b)
  open(f,'w').write(s);print("patched",f)
