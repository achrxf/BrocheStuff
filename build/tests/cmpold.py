from playwright.sync_api import sync_playwright
import json,sys
def grab(url):
  with sync_playwright() as p:
    b=p.chromium.launch();ctx=b.new_context(viewport={"width":1400,"height":900});ctx.add_init_script("window.__QA_ROLE='admin'")
    pg=ctx.new_page();pg.goto(url);pg.wait_for_timeout(1500);pg.evaluate("setLang('fr')")
    r=pg.evaluate("db.articles.slice(0,40).map(a=>{const m=makePDF(sheetData(a)).bsMeta,x=makePDF(xlData(a)).bsMeta;return [a.id,m.keys.join(','),m.colw.map(v=>Math.round(v*10)).join(','),x.keys.join(','),sheetData(a).tools.length]})")
    b.close();return r
old=grab("file:///tmp/claude-0/old.html");new=grab("file:///home/claude/qa/Demo.html")
d=[(o,n) for o,n in zip(old,new) if o!=n];print("differences:",len(d));[print(x) for x in d[:3]]
