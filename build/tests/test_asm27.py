from playwright.sync_api import sync_playwright
R=[]
def ok(n,c,x=""):R.append((n,bool(c)));print(("PASS " if c else "FAIL ")+n,"" if c else x)
with sync_playwright() as p:
  b=p.chromium.launch();ctx=b.new_context(viewport={"width":1440,"height":900},reduced_motion="reduce");ctx.add_init_script("window.__QA_ROLE='admin'")
  pg=ctx.new_page();errs=[];pg.on("pageerror",lambda e:errs.append(str(e)));pg.goto("file:///home/claude/qa/Demo.html");pg.wait_for_timeout(2200)
  if pg.locator(".langdlg").count():pg.click("[data-pick=fr]")
  H1=pg.evaluate("db.machines.find(x=>x.abbr==='H1').id");H2=pg.evaluate("db.machines.find(x=>x.abbr==='H2').id")
  # a new sheet on H1
  pg.evaluate(f"location.hash='#m-{H1}'");pg.wait_for_timeout(800);pg.click("#newa");pg.wait_for_timeout(1200)
  n0=pg.evaluate("asmList().length")
  def setcell(i,k,v):
    pg.evaluate("([i,k,v])=>{const el=document.querySelector(`#rows tr[data-i=\"${i}\"] [data-k=\"${k}\"]`);if(!el)throw new Error('no cell '+k);el.focus();el.value=v;el.dispatchEvent(new Event('input',{bubbles:true}));el.dispatchEvent(new Event('change',{bubbles:true}));el.blur()}",[i,k,v])
  setcell(0,"t","T07");setcell(0,"type","FRAISE QA");setcell(0,"diameter","13.7");setcell(0,"holder","HSK63-QA-TEST-1");setcell(0,"code","QA137");setcell(0,"ls","44")
  pg.wait_for_timeout(3000)
  ok("typing a full row no longer makes an assembly by itself",pg.evaluate("asmList().length")==n0,pg.evaluate("asmList().length-"+str(n0)))
  ok("'Make the assemblies' button shows 1",pg.locator("#b-mkasm").count()==1 and "(1)" in pg.inner_text("#b-mkasm"),pg.locator("#b-mkasm").all_inner_texts())
  pg.click("#b-mkasm");pg.wait_for_timeout(600)
  a=pg.evaluate(f"(()=>{{const a=asmList()[asmList().length-1];return {{code:a.code,tn:a.tnum,row:cur.tools[0].asm,keep:a.keep,auto:a.auto}}}})()")
  ok("assembly made and linked to the row",a["row"]==a["code"] and pg.evaluate("asmList().length")==n0+1,a)
  ok("it remembers T07 on H1",a["tn"].get(H1)=="T07",a)
  code=a["code"]
  # changing the T in the sheet moves the assembly's T
  setcell(0,"t","T09");pg.wait_for_timeout(500)
  ok("changing T in the sheet updates the assembly (H1 → T09)",pg.evaluate(f"asmFind('{code}').tnum['{H1}']")=="T09")
  # the same assembly on H2: no T yet → the row's T is remembered; then the T is reused
  pg.evaluate(f"location.hash='#m-{H2}'");pg.wait_for_timeout(800);pg.click("#newa");pg.wait_for_timeout(1200)
  setcell(0,"t","T21");setcell(0,"code",code);pg.wait_for_timeout(800)
  r=pg.evaluate("[cur.tools[0].asm,cur.tools[0].holder,cur.tools[0].t]")
  ok("typing the assembly code fills the row on H2",r[0]==code and r[1]=="HSK63-QA-TEST-1",r)
  ok("H2 had no T yet: the row's T21 is remembered",pg.evaluate(f"asmFind('{code}').tnum['{H2}']")=="T21")
  a2=pg.evaluate("cur.id")
  pg.evaluate(f"location.hash='#m-{H2}'");pg.wait_for_timeout(800);pg.click("#newa");pg.wait_for_timeout(1200)
  setcell(0,"code",code);pg.wait_for_timeout(800)
  ok("on another H2 sheet the T comes from the assembly (T21)",pg.evaluate("cur.tools[0].t")=="T21",pg.evaluate("cur.tools[0].t"))
  # editing the assembly updates the sheets; T per machine in the window
  pg.evaluate("location.hash='#asm'");pg.wait_for_timeout(1000)
  pg.evaluate(f"asmDialog(asmFind('{code}'))");pg.wait_for_timeout(500)
  ok("window shows T per machine",pg.locator(".asmtn [data-tnm]").count()>=2,pg.locator(".asmtn").all_inner_texts())
  pg.fill('[data-af="ls"]',"55");pg.fill(f'[data-tnm="{H2}"]',"T30");pg.click("#as-ok");pg.wait_for_timeout(700)
  rows=pg.evaluate(f"db.articles.flatMap(ar=>realTools(ar.tools).filter(x=>x.asm==='{code}').map(x=>[ar.machineId,x.t,x.ls]))")
  ok("every sheet using it now has LS 55",all(x[2]=="55" for x in rows) and len(rows)==3,rows)
  ok("H2 sheets take T30, H1 keeps T09",all((x[1]=="T30") if x[0]==H2 else (x[1]=="T09") for x in rows),rows)
  ok("list shows the T per machine",pg.locator(f"tr[data-asmid] .asmtnl").count()>=1)
  # a linked row changed in a sheet offers to update the assembly
  pg.evaluate(f"location.hash='#a-{a2}'");pg.wait_for_timeout(1200)
  setcell(0,"ls","60");pg.wait_for_timeout(800)
  ok("changing a linked row offers 'Update' the assembly",f"Mettre à jour {code}" in pg.inner_text("body"))
  pg.locator(".toast button",has_text=f"Mettre à jour {code}").first.click();pg.wait_for_timeout(500)
  ok("assembly updated from the row and pushed to the others",pg.evaluate(f"asmFind('{code}').tool.ls")=="60" and pg.evaluate(f"db.articles.flatMap(ar=>realTools(ar.tools).filter(x=>x.asm==='{code}').map(x=>x.ls))")==["60","60","60"])
  # unused cleanup
  pg.evaluate("asmList().push({id:uid(),code:asmNext(),tool:{holder:'X',code:'ZZZ'},sig:'zz-unused',auto:1,createdAt:Date.now()});saveDB()")
  pg.evaluate("location.hash='#'");pg.wait_for_timeout(300);pg.evaluate("location.hash='#asm'");pg.wait_for_timeout(1000)
  ok("'Delete the unused ones' offered",pg.locator("#asm-purge").count()==1,pg.locator("#asm-purge").count())
  # deleting unlinks the rows
  pg.evaluate(f"asmDialog(asmFind('{code}'))");pg.wait_for_timeout(400);pg.click("#as-del");pg.wait_for_timeout(300);pg.click("#as-delok");pg.wait_for_timeout(500)
  ok("deleted and rows unlinked",pg.evaluate(f"!asmFind('{code}')&&db.articles.every(ar=>realTools(ar.tools).every(x=>x.asm!=='{code}'))"))
  ok("no errors",not errs,errs)
  b.close()
print("FAILED:",[n for n,c in R if not c])
