import re,sys,json
from playwright.sync_api import sync_playwright
LANG=sys.argv[1]
SKIP=re.compile(r"^(EN|FR)$|supprim|delete|tout supprimer|réinitialiser|reset|restaurer|restore|sortir \d|take \d|charger l|vider|déconnex|sign out|changer de service|switch service|quitter|empty",re.I)
FRW=set("le la les des du une un pour avec sans dans sur est sont pas ou et au aux ce cette ces ici votre vos nous vous il elle qui que quoi tout tous toutes outil outils fiche fiches ajouter supprimer enregistrer annuler fermer modifier emplacement plaquette tiroir étagère porte-outil porte-outils aucun aucune encore déjà page pages rien trouvé ligne lignes colonne colonnes saisie opération opérations temps vie validée valider imprimer importer exporter nouveau nouvelle chercher rechercher magasin oui non mise sortie entrée stock bas rupture sans".split())
ENW=set("the and with without tool tools sheet sheets add delete save cancel close edit location holder holders insert search print settings new open back next done ready prep set none all of to in on for from your you is are not no yes this that these only here there when click typed shown show hide items item line lines column columns operation operations time life entry used uses kept where what which more less options option".split())
OK_EN=set("pdf excel ctrl k t h d ls lt z ok id hsk bt sk iso ap".split())
with sync_playwright() as p:
  b=p.chromium.launch();ctx=b.new_context(viewport={"width":1440,"height":900},accept_downloads=True);ctx.add_init_script("window.__QA_ROLE='admin'")
  pg=ctx.new_page();ERR=[];cur={"where":""};SEEN={}
  pg.on("pageerror",lambda e:ERR.append(cur["where"]+" :: "+str(e)[:200]))
  pg.on("dialog",lambda d:d.dismiss())
  pg.on("download",lambda d:None)
  pg.goto("file:///home/claude/qa/Demo.html");pg.wait_for_timeout(2500);pg.evaluate(f"setLang('{LANG}')")
  DATA=set(re.findall(r"[a-zà-ÿ'’-]+",pg.evaluate("JSON.stringify(db)").lower()))
  m=pg.evaluate("db.machines[0].id");a=pg.evaluate("db.articles.find(x=>realTools(x.tools).length>5&&x.status!=='done').id");a2=pg.evaluate("(db.articles.find(x=>x.status==='done')||db.articles[0]).id");c=pg.evaluate("db.catalog[0].code");h=pg.evaluate("db.holders[0].ref")
  P=[("home","#"),("machine","#m-"+m),("article","#a-"+a),("article-pdf","#a-"+a),("article-xl","#a-"+a),("done","#a-"+a2),("aview","#v-"+a),("arts","#arts"),("asm","#asm"),("crib","#crib"),("code","#c-"+c),("holders","#holders"),("holder","#h-"+h),("prod","#prod"),("pcode","#pc-"+c),("log","#log"),("mags","#mags"),("reports","#reports"),("admin","#admin"),("guide","#guide")]
  GRAB="""(()=>{const out=[];const add=(w,s)=>{s=(s||'').replace(/\\s+/g,' ').trim();if(s)out.push([w,s])};
    const vis=e=>e.offsetWidth||e.offsetHeight;
    add('text',(document.querySelector('#ov:not([hidden]) .dlg')||{}).innerText);
    add('text',document.querySelector('#view').innerText);add('text',document.querySelector('header.top').innerText);
    const t=document.querySelector('#toast');if(t&&vis(t))add('toast',t.innerText);
    document.querySelectorAll('[title],[placeholder],[aria-label]').forEach(e=>{if(!vis(e)&&!e.closest('#ov'))return;['title','placeholder','aria-label'].forEach(a=>{if(e.hasAttribute(a))add(a,e.getAttribute(a))})});
    return out})()"""
  def scan(where):
    for kind,s in pg.evaluate(GRAB):
      for line in re.split(r"\n|(?<=[.!?:])\s",s):
        toks=re.findall(r"[A-Za-zÀ-ÿ'’-]+",line);bad=[]
        for tk in toks:
          l=tk.lower().strip("'’-")
          if not l or l in DATA or l in OK_EN:continue
          if LANG=="en" and (l in FRW or re.search(r"[éèêàçùâîôûëï]",l)):bad.append(tk)
          if LANG=="fr" and l in ENW:bad.append(tk)
        if bad:
          key=line[:120]
          if key not in SEEN:SEEN[key]=(where,kind,bad)
  for n,hsh in P:
    pg.evaluate(f"location.hash={hsh!r}");pg.wait_for_timeout(1200)
    if n.startswith("article"):pg.evaluate("location.hash='#'");pg.wait_for_timeout(400);pg.evaluate(f"location.hash={hsh!r}");pg.wait_for_timeout(1200)
    if n=="article-pdf":pg.evaluate("setEdMode('pdf')");pg.wait_for_timeout(500)
    if n=="article-xl":pg.evaluate("setEdMode('excel')");pg.wait_for_timeout(500)
    if n=="article":pg.evaluate("setEdMode('saisie')");pg.wait_for_timeout(300)
    cur["where"]=n;scan(n)
    labels=pg.evaluate("""[...document.querySelectorAll('#view button, #view .chip, #view [data-go], #tbar button')].filter(e=>e.offsetWidth&&!e.disabled).map((e,i)=>{e.dataset.crawl=i;return [i,(e.innerText||e.title||e.getAttribute('aria-label')||'').trim().slice(0,40)]})""")
    seen=set()
    for i,lab in labels[:80]:
      if SKIP.search(lab) or (lab in seen and lab):continue
      seen.add(lab);cur["where"]=f"{n} › {lab or '#'+str(i)}"
      try:
        el=pg.locator(f'[data-crawl="{i}"]')
        if not el.count() or not el.is_visible():continue
        el.click(timeout=3000);pg.wait_for_timeout(400)
        if pg.evaluate("LANG")!=LANG:print("LANG CHANGED BY",cur["where"]);pg.evaluate(f"setLang('{LANG}')");pg.wait_for_timeout(300)
        scan(cur["where"])
      except Exception as e:pass
      if not pg.locator("#ov").is_hidden():
        pg.evaluate("(()=>{const o=document.querySelector('#ov');delete o.dataset.lock;closeDlg()})()")
      if pg.evaluate("location.hash")!=hsh or pg.locator("[data-crawl]").count()==0:
        pg.evaluate(f"location.hash={hsh!r}");pg.wait_for_timeout(700)
        if n=="article-pdf":pg.evaluate("setEdMode('pdf')")
        if n=="article-xl":pg.evaluate("setEdMode('excel')")
        pg.evaluate("""[...document.querySelectorAll('#view button, #view .chip, #view [data-go], #tbar button')].filter(e=>e.offsetWidth&&!e.disabled).forEach((e,i)=>e.dataset.crawl=i)""")
  pg.evaluate("setEdMode('saisie')")
  for k,(w,kind,bad) in SEEN.items():print(f"[{w}] ({kind}) {bad} :: {k}")
  print("ERRORS:",ERR)
  b.close()
