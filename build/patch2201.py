import sys
SUG=r'''
/* a row that fits an assembly: the same → its code goes in by itself; part of it → BrocheStuff offers the code */
Object.assign(I18N.en,{asmSugT:(T,c)=>`${T} fits assembly ${c}`, asmSugUse:c=>`Use ${c}`, asmSugPh:c=>`${c} ?`, asmSugTip:c=>`This row fits assembly ${c}: click, or press Enter, to use it`, asmAutoSet:(T,c)=>`${T}: same as assembly ${c}, code added`});
Object.assign(I18N.fr,{asmSugT:(T,c)=>`${T} correspond à l’assemblage ${c}`, asmSugUse:c=>`Utiliser ${c}`, asmSugPh:c=>`${c} ?`, asmSugTip:c=>`Cette ligne correspond à l’assemblage ${c} : cliquez, ou appuyez sur Entrée, pour l’utiliser`, asmAutoSet:(T,c)=>`${T} : identique à l’assemblage ${c}, code ajouté`});
// the assemblies a row could be: every box the row has is the same in the assembly
function asmFits(x){if(clean(x.asm))return [];const F=ASMF.filter(k=>clean(x[k]));if(!F.some(k=>k==="code"||k==="holder"))return [];
  return asmList().filter(a=>F.every(k=>clean(a.tool[k])&&fillSame(k,x[k],a.tool[k])))}
const ASMNO=new Set();
function asmCheckRow(i,tr){const x=cur&&cur.tools[i];if(!x||clean(x.asm))return;tr=tr||$(`#rows tr[data-i="${i}"]`);
  const exact=asmOfTool(x);
  if(exact){x.asm=exact.code;x.asmAuto=1;asmChips();saveDB();toast(t("asmAutoSet",normT(x.t)||"",exact.code));return}
  const L=asmFits(x);asmChips();if(L.length!==1)return;const a=L[0],key=cur.id+"|"+i+"|"+a.code;if(ASMNO.has(key))return;ASMNO.add(key);
  toast(t("asmSugT",normT(x.t)||"",a.code)+" · "+[a.tool.type,a.tool.diameter?"Ø"+normDia(a.tool.diameter):"",linesOf_(a.tool.holder)[0]].filter(Boolean).join(" · "),{label:t("asmSugUse",a.code),fn:()=>{if(!cur.tools[i]||cur.tools[i]!==x)return;x.asm=a.code;x.asmAuto=0;rowFill(i,a.tool,ASMF,"asm",a.code)}})}

/* ---------- 4. reports ---------- */'''
R=[
('''
/* ---------- 4. reports ---------- */''',SUG),
# open a sheet: its rows get their codes (2.19 / 2.20 sheets included), and once for every sheet after this update
('''function renderEditor(art){fillHolderList(M(art.machineId)?.cone);
  cur=art;''','''function renderEditor(art){fillHolderList(M(art.machineId)?.cone);
  cur=art;if(typeof asmLink==="function"&&asmLink(art))saveDB();'''),
('''function asmBoot(){if(asmDirty&&cur){clearTimeout(asmTimer);if(asmSync(cur)+asmLink(cur))saveDB()}''','''function asmBoot(){if(asmDirty&&cur){clearTimeout(asmTimer);if(asmSync(cur)+asmLink(cur))saveDB()}
  if(db.asmSeeded&&!db.asmLinked&&Array.isArray(db.articles)){db.articles.forEach(asmLink);db.asmLinked=1;saveDB()}'''),
('''  db.articles.forEach(asmLink);db.asmSeeded=1;if(n||db.articles.length)saveDB()}''','''  db.articles.forEach(asmLink);db.asmSeeded=1;db.asmLinked=1;if(n||db.articles.length)saveDB()}'''),
('''out.asmSeeded=m.asmSeeded||t.asmSeeded;if(!out.asmSeeded)delete out.asmSeeded;''','''out.asmSeeded=m.asmSeeded||t.asmSeeded;if(!out.asmSeeded)delete out.asmSeeded;out.asmLinked=m.asmLinked&&t.asmLinked;if(!out.asmLinked)delete out.asmLinked;'''),
# while typing: check the row when a box is left
('''  rows.addEventListener("input",e=>{if(e.target.dataset.k&&e.target.dataset.k!=="asm"){''','''  rows.addEventListener("change",e=>{const k=e.target.dataset.k;if(!k||k==="asm"||k==="t"||k==="corrH"||k==="corrD")return;const tr=e.target.closest("tr");if(!tr)return;const i=+tr.dataset.i;
    setTimeout(()=>{if($("#ov").hidden)asmCheckRow(i)},60)});
  // the suggested code: click it, or Enter in the empty box
  rows.addEventListener("click",e=>{const el=e.target.closest('input[data-k="asm"].sugg');if(!el)return;const tr=el.closest("tr"),i=+tr.dataset.i,x=cur.tools[i],a=asmFind(el.dataset.sugg);if(!a||clean(x.asm))return;e.preventDefault();x.asm=a.code;x.asmAuto=0;rowFill(i,a.tool,ASMF,"asm",a.code)});
  rows.addEventListener("keydown",e=>{if(e.key!=="Enter")return;const el=e.target.closest('input[data-k="asm"].sugg');if(!el||clean(el.value))return;const tr=el.closest("tr"),i=+tr.dataset.i,x=cur.tools[i],a=asmFind(el.dataset.sugg);if(!a)return;e.preventDefault();e.stopImmediatePropagation();x.asm=a.code;x.asmAuto=0;rowFill(i,a.tool,ASMF,"asm",a.code)},true);
  rows.addEventListener("input",e=>{if(e.target.dataset.k&&e.target.dataset.k!=="asm"){'''),
# the box shows the suggestion
('''  if(document.activeElement!==el)el.value=x.asm||"";asmMark(tr)});''','''  if(document.activeElement!==el)el.value=x.asm||"";asmMark(tr);
  const L=clean(x.asm)?[]:asmFits(x),sg=L.length===1?L[0].code:"";el.classList.toggle("sugg",!!sg);if(sg){el.dataset.sugg=sg;el.placeholder=t("asmSugPh",sg);el.title=t("asmSugTip",sg)}else{delete el.dataset.sugg;el.placeholder="AS…";if(!clean(x.asm))el.title=""}});'''),
('''.tt td input.bad{background:var(--miss-bg);border-color:var(--miss-bd)}''','''.tt td input.bad{background:var(--miss-bg);border-color:var(--miss-bd)}
.tt td input.sugg{border:1px dashed var(--low-ink);cursor:pointer}
.tt td input.sugg::placeholder{color:var(--low-ink);opacity:1;font-weight:700}'''),
]
for f in sys.argv[1:]:
  s=open(f).read()
  for a,b in R:
    assert s.count(a)==1,(f,s.count(a),a[:100])
    s=s.replace(a,b)
  open(f,'w').write(s);print("patched",f)
