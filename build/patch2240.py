import sys
# 2.24.0: easier to use everywhere — sticky column titles, drawing can be hidden, locations easy to fill and to find
# (crib filter, "+ location" in the crib, location on the tool card), pick list and location labels to print,
# calmer PDF boxes, designation in article lists, tidier toolbars, R typed in lower case fixed, small dialog fixes.
IMPORT_ICON='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12M7 10l5 5 5-5M4 17v3h16v-3"/></svg>'
NC_ICON='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 3H6v18h12V7z"/><path d="M14 3v4h4M9.5 12.5 8 14l1.5 1.5M14.5 12.5 16 14l-1.5 1.5"/></svg>'
BLOCK=r'''/* ---------- 2.24: easier to use ---------- */
Object.assign(I18N.en,{tdHide:"Hide the drawing",tdShow:"Show the drawing",fNoLoc:"No location",locAddT:"Add where this tool is kept",
  ppPrint:"Print the list",ppPrintT:"Print this list to take to the tool crib (in the order shown)",ppHead:"Tool prep",ppBy:"Prepared by",ppDate:"Date",ppQty:"Qty",
  lblBtn:"Location labels",lblBtnT:"Print a label for each shelf or drawer, with the tools kept there",lblT:"Location labels",lblP:"One label per location with the tools and holders kept there. Stick them on the shelves and drawers.",
  lblFilter:"Filter the locations…",lblAll:"All",lblNone:"None",lblPrint:n=>`Print ${n} label${n>1?"s":""}`,lblNone0:"No tool has a location yet. Add them in the tool crib (filter “No location”) or straight from a tool sheet.",
  lblN:n=>`${n} item${n>1?"s":""}`,lblMore:n=>`+ ${n} more`,emptyNC:"Read CNC programs",emptyImp:"Import a file"});
Object.assign(I18N.fr,{tdHide:"Masquer le schéma",tdShow:"Afficher le schéma",fNoLoc:"Sans emplacement",locAddT:"Ajouter l’endroit où l’outil est rangé",
  ppPrint:"Imprimer la liste",ppPrintT:"Imprimer cette liste pour aller au magasin (dans l’ordre affiché)",ppHead:"Préparation des outils",ppBy:"Préparé par",ppDate:"Date",ppQty:"Qté",
  lblBtn:"Étiquettes d’emplacement",lblBtnT:"Imprimer une étiquette par étagère ou tiroir, avec les outils qui y sont rangés",lblT:"Étiquettes d’emplacement",lblP:"Une étiquette par emplacement avec les outils et porte-outils qui y sont rangés. À coller sur les étagères et les tiroirs.",
  lblFilter:"Filtrer les emplacements…",lblAll:"Tous",lblNone:"Aucun",lblPrint:n=>`Imprimer ${n} étiquette${n>1?"s":""}`,lblNone0:"Aucun outil n’a encore d’emplacement. Ajoutez-les dans le magasin outils (filtre « Sans emplacement ») ou directement depuis une fiche outils.",
  lblN:n=>`${n} élément${n>1?"s":""}`,lblMore:n=>`+ ${n} autres`,emptyNC:"Lire des programmes CN",emptyImp:"Importer un fichier"});
// the tool drawing above the sheet can be hidden (remembered on this PC)
const tdOff=()=>lsGet("bs.tdoff")==="1";
const tdBtn=()=>`<button type="button" class="btn sm ghost tdtog" id="b-tdtog" aria-pressed="${!tdOff()}">${esc(t(tdOff()?"tdShow":"tdHide"))}</button>`;
document.body.classList.toggle("td-off",tdOff());
document.addEventListener("click",e=>{const b=e.target.closest&&e.target.closest("#b-tdtog");if(!b)return;lsSet("bs.tdoff",tdOff()?"0":"1");document.body.classList.toggle("td-off",tdOff());b.outerHTML=tdBtn();requestAnimationFrame(()=>{try{ttFit()}catch(_){}})});
// "r1" typed in the R / angle box becomes "R1" (like on the PDF)
document.addEventListener("change",e=>{const i=e.target;if(!i||!i.matches||!i.matches('#rows input[data-k="ra"]'))return;const v=i.value,n=v.replace(/^\s*r\s*(?=\d)/i,"R").replace(/(\d)\s*°/,"$1°");if(n!==v){i.value=n;i.dispatchEvent(new Event("input",{bubbles:true}))}},true);
// locations from anywhere: crib list, tool card
document.addEventListener("click",e=>{const b=e.target.closest&&e.target.closest("[data-locc]");if(!b)return;e.preventDefault();e.stopPropagation();locDialog(b.dataset.locc)},true);
function afterLoc(){try{if($("#crows"))drawCrib();if(route&&route.view==="code"&&$(".codehead"))render()}catch(_){}}
function codeLocChip(c){const L=clean(c.location),ed=hasRight("cribEdit");
  if(L)return ed?`<button type="button" class="codeloc" data-locc="${esc(c.code)}" title="${esc(t("locTip"))}">${pinIcon}<span>${esc(L)}</span></button>`:`<span class="codeloc ro">${pinIcon}<span>${esc(L)}</span></span>`;
  return ed?`<button type="button" class="codeloc add" data-locc="${esc(c.code)}" title="${esc(t("locAddT"))}">${pinIcon}<span>${esc(t("locAdd"))}</span></button>`:`<span class="codeloc none">${esc(t("locNone"))}</span>`}
document.addEventListener("input",e=>{if(e.target&&e.target.id==="cf-location"){const c=route&&route.view==="code"?C_(route.code||route.id||""):null,h=$(".codehead .codeloc");if(h&&c)h.outerHTML=codeLocChip(c)}});
// the pick list, printed in the order shown in the tool prep window
function printPick(){const art=ppArt;if(!art)return;const rows=prepSort(realTools(art.tools).filter(x=>clean(x.code)),art),A0=art.article||{},m=M(art.machineId);
  const qty=[...document.querySelectorAll("#ov input.ppq")].map(i=>i.value);
  const tr=rows.map((x,i)=>{const code=linesOf_(x.code)[0]||"",c=C_(code),loc=locLines(x,{opt:{locH:1}});
    return `<tr><td class="bx"><i></i></td><td class="loc">${loc?loc.split("\n").map((l,j)=>j?`<div class="sub2">${esc(l)}</div>`:esc(l)).join(""):"<span class=dim>—</span>"}</td><td class="m b">${esc(clean(x.t))}</td><td class="m b">${esc(normCode(code))}</td><td>${esc([clean(x.type).toUpperCase(),normDia(x.diameter)?"Ø"+normDia(x.diameter):"",raLabel(x.ra)].filter(Boolean).join(" "))}</td><td class="m">${esc(clean(x.ls))}</td><td>${esc(splitHolders(x.holder).join(" + "))}</td><td class="m c">${esc(qty[i]||"1")}</td><td class="m c">${c?(+c.stock||0):"—"}</td></tr>`}).join("");
  const css=`body{font:11px/1.35 "Segoe UI",Arial,sans-serif;color:#111;padding:12mm}h1{font-size:18px;margin:0 0 2px}.sub{color:#555;margin:0 0 10px}
    table{width:100%;border-collapse:collapse}th{font-size:9px;text-transform:uppercase;letter-spacing:.05em;color:#555;text-align:left;border-bottom:1.5px solid #111;padding:5px 6px}
    td{padding:7px 6px;border-bottom:1px solid #ccc;vertical-align:middle}.m{font-family:Consolas,"Courier New",monospace}.b{font-weight:700}.c{text-align:center}.loc{font-weight:700;font-size:12px}
    .sub2{font-size:9.5px;font-weight:400;color:#555;margin-top:1px}.bx i{display:block;width:12px;height:12px;border:1.5px solid #111;border-radius:2px}.dim{color:#999;font-weight:400}tr{break-inside:avoid}
    .foot{display:flex;gap:30px;margin-top:18px}.foot div{flex:1;border-top:1px solid #111;padding-top:4px;color:#555}`;
  printHTML({css,body:`<h1>${esc(t("ppHead"))} · ${esc(A0.number||"")}${A0.index?" "+esc(A0.index):""}</h1><p class="sub">${esc([m?mLabel(m):"",clean(A0.designation),clean(A0.program)].filter(Boolean).join(" · "))} · ${esc(new Date().toLocaleDateString(LANG==="fr"?"fr-FR":"en-GB"))}</p>
    <table><thead><tr><th></th><th>${esc(t("colLoc"))}</th><th>T</th><th>${esc(t("colCode"))}</th><th>${esc(t("colType"))}</th><th>LS</th><th>${esc(t("colHolder"))}</th><th>${esc(t("ppQty"))}</th><th>${esc(t("cStock"))}</th></tr></thead><tbody>${tr}</tbody></table>
    <div class="foot"><div>${esc(t("ppBy"))}</div><div>${esc(t("ppDate"))}</div></div>`},false)}
document.addEventListener("click",e=>{if(e.target.closest&&e.target.closest("#pp-print")){e.preventDefault();printPick()}});
// location labels: one per shelf / drawer with what is kept there
function locGroups(){const G=new Map(),add=(loc,item)=>{const k=clean(loc);if(!k)return;if(!G.has(k))G.set(k,[]);G.get(k).push(item)};
  (db.catalog||[]).forEach(c=>add(c.location,{k:"c",code:c.code,txt:[c.type,c.diameter?"Ø"+normDia(c.diameter):"",raLabel(c.ra)].filter(Boolean).join(" ")}));
  (db.holders||[]).forEach(h=>add(h.location,{k:"h",code:h.ref,txt:[t("locHol"),h.type].filter(Boolean).join(" · ")}));
  return [...G.entries()].sort((a,b)=>a[0].localeCompare(b[0],undefined,{numeric:true,sensitivity:"base"})).map(([loc,items])=>({loc,items:items.sort((a,b)=>(a.k>b.k)-(a.k<b.k)||String(a.code).localeCompare(String(b.code),undefined,{numeric:true}))}))}
function labelsDialog(){const G=locGroups();
  if(!G.length){dialog(esc(t("lblT")),`<p class="note" style="margin:0">${esc(t("lblNone0"))}</p>`,`<button class="btn red" id="d-cancel">${esc(t("close"))}</button>`);$("#d-cancel").onclick=closeDlg;return}
  const sel=new Set(G.map(g=>g.loc));
  dialog(esc(t("lblT")),`<p class="note" style="margin:0 0 10px">${esc(t("lblP"))}</p>
    <div class="lblbar"><div class="search">${searchIcon}<input id="lb-q" type="search" placeholder="${esc(t("lblFilter"))}" autocomplete="off"></div><button class="btn sm" id="lb-all">${esc(t("lblAll"))}</button><button class="btn sm" id="lb-none">${esc(t("lblNone"))}</button></div>
    <div class="lbllist" id="lb-list">${G.map((g,i)=>`<label class="lblrow" data-l="${esc(g.loc.toLowerCase())}"><input type="checkbox" data-lb="${i}" checked><span class="lbn">${pinIcon}<b>${esc(g.loc)}</b></span><span class="dim small">${esc(t("lblN",g.items.length))}</span></label>`).join("")}</div>`,
    `<button class="btn ghost" id="d-cancel">${esc(t("cancel"))}</button><button class="btn red" id="lb-ok"></button>`);
  $(".dlg").classList.add("wide");
  const upd=()=>{$("#lb-ok").textContent=t("lblPrint",sel.size);$("#lb-ok").disabled=!sel.size};upd();
  $("#lb-list").onchange=e=>{const i=+e.target.dataset.lb;if(e.target.checked)sel.add(G[i].loc);else sel.delete(G[i].loc);upd()};
  const vis=()=>[...document.querySelectorAll("#lb-list .lblrow")].filter(r=>!r.hidden);
  $("#lb-q").oninput=e=>{const q=e.target.value.trim().toLowerCase();document.querySelectorAll("#lb-list .lblrow").forEach(r=>r.hidden=!!q&&!r.dataset.l.includes(q))};
  $("#lb-all").onclick=()=>{vis().forEach(r=>{const c=r.querySelector("input");c.checked=true;sel.add(G[+c.dataset.lb].loc)});upd()};
  $("#lb-none").onclick=()=>{vis().forEach(r=>{const c=r.querySelector("input");c.checked=false;sel.delete(G[+c.dataset.lb].loc)});upd()};
  $("#d-cancel").onclick=closeDlg;
  $("#lb-ok").onclick=()=>{const L=G.filter(g=>sel.has(g.loc)),MAX=14;closeDlg();
    const css=`body{font:10px/1.3 "Segoe UI",Arial,sans-serif;color:#111;padding:8mm}.grid{display:grid;grid-template-columns:1fr 1fr;gap:5mm}
      .lb{border:1.5px solid #111;border-radius:3mm;padding:4mm 5mm;break-inside:avoid;min-height:38mm}.lb h2{font-size:22px;margin:0 0 3mm;letter-spacing:-.01em;border-bottom:1px solid #111;padding-bottom:2mm}
      .it{display:flex;gap:3mm;padding:.6mm 0}.it b{font-family:Consolas,"Courier New",monospace;min-width:14mm}.it span{color:#333;overflow:hidden;white-space:nowrap;text-overflow:ellipsis}.more{color:#666;margin-top:1mm}`;
    printHTML({css,body:`<div class="grid">${L.map(g=>`<div class="lb"><h2>${esc(g.loc)}</h2>${g.items.slice(0,MAX).map(it=>`<div class="it"><b>${esc(it.code)}</b><span>${esc(it.txt)}</span></div>`).join("")}${g.items.length>MAX?`<div class="more">${esc(t("lblMore",g.items.length-MAX))}</div>`:""}</div>`).join("")}</div>`},false)}}
document.addEventListener("click",e=>{if(e.target.closest&&e.target.closest("#b-labels")){e.preventDefault();labelsDialog()}});

'''
CSS=r'''
/* 2.24 */
.top .gfbtn kbd{border-color:currentColor!important;color:inherit!important;opacity:.55}
.ed .card h2:has(.tdtog) .hint{margin-left:auto}
.ed .card h2 .tdtog{margin-left:4px;font:500 12.5px/1 var(--body);letter-spacing:0;text-transform:none}
.ed .card h2:has(.tdtog){display:flex;align-items:center;gap:8px}
body.td-off .ed .tdiag.wide{display:none}
@media (min-width:761px){
  .ed .tw.fit{overflow:visible}
  .ed .tw.fit .tt thead th{position:sticky;top:var(--stk,0px);z-index:4;background-color:var(--thbg)}
  .ed .tw.fit .tt thead th:first-child{z-index:5}
  .ed .tw.fit .tt thead tr.prrow th{top:calc(var(--stk,0px) + var(--th1,36px));box-shadow:0 1px 0 var(--hair)}
  .ed .tw.fit .tt thead tr:first-child th{box-shadow:none}
}
.tt thead .prck{accent-color:var(--mid);opacity:.8;cursor:pointer}
.tt thead .prck:not(:checked){opacity:1}
.tt thead tr.prrow .asmpr input{accent-color:var(--mid)}
table.lt .ades{max-width:280px;margin-top:1px;font-size:12.5px}
.btn.ib2{display:inline-flex;align-items:center;gap:7px}.btn.ib2 svg{width:15px;height:15px;flex:0 0 auto}
.chip.c-noloc b{color:var(--mid)}
.locadd{display:inline-flex;align-items:center;gap:4px;padding:3px 8px 3px 6px;border:1px dashed var(--hair);border-radius:999px;background:transparent;color:var(--mid);font:500 12.5px/1.2 var(--body);cursor:pointer;white-space:nowrap}
.locadd svg{width:12px;height:12px}.locadd:hover{border-color:var(--red);color:var(--red)}
.ploc{font-weight:600}
.ploc:not(.none)::before{content:"";display:inline-block;width:12px;height:12px;margin:0 5px -1px 0;background:var(--red);-webkit-mask:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2.4' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M12 21s-6.5-5.7-6.5-11a6.5 6.5 0 0 1 13 0c0 5.3-6.5 11-6.5 11Z'/%3E%3Ccircle cx='12' cy='10' r='2.3'/%3E%3C/svg%3E") center/contain no-repeat;mask:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2.4' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M12 21s-6.5-5.7-6.5-11a6.5 6.5 0 0 1 13 0c0 5.3-6.5 11-6.5 11Z'/%3E%3Ccircle cx='12' cy='10' r='2.3'/%3E%3C/svg%3E") center/contain no-repeat}
.ploc.none{color:var(--soft);font-weight:400}
button.locedit{border:0;background:none;padding:0;margin:0;color:inherit;font:inherit;font-weight:600;cursor:pointer;text-align:left;max-width:100%}button.locedit:hover{color:var(--red);text-decoration:underline}
.codehead{flex-wrap:wrap}
.codeloc{display:inline-flex;align-items:center;gap:7px;align-self:center;padding:9px 16px 9px 12px;border:1.5px solid var(--hair);border-radius:12px;background:var(--paper);color:var(--ink);font:700 17px/1.1 var(--body);cursor:pointer;white-space:nowrap;max-width:100%}
.codeloc svg{width:18px;height:18px;color:var(--red);flex:0 0 auto}.codeloc span{overflow:hidden;text-overflow:ellipsis}
button.codeloc:hover{border-color:var(--ink)}
.codeloc.add{border-style:dashed;color:var(--mid);font-weight:600;font-size:15px}.codeloc.add svg{color:var(--mid)}button.codeloc.add:hover{color:var(--red);border-color:var(--red)}button.codeloc.add:hover svg{color:var(--red)}
.codeloc.ro{cursor:default}.codeloc.none{border:0;background:none;color:var(--soft);font-weight:400;font-size:14px;cursor:default}
.lblbar{display:flex;gap:8px;align-items:center;margin-bottom:10px}.lblbar .search{flex:1}
.lbllist{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:6px;max-height:min(420px,52vh);overflow:auto;padding:2px}
.lblrow{display:flex;align-items:center;gap:8px;padding:8px 10px;border:1px solid var(--hair);border-radius:10px;cursor:pointer}
.lblrow[hidden]{display:none}.lblrow:has(input:checked){border-color:var(--ink)}
.lblrow .lbn{display:inline-flex;align-items:center;gap:5px;flex:1;min-width:0}.lblrow .lbn b{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.lblrow svg{width:13px;height:13px;color:var(--red);flex:0 0 auto}
.empty .actions2 .btn svg{width:15px;height:15px}
.dlg .grid{align-items:start}
'''
R=[
# drawing toggle in the tools card title
('''<h2>${esc(t("tools"))} <span class="hint" id="count"></span></h2>''','''<h2>${esc(t("tools"))} <span class="hint" id="count"></span>${tdBtn()}</h2>'''),
# sticky titles when the table fits
('''tb.style.minWidth=need>avail?need+"px":"0px";tb.style.width="100%"}''','''tb.style.minWidth=need>avail?need+"px":"0px";tb.style.width="100%";
  tw.classList.toggle("fit",need<=avail);const r1=tb.querySelector("thead tr");if(r1)tw.style.setProperty("--th1",r1.offsetHeight+"px");const sp=tw.closest(".form");if(sp)tw.style.setProperty("--stk",-parseFloat(getComputedStyle(sp).paddingTop||0)+"px")}'''),
# designation under the article number
('''<td class="cl"><span class="clip an ${ar.number?"":"none"}" title="${esc(ar.number||"")}">${esc(ar.number||t("noNumber"))}</span></td>''','''<td class="cl"><span class="clip an ${ar.number?"":"none"}" title="${esc(ar.number||"")}">${esc(ar.number||t("noNumber"))}</span>${clean(ar.designation)?`<div class="clip dim ades" title="${esc(ar.designation)}">${esc(ar.designation)}</div>`:""}</td>'''),
# tidier toolbars
('''<button class="btn" id="b-impa" title="${esc(t("impT"))}">${esc(t("imp"))}</button><button class="btn" id="b-impnc" title="${esc(t("impNCP"))}">${esc(t("impNC"))}</button>''','''<button class="btn ghost ib2" id="b-impa" title="${esc(t("impT"))}">'''+IMPORT_ICON+'''${esc(t("imp"))}</button><button class="btn ghost ib2" id="b-impnc" title="${esc(t("impNCP"))}">'''+NC_ICON+'''${esc(t("impNC"))}</button>'''),
('''<button class="btn" id="b-impc" title="${esc(t("impT"))}">${esc(t("imp"))}</button>''','''<button class="btn ghost ib2" id="b-impc" title="${esc(t("impT"))}">'''+IMPORT_ICON+'''${esc(t("imp"))}</button><button class="btn ghost ib2" id="b-labels" title="${esc(t("lblBtnT"))}">${pinIcon}${esc(t("lblBtn"))}</button>'''),
('''<button class="btn" id="b-impm" title="${esc(t("impT"))}">${esc(t("imp"))}</button>''','''<button class="btn ghost ib2" id="b-impm" title="${esc(t("impT"))}">'''+IMPORT_ICON+'''${esc(t("imp"))}</button>'''),
# empty machine: the quickest ways in
('''<button class="btn red" id="newa2">${esc(t("newArticle"))}</button></div>`;$("#newa2").onclick=()=>newArticle(m);return}''','''<div class="actions2"><button class="btn red" id="newa2">${esc(t("newArticle"))}</button><button class="btn ib2" id="nca2" title="${esc(t("impNCP"))}">'''+NC_ICON+'''${esc(t("emptyNC"))}</button><button class="btn ib2" id="ima2">'''+IMPORT_ICON+'''${esc(t("emptyImp"))}</button></div></div>`;$("#newa2").onclick=()=>newArticle(m);$("#nca2").onclick=()=>importPrograms(m);$("#ima2").onclick=()=>startImport("articles",{machineId:m.id});return}'''),
# machine dialog: "why / until when" only when the machine is stopped
('''<label class="f c6">${esc(t("downWhy"))}<input id="d-downwhy"''','''<label class="f c6" id="d-whyl" ${m&&m.down?"":"hidden"}>${esc(t("downWhy"))}<input id="d-downwhy"'''),
('''const err=x=>{$("#d-err").textContent=x;$("#d-err").hidden=false};
  const ok=()=>{const abbr=$("#d-abbr")''','''const err=x=>{$("#d-err").textContent=x;$("#d-err").hidden=false};
  $("#d-down").onchange=()=>{$("#d-whyl").hidden=!$("#d-down").checked;if($("#d-down").checked)$("#d-downwhy").focus()};
  const ok=()=>{const abbr=$("#d-abbr")'''),
# crib: "No location" filter and "+ location" in the list
('''missing:missing.length};''','''missing:missing.length,noloc:cat.filter(c=>!clean(c.location)).length};''',1,'function drawCrib(){'),
('''[["all",t("fAll")],["low",t("fLow")],["out",t("fOut")],["missing",t("fMissing")]]''','''[["all",t("fAll")],["low",t("fLow")],["out",t("fOut")],["noloc",t("fNoLoc")],["missing",t("fMissing")]]''',1,'function drawCrib(){'),
('''cat.filter(c=>(cribF==="all"||stockState(c)===cribF)&&''','''cat.filter(c=>(cribF==="all"||(cribF==="noloc"?!clean(c.location):stockState(c)===cribF))&&'''),
('''<td class="cl"><span class="clip" title="${esc(c.location)}">${esc(c.location)}</span></td>''','''<td class="cl">${clean(c.location)?(hasRight("cribEdit")?`<button type="button" class="clip ploc locedit" data-locc="${esc(c.code)}" title="${esc(t("locTip"))}">${esc(c.location)}</button>`:`<span class="clip ploc" title="${esc(c.location)}">${esc(c.location)}</span>`):hasRight("cribEdit")?`<button type="button" class="locadd" data-locc="${esc(c.code)}" title="${esc(t("locAddT"))}">${pinIcon}${esc(t("locAdd"))}</button>`:""}</td>'''),
# tool card: where it is, big, at the top
('''<span class="bigcode">${esc(c.code)}</span><div>''','''<span class="bigcode">${esc(c.code)}</span>${codeLocChip(c)}<div>'''),
# production / read-only sheet: the location stands out
('''<span class="clip ploc">${esc(c&&c.location||"—")}</span>''','''<span class="clip ploc${c&&clean(c.location)?"":" none"}">${esc(c&&c.location||"—")}</span>'''),
('''<span class="clip ploc">${esc(c.location||"—")}</span>''','''<span class="clip ploc${clean(c.location)?"":" none"}">${esc(c.location||"—")}</span>'''),
('''<span class="clip ploc">${esc(h.location||"—")}</span>''','''<span class="clip ploc${clean(h.location)?"":" none"}">${esc(h.location||"—")}</span>'''),
('''<span class="clip ploc">${esc(c&&c.location||"")}</span>''','''<span class="clip ploc${c&&clean(c.location)?"":" none"}">${esc(c&&c.location||"")}</span>'''),
# location dialog refreshes the crib / tool card too
('''toast(t("locSaved",K,v))};''','''toast(t("locSaved",K,v));afterLoc()};'''),
# tool prep: print the list
('''${ppSortBar()}<span class="sp"></span>''','''${ppSortBar()}<span class="sp"></span><button type="button" class="btn sm ghost ib2" id="pp-print" title="${esc(t("ppPrintT"))}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9V3h12v6M6 18H4v-7h16v7h-2M7 14h10v7H7z"/></svg>${esc(t("ppPrint"))}</button>'''),
('''/* ---------- which columns go on the PDF and the Excel ----------''',BLOCK+'''/* ---------- which columns go on the PDF and the Excel ----------'''),
('''@media (max-width:520px){.top .gfbtn{display:none}}''','''@media (max-width:520px){.top .gfbtn{display:none}}'''+CSS),
]
for f in sys.argv[1:]:
  s=open(f).read()
  for r in R:
    a,b=r[0],r[1];n=r[2] if len(r)>2 else 1;after=r[3] if len(r)>3 else None
    if after:
      p=s.find(after);assert p>=0,(f,after);q=s.find(a,p);assert q>=0,(f,a[:80]);s=s[:q]+b+s[q+len(a):]
    else:
      assert s.count(a)==n,(f,s.count(a),a[:90]);s=s.replace(a,b)
  open(f,'w').write(s);print("patched",f)
