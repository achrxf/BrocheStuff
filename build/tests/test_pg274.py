from playwright.sync_api import sync_playwright
import json
R=[]
def ok(n,c,x=""):R.append((n,bool(c)));print(("PASS " if c else "FAIL ")+n,x if not c else "")
with sync_playwright() as p:
  b=p.chromium.launch();ctx=b.new_context(viewport={"width":1440,"height":900});ctx.add_init_script("window.__QA_ROLE='admin'")
  pg=ctx.new_page();errs=[];pg.on("pageerror",lambda e:errs.append(str(e)));pg.goto("file:///home/claude/qa/Demo.html");pg.wait_for_timeout(2000)
  if pg.locator(".langdlg").count():pg.click("[data-pick=fr]")
  m=pg.evaluate("db.machines.find(x=>x.abbr==='H1').id")
  pg.evaluate(f"location.hash='#m-{m}'");pg.wait_for_timeout(900);pg.click("#newa");pg.wait_for_timeout(1200)
  pg.evaluate("""cur.tools=[{t:'T12',type:'FORET',diameter:'8.5',ls:'60',holder:'MANDRIN',code:'D85'},{t:'T1',type:'FRAISE A SURFACER',diameter:'50',ls:'40',holder:'PORTE FRAISE',code:'S50'},{t:'T05',type:'FRAISE 2T',diameter:'12',ls:'45',holder:'FRETTE',code:'F12'},{t:'T30',type:'TARAUD',diameter:'M10',holder:'TARAUDAGE'}];edited();renderEditor(cur)""");pg.wait_for_timeout(800)
  def read():
    with pg.expect_file_chooser() as fc:pg.click("#b-ncimp")
    fc.value.set_files("nc/bride.nc");pg.wait_for_timeout(1200)
  read()
  ok("follow-the-program window opens",pg.locator("#pg-go").count()==1)
  txt=pg.locator(".overlay:not([hidden]) .dlg").inner_text();print(txt[:900])
  ok("it says T30 is kept at the end","T30" in txt and "gardé" in txt)
  pg.screenshot(path="/tmp/pg1.png")
  pg.click("#pg-go");pg.wait_for_timeout(1200)
  got=pg.evaluate("realTools(cur.tools).map(x=>[x.t,x.type,x.diameter,x.ls||'',x.holder||'',x.code||'',x.op||'',x.corrH||''])");print(json.dumps(got,ensure_ascii=False))
  ok("program order with repeats, T30 at the end",[x[0] for x in got]==["T1","T05","T12","T05","T1","T30"],got)
  ok("sheet data kept on every repeat",got[0][4]=="PORTE FRAISE" and got[4][4]=="PORTE FRAISE" and got[3][5]=="F12" and got[2][3]=="60",got)
  ok("sheet values win (Ø 12 not replaced)",got[1][2]=="12",got)
  ok("program fills empty boxes (corrector, radius) and names the operations",got[1][7]=="5" and got[1][6]=="CONTOURNAGE EBAUCHE" and got[3][6]=="CONTOURNAGE FINITION",got)
  ok("operation columns still off",not pg.evaluate("opsVis()"))
  ok("toast with undo",pg.locator("#toast .tact").count()==1)
  pg.click("#toast .tact");pg.wait_for_timeout(800)
  ok("undo puts the sheet back",pg.evaluate("realTools(cur.tools).map(x=>x.t)")==["T12","T1","T05","T30"])
  # other choices still reach the old window
  read();pg.click("#pg-other");pg.wait_for_timeout(800)
  ok("other choices opens the normal import window",pg.locator(".impdlg").count()==1)
  pg.keyboard.press("Escape");pg.wait_for_timeout(400)
  # with names shown
  read();pg.check("#pg-ops");pg.click("#pg-go");pg.wait_for_timeout(1000)
  ok("ticking the box shows the operation names",pg.evaluate("opsVis()"))
  # empty sheet: no extra question
  pg.evaluate(f"location.hash='#m-{m}'");pg.wait_for_timeout(900);pg.click("#newa");pg.wait_for_timeout(1200)
  read();ok("empty sheet: straight to the normal import",pg.locator("#pg-go").count()==0 and pg.locator(".impdlg").count()==1)
  ok("no errors",not errs,errs)
  b.close()
print("FAILED:",[n for n,c in R if not c])
