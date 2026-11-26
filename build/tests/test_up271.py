from playwright.sync_api import sync_playwright
R=[]
def ok(n,c,x=""):R.append((n,bool(c)));print(("PASS " if c else "FAIL ")+n,"" if c else x)
SEED="""db.machines.push({id:'m1',abbr:'S3',name:'X',cone:'BT50',createdAt:1});
 db.catalog.push({code:'F941',type:'fraise hfs cw',diameter:'20'});
 db.articles.push({id:'a1',machineId:'m1',article:{number:'1052',index:'A',designation:'Couvercle'},tools:[{t:'T01',type:'fraise 2 tailles eb',holder:'mandrin er32',code:'f941',insert:'rpht1204',op:'ébauche poche'},{t:'T02',type:'foret',diameter:'8.5'}],createdAt:1,updatedAt:1});
 db.articles.push({id:'a2',machineId:'m1',status:'done',validated:{ts:1,who:'x'},article:{number:'2000',index:'B'},tools:[{t:'T01',type:'foret signé'}],createdAt:2,updatedAt:2});
 delete db.up271;saveDB()"""
with sync_playwright() as p:
  b=p.chromium.launch();ctx=b.new_context(viewport={"width":1440,"height":900},reduced_motion="reduce");ctx.add_init_script("window.__QA_ROLE='admin'")
  pg=ctx.new_page();errs=[];pg.on("pageerror",lambda e:errs.append(str(e)))
  pg.goto("file:///home/claude/qa/ToolManager.html");pg.wait_for_timeout(1300);pg.evaluate("setLang('fr')");pg.evaluate(SEED)
  pg.evaluate("location.hash='#a-a1'");pg.wait_for_timeout(1500)
  x=pg.evaluate("A('a1').tools[0]")
  ok("existing sheet put in capitals",x["type"]=="FRAISE 2 TAILLES EB" and x["holder"]=="MANDRIN ER32" and x["code"]=="F941" and x["op"]=="ÉBAUCHE POCHE",x)
  ok("designation and numbers untouched",pg.evaluate("A('a1').article.designation")=="Couvercle" and pg.evaluate("A('a1').tools[1].diameter")=="8.5")
  ok("validated sheet keeps what was signed",pg.evaluate("A('a2').tools[0].type")=="foret signé")
  ok("crib types in capitals",pg.evaluate("C_('F941').type")=="FRAISE HFS CW")
  el=pg.locator('#rows tr[data-i="1"] [data-k="type"]').first
  el.fill("fraise chanfrein");ok("shown in capitals while typing",pg.evaluate("getComputedStyle(document.querySelector('#rows tr[data-i=\"1\"] [data-k=\"type\"]')).textTransform")=="uppercase")
  el.dispatch_event("change");pg.wait_for_timeout(300)
  ok("saved in capitals",pg.evaluate("cur.tools[1].type")=="FRAISE CHANFREIN",pg.evaluate("cur.tools[1].type"))
  pg.evaluate("cur.tools.push({t:'T03',type:'collé depuis excel'});edited()");pg.wait_for_timeout(2500)
  ok("pasted rows go in capitals too",pg.evaluate("cur.tools[2].type")=="COLLÉ DEPUIS EXCEL")
  # turn it off
  pg.click("#b-more");pg.wait_for_timeout(200);pg.click("#b-upper");pg.wait_for_timeout(300)
  ok("switch off",pg.evaluate("!!db.noUpper") and pg.evaluate("document.documentElement.classList.contains('noup')"))
  el=pg.locator('#rows tr[data-i="1"] [data-k="type"]').first;el.fill("Fraise Spéciale");el.dispatch_event("change");pg.wait_for_timeout(2000)
  ok("off: kept as typed",pg.evaluate("cur.tools[1].type")=="Fraise Spéciale")
  pg.click("#b-more");pg.wait_for_timeout(200);pg.click("#b-upper");pg.wait_for_timeout(500)
  ok("back on: everything in capitals again",pg.evaluate("A('a1').tools[1].type")=="FRAISE SPÉCIALE")
  ok("no errors",not errs,errs)
  b.close()
print("FAILED:",[n for n,c in R if not c])
