import sys
D="/home/claude/w/v2281/"
JS=open(D+"fix.js").read();CSS=open(D+"fix.css").read()
for f in sys.argv[1:]:
  s=open(f).read();assert "2.28.1 · one scrollbar" not in s
  i=s.find("<style>");j=s.find("</style>",i);s=s[:j]+CSS+s[j:]
  e="\n</script>\n</body></html>";k=s.rfind(e);assert k>0
  s=s[:k]+"\n"+JS+s[k:];open(f,"w").write(s);print("patched",f)
