import sys
R=[('''@media (max-width:600px){.gfkeys{display:none}.gfloc{max-width:46%}}''','''@media (max-width:600px){.gfkeys{display:none}.gfloc{max-width:46%}}
@media (max-width:520px){.top .gfbtn{display:none}}''')]
for f in sys.argv[1:]:
  s=open(f).read()
  for a,b in R:
    assert s.count(a)==1,(f,s.count(a),a[:80]);s=s.replace(a,b)
  open(f,'w').write(s);print("patched",f)
