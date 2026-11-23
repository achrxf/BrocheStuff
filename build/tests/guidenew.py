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
    H1=pg.evaluate("(db.machines.find(m=>m.abbr==='H1')||db.machines[0]).id")
    ed=pg.evaluate(f"db.articles.filter(x=>x.machineId==='{H1}'&&x.status!=='done'&&realTools(x.tools).length>=10)[0].id")
    # locations: the labels window over the crib, a few tools without location
    pg.evaluate("db.catalog.slice(0,60).forEach((c,i)=>{if(i%4==0)c.location=''})");pg.evaluate("location.hash='#crib'");pg.wait_for_timeout(1200)
    pg.click('[data-cf="noloc"]');pg.wait_for_timeout(500);grab(pg,f"{L}_loc")
    # search everywhere
    pg.keyboard.press("Control+k");pg.wait_for_timeout(300);pg.keyboard.type("F40");pg.wait_for_timeout(500);grab(pg,f"{L}_search");pg.keyboard.press("Escape")
    # operations: a sheet with operations, PDF tab
    pg.evaluate(f"""(()=>{{const a=A('{ed}');a.ops=true;const T=realTools(a.tools),out=[];const ops={json.dumps(["Ébauche","Finition","Reprise"] if L=="fr" else ["Roughing","Finishing","Rework"])};
      T.forEach((x,i)=>{{out.push({{...x,op:ops[0]+' '+(i+1),time:'0'+(i%9+1)+':'+(10+i*3%50)}});if(i%3==0)out.push({{...x,op:ops[1]+' '+(i+1),time:'0'+(i%5+2)+':05'}})}});a.tools=out}})()""")
    if not pg.evaluate("pvOn"):pg.evaluate("togglePreview()")
    pg.evaluate(f"location.hash='#a-{ed}'");pg.wait_for_timeout(2200);pg.evaluate("setEdMode('saisie')");pg.wait_for_timeout(300)
    pg.locator(".ed .tw").scroll_into_view_if_needed();pg.wait_for_timeout(400);grab(pg,f"{L}_sortsaisie")
    pg.evaluate("setEdMode('pdf')");pg.wait_for_timeout(1500);pg.locator("#modepanel").scroll_into_view_if_needed();pg.wait_for_timeout(500);grab(pg,f"{L}_sort")
    pg.evaluate("setEdMode('saisie')");ctx.close()
  br.close()
json.dump(G,open('guideimg.json','w'));print(sorted(G))
