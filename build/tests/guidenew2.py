import base64,io,json
from playwright.sync_api import sync_playwright
from PIL import Image
G=json.load(open('guideimg.json'))
def grab(pg,key):
  im=Image.open(io.BytesIO(pg.screenshot())).convert("RGB").resize((980,581),Image.LANCZOS);b=io.BytesIO();im.save(b,"JPEG",quality=80,optimize=True)
  G[key]="data:image/jpeg;base64,"+base64.b64encode(b.getvalue()).decode();im.save(f"ux/g_{key}.png")
with sync_playwright() as p:
  br=p.chromium.launch()
  for L in ["fr","en"]:
    ctx=br.new_context(viewport={"width":1470,"height":871});ctx.add_init_script("window.__QA_ROLE='admin'");pg=ctx.new_page()
    pg.goto("file:///home/claude/qa/Demo.html");pg.wait_for_timeout(2200);pg.evaluate(f"setLang('{L}')");pg.wait_for_timeout(400)
    pg.evaluate("location.hash='#arts'");pg.wait_for_timeout(1300);grab(pg,f"{L}_arts")
    pg.evaluate("location.hash='#asm'");pg.wait_for_timeout(1300);grab(pg,f"{L}_asm")
    H1=pg.evaluate("(db.machines.find(m=>m.abbr==='H1')||db.machines[0]).id")
    ed=pg.evaluate(f"db.articles.filter(x=>x.machineId==='{H1}'&&x.status!=='done'&&realTools(x.tools).length>=10)[0].id")
    if not pg.evaluate("pvOn"):pg.evaluate("togglePreview()")
    pg.evaluate(f"location.hash='#a-{ed}'");pg.wait_for_timeout(2200);pg.evaluate("setEdMode('pdf')");pg.wait_for_timeout(1200)
    pg.locator("#modepanel").scroll_into_view_if_needed();pg.wait_for_timeout(400);grab(pg,f"{L}_print")
    pg.evaluate("setEdMode('saisie')");ctx.close()
  br.close()
json.dump(G,open('guideimg.json','w'));print(len(G))
