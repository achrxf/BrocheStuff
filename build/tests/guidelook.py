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
    ctx=br.new_context(viewport={"width":1470,"height":871},reduced_motion="reduce");ctx.add_init_script("window.__QA_ROLE='admin'");pg=ctx.new_page()
    pg.goto("file:///home/claude/qa/Demo.html");pg.wait_for_timeout(2200);pg.evaluate(f"setLang('{L}')");pg.wait_for_timeout(400)
    pg.evaluate("location.hash='#crib'");pg.wait_for_timeout(1200);pg.click("[data-cview=plan]");pg.wait_for_timeout(900)
    pg.click(".drw >> nth=15");pg.wait_for_timeout(500);pg.evaluate("document.querySelector('.plan').scrollIntoView({block:'start'})");pg.evaluate("document.querySelector('#view').scrollTop-=90");pg.wait_for_timeout(400)
    grab(pg,f"{L}_look");ctx.close()
  br.close()
json.dump(G,open('guideimg.json','w'));print(len(G))
