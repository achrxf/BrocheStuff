from playwright.sync_api import sync_playwright
with sync_playwright() as p:
  b=p.chromium.launch();ctx=b.new_context(viewport={"width":1500,"height":900});ctx.add_init_script("window.__QA_ROLE='admin'")
  pg=ctx.new_page();errs=[];pg.on("pageerror",lambda e:errs.append(str(e)));pg.goto("file:///home/claude/qa/Demo.html");pg.wait_for_timeout(2200)
  a=pg.evaluate("db.articles.find(x=>realTools(x.tools).length>5&&x.status!=='done').id");pg.evaluate(f"location.hash='#a-{a}'");pg.wait_for_timeout(1500)
  th=pg.locator('.tt thead th[data-ck=holder]');th.scroll_into_view_if_needed();w0=th.bounding_box()["width"]
  h=pg.locator('.tt thead th[data-ck=holder] .colrs').bounding_box();x,y=h["x"]+3,h["y"]+h["height"]/2
  pg.mouse.move(x,y);pg.mouse.down();pg.mouse.move(x+40,y,steps=5);pg.mouse.up();pg.wait_for_timeout(300)
  w1=th.bounding_box()["width"];cb=pg.locator('.tt thead [data-pr=holder]').bounding_box()
  print("holder width",round(w0),"->",round(w1),"| box still under it:",th.bounding_box()["x"]<=cb["x"]<=th.bounding_box()["x"]+w1,"| errors",errs)
  b.close()
