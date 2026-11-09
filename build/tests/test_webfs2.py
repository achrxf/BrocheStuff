from playwright.sync_api import sync_playwright
R=[]
def ok(n,c,x=""):R.append((n,bool(c)));print(("PASS " if c else "FAIL ")+n,x)
URL="http://127.0.0.1:8765/ToolManager.html"
OLD='{"machines":[{"id":"m9","name":"OLD","abbr":"O1","createdAt":1}],"articles":[{"id":"a9","machineId":"m9","article":{"number":"OLD-1","index":"A"},"tools":[],"createdAt":1,"updatedAt":1}],"lastBackup":0}'
NEWD='{"machines":[{"id":"m1","name":"NEW","abbr":"S3","createdAt":1}],"articles":[{"id":"a1","machineId":"m1","article":{"number":"NEW-1","index":"A"},"tools":[],"createdAt":1,"updatedAt":1}],"lastBackup":0}'
INIT="""window.__QA_WEBFS=true;window.__QA_PICK=true;
window.showDirectoryPicker=async()=>{const r=await navigator.storage.getDirectory();return r.getDirectoryHandle(window.__DIRNAME||'PickA',{create:true})};"""
CNT="(async()=>(await Neutralino.filesystem.readDirectory(DIR+SEP+'Backups').catch(()=>[])).filter(f=>/^backup-/.test(f.entry)).length)()"
def login(pg):
  if pg.locator(".langdlg").count():pg.click("[data-pick=fr]");pg.wait_for_timeout(300)
  if pg.locator("#lg-name").count():pg.fill("#lg-name","admin");pg.fill("#lg-pw","admin");pg.click("#lg-go");pg.wait_for_timeout(1500)
def run(dirname,choice,seed_dir=None):
  b=p.chromium.launch();ctx=b.new_context(viewport={"width":1400,"height":900});ctx.add_init_script(INIT+f"window.__DIRNAME='{dirname}';")
  pg=ctx.new_page();errs=[];pg.on("pageerror",lambda e:errs.append(str(e)))
  pg.goto(URL);pg.wait_for_timeout(300)
  pg.evaluate(f"localStorage.setItem('toollistmaker.db.v2',{OLD!r})")
  if seed_dir:pg.evaluate("""async([n,t])=>{const d=await (await navigator.storage.getDirectory()).getDirectoryHandle(n,{create:true});const w=await (await d.getFileHandle('data.json',{create:true})).createWritable();await w.write(t);await w.close()}""",[dirname,seed_dir])
  pg.goto(URL);pg.wait_for_timeout(1500)
  res={"first":pg.locator("#wfs-pick").count()==1,"hasline":pg.locator("#wfs").count() and "autre PC" in pg.inner_text("#wfs") or pg.locator("#wfs").count() and "another PC" in pg.inner_text("#wfs")}
  pg.click("#wfs-pick");pg.wait_for_timeout(1200)
  res["asked"]=pg.locator("#wfs-take").count()==1
  if res["asked"]:res["qtext"]=pg.inner_text("#wfs");pg.click("#wfs-take" if choice=="take" else "#wfs-skip");pg.wait_for_timeout(2500)
  else:pg.wait_for_timeout(2000)
  login(pg);res["arts"]=pg.evaluate("db.articles.map(a=>a.article.number)");res["errs"]=errs;res["pg"]=pg;res["b"]=b
  return res
with sync_playwright() as p:
  r=run("PickA","skip")
  ok("first screen offers picking an existing folder",r["first"] and r["hasline"])
  ok("older browser data: asked",r["asked"],r.get("qtext","")[:200])
  ok("question counts the old data","1 fiche" in r.get("qtext","") or "1 sheet" in r.get("qtext",""))
  ok("start empty: no old article",r["arts"]==[],r["arts"])
  pg=r["pg"];pg.evaluate("db.machines.push({id:'m1',abbr:'S3',name:'NEW',createdAt:1});db.articles.push({id:'a1',machineId:'m1',article:{number:'NEW-1',index:'A'},tools:[],createdAt:1,updatedAt:1});saveDB()");pg.wait_for_timeout(1500)
  pg.evaluate("location.hash='#admin'");pg.wait_for_timeout(800)
  ok("backup schedule list",pg.evaluate("[...document.querySelectorAll('#ad-bkev option')].map(o=>o.value).join()")=="off,day,week,month")
  ok("default weekly",pg.input_value("#ad-bkev")=="week")
  pg.screenshot(path="admin_backup.png",full_page=True)
  pg.evaluate("(async()=>{for(const f of await Neutralino.filesystem.readDirectory(DIR+SEP+'Backups').catch(()=>[]))if(/^backup-/.test(f.entry))await Neutralino.filesystem.remove(DIR+SEP+'Backups'+SEP+f.entry)})()");pg.wait_for_timeout(500)
  pg.select_option("#ad-bkev","off");pg.wait_for_timeout(500);ok("off saved",pg.evaluate("db.bkEvery")=="off")
  pg.evaluate("desk.dailyBackup()");pg.wait_for_timeout(800);n=pg.evaluate(CNT);ok("off: no backup file",n==0,n)
  pg.select_option("#ad-bkev","month");pg.wait_for_timeout(1200);n=pg.evaluate(CNT);ok("monthly: first backup made",n==1,n)
  # an older file from last month -> monthly makes a new one; from this month -> not
  pg.evaluate("(async()=>{const L=(await Neutralino.filesystem.readDirectory(DIR+SEP+'Backups')).filter(f=>/^backup-/.test(f.entry));for(const f of L)await Neutralino.filesystem.remove(DIR+SEP+'Backups'+SEP+f.entry);const d=new Date();d.setDate(d.getDate()-3);await Neutralino.filesystem.writeFile(DIR+SEP+'Backups'+SEP+'backup-'+stampOf(d)+'.json','{}')})()");pg.wait_for_timeout(500)
  pg.select_option("#ad-bkev","week");pg.wait_for_timeout(1200);n=pg.evaluate(CNT);ok("weekly: 3-day-old file -> no new one",n==1,n)
  pg.select_option("#ad-bkev","day");pg.wait_for_timeout(1200);n=pg.evaluate(CNT);ok("daily: new one",n==2,n)
  pg.uncheck("#ad-snap");pg.wait_for_timeout(300);ok("5-min copies toggle off",pg.evaluate("db.snapOff")==True)
  c0=len(pg.evaluate("listSnapshots()") or []);pg.evaluate("DIRTY=true;takeSnapshot()");pg.wait_for_timeout(600);ok("no copy when off",len(pg.evaluate("listSnapshots()") or [])==c0)
  ok("no errors (1)",not r["errs"],r["errs"]);r["b"].close()
  r=run("PickB","take");ok("take: old article in the folder",r["arts"]==["OLD-1"],r["arts"]);ok("no errors (2)",not r["errs"],r["errs"]);r["b"].close()
  r=run("PickC","take",seed_dir=NEWD);ok("existing folder: not asked",not r["asked"]);ok("existing folder: its data",r["arts"]==["NEW-1"],r["arts"]);ok("no errors (3)",not r["errs"],r["errs"]);r["b"].close()
print("FAILED:",[n for n,c in R if not c])
