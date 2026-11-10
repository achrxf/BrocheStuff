from playwright.sync_api import sync_playwright
with sync_playwright() as p:
  b=p.chromium.launch();ctx=b.new_context(viewport={"width":1400,"height":950});ctx.add_init_script("window.__QA_ROLE='admin'")
  pg=ctx.new_page();errs=[];pg.on("pageerror",lambda e:errs.append(str(e)))
  pg.goto("http://127.0.0.1:8765/ToolManager.html");pg.wait_for_timeout(1500);pg.evaluate("setLang('fr')")
  pg.evaluate("db.machines.push({id:'m1',abbr:'S3',name:'DMU',createdAt:1});saveDB()")
  with pg.expect_file_chooser() as fc: pg.evaluate("void startImport('articles',{machineId:'m1'})")
  fc.value.set_files("arts.xlsx");pg.wait_for_timeout(1200)
  pg.check("#imp-sort");pg.click("#d-imp");pg.wait_for_timeout(800)
  r=pg.evaluate("db.articles.map(a=>a.article.number+' '+a.tools.map(x=>x.t).join(','))")
  print(("PASS" if r==["9999-1 T1,T2,T5,T12"] else "FAIL"),"articles import sorted",r,errs)
  b.close()
