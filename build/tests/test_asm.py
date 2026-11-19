from playwright.sync_api import sync_playwright
R=[]
def ok(n,c,x=""):R.append((n,bool(c)));print(("PASS " if c else "FAIL ")+n,x)
U="file:///home/claude/qa/ToolManager.html"
SEED="""db.machines.push({id:'m1',abbr:'S3',name:'TOYODA',cone:'BT50',createdAt:1});
 db.articles.push({id:'a1',machineId:'m1',article:{number:'1052',index:'A'},tools:[
  {t:'T09',corrH:'9',type:'TOURTEAU',insert:'RPHT1204',diameter:'63',ra:'R6',ls:'40',holder:'MANDRIN À TENON Ø22\\nBT50ADB-SM22-055-L1',code:'F863'},
  {t:'T02',corrH:'2',type:'TOURTEAU',diameter:'112',ra:'R6',ls:'63',holder:'MANDRIN À TENON Ø32\\nBT50ADB-SM32-055-L1',code:'F863'},
  {t:'T52',corrH:'52',type:'FRAISE HFS CW',diameter:'20',ra:'R3',ls:'55',holder:'CÔNE FRETTÉ\\nE3416560320100',code:'F941'},
  {t:'T10',corrH:'10',type:'FORET',diameter:'6.7',ls:'45'}],createdAt:1,updatedAt:1});
 db.articles.push({id:'a2',machineId:'m1',article:{number:'2000',index:'B'},tools:[{t:'T01'}],createdAt:2,updatedAt:2});delete db.asmSeeded;db.assemblies=[];saveDB()"""
with sync_playwright() as p:
  b=p.chromium.launch();ctx=b.new_context(viewport={"width":1440,"height":900});ctx.add_init_script("window.__QA_ROLE='admin'")
  pg=ctx.new_page();errs=[];pg.on("pageerror",lambda e:errs.append(str(e)));pg.on("console",lambda m:m.type=="error" and errs.append(m.text[:200]))
  pg.goto(U);pg.wait_for_timeout(1500);pg.evaluate("setLang('fr')");pg.evaluate(SEED)
  pg.evaluate("location.hash='#asm'");pg.wait_for_timeout(800)
  ok("menu has Assemblages",pg.locator("#nav-s").inner_text()=="Assemblages" and pg.locator("#nav-s").is_visible())
  codes=pg.evaluate("asmList().map(a=>a.code+':'+a.tool.type+':'+(a.tool.diameter||''))")
  ok("existing sheets fill the library (3 complete rows, not the one without holder)",codes==["AS0001:TOURTEAU:63","AS0002:TOURTEAU:112","AS0003:FRAISE HFS CW:20"],codes)
  ok("page lists them",pg.locator(".asmt tbody tr").count()==3)
  ok("used-in shows the sheet","1052" in pg.inner_text(".asmt"))
  pg.screenshot(path="asm_page.png")
  # sheet 2: type AS0003 in the code box
  pg.evaluate("location.hash='#a-a2'");pg.wait_for_timeout(1200)
  inp=pg.locator('#rows tr[data-i="0"] input[data-k="code"]').first
  inp.fill("as3");inp.dispatch_event("change");pg.wait_for_timeout(500)
  x=pg.evaluate("cur.tools[0]")
  ok("typing as3 fills the row",x.get("type")=="FRAISE HFS CW" and x.get("code")=="F941" and "CÔNE FRETTÉ" in x.get("holder","") and x.get("t")=="T01",x)
  ok("toast says so","AS0003" in pg.inner_text("#toast"))
  ok("chip under T shows AS0003",pg.locator('#rows tr[data-i="0"] .asmc').inner_text()=="AS0003")
  inp=pg.locator('#rows tr[data-i="0"] input[data-k="code"]').first
  # unknown code
  pg.evaluate("cur.tools.push({t:'T02'});renderRows()")
  i2=pg.locator('#rows tr[data-i="1"] input[data-k="code"]').first;i2.fill("AS0099");i2.dispatch_event("change");pg.wait_for_timeout(300)
  ok("unknown assembly code told","AS0099" in pg.inner_text("#toast"))
  # a new row typed by hand becomes an assembly after a pause; half-typed versions don't stay
  pg.evaluate("cur.tools[1]={t:'T02',type:'FORET CW',diameter:'8',holder:'MANDRIN',code:''};renderRows();edited()");pg.wait_for_timeout(2900)
  mid=pg.evaluate("asmList().map(a=>a.code)")
  pg.evaluate("cur.tools[1].holder='MANDRIN À PINCE ER32\\nBT50AD-ER32-120';cur.tools[1].code='F884';renderRows();edited()");pg.wait_for_timeout(2900)
  fin=pg.evaluate("asmList().map(a=>a.code+':'+a.tool.code)")
  ok("half-typed assembly made then replaced (no leftovers)",len(mid)==4 and fin[-1]=="AS0004:F884" and len(fin)==4,(mid,fin))
  ok("chip updates by itself",pg.locator('#rows tr[data-i="1"] .asmc').inner_text()=="AS0004")
  # sorting
  pg.evaluate("location.hash='#a-a1'");pg.wait_for_timeout(1200)
  pg.select_option("#a-sort","t");pg.wait_for_timeout(400)
  ok("sort by T",pg.evaluate("cur.tools.map(x=>x.t)")==["T02","T09","T10","T52"],pg.evaluate("cur.tools.map(x=>x.t)"))
  pg.select_option("#a-sort","diaD");pg.wait_for_timeout(400)
  ok("sort by Ø large to small",pg.evaluate("cur.tools.map(x=>x.diameter)")==["112","63","20","6.7"])
  ok("sort select goes back to —",pg.input_value("#a-sort")=="")
  pg.click("#toast .tact");pg.wait_for_timeout(400)
  ok("undo",pg.evaluate("cur.tools.map(x=>x.t)")==["T02","T09","T10","T52"])
  pg.select_option("#a-sort","holder");pg.wait_for_timeout(300)
  ok("sort by holder (no holder last)",pg.evaluate("cur.tools.map(x=>x.t)")==["T52","T09","T02","T10"],pg.evaluate("cur.tools.map(x=>x.t)"))
  pg.wait_for_timeout(500);pg.evaluate("flushEditor()");ok("order saved",pg.evaluate("A('a1').tools.map(x=>x.t)")==["T52","T09","T02","T10"])
  # page: edit, keep, delete, new
  pg.evaluate("location.hash='#asm'");pg.wait_for_timeout(700)
  pg.locator("[data-asmed]").first.click();pg.wait_for_timeout(300)
  pg.fill("#as-name","Tourteau 63 standard");pg.click("#as-ok");pg.wait_for_timeout(300)
  ok("name saved",pg.evaluate("asmFind('AS0001').name")=="Tourteau 63 standard")
  pg.click("#asm-new");pg.wait_for_timeout(300);pg.click("#as-ok");pg.wait_for_timeout(200)
  ok("new: needs holder",not pg.locator("#as-err").is_hidden())
  pg.fill("[data-af=type]","TARAUD M8");pg.fill("[data-af=code]","t88");pg.fill("[data-af=holder]","PORTE TARAUD\nBT50-TAP");pg.click("#as-ok");pg.wait_for_timeout(300)
  ok("new manual one, kept",pg.evaluate("(()=>{const a=asmFind('AS0005');return a&&a.keep&&!a.auto&&a.tool.code})()")=="T88")
  pg.click("[data-asf=free]");pg.wait_for_timeout(200);ok("filter 'in no sheet'",pg.locator(".asmt tbody tr").count()==1)
  pg.click("[data-asf=all]");pg.fill("#asm-q","fretté");pg.wait_for_timeout(300);ok("search",pg.locator(".asmt tbody tr").count()==1)
  pg.fill("#asm-q","");pg.wait_for_timeout(200)
  pg.locator("tr[data-asmid]").last.click();pg.wait_for_timeout(300);pg.click("#as-del");pg.wait_for_timeout(200);pg.click("#as-delok");pg.wait_for_timeout(300)
  ok("delete",pg.evaluate("asmList().length")==4)
  # merge between two PCs that made the same code
  r=pg.evaluate("""(()=>{const b={assemblies:[]},m={assemblies:[{id:'x1',code:'AS0009',tool:{holder:'H',code:'A'},createdAt:1}]},t2={assemblies:[{id:'x2',code:'AS0009',tool:{holder:'H',code:'B'},createdAt:2}]};
     const o=merge3db(b,m,t2);const save=db.assemblies;db.assemblies=o.assemblies;asmFix();const r=db.assemblies.map(a=>a.id+':'+a.code).sort();db.assemblies=save;return r})()""")
  ok("same code from two PCs -> second one renumbered",r==["x1:AS0009","x2:AS0010"],r)
  ok("no errors",not errs,errs)
  b.close()
print("FAILED:",[n for n,c in R if not c])
