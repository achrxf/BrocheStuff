import sys
JS=open("/home/claude/w/up2273.js").read()
R=[('''if(!/^(xlsx|xls|xlsm|xlsb|ods|csv)$/.test(ext)){const txt=await file.text();''','''if(!/^(xlsx|xls|xlsm|xlsb|ods|csv)$/.test(ext)){const txt=await ncText(file);'''),
   ('''for(const f of files){try{const txt=await f.text();const r=parseNC(txt,f.name);''','''for(const f of files){try{const txt=await ncText(f);const r=parseNC(txt,f.name);'''),
   ('''...(it.r.seqTools.length>it.r.tools.length||it.r.seqTools.some(x=>clean(x.op))?{ops:true}:{}),''','''''')]
for f in sys.argv[1:]:
  s=open(f).read();assert "2.27.3: operation columns only" not in s
  for a,b in R:
    assert s.count(a)==1,(f,a[:60]);s=s.replace(a,b)
  e="\n</script>\n</body></html>";k=s.rfind(e);assert k>0
  s=s[:k]+"\n"+JS+s[k:];open(f,"w").write(s);print("patched",f)
