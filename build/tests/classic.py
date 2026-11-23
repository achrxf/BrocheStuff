from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops
def shots(url,classic,tag):
  with sync_playwright() as p:
    b=p.chromium.launch();ctx=b.new_context(viewport={"width":1440,"height":900},reduced_motion="reduce");ctx.add_init_script("window.__QA_ROLE='admin';"+("try{localStorage.setItem('bs.skin','classic')}catch(e){}" if classic else ""))
    pg=ctx.new_page();errs=[];pg.on("pageerror",lambda e:errs.append(str(e)));pg.goto(url);pg.wait_for_timeout(1800)
    if pg.locator(".langdlg").count():pg.click("[data-pick=fr]")
    m=pg.evaluate("db.machines[0].id");a=pg.evaluate("db.articles.find(x=>realTools(x.tools).length>5).id")
    out=[]
    for n,h in [("home","#"),("machine","#m-"+m),("article","#a-"+a),("crib","#crib"),("log","#log")]:
      pg.evaluate(f"location.hash={h!r}");pg.wait_for_timeout(1500);f=f"/tmp/cl_{tag}_{n}.png";pg.screenshot(path=f);out.append(f)
    print(tag,"cls:",pg.evaluate("document.documentElement.className"),"errs",errs);b.close();return out
A=shots("file:///home/claude/qa/DemoOld.html",False,"old")
B=shots("file:///home/claude/qa/Demo.html",True,"cls")
for x,y in zip(A,B):
  d=ImageChops.difference(Image.open(x).convert("RGB"),Image.open(y).convert("RGB")).getbbox();print(x.split("_")[-1],"diff box:",d)
