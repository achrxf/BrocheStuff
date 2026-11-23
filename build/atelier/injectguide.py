import json,sys
G=json.load(open("/home/claude/qa/guideimg.json"))
for f in sys.argv[1:]:
  s=open(f).read();i=s.find("const GUIDEIMG={");j=s.find("};",i)
  assert i>0 and j>i
  s=s[:i]+"const GUIDEIMG="+json.dumps(G,separators=(",",":"))+";"+s[j+2:]
  open(f,"w").write(s);print("guide",f,len(G))
