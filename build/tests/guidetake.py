import base64,io,json
from playwright.sync_api import sync_playwright
from PIL import Image
G=json.load(open('guideimg.json'))
with sync_playwright() as p:
  br=p.chromium.launch()
  for L,lab in [("fr","Sortir 1"),("en","Take 1")]:
    ctx=br.new_context(viewport={"width":1470,"height":871});ctx.add_init_script("window.__QA_ROLE='prod'");pg=ctx.new_page()
    pg.goto("file:///home/claude/qa/Demo.html");pg.wait_for_timeout(2200);pg.evaluate(f"setLang('{L}')");pg.evaluate("location.hash='#prod'");pg.wait_for_timeout(900)
    pg.locator("#view input[type=search]").first.fill("F2");pg.wait_for_timeout(900)
    pg.locator(f"#view button:has-text('{lab}')").first.click();pg.wait_for_timeout(900)
    print(L,"dialog open:",not pg.locator("#ov").is_hidden())
    im=Image.open(io.BytesIO(pg.screenshot())).convert("RGB").resize((980,581),Image.LANCZOS);b=io.BytesIO();im.save(b,"JPEG",quality=80,optimize=True)
    G[f"{L}_take"]="data:image/jpeg;base64,"+base64.b64encode(b.getvalue()).decode();im.save(f"take_{L}.png");ctx.close()
  br.close()
json.dump(G,open('guideimg.json','w'))
