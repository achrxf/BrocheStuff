from playwright.sync_api import sync_playwright
with sync_playwright() as p:
  b=p.chromium.launch();ctx=b.new_context(viewport={"width":1500,"height":900});ctx.add_init_script("window.__QA_ROLE='admin'")
  pg=ctx.new_page();errs=[];pg.on("pageerror",lambda e:errs.append(str(e)))
  pg.goto("file:///home/claude/qa/ToolManager.html");pg.wait_for_timeout(1000);pg.evaluate("setLang('fr')")
  pg.evaluate("""db.machines.push({id:'m1',abbr:'S3',name:'X',createdAt:1});db.assemblies=[{id:'x1',code:'AS0001',tool:{type:'FRAISE',diameter:'20',holder:'H1',code:'F941'},auto:1,createdAt:1},
    {id:'x2',code:'AS0002',tool:{type:'TOURTEAU',diameter:'63',holder:'H2',code:'F863'},auto:1,createdAt:1},{id:'x3',code:'AS0003',tool:{type:'TOURTEAU',diameter:'63',holder:'H3',code:'F863'},auto:1,createdAt:1}];db.asmSeeded=1;db.asmLinked=1;
    db.articles.push({id:'a2',machineId:'m1',article:{number:'2'},tools:[{t:'T01'},{t:'T02'}],createdAt:2,updatedAt:2});saveDB();location.hash='#a-a2'""");pg.wait_for_timeout(900)
  el=pg.locator('#rows tr[data-i="0"] input[data-k="code"]');el.fill("F941");el.dispatch_event("change");pg.wait_for_timeout(400)
  print("code used by one assembly -> suggested:",pg.locator('#rows tr[data-i="0"] input[data-k="asm"]').get_attribute("placeholder"),"|",pg.inner_text("#toast")[:60])
  el=pg.locator('#rows tr[data-i="1"] input[data-k="code"]');el.fill("F863");el.dispatch_event("change");pg.wait_for_timeout(400)
  print("code used by two assemblies -> no guess:",pg.locator('#rows tr[data-i="1"] input[data-k="asm"]').get_attribute("placeholder"))
  print("errors",errs);b.close()
