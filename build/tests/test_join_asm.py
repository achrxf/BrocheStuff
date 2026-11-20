from playwright.sync_api import sync_playwright
R=[]
def ok(n,c,x=""):R.append((n,bool(c)));print(("PASS " if c else "FAIL ")+n,x)
U="file:///home/claude/qa/ToolManager.html"
with sync_playwright() as p:
  b=p.chromium.launch();ctx=b.new_context(viewport={"width":1500,"height":900});ctx.add_init_script("window.__QA_ROLE='admin'")
  pg=ctx.new_page();errs=[];pg.on("pageerror",lambda e:errs.append(str(e)));pg.on("console",lambda m:m.type=="error" and errs.append(m.text[:200]))
  pg.goto(U);pg.wait_for_timeout(1000);pg.evaluate("setLang('fr')")
  pg.evaluate("""db.machines.push({id:'m1',abbr:'S3',name:'X',cone:'BT50',createdAt:1});
    db.articles.push({id:'a1',machineId:'m1',article:{number:'1052',index:'A'},tools:[{t:'T52',corrH:'52',type:'FRAISE HFS CW',diameter:'20',ra:'R3',ls:'55',holder:'CÔNE FRETTÉ',code:'F941'},{t:'T09'}],createdAt:1,updatedAt:1});
    delete db.asmSeeded;db.assemblies=[];saveDB();location.hash='#a-a1'""");pg.wait_for_timeout(1500)
  heads=pg.evaluate("[...document.querySelectorAll('.tt thead tr:first-child th')].map(t=>t.textContent.trim()).slice(0,3)")
  ok("Standard: no separate Assemblage column",heads[1]!="Assemblage",heads)
  ok("code under the tool number",pg.locator('#rows tr[data-i="0"] td[data-col="t"] input[data-k="asm"]').input_value()=="AS0001")
  # typing a code under T still fills
  el=pg.locator('#rows tr[data-i="1"] td[data-col="t"] input[data-k="asm"]');el.fill("as1");el.dispatch_event("change");pg.wait_for_timeout(400)
  ok("typing under T fills the row",pg.evaluate("cur.tools[1].type")=="FRAISE HFS CW")
  ok("print box for it next to PDF",pg.locator('.prrow .prlab [data-pr=asm]').count()==1)
  # PDF: not printed by default; ticked -> under the T number
  ok("PDF default: no assembly",'asm' not in pg.evaluate("JSON.stringify(makePDF(sheetData(A('a1'))).bsMeta.gj)") and 'asm' not in pg.evaluate("makePDF(sheetData(A('a1'))).bsMeta.keys"))
  pg.check('.prrow .prlab [data-pr=asm]');pg.wait_for_timeout(400)
  gj=pg.evaluate("JSON.stringify(makePDF(sheetData(A('a1'))).bsMeta.gj)");ok("ticked: under T on the PDF",'"t":["asm"]' in gj,gj)
  ok("…and on the Excel",'"t":["asm"]' in pg.evaluate("JSON.stringify(makePDF(xlData(A('a1'))).bsMeta.gj)"))
  pg.evaluate("(async()=>{const d=makePDF(sheetData(A('a1')));window.__pdf=d.output('datauristring')})()")
  # layout: pick its own column, save as new layout -> separate column
  pg.click("#b-cols");pg.wait_for_timeout(600)
  ok("join picker shows 'Dans Outil' selected for Assemblage",pg.input_value('[data-jt=asm]')=="t",pg.input_value('[data-jt=asm]'))
  pg.select_option('[data-jt=asm]',"");pg.wait_for_timeout(300)
  pg.click("#lay-as");pg.fill("#lay-asname","Colonne assemblage");pg.click("#lay-asok");pg.wait_for_timeout(700)
  L=pg.evaluate("JSON.stringify(db.layouts.map(l=>({n:l.name,own:l.asmOwn,j:l.joinTo})))");ok("saved: own column",'"own":true' in L and '"asm"' not in L,L)
  heads=pg.evaluate("[...document.querySelectorAll('.tt thead tr:first-child th')].map(t=>t.textContent.trim()).slice(0,3)")
  ok("sheet on that layout: separate Assemblage column",heads[1]=="Assemblage",heads)
  # and back: join it under Outil in that layout
  pg.click("#b-cols");pg.wait_for_timeout(600);pg.select_option('[data-jt=asm]',"t");pg.click("#col-ok");pg.wait_for_timeout(700)
  L=pg.evaluate("JSON.stringify(db.layouts.map(l=>({own:l.asmOwn,j:l.joinTo})))");ok("joined again, saved",'"asm":"t"' in L and '"own":false' in L,L)
  heads=pg.evaluate("[...document.querySelectorAll('.tt thead tr:first-child th')].map(t=>t.textContent.trim()).slice(0,3)");ok("…code back under T",heads[1]!="Assemblage",heads)
  # read-only view
  pg.evaluate("location.hash='#v-a1'");pg.wait_for_timeout(800);ok("read-only view: code under T","AS0001" in pg.inner_text(".avt") and "Assemblage" not in pg.inner_text(".avt thead"))
  ok("no errors",not errs,errs)
  b.close()
print("FAILED:",[n for n,c in R if not c])
