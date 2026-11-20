import sys
R=[('''<td class="m">${c.done}</td><td style="min-width:120px">${stackBar(c)}</td></tr>`''','''<td class="m">${c.done}</td><td style="min-width:70px;width:34%">${stackBar(c)}</td></tr>`'''),
('''@media (max-width:1120px) and (min-width:761px){table.logt th,table.logt td{padding-left:6px!important;padding-right:6px!important}}''','''@media (max-width:1120px) and (min-width:761px){table.logt th,table.logt td{padding-left:6px!important;padding-right:6px!important}}
/* narrow windows (half a screen): list tables wrap their text instead of scrolling sideways */
@media (max-width:1000px) and (min-width:761px){#view .list table.lt{min-width:0!important;width:100%}#view .list table.lt td,#view .list table.lt th{white-space:normal!important;padding-left:7px!important;padding-right:7px!important;overflow-wrap:anywhere}
  #view .list table.lt .mtag,#view .list table.lt .ast,#view .list table.lt .spill{white-space:nowrap}}
@media (max-width:860px) and (min-width:761px){#view .list table.lt{font-size:12.5px}#view .list table.lt td,#view .list table.lt th{padding-left:5px!important;padding-right:5px!important}#view .list table.lt .btn.sm{padding:0 7px}.ed .tt td input{padding-left:3px;padding-right:3px}}''')]
for f in sys.argv[1:]:
  s=open(f).read()
  for a,b in R:
    assert s.count(a)==1,(f,s.count(a),a[:80]);s=s.replace(a,b)
  open(f,'w').write(s);print("patched",f)
