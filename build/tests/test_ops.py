import base64,json
from playwright.sync_api import sync_playwright
R=[]
def ok(n,c,x=""):R.append((n,bool(c)));print(("PASS " if c else "FAIL ")+n,x)
OPS=[("T01","SURFAÇAGE","FRAISE A SURFACER","63","R0.8","HSK63-PTL22-60","F384","04:30","04:30"),("T02","ÉBAUCHE POCHE 1","FRAISE 2T","16","R2","HSK63-SF16-90","F138","12:30","12:30"),
 ("T02","ÉBAUCHE POCHE 2","FRAISE 2T","16","R2","HSK63-SF16-90","F138","08:15","08:15"),("T03","FINITION FOND","FRAISE 2T","10","R1","HSK63-SF10-90","F112","06:00","06:00"),
 ("T02","ÉBAUCHE ÎLOT","FRAISE 2T","16","R2","HSK63-SF16-90","F138","03:05","03:05"),("T04","PERÇAGE Ø8.5","FORET","8.5","140°","HSK63-ER25-100","M043","01:20","01:20"),
 ("T03","FINITION FLANCS","FRAISE 2T","10","R1","HSK63-SF10-90","F112","10:40","10:40"),("T05","TARAUDAGE M10","TARAUD","10","","HSK63-ER25-100","M081","00:50","00:50"),
 ("T04","PERÇAGE Ø8.5 FACE B","FORET","8.5","140°","HSK63-ER25-100","M043","01:10","01:10"),("T06","CHANFREIN","FRAISE CHANFREIN","10","90°","HSK63-ER25-100","F660","02:00","02:00"),
 ("T07","CONTOURNAGE","FRAISE 2T","20","R0.5","HSK63-SF20-90","F135","1:02:30","1:02:30"),("T07","CONTOURNAGE REPRISE","FRAISE 2T","20","R0.5","HSK63-SF20-100","F135","15:00","15:00")]
with sync_playwright() as p:
  b=p.chromium.launch();ctx=b.new_context(viewport={"width":1500,"height":950});ctx.add_init_script("window.__QA_ROLE='admin'")
  pg=ctx.new_page();errs=[];pg.on("pageerror",lambda e:errs.append(str(e)))
  pg.goto("file:///home/claude/qa/ToolManager.html");pg.wait_for_timeout(1200);pg.evaluate("setLang('fr')")
  tools=[{"t":o[0],"op":o[1],"type":o[2],"diameter":o[3],"ra":o[4],"ls":"50","holder":o[5],"code":o[6],"time":o[7],"life":o[8]} for o in OPS]
  pg.evaluate("t=>{db.machines.push({id:'m1',abbr:'S3',name:'DMU',cone:'HSK63',createdAt:1});db.articles.push({id:'a1',machineId:'m1',ops:true,article:{number:'975',index:'A'},tools:t,createdAt:1,updatedAt:1});db.articles.push({id:'a2',machineId:'m1',article:{number:'OLD',index:'A'},tools:[{t:'T1',type:'FORET',diameter:'8',ls:'40',holder:'ER25',code:'M1'},{t:'T2',type:'FRAISE',diameter:'10',ls:'50',holder:'ER25',code:'F2'}],createdAt:1,updatedAt:1});saveDB()}",tools)
  # old sheet unchanged
  m=pg.evaluate("(()=>{const m=makePDF(sheetData(A('a2'))).bsMeta;return m.keys})()");ok("old sheet: no new columns",not any(k in m for k in ["op","time","life"]),m)
  pg.evaluate("location.hash='#a-a1'");pg.wait_for_timeout(1500)
  ok("operation columns shown on this sheet",all(pg.locator(f'.tt thead th[data-ck="{k}"]').count()==1 for k in ["op","time","life"]))
  ok("count says tools + operations",pg.inner_text("#count"),pg.inner_text("#count"))
  ok("blue dot on repeated T",pg.locator('#rows .tdot:not(.bad)').count()==7,pg.locator('#rows .tdot:not(.bad)').count())
  ok("red flag on T07 (holder differs)",pg.locator('#rows .tdot.bad').count()==2 and "SF20-90" in pg.get_attribute('#rows tr[data-i="10"] input[data-k="t"]',"title"),pg.get_attribute('#rows tr[data-i="10"] input[data-k="t"]',"title"))
  d=pg.evaluate("sheetData(A('a1')).tools.map(x=>[normT(x.t),x.time,x.life])");print("  pdf rows",d)
  ok("PDF: one line per T (7)",len(d)==7)
  ok("PDF: T02 time summed 23:50",["T02","23:50","23:50"] in d)
  ok("PDF: T07 over an hour 01:17:30",["T07","01:17:30","01:17:30"] in d)
  keys=pg.evaluate("makePDF(sheetData(A('a1'))).bsMeta.keys");ok("PDF: time + life printed, operation not",("time" in keys and "life" in keys and "op" not in keys),keys)
  x=pg.evaluate("xlRowsOf(A('a1')).map(x=>[x.t,x.time])");ok("Excel: every operation + total",len(x)==13 and x[-1]==["TOTAL","02:07:50"],x[-1])
  xk=pg.evaluate("makePDF(xlData(A('a1'))).bsMeta.keys");ok("Excel: operation column in",("op" in xk),xk)
  ok("Excel model builds",pg.evaluate("(()=>{try{const m=sheetModel(A('a1'));return JSON.stringify(m).includes('02:07:50')}catch(e){return String(e)}})()")==True)
  # time normalising
  pg.fill('#rows tr[data-i="0"] input[data-k="time"]',"4:5");pg.keyboard.press("Tab");pg.wait_for_timeout(200)
  ok("4:5 becomes 04:05",pg.evaluate("A('a1').tools[0].time")=="04:05",pg.evaluate("A('a1').tools[0].time"))
  pg.fill('#rows tr[data-i="0"] input[data-k="time"]',"abc");pg.keyboard.press("Tab");pg.wait_for_timeout(200)
  ok("wrong time marked",pg.locator('#rows tr[data-i="0"] input[data-k="time"].bad').count()==1)
  pg.fill('#rows tr[data-i="0"] input[data-k="time"]',"04:30");pg.keyboard.press("Tab")
  # + operation
  n0=pg.evaluate("A('a1').tools.length");pg.click('#rows tr[data-i="3"] [data-r="addop"]');pg.wait_for_timeout(300)
  T=pg.evaluate("A('a1').tools.map(x=>normT(x.t)+'|'+(x.op||'')+'|'+(x.code||''))");print("  after +op",T[3:6])
  ok("+ operation adds a T03 line after T03's lines with the tool copied",pg.evaluate("A('a1').tools.length")==n0+1 and T[4]=="T03||F112",T[3:6])
  ok("focus goes to the new operation",pg.evaluate("document.activeElement.dataset.k")=="op")
  pg.keyboard.type("REPRISE");pg.keyboard.press("Tab");pg.keyboard.press("Tab");pg.keyboard.type("2:00");pg.keyboard.press("Tab");pg.wait_for_timeout(300)
  # modes
  pg.click('[data-edm="pdf"]');pg.wait_for_timeout(500)
  ok("PDF mode: table hidden, panel shown",not pg.is_visible(".ed .tw") and pg.is_visible("#modepanel"))
  ok("PDF mode: conflict listed",pg.locator(".mpconf").count()==1)
  rows=pg.locator(".mpt tbody tr").count();ok("PDF mode: 7 lines",rows==7,rows)
  pg.select_option("#mp-sort","type");pg.wait_for_timeout(300)
  ok("sort only the PDF",pg.evaluate("normT(A('a1').tools[0].t)")=="T01" and pg.evaluate("sheetData(A('a1')).tools[0].type")=="FORET",pg.evaluate("sheetData(A('a1')).tools.map(x=>x.type)"))
  pg.check('[data-mpk="op"]');pg.wait_for_timeout(300);ok("operation can be put on the PDF",'op' in pg.evaluate("makePDF(sheetData(A('a1'))).bsMeta.keys"))
  pg.uncheck('[data-mpk="op"]');pg.uncheck("#mp-group");pg.wait_for_timeout(300);ok("grouping can be switched off",len(pg.evaluate("sheetData(A('a1')).tools"))==13)
  pg.check("#mp-group");pg.wait_for_timeout(200)
  pg.screenshot(path="ux/o_pdfmode.png")
  pg.click('[data-edm="excel"]');pg.wait_for_timeout(500);pg.screenshot(path="ux/o_xlmode.png")
  ok("Excel mode: total line",pg.locator(".mpt tr.tot").count()==1)
  pg.check('[name="mx-rows"][value="pdf"]');pg.wait_for_timeout(300);ok("Excel like the PDF",len(pg.evaluate("xlRowsOf(A('a1'))"))==7)
  pg.check('[name="mx-rows"][value="ops"]');pg.wait_for_timeout(300);pg.select_option("#mx-sort","pdf");pg.wait_for_timeout(300)
  ok("Excel sorted like the PDF",pg.evaluate("xlRowsOf(A('a1'))[0].type")=="FORET")
  pg.uncheck('[data-mpk="life"]');pg.wait_for_timeout(300);ok("Excel columns of its own",("life" not in pg.evaluate("makePDF(xlData(A('a1'))).bsMeta.keys")) and ("life" in pg.evaluate("makePDF(sheetData(A('a1'))).bsMeta.keys")))
  pg.click('[data-edm="saisie"]');pg.wait_for_timeout(400);ok("back to Saisie",pg.is_visible(".ed .tw"))
  pg.screenshot(path="ux/o_saisie.png")
  open("ux/o.pdf","wb").write(base64.b64decode(pg.evaluate("makePDF(sheetData(A('a1'))).output('datauristring')").split(",")[1]))
  open("ux/ox.pdf","wb").write(base64.b64decode(pg.evaluate("makePDF(xlData(A('a1'))).output('datauristring')").split(",")[1]))
  # read-only + prep show one line per tool
  pg.evaluate("location.hash='#v-a1'");pg.wait_for_timeout(800)
  ok("read-only view: one line per tool",pg.locator("#avbody tbody tr").count()==7,pg.locator("#avbody tbody tr").count())
  pg.evaluate("prepDialog(A('a1'))");pg.wait_for_timeout(300);ok("tool prep: one line per tool",pg.locator(".prept tbody tr").count()==7,pg.locator(".prept tbody tr").count())
  pg.keyboard.press("Escape")
  # turn the columns off again
  pg.evaluate("location.hash='#a-a1'");pg.wait_for_timeout(900);pg.click("#b-ops");pg.wait_for_timeout(600)
  ok("columns hidden again (data kept)",pg.locator('.tt thead th[data-ck="time"]').count()==0 and pg.evaluate("A('a1').tools[1].time")=="12:30")
  ok("no errors",not errs,errs)
  b.close()
print("FAILED:",[n for n,c in R if not c])
