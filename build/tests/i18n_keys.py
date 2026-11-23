from playwright.sync_api import sync_playwright
import json
with sync_playwright() as p:
  b=p.chromium.launch();pg=b.new_page();pg.add_init_script("window.__QA_ROLE='admin'")
  pg.goto("file:///home/claude/qa/Demo.html");pg.wait_for_timeout(1500)
  r=pg.evaluate("""(()=>{const E=I18N.en,F=I18N.fr,ke=Object.keys(E),kf=Object.keys(F);
   const onlyE=ke.filter(k=>!(k in F)),onlyF=kf.filter(k=>!(k in E));
   const same=ke.filter(k=>k in F&&typeof E[k]==="string"&&E[k]===F[k]&&/[a-z]{4}/i.test(E[k]));
   return {onlyE:onlyE.map(k=>[k,String(E[k]).slice(0,60)]),onlyF:onlyF.map(k=>[k,String(F[k]).slice(0,60)]),same:same.map(k=>[k,E[k].slice(0,60)])}})()""")
  print(json.dumps(r,ensure_ascii=False,indent=0)[:6000])
  b.close()
