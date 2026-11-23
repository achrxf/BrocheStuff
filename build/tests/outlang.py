import base64,re,json
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
  b=p.chromium.launch();pg=b.new_page();pg.add_init_script("window.__QA_ROLE='admin'")
  pg.goto("file:///home/claude/qa/Demo.html");pg.wait_for_timeout(1500)
  for L in ["en","fr"]:
    pg.evaluate(f"setLang('{L}')")
    aid=pg.evaluate("db.articles.find(x=>realTools(x.tools).length>8).id")
    pg.evaluate(f"(()=>{{const a=A('{aid}');a.ops=true;a.tools[0].op='X';a.tools[0].time='01:00';}})()")
    open(f"ux/lang_{L}.pdf","wb").write(base64.b64decode(pg.evaluate(f"makePDF(sheetData(A('{aid}'))).output('datauristring')").split(",")[1]))
    xl=pg.evaluate(f"JSON.stringify(sheetModel(A('{aid}')))")
    raw=pg.evaluate(f"(()=>{{try{{return JSON.stringify(rawModel(A('{aid}')))}}catch(e){{return ''}}}})()")
    open(f"ux/xl_{L}.json","w").write(xl+"\n"+raw)
    bl=pg.evaluate("blankSheet().output('datauristring')");open(f"ux/blank_{L}.pdf","wb").write(base64.b64decode(bl.split(",")[1]))
  b.close()
