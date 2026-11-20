import sys
PR=r'''
/* ---------- which columns go on the PDF and the Excel ----------
   The layout says it for every sheet (Columns window: "PDF / Excel" box); each sheet can change it
   with the box above each column of its tool table. */
Object.assign(I18N.en,{prT:"On the PDF and the Excel", prOn:c=>`“${c}” will be on the PDF and the Excel`, prOff:c=>`“${c}” will not be on the PDF and the Excel`, prLay:"PDF / Excel", prLayT:"Ticked: the column is on the PDF and the Excel of the sheets using this layout (each sheet can still change it above its tool table)"});
Object.assign(I18N.fr,{prT:"Sur le PDF et l’Excel", prOn:c=>`« ${c} » sera sur le PDF et l’Excel`, prOff:c=>`« ${c} » ne sera pas sur le PDF et l’Excel`, prLay:"PDF / Excel", prLayT:"Coché : la colonne est sur le PDF et l’Excel des fiches qui utilisent cette mise en page (chaque fiche peut encore le changer au-dessus de son tableau d’outils)"});
const prDef=(cfg,k)=>!((cfg&&cfg.noprint)||["asm"]).includes(k);
function prOn(art,k,cfg){const P=(art&&art.pr)||{};if(Object.prototype.hasOwnProperty.call(P,k))return !!P[k];return prDef(cfg||cfgOf(art),k)}
// the layout as it is printed: the columns not printed are left out, and nothing is put under them
function printCfg(cfg,art){if(!cfg)return cfg;const keys=[...LABK.filter(k=>k!=="t"),...(cfg.extra||[]).map(x=>xKey(x.id))].filter(k=>!prOn(art,k,cfg));
  if(!keys.length)return cfg;const hidden=[...new Set([...(cfg.hidden||[]),...keys])],joinTo={};
  Object.entries(cfg.joinTo||{}).forEach(([k,to])=>{if(!hidden.includes(k)&&!hidden.includes(to))joinTo[k]=to});
  return{...cfg,hidden,joinTo,join:Object.keys(joinTo)}}
function prStyle(){if(!cur)return;let el=$("#npstyle");if(!el){el=document.createElement("style");el.id="npstyle";document.head.appendChild(el)}
  const off=visCols(sheetCfg()).filter(k=>k!=="t"&&!prOn(cur,k));el.textContent=off.map(k=>`.tt td[data-col="${k}"] input{opacity:.5}`).join("")}

/* ---------- 4. reports ---------- */'''
R=[
('''
/* ---------- 4. reports ---------- */''',PR),
# printed layout used by the PDF, the preview, the automatic PDFs, the print and the Excel
('''tools:art.tools,cols:cfg,stamp:''','''tools:art.tools,cols:printCfg(cfg,art),stamp:'''),
('''function xlData(art){const d=sheetData(art),X=cfgXlOf(art);d.cols=X;''','''function xlData(art){const d=sheetData(art),X=printCfg(cfgXlOf(art),art);d.cols=X;'''),
('''const blankSheet=()=>makePDF({article:{},tools:[],blank:true,cols:sheetCfg()});''','''const blankSheet=()=>makePDF({article:{},tools:[],blank:true,cols:printCfg(sheetCfg(),null)});'''),
# layouts keep the list (the Assembly column is not printed unless asked)
('''opt:normOpt(c&&c.opt),style:normStyle(c&&c.style)});''','''opt:normOpt(c&&c.opt),style:normStyle(c&&c.style),noprint:c&&Array.isArray(c.noprint)?c.noprint.filter(k=>k&&k!=="t"):["asm"]});'''),
('''opt:normOpt(buf.opt),style:normStyle(buf.style),order:normOrder(buf.order,buf.extra.filter(x=>clean(x.label)))});''','''opt:normOpt(buf.opt),style:normStyle(buf.style),order:normOrder(buf.order,buf.extra.filter(x=>clean(x.label))),noprint:[...new Set(buf.noprint||[])].filter(k=>k!=="t")});'''),
('''joinTo:c.joinTo,join:Object.keys(c.joinTo),opt:c.opt,style:c.style,order:c.order}''','''joinTo:c.joinTo,join:Object.keys(c.joinTo),opt:c.opt,style:c.style,order:c.order,noprint:c.noprint}'''),
# Columns window: a "PDF / Excel" box on each column
('''<span class="coltag">${esc(k==="t"?t("colsFirst")''','''<label class="colpr" title="${esc(t("prLayT"))}"><input type="checkbox" data-cpr="${k}" ${k==="t"||!(buf.noprint||[]).includes(k)?"checked":""} ${k==="t"?"disabled":""}> ${esc(t("prLay"))}</label><span class="coltag">${esc(k==="t"?t("colsFirst")'''),
('''B.querySelectorAll("[data-opt]").forEach(c=>c.onchange=()=>{buf.opt[c.dataset.opt]=c.checked});''','''B.querySelectorAll("[data-opt]").forEach(c=>c.onchange=()=>{buf.opt[c.dataset.opt]=c.checked});
    B.querySelectorAll("[data-cpr]").forEach(c=>c.onchange=()=>{const k=c.dataset.cpr;buf.noprint=(buf.noprint||[]).filter(x=>x!==k);if(!c.checked)buf.noprint.push(k)});'''),
# the sheet: a box above each column
('''return `<th data-ck="${k}"${w?` style="width:${w}px"`:""}${ttl?` title="${esc(ttl)}"`:""}${k.startsWith("x_")?' class="xth"':""}>${esc(colLabel(k))}''','''return `<th data-ck="${k}"${w?` style="width:${w}px"`:""}${ttl?` title="${esc(ttl)}"`:""} class="${k.startsWith("x_")?"xth":""}${k!=="t"&&!prOn(cur,k)?" np":""}">${k!=="t"?`<input type="checkbox" class="prck" data-pr="${k}" ${prOn(cur,k)?"checked":""} title="${esc(t("prT"))}" tabindex="-1">`:""}${esc(colLabel(k))}'''),
('''  renderRows();checkDup();
  const rows=$("#rows");''','''  renderRows();checkDup();prStyle();
  $(".tt thead").addEventListener("change",e=>{const c=e.target.closest("[data-pr]");if(!c)return;const k=c.dataset.pr,def=prDef(cfgOf(cur),k);
    const P={...(cur.pr||{})};if(c.checked===def)delete P[k];else P[k]=c.checked;if(Object.keys(P).length)cur.pr=P;else delete cur.pr;
    c.closest("th").classList.toggle("np",!c.checked);prStyle();edited();toast(t(c.checked?"prOn":"prOff",colLabel(k)))});
  $(".tt thead").addEventListener("pointerdown",e=>{if(e.target.closest("[data-pr]"))e.stopPropagation()},true);
  const rows=$("#rows");'''),
# the PDF can print the Assembly column
('''                   :[["t",11],["corr",12],["type",62],''','''                   :[["t",11],["asm",17],["corr",12],["type",62],'''),
('''const SPEC=(BLANK?[["t",10],["corr",13],''','''const SPEC=(BLANK?[["t",10],["asm",15],["corr",13],'''),
('''  const SPW=Object.fromEntries([["t",11],["corr",12],''','''  const SPW=Object.fromEntries([["t",11],["asm",17],["corr",12],'''),
('''    if(KI.code!=null){at("code");''','''    if(KI.asm!=null){at("asm");useK("asm");const av=linesOf(t.asm).map(v=>v.toUpperCase());if(av.length)stack(av,X_("asm")+1.6,W_("asm")-2.8,"MonoB",9,6,"left",-0.1);else dash(X_("asm")+1.6);under("asm")}
    if(KI.code!=null){at("code");'''),
# the Excel: like the code
('''const base=k==="ls"?F(XL_MONO,11,1):k==="code"?F(XL_MONO,9.5,1):''','''const base=k==="ls"?F(XL_MONO,11,1):k==="code"||k==="asm"?F(XL_MONO,k==="asm"?9:9.5,1):'''),
# style
('''.tt td input.sugg{''','''.tt th .prck{width:13px;height:13px;margin:0 5px 0 0;vertical-align:-2px;accent-color:var(--red);cursor:pointer}
.tt th.np{color:var(--soft);text-decoration:line-through;text-decoration-color:var(--soft)}
.colpr{display:inline-flex;align-items:center;gap:4px;font-size:12px;color:var(--mid);white-space:nowrap;margin-right:6px}
.colpr input{accent-color:var(--red)}
.tt td input.sugg{'''),
# guide
('''["sort","Trier une fiche",''','''["print","Colonnes sur le PDF et l’Excel",["Chaque colonne du tableau d’outils a une case au-dessus : cochée, la colonne est sur le PDF et l’Excel de cette fiche ; décochée, elle reste dans la fiche mais n’est pas imprimée.","Par défaut, la case suit la mise en page (bouton Colonnes, case « PDF / Excel » de chaque colonne). La colonne Assemblage n’est pas imprimée par défaut."]],
   ["sort","Trier une fiche",'''),
('''["sort","Sorting a sheet",''','''["print","Columns on the PDF and the Excel",["Each column of the tools table has a box above it: ticked, the column is on this sheet’s PDF and Excel; unticked, it stays in the sheet but is not printed.","By default the box follows the layout (Columns button, “PDF / Excel” box of each column). The Assembly column is not printed by default."]],
   ["sort","Sorting a sheet",'''),
]
for f in sys.argv[1:]:
  s=open(f).read()
  for a,b in R:
    n=2 if a.startswith("joinTo:c.joinTo,join:") else 1
    assert s.count(a)==n,(f,s.count(a),a[:100])
    s=s.replace(a,b)
  open(f,'w').write(s);print("patched",f)
