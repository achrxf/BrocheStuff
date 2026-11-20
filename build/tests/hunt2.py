from playwright.sync_api import sync_playwright
R=[];ERR=[]
def ok(n,c,x=""):R.append((n,bool(c)));print(("PASS " if c else "FAIL ")+n,str(x)[:300])
U="file:///home/claude/qa/ToolManager.html"
def cell(pg,i,k):return pg.locator(f'#rows tr[data-i="{i}"] input[data-k="{k}"]').first
with sync_playwright() as p:
  b=p.chromium.launch();ctx=b.new_context(viewport={"width":1500,"height":950},accept_downloads=True);ctx.add_init_script("window.__QA_ROLE='admin'")
  pg=ctx.new_page();pg.on("pageerror",lambda e:ERR.append("pageerror: "+str(e)));pg.on("console",lambda m:m.type=="error" and ERR.append("console: "+m.text[:200]))
  pg.on("dialog",lambda d:(ERR.append("browser dialog: "+d.message[:80]),d.dismiss()))
  pg.goto(U);pg.wait_for_timeout(1000);pg.evaluate("setLang('fr')")
  pg.evaluate("""db.machines.push({id:'m1',abbr:'S3',name:'TOYODA',cone:'BT50',createdAt:1});
    db.articles.push({id:'a1',machineId:'m1',article:{number:'1052',index:'A',designation:'TRACK',program:'O1337'},tools:[{t:'T01',type:'FRAISE',diameter:'10',ls:'30',holder:'H1',code:'F1'},{t:'T02',type:'FORET',diameter:'6',ls:'40',holder:'H2',code:'F2'}],createdAt:1,updatedAt:1});saveDB();location.hash='#a-a1'""");pg.wait_for_timeout(1500)
  # duplicate T numbers in one sheet
  cell(pg,1,"t").fill("T1");cell(pg,1,"t").dispatch_event("change");pg.wait_for_timeout(300)
  print("   duplicate T: T input classes =",cell(pg,1,"t").get_attribute("class"),"| title =",cell(pg,1,"t").get_attribute("title"))
  cell(pg,1,"t").fill("T02");cell(pg,1,"t").dispatch_event("change");pg.wait_for_timeout(300)
  # validate, then new index, history
  pg.evaluate("flushEditor()")
  vb=pg.locator("#stbox .btn.red").first;vb.click();pg.wait_for_timeout(500)
  if not pg.locator("#ov").is_hidden():pg.locator("#ov .btn.red").last.click();pg.wait_for_timeout(500)
  ok("validated",pg.evaluate("A('a1').status")=="done")
  ok("locked: tool cells read-only",pg.evaluate("cell=document.querySelector('#rows input[data-k=type]');cell.disabled||cell.readOnly"))
  ok("locked: assembly box under T read-only too",pg.evaluate("(()=>{const c=document.querySelector('#rows input[data-k=asm]');return !c||c.disabled||c.readOnly})()"))
  ok("locked: sort button disabled",pg.evaluate("(()=>{const s=document.querySelector('#a-sort');return !s||s.disabled})()"))
  ok("locked: print boxes disabled",pg.evaluate("[...document.querySelectorAll('.tt thead [data-pr]')].every(c=>c.disabled)"))
  nb=pg.locator("#b-newix");nb.click();pg.wait_for_timeout(500)
  if pg.locator("#ov input").count():pg.locator("#ov input").first.fill("Ajout T03");
  if not pg.locator("#ov").is_hidden():pg.locator("#ov .btn.red").last.click();pg.wait_for_timeout(600)
  ok("new index B",pg.evaluate("A('a1').article.index")=="B",pg.evaluate("A('a1').article.index"))
  ok("unlocked after new index",pg.evaluate("!document.querySelector('#rows input[data-k=type]').disabled"))
  cell(pg,0,"ls").fill("35");pg.wait_for_timeout(600);pg.evaluate("flushEditor()")
  h=pg.evaluate("(A('a1').history||[]).slice(0,3).map(x=>x.act+':'+JSON.stringify(x.t||x.f||''))");print("   history:",h)
  ok("history shows the edit of T01",any("edit" in x and "T01" in x for x in h))
  # changes between indexes
  ch=pg.evaluate("JSON.stringify(changeRows(A('a1')).diffs)");ok("index changes list the LS change",'"LS"' in ch or '"ls"' in ch.lower(),ch[:300])
  ok("…and not the assembly code",'asm' not in ch.lower() and 'Assemblage' not in ch,ch[:300])
  # copy article to another number
  pg.evaluate("location.hash='#m-m1'");pg.wait_for_timeout(800)
  cp=pg.locator("[data-copy], button:has-text('Copier')").first
  if cp.count():
    cp.click();pg.wait_for_timeout(500)
    inp=pg.locator("#ov input").first
    if inp.count():inp.fill("1053");pg.locator("#ov .btn.red").last.click();pg.wait_for_timeout(800)
  c=pg.evaluate("db.articles.filter(a=>a.article.number==='1053').map(a=>({s:a.status,ix:a.article.index,n:a.tools.length,asm:a.tools.map(x=>x.asm)}))");print("   copy:",c)
  ok("copy made",len(c)==1)
  # file names with odd characters
  pg.evaluate("A('a1').article.number='10/52:A*';A('a1').article.designation='Bride \"spéciale\"'")
  fn=pg.evaluate("fileName(A('a1'),'pdf')");ok("file name has no forbidden characters",not any(ch in fn for ch in '/\\:*?"<>|'),fn)
  pg.evaluate("A('a1').article.number='1052'")
  # empty sheet: sort, paste, PDF
  pg.evaluate("db.articles.push({id:'a9',machineId:'m1',article:{number:'9'},tools:[{t:'T01'}],createdAt:9,updatedAt:9});location.hash='#a-a9'");pg.wait_for_timeout(1000)
  pg.select_option("#a-sort","diaD");pg.wait_for_timeout(300);ok("sorting an empty sheet does nothing bad",pg.evaluate("cur.tools.length")==1)
  # T number typed with odd format, normalised in PDF
  cell(pg,0,"t").fill("t 7");cell(pg,0,"type").fill("fraise");cell(pg,0,"t").dispatch_event("change");pg.wait_for_timeout(200)
  ok("T7 corrector H = 7",pg.evaluate("cur.tools[0].corrH")=="7",pg.evaluate("cur.tools[0]"))
  print("ERRORS:",ERR)
  b.close()
print("FAILED:",[n for n,c in R if not c])
