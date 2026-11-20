import sys
R=[('''const hit=e=>{const t=e.target;if(!t||!t.closest)return null;
    const th=t.closest("#view thead th");''','''const hit=e=>{const t=e.target;if(!t||!t.closest)return null;
    // a box or a button near a column edge is clicked, not dragged
    if(t.closest("input,select,button,a,label"))return null;
    const th=t.closest("#view thead th");''')]
for f in sys.argv[1:]:
  s=open(f).read()
  for a,b in R:
    assert s.count(a)==1,(f,s.count(a));s=s.replace(a,b)
  open(f,'w').write(s);print("patched",f)
# also: both layout save paths store asmOwn (order:c.order,noprint:c.noprint} -> ...,asmOwn:c.asmOwn})
