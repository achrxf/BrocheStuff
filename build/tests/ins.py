import base64
from playwright.sync_api import sync_playwright
exec(open("colw.py").read().split("with sync_playwright")[0])
with sync_playwright() as p:
  b=p.chromium.launch();ctx=b.new_context(viewport={"width":1400,"height":900});ctx.add_init_script("window.__QA_ROLE='admin'")
  pg=ctx.new_page();errs=[];pg.on("pageerror",lambda e:errs.append(str(e)))
  pg.goto(U);pg.wait_for_timeout(1200);pg.evaluate(SETUP)
  pg.evaluate("""(()=>{const a=A('a1');a.tools.push({t:'T07',corrH:'1',corrD:'1',type:'FRAISE A PLAQUETTES',insert:'XOMX 120408TR-ME08 F40M',diameter:'32',ls:'80',holder:'HSK-A63-PFR-Ø32-60',code:'F610'},
   {t:'T08',corrH:'1',corrD:'1',type:'TOURTEAU',insert:'SEKT 1204 AFTN-M14 MP2500',diameter:'63',ls:'45',holder:'HSK-A63-PFR-Ø27-60-EXTRA-LONG',code:'F610'},{t:'T09',corrH:'1',corrD:'1',type:'FRAISE-A-PLAQUETTES-RONDES',diameter:'125.5',ra:'R0.8',ls:'112.5',holder:'HSK-A63 + RALLONGE-PFR-Ø40-150',code:'F610'});
   a.tools.forEach(x=>{if(!x.insert&&/FRAISE 2/.test(x.type))x.insert='HM-R4-Z4-AL-LONG'});
   a.layoutData.extra.push({id:'e3',label:'Vc'},{id:'e4',label:'Fz'});a.tools.forEach(x=>{x.x_e3='120';x.x_e4='0.08'});saveDB()})()""")
  open("ux/ins.pdf","wb").write(base64.b64decode(pg.evaluate("makePDF(sheetData(A('a1'))).output('datauristring')").split(",")[1]))
  print(pg.evaluate("(()=>{const m=makePDF(sheetData(A('a1'))).bsMeta;return m.keys.map((k,i)=>k+':'+Math.round(m.colw[i]*10)/10).join(' ')})()"))
  print(errs);b.close()
