import sys
R=[
# paste without titles: the order of the note under the table (Tool, Type, Ø, R, LS, LT, Z, Holder, Code) — correctors and assembly are not in a copied list
('''    let keyOf=ci=>VCOLS[c0+ci];''','''    const PK=["t","type","diameter","ra","ls","oal","z","holder","code"],p0=PK.indexOf(e.target.dataset.k);
    let keyOf=ci=>p0>=0?PK[p0+ci]:VCOLS[c0+ci];'''),
# correctors: H from the tool number also when the T was already there (D already did)
('''if((k==="t"||k==="type")&&num){if(!clean(x.corrH)&&k==="t"){x.corrH=num;ch.push("corrH")}''','''if((k==="t"||k==="type")&&num){if(!clean(x.corrH)){x.corrH=num;ch.push("corrH")}'''),
]
for f in sys.argv[1:]:
  s=open(f).read()
  for a,b in R:
    assert s.count(a)==1,(f,s.count(a),a[:80]);s=s.replace(a,b)
  open(f,'w').write(s);print("patched",f)
