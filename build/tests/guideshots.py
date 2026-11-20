import base64,io,json
from playwright.sync_api import sync_playwright
from PIL import Image
OUT={}
def grab(pg,key):
  png=pg.screenshot();im=Image.open(io.BytesIO(png)).convert("RGB").resize((980,581),Image.LANCZOS)
  b=io.BytesIO();im.save(b,"JPEG",quality=80,optimize=True);OUT[key]="data:image/jpeg;base64,"+base64.b64encode(b.getvalue()).decode()
with sync_playwright() as p:
  br=p.chromium.launch()
  for L in ["fr","en"]:
    # start screen: no service chosen yet
    ctx=br.new_context(viewport={"width":1470,"height":871});pg=ctx.new_page()
    pg.goto("file:///home/claude/qa/Demo.html");pg.wait_for_timeout(2000)
    if pg.locator(".langdlg").count():pg.click(f"[data-pick={L}]");pg.wait_for_timeout(400)
    pg.evaluate(f"setLang('{L}')");pg.wait_for_timeout(500);grab(pg,f"{L}_start");ctx.close()
    ctx=br.new_context(viewport={"width":1470,"height":871},accept_downloads=True);ctx.add_init_script("window.__QA_ROLE='admin'");pg=ctx.new_page()
    pg.goto("file:///home/claude/qa/Demo.html");pg.wait_for_timeout(2200);pg.evaluate(f"setLang('{L}')");pg.wait_for_timeout(400)
    H1=pg.evaluate("(db.machines.find(m=>m.abbr==='H1')||db.machines[0]).id")
    ed=pg.evaluate(f"db.articles.filter(x=>x.machineId==='{H1}'&&x.status!=='done'&&realTools(x.tools).length>=10)[0].id")
    va=pg.evaluate(f"db.articles.filter(x=>x.machineId==='{H1}'&&x.status==='done'&&realTools(x.tools).length>=8)[0].id")
    def go(h,w=1200):pg.evaluate(f"location.hash={h!r}");pg.wait_for_timeout(w)
    go("#");grab(pg,f"{L}_machines")
    go(f"#m-{H1}");grab(pg,f"{L}_machine")
    if not pg.evaluate("pvOn"):pg.evaluate("togglePreview()")
    go(f"#a-{ed}",2600);grab(pg,f"{L}_editor")
    go(f"#a-{va}",2600);grab(pg,f"{L}_validated")
    go("#crib");grab(pg,f"{L}_crib")
    go("#c-F005");grab(pg,f"{L}_code")
    go("#holders");grab(pg,f"{L}_holders")
    go(f"#mag-{H1}");grab(pg,f"{L}_mag")
    go("#log");grab(pg,f"{L}_log")
    go("#reports");grab(pg,f"{L}_reports")
    # templates: the crib's Excel model window
    go("#crib");b=pg.locator("#view button:has-text('Excel')").first;b.click();pg.wait_for_timeout(900);grab(pg,f"{L}_templates");pg.evaluate("closeDlg()")
    # backup: the restore window
    go(f"#m-{H1}");pg.click("#b-more");pg.wait_for_timeout(200);pg.click("#b-restore");pg.wait_for_timeout(900);grab(pg,f"{L}_backup");pg.evaluate("closeDlg()")
    ctx.close()
    # production: as the production service
    ctx=br.new_context(viewport={"width":1470,"height":871});ctx.add_init_script("window.__QA_ROLE='prod'");pg=ctx.new_page()
    pg.goto("file:///home/claude/qa/Demo.html");pg.wait_for_timeout(2200);pg.evaluate(f"setLang('{L}')");pg.evaluate("location.hash='#prod'");pg.wait_for_timeout(900)
    q=pg.locator("#view input[type=search]").first;q.fill("F2");pg.wait_for_timeout(900);grab(pg,f"{L}_prod")
    tk=pg.locator("#view [data-take], #view button:has-text('1')").first
    try:
      tk.click(timeout=3000);pg.wait_for_timeout(800)
    except Exception as e:print("take button?",e)
    grab(pg,f"{L}_take");ctx.close()
  br.close()
json.dump(OUT,open("guideimg.json","w"));print(len(OUT),sorted(OUT))
