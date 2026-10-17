/* Tool Manager · Tool List Maker — app logic (machines, articles, tool crib, preview, EN/FR) */
const $=s=>document.querySelector(s);
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const COLS=["t","type","diameter","ra","ls","z","holder","code"];
const AFIELDS=["number","index","designation","program","material","notes","preparedBy","approvedBy","date"];
const DBKEY="toollistmaker.db.v2", OLDKEY="toollistmaker.draft.v1", LOGOKEY="toollistmaker.logo.v1", LANGKEY="toollistmaker.lang", PVKEY="toollistmaker.preview";
const lsGet=k=>{try{return localStorage.getItem(k)}catch(e){return null}};
const lsSet=(k,v)=>{try{localStorage.setItem(k,v);return true}catch(e){return false}};
const uid=()=>Date.now().toString(36)+Math.random().toString(36).slice(2,7);

/* ---------- language ---------- */
let LANG=lsGet(LANGKEY)||"";
const pl=(n,one,many)=>n===1?one:many;
const I18N={
en:{
  allMachines:"All machines", logo:"Logo", logoT:"Set the logo printed on every sheet", backup:"Back up", backupT:"Save everything to one file, to keep safe or move to another PC", restore:"Restore", restoreT:"Load a backup file",
  download:"Download PDF", preview:"Preview", previewT:"Show or hide the live preview of the sheet", on:"On", off:"Off",
  machines:"Machines", homeSub:"Click a machine to see its articles and make tool lists.", homeSearch:"Find an article, or a tool code like F241…",
  firstMachine:"Add your first machine", firstMachineP:"Create one place for each CNC in the shop. Inside each machine you add its articles, and each article gets its tool list.", addMachine:"+ Add machine",
  ofDone:n=>`of ${n} ${pl(n,"article","articles")} done`, done:"Done", inProgress:"In progress", notStarted:"Not started", all:"All",
  machine:"Machine", slashDone:n=>`/ ${n} done`, nInProgress:n=>`${n} in progress`, edit:"Edit", editT:"Rename or delete",
  footWeb:(m,n)=>`${m} ${pl(m,"machine","machines")} · ${n} ${pl(n,"article","articles")} · saved in this browser on this PC`,
  footDesk:(m,n)=>`${m} ${pl(m,"machine","machines")} · ${n} ${pl(n,"article","articles")} · saved automatically in Documents\\Tool List Maker`,
  footDaily:"A backup copy is made every day (last 30 kept).",
  notBacked:"Not backed up yet. Click “Back up” in the top bar to save everything to a file.", backedDays:d=>`Last backup ${d} days ago.`, backedOn:d=>`Last backup ${d}`,
  codeUsed:(c,n)=>`Tool code ${c} is used in ${n} ${pl(n,"article","articles")}`, codeStarts:c=>`No article uses exactly ${c} · showing codes starting with ${c}`, nFound:n=>`${n} ${pl(n,"article","articles")} found`,
  nothingFilter:"Nothing in this filter", searchHint:"Search looks at article number, designation, program and tool codes (F241, M318).", noMatch:"No article matches", noMatchOn:m=>`No article on ${m} matches`,
  machSearch:"Find an article, program or tool code (F241)…", newArticle:"+ New article", mCount:(n,d)=>`${n} ${pl(n,"article","articles")} · ${d} done`,
  noArticlesOn:m=>`No articles on ${m} yet`, noArticlesP:"Add an article, fill in its tools, and download the tool list sheet.",
  thArticle:"Article", thIndex:"Index", thDes:"Designation", thProg:"Program", thMachine:"Machine", thUses:"Uses", thTools:"Tools", thStatus:"Status", thUpdated:"Updated",
  noNumber:"No number", pdfT:"Download the PDF", copy:"Copy", copyT:"Copy this article (for a new index or another machine)", del:"Delete", confirm:"Confirm", deleted:x=>`Deleted ${x}`, articleWord:"article",
  editMachine:"Edit machine", addMachineT:"Add machine", machineName:"Machine name", machineModel:"Model / note (optional)", modelPh:"3-axis · Haas NGC", delMachine:"Delete machine",
  cancel:"Cancel", save:"Save", needName:"Give the machine a name.", nameTaken:"A machine with this name already exists.", machineSaved:"Machine saved", machineAdded:n=>`${n} added`,
  delWith:n=>`Delete with its ${n} ${pl(n,"article","articles")}?`, clickDel:"Click again to delete", machineDeleted:n=>`${n} deleted`, clickConfirm:"Click again to confirm",
  copyTitle:"Copy article", copyP:"Makes a new article with the same tools. Use it for a new index, or when the same article runs on another machine.", copyOn:"Put the copy on", articleNumber:"Article number", index:"Index", makeCopy:"Make copy", copyMade:"Copy made. You're now editing the copy.",
  article:"Article", autoSaved:"Saved automatically", designation:"Designation", desPh:"Support bracket", program:"Program", material:"Material",
  tools:"Tools", nTools:n=>`${n} ${pl(n,"tool","tools")}`, colTool:"Tool", colType:"Type", colHolder:"Holder", colCode:"Code", typePh:"END MILL", addTool:"+ Add tool",
  excelNote:"<b>From Excel:</b> copy the rows (Tool, Type, Ø, R/°, LS, Z, Holder, Code) and paste into any cell. <b>Enter</b> in the last row adds a new one.",
  notesSign:"Notes & sign-off", notes:"Notes", notesPh:"Printed on the sheet. Leave empty for blank lines to write on.", preparedBy:"Prepared by", approvedBy:"Approved by", date:"Date", datePh:"dd/mm/yyyy",
  signNote:"Leave Prepared by / Approved by empty to sign by hand on paper.", pages:n=>`A4 · ${n} ${pl(n,"page","pages")}`, pvError:"Preview error: ",
  up:"Move up", down:"Move down", remove:"Remove", markDone:"✓ Done", stillEmpty:n=>`${n} ${pl(n,"box","boxes")} still empty`, allFilled:"All boxes filled",
  markedDoneMiss:n=>`Marked as done · ${n} ${pl(n,"box","boxes")} still empty`, markedDone:"Marked as done",
  dup:(num,ix,m)=>`${num}${ix?" index "+ix:""} already exists on ${m}.`, movedTo:m=>`Moved to ${m}`, pasted:n=>`Pasted ${n} ${pl(n,"row","rows")}`, newArticleCrumb:"New article",
  savedTo:n=>`Saved ${n} to your Downloads`, saved:n=>`Saved ${n}`, openPdf:"Open PDF", pdfFail:"Could not make the PDF: ",
  backupDesk:"Backup saved. Keep a copy on a USB stick or the network too.", backupWeb:"Backup saved to your Downloads. Keep it somewhere safe.", backupFail:"Could not save the backup: ",
  restoreTitle:"Restore backup", restoreHas:(m,n)=>`This file has <b>${m} ${pl(m,"machine","machines")}</b> and <b>${n} ${pl(n,"article","articles")}</b>.`, restoreQ:"Replace everything in the program with it, or add it to what's already here?",
  addCurrent:"Add to current", replaceAll:"Replace all", restored:"Backup restored", added:"Backup added", opened:f=>`Opened ${f}`, notBackup:"That file isn't a Tool List Maker backup.",
  logoSet:"Logo set. It will be on every sheet.", storeFail:"Could not save: browser storage is full or blocked. Use Back up now.", deskFail:"Could not save to Documents\\Tool List Maker: ",
  saveSheetT:"Save tool list", saveBackupT:"Save backup", pdfFile:"PDF file", backupFile:"Backup file", filePrefix:"ToolList", backupPrefix:"ToolListMaker_backup", unassigned:"Unassigned",
  stackT:(d,p,n)=>`${d} done · ${p} in progress · ${n} not started`,
  types:["FACE MILL","END MILL","BULL NOSE","BALL NOSE","SHOULDER MILL","DRILL","SPOT DRILL","CENTER DRILL","CHAMFER MILL","TAP","THREAD MILL","REAMER","BORING BAR","T-SLOT","INSERT DRILL","PROBE"],
  holders:["ER32","ER25","ER16","SHRINK-FIT","WELDON","HYDRAULIC","SHELL MILL ARBOR","TAPPING CHUCK","DRILL CHUCK"]
},
fr:{
  allMachines:"Toutes les machines", logo:"Logo", logoT:"Choisir le logo imprimé sur chaque fiche", backup:"Sauvegarder", backupT:"Enregistrer tout dans un fichier, à garder en sécurité ou à copier sur un autre PC", restore:"Restaurer", restoreT:"Charger un fichier de sauvegarde",
  download:"Télécharger le PDF", preview:"Aperçu", previewT:"Afficher ou masquer l'aperçu en direct de la fiche", on:"Oui", off:"Non",
  machines:"Machines", homeSub:"Cliquez sur une machine pour voir ses articles et faire les fiches outils.", homeSearch:"Chercher un article ou un code outil (ex. F241)…",
  firstMachine:"Ajoutez votre première machine", firstMachineP:"Créez un espace pour chaque machine CNC de l'atelier. Dans chaque machine, vous ajoutez ses articles, et chaque article a sa fiche outils.", addMachine:"+ Ajouter une machine",
  ofDone:n=>`${pl(n,"article terminé","articles terminés")} sur ${n}`, done:"Terminé", inProgress:"En cours", notStarted:"Non commencé", all:"Tous",
  machine:"Machine", slashDone:n=>`/ ${n} ${pl(n,"terminé","terminés")}`, nInProgress:n=>`${n} en cours`, edit:"Modifier", editT:"Renommer ou supprimer",
  footWeb:(m,n)=>`${m} ${pl(m,"machine","machines")} · ${n} ${pl(n,"article","articles")} · enregistré dans ce navigateur sur ce PC`,
  footDesk:(m,n)=>`${m} ${pl(m,"machine","machines")} · ${n} ${pl(n,"article","articles")} · enregistré automatiquement dans Documents\\Tool List Maker`,
  footDaily:"Une copie de sauvegarde est faite chaque jour (les 30 dernières sont gardées).",
  notBacked:"Pas encore sauvegardé. Cliquez sur « Sauvegarder » en haut pour tout enregistrer dans un fichier.", backedDays:d=>`Dernière sauvegarde il y a ${d} jours.`, backedOn:d=>`Dernière sauvegarde le ${d}`,
  codeUsed:(c,n)=>`Le code outil ${c} est utilisé dans ${n} ${pl(n,"article","articles")}`, codeStarts:c=>`Aucun article n'utilise exactement ${c} · codes commençant par ${c}`, nFound:n=>`${n} ${pl(n,"article trouvé","articles trouvés")}`,
  nothingFilter:"Rien dans ce filtre", searchHint:"La recherche porte sur le numéro d'article, la désignation, le programme et les codes outils (F241, M318).", noMatch:"Aucun article ne correspond", noMatchOn:m=>`Aucun article sur ${m} ne correspond`,
  machSearch:"Chercher un article, un programme ou un code outil (F241)…", newArticle:"+ Nouvel article", mCount:(n,d)=>`${n} ${pl(n,"article","articles")} · ${d} ${pl(d,"terminé","terminés")}`,
  noArticlesOn:m=>`Aucun article sur ${m} pour l'instant`, noArticlesP:"Ajoutez un article, remplissez ses outils et téléchargez la fiche outils.",
  thArticle:"Article", thIndex:"Indice", thDes:"Désignation", thProg:"Programme", thMachine:"Machine", thUses:"Utilisé en", thTools:"Outils", thStatus:"État", thUpdated:"Modifié",
  noNumber:"Sans numéro", pdfT:"Télécharger le PDF", copy:"Copier", copyT:"Copier cet article (nouvel indice ou autre machine)", del:"Supprimer", confirm:"Confirmer", deleted:x=>`${x} supprimé`, articleWord:"Article",
  editMachine:"Modifier la machine", addMachineT:"Ajouter une machine", machineName:"Nom de la machine", machineModel:"Modèle / remarque (facultatif)", modelPh:"3 axes · Haas NGC", delMachine:"Supprimer la machine",
  cancel:"Annuler", save:"Enregistrer", needName:"Donnez un nom à la machine.", nameTaken:"Une machine porte déjà ce nom.", machineSaved:"Machine enregistrée", machineAdded:n=>`${n} ajoutée`,
  delWith:n=>`Supprimer avec ${pl(n,"son article","ses "+n+" articles")} ?`, clickDel:"Cliquez encore pour supprimer", machineDeleted:n=>`${n} supprimée`, clickConfirm:"Cliquez encore pour confirmer",
  copyTitle:"Copier l'article", copyP:"Crée un nouvel article avec les mêmes outils. Pour un nouvel indice, ou quand le même article passe sur une autre machine.", copyOn:"Mettre la copie sur", articleNumber:"Numéro d'article", index:"Indice", makeCopy:"Créer la copie", copyMade:"Copie créée. Vous modifiez maintenant la copie.",
  article:"Article", autoSaved:"Enregistré automatiquement", designation:"Désignation", desPh:"Support", program:"Programme", material:"Matière",
  tools:"Outils", nTools:n=>`${n} ${pl(n,"outil","outils")}`, colTool:"Outil", colType:"Type", colHolder:"Porte-outil", colCode:"Code", typePh:"FRAISE 2T", addTool:"+ Ajouter un outil",
  excelNote:"<b>Depuis Excel :</b> copiez les lignes (Outil, Type, Ø, R/°, LS, Z, Porte-outil, Code) et collez-les dans n'importe quelle case. <b>Entrée</b> sur la dernière ligne ajoute une ligne.",
  notesSign:"Remarques et visa", notes:"Remarques", notesPh:"Imprimé sur la fiche. Laissez vide pour avoir des lignes à remplir à la main.", preparedBy:"Établi par", approvedBy:"Approuvé par", date:"Date", datePh:"jj/mm/aaaa",
  signNote:"Laissez Établi par / Approuvé par vides pour signer à la main sur papier.", pages:n=>`A4 · ${n} page${n>1?"s":""}`, pvError:"Erreur d'aperçu : ",
  up:"Monter", down:"Descendre", remove:"Supprimer", markDone:"✓ Terminé", stillEmpty:n=>`${n} ${pl(n,"case encore vide","cases encore vides")}`, allFilled:"Toutes les cases sont remplies",
  markedDoneMiss:n=>`Marqué terminé · ${n} ${pl(n,"case encore vide","cases encore vides")}`, markedDone:"Marqué terminé",
  dup:(num,ix,m)=>`${num}${ix?" indice "+ix:""} existe déjà sur ${m}.`, movedTo:m=>`Déplacé vers ${m}`, pasted:n=>`${n} ${pl(n,"ligne collée","lignes collées")}`, newArticleCrumb:"Nouvel article",
  savedTo:n=>`${n} enregistré dans Téléchargements`, saved:n=>`${n} enregistré`, openPdf:"Ouvrir le PDF", pdfFail:"Impossible de créer le PDF : ",
  backupDesk:"Sauvegarde enregistrée. Gardez aussi une copie sur clé USB ou sur le réseau.", backupWeb:"Sauvegarde enregistrée dans Téléchargements. Gardez-la en lieu sûr.", backupFail:"Impossible d'enregistrer la sauvegarde : ",
  restoreTitle:"Restaurer une sauvegarde", restoreHas:(m,n)=>`Ce fichier contient <b>${m} ${pl(m,"machine","machines")}</b> et <b>${n} ${pl(n,"article","articles")}</b>.`, restoreQ:"Remplacer tout le contenu du programme, ou l'ajouter à ce qui existe déjà ?",
  addCurrent:"Ajouter", replaceAll:"Tout remplacer", restored:"Sauvegarde restaurée", added:"Sauvegarde ajoutée", opened:f=>`${f} ouvert`, notBackup:"Ce fichier n'est pas une sauvegarde Tool List Maker.",
  logoSet:"Logo enregistré. Il sera sur toutes les fiches.", storeFail:"Enregistrement impossible : le stockage du navigateur est plein ou bloqué. Faites une sauvegarde maintenant.", deskFail:"Impossible d'enregistrer dans Documents\\Tool List Maker : ",
  saveSheetT:"Enregistrer la fiche outils", saveBackupT:"Enregistrer la sauvegarde", pdfFile:"Fichier PDF", backupFile:"Fichier de sauvegarde", filePrefix:"FicheOutils", backupPrefix:"ToolListMaker_sauvegarde", unassigned:"Non affecté",
  stackT:(d,p,n)=>`${d} ${pl(d,"terminé","terminés")} · ${p} en cours · ${n} non ${pl(n,"commencé","commencés")}`,
  types:["FRAISE À SURFACER","FRAISE 2T","FRAISE TORIQUE","FRAISE BOULE","FRAISE À ÉPAULER","FORET","FORET À CENTRER","FORET À POINTER","FRAISE À CHANFREINER","TARAUD","FRAISE À FILETER","ALÉSOIR","BARRE D'ALÉSAGE","FRAISE À RAINURER EN T","FORET À PLAQUETTES","PALPEUR"],
  holders:["ER32","ER25","ER16","FRETTAGE","WELDON","HYDRAULIQUE","MANDRIN PORTE-FRAISE","MANDRIN DE TARAUDAGE","MANDRIN DE PERÇAGE"]
}};
const t=(k,...a)=>{const v=(I18N[LANG]||I18N.en)[k];return typeof v==="function"?v(...a):v};

function toast(m,act){const el=$("#toast");el.innerHTML="";el.append(document.createTextNode(m));
  if(act){const b=document.createElement("button");b.className="tact";b.textContent=act.label;b.onclick=()=>{el.hidden=true;act.fn()};el.append(b)}
  el.hidden=false;clearTimeout(toast.t);toast.t=setTimeout(()=>el.hidden=true,act?7000:2600)}
const today=()=>{const d=new Date();return `${String(d.getDate()).padStart(2,"0")}/${String(d.getMonth()+1).padStart(2,"0")}/${d.getFullYear()}`};
const when=ts=>{if(!ts)return"";const d=new Date(ts);return `${String(d.getDate()).padStart(2,"0")}/${String(d.getMonth()+1).padStart(2,"0")}/${d.getFullYear()}`};

/* ---------- value clean-up ---------- */
const clean=v=>{v=String(v??"").trim();return v==="/"||v==="-"||v==="—"?"":v};
const normT=v=>{v=clean(v);const m=v.match(/^[Tt]?\s*0*(\d+)$/);return m?"T"+m[1].padStart(2,"0"):v.toUpperCase()};
const normDia=v=>clean(v).replace(/^[øØ⌀Dd]\s*/,"").replace(",",".");
function normRA(v){v=clean(v);if(!v)return{kind:"",val:""};
  if(/^r/i.test(v))return{kind:"R",val:v.replace(/^r\s*/i,"").replace(",",".")};
  if(/['°º]|deg/i.test(v))return{kind:"A",val:v.replace(/[^\d.,]/g,"").replace(",",".")};
  return{kind:"R",val:v.replace(",",".")}}
const realTools=ts=>(ts||[]).filter(x=>COLS.some(k=>k!=="t"&&clean(x[k])));

/* sheet drawing: see js/sheet-pdf.js */

/* ---------- desktop program layer (Neutralino) ---------- */
const DESK=typeof window.NL_PORT!=="undefined"&&typeof window.Neutralino!=="undefined";
let DIR="",SEP="\\";
const stampOf=d=>`${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,"0")}-${String(d.getDate()).padStart(2,"0")}`;
const desk={
  t:null,pending:false,
  async init(){
    Neutralino.init();
    Neutralino.events.on("windowClose",async()=>{try{if(edTimer){clearTimeout(edTimer);edTimer=null}desk.pending=true;await desk.flush()}finally{Neutralino.app.exit()}});
    const docs=await Neutralino.os.getPath("documents");SEP=docs.includes("\\")?"\\":"/";DIR=docs.replace(/[\\/]+$/,"")+SEP+"Tool List Maker";
    for(const d of [DIR,DIR+SEP+"Backups",DIR+SEP+"Sheets"]){try{await Neutralino.filesystem.createDirectory(d)}catch(e){}}
  },
  async read(f){return JSON.parse(await Neutralino.filesystem.readFile(DIR+SEP+f))},
  async load(){try{return await desk.read("data.json")}catch(e){try{return await desk.read("data.previous.json")}catch(e2){return null}}},
  save(){desk.pending=true;clearTimeout(desk.t);desk.t=setTimeout(desk.flush,300)},
  async flush(){
    if(!desk.pending)return;desk.pending=false;clearTimeout(desk.t);
    const p=DIR+SEP+"data.json",prev=DIR+SEP+"data.previous.json";
    try{
      try{await Neutralino.filesystem.remove(prev)}catch(e){}
      try{await Neutralino.filesystem.copy(p,prev)}catch(e){}
      await Neutralino.filesystem.writeFile(p,JSON.stringify({...db,logo,lang:LANG}));
    }catch(e){toast(t("deskFail")+(e.message||e.code||e))}
  },
  async dailyBackup(){
    const d=new Date(),dir=DIR+SEP+"Backups",f=dir+SEP+`backup-${stampOf(d)}.json`;
    try{await Neutralino.filesystem.getStats(f);return}catch(e){}
    if(!db.articles.length&&!db.machines.length)return;
    try{
      await Neutralino.filesystem.writeFile(f,JSON.stringify({app:"tool-list-maker",version:3,savedAt:d.toISOString(),machines:db.machines,articles:db.articles,catalog:db.catalog,logo}));
      db.lastBackup=Date.now();saveDB();
      const list=(await Neutralino.filesystem.readDirectory(dir)).map(x=>x.entry).filter(x=>/^backup-\d{4}-\d\d-\d\d\.json$/.test(x)).sort();
      for(const old of list.slice(0,-30)){try{await Neutralino.filesystem.remove(dir+SEP+old)}catch(e){}}
    }catch(e){}
  },
  async saveAs(name,blob,kind){
    const pdf=kind==="pdf",csv=kind==="csv",def=DIR+SEP+(pdf?"Sheets"+SEP:csv?"":"Backups"+SEP)+name;
    let path=await Neutralino.os.showSaveDialog(pdf?t("saveSheetT"):csv?t("orderList"):t("saveBackupT"),{defaultPath:def,filters:[pdf?{name:t("pdfFile"),extensions:["pdf"]}:csv?{name:"CSV",extensions:["csv"]}:{name:t("backupFile"),extensions:["json"]}]});
    if(!path)return null;
    if(!new RegExp("\\."+kind+"$","i").test(path))path+="."+kind;
    await Neutralino.filesystem.writeBinaryFile(path,await blob.arrayBuffer());
    return path;
  }
};

/* ---------- data ---------- */
let db={machines:[],articles:[],lastBackup:0}, logo=null, canStore=true;
async function loadDB(){
  if(DESK){const d=await desk.load();
    if(d&&Array.isArray(d.machines)){const {logo:lg,lang,...rest}=d;db={lastBackup:0,...rest};logo=lg||null;if(!LANG&&lang)LANG=lang}
    else{try{const d2=JSON.parse(lsGet(DBKEY)||"null");if(d2&&Array.isArray(d2.machines))db={lastBackup:0,...d2}}catch(e){}}
    db.migrated=true;saveDB();await desk.dailyBackup();return}
  try{const d=JSON.parse(lsGet(DBKEY)||"null");if(d&&Array.isArray(d.machines))db={lastBackup:0,...d}}catch(e){}
  try{logo=JSON.parse(lsGet(LOGOKEY)||"null")}catch(e){}
  try{const old=JSON.parse(lsGet(OLDKEY)||"null");
    if(old&&old.article&&!db.migrated&&realTools(old.tools).length){
      const name=clean(old.article.machine)||t("unassigned");let m=db.machines.find(x=>x.name.toLowerCase()===name.toLowerCase());
      if(!m){m={id:uid(),name,model:"",createdAt:Date.now()};db.machines.push(m)}
      const {machine,...art}=old.article;db.articles.push({id:uid(),machineId:m.id,article:art,tools:old.tools,createdAt:Date.now(),updatedAt:Date.now()});
    }}catch(e){}
  db.migrated=true;saveDB();
}
function ensureDB(){if(!Array.isArray(db.catalog))db.catalog=[]}
function saveDB(){ensureDB();if(DESK){desk.save();return}canStore=lsSet(DBKEY,JSON.stringify(db));if(!canStore)toast(t("storeFail"))}
const M=id=>db.machines.find(m=>m.id===id);
const A=id=>db.articles.find(a=>a.id===id);
const artsOf=mid=>db.articles.filter(a=>a.machineId===mid);
const sheetData=art=>({article:{...art.article,machine:M(art.machineId)?.name||""},tools:art.tools});
function fileName(art,ext){const s=x=>String(x||"").trim().replace(/[\\/:*?"<>|]+/g,"-").replace(/\s+/g,"_");const a=art.article||{};return `${t("filePrefix")}_${s(a.number)||"sheet"}${a.index?"_"+s(a.index):""}.${ext}`}
async function download(name,blob,kind){if(DESK)return desk.saveAs(name,blob,kind);const a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download=name;document.body.appendChild(a);a.click();setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove()},1500);return "downloads"}
async function downloadPDF(art){try{const name=fileName(art,"pdf");const p=await download(name,makePDF(sheetData(art)).output("blob"),"pdf");if(!p)return;
  if(DESK)toast(t("saved",name),{label:t("openPdf"),fn:()=>Neutralino.os.open(p).catch(()=>Neutralino.os.open("file:///"+p.replace(/\\/g,"/")))});else toast(t("savedTo",name))}
  catch(e){toast(t("pdfFail")+(e.message||e))}}

/* ---------- routing (#m-<id>, #a-<id>) ---------- */
let route={view:"home"};
function go(hash){if(location.hash!==hash)location.hash=hash;else render()}
window.addEventListener("hashchange",render);
function parseRoute(){const h=location.hash.slice(1);
  if(h.startsWith("a-")&&A(h.slice(2)))return{view:"article",id:h.slice(2)};
  if(h.startsWith("m-")&&M(h.slice(2)))return{view:"machine",id:h.slice(2)};
  if(h==="crib")return{view:"crib"};
  if(h.startsWith("c-")){const k=decodeURIComponent(h.slice(2));if(C_(k))return{view:"code",code:normCode(k)};return{view:"crib"}}
  return{view:"home"}}
function arm(btn,fn,label){
  if(btn.classList.contains("armed")){fn();return}
  const old=btn.innerHTML;btn.classList.add("armed");btn.textContent=label||t("clickConfirm");
  setTimeout(()=>{if(btn.isConnected){btn.classList.remove("armed");btn.innerHTML=old}},3200);
}
const searchIcon=`<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>`;
const triIcon=`<svg viewBox="0 0 30 26"><path d="M15 2 L28 24 H2 Z" fill="none" stroke="#10171e" stroke-width="1.6" stroke-linejoin="round"/></svg>`;
const dlIcon=`<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 3v12m0 0-5-5m5 5 5-5M4 19h16"/></svg>`;
const eyeIcon=`<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/></svg>`;

/* ---------- chrome (top bar, lists) in the chosen language ---------- */
function chrome(){
  document.documentElement.lang=LANG||"en";
  $("#home").title=t("allMachines");
  const s=(id,txt,title)=>{const b=$(id);b.textContent=txt;b.title=title};
  s("#b-logo",t("logo"),t("logoT"));s("#b-backup",t("backup"),t("backupT"));s("#b-restore",t("restore"),t("restoreT"));
  document.querySelectorAll("[data-lang]").forEach(b=>b.setAttribute("aria-pressed",b.dataset.lang===LANG));
  $("#nav-m").textContent=t("navMachines");$("#nav-c").textContent=t("navCrib");
  $("#types").innerHTML=t("types").map(x=>`<option>${esc(x)}</option>`).join("");
  $("#holders").innerHTML=t("holders").map(x=>`<option>${esc(x)}</option>`).join("");
}
function setLang(l){if(edTimer){clearTimeout(edTimer);flushEditor()}LANG=l;lsSet(LANGKEY,l);if(DESK)saveDB();chrome();render()}
document.querySelectorAll("[data-lang]").forEach(b=>b.onclick=()=>setLang(b.dataset.lang));
document.querySelectorAll("[data-nav]").forEach(b=>b.onclick=()=>go(b.dataset.nav));
function chooseLanguage(){
  const ov=$("#ov");ov.innerHTML=`<div class="dlg langdlg" role="dialog" aria-modal="true"><header><h3>Choose your language · Choisissez votre langue</h3></header>
    <div class="bd"><div class="langpick"><button data-pick="en"><b>EN</b><span>English</span></button><button data-pick="fr"><b>FR</b><span>Français</span></button></div>
    <p class="note" style="margin:0">You can change it any time with EN / FR at the top. · Vous pouvez changer à tout moment avec EN / FR en haut.</p></div></div>`;
  ov.hidden=false;ov.dataset.lock="1";
  ov.querySelectorAll("[data-pick]").forEach(b=>b.onclick=()=>{delete ov.dataset.lock;closeDlg();setLang(b.dataset.pick)});
}

function render(){
  if(edTimer){clearTimeout(edTimer);edTimer=null;flushEditor()}
  route=parseRoute();
  const cr=$("#crumbs"), tb=$("#tbar");tb.innerHTML="";
  if(route.view!=="article")pvTeardown();
  document.querySelectorAll("[data-nav]").forEach(b=>b.setAttribute("aria-current",String((b.dataset.nav==="#crib")===(route.view==="crib"||route.view==="code"))));
  if(route.view==="home"){cr.innerHTML="";renderHome()}
  else if(route.view==="crib"){cr.innerHTML="";renderCrib()}
  else if(route.view==="code"){const c=C_(route.code);cr.innerHTML=`<i>/</i><a data-go="#crib">${esc(t("crib"))}</a><i>/</i><span>${esc(c.code)}</span>`;renderCode(c)}
  else if(route.view==="machine"){const m=M(route.id);cr.innerHTML=`<i>/</i><span>${esc(m.name)}</span>`;renderMachine(m)}
  else{const art=A(route.id),m=M(art.machineId);cr.innerHTML=`<i>/</i><a data-go="#m-${m.id}">${esc(m.name)}</a><i>/</i><span>${esc(art.article.number||t("newArticleCrumb"))}</span>`;
    tb.innerHTML=`<button class="tb pvtog" id="b-pv" title="${esc(t("previewT"))}" aria-pressed="${pvOn}">${eyeIcon}${esc(t("preview"))}<span class="sw"><i></i></span></button><button class="tb dl" id="b-dl">${dlIcon}${esc(t("download"))}</button>`;
    $("#b-dl").onclick=()=>{flushEditor();downloadPDF(A(route.id))};$("#b-pv").onclick=togglePreview;renderEditor(art)}
  cr.querySelectorAll("[data-go]").forEach(a=>a.onclick=()=>go(a.dataset.go));
}

/* ---------- progress & status ---------- */
const REQ_TOOL=["type","diameter","ls","holder","code"], REQ_ART=["number","designation","program"];
function progress(a){
  const ts=realTools(a.tools);let tot=REQ_ART.length+(ts.length?0:REQ_TOOL.length),ok=REQ_ART.filter(k=>clean(a.article[k])).length;
  ts.forEach(x=>{tot+=REQ_TOOL.length;ok+=REQ_TOOL.filter(k=>clean(x[k])).length});
  return Math.round(ok/tot*100);
}
function missing(a){const ts=realTools(a.tools);let n=REQ_ART.filter(k=>!clean(a.article[k])).length;ts.forEach(x=>n+=REQ_TOOL.filter(k=>!clean(x[k])).length);return n+(ts.length?0:REQ_TOOL.length)}
const statusOf=a=>a.status==="done"?"done":realTools(a.tools).length?"progress":"new";
const SL=s=>({new:t("notStarted"),progress:t("inProgress"),done:t("done")}[s]);
function statusCell(a){const s=statusOf(a),p=s==="done"?100:progress(a);
  return `<div class="st st-${s}"><span class="pill">${s==="done"?"✓ ":""}${esc(SL(s))}</span><div class="bar"><i style="width:${p}%"></i></div><span class="pct">${p}%</span></div>`}
function counts(list){const c={all:list.length,new:0,progress:0,done:0};list.forEach(a=>c[statusOf(a)]++);return c}
function stackBar(c,big){const n=c.all||1;return `<div class="stack${big?" big":""}" title="${esc(t("stackT",c.done,c.progress,c.new))}"><i class="d" style="width:${c.done/n*100}%"></i><i class="p" style="width:${c.progress/n*100}%"></i></div>`}
let stFilter="all";
function filterChips(list){const c=counts(list);
  return `<div class="chips" role="group">${[["all",t("all")],["new",t("notStarted")],["progress",t("inProgress")],["done",t("done")]].map(([k,l])=>`<button class="chip c-${k}" data-f="${k}" aria-pressed="${stFilter===k}">${k==="all"?"":`<i></i>`}${esc(l)}<b>${c[k]}</b></button>`).join("")}</div>`}
function wireChips(box,redraw){box.querySelectorAll("[data-f]").forEach(b=>b.onclick=()=>{stFilter=b.dataset.f;redraw()})}
const applyFilter=list=>stFilter==="all"?list:list.filter(a=>statusOf(a)===stFilter);

/* ---------- search (tool codes F241 / M318 match exactly) ---------- */
const isCode=q=>/^[fm]\s*\d+[a-z]?$/i.test(q.trim());
function searchArticles(list,q){
  q=q.trim().toLowerCase();
  if(isCode(q)){const code=q.replace(/\s+/g,"");
    let hits=list.filter(a=>a.tools.some(x=>clean(x.code).toLowerCase()===code));let exact=true;
    if(!hits.length){hits=list.filter(a=>a.tools.some(x=>clean(x.code).toLowerCase().startsWith(code)));exact=false}
    return{hits:hits.sort((x,y)=>(y.updatedAt||0)-(x.updatedAt||0)),code,exact}}
  const terms=q.split(/\s+/).filter(Boolean);
  return{hits:list.filter(a=>{const hay=[a.article.number,a.article.index,a.article.designation,a.article.program,a.article.material,...a.tools.map(x=>x.code)].join(" ").toLowerCase();return terms.every(w=>hay.includes(w))})
    .sort((x,y)=>(y.updatedAt||0)-(x.updatedAt||0)),code:null}
}
function usesCell(a,code,exact){const ts=a.tools.filter(x=>{const c=clean(x.code).toLowerCase();return exact?c===code:c.startsWith(code)});
  return `<div class="uses">${ts.map(x=>`<span class="use"><b>${esc(normT(x.t))}</b>${esc(clean(x.code).toUpperCase())}</span>`).join("")}</div>`}

/* ---------- home: machines ---------- */
let homeQ="";
function backupNote(){
  if(DESK)return `<div class="foot"><span>${esc(t("footDesk",db.machines.length,db.articles.length))}</span><span>${esc(t("footDaily"))}</span></div>`;
  const days=db.lastBackup?Math.floor((Date.now()-db.lastBackup)/86400000):null, n=db.articles.length;
  return `<div class="foot"><span>${esc(t("footWeb",db.machines.length,n))}</span>
    ${n?(days===null?`<span class="warn">${esc(t("notBacked"))}</span>`:days>=7?`<span class="warn">${esc(t("backedDays",days))}</span>`:`<span>${esc(t("backedOn",when(db.lastBackup)))}</span>`):""}</div>`;
}
function renderHome(){
  $("#view").innerHTML=`<div class="page">
    <div class="ph"><div><h2>${esc(t("machines"))}<b>.</b></h2><div class="sub">${esc(t("homeSub"))}</div></div><span class="sp"></span>
      <div class="search">${searchIcon}<input id="q" type="search" placeholder="${esc(t("homeSearch"))}" value="${esc(homeQ)}" autocomplete="off"></div></div>
    <div id="hres"></div>
    ${backupNote()}
  </div>`;
  const q=$("#q");q.oninput=()=>{homeQ=q.value;drawHome()};drawHome();
  if(homeQ){q.focus();q.setSelectionRange(q.value.length,q.value.length)}
}
function resultBlock(r,showMachine,emptyMsg){
  const list=applyFilter(r.hits),C=r.code?esc(r.code.toUpperCase()):"";
  const head=r.code?`<p class="res-h">${r.exact?t("codeUsed",C,r.hits.length):t("codeStarts",C)}</p>`:`<p class="res-h">${esc(t("nFound",r.hits.length))}</p>`;
  return `<div class="resbar">${head}<span class="sp"></span>${filterChips(r.hits)}</div>`+
    (list.length?articleTable(list,showMachine,r.code?{code:r.code,exact:r.exact}:null):`<div class="empty"><h3>${r.hits.length?esc(t("nothingFilter")):emptyMsg}</h3>${r.hits.length?"":`<p>${esc(t("searchHint"))}</p>`}</div>`);
}
function drawHome(){
  const box=$("#hres"),q=homeQ.trim();
  if(q){box.innerHTML=resultBlock(searchArticles(db.articles,q),true,esc(t("noMatch")));wireChips(box,drawHome);wireArticleTable(box);return}
  if(!db.machines.length){box.innerHTML=`<div class="empty"><h3>${esc(t("firstMachine"))}</h3><p>${esc(t("firstMachineP"))}</p><button class="btn red" id="addm">${esc(t("addMachine"))}</button></div>`;$("#addm").onclick=()=>machineDialog();return}
  const c=counts(db.articles);
  box.innerHTML=`${c.all?`<section class="overall">
      <div class="ov-n"><b>${c.done}</b><span>${esc(t("ofDone",c.all))}</span></div>
      <div class="ov-bar">${stackBar(c,true)}<div class="legend2"><span class="l-d"><i></i>${esc(t("done"))} ${c.done}</span><span class="l-p"><i></i>${esc(t("inProgress"))} ${c.progress}</span><span class="l-n"><i></i>${esc(t("notStarted"))} ${c.new}</span><span class="sp"></span><b>${Math.round(c.done/c.all*100)}%</b></div></div>
    </section>`:""}
    <div class="mgrid">${db.machines.map(m=>{const mc=counts(artsOf(m.id));return `<div class="mc" role="button" tabindex="0" data-m="${m.id}">
      <button class="edit-m" data-edit="${m.id}" title="${esc(t("editT"))}">${esc(t("edit"))}</button>
      <span class="lb">${esc(t("machine"))}</span><span class="nm">${esc(m.name)}</span><span class="md">${esc(m.model||"")}</span>
      <div class="ct"><b>${mc.done}</b><span>${esc(t("slashDone",mc.all))}</span><span class="sp"></span><span class="ip">${mc.progress?esc(t("nInProgress",mc.progress)):""}</span></div>
      ${stackBar(mc)}</div>`}).join("")}
    <button class="mc add" id="addm">${esc(t("addMachine"))}</button></div>`;
  box.querySelectorAll("[data-m]").forEach(cd=>{cd.onclick=e=>{if(e.target.closest("[data-edit]"))return;go("#m-"+cd.dataset.m)};cd.onkeydown=e=>{if(e.key==="Enter")go("#m-"+cd.dataset.m)}});
  box.querySelectorAll("[data-edit]").forEach(b=>b.onclick=()=>machineDialog(M(b.dataset.edit)));
  $("#addm").onclick=()=>machineDialog();
}

/* ---------- machine: its articles ---------- */
let machQ="";
function renderMachine(m){
  $("#view").innerHTML=`<div class="page">
    <div class="ph"><div><h2>${esc(m.name)}<b>.</b></h2><div class="sub">${esc(m.model||"")}${m.model?" · ":""}<span id="mcount"></span></div></div><span class="sp"></span>
      <div class="search">${searchIcon}<input id="q" type="search" placeholder="${esc(t("machSearch"))}" value="${esc(machQ)}" autocomplete="off"></div>
      <button class="btn red" id="newa">${esc(t("newArticle"))}</button></div>
    <div id="mres"></div>
  </div>`;
  $("#newa").onclick=()=>newArticle(m);
  const q=$("#q");q.oninput=()=>{machQ=q.value;drawMachine(m)};drawMachine(m);
}
function drawMachine(m){
  const all=artsOf(m.id),c=counts(all);$("#mcount").textContent=t("mCount",c.all,c.done);
  const box=$("#mres"),redraw=()=>drawMachine(m);
  if(!all.length){box.innerHTML=`<div class="empty"><h3>${esc(t("noArticlesOn",m.name))}</h3><p>${esc(t("noArticlesP"))}</p><button class="btn red" id="newa2">${esc(t("newArticle"))}</button></div>`;$("#newa2").onclick=()=>newArticle(m);return}
  if(!machQ.trim()){const sorted=all.slice().sort((x,y)=>String(x.article.number||"").localeCompare(String(y.article.number||""),undefined,{numeric:true}));const list=applyFilter(sorted);
    box.innerHTML=`<div class="resbar">${stackBar(c)}<span class="sp"></span>${filterChips(all)}</div>`+(list.length?articleTable(list,false):`<div class="empty"><h3>${esc(t("nothingFilter"))}</h3></div>`)}
  else box.innerHTML=resultBlock(searchArticles(all,machQ),false,esc(t("noMatchOn",m.name)));
  wireChips(box,redraw);wireArticleTable(box);
}
function articleTable(list,showMachine,cq){
  return `<div class="list"><table class="lt"><thead><tr><th>${t("thArticle")}</th><th>${t("thIndex")}</th><th>${t("thDes")}</th><th>${t("thProg")}</th>${showMachine?`<th>${t("thMachine")}</th>`:""}<th>${cq?t("thUses"):t("thTools")}</th><th style="min-width:230px">${t("thStatus")}</th><th>${t("thUpdated")}</th><th></th></tr></thead><tbody>
  ${list.map(a=>{const ar=a.article||{};return `<tr class="row" data-a="${a.id}">
    <td><span class="an ${ar.number?"":"none"}">${esc(ar.number||t("noNumber"))}</span></td>
    <td>${ar.index?`<span class="ix">${triIcon}<b>${esc(ar.index)}</b></span>`:`<span class="dim">—</span>`}</td>
    <td>${esc(ar.designation||"")}</td><td class="m">${esc(ar.program||"")}</td>
    ${showMachine?`<td><span class="mtag">${esc(M(a.machineId)?.name||"?")}</span></td>`:""}
    ${cq?`<td>${usesCell(a,cq.code,cq.exact)}</td>`:`<td class="m"><b>${realTools(a.tools).length}</b></td>`}
    <td>${statusCell(a)}</td><td class="dim">${when(a.updatedAt)}</td>
    <td><div class="acts"><button class="btn sm" data-pdf="${a.id}" title="${esc(t("pdfT"))}">PDF</button><button class="btn sm ghost" data-dup="${a.id}" title="${esc(t("copyT"))}">${esc(t("copy"))}</button><button class="btn sm danger" data-del="${a.id}">${esc(t("del"))}</button></div></td></tr>`}).join("")}
  </tbody></table></div>`;
}
function wireArticleTable(box){
  box.querySelectorAll("tr[data-a]").forEach(tr=>tr.onclick=e=>{if(e.target.closest("button"))return;go("#a-"+tr.dataset.a)});
  box.querySelectorAll("[data-pdf]").forEach(b=>b.onclick=()=>downloadPDF(A(b.dataset.pdf)));
  box.querySelectorAll("[data-dup]").forEach(b=>b.onclick=()=>copyDialog(A(b.dataset.dup)));
  box.querySelectorAll("[data-del]").forEach(b=>b.onclick=()=>arm(b,()=>{const a=A(b.dataset.del);db.articles=db.articles.filter(x=>x!==a);saveDB();toast(t("deleted",a.article.number||t("articleWord")));render()},t("confirm")));
}
function newArticle(m){
  const art={id:uid(),machineId:m.id,article:{date:today()},tools:[{t:"T01"}],status:"progress",createdAt:Date.now(),updatedAt:Date.now(),fresh:true};
  db.articles.push(art);saveDB();go("#a-"+art.id);
}

/* ---------- dialogs ---------- */
function dialog(title,body,foot){const ov=$("#ov");ov.innerHTML=`<div class="dlg" role="dialog" aria-modal="true"><header><h3>${title}</h3></header><div class="bd">${body}</div><div class="ft">${foot}</div></div>`;ov.hidden=false;
  setTimeout(()=>ov.querySelector("input,select")?.focus(),0);return ov}
function closeDlg(){const ov=$("#ov");if(ov.dataset.lock)return;ov.hidden=true;ov.innerHTML=""}
$("#ov").addEventListener("mousedown",e=>{if(e.target.id==="ov")closeDlg()});
document.addEventListener("keydown",e=>{if(e.key==="Escape"&&!$("#ov").hidden)closeDlg()});
function machineDialog(m){
  const ov=dialog(esc(m?t("editMachine"):t("addMachineT")),`
    <label class="f">${esc(t("machineName"))}<input id="d-name" value="${esc(m?.name||"")}" placeholder="Haas VF-2 · CNC 04"></label>
    <label class="f">${esc(t("machineModel"))}<input id="d-model" value="${esc(m?.model||"")}" placeholder="${esc(t("modelPh"))}"></label>
    <p class="err" id="d-err" hidden></p>`,
    `${m?`<button class="btn danger" id="d-del">${esc(t("delMachine"))}</button><span class="sp"></span>`:""}<button class="btn ghost" id="d-cancel">${esc(t("cancel"))}</button><button class="btn red" id="d-ok">${esc(m?t("save"):t("addMachineT"))}</button>`);
  const ok=()=>{const name=$("#d-name").value.trim();if(!name){$("#d-err").textContent=t("needName");$("#d-err").hidden=false;return}
    if(db.machines.some(x=>x!==m&&x.name.toLowerCase()===name.toLowerCase())){$("#d-err").textContent=t("nameTaken");$("#d-err").hidden=false;return}
    if(m){m.name=name;m.model=$("#d-model").value.trim()}else db.machines.push({id:uid(),name,model:$("#d-model").value.trim(),createdAt:Date.now()});
    saveDB();closeDlg();render();toast(m?t("machineSaved"):t("machineAdded",name))};
  $("#d-ok").onclick=ok;ov.querySelectorAll("input").forEach(i=>i.onkeydown=e=>{if(e.key==="Enter")ok()});
  $("#d-cancel").onclick=closeDlg;
  if(m){const n=artsOf(m.id).length;$("#d-del").onclick=e=>arm(e.currentTarget,()=>{db.articles=db.articles.filter(a=>a.machineId!==m.id);db.machines=db.machines.filter(x=>x!==m);saveDB();closeDlg();go("#");toast(t("machineDeleted",m.name))},n?t("delWith",n):t("clickDel"))}
}
function copyDialog(src){
  dialog(esc(t("copyTitle")),`
    <p class="note" style="margin:0">${esc(t("copyP"))}</p>
    <label class="f">${esc(t("copyOn"))}<select id="d-m">${db.machines.map(m=>`<option value="${m.id}" ${m.id===src.machineId?"selected":""}>${esc(m.name)}</option>`).join("")}</select></label>
    <div class="grid"><label class="f c4">${esc(t("articleNumber"))}<input id="d-num" class="big" value="${esc(src.article.number||"")}"></label><label class="f c2">${esc(t("index"))}<input id="d-ix" class="big" value="${esc(src.article.index||"")}"></label></div>`,
    `<button class="btn ghost" id="d-cancel">${esc(t("cancel"))}</button><button class="btn red" id="d-ok">${esc(t("makeCopy"))}</button>`);
  $("#d-cancel").onclick=closeDlg;
  $("#d-ok").onclick=()=>{const art={id:uid(),machineId:$("#d-m").value,article:{...src.article,number:$("#d-num").value.trim(),index:$("#d-ix").value.trim(),date:today()},tools:JSON.parse(JSON.stringify(src.tools)),status:"progress",createdAt:Date.now(),updatedAt:Date.now()};
    db.articles.push(art);saveDB();closeDlg();go("#a-"+art.id);toast(t("copyMade"))};
}

/* ---------- editor (the tool list maker) ---------- */
let cur=null, edTimer=null, pvTimer=null;
let pvOn=lsGet(PVKEY)!=="off";
function rowHTML(x,i){
  const v=k=>esc(x[k]??"");
  return `<tr data-i="${i}">
    <td><input class="m b up" data-k="t" value="${v("t")}" placeholder="T${String(i+1).padStart(2,"0")}"></td>
    <td><input class="up b" data-k="type" value="${v("type")}" list="types" placeholder="${esc(t("typePh"))}"></td>
    <td><input class="m" data-k="diameter" value="${v("diameter")}" placeholder="Ø12"></td>
    <td><input class="m" data-k="ra" value="${v("ra")}" placeholder="R2"></td>
    <td><input class="m b" data-k="ls" value="${v("ls")}" placeholder="50"></td>
    <td><input class="m" data-k="z" value="${v("z")}" placeholder="4"></td>
    <td><input class="up" data-k="holder" value="${v("holder")}" list="holders" placeholder="ER32"></td>
    <td class="codecell"><input class="m b up" data-k="code" value="${v("code")}" placeholder="F241" list="codes">${stockDot(x.code)}</td>
    <td class="act"><button class="ib" data-r="up" title="${esc(t("up"))}" tabindex="-1">↑</button><button class="ib" data-r="down" title="${esc(t("down"))}" tabindex="-1">↓</button><button class="ib x" data-r="del" title="${esc(t("remove"))}" tabindex="-1">✕</button></td></tr>`;
}
function renderEditor(art){
  cur=art;const a=art.article,m=M(art.machineId);
  $("#view").innerHTML=`<div class="ed ${pvOn?"":"nopv"}" id="ed">
  <section class="form">
    <div class="card">
      <h2>${esc(t("article"))} <span class="hint">${esc(t("autoSaved"))}</span></h2>
      <div class="status-box" id="stbox"></div>
      <div class="grid">
        <label class="f c4">${esc(t("articleNumber"))}<input id="a-number" class="big" placeholder="12345-678" autocomplete="off"></label>
        <label class="f c2">${esc(t("index"))}<input id="a-index" class="big" placeholder="C" autocomplete="off"></label>
        <p class="warnline c6" id="dupwarn" hidden></p>
        <label class="f c6">${esc(t("designation"))}<input id="a-designation" placeholder="${esc(t("desPh"))}"></label>
        <label class="f c2">${esc(t("program"))}<input id="a-program" placeholder="O1234"></label>
        <label class="f c2">${esc(t("machine"))}<select id="a-machine">${db.machines.map(x=>`<option value="${x.id}" ${x.id===m.id?"selected":""}>${esc(x.name)}</option>`).join("")}</select></label>
        <label class="f c2">${esc(t("material"))}<input id="a-material" placeholder="AL 7075-T7351"></label>
      </div>
    </div>
    <div class="card">
      <h2>${esc(t("tools"))} <span class="hint" id="count"></span></h2>
      <div class="tw"><table class="tt">
        <thead><tr><th style="width:62px">${esc(t("colTool"))}</th><th style="min-width:170px">${esc(t("colType"))}</th><th style="width:74px">Ø</th><th style="width:74px">R / ∠</th><th style="width:62px">LS</th><th style="width:48px">Z</th><th style="width:130px">${esc(t("colHolder"))}</th><th style="width:104px">${esc(t("colCode"))}</th><th></th></tr></thead>
        <tbody id="rows"></tbody></table></div>
      <div class="rowbar"><button class="btn" id="b-add">${esc(t("addTool"))}</button><button class="btn ghost" id="b-prep" title="${esc(t("prepT"))}">${esc(t("prep"))}</button><span class="note">${t("excelNote")}</span></div>
    </div>
    <div class="card">
      <h2>${esc(t("notesSign"))}</h2>
      <div class="grid">
        <label class="f c6">${esc(t("notes"))}<textarea id="a-notes" placeholder="${esc(t("notesPh"))}"></textarea></label>
        <label class="f c2">${esc(t("preparedBy"))}<input id="a-preparedBy"></label>
        <label class="f c2">${esc(t("approvedBy"))}<input id="a-approvedBy"></label>
        <label class="f c2">${esc(t("date"))}<input id="a-date" class="m" placeholder="${esc(t("datePh"))}"></label>
      </div>
      <span class="note">${esc(t("signNote"))}</span>
    </div>
  </section>
  <section class="pv" id="pvsec"><div class="pvbar"><span>${esc(t("preview"))}</span><span id="pvinfo">A4</span></div><div class="pvpages" id="pvpages"></div></section></div>`;
  AFIELDS.forEach(k=>{const el=$("#a-"+k);el.value=a[k]??"";el.addEventListener("input",()=>{cur.article[k]=el.value;edited();if(REQ_ART.includes(k))drawStatus();if(k==="number"||k==="index"){checkDup();$("#crumbs span:last-child").textContent=cur.article.number||t("newArticleCrumb")}})});
  $("#a-machine").onchange=e=>{cur.machineId=e.target.value;edited();const mm=M(cur.machineId);$("#crumbs a").textContent=mm.name;$("#crumbs a").dataset.go="#m-"+mm.id;checkDup();toast(t("movedTo",mm.name))};
  renderRows();checkDup();
  const rows=$("#rows");
  rows.addEventListener("input",e=>{const tr=e.target.closest("tr"),k=e.target.dataset.k;if(!tr||!k)return;cur.tools[+tr.dataset.i][k]=e.target.value;countTools();edited();
    if(k==="code")tr.querySelector(".sdot").outerHTML=stockDot(e.target.value)});
  rows.addEventListener("change",e=>{const tr=e.target.closest("tr");if(!tr||e.target.dataset.k!=="code")return;const i=+tr.dataset.i;
    if(fillFromCrib(i)){renderRows();edited();toast(t("filled",normCode(cur.tools[i].code)))}});
  rows.addEventListener("click",e=>{const b=e.target.closest("[data-r]");if(!b)return;const i=+b.closest("tr").dataset.i,T=cur.tools;
    if(b.dataset.r==="del"){T.splice(i,1);if(!T.length)T.push({t:"T01"})}
    if(b.dataset.r==="up"&&i>0)[T[i-1],T[i]]=[T[i],T[i-1]];
    if(b.dataset.r==="down"&&i<T.length-1)[T[i+1],T[i]]=[T[i],T[i+1]];
    renderRows();edited()});
  rows.addEventListener("keydown",e=>{if(e.key!=="Enter")return;const tr=e.target.closest("tr");if(!tr)return;e.preventDefault();const i=+tr.dataset.i,k=e.target.dataset.k;
    if(i===cur.tools.length-1)addRow();else{const el=$(`#rows tr[data-i="${i+1}"] input[data-k="${k}"]`);el?.focus();el?.select()}});
  rows.addEventListener("paste",e=>{
    const text=(e.clipboardData||window.clipboardData)?.getData("text")||"";if(!/[\t\n]/.test(text.trim()))return;
    e.preventDefault();const tr=e.target.closest("tr");const r0=+tr.dataset.i,c0=COLS.indexOf(e.target.dataset.k);
    let lines=text.replace(/\r/g,"").split("\n").filter(l=>l.trim()!=="").map(l=>l.split("\t"));
    if(lines.length&&/type|diam|holder|porte|outil|t\s*number|reference|référence/i.test(lines[0].join(" ")))lines.shift();
    lines.forEach((cells,ri)=>{const idx=r0+ri;if(!cur.tools[idx])cur.tools[idx]={};cells.forEach((v,ci)=>{const k=COLS[c0+ci];if(k)cur.tools[idx][k]=v.trim()})});
    renderRows();edited();toast(t("pasted",lines.length))});
  $("#b-add").onclick=()=>addRow();
  $("#b-prep").onclick=()=>{flushEditor();prepDialog(cur)};
  $("#codes").innerHTML=(db.catalog||[]).map(c=>`<option value="${esc(c.code)}">${esc([c.type,c.diameter?"Ø"+c.diameter:""].filter(Boolean).join(" "))}</option>`).join("");
  pvSetup();
  if(art.fresh){delete art.fresh;$("#a-number").focus()}
}
function countTools(){$("#count").textContent=t("nTools",realTools(cur.tools).length);markMissing();drawStatus()}
function markMissing(){document.querySelectorAll("#rows tr").forEach(tr=>{const x=cur.tools[+tr.dataset.i];const real=x&&COLS.some(k=>k!=="t"&&clean(x[k]));
  REQ_TOOL.forEach(k=>tr.querySelector(`[data-k="${k}"]`)?.classList.toggle("miss",!!real&&!clean(x[k])))})}
function drawStatus(){const box=$("#stbox");if(!box)return;const done=cur.status==="done",miss=missing(cur);
  box.classList.toggle("is-done",done);
  box.innerHTML=`<div class="seg" role="group"><button data-s="progress" aria-pressed="${!done}">${esc(t("inProgress"))}</button><button class="done" data-s="done" aria-pressed="${done}">${esc(t("markDone"))}</button></div>
    ${statusCell({...cur,status:done?"done":cur.status})}<span class="miss-n">${esc(miss?t("stillEmpty",miss):t("allFilled"))}</span>`;
  box.querySelectorAll("[data-s]").forEach(b=>b.onclick=()=>{const was=cur.status;cur.status=b.dataset.s;if(was!==cur.status){edited();drawStatus();
    if(cur.status==="done")toast(miss?t("markedDoneMiss",miss):t("markedDone"))}})}
function renderRows(focus){$("#rows").innerHTML=cur.tools.map(rowHTML).join("");countTools();
  if(focus){const el=$(`#rows tr[data-i="${focus[0]}"] input[data-k="${focus[1]}"]`);el?.focus()}}
function nextT(){const nums=cur.tools.map(x=>parseInt(String(x.t).replace(/\D/g,""))).filter(Boolean);return "T"+String((nums.length?Math.max(...nums):0)+1).padStart(2,"0")}
function addRow(){cur.tools.push({t:nextT()});renderRows([cur.tools.length-1,"type"]);edited()}
function checkDup(){const n=clean(cur.article.number).toLowerCase(),ix=clean(cur.article.index).toLowerCase(),w=$("#dupwarn");
  const d=n&&db.articles.find(x=>x!==cur&&x.machineId===cur.machineId&&clean(x.article.number).toLowerCase()===n&&clean(x.article.index).toLowerCase()===ix);
  w.hidden=!d;if(d)w.textContent=t("dup",cur.article.number,cur.article.index,M(cur.machineId).name)}
function edited(){cur.updatedAt=Date.now();clearTimeout(edTimer);edTimer=setTimeout(flushEditor,400);schedulePreview()}
function flushEditor(){edTimer=null;saveDB()}

/* ---------- live preview: drawn off-screen, swapped in when ready (no flicker) ---------- */
let pvGen=0, pvBusy=false, pvAgain=false, pvRO=null, pvLastKey="", pvLastW=0;
function schedulePreview(delay=350){if(!pvOn)return;clearTimeout(pvTimer);pvTimer=setTimeout(preview,delay)}
function pvSetup(){
  const host=$("#pvpages");if(!host)return;
  pvLastKey="";pvLastW=0;
  if(pvRO)pvRO.disconnect();
  pvRO=new ResizeObserver(()=>{if(pvOn&&Math.abs(host.clientWidth-pvLastW)>4)schedulePreview(200)});pvRO.observe(host);
  if(pvOn)preview();
}
function pvTeardown(){if(pvRO){pvRO.disconnect();pvRO=null}clearTimeout(pvTimer);pvGen++}
function togglePreview(){
  pvOn=!pvOn;lsSet(PVKEY,pvOn?"on":"off");
  $("#b-pv")?.setAttribute("aria-pressed",pvOn);$("#ed")?.classList.toggle("nopv",!pvOn);
  if(pvOn){pvLastKey="";schedulePreview(30)}
}
async function preview(){
  const host=$("#pvpages");if(!cur||!host||!pvOn)return;
  if(pvBusy){pvAgain=true;return}
  const W=Math.floor(host.clientWidth-28);if(W<120)return;
  const key=JSON.stringify([sheetData(cur),LANG,!!logo,logo?.data?.length]);
  if(key===pvLastKey&&Math.abs(W-pvLastW)<=4)return;
  pvBusy=true;const gen=++pvGen;
  try{
    const doc=makePDF(sheetData(cur));const data=new Uint8Array(doc.output("arraybuffer"));
    const pdf=await pdfjsLib.getDocument({data,isEvalSupported:false,disableFontFace:false}).promise;
    const dpr=Math.min(window.devicePixelRatio||1,2),out=[];
    for(let i=1;i<=pdf.numPages;i++){
      const page=await pdf.getPage(i);const vp1=page.getViewport({scale:1});const vp=page.getViewport({scale:W/vp1.width*dpr});
      const c=document.createElement("canvas");c.width=Math.round(vp.width);c.height=Math.round(vp.height);c.style.width=W+"px";c.style.height=Math.round(vp.height/dpr)+"px";
      await page.render({canvasContext:c.getContext("2d",{alpha:false}),viewport:vp}).promise;out.push(c);
      if(gen!==pvGen)break;
    }
    if(gen===pvGen&&host.isConnected){const st=host.scrollTop;host.replaceChildren(...out);host.scrollTop=st;pvLastKey=key;pvLastW=W;
      $("#pvinfo").textContent=t("pages",pdf.numPages)}
    pdf.destroy();
  }catch(e){const i=$("#pvinfo");if(i)i.textContent=t("pvError")+(e.message||e);console.error(e)}
  finally{pvBusy=false;if(pvAgain){pvAgain=false;schedulePreview(60)}}
}

/* ---------- tool crib (F / M codes, details, stock) ---------- */
Object.assign(I18N.en,{
  navMachines:"Machines", navCrib:"Tool crib",
  crib:"Tool crib", cribSub:"Every tool code (F / M) with its details, where it's used, and what's on the shelf.", cribSearch:"Find a code, type or diameter…",
  newCode:"+ New code", orderList:"Order list (CSV)", orderListT:"Download the codes at or below their minimum, to order",
  tCodes:"codes in the crib", tLow:"low stock", tOut:"out of stock", tMissing:"used in articles, no card yet",
  fAll:"All", fLow:"Low stock", fOut:"Out of stock", fMissing:"No card yet",
  cCode:"Code", cType:"Type", cLoc:"Location", cUsed:"Used in", cStock:"Stock", cMin:"Min",
  nArticles:n=>`${n} ${pl(n,"article","articles")}`,
  missingP:"These codes are used in your articles but have no card in the tool crib yet. Adding them copies type, Ø, R / ∠ and Z from the articles.",
  add:"Add", addAll:n=>`Add all ${n}`, codesAdded:n=>`${n} ${pl(n,"code","codes")} added to the tool crib`,
  cribEmpty:"No tool codes yet", cribEmptyP:"Add codes one by one, or bring in every code already used in your articles in one click.", importArticles:"Add codes from articles", noCodeMatch:"No code matches",
  diameter:"Diameter Ø", flutes:"Flutes / inserts (Z)", cutLength:"Cut length", oal:"Overall length", holder:"Holder", defLS:"Usual LS", ref:"Brand & reference", supplier:"Supplier", grade:"Grade / coating", location:"Location (shelf / drawer)",
  details:"Details", inStock:"In stock", sOk:"OK", sLow:"Low", sOut:"Out", minimum:"Minimum", setCount:"Correct the count", setBtn:"Set",
  history:"Stock history", noMoves:"No stock movements yet.", usedIn:"Used in", notUsed:"Not used in any article yet.", delCode:"Delete code",
  codeTaken:"This code already exists.", needCode:"Enter a code, e.g. F241.", newCodeT:"New tool code", create:"Create", codeDeleted:c=>`${c} deleted`,
  hTake:"Taken", hAdd:"Added", hSet:"Count corrected", hPrep:a=>`Taken for article ${a}`,
  prep:"Tool prep", prepT:"Check stock for this article's tools and take them from the shelf", prepTitle:a=>`Tool prep · ${a}`,
  prepP:"What tool prep needs for this article, with stock and location.", notInCrib:"No card in the crib", takeAll:"Take from stock (−1 each)", taken:n=>`Stock updated: ${n} ${pl(n,"tool","tools")} taken`, close:"Close",
  stockTip:(s,n)=>({ok:`In stock: ${n}`,low:`Low stock: ${n}`,out:"Out of stock",new:"Not counted yet",none:"Not in the tool crib"}[s]),sNew:"Not counted",
  filled:c=>`Filled from the tool crib (${c})`, noOrder:"No code is at or below its minimum.", orderPrefix:"OrderList", toOrder:"To order", openCard:"Open card",
  csvHead:["Code","Type","Ø","R / ∠","Z","Brand & reference","Supplier","Location","Stock","Minimum","To order"]
});
Object.assign(I18N.fr,{
  navMachines:"Machines", navCrib:"Magasin outils",
  crib:"Magasin outils", cribSub:"Chaque code outil (F / M) avec ses caractéristiques, où il est utilisé et ce qu'il y a en stock.", cribSearch:"Chercher un code, un type ou un diamètre…",
  newCode:"+ Nouveau code", orderList:"Liste de commande (CSV)", orderListT:"Télécharger les codes à leur minimum ou en dessous, pour commander",
  tCodes:"codes au magasin", tLow:"stock bas", tOut:"en rupture", tMissing:"utilisés dans des articles, sans fiche",
  fAll:"Tous", fLow:"Stock bas", fOut:"Rupture", fMissing:"Sans fiche",
  cCode:"Code", cType:"Type", cLoc:"Emplacement", cUsed:"Utilisé dans", cStock:"Stock", cMin:"Min",
  nArticles:n=>`${n} ${pl(n,"article","articles")}`,
  missingP:"Ces codes sont utilisés dans vos articles mais n'ont pas encore de fiche au magasin. Les ajouter recopie le type, Ø, R / ∠ et Z depuis les articles.",
  add:"Ajouter", addAll:n=>`Tout ajouter (${n})`, codesAdded:n=>`${n} ${pl(n,"code ajouté","codes ajoutés")} au magasin`,
  cribEmpty:"Aucun code outil pour l'instant", cribEmptyP:"Ajoutez les codes un par un, ou importez en un clic tous les codes déjà utilisés dans vos articles.", importArticles:"Importer les codes des articles", noCodeMatch:"Aucun code ne correspond",
  diameter:"Diamètre Ø", flutes:"Dents / plaquettes (Z)", cutLength:"Longueur de coupe", oal:"Longueur totale", holder:"Porte-outil", defLS:"LS habituelle", ref:"Marque et référence", supplier:"Fournisseur", grade:"Nuance / revêtement", location:"Emplacement (étagère / tiroir)",
  details:"Caractéristiques", inStock:"En stock", sOk:"OK", sLow:"Bas", sOut:"Rupture", minimum:"Minimum", setCount:"Corriger le stock", setBtn:"Valider",
  history:"Historique du stock", noMoves:"Aucun mouvement de stock pour l'instant.", usedIn:"Utilisé dans", notUsed:"Utilisé dans aucun article pour l'instant.", delCode:"Supprimer le code",
  codeTaken:"Ce code existe déjà.", needCode:"Entrez un code, ex. F241.", newCodeT:"Nouveau code outil", create:"Créer", codeDeleted:c=>`${c} supprimé`,
  hTake:"Sortie", hAdd:"Entrée", hSet:"Stock corrigé", hPrep:a=>`Sorti pour l'article ${a}`,
  prep:"Préparation", prepT:"Vérifier le stock des outils de cet article et les sortir du magasin", prepTitle:a=>`Préparation des outils · ${a}`,
  prepP:"Ce que la préparation doit sortir pour cet article, avec le stock et l'emplacement.", notInCrib:"Pas de fiche au magasin", takeAll:"Sortir du stock (−1 chacun)", taken:n=>`Stock mis à jour : ${n} ${pl(n,"outil sorti","outils sortis")}`, close:"Fermer",
  stockTip:(s,n)=>({ok:`En stock : ${n}`,low:`Stock bas : ${n}`,out:"En rupture",new:"Pas encore compté",none:"Absent du magasin"}[s]),sNew:"Non compté",
  filled:c=>`Rempli depuis le magasin (${c})`, noOrder:"Aucun code n'est à son minimum ou en dessous.", orderPrefix:"ListeCommande", toOrder:"À commander", openCard:"Ouvrir la fiche",
  csvHead:["Code","Type","Ø","R / ∠","Z","Marque et référence","Fournisseur","Emplacement","Stock","Minimum","À commander"]
});

const CFIELDS=["type","diameter","ra","z","cutLength","oal","ls","ref","supplier","grade","location","notes"];
const normCode=c=>String(c||"").trim().toUpperCase().replace(/\s+/g,"");
const C_=code=>(db.catalog||[]).find(c=>c.code===normCode(code));
const stockState=c=>{if(!c)return"none";const s=+c.stock||0,m=+c.min||0;if(!s&&!m&&!(c.history||[]).length)return"new";return s<=0?"out":(m>0&&s<=m)?"low":"ok"};
const SSL=s=>({ok:t("sOk"),low:t("sLow"),out:t("sOut"),new:t("sNew"),none:"—"}[s]);
function usesOf(code){const k=normCode(code),out=[];db.articles.forEach(a=>a.tools.forEach(x=>{if(normCode(x.code)===k)out.push({a,x})}));return out}
function allUsedCodes(){const m=new Map();db.articles.forEach(a=>a.tools.forEach(x=>{const k=normCode(x.code);if(!k)return;if(!m.has(k))m.set(k,[]);m.get(k).push({a,x})}));return m}
// most common non-empty value among the articles using a code
function guessFrom(uses){const pick=k=>{const n={};uses.forEach(u=>{const v=clean(u.x[k]);if(v)n[v]=(n[v]||0)+1});return Object.entries(n).sort((p,q)=>q[1]-p[1])[0]?.[0]||""};
  return{type:pick("type").toUpperCase(),diameter:normDia(pick("diameter")),ra:pick("ra"),z:pick("z"),ls:pick("ls")}}
function newCard(code,from){return{code:normCode(code),...Object.fromEntries(CFIELDS.map(k=>[k,""])),...(from||{}),stock:0,min:0,history:[],createdAt:Date.now(),updatedAt:Date.now()}}
function moveStock(c,delta,note){c.stock=Math.max(0,(+c.stock||0)+delta);c.history=[{ts:Date.now(),d:delta,note:note||""},...(c.history||[])].slice(0,60);c.updatedAt=Date.now()}
function stockDot(code){const c=C_(code),s=stockState(c);return `<span class="sdot s-${s}" title="${esc(t("stockTip",s,c?+c.stock||0:0))}"></span>`}

/* list page */
let cribQ="", cribF="all";
function renderCrib(){
  $("#view").innerHTML=`<div class="page">
    <div class="ph"><div><h2>${esc(t("crib"))}<b>.</b></h2><div class="sub">${esc(t("cribSub"))}</div></div><span class="sp"></span>
      <div class="search">${searchIcon}<input id="q" type="search" placeholder="${esc(t("cribSearch"))}" value="${esc(cribQ)}" autocomplete="off"></div>
      <button class="btn" id="b-order" title="${esc(t("orderListT"))}">${esc(t("orderList"))}</button>
      <button class="btn red" id="b-newcode">${esc(t("newCode"))}</button></div>
    <div id="cres"></div></div>`;
  $("#b-newcode").onclick=()=>newCodeDialog();$("#b-order").onclick=orderCSV;
  const q=$("#q");q.oninput=()=>{cribQ=q.value;drawCrib()};drawCrib();
  if(cribQ){q.focus();q.setSelectionRange(q.value.length,q.value.length)}
}
function drawCrib(){
  const box=$("#cres"),cat=db.catalog||[],used=allUsedCodes();
  const missing=[...used.keys()].filter(k=>!C_(k)).sort((p,q)=>p.localeCompare(q,undefined,{numeric:true}));
  const n={all:cat.length,low:cat.filter(c=>stockState(c)==="low").length,out:cat.filter(c=>stockState(c)==="out").length,missing:missing.length};
  if(!cat.length&&!missing.length){box.innerHTML=`<div class="empty"><h3>${esc(t("cribEmpty"))}</h3><p>${esc(t("cribEmptyP"))}</p><button class="btn red" id="nc2">${esc(t("newCode"))}</button></div>`;$("#nc2").onclick=()=>newCodeDialog();return}
  const tiles=`<section class="tiles4">
    <button class="tile4" data-cf="all"><b>${n.all}</b><span>${esc(t("tCodes"))}</span></button>
    <button class="tile4 t-low" data-cf="low"><b>${n.low}</b><span>${esc(t("tLow"))}</span></button>
    <button class="tile4 t-out" data-cf="out"><b>${n.out}</b><span>${esc(t("tOut"))}</span></button>
    <button class="tile4 t-miss" data-cf="missing"><b>${n.missing}</b><span>${esc(t("tMissing"))}</span></button></section>`;
  const chips=`<div class="chips">${[["all",t("fAll")],["low",t("fLow")],["out",t("fOut")],["missing",t("fMissing")]].map(([k,l])=>`<button class="chip c-${k}" data-cf="${k}" aria-pressed="${cribF===k}">${esc(l)}<b>${n[k]}</b></button>`).join("")}</div>`;
  const q=cribQ.trim().toLowerCase().replace(/^ø/,""),terms=q.split(/\s+/).filter(Boolean);
  const match=(...vals)=>{const hay=vals.join(" ").toLowerCase();return terms.every(w=>hay.includes(w))};
  let body;
  if(cribF==="missing"){
    const list=missing.filter(k=>match(k,...used.get(k).map(u=>u.x.type)));
    body=list.length?`<p class="note" style="margin:0">${esc(t("missingP"))}</p>
      <div class="list"><table class="lt"><thead><tr><th>${t("cCode")}</th><th>${t("cType")}</th><th>Ø</th><th>R / ∠</th><th>Z</th><th>${t("cUsed")}</th><th><button class="btn sm red" id="addall">${esc(t("addAll",list.length))}</button></th></tr></thead><tbody>
      ${list.map(k=>{const g=guessFrom(used.get(k)),arts=new Set(used.get(k).map(u=>u.a.id)).size;return `<tr><td><span class="an">${esc(k)}</span></td><td>${esc(g.type)}</td><td class="m">${g.diameter?"Ø"+esc(g.diameter):""}</td><td class="m">${esc(g.ra)}</td><td class="m">${esc(g.z)}</td><td>${esc(t("nArticles",arts))}</td><td><button class="btn sm" data-addc="${esc(k)}">${esc(t("add"))}</button></td></tr>`}).join("")}</tbody></table></div>`
      :`<div class="empty"><h3>${esc(t("noCodeMatch"))}</h3></div>`;
  }else{
    const list=cat.filter(c=>(cribF==="all"||stockState(c)===cribF)&&match(c.code,c.type,c.diameter,"ø"+c.diameter,c.ref,c.location,c.supplier))
      .sort((p,q)=>p.code.localeCompare(q.code,undefined,{numeric:true}));
    body=list.length?`<div class="list"><table class="lt"><thead><tr><th>${t("cCode")}</th><th>${t("cType")}</th><th>Ø</th><th>R / ∠</th><th>Z</th><th>${t("cLoc")}</th><th>${t("cUsed")}</th><th style="min-width:200px">${t("cStock")}</th><th>${t("cMin")}</th></tr></thead><tbody>
      ${list.map(c=>{const s=stockState(c),ua=new Set(usesOf(c.code).map(u=>u.a.id)).size;return `<tr class="row" data-code="${esc(c.code)}">
        <td><span class="an">${esc(c.code)}</span></td><td><b class="tyc">${esc(c.type)}</b>${c.ref?`<div class="dim small">${esc(c.ref)}</div>`:""}</td>
        <td class="m">${c.diameter?"Ø"+esc(c.diameter):""}</td><td class="m">${esc(raLabel(c.ra))}</td><td class="m">${esc(c.z)}</td><td>${esc(c.location)}</td>
        <td>${ua?esc(t("nArticles",ua)):`<span class="dim">—</span>`}</td>
        <td><div class="stk"><div class="stepper"><button data-sd="-1" data-c="${esc(c.code)}" aria-label="−1">−</button><span>${+c.stock||0}</span><button data-sd="1" data-c="${esc(c.code)}" aria-label="+1">+</button></div><span class="spill s-${s}">${esc(SSL(s))}</span></div></td>
        <td class="m">${+c.min||0}</td></tr>`}).join("")}</tbody></table></div>`
      :`<div class="empty"><h3>${esc(t(cat.length?"noCodeMatch":"cribEmpty"))}</h3>${cat.length?"":`<p>${esc(t("cribEmptyP"))}</p>`}</div>`;
  }
  box.innerHTML=tiles+`<div class="resbar"><span class="sp"></span>${chips}</div>`+body;
  box.querySelectorAll("[data-cf]").forEach(b=>b.onclick=()=>{cribF=b.dataset.cf;drawCrib()});
  box.querySelectorAll("tr[data-code]").forEach(tr=>tr.onclick=e=>{if(e.target.closest("button"))return;go("#c-"+encodeURIComponent(tr.dataset.code))});
  box.querySelectorAll("[data-sd]").forEach(b=>b.onclick=()=>{const c=C_(b.dataset.c);moveStock(c,+b.dataset.sd,+b.dataset.sd>0?t("hAdd"):t("hTake"));saveDB();drawCrib()});
  const addCodes=ks=>{ks.forEach(k=>{if(!C_(k))db.catalog.push(newCard(k,guessFrom(used.get(k))))});saveDB();toast(t("codesAdded",ks.length));if(!missing.some(k=>!C_(k)))cribF="all";drawCrib()};
  box.querySelectorAll("[data-addc]").forEach(b=>b.onclick=()=>addCodes([b.dataset.addc]));
  $("#addall")&&($("#addall").onclick=()=>addCodes(missing.filter(k=>match(k,...used.get(k).map(u=>u.x.type)))));
}
const raLabel=v=>{const r=normRA(v);return r.kind==="R"?"R"+r.val:r.kind==="A"?r.val+"°":""};

/* code card page */
function renderCode(c){
  const uses=usesOf(c.code),s=stockState(c);
  const f=(k,label,cls="",ph="")=>`<label class="f ${cls}">${esc(label)}<input id="cf-${k}" data-cf="${k}" value="${esc(c[k]??"")}" placeholder="${esc(ph)}" ${k==="type"?`list="types" class="up"`:""}></label>`;
  $("#view").innerHTML=`<div class="page">
    <div class="ph"><div class="codehead"><span class="bigcode">${esc(c.code)}</span><div><div class="sub" style="margin:0">${esc(c.type||"")}${c.diameter?" · Ø"+esc(c.diameter):""}</div><div class="sub" style="margin:0">${esc(t("autoSaved"))}</div></div></div><span class="sp"></span>
      <button class="btn danger" id="b-delc">${esc(t("delCode"))}</button></div>
    <div class="cgrid">
      <div class="card"><h2>${esc(t("details"))}</h2>
        <div class="grid">
          <label class="f c2">${esc(t("cCode"))}<input id="cf-code" class="big up" value="${esc(c.code)}"></label>
          ${f("type",t("cType"),"c4",t("typePh"))}
          ${f("diameter",t("diameter"),"c2","12")}${f("ra","R / ∠","c2","R2 / 118°")}${f("z",t("flutes"),"c2","4")}
          ${f("cutLength",t("cutLength"),"c2","22")}${f("oal",t("oal"),"c2","72")}${f("ls",t("defLS"),"c2","50")}
          ${f("grade",t("grade"),"c6","AlTiN")}
          ${f("ref",t("ref"),"c3","")}${f("supplier",t("supplier"),"c3","")}
          <label class="f c6">${esc(t("notes"))}<textarea id="cf-notes" data-cf="notes">${esc(c.notes||"")}</textarea></label>
        </div><p class="err" id="cerr" hidden></p></div>
      <div class="side">
        <div class="card stockcard s-${s}" id="stockcard"></div>
        <div class="card"><h2>${esc(t("usedIn"))} <span class="hint">${esc(t("nArticles",new Set(uses.map(u=>u.a.id)).size))}</span></h2>
          ${uses.length?`<div class="uselist">${uses.map(u=>`<button class="useitem" data-go="#a-${u.a.id}"><span class="an">${esc(u.a.article.number||t("noNumber"))}</span>${u.a.article.index?`<span class="ix">${triIcon}<b>${esc(u.a.article.index)}</b></span>`:""}<span class="mtag">${esc(M(u.a.machineId)?.name||"?")}</span><span class="use"><b>${esc(normT(u.x.t))}</b>${esc(c.code)}</span>${clean(u.x.ls)?`<span class="dim m">LS ${esc(u.x.ls)}</span>`:""}</button>`).join("")}</div>`:`<p class="note" style="margin:0">${esc(t("notUsed"))}</p>`}
        </div>
      </div>
    </div></div>`;
  drawStockCard(c);
  $("#view").querySelectorAll("[data-cf]").forEach(el=>el.addEventListener("input",()=>{c[el.dataset.cf]=el.value;c.updatedAt=Date.now();saveDB()}));
  const ci=$("#cf-code");ci.addEventListener("change",()=>{const nc=normCode(ci.value),e=$("#cerr");
    if(!nc){e.textContent=t("needCode");e.hidden=false;ci.value=c.code;return}
    if(nc!==c.code&&C_(nc)){e.textContent=t("codeTaken");e.hidden=false;ci.value=c.code;return}
    e.hidden=true;if(nc!==c.code){db.articles.forEach(a=>a.tools.forEach(x=>{if(normCode(x.code)===c.code)x.code=nc}));c.code=nc;saveDB();history.replaceState(null,"","#c-"+encodeURIComponent(nc));render()}});
  $("#view").querySelectorAll("[data-go]").forEach(b=>b.onclick=()=>go(b.dataset.go));
  $("#b-delc").onclick=e=>arm(e.currentTarget,()=>{db.catalog=db.catalog.filter(x=>x!==c);saveDB();go("#crib");toast(t("codeDeleted",c.code))});
}
function drawStockCard(c){
  const box=$("#stockcard"),s=stockState(c);box.className=`card stockcard s-${s}`;
  box.innerHTML=`<h2>${esc(t("inStock"))} <span class="spill s-${s}">${esc(SSL(s))}</span></h2>
    <div class="bigstock"><button class="bs" data-mv="-1" aria-label="−1">−</button><b>${+c.stock||0}</b><button class="bs" data-mv="1" aria-label="+1">+</button></div>
    <div class="grid"><label class="f c3">${esc(t("minimum"))}<input id="cf-min" class="m" inputmode="numeric" value="${+c.min||0}"></label>
      <label class="f c3">${esc(t("location"))}<input id="cf-location" value="${esc(c.location||"")}" placeholder="A3"></label>
      <label class="f c6">${esc(t("setCount"))}<span class="inrow"><input id="cf-set" class="m" inputmode="numeric" placeholder="${+c.stock||0}"><button class="btn" id="b-set">${esc(t("setBtn"))}</button></span></label></div>
    <h2 style="margin-top:4px">${esc(t("history"))}</h2>
    ${(c.history||[]).length?`<ul class="hist">${c.history.slice(0,12).map(h=>`<li><b class="${h.d>0?"pos":h.d<0?"neg":""}">${h.d>0?"+"+h.d:h.d<0?"−"+(-h.d):"="+(h.set??"")}</b><span>${esc(h.note||"")}</span><span class="dim">${when(h.ts)}</span></li>`).join("")}</ul>`:`<p class="note" style="margin:0">${esc(t("noMoves"))}</p>`}`;
  box.querySelectorAll("[data-mv]").forEach(b=>b.onclick=()=>{moveStock(c,+b.dataset.mv,+b.dataset.mv>0?t("hAdd"):t("hTake"));saveDB();drawStockCard(c)});
  $("#cf-min").oninput=e=>{c.min=Math.max(0,parseInt(e.target.value)||0);saveDB();const ns=stockState(c);box.className=`card stockcard s-${ns}`;box.querySelector("h2 .spill").className=`spill s-${ns}`;box.querySelector("h2 .spill").textContent=SSL(ns)};
  $("#cf-location").oninput=e=>{c.location=e.target.value;saveDB()};
  const set=()=>{const v=parseInt($("#cf-set").value);if(isNaN(v)||v<0)return;const d=v-(+c.stock||0);c.stock=v;c.history=[{ts:Date.now(),d:0,set:v,note:t("hSet")+(d?` (${d>0?"+":""}${d})`:"")},...(c.history||[])].slice(0,60);saveDB();drawStockCard(c)};
  $("#b-set").onclick=set;$("#cf-set").onkeydown=e=>{if(e.key==="Enter")set()};
}
function newCodeDialog(){
  dialog(esc(t("newCodeT")),`<label class="f">${esc(t("cCode"))}<input id="d-code" class="big up" placeholder="F241" autocomplete="off"></label><p class="err" id="d-err" hidden></p>`,
    `<button class="btn ghost" id="d-cancel">${esc(t("cancel"))}</button><button class="btn red" id="d-ok">${esc(t("create"))}</button>`);
  const ok=()=>{const k=normCode($("#d-code").value),e=$("#d-err");if(!k){e.textContent=t("needCode");e.hidden=false;return}
    if(C_(k)){closeDlg();go("#c-"+encodeURIComponent(k));return}
    const u=usesOf(k);db.catalog.push(newCard(k,u.length?guessFrom(u):null));saveDB();closeDlg();go("#c-"+encodeURIComponent(k))};
  $("#d-ok").onclick=ok;$("#d-code").onkeydown=e=>{if(e.key==="Enter")ok()};$("#d-cancel").onclick=closeDlg;
}
async function orderCSV(){
  const list=(db.catalog||[]).filter(c=>["low","out"].includes(stockState(c))).sort((p,q)=>p.code.localeCompare(q.code,undefined,{numeric:true}));
  if(!list.length){toast(t("noOrder"));return}
  const q=v=>`"${String(v??"").replace(/"/g,'""')}"`;
  const rows=[t("csvHead"),...list.map(c=>[c.code,c.type,c.diameter,raLabel(c.ra),c.z,c.ref,c.supplier,c.location,+c.stock||0,+c.min||0,Math.max(1,(+c.min||0)+1-(+c.stock||0))])];
  const name=`${t("orderPrefix")}_${stampOf(new Date())}.csv`;
  try{const p=await download(name,new Blob(["﻿"+rows.map(r=>r.map(q).join(";")).join("\r\n")],{type:"text/csv"}),"csv");if(p)toast(DESK?t("saved",name):t("savedTo",name))}catch(e){toast(String(e.message||e))}
}

/* tool prep for one article */
function prepDialog(art){
  const rows=realTools(art.tools).filter(x=>clean(x.code));
  const need=new Map();rows.forEach(x=>{const k=normCode(x.code);need.set(k,(need.get(k)||0)+1)});
  dialog(esc(t("prepTitle",art.article.number||t("noNumber"))),`<p class="note" style="margin:0">${esc(t("prepP"))}</p>
    <div class="tw"><table class="lt prept"><thead><tr><th>${t("colTool")}</th><th>${t("cCode")}</th><th>${t("cType")}</th><th>Ø</th><th>LS</th><th>${t("cLoc")}</th><th>${t("cStock")}</th></tr></thead><tbody>
    ${rows.map(x=>{const c=C_(x.code),s=stockState(c);return `<tr><td class="m"><b>${esc(normT(x.t))}</b></td><td><button class="linkcode" data-go="#c-${encodeURIComponent(normCode(x.code))}" title="${esc(t("openCard"))}">${esc(normCode(x.code))}</button></td><td>${esc(clean(x.type).toUpperCase())}</td><td class="m">${normDia(x.diameter)?"Ø"+esc(normDia(x.diameter)):""}</td><td class="m"><b>${esc(clean(x.ls))}</b></td><td>${esc(c?.location||"")}</td><td>${c?`<span class="spill s-${s}">${+c.stock||0}</span>`:`<span class="spill s-none">${esc(t("notInCrib"))}</span>`}</td></tr>`}).join("")}
    </tbody></table></div>`,
    `<button class="btn ghost" id="d-cancel">${esc(t("close"))}</button><button class="btn red" id="d-take">${esc(t("takeAll"))}</button>`);
  $(".dlg").classList.add("wide");
  $("#d-cancel").onclick=closeDlg;
  $("#ov").querySelectorAll("[data-go]").forEach(b=>b.onclick=()=>{closeDlg();go(b.dataset.go)});
  $("#d-take").onclick=()=>{let n=0;need.forEach((q,k)=>{const c=C_(k);if(c){moveStock(c,-q,t("hPrep",art.article.number||""));n+=q}});saveDB();closeDlg();toast(t("taken",n));if(route.view==="article")renderRows()};
}

/* article editor hooks: stock dot next to each code, fill a new row from the crib */
function fillFromCrib(i){
  const x=cur.tools[i],c=C_(x.code);if(!c)return false;let did=false;
  [["type","type"],["diameter","diameter"],["ra","ra"],["z","z"],["ls","ls"]].forEach(([tk,ck])=>{if(!clean(x[tk])&&clean(c[ck])){x[tk]=c[ck];did=true}});
  return did;
}

/* ---------- top bar ---------- */
$("#home").onclick=()=>go("#");
$("#b-backup").onclick=()=>{if(edTimer){clearTimeout(edTimer);flushEditor()}
  const d=new Date();
  download(`${t("backupPrefix")}_${stampOf(d)}.json`,new Blob([JSON.stringify({app:"tool-list-maker",version:3,savedAt:d.toISOString(),machines:db.machines,articles:db.articles,catalog:db.catalog,logo},null,1)],{type:"application/json"}),"json")
    .then(p=>{if(!p)return;db.lastBackup=Date.now();saveDB();toast(DESK?t("backupDesk"):t("backupWeb"));if(route.view==="home")render()})
    .catch(e=>toast(t("backupFail")+(e.message||e)))};
$("#b-restore").onclick=()=>$("#f-restore").click();
$("#f-restore").onchange=async e=>{const f=e.target.files[0];e.target.value="";if(!f)return;
  try{const d=JSON.parse(await f.text());
    if(Array.isArray(d.machines)&&Array.isArray(d.articles)){
      dialog(esc(t("restoreTitle")),`<p style="margin:0">${t("restoreHas",d.machines.length,d.articles.length)}</p><p class="note" style="margin:0">${esc(t("restoreQ"))}</p>`,
        `<button class="btn ghost" id="d-cancel">${esc(t("cancel"))}</button><button class="btn" id="d-merge">${esc(t("addCurrent"))}</button><button class="btn red" id="d-rep">${esc(t("replaceAll"))}</button>`);
      $("#d-cancel").onclick=closeDlg;
      $("#d-rep").onclick=()=>{db={machines:d.machines,articles:d.articles,catalog:Array.isArray(d.catalog)?d.catalog:[],lastBackup:Date.now(),migrated:true};if(d.logo){logo=d.logo;lsSet(LOGOKEY,JSON.stringify(logo))}saveDB();closeDlg();go("#");toast(t("restored"))};
      $("#d-merge").onclick=()=>{const ids=new Set(db.machines.map(m=>m.id));d.machines.forEach(m=>{if(!ids.has(m.id))db.machines.push(m)});const aids=new Set(db.articles.map(a=>a.id));d.articles.forEach(a=>{if(!aids.has(a.id))db.articles.push(a)});ensureDB();(d.catalog||[]).forEach(c=>{if(!C_(c.code))db.catalog.push(c)});saveDB();closeDlg();render();toast(t("added"))};
    }else if(d.article&&Array.isArray(d.tools)){
      const name=clean(d.article.machine)||t("unassigned");let m=db.machines.find(x=>x.name.toLowerCase()===name.toLowerCase());if(!m){m={id:uid(),name,model:"",createdAt:Date.now()};db.machines.push(m)}
      const {machine,...art}=d.article;const a={id:uid(),machineId:m.id,article:art,tools:d.tools,createdAt:Date.now(),updatedAt:Date.now()};db.articles.push(a);saveDB();go("#a-"+a.id);toast(t("opened",f.name));
    }else throw 0;
  }catch(err){toast(t("notBackup"))}};
$("#b-logo").onclick=()=>$("#f-logo").click();
$("#f-logo").onchange=e=>{const f=e.target.files[0];e.target.value="";if(!f)return;const r=new FileReader();
  r.onload=()=>{logo={data:r.result,type:/png/i.test(f.type)?"PNG":"JPEG"};lsSet(LOGOKEY,JSON.stringify(logo));saveDB();if(route.view==="article")schedulePreview(30);toast(t("logoSet"))};r.readAsDataURL(f)};
window.addEventListener("beforeunload",()=>{if(edTimer){clearTimeout(edTimer);flushEditor()}if(DESK)desk.flush()});

if(DESK)document.addEventListener("keydown",e=>{if(e.key==="F5"||((e.ctrlKey||e.metaKey)&&(e.key==="r"||e.key==="R")))e.preventDefault()});
(async()=>{if(DESK){try{await desk.init()}catch(e){console.error(e)}}await loadDB();ensureDB();chrome();render();if(!LANG)chooseLanguage()})();
