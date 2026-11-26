from playwright.sync_api import sync_playwright
import json
R=[]
def ok(n,c,x=""):R.append((n,bool(c)));print(("PASS " if c else "FAIL ")+n,x if not c else "")
with sync_playwright() as p:
  b=p.chromium.launch();ctx=b.new_context(viewport={"width":1440,"height":900},reduced_motion="reduce");ctx.add_init_script("window.__QA_ROLE='admin'")
  pg=ctx.new_page();errs=[];pg.on("pageerror",lambda e:errs.append(str(e)));pg.goto("file:///home/claude/qa/Demo.html");pg.wait_for_timeout(2000)
  if pg.locator(".langdlg").count():pg.click("[data-pick=fr]")
  for f,exp in [("bride.nc",["T01","T05","T12","T05","T01"]),("tnc.h",["T14","T22","T14"])]:
    txt=open("nc/"+f).read()
    r=pg.evaluate("([t,f])=>{const r=parseNC(t,f);return {seq:r.seqTools.map(x=>[x.t,x.op||'',x.corrH||'']),u:r.tools.map(x=>x.t),nc:looksNC(t)}}",[txt,f])
    print(f,json.dumps(r))
    ok(f+": every tool change in order, repeats kept",[x[0] for x in r["seq"]]==exp,r)
    ok(f+": recognised as a CNC program",r["nc"])
  r=pg.evaluate("([t])=>parseNC(t,'b.nc').seqTools.map(x=>x.op)",[open("nc/bride.nc").read()])
  ok("operation names from the comments",r==["SURFACAGE","CONTOURNAGE EBAUCHE","PERCAGE D8.5","CONTOURNAGE FINITION","CHANFREIN"],r)
  r=pg.evaluate("([t])=>parseNC(t,'t.h').seqTools.map(x=>x.op||'')",[open("nc/tnc.h").read()])
  ok("Heidenhain ; comments name the operations",r==["EBAUCHE POCHE","PERCAGE","FINITION POCHE"],r)
  # a CSV tool list that mentions M6 is still read as a table, not a program

  # full flow: editor → read a program
  m=pg.evaluate("db.machines.find(x=>x.abbr==='H1').id")
  pg.evaluate(f"location.hash='#m-{m}'");pg.wait_for_timeout(900);pg.click("#newa");pg.wait_for_timeout(1200)
  with pg.expect_file_chooser() as fc:pg.click("#b-ncimp")
  fc.value.set_files("nc/bride.nc");pg.wait_for_timeout(1200)
  ok("import window opened",pg.locator(".impdlg").count()==1)
  ok("sort by T is off for a program",not pg.locator("#imp-sort").is_checked())
  pg.click("#d-imp");pg.wait_for_timeout(1200)
  ok("no 'which double to keep' question",pg.locator(".dupg").count()==0)
  if pg.locator(".overlay:not([hidden]) #d-imp").count():pg.click("#d-imp");pg.wait_for_timeout(800)
  got=pg.evaluate("realTools(cur.tools).map(x=>[x.t,x.op||''])")
  ok("sheet has the 5 lines in program order",[x[0] for x in got]==["T01","T05","T12","T05","T01"],got)
  ok("operation names on the sheet",[x[1] for x in got][1]=="CONTOURNAGE EBAUCHE",got)
  ok("operation columns switched on",pg.evaluate("!!cur.ops"))
  pdf=pg.evaluate("pdfRowsOf(cur).map(x=>x.t)")
  ok("PDF still one line per tool",sorted(pdf)==["T01","T05","T12"],pdf)
  ok("no errors",not errs,errs)
  b.close()
print("FAILED:",[n for n,c in R if not c])
