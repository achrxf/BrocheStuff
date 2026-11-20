from playwright.sync_api import sync_playwright
R=[]
def ok(n,c,x=""):R.append((n,bool(c)));print(("PASS " if c else "FAIL ")+n,x)
U="file:///home/claude/qa/ToolManager.html"
SEED="""db.machines.push({id:'m1',abbr:'S3',name:'TOYODA',cone:'BT50',createdAt:1});
 db.catalog.push({code:'F941',type:'FRAISE HFS CW',diameter:'20',ra:'R3',z:'4',ls:'55'});
 db.articles.push({id:'a1',machineId:'m1',article:{number:'1052',index:'A'},tools:[
  {t:'T52',corrH:'52',type:'FRAISE HFS CW',diameter:'20',ra:'R3',ls:'55',holder:'CÔNE FRETTÉ\\nE3416560320100',code:'F941'},
  {t:'T09',corrH:'9',type:'TOURTEAU',insert:'RPHT1204',diameter:'63',ra:'R6',ls:'40',holder:'MANDRIN À TENON Ø22',code:'F863'}],createdAt:1,updatedAt:1});
 db.articles.push({id:'a2',machineId:'m1',article:{number:'2000',index:'B'},tools:[{t:'T01'},{t:'T02',type:'FRAISE 2T'},{t:'T03',diameter:'16'},{t:'T04'},{t:'T05'}],createdAt:2,updatedAt:2});
 db.layouts=[{id:'lold',name:'Ancienne',labels:{},extra:[],hidden:['oal','z'],order:['corr','type','diameter','ra','insert','ls','oal','z','holder','code']}];
 delete db.asmSeeded;db.assemblies=[];saveDB()"""
def cell(pg,i,k):return pg.locator(f'#rows tr[data-i="{i}"] input[data-k="{k}"]').first
def typ(pg,i,k,v):el=cell(pg,i,k);el.fill(v);el.dispatch_event("change");pg.wait_for_timeout(350)
with sync_playwright() as p:
  b=p.chromium.launch();ctx=b.new_context(viewport={"width":1500,"height":900});ctx.add_init_script("window.__QA_ROLE='admin'")
  pg=ctx.new_page();errs=[];pg.on("pageerror",lambda e:errs.append(str(e)));pg.on("console",lambda m:m.type=="error" and errs.append(m.text[:200]))
  pg.goto(U);pg.wait_for_timeout(1300);pg.evaluate("setLang('fr')");pg.evaluate(SEED)
  pg.evaluate("location.hash='#a-a1'");pg.wait_for_timeout(1200)
  ok("Assemblage column right after Outil",pg.evaluate("[...document.querySelectorAll('.tt thead th')].slice(0,3).map(t=>t.textContent.trim())")[:2]==["Outil","Assemblage"],pg.evaluate("[...document.querySelectorAll('.tt thead th')].slice(0,3).map(t=>t.textContent.trim())"))
  ok("existing rows show their code",[cell(pg,0,"asm").input_value(),cell(pg,1,"asm").input_value()]==["AS0001","AS0002"])
  ok("auto codes are not edits in the history",pg.evaluate("(A('a1').history||[]).length")==0)
  pg.evaluate("location.hash='#a-a2'");pg.wait_for_timeout(1000)
  # 1 empty row + assembly code -> filled, no question
  typ(pg,0,"asm","as1");x=pg.evaluate("cur.tools[0]")
  ok("empty row: filled from AS0001, no dialog",x.get("type")=="FRAISE HFS CW" and x.get("code")=="F941" and x.get("asm")=="AS0001" and pg.locator("#fill-go").count()==0,x)
  ok("T number kept",x["t"]=="T01")
  # 2 row with a different type -> dialog, keep by default
  typ(pg,1,"asm","AS0001")
  ok("different type: dialog shown",pg.locator("#fill-go").count()==1)
  txt=pg.inner_text(".filltab");ok("dialog shows both values","FRAISE 2T" in txt and "FRAISE HFS CW" in txt,txt)
  ok("replace boxes start unticked",pg.locator("[data-rep]:checked").count()==0)
  pg.screenshot(path="fill_dialog.png")
  pg.click("#fill-go");pg.wait_for_timeout(400);x=pg.evaluate("cur.tools[1]")
  ok("kept my type, filled the empty boxes",x.get("type")=="FRAISE 2T" and x.get("code")=="F941" and x.get("ls")=="55",x)
  ok("row marked orange (differs from its assembly)","warn" in cell(pg,1,"asm").get_attribute("class") and "Type" in (cell(pg,1,"asm").get_attribute("title") or ""))
  # 3 replace when ticked
  typ(pg,1,"asm","AS0001");pg.check("[data-rep=type]");pg.click("#fill-go");pg.wait_for_timeout(400)
  ok("ticked box replaced",pg.evaluate("cur.tools[1].type")=="FRAISE HFS CW")
  ok("no more orange","warn" not in (cell(pg,1,"asm").get_attribute("class") or ""))
  # 4 tool code from the crib, row has another diameter -> dialog
  typ(pg,2,"code","f941")
  ok("tool code: dialog for the Ø difference",pg.locator("#fill-go").count()==1 and "16" in pg.inner_text(".filltab"))
  pg.click("#fill-keep");pg.wait_for_timeout(400);x=pg.evaluate("cur.tools[2]")
  ok("kept Ø 16, filled type, R, Z, LS",x.get("diameter")=="16" and x.get("type")=="FRAISE HFS CW" and x.get("z")=="4" and x.get("ls")=="55",x)
  # 5 assembly code typed in the Code box goes to the Assembly column
  typ(pg,3,"code","AS0002");x=pg.evaluate("cur.tools[3]")
  ok("AS code in Code box -> Assembly column + filled",x.get("asm")=="AS0002" and x.get("code")=="F863" and x.get("type")=="TOURTEAU",x)
  # 6 unknown code
  typ(pg,4,"asm","AS0099")
  ok("unknown assembly: red box + message","bad" in cell(pg,4,"asm").get_attribute("class") and "AS0099" in pg.inner_text("#toast"))
  # 7 same values -> nothing to ask
  typ(pg,0,"asm","AS0001");ok("already matching: no dialog",pg.locator("#fill-go").count()==0 and "correspond" in pg.inner_text("#toast"))
  # 8 a new complete row gets its code by itself
  pg.evaluate("cur.tools.push({t:'T06',type:'FORET',diameter:'8',holder:'PINCE ER32',code:'M100'});renderRows();edited()");pg.wait_for_timeout(2900)
  ok("new row gets a new assembly code",cell(pg,5,"asm").input_value()=="AS0003",cell(pg,5,"asm").input_value())
  # 9 history: real edits recorded, without the assembly field
  pg.evaluate("flushEditor()");h=pg.evaluate("JSON.stringify((A('a2').history||[])[0]||{})")
  ok("history records the edit",'"edit"' in h,h[:200])
  # 10 the other pages
  pg.evaluate("location.hash='#v-a2'");pg.wait_for_timeout(900)
  ok("read-only view shows Assemblage","Assemblage" in pg.inner_text(".avt thead") and "AS0002" in pg.inner_text(".avt"))
  pg.evaluate("location.hash='#a-a2'");pg.wait_for_timeout(900)
  pg.click("#b-cols");pg.wait_for_timeout(600);ok("layout editor lists Assemblage","Assemblage" in pg.inner_text(".dlg"));pg.evaluate("closeDlg()")
  n=pg.evaluate("makePDF(sheetData(A('a2'))).getNumberOfPages()");ok("PDF still builds",n>=1)
  pg.evaluate("cur.layout='lold';refreshCols(cur);render()");pg.wait_for_timeout(800)
  ok("older layout: Assemblage placed after Outil",pg.evaluate("[...document.querySelectorAll('.tt thead th')].slice(0,2).map(t=>t.textContent.trim())")==["Outil","Assemblage"])
  ok("no errors",not errs,errs)
  b.close()
print("FAILED:",[n for n,c in R if not c])
