import sys
FILL=r'''
/* ---------- filling a row from an assembly code or a tool code ----------
   Empty boxes are filled. A box that already holds something else is never changed by itself:
   the differences are shown and you choose which ones to replace. */
Object.assign(I18N.en,{colAsm:"Assembly", fAsm:"Assembly",
  fillT:k=>k==="asm"?"Differences with the assembly":"Differences with the tool card", fillP:(n,lab)=>`${n?`${n} empty ${pl(n,"box","boxes")} will be filled. `:""}These boxes already hold something different from ${lab}. Tick the ones to replace:`,
  fillCol:"Column", fillMine:"In the row", fillAsm:"In the assembly", fillCrib:"In the tool crib", fillRep:"Replace", fillAll:"Tick all", fillGo:"Apply", fillKeep:"Keep my row as it is",
  fillDone:(lab,n,r)=>`${lab}: ${n} ${pl(n,"box","boxes")} filled${r?` · ${r} replaced`:""}`, fillSame:lab=>`${lab}: the row already matches`, fillKept:lab=>`${lab}: row kept as it is (differences remain)`,
  asmDiff:(c,L)=>`Differs from assembly ${c}: ${L}`, asmMissing:c=>`No assembly ${c}`});
Object.assign(I18N.fr,{colAsm:"Assemblage", fAsm:"Assemblage",
  fillT:k=>k==="asm"?"Différences avec l’assemblage":"Différences avec la fiche outil", fillP:(n,lab)=>`${n?`${n} ${pl(n,"case vide sera remplie","cases vides seront remplies")}. `:""}Ces cases contiennent déjà autre chose que ${lab}. Cochez celles à remplacer :`,
  fillCol:"Colonne", fillMine:"Dans la ligne", fillAsm:"Dans l’assemblage", fillCrib:"Au magasin", fillRep:"Remplacer", fillAll:"Tout cocher", fillGo:"Appliquer", fillKeep:"Garder ma ligne telle quelle",
  fillDone:(lab,n,r)=>`${lab} : ${n} ${pl(n,"case remplie","cases remplies")}${r?` · ${r} ${pl(r,"remplacée","remplacées")}`:""}`, fillSame:lab=>`${lab} : la ligne correspond déjà`, fillKept:lab=>`${lab} : ligne gardée telle quelle (des différences restent)`,
  asmDiff:(c,L)=>`Diffère de l’assemblage ${c} : ${L}`, asmMissing:c=>`Pas d’assemblage ${c}`});
const CRIBMAP=[["type","type"],["diameter","diameter"],["ra","ra"],["insert","insert"],["z","z"],["ls","ls"],["oal","oal"]];
const fillSame=(k,a,b)=>{a=clean(a);b=clean(b);if(k==="diameter")return normDia(a)===normDia(b);if(k==="code")return normCode(a)===normCode(b);return asmNv(a.replace(/\n/g," "))===asmNv(b.replace(/\n/g," "))};
// what differs between a row and its assembly (the boxes the assembly fills)
function asmDiffs(x){const a=clean(x.asm)&&asmFind(x.asm);if(!a)return null;return ASMF.filter(k=>clean(a.tool[k])&&!fillSame(k,x[k],a.tool[k]))}
function asmMark(tr){if(!tr||!cur)return;const x=cur.tools[+tr.dataset.i],el=tr.querySelector('input[data-k="asm"]');if(!x||!el)return;
  const v=clean(x.asm),a=v&&asmFind(v),d=a?asmDiffs(x):null;
  el.classList.toggle("bad",!!v&&!a);el.classList.toggle("warn",!!(d&&d.length));
  el.title=v&&!a?t("asmMissing",asmKey(v)||v.toUpperCase()):d&&d.length?t("asmDiff",a.code,d.map(k=>colLabel(k)).join(", ")):""}
function rowFill(i,src,keys,kind,label){const x=cur.tools[i];if(!x)return;const fill=[],clash=[];
  keys.forEach(k=>{const nv=clean(src[k]);if(!nv)return;if(!clean(x[k]))fill.push(k);else if(!fillSame(k,x[k],src[k]))clash.push(k)});
  const done=(rep)=>{fill.forEach(k=>x[k]=String(src[k]).trim());rep.forEach(k=>x[k]=String(src[k]).trim());if(kind==="asm")x.asmAuto=0;renderRows();edited();
    toast(fill.length||rep.length?t("fillDone",label,fill.length,rep.length):clash.length?t("fillKept",label):t("fillSame",label))};
  if(!clash.length){done([]);return}
  const show=(k,v)=>esc(String(v||"").replace(/\n/g," · "))||"—";
  dialog(esc(t("fillT",kind)),`<p style="margin:0 0 10px">${esc(t("fillP",fill.length,label))}</p>
    <div class="tw"><table class="lt filltab"><thead><tr><th>${esc(t("fillCol"))}</th><th>${esc(t("fillMine"))}</th><th>${esc(kind==="asm"?t("fillAsm"):t("fillCrib"))}</th><th>${esc(t("fillRep"))}</th></tr></thead><tbody>
    ${clash.map(k=>`<tr><td><b>${esc(colLabel(k))}</b></td><td class="m mine">${show(k,x[k])}</td><td class="m theirs">${show(k,src[k])}</td><td><label class="chk"><input type="checkbox" data-rep="${k}"></label></td></tr>`).join("")}</tbody></table></div>
    <button class="btn sm ghost" id="fill-all" style="margin-top:8px;align-self:flex-start;width:auto">${esc(t("fillAll"))}</button>`,
    `<button class="btn ghost" id="fill-keep">${esc(t("fillKeep"))}</button><span class="sp"></span><button class="btn red" id="fill-go">${esc(t("fillGo"))}</button>`);
  $(".dlg").classList.add("wide");
  $("#fill-all").onclick=()=>document.querySelectorAll("[data-rep]").forEach(c=>c.checked=true);
  $("#fill-keep").onclick=()=>{closeDlg();done([])};
  $("#fill-go").onclick=()=>{const rep=[...document.querySelectorAll("[data-rep]:checked")].map(c=>c.dataset.rep);closeDlg();done(rep)}}
function cribTool(c){const o={};CRIBMAP.forEach(([tk,ck])=>{if(clean(c[ck]))o[tk]=c[ck]});return o}

/* ---------- 4. reports ---------- */'''
R=[
# the column itself
('''const BASEK=["t","corrH","corrD","type","diameter","ra","insert","ls","oal","z","holder","code"];
const LABK=["t","corr","type","diameter","ra","insert","ls","oal","z","holder","code"];''','''const BASEK=["t","asm","corrH","corrD","type","diameter","ra","insert","ls","oal","z","holder","code"];
const LABK=["t","asm","corr","type","diameter","ra","insert","ls","oal","z","holder","code"];'''),
# layouts saved before: the new column goes right after the tool number
('''keys.forEach(k=>{if(!out.includes(k))out.push(k)});return out};''','''keys.forEach(k=>{if(!out.includes(k)){if(k==="asm")out.unshift(k);else out.push(k)}});return out};'''),
('''const defLabel=k=>({t:t("colTool"),''','''const defLabel=k=>({asm:t("colAsm"),t:t("colTool"),'''),
('''const DEFW={t:50,''','''const DEFW={asm:88,t:50,'''),
('''const ML_ATTR={type:''','''const ML_ATTR={asm:{cls:"m b up",list:"asmcodes",ph:"AS…"},type:'''),
('''const TOOLF0=[["t","fT"],''','''const TOOLF0=[["t","fT"],["asm","fAsm"],'''),
('''  t:["t number","t","tool","outil",''','''  asm:["assemblage","assembly","asm","code assemblage","assembly code","n assemblage"],
  t:["t number","t","tool","outil",'''),
('''<datalist id="codes"></datalist>''','''<datalist id="codes"></datalist><datalist id="asmcodes"></datalist>'''),
# read-only view and the PDF (when a layout puts it under another column)
('''const cells={t:`<td class="m" data-col="t"><b>${esc(normT(x.t))}</b></td>`,''','''const cells={asm:`<td class="m" data-col="asm">${clean(x.asm)?`<b>${esc(clean(x.asm).toUpperCase())}</b>`:`<span class="dim">—</span>`}</td>`,t:`<td class="m" data-col="t"><b>${esc(normT(x.t))}</b></td>`,'''),
('''holder:lab("holder",L.head[6]),code:lab("code",L.head[7])};''','''holder:lab("holder",L.head[6]),code:lab("code",L.head[7]),asm:lab("asm",LANG==="fr"?"Assemblage":"Assembly")};'''),
# editor: no more code under the T number (the column shows it), the list of codes, marks
('''function asmChipHTML(x){const a=asmOfTool(x);return `<button class="asmc" data-asm="${a?esc(a.code):""}" title="${esc(t("asmChipT"))}" tabindex="-1"${a?"":" hidden"}>${a?esc(a.code):""}</button>`}
function asmChips(){const R=$("#rows");if(!R||!cur)return;R.querySelectorAll("tr[data-i]").forEach(tr=>{const x=cur.tools[+tr.dataset.i],b=tr.querySelector(".asmc");if(!x||!b)return;const a=asmOfTool(x);b.hidden=!a;b.dataset.asm=a?a.code:"";b.textContent=a?a.code:""})}''',
 '''function asmChipHTML(x){return ""}
// each finished row shows the code of its assembly (a code typed by hand stays as typed)
function asmLink(art){let ch=0;realTools(art.tools).forEach(x=>{const a=asmOfTool(x);if(!a)return;const v=clean(x.asm),cur0=v&&asmFind(v);
  if(!v||!cur0||(x.asmAuto!==0&&cur0!==a)){if(x.asm!==a.code){x.asm=a.code;x.asmAuto=1;ch++}}});return ch}
function asmChips(){const R=$("#rows");if(!R||!cur)return;R.querySelectorAll("tr[data-i]").forEach(tr=>{const x=cur.tools[+tr.dataset.i],el=tr.querySelector('input[data-k="asm"]');if(!x||!el)return;
  if(document.activeElement!==el)el.value=x.asm||"";asmMark(tr)});const dl=$("#asmcodes");if(dl)dl.innerHTML=asmCodeOptions()}'''),
('''function asmLater(){asmDirty=true;clearTimeout(asmTimer);asmTimer=setTimeout(()=>{if(cur&&asmDirty&&asmSync(cur)){saveDB();asmChips()}},2500)}''',
 '''function asmLater(){asmDirty=true;clearTimeout(asmTimer);asmTimer=setTimeout(()=>{if(cur&&asmDirty){const a=asmSync(cur),b=asmLink(cur);if(a||b){saveDB();asmChips()}}},2500)}'''),
('''function asmBoot(){if(asmDirty&&cur){clearTimeout(asmTimer);if(asmSync(cur))saveDB()}''','''function asmBoot(){if(asmDirty&&cur){clearTimeout(asmTimer);if(asmSync(cur)+asmLink(cur))saveDB()}'''),
('''  db.asmSeeded=1;if(n||db.articles.length)saveDB()}''','''  db.articles.forEach(asmLink);db.asmSeeded=1;if(n||db.articles.length)saveDB()}'''),
# typing a code: assembly or tool card
('''    const as0=asmFind(cur.tools[i].code);if(as0){asmApply(cur.tools[i],as0);renderRows();edited();toast(t("asmFilled",as0.code));return}
    if(asmKey(cur.tools[i].code)){toast(t("asmUnknown",asmKey(cur.tools[i].code)));return}
    if(fillFromCrib(i)){renderRows();edited();toast(t("filled",normCode(cur.tools[i].code)))}});''',
 '''    const x=cur.tools[i],as0=asmFind(x.code);
    // an assembly code typed in the Code box goes to the Assembly column
    if(as0){x.code="";x.asm=as0.code;x.asmAuto=0;rowFill(i,as0.tool,ASMF,"asm",as0.code);return}
    if(asmKey(x.code)){toast(t("asmUnknown",asmKey(x.code)));return}
    const c=C_(x.code);if(c)rowFill(i,cribTool(c),CRIBMAP.map(m=>m[0]),"crib",normCode(c.code))});
  rows.addEventListener("change",e=>{const tr=e.target.closest("tr");if(!tr||e.target.dataset.k!=="asm")return;const i=+tr.dataset.i,x=cur.tools[i],v=clean(x.asm);
    if(!v){x.asmAuto=0;asmMark(tr);return}const a=asmFind(v);
    if(!a){toast(t("asmUnknown",asmKey(v)||v.toUpperCase()));asmMark(tr);return}
    x.asm=a.code;x.asmAuto=0;rowFill(i,a.tool,ASMF,"asm",a.code)});
  rows.addEventListener("input",e=>{if(e.target.dataset.k&&e.target.dataset.k!=="asm"){const tr=e.target.closest("tr");if(tr&&clean(cur.tools[+tr.dataset.i].asm))asmMark(tr)}});'''),
('''function renderRows(focus){$("#rows").innerHTML=cur.tools.map(rowHTML).join("");countTools();''','''function renderRows(focus){$("#rows").innerHTML=cur.tools.map(rowHTML).join("");countTools();if(typeof asmChips==="function")asmChips();'''),
('''
/* ---------- 4. reports ---------- */''',FILL),
('''.asmc{font-size:9px!important;''','''.tt td input.warn{background:var(--low-bg);border-color:var(--low-ink);color:var(--low-ink)}
.tt td input.bad{background:var(--miss-bg);border-color:var(--miss-bd)}
.filltab td.mine{color:var(--mid)}
.filltab td.theirs{font-weight:600}
.filltab td,.filltab th{padding:8px 10px;vertical-align:top}
.asmc{font-size:9px!important;'''),
# guide
('''"Le code s’affiche sous le numéro T de la ligne. Tapez-le dans la case Code d’une autre fiche : toute la ligne se remplit."''','''"La colonne « Assemblage » de la fiche montre le code de chaque ligne. Tapez un code d’assemblage dans cette colonne (ou un code outil dans la colonne Code) : les cases vides se remplissent. Si une case contient déjà autre chose, BrocheStuff montre la différence et ne remplace que ce que vous cochez. Une ligne qui ne correspond plus à son assemblage est surlignée en orange."'''),
('''"The code shows under the row’s T number. Type it in the Code box of another sheet: the whole row fills in."''','''"The sheet’s “Assembly” column shows each row’s code. Type an assembly code in that column (or a tool code in the Code column): the empty boxes fill in. If a box already holds something else, BrocheStuff shows the difference and only replaces what you tick. A row that no longer matches its assembly is shown in orange."'''),
]
for f in sys.argv[1:]:
  s=open(f).read()
  for a,b in R:
    assert s.count(a)==1,(f,s.count(a),a[:100])
    s=s.replace(a,b)
  open(f,'w').write(s);print("patched",f)
