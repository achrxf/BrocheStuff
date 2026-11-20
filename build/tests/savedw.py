# a person who dragged column edges at some point: saved widths, then smaller windows
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
  b=p.chromium.launch();ctx=b.new_context(viewport={"width":1920,"height":900});ctx.add_init_script("window.__QA_ROLE='admin'")
  pg=ctx.new_page();pg.goto("file:///home/claude/qa/Demo.html");pg.wait_for_timeout(2200)
  a=pg.evaluate("db.articles.find(x=>realTools(x.tools).length>5&&x.status!=='done').id");m=pg.evaluate("db.machines[0].id")
  # widen columns by dragging: in the machine list and in the tool table
  for hsh,sel in [(f"#m-{m}","#view .list table.lt thead th"),(f"#a-{a}",".tt thead tr:first-child th[data-ck=holder]")]:
    pg.evaluate(f"location.hash={hsh!r}");pg.wait_for_timeout(1500)
    th=pg.locator(sel).nth(1 if 'list' in sel else 0);bb=th.bounding_box();x=bb["x"]+bb["width"]-2;y=bb["y"]+bb["height"]/2
    pg.mouse.move(x,y);pg.mouse.down();pg.mouse.move(x+150,y,steps=6);pg.mouse.up();pg.wait_for_timeout(300)
  for w in [1920,1440,1280,1024]:
    pg.set_viewport_size({"width":w,"height":900});pg.wait_for_timeout(600)
    for hsh,box in [(f"#m-{m}","#view .list"),(f"#a-{a}",".ed .tw")]:
      pg.evaluate(f"location.hash={hsh!r}");pg.wait_for_timeout(1300)
      r=pg.evaluate(f"(()=>{{const e=document.querySelector({box!r});return e.scrollWidth+'/'+e.clientWidth}})()")
      sw,cw=map(int,r.split('/'));print(w,hsh[:3],"sideways scroll" if sw>cw+1 else "fits",r)
  b.close()
