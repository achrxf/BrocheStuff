from playwright.sync_api import sync_playwright
R=[]
def ok(n,c,x=""):R.append((n,bool(c)));print(("PASS " if c else "FAIL ")+n,x)
with sync_playwright() as p:
  b=p.chromium.launch();ctx=b.new_context(viewport={"width":1400,"height":950});ctx.add_init_script("window.__QA_ROLE='admin'")
  pg=ctx.new_page();errs=[];pg.on("pageerror",lambda e:errs.append(str(e)))
  pg.goto("file:///home/claude/qa/ToolManager.html");pg.wait_for_timeout(1500);pg.evaluate("setLang('en')")
  # the models window in English
  for k in ["machines","articles","tools","crib","holders"]:
    h=pg.evaluate(f"(()=>{{const tp=TPLS.find(x=>x.k==='{k}');const d=tplRead(tp);return [tplF(tp),d.head.join(' | '),d.guide.length,tplReq(tp).filter(r=>d.head.includes(r)).length===tplReq(tp).length]}})()")
    print(" ",k,h[0],"::",h[1][:150])
    ok(k+": English model with its instructions",h[0].endswith("_EN.xlsx") and h[2]>3 and h[3])
  pg.evaluate("setLang('fr')");ok("French keeps the French model",pg.evaluate("tplF(TPLS[0])")=="1_Machines_Template.xlsx" and "Abréviation" in pg.evaluate("tplRead(TPLS[0]).head.join()"))
  pg.evaluate("setLang('en')")
  import base64,glob,os
  fb={os.path.basename(x):base64.b64encode(open(x,'rb').read()).decode() for x in glob.glob('/home/claude/qa/tplfill/*.xlsx')}
  pg.evaluate("fb=>{window.__FB={};for(const k in fb)window.__FB[k]=Uint8Array.from(atob(fb[k]),c=>c.charCodeAt(0))}",fb)
  # import the example rows of each English model
  def imp(kind,ctxjs="{}",tk=None):
    pg.evaluate(f"""(()=>{{const tp=TPLS.find(x=>x.k==='{tk or kind}'),F=tplF(tp);window.pickFile=async()=>new File([window.__FB[F]],F);void startImport('{kind}',{ctxjs})}})()""");pg.wait_for_timeout(1500)
    txt=pg.inner_text(".dlg") if not pg.locator("#ov").is_hidden() else "(no window)"
    return txt
  t=imp("machines");print("   ",t[:300].replace("\n"," | "))
  pg.click("#d-imp");pg.wait_for_timeout(800);
  if not pg.locator("#ov").is_hidden():pg.evaluate("closeDlg()")
  m=pg.evaluate("db.machines.map(m=>[m.abbr,m.name,m.brand,m.control,m.cone])");ok("machines imported with every column",any(x[0]=="M6" and x[1] and x[2] and x[3] and x[4] for x in m),m)
  t=imp("codes",tk="crib");print("   ",t[:400].replace("\n"," | "))
  pg.click("#d-imp");pg.wait_for_timeout(800)
  if not pg.locator("#ov").is_hidden():pg.evaluate("closeDlg()")
  c=pg.evaluate("(db.catalog||[]).filter(c=>c.code==='A-1024').map(c=>[c.type,c.diameter,c.ra,c.z,c.insert,c.location,c.stock,c.min,c.supplier,c.cutLength,c.oal,c.grade,c.workMat,c.family,c.subfamily,c.ref])");ok("crib imported with location, stock, min",c and c[0][5] and str(c[0][6])=="4",c)
  t=imp("holders");print("   ",t[:300].replace("\n"," | "))
  pg.click("#d-imp");pg.wait_for_timeout(800)
  if not pg.locator("#ov").is_hidden():pg.evaluate("closeDlg()")
  h=pg.evaluate("(db.holders||[]).map(h=>[h.ref,h.cone,h.type,h.clamp,h.nose,h.length,h.location,h.stock])");ok("holders imported",len(h)>=1 and any(x[1] and x[6] for x in h),h[:3])
  t=imp("articles","{machineId:db.machines.find(m=>m.abbr==='M6').id}");print("   ",t[:300].replace("\n"," | "))
  pg.click("#d-imp");pg.wait_for_timeout(1000)
  if not pg.locator("#ov").is_hidden():
    print("   after:",pg.inner_text(".dlg")[:200].replace("\n"," | "));pg.evaluate("closeDlg()")
  a=pg.evaluate("db.articles.map(a=>[a.article.number,a.article.index,a.article.designation,a.article.program,realTools(a.tools).map(x=>[x.t,x.corrH,x.corrD,x.type,x.diameter,x.ls,x.holder,x.code].join('/')).join(' ; ')])");ok("articles imported with tools",any(x[0]=="11111-001" and x[4] for x in a),a)
  ok("no errors",not errs,errs)
  b.close()
print("FAILED:",[n for n,c in R if not c])
