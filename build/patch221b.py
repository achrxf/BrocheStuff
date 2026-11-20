import sys
# the boxes sit in their own thin row under the column titles (the title row keeps the widths)
R=[
('''<thead><tr class="prrow">${visCols(sheetCfg()).map(k=>k==="t"?`<th class="prlab" title="${esc(t("prT"))}">${esc(t("prShort"))}</th>`:`<th title="${esc(t("prT"))}"><input type="checkbox" class="prck" data-pr="${k}" ${prOn(cur,k)?"checked":""} tabindex="-1" aria-label="${esc(t("prT")+" : "+colLabel(k))}"></th>`).join("")}<th></th></tr><tr>${visCols(sheetCfg()).map(k=>{const w=thW(k),''','''<thead><tr>${visCols(sheetCfg()).map(k=>{const w=thW(k),'''),
('''<th class="actth"></th></tr></thead>''','''<th class="actth"></th></tr><tr class="prrow">${visCols(sheetCfg()).map(k=>k==="t"?`<th class="prlab" title="${esc(t("prT"))}">${esc(t("prShort"))}</th>`:`<th title="${esc(t("prT"))}"><input type="checkbox" class="prck" data-pr="${k}" ${prOn(cur,k)?"checked":""} tabindex="-1" aria-label="${esc(t("prT")+" : "+colLabel(k))}"></th>`).join("")}<th></th></tr></thead>'''),
('''.tt thead tr.prrow th{padding:5px 6px 0;height:auto;border-bottom:0;background-image:none!important;line-height:1}''','''.tt thead tr:first-child th{border-bottom:0}
.tt thead tr.prrow th{padding:0 6px 6px;height:auto;border-bottom:1px solid var(--hair);background-image:none!important;line-height:1}'''),
('''.tt thead tr.prrow+tr th{padding-top:5px}''','''.tt thead tr:first-child th{padding-bottom:4px}'''),
]
for f in sys.argv[1:]:
  s=open(f).read()
  for a,b in R:
    assert s.count(a)==1,(f,s.count(a),a[:90]);s=s.replace(a,b)
  open(f,'w').write(s);print("patched",f)
