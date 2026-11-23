from playwright.sync_api import sync_playwright
import sys
th=sys.argv[1] if len(sys.argv)>1 else "light"
with sync_playwright() as p:
  b=p.chromium.launch();ctx=b.new_context(viewport={"width":1440,"height":900})
  pg=ctx.new_page();errs=[];pg.on("pageerror",lambda e:errs.append(str(e)));pg.goto("file:///home/claude/qa/Demo.html");pg.wait_for_timeout(1800)
  pg.evaluate(f"document.documentElement.dataset.theme='{th}'")
  pg.screenshot(path=f"/tmp/at_lang_{th}.png")
  pg.click("[data-pick=fr]");pg.wait_for_timeout(700);pg.screenshot(path=f"/tmp/at_gate_{th}.png")
  pg.click("[data-role=methode]");pg.wait_for_timeout(500);pg.locator("input:visible").first.fill("Achraf");pg.keyboard.press("Enter");pg.wait_for_timeout(1500)
  a=pg.evaluate("db.articles.find(x=>realTools(x.tools).length>8&&x.status!=='done').id")
  pg.evaluate(f"location.hash='#a-{a}'");pg.wait_for_timeout(2000);pg.screenshot(path=f"/tmp/at_ed_{th}.png")
  pg.click("#b-more");pg.wait_for_timeout(400);pg.screenshot(path=f"/tmp/at_menu_{th}.png");pg.keyboard.press("Escape")
  pg.evaluate("location.hash='#m-'+db.machines[0].id");pg.wait_for_timeout(900);pg.click("#newa");pg.wait_for_timeout(500);pg.screenshot(path=f"/tmp/at_dlg_{th}.png")
  print("errors",errs)
  b.close()
