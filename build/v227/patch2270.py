import sys
# 2.27.0: a CNC program gives every tool call in order (repeats = operations), compressed blocks (N10T12M6, M06T5) are read,
# assemblies are only made when you ask, editing one updates its sheets, and each assembly keeps its T number per machine.
W="/home/claude/w/"
JS=open(W+"asm2270.js").read()
CSS=r"""
/* 2.27: T per machine in the assembly window and list */
.asmtn{display:flex;flex-direction:column;gap:8px;padding:12px;border:1px solid var(--hair);background:var(--fill);border-radius:4px}
html.at .asmtn{border-radius:2px}
.asmtn .tnh{display:flex;flex-direction:column;gap:2px}
.asmtn .tnh b{font:700 13px var(--display);letter-spacing:.04em}
.asmtn .tnh span{font-size:12.5px;color:var(--mid)}
.asmtn .tng{display:flex;flex-wrap:wrap;gap:6px}
.asmtn .tnr{display:inline-flex;align-items:stretch;border:1px solid var(--line2);background:var(--paper)}
.asmtn .tnr span{display:flex;align-items:center;padding:0 8px;background:var(--ink);color:var(--bg);font:700 12px var(--mono)}
.asmtn .tnr input{width:62px;border:0;padding:6px 8px;background:transparent;color:var(--ink);font:600 13px var(--mono)}
.asmtn .tnr input:focus{outline:2px solid var(--red);outline-offset:-2px}
.asmtn .tnadd{max-width:260px}
.asmtnl{display:flex;flex-wrap:wrap;gap:3px;margin-top:4px}
.asmtnl span{display:inline-flex;border:1px solid var(--line2);font:600 11px var(--mono);color:var(--ink)}
.asmtnl span i{font-style:normal;padding:0 4px;background:var(--fill);color:var(--mid);border-right:1px solid var(--line2)}
.asmtnl span{padding-right:4px}
.asmtnl span i{margin-right:4px}
"""
FR_ASM='["asm","Assemblages",["Un assemblage, c’est un outil avec son porte-outil, gardé sous un code (AS0001…). Il ne se crée plus tout seul : sous le tableau d’une fiche, « Créer les assemblages » en fait un pour chaque ligne complète (porte-outil + code outil, ou type + Ø), ou bien « + Nouvel assemblage » sur la page Assemblages.","Chaque assemblage garde son numéro d’outil par machine. Tapez son code dans la colonne Assemblage (ou dans la colonne Code) : la ligne se remplit, et le T aussi s’il est connu pour cette machine. Changez le T dans la fiche, et l’assemblage retient le nouveau T pour cette machine. Sur une autre machine, il peut avoir un autre T.","Modifier un assemblage (page Assemblages, clic sur la ligne) met à jour toutes les fiches qui l’utilisent, sauf les fiches validées qui gardent l’ancien. La fenêtre montre aussi le T sur chaque machine, à changer ou à ajouter.","Si vous changez l’outil d’une ligne reliée (Ø, LS, porte-outil…), elle passe en orange et BrocheStuff propose « Mettre à jour » l’assemblage. Pour détacher une ligne, videz sa case Assemblage. « Supprimer les inutilisés » nettoie les anciens assemblages créés tout seuls que plus aucune fiche n’utilise."]],'
EN_ASM='["asm","Assemblies",["An assembly is a tool with its holder, kept under a code (AS0001…). It is no longer made by itself: under a sheet’s table, “Make the assemblies” makes one for each complete row (holder + tool code, or type + Ø), or use “+ New assembly” on the Assemblies page.","Each assembly keeps its tool number per machine. Type its code in the Assembly column (or the Code column): the row fills in, and the T too when it is known for this machine. Change the T in the sheet and the assembly remembers the new T for that machine. On another machine it can have another T.","Changing an assembly (Assemblies page, click its row) updates every sheet that uses it, except validated sheets, which keep the old one. The window also shows the T on each machine, to change or add.","If you change the tool of a linked row (Ø, LS, holder…), it turns orange and BrocheStuff offers to “Update” the assembly. To unlink a row, empty its Assembly box. “Delete the unused ones” clears the old automatic assemblies that no sheet uses any more."]],'
R=[
# compressed blocks: N10T12M6 · T12M06 · M06T12
('''else{const tm=code.match(/\\bT\\s*(\\d{1,4})\\b/);const m6=/\\bM0?6\\b/.test(code);''',
 '''else{const tm=code.match(/(?:^|[^A-Z])T\\s*(\\d{1,4})(?!\\d)/);const m6=/(?:^|[^A-Z])M0*6(?![\\d.])/.test(code);'''),
# every call, in order, with the operation comment written just before it
('''    if(call){seen(call);lastTool=call;afterCall=2;''','''    if(call){seen(call);seq.push({k:call,op:opBuf});opBuf="";lastTool=call;afterCall=2;'''),
('''{note(lastTool,c);afterCall=0}
      else lastComment=c}''','''{note(lastTool,c);afterCall=0;if(/^\\s*(?:N?\\d+\\s*)?;/.test(line)&&ncOp(c))opBuf=ncOp(c)}
      else{lastComment=c;if(ncOp(c)&&!/^\\s*[O:%]\\d/.test(code.trim()))opBuf=ncOp(c)}}'''),
('''  let program="",pendingT=null;const order=[],info=new Map(),calls=new Map(),corr=new Map();''','''  let program="",pendingT=null;const order=[],info=new Map(),calls=new Map(),corr=new Map(),seq=[];let opBuf="";'''),
('''  const base=String(fname||"").replace(/\\.[^.]+$/,"");
  return{program:program||base,name:base,tools,calls:Object.fromEntries(calls)};''','''  const base=String(fname||"").replace(/\\.[^.]+$/,"");
  // the tools in the order the program uses them, a line for every tool change (a tool used twice = two operations)
  const byK=new Map(tools.map(x=>[x.t,x]));const seqTools=seq.map(s=>({...byK.get(s.k),...(s.op?{op:s.op}:{})}));
  tools.forEach(x=>{if(!seq.some(s=>s.k===x.t))seqTools.push({...x})});
  return{program:program||base,name:base,tools,seqTools,calls:Object.fromEntries(calls)};'''),
('''function parseNC(text,fname){''','''// the operation comment before a tool change, e.g. (CONTOURNAGE EBAUCHE) — not the tool's own description or the program header
const ncOp=c=>{c=String(c||"").trim();if(!c||c.length>70)return"";if(/^\\s*T\\s*\\d/i.test(c)||/^\\s*TOOL\\b|DIA\\.?\\s*OFF|LEN\\.?\\s*-|PROGRAM|PROGRAMME|DATE|TIME|HEURE|MCX|NC FILE|MATERIAL|MATIERE|POST|^O\\d+$/i.test(c))return"";return c.replace(/\\s+/g," ")};
function parseNC(text,fname){'''),
('''const looksNC=txt=>/\\bM0?6\\b|TOOL CALL|''','''const looksNC=txt=>/(?:^|\\n)\\s*(?:N\\d+\\s*)?(?:T\\d{1,4}\\s*M0?6|M0?6\\s*T\\d{1,4})(?!\\d)/i.test(txt.slice(0,200000))||/\\bM0?6\\b|TOOL CALL|'''),
('''const NC_HEAD=["T number","Type","Diameter","Radius / angle","Insert","LS","LT","Z","Offset H","Offset D","Holder","Code"];
const ncRows=tools=>{const ex=sheetCfg().extra;return [[...NC_HEAD,...ex.map(e=>e.label)],...tools.map(x=>[x.t,x.type,x.diameter,x.ra,x.insert||"",x.ls,x.oal,x.z,x.corrH||"",x.corrD||"",x.holder,x.code,...ex.map(e=>x[xKey(e.id)]||"")])]};''',
 '''const NC_HEAD=["T number","Type","Diameter","Radius / angle","Insert","LS","LT","Z","Offset H","Offset D","Holder","Code"];
const ncRows=tools=>{const ex=sheetCfg().extra,op=tools.some(x=>clean(x.op));return [[...NC_HEAD,...(op?["Operation"]:[]),...ex.map(e=>e.label)],...tools.map(x=>[x.t,x.type,x.diameter,x.ra,x.insert||"",x.ls,x.oal,x.z,x.corrH||"",x.corrD||"",x.holder,x.code,...(op?[x.op||""]:[]),...ex.map(e=>x[xKey(e.id)]||"")])]};'''),
('''if(looksNC(txt)){const r=parseNC(txt,file.name);if(r.tools.length)return [{name:file.name,rows:ncRows(r.tools),nc:r}]}''',
 '''if(looksNC(txt)){const r=parseNC(txt,file.name);if(r.tools.length)return [{name:file.name,rows:ncRows(r.seqTools),nc:r}]}'''),
# many programs at once: the same full order
('''<td>${it.r&&it.r.tools.length?esc(it.r.tools.map(x=>x.t).join(" ")):''','''<td>${it.r&&it.r.tools.length?esc(it.r.seqTools.map(x=>x.t).join(" ")):'''),
('''tools:it.r.tools,status:"progress",''','''tools:it.r.seqTools.map(x=>({...x})),...(it.r.seqTools.length>it.r.tools.length||it.r.seqTools.some(x=>clean(x.op))?{ops:true}:{}),status:"progress",'''),
# importing a program: keep its order, keep every call (no "which double to keep" question for the program's own repeats)
('''let si=0,hdr,map,mode="add",sortT=false;try{sortT=localStorage.getItem("bs.impsort")==="1"}catch(e){}''',
 '''let si=0,hdr,map,mode="add",sortT=false;try{sortT=localStorage.getItem("bs.impsort")==="1"}catch(e){}if(sheets&&sheets.some(s=>s.nc))sortT=false;'''),
('''    if(kind==="tools"&&!ctx.plan){const groups=impDupGroups(mode==="replace"?[]:cur.tools,rows,val,hdr);
      if(groups.length){''','''    if(kind==="tools"&&!ctx.plan){let groups=impDupGroups(mode==="replace"?[]:cur.tools,rows,val,hdr);
      if(sheets[si].nc&&groups.length){groups.forEach(g=>{if(g.copies.every(c=>c.src!=="sheet"))g.choice=-1});if(groups.every(g=>g.choice===-1)){ctx.plan=groups;groups=[]}}
      if(groups.length){'''),
('''    if(ctx.sortT)out=sortByT(out);
    cur.tools=out.length?out:[{t:"T01"}];''','''    if(ctx.sortT)out=sortByT(out);
    cur.tools=out.length?out:[{t:"T01"}];
    {const ts=realTools(cur.tools).map(x=>tNum(x.t)).filter(n=>n!=null);if(!cur.ops&&(got.some(x=>clean(x.op))||new Set(ts).size<ts.length)){cur.ops=true;try{refreshCols(cur)}catch(_){}const A=cur;setTimeout(()=>{if(cur===A&&route.view==="article")renderEditor(A)},0)}}'''),
]
for f in sys.argv[1:]:
  s=open(f).read()
  assert "2.27: assemblies that you control" not in s,"already patched "+f
  for a,b in R:
    assert s.count(a)==1,(f,s.count(a),a[:100]);s=s.replace(a,b)
  for a,b in [('["asm","Assemblages",[',FR_ASM),('["asm","Assemblies",[',EN_ASM)]:
    i=s.find(a);assert i>0;j=s.find(']],',i)+3;s=s[:i]+b+s[j:]
  i=s.find("<style>");j=s.find("</style>",i);s=s[:j]+CSS+s[j:]
  e="\n</script>\n</body></html>"
  k=s.rfind(e);assert k>0
  s=s[:k]+"\n"+JS+s[k:]
  open(f,"w").write(s);print("patched",f)
