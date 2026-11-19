import json
from playwright.sync_api import sync_playwright
JS=r"""()=>{const out=[];const lum=c=>{const m=c.match(/[\d.]+/g);if(!m)return null;let [r,g,b,a]=m.map(Number);if(a===0)return null;[r,g,b]=[r,g,b].map(v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)});return .2126*r+.7152*g+.0722*b};
 const bgOf=e=>{for(let x=e;x;x=x.parentElement){const c=getComputedStyle(x).backgroundColor;if(c&&!/rgba\(0, 0, 0, 0\)|transparent/.test(c))return c}return 'rgb(255,255,255)'};
 document.querySelectorAll('#view .btn, #view button.chip, header.top .tb, #view .laysel').forEach(e=>{if(!e.offsetWidth||e.closest('[hidden]'))return;const r=e.getBoundingClientRect();if(r.bottom<0||r.top>window.innerHeight*3)return;const cs=getComputedStyle(e);
   const L1=lum(cs.color),L2=lum(bgOf(e));const cr=(L1!=null&&L2!=null)?(Math.max(L1,L2)+.05)/(Math.min(L1,L2)+.05):null;
   out.push({cls:(e.className||'').toString().split(' ').filter(c=>!['row'].includes(c)).join('.'),txt:(e.innerText||e.title||'').trim().slice(0,22),h:Math.round(r.height),rad:cs.borderTopLeftRadius,fs:cs.fontSize,cr:cr&&Math.round(cr*10)/10})});return out}"""
with sync_playwright() as p:
  b=p.chromium.launch();res={}
  for scheme in ["light","dark"]:
    ctx=b.new_context(viewport={"width":1440,"height":900},color_scheme=scheme);ctx.add_init_script("window.__QA_ROLE='admin'")
    pg=ctx.new_page();pg.goto("file:///home/claude/qa/Demo.html");pg.wait_for_timeout(2500);pg.evaluate("setLang('fr')")
    m=pg.evaluate("db.machines[0].id");a=pg.evaluate("db.articles.find(x=>realTools(x.tools).length>5&&x.status!=='done').id");c=pg.evaluate("db.catalog[0].code");h=pg.evaluate("db.holders[0].ref")
    for n,hsh in [("home","#"),("machine","#m-"+m),("article","#a-"+a),("aview","#v-"+a),("arts","#arts"),("asm","#asm"),("crib","#crib"),("code","#c-"+c),("holders","#holders"),("holder","#h-"+h),("prod","#prod"),("log","#log"),("mags","#mags"),("reports","#reports")]:
      pg.evaluate(f"location.hash={hsh!r}");pg.wait_for_timeout(900)
      for it in pg.evaluate(JS):
        it["page"]=n;it["scheme"]=scheme;res.setdefault(scheme,[]).append(it)
    ctx.close()
  b.close()
json.dump(res,open("audit.json","w"))
for scheme,L in res.items():
  low=[x for x in L if x["cr"] and x["cr"]<3.0]
  print(scheme,"buttons:",len(L),"| low contrast (<3):",len(low))
  for x in low[:25]:print("   ",x["page"],x["cls"],repr(x["txt"]),x["cr"])
  from collections import Counter
  print("  heights .btn:",Counter((x["h"]) for x in L if x["cls"].startswith("btn") and "sm" not in x["cls"].split(".")).most_common(8))
  print("  heights .btn.sm:",Counter((x["h"]) for x in L if "sm" in x["cls"].split(".")).most_common(6))
  print("  radius .btn:",Counter((x["rad"]) for x in L if x["cls"].startswith("btn")).most_common(6))
  odd=[x for x in L if x["cls"].startswith("btn") and "sm" not in x["cls"].split(".") and x["h"] not in (36,)]
  from itertools import groupby
  seen=set()
  for x in odd:
    k=(x["page"],x["cls"],x["h"])
    if k in seen:continue
    seen.add(k);print("    odd h",x["page"],x["cls"],repr(x["txt"]),x["h"],x["fs"])
