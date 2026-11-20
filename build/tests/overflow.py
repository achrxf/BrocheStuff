import sys,json
from playwright.sync_api import sync_playwright
JS=r"""()=>{const out=[];const D=document.documentElement,V=document.querySelector('#view');
  out.push({el:'document',sw:D.scrollWidth,cw:D.clientWidth});if(V)out.push({el:'#view',sw:V.scrollWidth,cw:V.clientWidth,ox:getComputedStyle(V).overflowX});
  document.querySelectorAll('#view *').forEach(e=>{const cs=getComputedStyle(e);if(!/(auto|scroll)/.test(cs.overflowX))return;if(e.scrollWidth>e.clientWidth+1&&e.offsetWidth)out.push({el:(e.id?'#'+e.id:'')+'.'+String(e.className).split(' ').join('.'),sw:e.scrollWidth,cw:e.clientWidth})});
  return out}"""
pages=sys.argv[2:] if len(sys.argv)>2 else None
with sync_playwright() as p:
  b=p.chromium.launch()
  for w in [int(x) for x in sys.argv[1].split(',')]:
    ctx=b.new_context(viewport={"width":w,"height":900});ctx.add_init_script("window.__QA_ROLE='admin'")
    pg=ctx.new_page();pg.goto("file:///home/claude/qa/Demo.html");pg.wait_for_timeout(2200);pg.evaluate("setLang('fr')")
    m=pg.evaluate("db.machines[0].id");a=pg.evaluate("db.articles.find(x=>realTools(x.tools).length>5&&x.status!=='done').id");c=pg.evaluate("db.catalog[0].code");h=pg.evaluate("db.holders[0].ref")
    P=[("home","#"),("machine","#m-"+m),("article","#a-"+a),("aview","#v-"+a),("arts","#arts"),("asm","#asm"),("crib","#crib"),("code","#c-"+c),("holders","#holders"),("holder","#h-"+h),("prod","#prod"),("log","#log"),("mags","#mags"),("mag","#g-"+m),("reports","#reports"),("guide","#guide")]
    for n,hsh in P:
      pg.evaluate(f"location.hash={hsh!r}");pg.wait_for_timeout(1300 if n in("article","aview") else 600)
      r=[x for x in pg.evaluate(JS) if x['sw']>x['cw']+1]
      if r:print(w,n,json.dumps(r)[:400])
    ctx.close()
  b.close()
