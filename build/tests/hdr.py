import sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
  b=p.chromium.launch()
  for role in ["admin","methode","outil","prod"]:
   for w in [1920,1700,1600,1536,1440,1366,1280,1180,1100,1024,960,900,800,770]:
    ctx=b.new_context(viewport={"width":w,"height":800});ctx.add_init_script(f"window.__QA_ROLE='{role}'")
    pg=ctx.new_page();pg.goto("file:///home/claude/qa/ToolManager.html");pg.wait_for_timeout(900);pg.evaluate("setLang('fr')")
    pg.evaluate("db.machines.push({id:'m1',abbr:'S3',name:'X',createdAt:1});db.articles.push({id:'a1',machineId:'m1',article:{number:'1'},tools:[{t:'T1'}],createdAt:1,updatedAt:1});saveDB();location.hash='#a-a1'");pg.wait_for_timeout(900)
    r=pg.evaluate("(()=>{const h=document.querySelector('header.top');const nv=document.querySelector('.mainnav');const tops=[...h.children].filter(e=>e.offsetWidth).map(e=>e.getBoundingClientRect().top);return {clip:nv.scrollWidth-nv.clientWidth,h:Math.round(h.getBoundingClientRect().height),rows:new Set(tops.map(t=>Math.round(t/20))).size,menu:getComputedStyle(document.querySelector('#b-menu')).display}})()")
    print(role,w,r)
    if w==1440 and role=="admin":pg.screenshot(path="hdr1440.png",clip={"x":0,"y":0,"width":w,"height":70})
    ctx.close()
  b.close()
