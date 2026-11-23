O="/home/claude/qa/ux/"
def start(p,w=1440,h=900,scheme="light",url="file:///home/claude/qa/ToolManager.html",role="Préparateur méthode"):
  b=p.chromium.launch();ctx=b.new_context(viewport={"width":w,"height":h},color_scheme=scheme)
  pg=ctx.new_page();pg.errs=[];pg.on("pageerror",lambda e:pg.errs.append(str(e)))
  pg.goto(url);pg.wait_for_timeout(1200)
  if pg.get_by_text("Français").count():pg.get_by_text("Français").click();pg.wait_for_timeout(400)
  if role:
    pg.locator("#view").get_by_text(role,exact=True).first.click();pg.wait_for_timeout(500)
    if pg.locator("#view input").count():pg.keyboard.type("Achraf");pg.keyboard.press("Enter");pg.wait_for_timeout(1000)
  return b,pg
def snap(pg,n,full=False):pg.screenshot(path=O+n+".png",full_page=full)
