import sys
R=[
('''function markMissing(){document.querySelectorAll("#rows tr").forEach(tr=>{''','''// the same tool number twice in a sheet (T1 and T01 are the same)
function tDupMark(){if(!cur)return;const n=new Map();cur.tools.forEach(x=>{const k=normT(x.t);if(k&&realTools([x]).length)n.set(k,(n.get(k)||0)+1)});
  document.querySelectorAll("#rows tr[data-i]").forEach(tr=>{const x=cur.tools[+tr.dataset.i],el=tr.querySelector('input[data-k="t"]');if(!x||!el)return;const d=(n.get(normT(x.t))||0)>1&&realTools([x]).length>0;
    el.classList.toggle("warn",d);el.title=d?t("tDup",normT(x.t)):""})}
function markMissing(){tDupMark();document.querySelectorAll("#rows tr").forEach(tr=>{'''),
('''  rows.addEventListener("input",e=>{if(e.target.dataset.k&&e.target.dataset.k!=="asm"){''','''  rows.addEventListener("input",e=>{if(e.target.dataset.k==="t")tDupMark()});
  rows.addEventListener("input",e=>{if(e.target.dataset.k&&e.target.dataset.k!=="asm"){'''),
('''prT:"On the PDF and the Excel", prShort:"PDF",''','''prT:"On the PDF and the Excel", prShort:"PDF", tDup:T=>`${T} is used twice in this sheet`,'''),
('''prT:"Sur le PDF et l’Excel", prShort:"PDF",''','''prT:"Sur le PDF et l’Excel", prShort:"PDF", tDup:T=>`${T} est utilisé deux fois dans cette fiche`,'''),
]
for f in sys.argv[1:]:
  s=open(f).read()
  for a,b in R:
    assert s.count(a)==1,(f,s.count(a),a[:80]);s=s.replace(a,b)
  open(f,'w').write(s);print("patched",f)
