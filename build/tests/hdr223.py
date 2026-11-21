from playwright.sync_api import sync_playwright
with sync_playwright() as p:
  b=p.chromium.launch()
  for w in [1920,1600,1440,1366,1280,1150,1024,900,800,761,700,480,390]:
    ctx=b.new_context(viewport={"width":w,"height":800});ctx.add_init_script("window.__QA_ROLE='admin'")
    pg=ctx.new_page();pg.goto("file:///home/claude/qa/Demo.html");pg.wait_for_timeout(1500);pg.evaluate("setLang('fr')")
    a=pg.evaluate("db.articles.find(x=>realTools(x.tools).length>5&&x.status!=='done').id")
    for h in ["#","#a-"+a,"#crib","#prod"]:
      pg.evaluate(f"location.hash='{h}'");pg.wait_for_timeout(700)
      r=pg.evaluate("(()=>{const H=document.querySelector('header.top');return {h:Math.round(H.getBoundingClientRect().height),f:!document.querySelector('#b-find').hidden&&document.querySelector('#b-find').offsetWidth,sw:document.documentElement.scrollWidth}})()")
      print(w,h[:3],r)
    ctx.close()
  b.close()
