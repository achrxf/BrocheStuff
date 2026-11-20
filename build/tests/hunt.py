import sys,json
from playwright.sync_api import sync_playwright
R=[];ERR=[]
def ok(n,c,x=""):R.append((n,bool(c)));print(("PASS " if c else "FAIL ")+n,str(x)[:300])
U="file:///home/claude/qa/ToolManager.html"
def cell(pg,i,k):return pg.locator(f'#rows tr[data-i="{i}"] input[data-k="{k}"]').first
with sync_playwright() as p:
  b=p.chromium.launch()
  ctx=b.new_context(viewport={"width":1500,"height":950},accept_downloads=True);ctx.add_init_script("window.__QA_ROLE='admin'")
  ctx.grant_permissions(["clipboard-read","clipboard-write"])
  pg=ctx.new_page();pg.on("pageerror",lambda e:ERR.append("pageerror: "+str(e)));pg.on("console",lambda m:m.type=="error" and ERR.append("console: "+m.text[:200]))
  pg.on("dialog",lambda d:(ERR.append("browser dialog: "+d.message[:80]),d.dismiss()))
  pg.goto(U);pg.wait_for_timeout(1000);pg.evaluate("setLang('fr')")
  pg.evaluate("""db.machines.push({id:'m1',abbr:'S3',name:'TOYODA',cone:'BT50',createdAt:1},{id:'m2',abbr:'H1',name:'DMU',cone:'HSK63',createdAt:1});
    db.catalog.push({code:'F941',type:'FRAISE HFS CW',diameter:'20',ra:'R3',z:'4',stock:3});db.holders.push({ref:'BT50-ER32-100',type:'PINCE ER',cone:'BT50',stock:2});
    db.articles.push({id:'a1',machineId:'m1',article:{number:'1052',index:'A',designation:'TRACK',program:'O1337'},tools:[{t:'T01'}],createdAt:1,updatedAt:1});saveDB();location.hash='#a-a1'""");pg.wait_for_timeout(1500)
  # 1 typing a row, Enter on the last row adds a row and keeps the column
  cell(pg,0,"type").fill("fraise 2t");cell(pg,0,"diameter").fill("12");cell(pg,0,"ls").fill("40");cell(pg,0,"holder").fill("BT50-ER32-100");cell(pg,0,"code").fill("F941");cell(pg,0,"code").dispatch_event("change");pg.wait_for_timeout(500)
  if pg.locator("#fill-keep").count():pg.click("#fill-keep");pg.wait_for_timeout(300)
  cell(pg,0,"ls").press("Enter");pg.wait_for_timeout(300)
  ok("Enter on last row adds a row",pg.evaluate("cur.tools.length")==2)
  ok("…focus goes to the new row",pg.evaluate("+document.activeElement.closest('tr').dataset.i")==1)
  ok("new row numbered T02",pg.evaluate("cur.tools[1].t")=="T02")
  ok("T01 correctors: H and D from the tool number",pg.evaluate("cur.tools[0].corrH")=="1" and pg.evaluate("cur.tools[0].corrD")=="1",pg.evaluate("cur.tools[0]"))
  # 2 Shift+Enter: second line in the holder
  h=cell(pg,0,"holder");h.click();pg.keyboard.press("End");pg.keyboard.press("Shift+Enter");pg.keyboard.type("+ ALLONGE 50");pg.wait_for_timeout(300)
  ok("Shift+Enter makes a 2nd line in the holder",pg.evaluate("cur.tools[0].holder")=="BT50-ER32-100\n+ ALLONGE 50",pg.evaluate("cur.tools[0].holder"))
  pg.keyboard.press("Home");pg.keyboard.press("Backspace");pg.wait_for_timeout(200)
  ok("Backspace at start joins the lines back",pg.evaluate("cur.tools[0].holder").startswith("BT50-ER32-100"),repr(pg.evaluate("cur.tools[0].holder")))
  # 3 paste several rows from Excel
  pg.evaluate("cur.tools.push({t:'T03'});renderRows()")
  txt="T05\tFORET\t8\t\t45\n\tTARAUD M8\t8\t\t30\n"
  el=cell(pg,2,"t");el.click()
  pg.evaluate("([t])=>{const dt=new DataTransfer();dt.setData('text',t);const e=new ClipboardEvent('paste',{clipboardData:dt,bubbles:true,cancelable:true});document.activeElement.dispatchEvent(e)}",[txt]);pg.wait_for_timeout(500)
  T=pg.evaluate("cur.tools.map(x=>[x.t,x.type||'',x.diameter||'',x.ls||'',x.corrH||''])");ok("paste of 2 rows from Excel lands in Outil/Type/Ø/R/LS",["T05","FORET","8","45",""] in T and any(r[1]=="TARAUD M8" and r[3]=="30" for r in T),T)
  # 4 row arrows and delete
  n0=pg.evaluate("cur.tools.length");pg.locator('#rows tr[data-i="1"] [data-r="up"]').click();pg.wait_for_timeout(200)
  ok("↑ moves a row up",pg.evaluate("cur.tools[0].t")=="T02",pg.evaluate("cur.tools.map(x=>x.t)"))
  pg.locator('#rows tr[data-i="0"] [data-r="down"]').click();pg.wait_for_timeout(200)
  pg.locator(f'#rows tr[data-i="{n0-1}"] [data-r="del"]').click();pg.wait_for_timeout(200)
  ok("✕ removes a row",pg.evaluate("cur.tools.length")==n0-1)
  # 5 sort and undo
  bef=pg.evaluate("cur.tools.map(x=>x.t)");pg.select_option("#a-sort","t");pg.wait_for_timeout(300);aft=pg.evaluate("cur.tools.map(x=>x.t)");print("   sort:",bef,"->",aft,"| real:",pg.evaluate("cur.tools.map(x=>realTools([x]).length)"))
  # 6 article fields, duplicate warning, phase
  pg.fill("#a-designation","TRACK SECONDARY");pg.fill("#a-material","ACIER");pg.wait_for_timeout(500)
  ok("article fields saved",pg.evaluate("A('a1').article.designation")=="TRACK SECONDARY")
  # 7 move to another machine (cone warning)
  pg.select_option("#a-machine","m2");pg.wait_for_timeout(400);ok("move to another machine",pg.evaluate("A('a1').machineId")=="m2" and "H1" in pg.inner_text("#crumbs"))
  pg.select_option("#a-machine","m1");pg.wait_for_timeout(300)
  # 8 preview toggle, PDF/Excel preview tabs
  pg.click("#b-pv");pg.wait_for_timeout(500);pg.click("#b-pv");pg.wait_for_timeout(1500)
  pg.click("[data-pvm=xlsx]");pg.wait_for_timeout(2500);ok("Excel preview shows",pg.locator("#pvpages").inner_html().strip()!="")
  pg.click("[data-pvm=pdf]");pg.wait_for_timeout(1500)
  # 9 downloads
  with pg.expect_download(timeout=15000) as d: pg.click("#b-dl")
  ok("PDF downloads",d.value.suggested_filename.endswith(".pdf"),d.value.suggested_filename)
  with pg.expect_download(timeout=20000) as d: pg.click("#b-xl")
  ok("Excel downloads",d.value.suggested_filename.endswith(".xlsx"),d.value.suggested_filename)
  # 10 layout select and Excel layout select
  pg.select_option("#a-layoutxl","std");pg.wait_for_timeout(500);pg.select_option("#a-layoutxl","");pg.wait_for_timeout(300)
  # 12 Columns window: rename, own column, hide, style; then the sheet
  pg.evaluate("closeDlg()");pg.click("#b-cols");pg.wait_for_timeout(600)
  pg.fill('[data-ct=type]',"Désignation outil");pg.fill("#col-new","Vc");pg.click("#col-add");pg.wait_for_timeout(300)
  pg.click("#lay-as");pg.fill("#lay-asname","Test");pg.click("#lay-asok");pg.wait_for_timeout(800)
  heads=pg.evaluate("[...document.querySelectorAll('.tt thead tr:first-child th')].map(t=>t.textContent.trim())")
  ok("renamed + own column visible",("Désignation outil" in " ".join(heads)) and "Vc" in heads,heads)
  ok("print boxes row has one box per printable column",pg.locator(".tt thead .prrow [data-pr]").count()>=len(heads)-2,pg.locator(".tt thead .prrow [data-pr]").count())
  # 13 the read-only view and print
  pg.evaluate("location.hash='#v-a1'");pg.wait_for_timeout(1200);ok("read-only view opens",pg.locator(".avt").count()==1 or pg.locator("#avpages").count()==1)
  pg.evaluate("location.hash='#a-a1'");pg.wait_for_timeout(1200)
  # 14 blank template and table empty sheet
  ok("blank sheet",pg.evaluate("blankSheet().getNumberOfPages()")>=1)
  # 15 an empty article: PDF and Excel
  pg.evaluate("db.articles.push({id:'a3',machineId:'m1',article:{},tools:[{t:'T01'}],createdAt:3,updatedAt:3});saveDB()")
  ok("empty article PDF",pg.evaluate("makePDF(sheetData(A('a3'))).getNumberOfPages()")>=1)
  ok("empty article Excel",pg.evaluate("(async()=>{const b=await sheetXLSX(A('a3'));return b&&b.size>1000})()"))
  # 16 a long sheet: 60 tools, multi pages
  pg.evaluate("A('a3').tools=Array.from({length:60},(_,i)=>({t:'T'+(i+1),type:'FRAISE 2T',diameter:String(i+2),ls:'40',holder:'BT50-ER32-100\\n+ RALLONGE',code:'F'+(900+i)}));saveDB()")
  n=pg.evaluate("makePDF(sheetData(A('a3'))).getNumberOfPages()");ok("60 tools: several pages",n>=2,n)
  pg.evaluate("location.hash='#a-a3'");pg.wait_for_timeout(2500);ok("60-tool sheet opens, count shown","60" in pg.inner_text("#count"),pg.inner_text("#count"))
  pg.evaluate("location.hash='#a-a1'");pg.wait_for_timeout(1200);pg.evaluate("flushEditor()")
  # 11 validate, new index, history
  pg.evaluate("flushEditor()")
  vb=pg.locator("#b-valid, #b-validate, .status-box .btn.red").first
  if vb.count():vb.click();pg.wait_for_timeout(600)
  if pg.locator("#ov:not([hidden]) .btn.red").count():pg.locator("#ov:not([hidden]) .btn.red").last.click();pg.wait_for_timeout(600)
  st=pg.evaluate("A('a1').status");print("   status after validate:",st,"| missing:",pg.evaluate("missing(A('a1'))"))
  print("ERRORS:",ERR)
  b.close()
print("FAILED:",[n for n,c in R if not c])
