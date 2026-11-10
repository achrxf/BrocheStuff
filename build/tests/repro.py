import base64,sys,json
from playwright.sync_api import sync_playwright
TOOLS=[{"t":"T02","corrH":"2","type":"TOURTEAU","insert":"RPHT1204M0T-6-M08 F40M","diameter":"112","ra":"R6","ls":"63","holder":"MANDRIN À TENON Ø32 AVEC ARROSAGE CENTRAL\nBT50ADB-SM32-055-L1","code":"F863"},
 {"t":"T52","corrH":"52","corrD":"52","type":"FRAISE HFS CW","diameter":"20","ra":"R3","ls":"55","holder":"CÔNE FRETTÉ\nE3416560320100","code":"F941"},
 {"t":"T38","corrH":"38","type":"TOURTEAU GRANDE VF","insert":"LPKT09T420TR-M13 MS2050","diameter":"32","ls":"57+35","holder":"MANDRIN COMBIMASTER M16 LG 57\nE341658201695","code":"F879"},
 {"t":"T29","corrH":"29","type":"FORET CW","diameter":"6.7","ls":"45","holder":"MANDRIN À PINCE ER32 SÉRIE LONGUE LG 120\nBT50AD-ER32-120","code":"F884"},
 {"t":"T22","corrH":"22","type":"TOURTEAU","insert":"RDHW0803M0-MD03 MS2050","diameter":"25","ra":"R4","ls":"57+40","holder":"MANDRIN COMBIMASTER M12 LG 57 E3416 5820 1295\n+ ALLONGE BS012 5820 1240","code":"F871"},
 {"t":"T27","corrH":"27","type":"OUTIL D'ALÉSAGE EXTER À PATIN","insert":"EK153L6-IF005","diameter":"14.25","ls":"44","holder":"MANDRIN HYDRAULIQUE Ø25 MAPAL: 303 200 46\nCÔNE RÉGLABLE MAPAL: 310 68 652","code":""}]
def low(ts):return [{**t,"holder":t["holder"].lower()} for t in ts]
with sync_playwright() as p:
  b=p.chromium.launch();pg=b.new_page();pg.add_init_script("window.__QA_ROLE='admin'")
  pg.goto("file:///home/claude/qa/ToolManager.html");pg.wait_for_timeout(1500);pg.evaluate("setLang('fr')")
  for name,tools,style in [("plain",TOOLS,{}),("caps",low(TOOLS),{"holder":{"u":True}}),("big",TOOLS,{"holder":{"k":1.2}})]:
    cfg=pg.evaluate("(st)=>{const c=JSON.parse(JSON.stringify(cfgOf?cfgOf({}):{}));c.style=st;return c}",style) if False else None
    d=pg.evaluate("""([tools,st])=>{const art={article:{number:'1052',index:'A',designation:'TRACK SECONDARY 12OC',reference:'BDL0948-02-0',program:'O1337',material:'ACIER'},tools};
      const cols=JSON.parse(JSON.stringify(normCfg({})));cols.style=st;return makePDF({...art,cols}).output('datauristring')}""",[tools,style])
    open(name+".pdf","wb").write(base64.b64decode(d.split(",")[1]))
  b.close()
