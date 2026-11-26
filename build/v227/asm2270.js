/* ===================== 2.27: assemblies that you control, with their tool number per machine ===================== */
Object.assign(I18N.fr,{asmMk:n=>n?`Créer les assemblages (${n})`:"Créer les assemblages",asmMkT:"Chaque ligne avec un porte-outil et un code outil (ou un type et un Ø) devient un assemblage, avec son numéro T pour cette machine. Rien n’est plus créé tout seul.",
  asmMkDone:(n,l)=>`${n} ${pl(n,"assemblage créé","assemblages créés")}${l?` · ${l} ${pl(l,"ligne reliée","lignes reliées")} à un assemblage existant`:""}`,asmMkNone:"Toutes les lignes complètes ont déjà leur assemblage.",
  asmTn:"Numéro d’outil par machine",asmTnP:"Le T de cet assemblage sur chaque machine. Il remplit la case T quand vous tapez le code de l’assemblage dans une fiche de cette machine, et il se met à jour quand vous changez le T dans une fiche.",
  asmTnNone:"Pas encore utilisé sur une machine.",asmTnAdd:"Ajouter une machine",asmTnChip:(m,tn)=>`${m} ${tn}`,
  asmPushed:(c,n)=>`${c} enregistré · ${n} ${pl(n,"fiche mise à jour","fiches mises à jour")}`,asmLockedN:n=>`${n} ${pl(n,"fiche validée garde","fiches validées gardent")} l’ancien`,
  asmRowDiff:(T,c)=>`${T} n’est plus pareil que l’assemblage ${c}`,asmRowUpd:c=>`Mettre à jour ${c}`,asmUpdOk:(c,n)=>`${c} mis à jour${n?` · ${n} autre${n>1?"s":""} fiche${n>1?"s":""}`:""}`,
  asmTnSet:(c,m,tn)=>`${c} : ${tn} sur ${m}`,asmTFill:(T,c)=>`${T} vient de l’assemblage ${c} pour cette machine`,
  asmPurge:n=>`Supprimer les inutilisés (${n})`,asmPurgeT:"Les assemblages créés tout seuls par les anciennes versions, qu’aucune fiche n’utilise et que vous n’avez pas gardés.",asmPurgeQ:n=>`Supprimer ${n} ${pl(n,"assemblage inutilisé","assemblages inutilisés")} ? Les fiches ne changent pas.`,asmPurged:n=>`${n} ${pl(n,"assemblage supprimé","assemblages supprimés")}`,
  asmNoneP2:"Créez-les depuis une fiche outils (« Créer les assemblages » sous le tableau) ou ici avec « + Nouvel assemblage ».",
  asmDelRows:n=>n?` · ${n} ${pl(n,"ligne détachée","lignes détachées")}`:""});
Object.assign(I18N.en,{asmMk:n=>n?`Make the assemblies (${n})`:"Make the assemblies",asmMkT:"Each row with a holder and a tool code (or a type and a Ø) becomes an assembly, with its T number for this machine. Nothing is made by itself any more.",
  asmMkDone:(n,l)=>`${n} ${pl(n,"assembly made","assemblies made")}${l?` · ${l} ${pl(l,"row linked","rows linked")} to an existing assembly`:""}`,asmMkNone:"Every complete row already has its assembly.",
  asmTn:"Tool number per machine",asmTnP:"The T of this assembly on each machine. It fills the T box when you type the assembly code in a sheet of that machine, and it follows when you change the T in a sheet.",
  asmTnNone:"Not used on a machine yet.",asmTnAdd:"Add a machine",asmTnChip:(m,tn)=>`${m} ${tn}`,
  asmPushed:(c,n)=>`${c} saved · ${n} ${pl(n,"sheet updated","sheets updated")}`,asmLockedN:n=>`${n} validated ${pl(n,"sheet keeps","sheets keep")} the old one`,
  asmRowDiff:(T,c)=>`${T} no longer matches assembly ${c}`,asmRowUpd:c=>`Update ${c}`,asmUpdOk:(c,n)=>`${c} updated${n?` · ${n} other ${pl(n,"sheet","sheets")}`:""}`,
  asmTnSet:(c,m,tn)=>`${c}: ${tn} on ${m}`,asmTFill:(T,c)=>`${T} comes from assembly ${c} for this machine`,
  asmPurge:n=>`Delete the unused ones (${n})`,asmPurgeT:"Assemblies made by themselves by older versions, used by no sheet and not kept.",asmPurgeQ:n=>`Delete ${n} unused ${pl(n,"assembly","assemblies")}? The sheets do not change.`,asmPurged:n=>`${n} ${pl(n,"assembly","assemblies")} deleted`,
  asmNoneP2:"Make them from a tool sheet (“Make the assemblies” under the table) or here with “+ New assembly”.",
  asmDelRows:n=>n?` · ${n} ${pl(n,"row","rows")} unlinked`:""});

const asmLocked=ar=>!!(ar&&ar.validated&&ar.status==="done");
const asmByCode=v=>{const k=asmKey(v)||clean(v).toUpperCase();return k?asmList().find(a=>a.code===k)||null:null};
const asmTn=a=>(a&&a.tnum&&typeof a.tnum==="object")?a.tnum:{};
function asmSetTn(a,mid,tn){if(!a||!mid)return false;tn=normT(tn);const o={...asmTn(a)};if(!tn){if(!(mid in o))return false;delete o[mid]}else{if(o[mid]===tn)return false;o[mid]=tn}a.tnum=o;a.updatedAt=Date.now();return true}
const asmMName=id=>{const m=M(id);return m?(clean(m.abbr)||clean(m.name)):"?"};

// usage is by the code written in the row, not by the look-alike values: editing an assembly never "loses" its sheets
asmUses=function(){const U=new Map(),by=new Map(asmList().map(a=>[a.code,a]));
  db.articles.forEach(ar=>realTools(ar.tools).forEach(x=>{const v=clean(x.asm);if(!v)return;const a=by.get(asmKey(v)||v.toUpperCase());if(!a)return;if(!U.has(a.sig))U.set(a.sig,[]);U.get(a.sig).push(ar)}));return U};
// a row that already has a code keeps it; only an empty one takes the assembly it is identical to
asmLink=function(art){let ch=0;if(!art||!Array.isArray(art.tools))return 0;realTools(art.tools).forEach(x=>{if(clean(x.asm))return;const a=asmOfTool(x);if(!a)return;x.asm=a.code;x.asmAuto=1;ch++;
    if(!asmTn(a)[art.machineId]&&clean(x.t))asmSetTn(a,art.machineId,x.t)});return ch};
// nothing is made by itself any more while you type: rows are only linked, and the T of linked rows is remembered for the machine
asmSync=function(){asmDirty=false;return 0};
asmLater=function(){asmDirty=true;clearTimeout(asmTimer);asmTimer=setTimeout(()=>{asmDirty=false;if(!cur)return;let ch=asmLink(cur);
  realTools(cur.tools).forEach(x=>{const a=clean(x.asm)&&asmByCode(x.asm);if(a&&clean(x.t)&&!asmTn(a)[cur.machineId]&&asmSetTn(a,cur.machineId,x.t))ch++});
  if(ch){saveDB();asmChips()}asmMkCount()},1200)};

// "Make the assemblies" under the tool table
function asmMissing(art){return realTools(art.tools).filter(x=>!clean(x.asm)&&asmReady(x))}
function asmMakeFor(art){if(!art)return;flushEditor();const L=asmList();let made=0,linked=0;
  asmMissing(art).forEach(x=>{let a=asmOfTool(x);
    if(a)linked++;else{const tool={};ASMF.forEach(k=>{if(clean(x[k]))tool[k]=String(x[k]).trim()});a={id:uid(),code:asmNext(),tool,sig:asmSig(tool),auto:0,src:art.id,keep:1,createdAt:Date.now()};L.push(a);made++}
    x.asm=a.code;x.asmAuto=0;if(clean(x.t)&&!asmTn(a)[art.machineId])asmSetTn(a,art.machineId,x.t)});
  if(!made&&!linked){toast(t("asmMkNone"));return}
  saveDB();if(route.view==="article"){renderRows();edited()}asmChips();asmMkCount();toast(t("asmMkDone",made,linked))}
function asmMkCount(){const b=$("#b-mkasm");if(!b||!cur)return;const n=asmMissing(cur).length;b.textContent=t("asmMk",n);b.disabled=!n||!can("article")||asmLocked(cur)}
document.addEventListener("click",e=>{const b=e.target.closest&&e.target.closest("#b-mkasm");if(b&&cur)asmMakeFor(cur)});
{const r0=renderEditor;renderEditor=function(art){r0.apply(this,arguments);try{const ops=$("#b-ops");if(ops&&!$("#b-mkasm")){const b=document.createElement("button");b.className="btn ghost";b.id="b-mkasm";b.type="button";b.title=t("asmMkT");ops.after(b)}asmMkCount()}catch(_){}}}

// typing an assembly code in a row: its T for this machine comes with it (or the row's T is remembered when the machine has none yet)
{const rf0=rowFill;rowFill=function(i,src,keys,kind,label){if(kind==="asm"&&cur){const x=cur.tools[i],a=asmByCode(label);
    if(x&&a){const tn=asmTn(a)[cur.machineId];if(tn&&normT(x.t)!==tn){x.t=tn}else if(!tn&&clean(x.t)){asmSetTn(a,cur.machineId,x.t)}}}
  return rf0.apply(this,arguments)}}

// in a sheet: changing the T of a linked row moves the assembly's T for this machine; changing the tool itself offers to update the assembly
document.addEventListener("change",e=>{const el=e.target,k=el&&el.dataset&&el.dataset.k;if(!k||!cur)return;const tr=el.closest&&el.closest("#rows tr[data-i]");if(!tr)return;
  const x=cur.tools[+tr.dataset.i];if(!x)return;const a=clean(x.asm)&&asmByCode(x.asm);if(!a)return;
  if(k==="t"){if(clean(x.t)&&asmSetTn(a,cur.machineId,x.t)){saveDB();toast(t("asmTnSet",a.code,asmMName(cur.machineId),normT(x.t)))}return}
  if(!ASMF.includes(k))return;
  setTimeout(()=>{if(!cur||cur.tools[+tr.dataset.i]!==x)return;const d=asmDiffs(x);if(!d||!d.length||!can("article"))return;
    toast(t("asmRowDiff",normT(x.t)||"",a.code),{label:t("asmRowUpd",a.code),fn:()=>asmUpdateFrom(a,x)})},350)});
function asmUpdateFrom(a,x){const tool={};ASMF.forEach(k=>{const v=clean(x[k])?String(x[k]).trim():clean(a.tool[k])?a.tool[k]:"";if(v)tool[k]=k==="code"?normCode(v):v});
  if(!asmReady(tool)){toast(t("asmNeed"));return}const s=asmSig(tool),other=asmList().find(o=>o!==a&&o.sig===s);if(other){toast(t("asmSame",other.code));return}
  a.tool=tool;a.sig=s;a.updatedAt=Date.now();const r=asmPush(a,cur);saveDB();if(route.view==="article"){asmChips();renderRows()}toast(t("asmUpdOk",a.code,r.n))}
// an assembly's tool goes into every sheet that uses it (validated sheets are locked and keep theirs); its T per machine too
function asmPush(a,skip){let n=0,locked=0;db.articles.forEach(ar=>{if(ar===skip)return;let ch=false;
  realTools(ar.tools).forEach(x=>{if(!clean(x.asm)||asmByCode(x.asm)!==a)return;
    if(asmLocked(ar)){if(asmDiffs(x)?.length)locked++;return}
    ASMF.forEach(k=>{const v=a.tool[k]||"";if(String(x[k]||"")!==v){x[k]=v;ch=true}});
    const tn=asmTn(a)[ar.machineId];if(tn&&normT(x.t)!==tn){x.t=tn;ch=true}});
  if(ch){ar.updatedAt=Date.now();n++}});return{n,locked}}

// the assembly window: T per machine, and saving updates the sheets
{const d0=asmDialog;asmDialog=function(a){d0.apply(this,arguments);const form=$(".dlg .asmform");if(!form)return;const isNew=!a;
  const tn={...asmTn(a)},used=new Set(Object.keys(tn));if(a)(asmUses().get(a.sig)||[]).forEach(ar=>used.add(ar.machineId));
  const ms=db.machines.filter(m=>used.has(m.id)),rest=db.machines.filter(m=>!used.has(m.id));
  const box=document.createElement("div");box.className="c6 asmtn";
  const row=m=>`<label class="tnr"><span>${esc(clean(m.abbr)||clean(m.name))}</span><input data-tnm="${m.id}" class="m up" value="${esc(tn[m.id]||"")}" placeholder="T…" autocomplete="off"></label>`;
  box.innerHTML=`<div class="tnh"><b>${esc(t("asmTn"))}</b><span>${esc(t("asmTnP"))}</span></div><div class="tng">${ms.map(row).join("")||`<span class="dim small" id="tn-none">${esc(t("asmTnNone"))}</span>`}</div>
    ${rest.length?`<label class="f tnadd"><select id="tn-add"><option value="">${esc(t("asmTnAdd"))}…</option>${rest.map(m=>`<option value="${m.id}">${esc(mLabel(m))}</option>`).join("")}</select></label>`:""}`;
  const keep=form.querySelector("#as-keep");(keep?keep.closest("label"):form.lastElementChild).before(box);
  const add=box.querySelector("#tn-add");if(add)add.onchange=()=>{const m=M(add.value);if(!m)return;const n=box.querySelector("#tn-none");if(n)n.remove();box.querySelector(".tng").insertAdjacentHTML("beforeend",row(m));add.querySelector(`option[value="${m.id}"]`).remove();add.value="";box.querySelector(`[data-tnm="${m.id}"]`).focus()};
  const ok=$("#as-ok");if(!ok)return;
  ok.addEventListener("click",()=>{const vals={};box.querySelectorAll("[data-tnm]").forEach(i=>{const v=normT(i.value);if(v)vals[i.dataset.tnm]=v});const n0=asmList().length,before=a?JSON.stringify(a.tool)+JSON.stringify(asmTn(a)):"";
    setTimeout(()=>{if($("#as-err")&&!$("#as-err").hidden)return;const tgt=isNew?(asmList().length>n0?asmList()[asmList().length-1]:null):a;if(!tgt)return;tgt.tnum=vals;
      if(isNew)return void saveDB();
      if(JSON.stringify(tgt.tool)+JSON.stringify(asmTn(tgt))!==before){const r=asmPush(tgt,null);saveDB();try{drawAsm()}catch(_){}toast(t("asmPushed",tgt.code,r.n)+(r.locked?" · "+t("asmLockedN",r.locked):""))}else saveDB()},0)},true);
  const del=$("#as-del");if(del)del.addEventListener("click",()=>{setTimeout(()=>{const go=$("#as-delok");if(go)go.addEventListener("click",()=>{let n=0;db.articles.forEach(ar=>{if(asmLocked(ar))return;realTools(ar.tools).forEach(x=>{if(clean(x.asm)&&(asmKey(x.asm)||clean(x.asm).toUpperCase())===a.code){x.asm="";x.asmAuto=0;n++}})});
    if(n){saveDB();setTimeout(()=>toast(t("asmDelOk",a.code)+t("asmDelRows",n)),50)}},true)},0)})}}

// the assemblies page: T per machine under each code, and a clean-up of the unused automatic ones
{const d0=drawAsm;drawAsm=function(){d0.apply(this,arguments);const box=$("#asmres");if(!box)return;
  box.querySelectorAll("tr[data-asmid]").forEach(tr=>{const a=asmList().find(x=>x.id===tr.dataset.asmid);if(!a)return;const tn=asmTn(a),ks=Object.keys(tn);if(!ks.length)return;
    const td=tr.querySelector("td");if(td)td.insertAdjacentHTML("beforeend",`<div class="asmtnl">${ks.sort((p,q)=>asmMName(p).localeCompare(asmMName(q),undefined,{numeric:true})).map(id=>`<span><i>${esc(asmMName(id))}</i>${esc(tn[id])}</span>`).join("")}</div>`)});
  const e=box.querySelector(".empty p");if(e&&!asmList().length)e.textContent=t("asmNoneP2");asmPurgeBtn()}}
function asmUnused(){const U=asmUses();return asmList().filter(a=>a.auto&&!a.keep&&!U.has(a.sig))}
function asmPurgeBtn(){const ph=$("#view .asmp .ph");if(!ph)return;let b=$("#asm-purge");const n=asmUnused().length;
  if(!n||!can("article")){if(b)b.remove();return}
  if(!b){b=document.createElement("button");b.className="btn ghost";b.id="asm-purge";b.title=t("asmPurgeT");const nw=$("#asm-new");nw?nw.before(b):ph.appendChild(b);
    b.onclick=()=>{const L=asmUnused();dialog(esc(t("asmPurge",L.length)),`<p style="margin:0">${esc(t("asmPurgeQ",L.length))}</p>`,`<button class="btn ghost" id="d-cancel">${esc(t("cancel"))}</button><button class="btn red" id="pg-ok">${esc(t("asmDel"))}</button>`);
      $("#d-cancel").onclick=closeDlg;$("#pg-ok").onclick=()=>{const S=new Set(L);db.assemblies=asmList().filter(a=>!S.has(a));saveDB();closeDlg();drawAsm();toast(t("asmPurged",L.length))}}}
  b.textContent=t("asmPurge",n)}

// first start with 2.27: remember the T of the rows already linked, machine by machine
function asmT27(){try{if(!db||db.asmT27||!Array.isArray(db.articles))return;let ch=0;
  [...db.articles].sort((p,q)=>(q.updatedAt||0)-(p.updatedAt||0)).forEach(ar=>realTools(ar.tools).forEach(x=>{const a=clean(x.asm)&&asmByCode(x.asm);if(a&&clean(x.t)&&!asmTn(a)[ar.machineId]&&asmSetTn(a,ar.machineId,x.t))ch++}));
  db.asmT27=1;saveDB()}catch(_){}}
// nothing is made by itself at the first start either (older versions filled the library from every sheet)
{const b0=asmBoot;asmBoot=function(){try{if(db&&Array.isArray(db.articles)&&!db.asmSeeded){db.asmSeeded=1;db.asmLinked=1}}catch(_){}b0.apply(this,arguments);asmT27()}}
