import sys
FR_OLD='Ce navigateur contient encore des données de l’ancienne version web'
R=[
# --- backup schedule ---
('''  async dailyBackup(){
    const d=new Date(),dir=DIR+SEP+"Backups",f=dir+SEP+`backup-${stampOf(d)}.json`;
    try{await Neutralino.filesystem.getStats(f);return}catch(e){}
    if(!db.articles.length&&!db.machines.length)return;
    try{''','''  async dailyBackup(){
    const ev=bkEvery();if(ev==="off")return;
    const d=new Date(),dir=DIR+SEP+"Backups",f=dir+SEP+`backup-${stampOf(d)}.json`;
    try{await Neutralino.filesystem.getStats(f);return}catch(e){}
    if(!db.articles.length&&!db.machines.length)return;
    // weekly / monthly: only when the last backup file is old enough
    if(ev!=="day"){try{const L=(await Neutralino.filesystem.readDirectory(dir)).map(x=>x.entry).filter(x=>/^backup-\\d{4}-\\d\\d-\\d\\d\\.json$/.test(x)).sort(),last=L[L.length-1];
      if(last){const [y,m,dd]=last.slice(7,17).split("-").map(Number),ld=new Date(y,m-1,dd);
        if(ev==="week"&&(d-ld)<6.5*864e5)return;if(ev==="month"&&ld.getFullYear()===d.getFullYear()&&ld.getMonth()===d.getMonth())return}}catch(e){}}
    try{'''),
('''      for(const old of list.slice(0,-30)){try{await Neutralino.filesystem.remove(dir+SEP+old)}catch(e){}}''','''      for(const old of list.slice(0,-({day:30,week:26,month:24}[ev]||30))){try{await Neutralino.filesystem.remove(dir+SEP+old)}catch(e){}}'''),
('''async function takeSnapshot(force){
  if(!DIRTY&&!force)return;''','''const BK_EVERY=["off","day","week","month"],bkEvery=()=>BK_EVERY.includes(db.bkEvery)?db.bkEvery:"week";
async function takeSnapshot(force){
  if(db.snapOff&&!force)return;
  if(!DIRTY&&!force)return;'''),
('''style="margin:0">${esc(t("bkAuto",snaps.length))}</p>
        <div class="admact"><button class="btn" id="ad-bk">''','''style="margin:0">${esc(t("bkAuto",snaps.length))}</p>
        <label class="f">${esc(t("bkEveryL"))}<select id="ad-bkev">${BK_EVERY.map(k=>`<option value="${k}" ${bkEvery()===k?"selected":""}>${esc(t("bkEv_"+k))}</option>`).join("")}</select></label>
        <label class="chk"><input type="checkbox" id="ad-snap" ${db.snapOff?"":"checked"}> ${esc(t("bkSnapL"))}</label><p class="note" style="margin:0">${esc(t("bkEvT"))}</p>
        <div class="admact"><button class="btn" id="ad-bk">'''),
('''  $("#ad-ap").onchange=e=>{''','''  $("#ad-bkev").onchange=e=>{db.bkEvery=e.target.value;saveDB();if(db.bkEvery!=="off")desk.dailyBackup();toast(t("bkEv_"+db.bkEvery))};
  $("#ad-snap").onchange=e=>{db.snapOff=!e.target.checked;saveDB()};
  $("#ad-ap").onchange=e=>{'''),
('bkNow:"Back up now"','bkEveryL:"Full backup file", bkEv_off:"Off", bkEv_day:"Every day", bkEv_week:"Every week", bkEv_month:"Every month", bkEvT:"Backup files go to Backups. The 5-minute copies are a separate safety net (Backups/auto).", bkSnapL:"Copy every 5 minutes when something changed", bkNow:"Back up now"'),
('bkNow:"Sauvegarder','bkEveryL:"Fichier de sauvegarde complet", bkEv_off:"Désactivé", bkEv_day:"Chaque jour", bkEv_week:"Chaque semaine", bkEv_month:"Chaque mois", bkEvT:"Les fichiers vont dans Backups. Les copies toutes les 5 minutes sont une sécurité à part (Backups/auto).", bkSnapL:"Copie toutes les 5 minutes quand quelque chose a changé", bkNow:"Sauvegarder'),
('footDaily:"A backup copy is made every day (last 30 kept).",','footDaily:"Backup copies follow the schedule chosen in Admin (weekly by default).",'),
('footDaily:"Une copie de sauvegarde est faite chaque jour (les 30 dernières sont gardées).",','footDaily:"Les copies de sauvegarde suivent le rythme choisi dans Admin (chaque semaine par défaut).",'),
('["Une copie de tout est gardée toutes les 5 minutes quand quelque chose change.",','["Une copie de tout est gardée toutes les 5 minutes quand quelque chose change (désactivable dans Admin).","Dans Admin, la sauvegarde complète se règle : désactivée, chaque jour, chaque semaine (par défaut) ou chaque mois.",'),
('["A copy of everything is kept every 5 minutes when something changes.",','["A copy of everything is kept every 5 minutes when something changes (can be turned off in Admin).","In Admin, the full backup can be set to off, daily, weekly (default) or monthly.",'),
# --- web folder: start empty / bring old data / continue an existing folder ---
('''const roots={};let ready=null,files=new Map(),fileN=0;''','''const roots={};let ready=null,files=new Map(),fileN=0,take=!!W.__QA_TAKEOLD;
  // data kept in this browser by the earlier web version (only counted here)
  const oldData=async()=>{let n=0,m=0;try{const raw=localStorage.getItem("toollistmaker.db.v2");if(raw){const d=JSON.parse(raw);n=(d.articles||[]).length;m=(d.machines||[]).length}}catch(e){}
    try{const L=indexedDB.databases?await indexedDB.databases():[{name:"toolmanager"}];if(L.some(x=>x.name==="toolmanager")){const d=await new Promise(res=>{const r=indexedDB.open("toolmanager");r.onsuccess=()=>res(r.result);r.onerror=()=>res(null);r.onupgradeneeded=()=>{try{r.transaction.abort()}catch(e){}}});
      if(d&&d.objectStoreNames.contains("kv")){const raw=await new Promise(res=>{const q=d.transaction("kv").objectStore("kv").get("db");q.onsuccess=()=>res(q.result);q.onerror=()=>res(null)});d.close();if(raw){const x=JSON.parse(raw);if((x.articles||[]).length>=n){n=(x.articles||[]).length;m=(x.machines||[]).length}}}else if(d)d.close()}}catch(e){}
    return n||m?{n,m}:null};'''),
('''    if(!has&&!empty&&h.name.toLowerCase()!=="brochestuff")use=await h.getDirectoryHandle("BrocheStuff",{create:true});return use};''','''    if(!has&&!empty&&h.name.toLowerCase()!=="brochestuff")use=await h.getDirectoryHandle("BrocheStuff",{create:true});
    if(use!==h){has=false;for await(const [n] of use.entries())if(n==="data.json"||n==="users.json"){has=true;break}}
    return{use,has}};'''),
('''    if(W.__QA_WEBFS){roots.main=''','''    if(W.__QA_WEBFS&&!W.__QA_PICK){roots.main='''),
('''<p class="wfsn">${T.p2}</p><button class="btn red big" id="wfs-pick">''','''<p class="wfsn">${T.p2}</p><p class="wfsn">${T.has}</p><button class="btn red big" id="wfs-pick">'''),
('''        o.querySelector("#wfs-pick").onclick=async()=>{try{const u=await pick();if(!await perm(u,true))throw new Error("perm");roots.main=u;await hput("main",u);o.remove();done()}catch(e){''','''        o.querySelector("#wfs-pick").onclick=async()=>{try{const {use:u,has}=await pick();if(!await perm(u,true))throw new Error("perm");roots.main=u;await hput("main",u);
          // a folder with data is simply used as it is; an empty one + older data in this browser: ask
          const old=has?null:await oldData();
          if(!old){o.remove();done();return}
          const q=screen(`<h1>${T.oldT}</h1><p>${T.oldP(T.cnt(old))}</p><button class="btn red big" id="wfs-take">${T.take}</button><button class="btn ghost" id="wfs-skip">${T.skip}</button>`);
          q.querySelector("#wfs-take").onclick=()=>{take=true;q.remove();done()};q.querySelector("#wfs-skip").onclick=()=>{take=false;q.remove();done()}}catch(e){'''),
('''no:"Le navigateur n’a pas donné l’accès au dossier. Réessayez et choisissez « Autoriser » / « Modifier les fichiers »."}''','''no:"Le navigateur n’a pas donné l’accès au dossier. Réessayez et choisissez « Autoriser » / « Modifier les fichiers ».",
      has:"Vous avez déjà un dossier BrocheStuff (autre PC, programme Windows) ? Choisissez-le : tout reprend à partir de lui.",oldT:"Anciennes données dans ce navigateur",oldP:n=>`'''+FR_OLD+''' (${n}). Les reprendre dans ce dossier, ou commencer à vide ?`,take:"Les reprendre dans le dossier",skip:"Commencer à vide",cnt:o=>`${o.n} fiche${o.n>1?"s":""}, ${o.m} machine${o.m>1?"s":""}`}'''),
('''no:"The browser didn’t allow the folder. Try again and choose “Allow” / “Edit files”."}''','''no:"The browser didn’t allow the folder. Try again and choose “Allow” / “Edit files”.",
      has:"Already have a BrocheStuff folder (another PC, the Windows program)? Pick it: everything carries on from it.",oldT:"Older data in this browser",oldP:n=>`This browser still holds data from the earlier web version (${n}). Bring it into this folder, or start empty?`,take:"Bring it into the folder",skip:"Start empty",cnt:o=>`${o.n} sheet${o.n>1?"s":""}, ${o.m} machine${o.m>1?"s":""}`}'''),
('''return{connect,saveAs,name:()=>roots.main?roots.main.name:"",MAIN,''','''return{connect,saveAs,name:()=>roots.main?roots.main.name:"",MAIN,takeOld:()=>take,'''),
('''    else{try{const d2=JSON.parse(lsGet(DBKEY)''','''    else if(WEBFS&&!WEBFS.takeOld()){/* a new, empty folder: start empty */}
    else{try{const d2=JSON.parse(lsGet(DBKEY)'''),
]
for f in sys.argv[1:]:
  s=open(f).read()
  for a,b in R:
    assert s.count(a)==1,(f,s.count(a),a[:90])
    s=s.replace(a,b)
  s=s.replace("2.15.0","2.16.0") if f.endswith("config.json") else s
  open(f,'w').write(s);print("patched",f)
