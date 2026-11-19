from playwright.sync_api import sync_playwright
with sync_playwright() as p:
  b=p.chromium.launch()
  for role in ["admin","methode","outil","prod"]:
    ctx=b.new_context(viewport={"width":1440,"height":900});ctx.add_init_script(f"window.__QA_ROLE='{role}'")
    pg=ctx.new_page();errs=[];pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.goto("file:///home/claude/qa/ToolManager.html");pg.wait_for_timeout(900);pg.evaluate("location.hash='#asm'");pg.wait_for_timeout(600)
    print(role,"menu:",pg.locator("#nav-s").is_visible(),"| opens page:",pg.locator(".asmp").count()==1,"| new button:",pg.locator("#asm-new").count()==1,"| errors:",errs)
    ctx.close()
  b.close()
