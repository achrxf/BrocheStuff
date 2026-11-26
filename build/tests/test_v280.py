from playwright.sync_api import sync_playwright
import json,sys
R=[]
def ok(n,c,x=""):R.append((n,bool(c)));print(("PASS " if c else "FAIL ")+n,x if not c else "")
SHOT="/tmp/v280"
import os;os.makedirs(SHOT,exist_ok=True)
with sync_playwright() as p:
  b=p.chromium.launch();ctx=b.new_context(viewport={"width":1600,"height":950});ctx.add_init_script("window.__QA_ROLE='admin'")
  pg=ctx.new_page();errs=[];pg.on("pageerror",lambda e:errs.append(str(e)));pg.goto("file:///home/claude/qa/Demo.html");pg.wait_for_timeout(2000)
  if pg.locator(".langdlg").count():pg.click("[data-pick=fr]")
  m=pg.evaluate("db.machines.find(x=>x.abbr==='H1').id")
  pg.evaluate(f"""(()=>{{const L=asmList();const mk=(code,tool,tn)=>{{const a={{id:uid(),code,tool,sig:asmSig(tool),auto:0,keep:1,tnum:tn,createdAt:Date.now()}};L.push(a);return a}};
    mk('AS0901',{{type:'FRAISE 2T',diameter:'12',ls:'45',holder:'FRETTE HSK63\\nE3416',code:'FR12A'}},{{'{m}':'T12'}});
    mk('AS0902',{{type:'FRAISE 2T',diameter:'12',ls:'60',holder:'FRETTE HSK63 LONG',code:'FR12B'}},{{'{m}':'T12'}});
    mk('AS0903',{{type:'FORET',diameter:'8.5',ls:'70',holder:'MANDRIN HSK63',code:'D85X'}},{{'{m}':'T05'}});saveDB();return 1}})()""")
  pg.evaluate(f"location.hash='#m-{m}'");pg.wait_for_timeout(900);pg.click("#newa");pg.wait_for_timeout(1400)
  cell=lambda i,k:pg.locator(f'#rows tr[data-i="{i}"] [data-k="{k}"]').first
  # 1. T typed -> the two assemblies with T12 on H1
  cell(0,"t").fill("T12");cell(0,"t").press("Tab");pg.wait_for_timeout(500)
  ok("T12 typed: picker opens",pg.locator(".apk:not(.hov)").count()==1)
  codes=pg.evaluate("[...document.querySelectorAll('.apk .apc')].map(e=>e.dataset.apk||'L'+e.dataset.apline)")
  ok("both assemblies with T12 on this machine",codes==["AS0901","AS0902"],codes)
  ok("cards show type, Ø, holder, code, T chip","FRAISE 2T" in pg.locator(".apk").inner_text() and "FR12B" in pg.locator(".apk").inner_text() and pg.locator(".apk .apt.here").count()==2)
  pg.screenshot(path=SHOT+"/1-picker.png")
  pg.keyboard.press("ArrowDown");pg.keyboard.press("Enter");pg.wait_for_timeout(700)
  x=pg.evaluate("cur.tools[0]");ok("arrow+Enter takes AS0902 and fills the row",x.get("asm")=="AS0902" and x.get("ls")=="60" and x.get("code")=="FR12B" and x.get("t")=="T12",x)
  ok("picker closed",pg.locator(".apk:not(.hov)").count()==0)
  # 2. same T on another line -> "same as line 1" first
  pg.evaluate("cur.tools.push({t:''},{t:''},{t:''},{t:''});renderRows();1")
  cell(1,"op").fill("FINITION") if pg.locator('#rows tr[data-i="1"] [data-k="op"]').count() else None
  cell(1,"t").fill("T12");cell(1,"t").press("Tab");pg.wait_for_timeout(500)
  codes=pg.evaluate("[...document.querySelectorAll('.apk .apc')].map(e=>e.dataset.apk||'L'+e.dataset.apline)")
  ok("same T in the sheet: 'same as line 1' offered first, then the assemblies",codes==["L0","AS0901","AS0902"],codes)
  pg.screenshot(path=SHOT+"/2-sameT.png")
  pg.locator(".apk .apc.line").click();pg.wait_for_timeout(600)
  x=pg.evaluate("cur.tools[1]");ok("copying the line fills the empty boxes (asm too)",x.get("ls")=="60" and x.get("asm")=="AS0902" and x.get("holder")=="FRETTE HSK63 LONG",x)
  ok("blue dot on both T12 lines",pg.locator('#rows .tdot.ok').count()==2,pg.evaluate("[...document.querySelectorAll('#rows .tdot')].map(e=>e.className)"))
  # 3. picker skip: Esc closes, nothing filled
  cell(2,"t").fill("T05");cell(2,"t").press("Tab");pg.wait_for_timeout(400);ok("T05: picker with AS0903",pg.locator('.apk .apc[data-apk="AS0903"]').count()==1)
  pg.keyboard.press("Escape");pg.wait_for_timeout(300);ok("Esc closes, row untouched",pg.locator(".apk:not(.hov)").count()==0 and not pg.evaluate("cur.tools[2].asm"))
  # 4. Assembly box: searchable picker
  cell(3,"asm").click();pg.wait_for_timeout(300);ok("assembly box opens the picker",pg.locator(".apk:not(.hov)").count()==1)
  pg.keyboard.type("8.5");pg.wait_for_timeout(300)
  codes=pg.evaluate("[...document.querySelectorAll('.apk .apc')].map(e=>e.dataset.apk)");ok("search by Ø finds AS0903 only",codes==["AS0903"],codes)
  pg.screenshot(path=SHOT+"/3-search.png")
  pg.keyboard.press("Enter");pg.wait_for_timeout(600);x=pg.evaluate("cur.tools[3]")
  ok("Enter takes it: row filled and T comes from the machine",x.get("asm")=="AS0903" and x.get("code")=="D85X" and x.get("t")=="T05",x)
  pg.keyboard.press("Escape")
  ok("no plain datalist on the assembly box",pg.locator('#rows input[data-k="asm"][list]').count()==0)
  # 5. dots: T05 on rows 2 and 3, row 2 empty -> orange
  pg.wait_for_timeout(300);st=pg.evaluate("[...document.querySelectorAll('#rows tr[data-i=\"2\"] .tdot,#rows tr[data-i=\"3\"] .tdot')].map(e=>e.className)")
  ok("T05 with empty boxes on one line: orange dot",all("miss" in c for c in st) and len(st)==2,st)
  # conflict: change LS on row 1
  pg.evaluate("cur.tools[1].ls='61';renderRows();1");pg.wait_for_timeout(200)
  ok("T12 with LS 60 / 61: red dot",pg.locator('#rows tr[data-i="0"] .tdot.bad').count()==1)
  ok("tooltip names the box",'LS' in (pg.locator('#rows tr[data-i="0"] .tdot').get_attribute("title") or ""))
  pg.locator('#rows tr[data-i="0"] .tdot').click();pg.wait_for_timeout(400)
  ok("dot click opens the same-tool window",pg.locator(".rpt").count()==1)
  pg.screenshot(path=SHOT+"/4-rep.png")
  pg.locator('.rpt tr[data-rk="ls"] .rpv[data-rj="1"]').click();pg.click("#rp-go");pg.wait_for_timeout(500)
  ok("choosing 61 puts 61 on both lines",pg.evaluate("[cur.tools[0].ls,cur.tools[1].ls]")==["61","61"])
  ok("dot back to blue",pg.locator('#rows tr[data-i="0"] .tdot.ok').count()==1)
  pg.click("#toast .tact");pg.wait_for_timeout(400);ok("undo",pg.evaluate("[cur.tools[0].ls,cur.tools[1].ls]")==["60","61"])
  # 6. check panel
  pg.wait_for_timeout(700);ok("check button with a count",pg.locator("#b-chk").count()==1 and "·" in pg.locator("#b-chk").inner_text(),pg.locator("#b-chk").inner_text() if pg.locator("#b-chk").count() else "")
  pg.click("#b-chk");pg.wait_for_timeout(400);txt=pg.locator("#ov .dlg").inner_text();print(txt[:900])
  ok("check lists the T12 conflict and the missing info","T12" in txt and "pas le même outil" in txt and "Infos de la fiche" in txt)
  pg.screenshot(path=SHOT+"/5-check.png")
  pg.locator("#ov [data-ckfix]").first.click();pg.wait_for_timeout(500);ok("Fix opens the same-tool window",pg.locator(".rpt").count()==1)
  pg.keyboard.press("Escape");pg.wait_for_timeout(200)
  pg.click("#b-chk");pg.wait_for_timeout(300);pg.locator("#ov [data-ckgo]").nth(2).click();pg.wait_for_timeout(700)
  ok("Go there closes and highlights a row",pg.locator("#ov .dlg").count()==0 and pg.locator("#rows tr.ckflash").count()==1)
  # 7. assembly page: twins shown
  pg.evaluate("location.hash='#asm'");pg.wait_for_timeout(1200)
  ok("assemblies page notes the shared T12",pg.locator(".asmtw").count()>=2,pg.locator(".asmtw").count())
  pg.screenshot(path=SHOT+"/6-asmpage.png")
  # 8. hover card
  pg.evaluate(f"history.back()");pg.wait_for_timeout(1200)
  if pg.locator('#rows tr[data-i="0"] [data-k="asm"]').count():
    pg.locator('#rows tr[data-i="0"] [data-k="asm"]').hover();pg.wait_for_timeout(700);ok("hover shows the assembly card",pg.locator("#aphov .apc").count()==1)
  ok("no errors",not errs,errs)
  b.close()
print("FAILED:",[n for n,c in R if not c])
