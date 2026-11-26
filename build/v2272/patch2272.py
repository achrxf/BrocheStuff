import sys
JS=open("/home/claude/w/up2272.js").read()
for f in sys.argv[1:]:
  s=open(f).read();assert "2.27.2: the operation columns" not in s
  e="\n</script>\n</body></html>";k=s.rfind(e);assert k>0
  s=s[:k]+"\n"+JS+s[k:];open(f,"w").write(s);print("patched",f)
