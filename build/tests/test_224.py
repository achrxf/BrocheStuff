from playwright.sync_api import sync_playwright
R=[]
def ok(n,c,x=""):R.append((n,bool(c)));print(("PASS " if c else "FAIL ")+n,x)
with sync_playwright() as p:
  b=p.chromium.launch()
  for role in ["admin","outil","methode","prod"]:
    ctx=b.new_context(viewport={"width":1440,"height":900});ctx.add_init_script(f"window.__QA_ROLE='{role}'")
    pg=ctx.new_page();errs=[];pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.goto("file:///home/claude/qa/Demo.html");pg.wait_for_timeout(1500);pg.evaluate("setLang('fr')")
    if not pg.evaluate("$('#ov').hidden"):pg.keyboard.press("Escape")
    pg.evaluate("window.printHTML=(h)=>{window.__ph=h;return Promise.resolve()}")
    ed=pg.evaluate("hasRight('cribEdit')")
    if pg.evaluate("can('crib')"):
      pg.evaluate("db.catalog[0].location='';saveDB();location.hash='#crib'");pg.wait_for_timeout(900)
      ok(role+": crib no-location chip",pg.locator('[data-cf=noloc]').count()==1)
      pg.click('[data-cf=noloc]');pg.wait_for_timeout(400)
      ok(role+": filter shows only tools without location",pg.evaluate("[...document.querySelectorAll('#crows tr')].every(tr=>!C_(tr.dataset.code).location)"))
      ok(role+": + location only with the right",(pg.locator('#crows .locadd').count()>0)==ed)
      ok(role+": labels button",pg.locator('#b-labels').count()==1)
      pg.click('#b-labels');pg.wait_for_timeout(300);pg.click('#lb-ok');pg.wait_for_timeout(200)
      ok(role+": labels print",pg.evaluate("!!(window.__ph&&window.__ph.body.includes('class=\"lb\"'))"))
    if pg.evaluate("can('article')"):
      aid=pg.evaluate("db.articles.filter(a=>realTools(a.tools).length>14&&a.status!=='done')[0].id")
      pg.evaluate(f"location.hash='#a-{aid}'");pg.wait_for_timeout(1300)
      ok(role+": drawing toggle",pg.locator('#b-tdtog').count()==1)
      pg.click('#b-tdtog');pg.wait_for_timeout(200);ok(role+": drawing hidden",not pg.is_visible('.ed .tdiag.wide'))
      pg.click('#b-tdtog');pg.wait_for_timeout(200);ok(role+": drawing back",pg.is_visible('.ed .tdiag.wide'))
      ok(role+": sticky titles",pg.evaluate("getComputedStyle(document.querySelector('.tt thead th')).position")=="sticky")
    if pg.evaluate("can('aview')"):
      aid=pg.evaluate("db.articles.filter(a=>realTools(a.tools).length>8)[0].id")
      pg.evaluate(f"location.hash='#v-{aid}'");pg.wait_for_timeout(900)
      if pg.locator("#b-prep, [data-prep]").count():
        pg.locator("#b-prep, [data-prep]").first.click();pg.wait_for_timeout(300)
      else: pg.evaluate(f"prepDialog(A('{aid}'))");pg.wait_for_timeout(300)
      if pg.locator('#pp-print').count():
        pg.click('#pp-print');pg.wait_for_timeout(200);ok(role+": pick list print",pg.evaluate("!!(window.__ph&&window.__ph.body.includes('<table>'))"))
      pg.keyboard.press("Escape")
    ok(role+": no errors",not errs,errs)
    ctx.close()
  b.close()
print("FAILED:",[n for n,c in R if not c])
