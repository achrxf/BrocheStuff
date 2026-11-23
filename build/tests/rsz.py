from playwright.sync_api import sync_playwright
from uxlib import *
import sys
W=int(sys.argv[1]) if len(sys.argv)>1 else 1440
with sync_playwright() as p:
  b,pg=start(p,w=W,url="file:///home/claude/qa/Demo.html",role="Préparateur méthode")
  aid=pg.evaluate("db.articles.filter(a=>realTools(a.tools).length>8&&a.status!=='done')[0].id")
  pg.evaluate(f"location.hash='#a-{aid}'");pg.wait_for_timeout(1500)
  ws=lambda:pg.evaluate("[...document.querySelectorAll('.tt thead tr:first-child th[data-ck]')].map(th=>th.dataset.ck+':'+Math.round(th.getBoundingClientRect().width)).join(' ')")
  print("start",ws())
  for k,dx in [("holder",60),("holder",-60),("ls",40),("type",-40)]:
    h=pg.locator(f'.tt thead th[data-ck="{k}"] .colrs')
    if not h.count():print("no handle",k);continue
    bb=h.bounding_box();x=bb["x"]+bb["width"]/2;y=bb["y"]+bb["height"]/2
    pg.mouse.move(x,y);pg.mouse.down();pg.mouse.move(x+dx/2,y,steps=4);pg.mouse.move(x+dx,y,steps=4);pg.mouse.up();pg.wait_for_timeout(400)
    print(k,dx,ws(),"saved",pg.evaluate("lsGet('toollistmaker.colw')"))
  print(pg.errs);b.close()
