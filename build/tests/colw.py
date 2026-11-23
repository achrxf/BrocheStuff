import sys,base64
from playwright.sync_api import sync_playwright
U="file:///home/claude/qa/ToolManager.html"
SETUP="""(()=>{setLang('en');db.machines.push({id:'m1',abbr:'M5',name:'NMV5000TITAN',cone:'HSK63',createdAt:1});
db.catalog=db.catalog||[];['F886','F660','F603','F605','F610'].forEach(c=>db.catalog.push({code:c,type:'X',location:'CAB Méthode',stock:1,min:0,history:[]}));
db.layouts=db.layouts||[];db.layouts.push({id:'L1',name:'ABIPA',labels:{corr:'Offset',holder:'Ref Attachement'},extra:[{id:'e1',label:'DDV/P'},{id:'e2',label:'Temp / min'}],hidden:['asm','oal','z'],joinTo:{insert:'type',loc:'code'},order:['asm','corr','type','diameter','ra','insert','ls','oal','z','x_e1','x_e2','holder','code','loc'],noprint:['asm']});
db.articles.push({id:'a1',machineId:'m1',layout:'L1',layoutData:db.layouts[db.layouts.length-1],article:{number:'975',index:'A',reference:'BNL2184-02-0',program:'01339',material:'TITAN',designation:'COVER-FWD MOUNT LOWER'},tools:[
{t:'T01',corrH:'1',corrD:'1',type:'TOURTEAU U6V',insert:'DAH-37-022-SE-DM',diameter:'50',ls:'40',x_e1:'1',holder:'DAHM.37.063.A2740.07',code:'F886'},
{t:'T02',corrH:'1',corrD:'1',type:'TOURTEAU U6V',insert:'DAH-37-022-SE-DM',diameter:'50',ls:'40',x_e1:'1',holder:'DAHM.37.063.A2740.07',code:'F886'},
{t:'T04',corrH:'1',corrD:'1',type:'FRAISE CHANFRIEN',diameter:'10',ra:'90°',ls:'52',holder:'HSK-A63-PER-25-42-100',code:'F660'},
{t:'T05',corrH:'1',corrD:'1',type:'FRAISE 2 TAILLES EB',diameter:'16',ra:'R4',ls:'65',holder:'HSK-A63-PFR-Ø16-42-52-85',code:'F603'},
{t:'T06',corrH:'1',corrD:'1',type:'FRAISE 2 TAILLES EB',diameter:'16',ra:'R2',ls:'65',holder:'HSK-A63-PFR-Ø16-42-52-85',code:'F605'}],createdAt:1,updatedAt:1});saveDB()})()"""
with sync_playwright() as p:
  b=p.chromium.launch();ctx=b.new_context(viewport={"width":1400,"height":900});ctx.add_init_script("window.__QA_ROLE='admin'")
  pg=ctx.new_page();errs=[];pg.on("pageerror",lambda e:errs.append(str(e)))
  pg.goto(U);pg.wait_for_timeout(1200);pg.evaluate(SETUP);pg.wait_for_timeout(300)
  m=pg.evaluate("(()=>{const d=makePDF(sheetData(A('a1'))),m=d.bsMeta;return {keys:m.keys,w:(m.colw||m.ws||[]).map(x=>Math.round(x*10)/10)}})()");print(m)
  pdf=pg.evaluate("makePDF(sheetData(A('a1'))).output('datauristring')");open(sys.argv[1]+".pdf","wb").write(base64.b64decode(pdf.split(",")[1]))
  print(errs);b.close()
