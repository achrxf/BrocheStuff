import sys
R=[
# reports: the period note goes under the title instead of squeezing it
('''<div class="card"><h2>${esc(t("repMonths"))} <span class="hint">${esc(t("rep12m"))}</span></h2>${months}</div>''','''<div class="card"><h2>${esc(t("repMonths"))}</h2><p class="hint" style="margin:-4px 0 6px">${esc(t("rep12m"))}</p>${months}</div>'''),
# assemblies: a search hint that fits its box
('''asmQ:"Code d’assemblage, type, Ø, porte-outil, code outil…",''','''asmQ:"Code, type, Ø, porte-outil…",'''),
('''asmQ:"Assembly code, type, Ø, holder, tool code…",''','''asmQ:"Code, type, Ø, holder…",'''),
('''/* tables inside small cards wrap instead of scrolling */''','''/* the same status looks the same on every page */
.st-done .pill{background:var(--done-l);color:var(--done);border:1px solid var(--done-bd)}
.st-progress .pill{background:var(--paper);color:var(--ink);border:1px solid var(--line2)}
.st.st-done .bar i{background:var(--done)}
/* boxes on one row line up even when a label takes two lines */
.grid{align-items:end}
/* tables inside small cards wrap instead of scrolling */'''),
]
for f in sys.argv[1:]:
  s=open(f).read()
  for a,b in R:
    assert s.count(a)==1,(f,s.count(a),a[:80]);s=s.replace(a,b)
  open(f,'w').write(s);print("patched",f)
# phones: #b-print hidden <=480px
