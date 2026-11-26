import sys
JS=open("/home/claude/w/up2271.js").read()
CSS="""
/* 2.27.1: capitals while you type (the saved text is put in capitals when you leave the box) */
html:not(.noup) .tt td:is([data-col="type"],[data-col="insert"],[data-col="holder"],[data-col="code"],[data-col="op"],[data-col^="x_"]) :is(input,textarea),
html:not(.noup) .tt .asmin,html:not(.noup) input[list="types"],html:not(.noup) :is([data-af="type"],[data-af="insert"],[data-af="holder"],[data-af="code"]){text-transform:uppercase}
html:not(.noup) .tt td:is([data-col="type"],[data-col="insert"],[data-col="holder"],[data-col="code"],[data-col="op"],[data-col^="x_"]) :is(input,textarea)::placeholder{text-transform:none}
#b-upper .upck{margin-left:auto;font-weight:700;color:var(--done,#2b7a50)}
@media (max-width:760px){#b-upper .lbl{display:none}}
"""
for f in sys.argv[1:]:
  s=open(f).read()
  assert "2.27.1: everything in capitals" not in s
  a='const items=()=>["#b-theme","#b-skin",".lang",'
  assert s.count(a)==1,f
  s=s.replace(a,'const items=()=>["#b-theme","#b-skin","#b-upper",".lang",')
  i=s.find("<style>");j=s.find("</style>",i);s=s[:j]+CSS+s[j:]
  e="\n</script>\n</body></html>";k=s.rfind(e);assert k>0
  s=s[:k]+"\n"+JS+s[k:]
  open(f,"w").write(s);print("patched",f)
