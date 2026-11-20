import sys
R=[('''<div class="card"><h2>${esc(t("repMach"))}</h2><div class="list"><table class="lt">''','''<div class="card"><h2>${esc(t("repMach"))}</h2><div class="list fitlist"><table class="lt">'''),
('''/* the editor keeps room for its table on mid-size screens (a width dragged by hand still wins) */''','''/* tables inside small cards wrap instead of scrolling */
.fitlist table.lt{min-width:0!important;width:100%}.fitlist td,.fitlist th{white-space:normal!important;padding:8px 6px!important}
@media (max-width:1120px) and (min-width:761px){table.logt th,table.logt td{padding-left:6px!important;padding-right:6px!important}}
/* the editor keeps room for its table on mid-size screens (a width dragged by hand still wins) */''')]
for f in sys.argv[1:]:
  s=open(f).read()
  for a,b in R:
    assert s.count(a)==1,(f,s.count(a),a[:80]);s=s.replace(a,b)
  open(f,'w').write(s);print("patched",f)
