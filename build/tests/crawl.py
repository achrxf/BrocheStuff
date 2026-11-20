import re
from playwright.sync_api import sync_playwright
SKIP=re.compile(r"supprim|delete|tout supprimer|réinitialiser|reset|restaurer|restore|sortir \d|take|charger l|vider|déconnex|sign out|changer de service|quitter",re.I)
with sync_playwright() as p:
  b=p.chromium.launch();ctx=b.new_context(viewport={"width":1440,"height":900},accept_downloads=True);ctx.add_init_script("window.__QA_ROLE='admin'")
  pg=ctx.new_page();ERR=[];cur={"where":""}
  pg.on("pageerror",lambda e:ERR.append(cur["where"]+" :: "+str(e)[:200]))
  pg.on("dialog",lambda d:(ERR.append(cur["where"]+" :: browser dialog "+d.message[:60]),d.dismiss()))
  pg.on("download",lambda d:None)
  pg.goto("file:///home/claude/qa/Demo.html");pg.wait_for_timeout(2500);pg.evaluate("setLang('fr')")
  m=pg.evaluate("db.machines[0].id");a=pg.evaluate("db.articles.find(x=>realTools(x.tools).length>5&&x.status!=='done').id");c=pg.evaluate("db.catalog[0].code");h=pg.evaluate("db.holders[0].ref")
  P=[("home","#"),("machine","#m-"+m),("article","#a-"+a),("aview","#v-"+a),("arts","#arts"),("asm","#asm"),("crib","#crib"),("code","#c-"+c),("holders","#holders"),("holder","#h-"+h),("prod","#prod"),("pcode","#pc-"+c),("log","#log"),("mags","#mags"),("reports","#reports")]
  total=0
  for n,hsh in P:
    pg.evaluate(f"location.hash={hsh!r}");pg.wait_for_timeout(1200)
    labels=pg.evaluate("""[...document.querySelectorAll('#view button, #view .chip, #view [data-go], #tbar button')].filter(e=>e.offsetWidth&&!e.disabled).map((e,i)=>{e.dataset.crawl=i;return [i,(e.innerText||e.title||e.getAttribute('aria-label')||'').trim().slice(0,40)]})""")
    seen=set()
    for i,lab in labels[:60]:
      if SKIP.search(lab) or (lab in seen and lab):continue
      seen.add(lab);cur["where"]=f"{n} › {lab or '#'+str(i)}"
      try:
        el=pg.locator(f'[data-crawl="{i}"]')
        if not el.count() or not el.is_visible():continue
        el.click(timeout=3000);total+=1;pg.wait_for_timeout(350)
      except Exception as e:pass
      # close what opened, come back
      if not pg.locator("#ov").is_hidden():
        pg.evaluate("(()=>{const o=document.querySelector('#ov');delete o.dataset.lock;closeDlg()})()")
      if pg.evaluate("location.hash")!=hsh or pg.locator("[data-crawl]").count()==0:
        pg.evaluate(f"location.hash={hsh!r}");pg.wait_for_timeout(700)
        pg.evaluate("""[...document.querySelectorAll('#view button, #view .chip, #view [data-go], #tbar button')].filter(e=>e.offsetWidth&&!e.disabled).forEach((e,i)=>e.dataset.crawl=i)""")
  print("clicked",total,"controls");print("ERRORS:");[print("  ",e) for e in ERR]
  b.close()
