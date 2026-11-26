import sys,os
D="/home/claude/w/v228/"
exec(open(D+"patch_perf.py").read())
MODS=[m for m in ["perf.js","asm.js","rep.js","chk.js"] if os.path.exists(D+m)]
JS="\n".join(open(D+m).read() for m in MODS)
CSS=open(D+"v228.css").read() if os.path.exists(D+"v228.css") else ""
EXTRA=[]
if os.path.exists(D+"patch_more.py"):exec(open(D+"patch_more.py").read())
for f in sys.argv[1:]:
  s=open(f).read();assert "2.28.0 · speed" not in s,"already "+f
  for a,b in R+EXTRA:
    assert s.count(a)==1,(f,s.count(a),a[:80]);s=s.replace(a,b)
  i=s.find("<style>");j=s.find("</style>",i);s=s[:j]+CSS+s[j:]
  e="\n</script>\n</body></html>";k=s.rfind(e);assert k>0
  s=s[:k]+"\n"+JS+s[k:];open(f,"w").write(s);print("patched",f,MODS)
