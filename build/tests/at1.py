from playwright.sync_api import sync_playwright
import sys
th=sys.argv[1] if len(sys.argv)>1 else "light"
with sync_playwright() as p:
  b=p.chromium.launch();ctx=b.new_context(viewport={"width":1440,"height":900});ctx.add_init_script("window.__QA_ROLE='admin'")
  pg=ctx.new_page();errs=[];pg.on("pageerror",lambda e:errs.append(str(e)));pg.goto("file:///home/claude/qa/Demo.html");pg.wait_for_timeout(1800)
  if pg.locator(".langdlg").count():pg.click("[data-pick=fr]")
  pg.evaluate(f"document.documentElement.dataset.theme='{th}'")
  pg.evaluate("location.hash='#crib'");pg.wait_for_timeout(900)
  pg.click("[data-cview=plan]");pg.wait_for_timeout(900);pg.screenshot(path=f"/tmp/at_plan_{th}.png")
  pg.click(".drw >> nth=7");pg.wait_for_timeout(600);pg.screenshot(path=f"/tmp/at_plan2_{th}.png")
  pg.click("[data-cf=low]");pg.wait_for_timeout(700);pg.screenshot(path=f"/tmp/at_plan3_{th}.png")
  pg.evaluate("location.hash='#'");pg.wait_for_timeout(300);pg.screenshot(path=f"/tmp/at_anim_{th}.png")
  print("errors",errs)
  b.close()
