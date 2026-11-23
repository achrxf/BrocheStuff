import base64
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
  b=p.chromium.launch();ctx=b.new_context(viewport={"width":1400,"height":900});ctx.add_init_script("window.__QA_ROLE='admin'")
  pg=ctx.new_page();errs=[];pg.on("pageerror",lambda e:errs.append(str(e)))
  pg.goto("file:///home/claude/qa/Demo.html");pg.wait_for_timeout(1500);pg.evaluate("setLang('fr')")
  ids=pg.evaluate("db.articles.filter(a=>realTools(a.tools).length>12).slice(0,3).map(a=>a.id)")
  for n,aid in enumerate(ids):
    print(pg.evaluate(f"(()=>{{const m=makePDF(sheetData(A('{aid}'))).bsMeta;return m.keys.map((k,i)=>k+':'+Math.round(m.colw[i]*10)/10).join(' ')}})()"))
    open(f"ux/std{n}.pdf","wb").write(base64.b64decode(pg.evaluate(f"makePDF(sheetData(A('{aid}'))).output('datauristring')").split(",")[1]))
  # everything on: all columns own, 3 extras, long values
  pg.evaluate("""(()=>{const a=A(db.articles[0].id);a.layoutData={labels:{},extra:[{id:'e1',label:'Vitesse'},{id:'e2',label:'Avance'},{id:'e3',label:'Remarque outil'}],hidden:[],joinTo:{},order:[],noprint:[],asmOwn:true,locOwn:true,opt:{}};a.tools.forEach(x=>{x.x_e1='12000';x.x_e2='2400';x.x_e3='Contrôler usure plaquette'});})()""")
  aid=pg.evaluate("db.articles[0].id")
  print(pg.evaluate(f"(()=>{{const m=makePDF(sheetData(A('{aid}'))).bsMeta;return m.keys.map((k,i)=>k+':'+Math.round(m.colw[i]*10)/10).join(' ')+' SUM '+Math.round(m.colw.reduce((a,b)=>a+b,0))}})()"))
  open("ux/wide.pdf","wb").write(base64.b64decode(pg.evaluate(f"makePDF(sheetData(A('{aid}'))).output('datauristring')").split(",")[1]))
  print("blank",pg.evaluate("blankSheet().bsMeta.colw.map(x=>Math.round(x)).join(',')"))
  print(errs);b.close()
