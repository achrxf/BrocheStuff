import sys
R=[
('''function thW(k){const w=colW()[k];return w?w:(k.startsWith("x_")?120:DEFW[k])}''','''function thW(k){const w=colW()[k];return w?w:(k.startsWith("x_")?120:k==="code"&&locUnderC(LAYCFG)?124:DEFW[k])}'''),
('''const SMALL={t:52,asm:72,corr:54,diameter:46,ra:48,ls:42,oal:44,z:32,code:66}''','''const SMALL={t:52,asm:72,corr:54,diameter:46,ra:48,ls:42,oal:44,z:32,code:locUnderC(LAYCFG)?72:66}'''),
]
for f in sys.argv[1:]:
  s=open(f).read()
  for a,b in R:
    assert s.count(a)==1,(f,s.count(a),a[:80]);s=s.replace(a,b)
  open(f,'w').write(s);print("patched",f)
