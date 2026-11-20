import sys
R=[
('''function edBaseline(){edBase=cur?JSON.stringify({article:cur.article,tools:cur.tools,machineId:cur.machineId}):null}''',
 '''// the assembly code a row gets by itself is not an edit
const noAsm=L=>(L||[]).map(x=>{const {asm,asmAuto,...r}=x||{};return r});
function edBaseline(){edBase=cur?JSON.stringify({article:cur.article,tools:noAsm(cur.tools),machineId:cur.machineId}):null}'''),
('''  if(!cur||!edBase)return;const now=JSON.stringify({article:cur.article,tools:cur.tools,machineId:cur.machineId});if(now===edBase)return;''',
 '''  if(!cur||!edBase)return;const now=JSON.stringify({article:cur.article,tools:noAsm(cur.tools),machineId:cur.machineId});if(now===edBase)return;'''),
('''.filter(k=>k!=="t"&&!k.startsWith("_")&&typeof (x[k]??y[k])!=="object");''','''.filter(k=>k!=="t"&&k!=="asm"&&k!=="asmAuto"&&!k.startsWith("_")&&typeof (x[k]??y[k])!=="object");'''),
]
for f in sys.argv[1:]:
  s=open(f).read()
  for a,b in R:
    assert s.count(a)==1,(f,s.count(a),a[:90]);s=s.replace(a,b)
  open(f,'w').write(s);print("patched",f)
# (also applied: recordEdit compares noAsm(cur.tools) per tool)
