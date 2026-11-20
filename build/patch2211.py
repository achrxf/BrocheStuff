import sys
R=[
# the Assembly column can be joined (it was missing from the list, so its join was dropped)
('''const JOINORD=["t","corr",''','''const JOINORD=["t","asm","corr",'''),
('''ORD=["t","corr","type","diameter","ra","insert","ls","oal","z","holder","code",...EXTRA.map(x=>"x_"+x.id)];''','''ORD=["t","asm","corr","type","diameter","ra","insert","ls","oal","z","holder","code",...EXTRA.map(x=>"x_"+x.id)];'''),
# by default the assembly code sits under the tool number (unless a layout gives it its own column)
('''  Object.keys(out).forEach(k=>{if(out[out[k]])delete out[k]});return out}''','''  Object.keys(out).forEach(k=>{if(out[out[k]])delete out[k]});
  if(!(c&&c.asmOwn)&&!out.asm&&!(hidden||[]).includes("asm")&&!Object.values(out).includes("asm"))out.asm="t";
  return out}'''),
('''joinTo:normJoin({joinTo:buf.joinTo},buf.hidden,buf.extra.filter(x=>clean(x.label))),opt:normOpt(buf.opt),style:normStyle(buf.style),order:normOrder(buf.order,buf.extra.filter(x=>clean(x.label))),noprint:''','''joinTo:normJoin({joinTo:buf.joinTo,asmOwn:!buf.joinTo.asm},buf.hidden,buf.extra.filter(x=>clean(x.label))),asmOwn:!buf.joinTo.asm,opt:normOpt(buf.opt),style:normStyle(buf.style),order:normOrder(buf.order,buf.extra.filter(x=>clean(x.label))),noprint:'''),
('''const normCfg=c=>{const n=normCfg0(c);''','''const normCfg=c=>{const n=normCfg0(c);n.asmOwn=!!(c&&c.asmOwn);'''),
# the sheet: a column joined under the tool number is shown in the tool number's cell
('''const visCols=cfg=>{''','''// the columns of the sheet table: the assembly code joined under the tool number sits in its cell
const asmUnderT=cfg=>!!(cfg&&cfg.joinTo&&cfg.joinTo.asm==="t");
const edCols=cfg=>visCols(cfg).filter(k=>!(k==="asm"&&asmUnderT(cfg||LAYCFG)));
const visCols=cfg=>{'''),
('''VCOLS=visCols(LAYCFG).flatMap(''','''VCOLS=edCols(LAYCFG).flatMap('''),
('''<td data-col="t"><input class="m b up" data-k="t" value="${v("t")}" placeholder="T${String(i+1).padStart(2,"0")}">${asmChipHTML(x)}</td>`''','''<td data-col="t"><input class="m b up" data-k="t" value="${v("t")}" placeholder="T${String(i+1).padStart(2,"0")}">${asmUnderT(sheetCfg())?`<input class="m up asmin" data-k="asm" value="${v("asm")}" placeholder="AS…" list="asmcodes" title="${esc(t("colAsm"))}">`:""}</td>`'''),
('''<th class="prlab" title="${esc(t("prT"))}">${esc(t("prShort"))}</th>`''','''<th class="prlab" title="${esc(t("prT"))}">${esc(t("prShort"))}${asmUnderT(sheetCfg())?` <input type="checkbox" class="prck" data-pr="asm" ${prOn(cur,"asm")?"checked":""} tabindex="-1" title="${esc(t("prT")+" : "+colLabel("asm"))}">`:""}</th>`'''),
('''const off=visCols(sheetCfg()).filter(k=>k!=="t"&&!prOn(cur,k));el.textContent=off.map(k=>`.tt td[data-col="${k}"] input{opacity:.5}`).join("")}''','''const off=visCols(sheetCfg()).filter(k=>k!=="t"&&!prOn(cur,k));el.textContent=off.map(k=>k==="asm"?`.tt input[data-k="asm"]{opacity:.5}`:`.tt td[data-col="${k}"] input{opacity:.5}`).join("")}'''),
# read-only view
('''const cells={asm:`<td class="m" data-col="asm">''','''const AT=asmUnderT(AC);const cells={asm:`<td class="m" data-col="asm">'''),
('''t:`<td class="m" data-col="t"><b>${esc(normT(x.t))}</b></td>`,''','''t:`<td class="m" data-col="t"><b>${esc(normT(x.t))}</b>${AT&&clean(x.asm)?`<div class="dim small">${esc(clean(x.asm).toUpperCase())}</div>`:""}</td>`,'''),
('''.tt th .prck{''','''.tt td[data-col="t"] input.asmin{display:block;height:20px!important;margin-top:2px;padding:1px 4px!important;font-size:10px!important;font-weight:600;color:var(--mid);letter-spacing:-.02em}
.tt td[data-col="t"] input.asmin::placeholder{color:var(--ph2);font-weight:400}
.tt td[data-col="t"] input.asmin.warn{color:var(--low-ink)}
.tt thead tr.prrow th.prlab .prck{margin-left:4px}
.tt th .prck{'''),
]
for f in sys.argv[1:]:
  s=open(f).read()
  for a,b in R:
    assert s.count(a)==1,(f,s.count(a),a[:100]);s=s.replace(a,b)
  # every sheet-table use of the columns
  s=s.replace("visCols(sheetCfg()).reduce(","edCols(sheetCfg()).reduce(").replace("<thead><tr>${visCols(sheetCfg()).map(","<thead><tr>${edCols(sheetCfg()).map(").replace('<tr class="prrow">${visCols(sheetCfg()).map(','<tr class="prrow">${edCols(sheetCfg()).map(').replace("    ${visCols(sheetCfg()).map(k=>k===\"t\"?`<td data-col=\"t\">","    ${edCols(sheetCfg()).map(k=>k===\"t\"?`<td data-col=\"t\">")
  s=s.replace("${visCols(AC).filter(k=>!k.startsWith(\"x_\")).map(k=>`<th","${edCols(AC).filter(k=>!k.startsWith(\"x_\")).map(k=>`<th").replace("${visCols(AC).filter(q=>!q.startsWith(\"x_\")).map(q=>cells[q])","${edCols(AC).filter(q=>!q.startsWith(\"x_\")).map(q=>cells[q])")
  open(f,'w').write(s);print("patched",f,s.count("edCols("))
