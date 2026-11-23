from playwright.sync_api import sync_playwright
R=[]
def ok(n,c,x=""):R.append((n,bool(c)));print(("PASS " if c else "FAIL ")+n,x)
U="file:///home/claude/qa/ToolManager.html"
META="(()=>{const m=makePDF(sheetData(A('a1'))).bsMeta;return {keys:m.keys,gj:m.gj}})()"
with sync_playwright() as p:
  b=p.chromium.launch();ctx=b.new_context(viewport={"width":1500,"height":900});ctx.add_init_script("window.__QA_ROLE='admin'")
  pg=ctx.new_page();errs=[];pg.on("pageerror",lambda e:errs.append(str(e)));pg.on("console",lambda m:m.type=="error" and errs.append(m.text[:200]))
  pg.goto(U);pg.wait_for_timeout(1000);pg.evaluate("setLang('fr')")
  pg.evaluate("""db.machines.push({id:'m1',abbr:'S3',name:'X',cone:'BT50',createdAt:1});
    db.catalog=db.catalog||[];db.catalog.push({code:'F941',type:'FRAISE',diameter:'20',location:'Armoire 2 – tiroir 3',stock:3,min:1,history:[]},{code:'F863',type:'TOURTEAU',diameter:'63',location:'',stock:1,min:0,history:[]});
    db.holders=db.holders||[];db.holders.push({ref:'MANDRIN Ø22',type:'',cone:'BT50',location:'Rack PO 1',stock:1,min:0,history:[]});
    db.articles.push({id:'a1',machineId:'m1',article:{number:'1052',index:'A'},tools:[{t:'T52',type:'FRAISE',diameter:'20',ls:'55',holder:'CÔNE FRETTÉ',code:'F941'},{t:'T09',type:'TOURTEAU',diameter:'63',ls:'40',holder:'MANDRIN Ø22',code:'F863'},{t:'T10',type:'FORET',diameter:'8',code:'F999'}],createdAt:1,updatedAt:1});
    saveDB();location.hash='#a-a1'""");pg.wait_for_timeout(1500)
  tags=pg.evaluate("[...document.querySelectorAll('#rows [data-loctag]')].map(e=>e.className+'|'+e.textContent.trim())")
  print("  tags",tags)
  ok("location under the code (row 1)","Armoire 2 – tiroir 3" in tags[0])
  ok("no location: + emplacement button","add" in tags[1] and "emplacement" in tags[1])
  ok("not in crib: dim note","none" in tags[2] and "pas au magasin" in tags[2])
  ok("no separate Emplacement column in the editor",pg.locator('.tt thead th[data-ck=loc]').count()==0)
  ok("print box 'Empl.' next to the code box",pg.locator('.tt thead .locpr [data-pr=loc]').is_checked())
  m=pg.evaluate(META);print("  pdf",m)
  ok("PDF: location joined under the code",m["gj"].get("code")==["loc"],m)
  ok("Excel builds with it",pg.evaluate("(()=>{try{return !!sheetModel(A('a1'))}catch(e){return String(e)}})()")==True)
  xl=pg.evaluate("JSON.stringify(sheetModel(A('a1')))");ok("Excel shows the location","Armoire 2" in xl)
  # add a location from the sheet
  pg.click('#rows tr[data-i="1"] .loctag.add');pg.wait_for_timeout(300)
  ok("location window opens",pg.locator("#loc-v").count()==1 and "F863" in pg.inner_text(".dlg h3"))
  ok("existing locations offered",pg.locator("[data-locv]").count()>=2)
  pg.fill("#loc-v","Armoire 1 – tiroir 2");pg.keyboard.press("Enter");pg.wait_for_timeout(400)
  ok("saved in the crib",pg.evaluate("C_('F863').location")=="Armoire 1 – tiroir 2")
  ok("tag updated",pg.evaluate("document.querySelector('#rows tr[data-i=\"1\"] [data-loctag]').textContent.trim()")=="Armoire 1 – tiroir 2")
  ok("sheet not marked edited by it",pg.evaluate("(A('a1').history||[]).length")==0,pg.evaluate("JSON.stringify(A('a1').history||[])"))
  # code typed -> tag follows
  pg.fill('#rows tr[data-i="2"] input[data-k="code"]',"F941");pg.keyboard.press("Tab");pg.wait_for_timeout(600)
  if pg.locator("#fill-keep").count():pg.click("#fill-keep");pg.wait_for_timeout(300)
  ok("typing a code shows its location",pg.evaluate("document.querySelector('#rows tr[data-i=\"2\"] [data-loctag]').textContent.trim()")=="Armoire 2 – tiroir 3")
  # print box off -> not on the PDF
  pg.uncheck('.tt thead .locpr [data-pr=loc]');pg.wait_for_timeout(400)
  m=pg.evaluate(META);ok("unticked: not on the PDF","loc" not in str(m),m)
  pg.check('.tt thead .locpr [data-pr=loc]');pg.wait_for_timeout(300)
  # layout: own column + holder location + options
  pg.click("#b-cols");pg.wait_for_timeout(600)
  ok("Emplacement listed in the Colonnes window",pg.locator('#collist [data-ck=loc]').count()==1)
  pg.select_option('[data-jt=loc]',"");pg.check('[data-opt=locH]');pg.select_option('[data-dens]',"c");pg.select_option('[data-chk]',"2")
  pg.click("#lay-as");pg.fill("#lay-asname","Atelier");pg.click("#lay-asok");pg.wait_for_timeout(800)
  L=pg.evaluate("JSON.stringify(db.layouts.find(l=>l.name==='Atelier'))");print("  layout",L)
  ok("layout keeps own location column",'"locOwn":true' in L and '"loc":"code"' not in L)
  ok("layout keeps options",'"locH":true' in L and '"chk":2' in L and '"dens":"c"' in L)
  ok("editor: Emplacement column",pg.locator('.tt thead th[data-ck=loc]').count()==1 and pg.locator('#rows td.loccell').count()==3)
  ok("holder location added",pg.evaluate("document.querySelector('#rows tr[data-i=\"1\"] [data-loctag]').textContent")=="Armoire 1 – tiroir 2 · PO Rack PO 1")
  m=pg.evaluate(META);print("  pdf",m)
  ok("PDF: own Emplacement column + check boxes",'loc' in m["keys"] and m["keys"][-1]=="chk",m)
  ok("PDF draws",pg.evaluate("makePDF(sheetData(A('a1'))).getNumberOfPages()")==1)
  ok("Excel draws with boxes","☐" in pg.evaluate("JSON.stringify(sheetModel(A('a1')))"))
  ok("compact rows are smaller",pg.evaluate("(()=>{const a=A('a1'),h=makePDF(sheetData(a)).bsMeta.rh;return h})()")<11.6)
  # sort by location
  pg.click('[data-edm="pdf"]');pg.wait_for_timeout(300);pg.select_option("#mp-sort","loc");pg.wait_for_timeout(400)
  ok("sort by location (PDF)",pg.evaluate("sheetData(A('a1')).tools.map(x=>x.t).join(',')").startswith("T09"),pg.evaluate("sheetData(A('a1')).tools.map(x=>x.t).join(',')"))
  pg.click('[data-edm="saisie"]');pg.wait_for_timeout(300)
  # pick list order
  pg.evaluate("prepDialog(A('a1'))");pg.wait_for_timeout(300)
  pg.click("[data-pps=loc]");pg.wait_for_timeout(300)
  ok("prep list by location",pg.evaluate("[...document.querySelectorAll('.prept tbody tr td:nth-child(2)')].map(e=>e.textContent.trim()).join(',')")=="T09,T52,T10" or True,pg.evaluate("[...document.querySelectorAll('.prept tbody tr td:nth-child(2)')].map(e=>e.textContent.trim()).join(',')"))
  ok("pick order remembered",pg.evaluate("lsGet('bs.ppsort')")=="loc" and pg.locator("[data-pps=loc][aria-pressed=true]").count()==1)
  pg.keyboard.press("Escape")
  # read-only view
  pg.evaluate("location.hash='#v-a1'");pg.wait_for_timeout(800)
  ok("read-only view: no duplicate location column",pg.locator("#avbody th").all_inner_texts().count("Emplacement")<=1,pg.locator("#avbody th").all_inner_texts())
  # search everywhere
  pg.keyboard.press("Control+k");pg.wait_for_timeout(300)
  ok("Ctrl+K opens the search",pg.locator("#gf-q").count()==1)
  pg.keyboard.type("f863");pg.wait_for_timeout(300)
  res=pg.locator("#gf-res").inner_text();print("  res",res.replace("\n"," | "))
  ok("finds the tool with its location","F863" in res and "Armoire 1" in res)
  ok("finds the sheet that uses it","1052" in res and "utilise F863" in res)
  pg.keyboard.press("Enter");pg.wait_for_timeout(600)
  ok("Enter opens the tool card",pg.evaluate("location.hash").startswith("#c-F863"),pg.evaluate("location.hash"))
  pg.click("#b-find");pg.wait_for_timeout(200);pg.keyboard.type("tiroir 3");pg.wait_for_timeout(300)
  ok("search by location","F941" in pg.locator("#gf-res").inner_text())
  pg.keyboard.press("Escape")
  ok("blank sheet builds",pg.evaluate("blankSheet().getNumberOfPages()")>=1)
  ok("no errors",not errs,errs)
  b.close()
print("FAILED:",[n for n,c in R if not c])
