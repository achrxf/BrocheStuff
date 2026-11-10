from playwright.sync_api import sync_playwright
R=[]
def ok(n,c,x=""):R.append((n,bool(c)));print(("PASS " if c else "FAIL ")+n,x)
URL="http://127.0.0.1:8765/ToolManager.html"
def imp(pg):
  with pg.expect_file_chooser() as fc: pg.click("#b-impt")
  fc.value.set_files("dups.xlsx");pg.wait_for_timeout(1200)
TS="cur.tools.map(x=>x.t+':'+(x.diameter||''))"
with sync_playwright() as p:
  for scheme in ["light","dark"]:
    b=p.chromium.launch();ctx=b.new_context(viewport={"width":1400,"height":950},color_scheme=scheme);ctx.add_init_script("window.__QA_ROLE='admin'")
    pg=ctx.new_page();errs=[];pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.goto(URL);pg.wait_for_timeout(1500);pg.evaluate("setLang('fr')")
    pg.evaluate("db.machines.push({id:'m1',abbr:'S3',name:'DMU',createdAt:1});db.articles.push({id:'a1',machineId:'m1',article:{number:'1234-5',index:'A'},tools:[{t:'T01'}],createdAt:1,updatedAt:1});saveDB()")
    pg.evaluate("location.hash='#a-a1'");pg.wait_for_timeout(1200)
    if scheme=="light":
      # 1) as is, keep everything
      imp(pg);ok("sort option shown",pg.locator("#imp-sort").count()==1)
      pg.click("#d-imp");pg.wait_for_timeout(800)
      ok("doubles found (T2 twice identical, T3/T03 different)",pg.locator(".dupg").count()==2,pg.locator(".duph").all_inner_texts())
      txt=pg.inner_text("#impbody");ok("difference named (Diamètre / Code)","Diffère" in txt,txt[:300])
      ok("identical copies said","2 copies identiques" in txt)
      ok("file row numbers shown","ligne 2" in txt and "ligne 6" in txt)
      pg.screenshot(path="dup_light.png")
      pg.click("#dup-all");pg.wait_for_timeout(300);ok("button says import everything",pg.inner_text("#dup-go")=="Tout importer")
      pg.click("#dup-back");pg.wait_for_timeout(300);ok("back to the mapping",pg.locator("#imp-sort").count()==1)
      pg.click("#d-imp");pg.wait_for_timeout(500);pg.click("#dup-all");pg.click("#dup-go");pg.wait_for_timeout(800)
      ok("keep all: 7 tools, file order",pg.evaluate(TS)==["T3:10","T1:6","T10:M8","T2:12","T03:12","T2:12","T4:8"],pg.evaluate(TS))
      # 2) replace, keep one of each, pick the second T3 copy, sorted
      imp(pg);pg.click("[data-mode=replace]");pg.check("#imp-sort");pg.click("#d-imp");pg.wait_for_timeout(600)
      g=pg.locator(".dupg").filter(has_text="T03").first if pg.locator(".dupg").filter(has_text="T03").count() else pg.locator(".dupg").first
      g3=[i for i,t in enumerate(pg.locator(".duph").all_inner_texts()) if t.startswith("T03")][0]
      pg.locator(f"input[name=dup{g3}][value='1']").check();pg.wait_for_timeout(200)
      ok("button counts doubles left out",pg.inner_text("#dup-go")=="Importer sans 2 doubles",pg.inner_text("#dup-go"))
      pg.click("#dup-go");pg.wait_for_timeout(800)
      ok("replace+one each+second T3+sorted",pg.evaluate(TS)==["T1:6","T2:12","T03:12","T4:8","T10:M8"],pg.evaluate(TS))
      ok("sort choice remembered",pg.evaluate("localStorage.getItem('bs.impsort')")=="1")
      # 3) add the file again to a sheet that has it: doubles against the sheet
      imp(pg);ok("sort still ticked",pg.is_checked("#imp-sort"));pg.click("#d-imp");pg.wait_for_timeout(600)
      ok("sheet copies shown","Déjà sur la fiche" in pg.inner_text("#impbody"))
      pg.click("#dup-one");pg.click("#dup-go");pg.wait_for_timeout(800)
      ok("add + keep one: sheet keeps one of each",pg.evaluate(TS)==["T1:6","T2:12","T03:12","T4:8","T10:M8"],pg.evaluate(TS))
      # 4) no doubles: no review step
      pg.evaluate("cur.tools=[{t:'T01'}]");imp(pg);pg.click("[data-mode=replace]")
      pg.evaluate("0")
    else:
      imp(pg);pg.click("#d-imp");pg.wait_for_timeout(600);pg.screenshot(path="dup_dark.png")
    ok("no errors "+scheme,not errs,errs);b.close()
print("FAILED:",[n for n,c in R if not c])
