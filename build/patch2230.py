import sys
# 2.23.0: Location column (from the tool crib, under the tool code by default), sheet options
# (holder location, row height, check boxes), pick list by location, search everywhere (Ctrl+K)
BLOCK=r'''/* ---------- where each tool is (2.23): the Location column, filled from the tool crib ----------
   It is not typed in the sheet: it shows the location of the tool code in the crib (and, as an option, of the holder),
   so it is always up to date. By default it sits under the tool code, like the assembly code under the tool number. */
Object.assign(I18N.en,{colLoc:"Location",locShort:"Loc.",locHol:"H",locAdd:"+ location",locNone:"no location",locNoCard:"not in the crib",
  locTip:"Location in the tool crib: click to change it",locTipRO:"Location in the tool crib",locAddTip:"This tool has no location yet: click to add it",
  locDlgT:c=>`Where is ${c}?`,locDlgP:"The shelf, cabinet or drawer where this tool is kept. It shows on every tool sheet that uses it, on the PDF and in the tool prep list.",
  locPh:"e.g. Cabinet 2 – drawer 3",locUsed:"Locations already used",locSaved:(c,l)=>l?`${c}: ${l}`:`${c}: location removed`,
  layOptLocH:"Location: add the holder's", layOptDens:"Row height", densC:"Compact", densN:"Normal", densA:"Airy",
  layOptChk:"Check boxes", chkN:["None","1 box (Ready)","2 boxes (Prepared · Mounted)"],
  ppSortT:"Pick order", ppByT:"By T", ppByLoc:"By location",
  gfT:"Search everywhere",gfPh:"Tool code, article, holder, assembly, location…",gfKeys:"↑ ↓ to move · Enter to open · Esc to close",gfBtn:"Search",gfBtnT:"Search everywhere (Ctrl+K)",
  gfNone:"Nothing found.",gfStart:"Type a tool code, an article number, a holder, an assembly code or a location.",
  gfG:{crib:"Tools (crib)",holders:"Holders",arts:"Tool sheets",asm:"Assemblies",mach:"Machines"},gfIn:c=>`uses ${c}`,gfMore:n=>`+ ${n} more`});
Object.assign(I18N.fr,{colLoc:"Emplacement",locShort:"Empl.",locHol:"PO",locAdd:"+ emplacement",locNone:"sans emplacement",locNoCard:"pas au magasin",
  locTip:"Emplacement au magasin outils : cliquez pour le changer",locTipRO:"Emplacement au magasin outils",locAddTip:"Cet outil n’a pas encore d’emplacement : cliquez pour l’ajouter",
  locDlgT:c=>`Où est ${c} ?`,locDlgP:"L’étagère, l’armoire ou le tiroir où l’outil est rangé. Il s’affiche sur toutes les fiches qui l’utilisent, sur le PDF et dans la liste de préparation.",
  locPh:"ex. Armoire 2 – tiroir 3",locUsed:"Emplacements déjà utilisés",locSaved:(c,l)=>l?`${c} : ${l}`:`${c} : emplacement retiré`,
  layOptLocH:"Emplacement : ajouter celui du porte-outil", layOptDens:"Hauteur des lignes", densC:"Serrée", densN:"Normale", densA:"Aérée",
  layOptChk:"Cases à cocher", chkN:["Aucune","1 case (Prêt)","2 cases (Préparé · Monté)"],
  ppSortT:"Ordre de sortie", ppByT:"Par T", ppByLoc:"Par emplacement",
  gfT:"Rechercher partout",gfPh:"Code outil, article, porte-outil, assemblage, emplacement…",gfKeys:"↑ ↓ pour choisir · Entrée pour ouvrir · Échap pour fermer",gfBtn:"Rechercher",gfBtnT:"Rechercher partout (Ctrl+K)",
  gfNone:"Rien trouvé.",gfStart:"Tapez un code outil, un numéro d’article, un porte-outil, un code d’assemblage ou un emplacement.",
  gfG:{crib:"Outils (magasin)",holders:"Porte-outils",arts:"Fiches outils",asm:"Assemblages",mach:"Machines"},gfIn:c=>`utilise ${c}`,gfMore:n=>`+ ${n} autres`});
try{I18N.en.sortBy.loc="Location (for the tool prep)";I18N.fr.sortBy.loc="Emplacement (pour la préparation)"}catch(e){}
const pinIcon=`<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21s-6.5-5.7-6.5-11a6.5 6.5 0 0 1 13 0c0 5.3-6.5 11-6.5 11Z"/><circle cx="12" cy="10" r="2.3"/></svg>`;
const locUnderC=cfg=>!!(cfg&&cfg.joinTo&&cfg.joinTo.loc==="code");
// the location lines of a row: each tool code's place in the crib, then (layout option) each holder's
function locLines(x,cfg){if(!x)return "";const o=((cfg||LAYCFG)&&(cfg||LAYCFG).opt)||{},out=[];
  linesOf_(x.code).forEach(l=>{const c=C_(l);if(c&&clean(c.location))out.push(clean(c.location))});
  if(o.locH)splitHolders(x.holder).forEach(p=>{const h=H_(p);if(h&&clean(h.location))out.push(t("locHol")+" "+clean(h.location))});
  return [...new Set(out)].join("\n")}
const withLoc=(tools,cfg)=>(tools||[]).map(x=>{if(!x||!clean(x.code)&&!clean(x.holder))return x;const l=locLines(x,cfg);return l?{...x,loc:l}:x});
SORTK.loc=x=>locLines(x,sheetCfg(cur)).split("\n")[0]||null;
// what the editor shows under the code (or in its own column)
function locTag(x){const code=linesOf_(x&&x.code)[0];if(!code)return `<span class="loctag empty" data-loctag></span>`;
  const c=C_(code),L=locLines(x,sheetCfg(cur)),ed=hasRight("cribEdit");
  if(L)return `<button type="button" class="loctag${ed?"":" ro"}" data-loctag data-lc="${esc(normCode(code))}" tabindex="-1" title="${esc(t(ed?"locTip":"locTipRO"))}">${pinIcon}<span>${esc(L.replace(/\n/g," · "))}</span></button>`;
  if(c&&ed)return `<button type="button" class="loctag add" data-loctag data-lc="${esc(normCode(code))}" tabindex="-1" title="${esc(t("locAddTip"))}">${pinIcon}<span>${esc(t("locAdd"))}</span></button>`;
  return `<span class="loctag none" data-loctag>${esc(c?t("locNone"):t("locNoCard"))}</span>`}
function locRefresh(){if(!cur)return;document.querySelectorAll("#rows tr[data-i]").forEach(tr=>{const x=cur.tools[+tr.dataset.i],el=tr.querySelector("[data-loctag]");if(x&&el)el.outerHTML=locTag(x)})}
const locAll=()=>[...new Set([...(db.catalog||[]),...(db.holders||[])].map(q=>clean(q.location)).filter(Boolean))].sort((a,b)=>a.localeCompare(b,undefined,{numeric:true,sensitivity:"base"}));
function locDialog(code){const c=C_(code);if(!c||!hasRight("cribEdit"))return;const all=locAll(),K=normCode(c.code);
  dialog(esc(t("locDlgT",K)),`<p class="note" style="margin:0 0 10px">${esc(t("locDlgP"))}</p>
    <label class="f">${esc(t("cLoc"))}<input id="loc-v" value="${esc(c.location||"")}" list="loclist" placeholder="${esc(t("locPh"))}" autocomplete="off"></label><datalist id="loclist">${all.map(v=>`<option value="${esc(v)}">`).join("")}</datalist>
    ${all.length?`<div class="locsugg"><span class="dim small">${esc(t("locUsed"))}</span>${all.slice(0,16).map(v=>`<button type="button" class="chip sm" data-locv="${esc(v)}">${pinIcon}${esc(v)}</button>`).join("")}</div>`:""}`,
    `<button class="btn ghost" id="d-cancel">${esc(t("cancel"))}</button><button class="btn red" id="loc-ok">${esc(t("save"))}</button>`);
  const inp=$("#loc-v");setTimeout(()=>{inp.focus();inp.select()},0);
  const save=()=>{const v=clean(inp.value);if(v===clean(c.location)){closeDlg();return}c.location=v;c.updatedAt=Date.now();saveDB();closeDlg();locRefresh();pvLastKey="";schedulePreview(10);toast(t("locSaved",K,v))};
  $("#d-cancel").onclick=closeDlg;$("#loc-ok").onclick=save;inp.onkeydown=e=>{if(e.key==="Enter"){e.preventDefault();save()}};
  $("#ov").querySelectorAll("[data-locv]").forEach(b=>b.onclick=()=>{inp.value=b.dataset.locv;inp.focus()})}
document.addEventListener("click",e=>{const b=e.target.closest&&e.target.closest(".tt [data-loctag][data-lc]");if(!b)return;e.preventDefault();if(hasRight("cribEdit"))locDialog(b.dataset.lc)});
document.addEventListener("change",e=>{const i=e.target;if(i&&i.matches&&i.matches('#rows input[data-k="code"],#rows input[data-k="holder"]'))setTimeout(locRefresh,0)});
// the tool prep list can be taken out in shop order (by location)
let ppArt=null;
function prepSort(rows,art){ppArt=art;if(lsGet("bs.ppsort")!=="loc")return rows;const L=x=>locLines(x,{opt:{}})||"￿";
  return rows.map((x,i)=>({x,i,l:L(x)})).sort((a,b)=>a.l.localeCompare(b.l,undefined,{numeric:true,sensitivity:"base"})||a.i-b.i).map(o=>o.x)}
const ppSortBar=()=>{const v=lsGet("bs.ppsort")==="loc"?"loc":"t";return `<span class="ppsort" role="group" aria-label="${esc(t("ppSortT"))}"><button type="button" class="chip sm" data-pps="t" aria-pressed="${v==="t"}">${esc(t("ppByT"))}</button><button type="button" class="chip sm" data-pps="loc" aria-pressed="${v==="loc"}">${pinIcon}${esc(t("ppByLoc"))}</button></span>`};
document.addEventListener("click",e=>{const b=e.target.closest&&e.target.closest("[data-pps]");if(!b||!ppArt)return;lsSet("bs.ppsort",b.dataset.pps);const a=ppArt;closeDlg();prepDialog(a)});

/* ---------- search everywhere (Ctrl+K, or the magnifier in the top bar) ---------- */
const gfN=s=>String(s??"").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g,"");
function gfSearch(q){const Q=gfN(q).trim();if(!Q)return [];const W=Q.split(/\s+/).filter(Boolean),hit=s=>{const T=gfN(s);return W.every(w=>T.includes(w))};
  const rank=(key)=>{const k=gfN(key);return k===Q?0:k.startsWith(Q)?1:2},G=[];
  const add=(g,items)=>{if(items.length)G.push({g,items:items.sort((a,b)=>a.r-b.r||String(a.title).localeCompare(String(b.title),undefined,{numeric:true}))})};
  if(can("code")||can("pcode"))add("crib",(db.catalog||[]).filter(c=>hit([c.code,c.type,c.diameter?"Ø"+c.diameter:"",c.ref,c.insertRef,c.supplier,c.location].join(" "))).map(c=>({r:rank(c.code),title:c.code,mono:1,sub:[c.type,c.diameter?"Ø"+normDia(c.diameter):"",c.ref].filter(Boolean).join(" · "),loc:clean(c.location),stock:c,href:"#c-"+encodeURIComponent(c.code)})));
  if(can("holder")||can("pholder"))add("holders",(db.holders||[]).filter(h=>hit([h.ref,h.type,h.cone,h.supplier,h.location].join(" "))).map(h=>({r:rank(h.ref),title:h.ref,mono:1,sub:[h.type,h.cone].filter(Boolean).join(" · "),loc:clean(h.location),href:"#h-"+encodeURIComponent(h.ref)})));
  if(can("article")||can("aview")){const ed=can("article");add("arts",(db.articles||[]).map(a=>{const A0=a.article||{},m=M(a.machineId),base=[A0.number,A0.designation,A0.reference,A0.program,A0.phase,A0.index,m?mLabel(m):""].join(" ");
      let sub=[clean(A0.designation),m?mShort(m):"",SL(statusOf(a))].filter(Boolean).join(" · ");
      if(!hit(base)){const tc=realTools(a.tools).flatMap(x=>linesOf_(x.code)).map(normCode).find(c=>hit(c));if(!tc)return null;sub=t("gfIn",tc)+" · "+sub}
      return{r:rank(A0.number),title:(clean(A0.number)||t("noNumber"))+(clean(A0.index)?" · "+clean(A0.index):"")+(clean(A0.phase)?" · "+clean(A0.phase):""),mono:1,sub,href:(ed?"#a-":"#v-")+a.id}}).filter(Boolean))}
  if(can("asm"))add("asm",asmList().filter(a=>hit([a.code,a.name,a.tool&&a.tool.type,a.tool&&a.tool.diameter?"Ø"+a.tool.diameter:"",a.tool&&a.tool.holder,a.tool&&a.tool.code].join(" "))).map(a=>({r:rank(a.code),title:a.code,mono:1,sub:[a.tool.type,a.tool.diameter?"Ø"+normDia(a.tool.diameter):"",linesOf_(a.tool.holder)[0],a.tool.code].filter(Boolean).join(" · "),fn:()=>{asmQ=a.code;go("#asm")}})));
  if(can("machine"))add("mach",(db.machines||[]).filter(m=>m.id!=="nomachine"&&hit([m.name,m.abbr,m.brand,m.cone].join(" "))).map(m=>({r:rank(m.abbr||m.name),title:mLabel(m),sub:[normCone(m.cone),t("nArticles",db.articles.filter(a=>a.machineId===m.id).length)].filter(Boolean).join(" · "),href:"#m-"+m.id})));
  return G}
function gfind(q0){if(!ROLE||!$("#ov").hidden&&$("#gf-q"))return;
  dialog(esc(t("gfT")),`<div class="gfbox">${searchIcon}<input id="gf-q" type="search" placeholder="${esc(t("gfPh"))}" autocomplete="off" spellcheck="false" value="${esc(q0||"")}"></div><div class="gfres" id="gf-res" role="listbox"></div>`,
    `<span class="dim small gfkeys">${esc(t("gfKeys"))}</span><span class="sp"></span><button class="btn ghost" id="d-cancel">${esc(t("close"))}</button>`);
  $(".dlg").classList.add("wide","gfdlg");$("#d-cancel").onclick=closeDlg;
  const q=$("#gf-q"),box=$("#gf-res");let flat=[],on=0,tm;
  const open=i=>{const it=flat[i];if(!it)return;closeDlg();if(it.fn)it.fn();else go(it.href)};
  const mark=()=>{box.querySelectorAll(".gfi").forEach((b,i)=>b.classList.toggle("on",i===on));const b=box.querySelector(".gfi.on");if(b)b.scrollIntoView({block:"nearest"})};
  const draw=()=>{const G=gfSearch(q.value);flat=[];on=0;
    if(!clean(q.value)){box.innerHTML=`<p class="note gfempty">${esc(t("gfStart"))}</p>`;return}
    if(!G.length){box.innerHTML=`<p class="note gfempty">${esc(t("gfNone"))}</p>`;return}
    box.innerHTML=G.map(({g,items})=>{const show=items.slice(0,g==="arts"?8:6);return `<div class="gfg"><span>${esc(t("gfG")[g])}</span><b>${items.length}</b></div>`+show.map(it=>{const i=flat.push(it)-1,s=it.stock?stockState(it.stock):"";
      return `<button type="button" class="gfi g-${g}" data-gi="${i}" role="option"><span class="gft"><b class="${it.mono?"m":""}">${esc(it.title)}</b>${it.sub?`<span class="dim">${esc(it.sub)}</span>`:""}</span>${it.loc?`<span class="gfloc">${pinIcon}${esc(it.loc)}</span>`:""}${s?`<span class="spill s-${s}">${+it.stock.stock||0}</span>`:""}</button>`}).join("")+(items.length>show.length?`<div class="gfmore dim small">${esc(t("gfMore",items.length-show.length))}</div>`:"")}).join("");
    box.querySelectorAll(".gfi").forEach(b=>{b.onclick=()=>open(+b.dataset.gi);b.onmousemove=()=>{if(on!==+b.dataset.gi){on=+b.dataset.gi;mark()}}});mark()};
  q.oninput=()=>{clearTimeout(tm);tm=setTimeout(draw,(db.catalog||[]).length>2000?120:40)};
  q.onkeydown=e=>{if(e.key==="ArrowDown"){e.preventDefault();if(flat.length){on=(on+1)%flat.length;mark()}}else if(e.key==="ArrowUp"){e.preventDefault();if(flat.length){on=(on-1+flat.length)%flat.length;mark()}}else if(e.key==="Enter"){e.preventDefault();open(on)}};
  draw();setTimeout(()=>{q.focus();q.select()},0)}
document.addEventListener("keydown",e=>{if(!ROLE)return;const k=(e.key||"").toLowerCase();
  const typing=/^(input|textarea|select)$/i.test((document.activeElement||{}).tagName||"")||(document.activeElement&&document.activeElement.isContentEditable);
  if((e.ctrlKey||e.metaKey)&&!e.shiftKey&&!e.altKey&&k==="k"){e.preventDefault();gfind();return}
  if(k==="/"&&!typing&&!e.ctrlKey&&!e.metaKey&&$("#ov").hidden){e.preventDefault();gfind()}});
function gfChrome(){const b=$("#b-find");if(!b)return;b.hidden=!ROLE||route&&route.view==="gate";b.title=t("gfBtnT");b.setAttribute("aria-label",t("gfBtnT"));
  b.innerHTML=searchIcon+`<span class="lbl">${esc(t("gfBtn"))}</span><kbd>Ctrl K</kbd>`}
{const b=$("#b-find");if(b){b.onclick=()=>gfind();gfChrome();try{new MutationObserver(()=>{const h=!ROLE||route&&route.view==="gate";if(b.hidden!==h||b.title!==t("gfBtnT"))gfChrome()}).observe($("#view"),{childList:true})}catch(e){}}}

'''
CSS=r'''
/* 2.23: location under the tool code (or in its own column) */
.tt .loctag{display:flex;align-items:center;gap:3px;width:max-content;max-width:100%;margin:2px 0 0;padding:1px 5px 1px 3px;border:0;border-radius:6px;background:transparent;color:var(--mid);font:600 11px/1.35 var(--body);cursor:pointer;white-space:nowrap;overflow:hidden;text-align:left}
.tt .loctag span{overflow:hidden;text-overflow:ellipsis}
.tt .loctag svg{width:12px;height:12px;flex:0 0 auto;color:var(--red)}
.tt .loctag:hover{background:var(--fill);color:var(--ink)}
.tt .loctag.ro{cursor:default}.tt .loctag.ro:hover{background:transparent;color:var(--mid)}
.tt .loctag.add{color:var(--soft);font-weight:500}.tt .loctag.add svg{color:var(--soft)}.tt .loctag.add:hover{color:var(--red)}.tt .loctag.add:hover svg{color:var(--red)}
.tt .loctag.none{cursor:default;color:var(--soft);font-weight:400;font-size:10.5px;padding-left:4px}
.tt .loctag.empty{display:none}
.tt td.loccell{vertical-align:middle}.tt td.loccell .loctag{margin:0}
.tt thead tr.prrow .locpr{margin-left:4px}
.locsugg{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-top:12px}.locsugg .dim{width:100%}
.locsugg .chip svg,.ppsort .chip svg{width:12px;height:12px;color:var(--red)}
.ppsort{display:inline-flex;gap:4px;margin-left:6px}.ppsort .chip[aria-pressed="true"]{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.ppsort .chip[aria-pressed="true"] svg{color:inherit}
/* search everywhere */
.top .gfbtn{display:inline-flex;align-items:center;gap:7px}
.top .gfbtn svg{width:17px;height:17px}
.top .gfbtn kbd{font:600 10px/1 var(--mono);padding:3px 5px;border-radius:5px;border:1px solid rgba(255,255,255,.28);color:rgba(255,255,255,.75)}
.top .gfbtn .lbl,.top .gfbtn kbd{display:none}
@media (min-width:1400px){.top .gfbtn .lbl,.top .gfbtn kbd{display:inline}}
.dlg.gfdlg{width:min(720px,calc(100vw - 24px))}
.dlg.gfdlg .bd{display:flex;flex-direction:column;gap:10px;min-height:min(460px,60vh)}
.gfbox{position:relative}
.gfbox svg{position:absolute;left:12px;top:50%;width:18px;height:18px;transform:translateY(-50%);color:var(--mid);pointer-events:none}
.gfbox input{width:100%;height:46px;padding:0 14px 0 40px;border:1.5px solid var(--hair);border-radius:12px;background:var(--paper);font-size:16px}
.gfbox input:focus{outline:none;border-color:var(--ink)}
.gfres{display:flex;flex-direction:column;gap:2px;overflow:auto;max-height:60vh}
.gfg{display:flex;align-items:center;gap:8px;margin:10px 2px 3px;font:600 11px/1 var(--body);text-transform:uppercase;letter-spacing:.06em;color:var(--mid)}
.gfg:first-child{margin-top:2px}.gfg b{font:600 11px/1 var(--mono);color:var(--soft)}
.gfi{display:flex;align-items:center;gap:10px;width:100%;padding:8px 10px;border:1px solid transparent;border-radius:10px;background:transparent;text-align:left;cursor:pointer}
.gfi.on{background:var(--fill);border-color:var(--hair)}
.gfi .gft{display:flex;flex-direction:column;gap:1px;min-width:0;flex:1}
.gfi .gft b{font-size:14px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.gfi .gft b.m{font-family:var(--mono)}
.gfi .gft .dim{font-size:12.5px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.gfloc{display:inline-flex;align-items:center;gap:4px;flex:0 0 auto;max-width:42%;padding:3px 9px 3px 7px;border-radius:999px;background:var(--fill);border:1px solid var(--hair);font:600 12px/1.2 var(--body);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.gfloc svg{width:13px;height:13px;color:var(--red);flex:0 0 auto}
.gfi .spill{flex:0 0 auto}
.gfmore{padding:2px 12px 4px}
.gfempty{margin:18px 4px}
@media (max-width:600px){.gfkeys{display:none}.gfloc{max-width:46%}}
'''
R=[
# --- the column itself
('''const LABK=["t","asm","corr","type","diameter","ra","insert","ls","oal","z","holder","code"];''','''const LABK=["t","asm","corr","type","diameter","ra","insert","ls","oal","z","holder","code","loc"];'''),
('''const JOINORD=["t","asm","corr","type","diameter","ra","insert","ls","oal","z","holder","code"];''','''const JOINORD=["t","asm","corr","type","diameter","ra","insert","ls","oal","z","holder","code","loc"];'''),
('''if(!(c&&c.asmOwn)&&!out.asm&&!(hidden||[]).includes("asm")&&!Object.values(out).includes("asm"))out.asm="t";''',
 '''if(!(c&&c.asmOwn)&&!out.asm&&!(hidden||[]).includes("asm")&&!Object.values(out).includes("asm"))out.asm="t";
  if(!(c&&c.locOwn)&&!out.loc&&!out.code&&!(hidden||[]).includes("loc")&&!(hidden||[]).includes("code")&&!Object.values(out).includes("loc"))out.loc="code";'''),
('''keys.forEach(k=>{if(!out.includes(k)){if(k==="asm")out.unshift(k);else out.push(k)}});return out};''','''keys.forEach(k=>{if(!out.includes(k)){if(k==="asm")out.unshift(k);else if(k==="loc"&&out.includes("code"))out.splice(out.indexOf("code")+1,0,k);else out.push(k)}});return out};'''),
('''const edCols=cfg=>visCols(cfg).filter(k=>!(k==="asm"&&asmUnderT(cfg||LAYCFG)));''','''const edCols=cfg=>visCols(cfg).filter(k=>!(k==="asm"&&asmUnderT(cfg||LAYCFG))&&!(k==="loc"&&locUnderC(cfg||LAYCFG)));'''),
('''n.asmOwn=!!(c&&c.asmOwn);''','''n.asmOwn=!!(c&&c.asmOwn);n.locOwn=!!(c&&c.locOwn);'''),
('''VCOLS=edCols(LAYCFG).flatMap''','''VCOLS=edCols(LAYCFG).filter(k=>k!=="loc").flatMap'''),
('''holder:t("colHolder"),code:t("colCode")}''','''holder:t("colHolder"),code:t("colCode"),loc:t("colLoc")}'''),
('''{joinTo:buf.joinTo,asmOwn:!buf.joinTo.asm}''','''{joinTo:buf.joinTo,asmOwn:!buf.joinTo.asm,locOwn:!buf.joinTo.loc}'''),
('''asmOwn:!buf.joinTo.asm,opt:''','''asmOwn:!buf.joinTo.asm,locOwn:!buf.joinTo.loc,opt:'''),
('''noprint:c.noprint,asmOwn:c.asmOwn}''','''noprint:c.noprint,asmOwn:c.asmOwn,locOwn:c.locOwn}''',2),
('''code:"F102"}[k]||"Abc 123"''','''code:"F102",loc:"A-03"}[k]||"Abc 123"'''),
('''const DEFW={asm:88,''','''const DEFW={loc:110,asm:88,'''),
('''const MIN={type:140,holder:100,insert:76}''','''const MIN={type:140,holder:100,insert:76,loc:72}'''),
# --- layout options
('''zebra:!!o.zebra,blank:''','''zebra:!!o.zebra,locH:!!o.locH,chk:[1,2].includes(+o.chk)?+o.chk:0,dens:o.dens==="c"||o.dens==="a"?o.dens:"n",blank:'''),
('''ck("zebra",t("layOptZebra"))}''','''ck("zebra",t("layOptZebra"))}${ck("locH",t("layOptLocH"))}<label class="f sm">${esc(t("layOptDens"))}<select data-dens>${[["c",t("densC")],["n",t("densN")],["a",t("densA")]].map(([v,l])=>`<option value="${v}" ${(buf.opt.dens||"n")===v?"selected":""}>${esc(l)}</option>`).join("")}</select></label><label class="f sm">${esc(t("layOptChk"))}<select data-chk>${[0,1,2].map(n=>`<option value="${n}" ${(buf.opt.chk||0)===n?"selected":""}>${esc(t("chkN")[n])}</option>`).join("")}</select></label>'''),
('''B.querySelectorAll("[data-blank]").forEach(c=>c.onchange=()=>{buf.opt.blank=+c.value});''','''B.querySelectorAll("[data-blank]").forEach(c=>c.onchange=()=>{buf.opt.blank=+c.value});B.querySelectorAll("[data-dens]").forEach(c=>c.onchange=()=>{buf.opt.dens=c.value});B.querySelectorAll("[data-chk]").forEach(c=>c.onchange=()=>{buf.opt.chk=+c.value});'''),
# --- PDF
('''zebra:!!O0.zebra,blank:''','''zebra:!!O0.zebra,chk:[1,2].includes(+O0.chk)?+O0.chk:0,dens:O0.dens,blank:'''),
('''const TSUB=["diameter","ra","insert"],ORD=["t","asm","corr","type","diameter","ra","insert","ls","oal","z","holder","code",''','''const TSUB=["diameter","ra","insert"],ORD=["t","asm","corr","type","diameter","ra","insert","ls","oal","z","holder","code","loc",'''),
('''.concat(EXTRA.map(x=>["x_"+x.id,BLANK?16:18])).filter(([k])=>k==="t"||(BLANK?on(k):k==="type"?typeOn:sepC(k)));''','''.concat(EXTRA.map(x=>["x_"+x.id,BLANK?16:18])).concat([["loc",24]]).filter(([k])=>k==="t"||(BLANK?on(k)&&k!=="loc":k==="type"?typeOn:sepC(k)));'''),
('''  const KEYS=SPEC.map(s=>s[0]),KI=''','''  if(OPT.chk)SPEC.push(["chk",OPT.chk>1?17:10]);
  const KEYS=SPEC.map(s=>s[0]),KI='''),
('''["holder",42],["code",21],...EXTRA.map(x=>["x_"+x.id,18])]);''','''["holder",42],["code",21],["loc",24],["chk",10],...EXTRA.map(x=>["x_"+x.id,18])]);'''),
('''code:lab("code",L.head[7]),asm:''','''code:lab("code",L.head[7]),loc:lab("loc",LANG==="fr"?"Emplacement":"Location"),chk:OPT.chk>1?(LANG==="fr"?"Prép. Monté":"Prep Set"):(LANG==="fr"?"Prêt":"Ready"),asm:'''),
('''const lb=HEADOF[j]+" "''','''const lb=(j==="loc"&&!clean(LAB.loc)?(LANG==="fr"?"Empl.":"Loc."):HEADOF[j])+" "'''),
('''/^(holder|type)$/.test(j)||j.startsWith("x_")?"Plex5"''','''/^(holder|type|loc)$/.test(j)||j.startsWith("x_")?"Plex5"''',2),
('''["ls","oal","z","code","diameter","ra","insert"].filter''','''["ls","oal","z","code","diameter","ra","insert","loc"].filter'''),
('''// your own columns
    EXTRA.forEach''','''if(KI.loc!=null){at("loc");useK("loc");const lv=linesOf(t.loc);if(lv.length)stack(lv,X_("loc")+1.6,W_("loc")-2.8,"Plex5",8.4,5.6,"left");else dash(X_("loc")+1.6);under("loc")}
    // your own columns
    EXTRA.forEach'''),
('''under(k)});SK=null;color(C.ink);
    if(last)line''','''under(k)});SK=null;color(C.ink);
    if(KI.chk!=null){const x0=X_("chk"),w0=W_("chk"),nb=OPT.chk>1?2:1,bs=3.6,gp=(w0-nb*bs)/(nb+1);stroke(C.ink);doc.setLineWidth(0.3);for(let b=0;b<nb;b++)doc.roundedRect(x0+gp+b*(bs+gp),MID0-bs/2,bs,bs,0.5,0.5,"S")}
    if(last)line'''),
('''rh=n>17?9.6:11.6''','''rh=(n>17?9.6:11.6)*(OPT.dens==="c"?0.84:OPT.dens==="a"?1.2:1)'''),
('''tools:art.tools,cols:printCfg(cfg,art)''','''tools:withLoc(art.tools,cfg),cols:printCfg(cfg,art)'''),
# --- Excel
(''',tools=realTools(art.tools),done=art.status==="done"''',''',tools=realTools(withLoc(art.tools,cfgXlOf(art))),done=art.status==="done"'''),
('''const cell=(t,k)=>{const R0=[],add=(s,f)=>R0.push([R0.length?s:s.replace(/^\\n/,""),f]);''','''const cell=(t,k)=>{const R0=[],add=(s,f)=>R0.push([R0.length?s:s.replace(/^\\n/,""),f]);
    if(k==="chk"){add(Array(O.chk>1?2:1).fill("☐").join("    "),F(XL_SANS,13,0,MID));return{runs:R0}}'''),
('''k==="code"||k==="asm"?F(XL_MONO''','''k==="loc"?F(XL_SANS,8.4):k==="code"||k==="asm"?F(XL_MONO'''),
('''/^(holder|type)$/.test(j)||j.startsWith("x_")?XL_SANS''','''/^(holder|type|loc)$/.test(j)||j.startsWith("x_")?XL_SANS'''),
('''add("\\n"+(li?"":M.hl[j]+" ")''','''add("\\n"+(li?"":(j==="loc"&&M.hl.loc===(LANG==="fr"?"Emplacement":"Location")?(LANG==="fr"?"Empl.":"Loc."):M.hl[j])+" ")'''),
('''h:k==="z"?"center":"left"''','''h:k==="z"||k==="chk"?"center":"left"'''),
# --- editor
('''mlCell(k,x,k.startsWith("x_")?"xcell":k==="holder"?"holdcell":k==="code"?"codecell":"")).join("")}''','''(k==="loc"?`<td class="loccell" data-col="loc">${locTag(x)}</td>`:k==="code"&&locUnderC(sheetCfg())?mlCell(k,x,"codecell").replace(/<\\/td>$/,locTag(x)+"</td>"):mlCell(k,x,k.startsWith("x_")?"xcell":k==="holder"?"holdcell":k==="code"?"codecell":""))).join("")}'''),
('''prOn(cur,k)?"checked":""} tabindex="-1" aria-label="${esc(t("prT")+" : "+colLabel(k))}"></th>`).join("")}''','''prOn(cur,k)?"checked":""} tabindex="-1" aria-label="${esc(t("prT")+" : "+colLabel(k))}">${k==="code"&&locUnderC(sheetCfg())?`<label class="asmpr locpr" title="${esc(t("prT")+" : "+colLabel("loc"))}"><input type="checkbox" class="prck" data-pr="loc" ${prOn(cur,"loc")?"checked":""} tabindex="-1">${esc(t("locShort"))}</label>`:""}</th>`).join("")}'''),
('''k==="asm"?`.tt input[data-k="asm"]{opacity:.5}`:''','''k==="asm"?`.tt input[data-k="asm"]{opacity:.5}`:k==="loc"?`.tt .loctag{opacity:.45}`:'''),
# read-only view has its own "Location" column already
('''edCols(AC).filter(k=>!k.startsWith("x_"))''','''edCols(AC).filter(k=>!k.startsWith("x_")&&k!=="loc")'''),
('''edCols(AC).filter(q=>!q.startsWith("x_"))''','''edCols(AC).filter(q=>!q.startsWith("x_")&&q!=="loc")'''),
# --- tool prep: pick order
('''const rows=realTools(art.tools).filter(x=>clean(x.code));const ok=''','''const rows=prepSort(realTools(art.tools).filter(x=>clean(x.code)),art);const ok='''),
('''<button class="btn sm" id="pp-none">${esc(t("prepNone"))}</button><span class="sp"></span>''','''<button class="btn sm" id="pp-none">${esc(t("prepNone"))}</button>${ppSortBar()}<span class="sp"></span>'''),
# --- search everywhere
('''  <span class="sp"></span>
  <span id="tbar"></span>''','''  <span class="sp"></span>
  <button class="tb gfbtn" id="b-find" hidden></button>
  <span id="tbar"></span>'''),
('''/* ---------- which columns go on the PDF and the Excel ----------''',BLOCK+'''/* ---------- which columns go on the PDF and the Excel ----------'''),
('''minmax(340px,33%))}}
</style>''','''minmax(340px,33%))}}'''+CSS+'''</style>'''),
]
for f in sys.argv[1:]:
  s=open(f).read()
  for r in R:
    a,b=r[0],r[1];n=r[2] if len(r)>2 else 1
    assert s.count(a)==n,(f,s.count(a),a[:90]);s=s.replace(a,b)
  open(f,'w').write(s);print("patched",f)
