from playwright.sync_api import sync_playwright
from PIL import Image
with sync_playwright() as p:
  b=p.chromium.launch();ctx=b.new_context(viewport={"width":390,"height":844},is_mobile=True,has_touch=True);ctx.add_init_script("window.__QA_ROLE='admin'")
  pg=ctx.new_page();errs=[];pg.on("pageerror",lambda e:errs.append(str(e)));pg.goto("file:///home/claude/qa/Demo.html");pg.wait_for_timeout(1800)
  if pg.locator(".langdlg").count():pg.click("[data-pick=fr]")
  m=pg.evaluate("db.machines[0].id");a=pg.evaluate("db.articles.find(x=>realTools(x.tools).length>5).id")
  fs=[]
  for n,h in [("home","#"),("machine","#m-"+m),("article","#a-"+a),("crib","#crib")]:
    pg.evaluate(f"location.hash={h!r}");pg.wait_for_timeout(1300)
    if n=="crib":pg.click("[data-cview=plan]");pg.wait_for_timeout(700)
    ow=pg.evaluate("document.documentElement.scrollWidth>innerWidth+1||[...document.querySelectorAll('#view *')].some(e=>{const r=e.getBoundingClientRect();return r.right>innerWidth+2&&getComputedStyle(e).position!=='fixed'&&!e.closest('.list,.tw,[style*=overflow],.lt,.pv,.plan .cabs')})")
    print(n,"overflow:",ow);f=f"/tmp/mob_{n}.png";pg.screenshot(path=f);fs.append(f)
  o=Image.new("RGB",(390*4+30,844),"white")
  for i,f in enumerate(fs):o.paste(Image.open(f),(i*400,0))
  o.save("/tmp/mob_sheet.png");print(errs);b.close()
