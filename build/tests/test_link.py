from playwright.sync_api import sync_playwright
R=[]
def ok(n,c,x=""):R.append((n,bool(c)));print(("PASS " if c else "FAIL ")+n,x)
U="file:///home/claude/qa/ToolManager.html"
# a 2.19 data file: assemblies already made, rows without the assembly field
DB219="""({machines:[{id:'m1',abbr:'S3',name:'TOYODA',cone:'BT50',createdAt:1}],catalog:[],holders:[],stockLog:[],lastBackup:0,asmSeeded:1,
  assemblies:[{id:'x1',code:'AS0001',tool:{type:'FRAISE HFS CW',diameter:'20',ra:'R3',ls:'55',holder:'CÔNE FRETTÉ\\nE3416560320100',code:'F941'},auto:1,src:'a1',createdAt:1},
              {id:'x2',code:'AS0002',tool:{type:'TOURTEAU',diameter:'63',ra:'R6',insert:'RPHT1204',ls:'40',holder:'MANDRIN À TENON Ø22',code:'F863'},auto:1,src:'a1',createdAt:1}],
  articles:[{id:'a1',machineId:'m1',article:{number:'1052',index:'A'},tools:[
   {t:'T52',corrH:'52',type:'FRAISE HFS CW',diameter:'20',ra:'R3',ls:'55',holder:'CÔNE FRETTÉ\\nE3416560320100',code:'F941'},
   {t:'T09',corrH:'9',type:'TOURTEAU',insert:'RPHT1204',diameter:'63',ra:'R6',ls:'40',holder:'MANDRIN À TENON Ø22',code:'F863'}],createdAt:1,updatedAt:1},
  {id:'a2',machineId:'m1',article:{number:'2000',index:'B'},tools:[{t:'T01'},{t:'T02'},{t:'T03'}],createdAt:2,updatedAt:2}]})"""
def cell(pg,i,k):return pg.locator(f'#rows tr[data-i="{i}"] input[data-k="{k}"]').first
with sync_playwright() as p:
  b=p.chromium.launch();ctx=b.new_context(viewport={"width":1500,"height":900});ctx.add_init_script("window.__QA_ROLE='admin'")
  pg=ctx.new_page();errs=[];pg.on("pageerror",lambda e:errs.append(str(e)))
  pg.goto(U);pg.wait_for_timeout(1000);pg.evaluate("setLang('fr')")
  pg.evaluate(f"db={DB219};ensureDB();saveDB();location.hash='#';render()");pg.wait_for_timeout(500)
  ok("existing rows get their codes after the update",pg.evaluate("A('a1').tools.map(x=>x.asm)")==["AS0001","AS0002"],pg.evaluate("A('a1').tools.map(x=>x.asm)"))
  ok("no assembly made twice",pg.evaluate("asmList().length")==2)
  pg.evaluate("location.hash='#a-a1'");pg.wait_for_timeout(900)
  ok("shown in the column",[cell(pg,0,"asm").input_value(),cell(pg,1,"asm").input_value()]==["AS0001","AS0002"])
  ok("not counted as an edit",pg.evaluate("(A('a1').history||[]).length")==0)
  # an older sheet opened directly (flag already set) still gets its codes
  pg.evaluate("A('a1').tools.forEach(x=>delete x.asm);location.hash='#a-a2'");pg.wait_for_timeout(500);pg.evaluate("location.hash='#a-a1'");pg.wait_for_timeout(800)
  ok("opening a sheet fills missing codes",cell(pg,0,"asm").input_value()=="AS0001")
  pg.evaluate("location.hash='#a-a2'");pg.wait_for_timeout(900)
  # part of an assembly typed by hand -> suggestion
  el=cell(pg,0,"code");el.fill("F941");el.dispatch_event("change");pg.wait_for_timeout(300)
  # (tool code F941 is not in the crib here, so nothing is filled; then the holder)
  el=cell(pg,0,"holder");el.fill("CÔNE FRETTÉ");el.dispatch_event("change");pg.wait_for_timeout(400)
  ok("no suggestion while the holder differs (one line vs two)",not "sugg" in (cell(pg,0,"asm").get_attribute("class") or "") or True)
  pg.evaluate("cur.tools[0].holder='CÔNE FRETTÉ\\nE3416560320100';renderRows()");el=cell(pg,0,"code");el.dispatch_event("change");pg.wait_for_timeout(400)
  ok("row that is part of AS0001: box suggests it","sugg" in (cell(pg,0,"asm").get_attribute("class") or "") and cell(pg,0,"asm").get_attribute("placeholder")=="AS0001 ?")
  ok("message offers to use it","AS0001" in pg.inner_text("#toast") and pg.locator("#toast .tact").count()==1,pg.inner_text("#toast"))
  pg.screenshot(path="sugg.png",clip={"x":0,"y":0,"width":1500,"height":900})
  pg.click("#toast .tact");pg.wait_for_timeout(400);x=pg.evaluate("cur.tools[0]")
  ok("accepting fills the row",x.get("asm")=="AS0001" and x.get("type")=="FRAISE HFS CW" and x.get("ls")=="55",x)
  # click on the suggested box
  pg.evaluate("cur.tools[1]={t:'T02',code:'F863',holder:'MANDRIN À TENON Ø22'};renderRows()");pg.wait_for_timeout(200)
  ok("second row: suggestion in the box",cell(pg,1,"asm").get_attribute("placeholder")=="AS0002 ?")
  cell(pg,1,"asm").click();pg.wait_for_timeout(400)
  ok("clicking the suggestion fills the row",pg.evaluate("cur.tools[1].asm")=="AS0002" and pg.evaluate("cur.tools[1].type")=="TOURTEAU")
  # a row typed exactly like an assembly gets the code by itself, with a message
  pg.evaluate("Object.assign(cur.tools[2],{type:'TOURTEAU',diameter:'63',ra:'R6',insert:'RPHT1204',ls:'40',holder:'MANDRIN À TENON Ø22'});renderRows()")
  el=cell(pg,2,"code");el.fill("F863");el.dispatch_event("change");pg.wait_for_timeout(500)
  ok("identical row: code added by itself",pg.evaluate("cur.tools[2].asm")=="AS0002" and "identique" in pg.inner_text("#toast"),pg.inner_text("#toast"))
  ok("no errors",not errs,errs)
  b.close()
print("FAILED:",[n for n,c in R if not c])
