from playwright.sync_api import sync_playwright
R=[]
def ok(n,c,x=""):R.append((n,bool(c)));print(("PASS " if c else "FAIL ")+n,x)
U="file:///home/claude/qa/ToolManager.html"
KEYS="makePDF(sheetData(A('a1'))).bsMeta.keys"
XK="sheetModel(A('a1'))&&makePDF(xlData(A('a1'))).bsMeta.keys"
with sync_playwright() as p:
  b=p.chromium.launch();ctx=b.new_context(viewport={"width":1500,"height":900});ctx.add_init_script("window.__QA_ROLE='admin'")
  pg=ctx.new_page();errs=[];pg.on("pageerror",lambda e:errs.append(str(e)));pg.on("console",lambda m:m.type=="error" and errs.append(m.text[:200]))
  pg.goto(U);pg.wait_for_timeout(1000);pg.evaluate("setLang('fr')")
  pg.evaluate("""db.machines.push({id:'m1',abbr:'S3',name:'X',cone:'BT50',createdAt:1});
    db.articles.push({id:'a1',machineId:'m1',article:{number:'1052',index:'A'},tools:[{t:'T52',corrH:'52',type:'FRAISE HFS CW',diameter:'20',ra:'R3',ls:'55',holder:'CÔNE FRETTÉ\\nE3416560320100',code:'F941'},{t:'T09',type:'TOURTEAU',diameter:'63',ls:'40',holder:'MANDRIN Ø22',code:'F863'}],createdAt:1,updatedAt:1});
    delete db.asmSeeded;db.assemblies=[];saveDB();location.hash='#a-a1'""");pg.wait_for_timeout(1500)
  ok("box above each column (not above Outil)",pg.locator(".tt thead [data-pr]").count()==len(pg.evaluate("visCols(sheetCfg())"))-1)
  ok("Assemblage unticked by default, others ticked",pg.evaluate("[...document.querySelectorAll('.tt thead [data-pr]')].filter(c=>!c.checked).map(c=>c.dataset.pr)")==["asm"])
  ok("PDF by default: no Assemblage",'asm' not in pg.evaluate(KEYS),pg.evaluate(KEYS))
  # tick Assemblage
  pg.check('.tt thead [data-pr=asm]');pg.wait_for_timeout(500)
  ok("ticked: Assemblage on the PDF",'asm' in pg.evaluate(KEYS),pg.evaluate(KEYS))
  ok("…and on the Excel",'asm' in pg.evaluate(XK))
  ok("saved on the sheet",pg.evaluate("JSON.stringify(A('a1').pr)")=='{"asm":true}')
  ok("message","Assemblage" in pg.inner_text("#toast"))
  n=pg.evaluate("(()=>{const d=makePDF(sheetData(A('a1')));return d.bsMeta.colw[d.bsMeta.keys.indexOf('asm')]})()");ok("Assemblage column has a real width on the PDF",n and n>=12,n)
  # untick LS
  pg.uncheck('.tt thead [data-pr=ls]');pg.wait_for_timeout(500)
  ok("LS off: not on the PDF",'ls' not in pg.evaluate(KEYS))
  ok("LS off: not on the Excel",'ls' not in pg.evaluate(XK))
  ok("LS still in the sheet (greyed header)",pg.locator('.tt thead th[data-ck=ls]').count()==1 and "np" in pg.locator('.tt thead th[data-ck=ls]').get_attribute("class"))
  ok("toggling a box is not a tool edit",pg.evaluate("(A('a1').history||[]).filter(h=>h.act==='edit'&&(h.t||[]).length).length")==0)
  pg.screenshot(path="prhead.png",clip={"x":0,"y":560,"width":900,"height":200})
  # back to the layout default -> override removed
  pg.check('.tt thead [data-pr=ls]');pg.uncheck('.tt thead [data-pr=asm]');pg.wait_for_timeout(400)
  ok("back to default: nothing stored",pg.evaluate("A('a1').pr")==None)
  # the layout: Columns window, a 'PDF / Excel' box per column, saved as a new layout
  pg.click("#b-cols");pg.wait_for_timeout(600)
  ok("Columns window: PDF / Excel box per column",pg.locator("[data-cpr]").count()>=8 and not pg.is_checked("[data-cpr=asm]") and pg.is_checked("[data-cpr=type]"))
  pg.check("[data-cpr=asm]");pg.uncheck("[data-cpr=ra]")
  pg.click("#lay-as");pg.wait_for_timeout(200);pg.fill("#lay-asname","Avec assemblage");pg.click("#lay-asok")
  pg.wait_for_timeout(600)
  L=pg.evaluate("JSON.stringify((db.layouts||[]).map(l=>({n:l.name,np:l.noprint})))");print("   layouts:",L)
  ok("layout saved with its PDF/Excel choice",'"np":["ra"]' in L,L)
  pg.evaluate("render()");pg.wait_for_timeout(800)
  ok("sheet on that layout: boxes follow it",pg.evaluate("[...document.querySelectorAll('.tt thead [data-pr]')].filter(c=>!c.checked).map(c=>c.dataset.pr)")==["ra"],pg.evaluate("[...document.querySelectorAll('.tt thead [data-pr]')].filter(c=>!c.checked).map(c=>c.dataset.pr)"))
  k=pg.evaluate(KEYS);ok("PDF follows: Assemblage on, R off",'asm' in k and 'ra' not in k,k)
  ok("blank sheet builds",pg.evaluate("blankSheet().getNumberOfPages()")>=1)
  ok("no errors",not errs,errs)
  b.close()
print("FAILED:",[n for n,c in R if not c])
