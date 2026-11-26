/* ===================== 2.28.0 · assemblies come to you ===================== */
Object.assign(I18N.fr,{apkFor:(T,m)=>`${T} sur ${m}`,apkN:n=>`${n} ${pl(n,"assemblage","assemblages")} avec ce numéro`,apkLine:i=>`Comme la ligne ${i}`,apkLineS:"même T dans cette fiche",
  apkSearch:"Chercher un assemblage : Ø, type, porte-outil, code, T…",apkAll:"Tous les assemblages",apkHere:m=>`Sur ${m}`,apkNone:"Aucun assemblage ne correspond.",apkNoneYet:"Pas encore d’assemblage. Remplissez la ligne puis « Créer les assemblages » sous le tableau.",
  apkUse:"Utiliser",apkSkip:"Aucun, je remplis moi-même",apkUsed:n=>n?`${n} ${pl(n,"fiche","fiches")}`:"pas encore utilisé",apkKeys:"↑ ↓ pour choisir · Entrée pour prendre · Échap pour fermer",
  apkCopied:(T,i)=>`${T} : infos de la ligne ${i} copiées`,apkTwin:(T,m,L)=>`${T} sur ${m} sert aussi pour ${L} : choisissez le bon dans la liste quand vous tapez ${T}.`,apkTwinS:L=>`Même T aussi : ${L}`,apkCur:"sur cette ligne",apkTwinTn:(m,tn,c)=>`${tn} est aussi le T de ${c} sur ${m}. C’est permis : en tapant ${tn} dans une fiche de ${m}, vous choisirez lequel.`});
Object.assign(I18N.en,{apkFor:(T,m)=>`${T} on ${m}`,apkN:n=>`${n} ${pl(n,"assembly","assemblies")} with this number`,apkLine:i=>`Same as line ${i}`,apkLineS:"same T in this sheet",
  apkSearch:"Find an assembly: Ø, type, holder, code, T…",apkAll:"All assemblies",apkHere:m=>`On ${m}`,apkNone:"No assembly matches.",apkNoneYet:"No assembly yet. Fill the row, then “Make the assemblies” under the table.",
  apkUse:"Use",apkSkip:"None, I fill it in myself",apkUsed:n=>n?`${n} ${pl(n,"sheet","sheets")}`:"not used yet",apkKeys:"↑ ↓ to choose · Enter to take · Esc to close",
  apkCopied:(T,i)=>`${T}: info from line ${i} copied`,apkTwin:(T,m,L)=>`${T} on ${m} is also used for ${L}: pick the right one in the list when you type ${T}.`,apkTwinS:L=>`Same T too: ${L}`,apkCur:"on this row",apkTwinTn:(m,tn,c)=>`${tn} is also the T of ${c} on ${m}. That is allowed: when you type ${tn} in a sheet of ${m}, you pick which one.`});

// a little picture of the tool, from its type
function toolGlyph(type){const s=String(type||"").toUpperCase();const P=(d)=>`<svg viewBox="0 0 40 16" aria-hidden="true" class="tg">${d}</svg>`;
  const body='<rect x="1" y="4" width="11" height="8" rx="1" class="tgh"/>';
  if(/TARAUD|TAP/.test(s))return P(body+'<rect x="12" y="6" width="12" height="4"/><path d="M24 5h14v6H24z" class="tgc"/><path d="M26 5l2 6M29 5l2 6M32 5l2 6M35 5l2 6" class="tgl"/>');
  if(/FORET|DRILL|CENTR|POINT/.test(s))return P(body+'<rect x="12" y="6" width="8" height="4"/><path d="M20 5.5h14l4 2.5-4 2.5H20z" class="tgc"/><path d="M22 5.5l4 5M26 5.5l4 5M30 5.5l3 4" class="tgl"/>');
  if(/ALES|REAM/.test(s))return P(body+'<rect x="12" y="6" width="10" height="4"/><path d="M22 5.5h16v5H22z" class="tgc"/><path d="M24 5.5v5M27 5.5v5M30 5.5v5M33 5.5v5M36 5.5v5" class="tgl"/>');
  if(/CHANF|CHAMF|CHANFREIN/.test(s))return P(body+'<rect x="12" y="6" width="14" height="4"/><path d="M26 4h6l6 4-6 4h-6z" class="tgc"/>');
  if(/SURFA|FACE|PLAT|DISQUE|DISC/.test(s))return P(body+'<rect x="12" y="6" width="10" height="4"/><path d="M22 2h10v12H22z" class="tgc"/><path d="M24 2v12M27 2v12M30 2v12" class="tgl"/>');
  if(/BOUL|BALL|HEMI|TORI|TORE|R[ ]?\d/.test(s))return P(body+'<rect x="12" y="6" width="12" height="4"/><path d="M24 4.5h9a3.5 3.5 0 0 1 0 7h-9z" class="tgc"/><path d="M26 4.5l3 7M30 4.5l3 6" class="tgl"/>');
  if(/FRAISE|MILL|FR\b|2T|3T|4T/.test(s))return P(body+'<rect x="12" y="6" width="12" height="4"/><path d="M24 4.5h14v7H24z" class="tgc"/><path d="M26 4.5l3 7M30 4.5l3 7M34 4.5l3 7" class="tgl"/>');
  if(/PALP|PROBE|SONDE/.test(s))return P(body+'<rect x="12" y="7" width="20" height="2"/><circle cx="35" cy="8" r="3" class="tgc"/>');
  return P(body+'<rect x="12" y="6" width="12" height="4"/><path d="M24 5h12v6H24z" class="tgc"/>')}
const apkNorm=v=>String(v||"").toUpperCase().replace(/[ØΦ⌀]/g,"").replace(/,/g,".").replace(/\s+/g," ").trim();
function apkHay(a){const x=a.tool||{},tn=asmTn(a);return apkNorm([a.code,x.type,x.diameter,"D"+(x.diameter||""),x.ra,x.insert,x.ls,x.oal,x.holder,x.code,...Object.entries(tn).map(([m,v])=>asmMName(m)+" "+v+" "+v)].join(" "))}
let APK=null;   // the open picker
let APKUSE=null;// usage counts, computed once per opening
function apkUses(){if(APKUSE&&Date.now()-APKUSE.at<4000)return APKUSE.m;const m=new Map();asmUses().forEach((L,sig)=>{const a=asmList().find(x=>x.sig===sig);if(a)m.set(a.code,new Set(L.map(ar=>ar.id)).size)});APKUSE={at:Date.now(),m};return m}
function apkCard(a,o){o=o||{};const x=a.tool||{},tn=asmTn(a),mid=cur&&cur.machineId,us=apkUses().get(a.code)||0;
  const hl=String(x.holder||"").split("\n"),dim=[x.diameter?`Ø${esc(x.diameter)}`:"",clean(x.ra)?esc(x.ra):"",clean(x.ls)?`LS ${esc(x.ls)}`:"",clean(x.oal)?`LT ${esc(x.oal)}`:"",clean(x.z)?`Z${esc(x.z)}`:""].filter(Boolean).join(" · ");
  const chips=Object.keys(tn).sort((p,q)=>(q===mid)-(p===mid)||asmMName(p).localeCompare(asmMName(q),undefined,{numeric:true})).map(m=>`<span class="apt${m===mid?" here":""}"><i>${esc(asmMName(m))}</i>${esc(tn[m])}</span>`).join("");
  return `<div class="apc${o.on?" on":""}${o.cur?" cur":""}" role="option" data-apk="${esc(a.code)}" aria-selected="${!!o.on}">
    <div class="apg">${toolGlyph(x.type)}<b>${esc(a.code)}</b></div>
    <div class="apb"><div class="apl1"><b>${esc(x.type||"—")}</b>${dim?`<span>${dim}</span>`:""}</div>
      <div class="apl2">${esc(hl[0]||"")}${hl[1]?` <small>${esc(hl.slice(1).join(" "))}</small>`:""}${clean(x.code)?` <span class="apcode">${esc(x.code)}</span>`:""}${clean(x.insert)?` <span class="apins">${esc(x.insert)}</span>`:""}</div>
      <div class="apl3">${chips||""}<em>${esc(o.cur?t("apkCur"):t("apkUsed",us))}</em></div></div></div>`}
function apkLineCard(j,y){const hl=String(y.holder||"").split("\n")[0];
  return `<div class="apc line" role="option" data-apline="${j}"><div class="apg">${toolGlyph(y.type)}<b>L${j+1}</b></div><div class="apb"><div class="apl1"><b>${esc(t("apkLine",j+1))}</b><span>${esc(t("apkLineS"))}</span></div>
    <div class="apl2"><b>${esc(y.type||"—")}</b>${clean(y.diameter)?` Ø${esc(y.diameter)}`:""}${hl?` · ${esc(hl)}`:""}${clean(y.code)?` <span class="apcode">${esc(y.code)}</span>`:""}${clean(y.asm)?` <span class="apcode">${esc(y.asm)}</span>`:""}</div></div></div>`}
function apkClose(){if(!APK)return;const el=APK.el;APK=null;el.classList.add("out");setTimeout(()=>el.remove(),140)}
function apkPlace(){if(!APK)return;const r=APK.anchor.getBoundingClientRect();if(!r.width&&!r.height){apkClose();return}const el=APK.el,W=Math.min(460,innerWidth-16);el.style.width=W+"px";
  let left=Math.min(Math.max(8,r.left),innerWidth-W-8),top=r.bottom+6;const h=el.offsetHeight;if(top+h>innerHeight-8&&r.top-h-6>8)top=r.top-h-6;el.style.left=left+"px";el.style.top=Math.max(8,top)+"px"}
// the list: same T on this machine first, then this machine's assemblies, then the rest
function apkRank(q,T){const mid=cur&&cur.machineId,toks=apkNorm(q).split(" ").filter(Boolean),L=[];
  asmList().forEach(a=>{const tn=asmTn(a)[mid];let sc=0;if(T&&tn===T)sc+=1000;if(tn)sc+=100;if(toks.length){const h=apkHay(a);if(!toks.every(k=>h.includes(k)))return;if(apkNorm(a.code).startsWith(toks[0]))sc+=50}L.push([sc,a])});
  L.sort((p,q)=>q[0]-p[0]||String(p[1].code).localeCompare(String(q[1].code),undefined,{numeric:true}));return L.map(x=>x[1])}
function apkDraw(){if(!APK)return;const {i,mode}=APK,x=cur.tools[i];if(!x){apkClose();return}const mid=cur.machineId,mN=asmMName(mid),T=normT(x.t);
  let items=[],head="",sub="";
  if(mode==="t"){items=[...APK.lines.map(j=>({line:j})),...APK.asms.map(a=>({a}))];head=t("apkFor",T,mN);sub=APK.asms.length?t("apkN",APK.asms.length):""}
  else{const q=APK.q||"";const L=apkRank(q,T).slice(0,60);items=L.map(a=>({a}));head=q?"":(T&&L.some(a=>asmTn(a)[mid]===T)?t("apkFor",T,mN):t("apkAll"))}
  APK.items=items;if(APK.sel>=items.length)APK.sel=items.length-1;if(APK.sel<0&&items.length)APK.sel=0;
  const curCode=clean(x.asm)&&(asmKey(x.asm)||clean(x.asm).toUpperCase());
  APK.el.innerHTML=`${mode==="q"?"":`<div class="aph"><b>${esc(head)}</b>${sub?`<span>${esc(sub)}</span>`:""}<button class="apx" data-apx aria-label="${esc(t("close"))}">✕</button></div>`}
    ${mode==="q"&&head?`<div class="aph sm"><b>${esc(head)}</b><button class="apx" data-apx aria-label="${esc(t("close"))}">✕</button></div>`:""}
    <div class="apls" role="listbox">${items.length?items.map((it,k)=>it.line!=null?apkLineCard(it.line,cur.tools[it.line]).replace('class="apc line"',`class="apc line${k===APK.sel?" on":""}"`):apkCard(it.a,{on:k===APK.sel,cur:curCode===it.a.code})).join(""):`<p class="apnone">${esc(asmList().length?t("apkNone"):t("apkNoneYet"))}</p>`}</div>
    <div class="apf">${mode==="t"?`<button class="btn sm ghost" data-apskip>${esc(t("apkSkip"))}</button>`:""}<span>${esc(t("apkKeys"))}</span></div>`;
  apkPlace();const on=APK.el.querySelector(".apc.on");if(on)on.scrollIntoView({block:"nearest"})}
function apkOpen(i,mode,anchor){if(!cur||asmLocked(cur)||!can("article"))return;const x=cur.tools[i];if(!x)return;APKUSE=null;
  if(APK&&APK.i===i&&APK.mode===mode){APK.anchor=anchor;apkDraw();return}apkClose();
  const el=document.createElement("div");el.className="apk";el.setAttribute("role","dialog");document.body.append(el);
  APK={el,i,mode,anchor,sel:0,q:"",lines:[],asms:[]};
  if(mode==="t"){const T=normT(x.t),mid=cur.machineId;
    APK.lines=cur.tools.map((y,j)=>j).filter(j=>j!==i&&normT(cur.tools[j].t)===T&&realTools([cur.tools[j]]).length&&ASMF.some(k=>clean(cur.tools[j][k])&&!clean(x[k]))).slice(0,1);
    APK.asms=asmList().filter(a=>asmTn(a)[mid]===T);
    if(!APK.lines.length&&!APK.asms.length){apkClose();return}}
  apkDraw()}
// take a choice
function apkTake(k){if(!APK||!cur)return;const it=APK.items[k],i=APK.i;if(!it)return;apkClose();const x=cur.tools[i];if(!x)return;
  if(it.line!=null){const y=cur.tools[it.line];if(!y)return;const keys=[...ASMF,"asm",...Object.keys(y).filter(f=>f.startsWith("x_"))];
    let n=0;keys.forEach(f=>{if(!clean(x[f])&&clean(y[f])){x[f]=y[f];n++}});if(clean(y.asm)&&!clean(x.asm)){x.asm=y.asm;x.asmAuto=0}
    renderRows();edited();try{tDupMark()}catch(_){}toast(t("apkCopied",normT(x.t),it.line+1));return}
  const a=it.a;x.asm=a.code;x.asmAuto=0;rowFill(i,a.tool,ASMF,"asm",a.code)}
// T typed in a row (by you): the assemblies of this machine with that T, and the same T already in the sheet
document.addEventListener("change",e=>{const el=e.target;if(!e.isTrusted||!el||!el.matches||!el.matches('#rows input[data-k="t"]')||!cur)return;const tr=el.closest("tr[data-i]");if(!tr)return;const i=+tr.dataset.i,x=cur.tools[i];
  if(!x||!clean(x.t)||clean(x.asm))return;setTimeout(()=>{if(cur&&cur.tools[i]===x&&$("#ov").hidden)apkOpen(i,"t",el)},30)});
// the Assembly box: a real picker, searchable by anything
document.addEventListener("focusin",e=>{const el=e.target;if(!el||!el.matches||!el.matches('#rows input[data-k="asm"]')||!cur)return;const tr=el.closest("tr[data-i]");if(!tr)return;
  if(el.classList.contains("sugg")&&!clean(el.value))return;  // the "AS0003 ?" suggestion keeps its own click/Enter
  const i=+tr.dataset.i;setTimeout(()=>{if(document.activeElement!==el||!asmList().length)return;if(APK&&APK.i===i&&APK.mode==="t")return;apkOpen(i,"q",el);if(APK){APK.q="";apkDraw()}},60)});
document.addEventListener("input",e=>{const el=e.target;if(el&&el.matches&&el.matches('#rows input[data-k="asm"]')&&(!APK||APK.anchor!==el||APK.mode!=="q")){const tr=el.closest("tr[data-i]");if(tr&&cur){apkClose();apkOpen(+tr.dataset.i,"q",el)}}
  if(!APK||APK.mode!=="q"||el!==APK.anchor)return;const v=el.value;APK.q=asmKey(v)?asmKey(v):v;APK.sel=0;apkDraw()});
document.addEventListener("keydown",e=>{if(!APK)return;const a=document.activeElement,inRow=a&&a.closest&&a.closest(`#rows tr[data-i="${APK.i}"]`);
  if(e.key==="Escape"){apkClose();e.stopPropagation();return}
  if(!inRow&&a!==APK.anchor)return;
  if(e.key==="ArrowDown"||e.key==="ArrowUp"){if(!APK.items.length)return;e.preventDefault();e.stopImmediatePropagation();APK.sel=(APK.sel+(e.key==="ArrowDown"?1:-1)+APK.items.length)%APK.items.length;apkDraw()}
  else if(e.key==="Enter"&&APK.items.length&&(APK.mode==="t"||a===APK.anchor)){if(APK.mode==="q"&&asmFind(a.value)&&!APK.q)return;e.preventDefault();e.stopImmediatePropagation();const k=APK.sel;if(APK.mode==="q")a.value="";apkTake(k)}},true);
document.addEventListener("mousedown",e=>{if(!APK)return;if(APK.el.contains(e.target)){e.preventDefault();return}if(e.target===APK.anchor)return;apkClose()},true);
document.addEventListener("click",e=>{if(!APK||!APK.el.contains(e.target))return;if(e.target.closest("[data-apx]")){apkClose();return}if(e.target.closest("[data-apskip]")){apkClose();return}
  const c=e.target.closest(".apc");if(!c)return;const k=[...APK.el.querySelectorAll(".apc")].indexOf(c);if(k>=0){if(APK.mode==="q"&&APK.anchor)APK.anchor.value="";apkTake(k)}});
addEventListener("scroll",()=>{if(APK)apkPlace()},true);addEventListener("resize",()=>{if(APK)apkPlace()});
document.addEventListener("focusout",e=>{if(!APK||APK.mode!=="q"||e.target!==APK.anchor)return;setTimeout(()=>{if(APK&&APK.mode==="q"&&document.activeElement!==APK.anchor&&!APK.el.contains(document.activeElement))apkClose()},120)});
window.addEventListener("hashchange",apkClose);
// the picker replaces the plain code list
{const r0=renderRows;renderRows=function(){apkClose();const r=r0.apply(this,arguments);try{document.querySelectorAll('#rows input[data-k="asm"][list]').forEach(el=>el.removeAttribute("list"))}catch(_){}return r}}
// hovering a linked Assembly box shows what it is
let APH=null;
document.addEventListener("mouseover",e=>{const el=e.target.closest&&e.target.closest('#rows input[data-k="asm"]');if(!el||APK||!cur)return;const a=asmFind(el.value);if(!a)return;clearTimeout(APH&&APH.t);
  const t0=setTimeout(()=>{if(APK)return;let h=$("#aphov");if(!h){h=document.createElement("div");h.id="aphov";h.className="apk hov";document.body.append(h)}h.innerHTML=`<div class="apls">${apkCard(a,{cur:true})}</div>`;
    const r=el.getBoundingClientRect(),W=Math.min(420,innerWidth-16);h.style.width=W+"px";h.style.left=Math.min(Math.max(8,r.left),innerWidth-W-8)+"px";h.style.top=(r.bottom+6+h.offsetHeight>innerHeight?r.top-h.offsetHeight-6:r.bottom+6)+"px";h.classList.add("in")},380);
  APH={t:t0,el}});
document.addEventListener("mouseout",e=>{if(!APH)return;const el=e.target.closest&&e.target.closest('#rows input[data-k="asm"]');if(el!==APH.el)return;clearTimeout(APH.t);APH=null;const h=$("#aphov");if(h)h.remove()});
document.addEventListener("focusin",()=>{const h=$("#aphov");if(h&&APK)h.remove()});

// assemblies sharing one T on a machine: shown on the Assemblies page, and explained when you give a T that is taken
function asmTwins(a,mid){const tn=asmTn(a)[mid];if(!tn)return[];return asmList().filter(o=>o!==a&&asmTn(o)[mid]===tn)}
{const d0=drawAsm;drawAsm=function(){d0.apply(this,arguments);const box=$("#asmres");if(!box)return;
  box.querySelectorAll("tr[data-asmid]").forEach(tr=>{const a=asmList().find(x=>x.id===tr.dataset.asmid);if(!a)return;const td=tr.querySelector("td");
    const tw=[];Object.keys(asmTn(a)).forEach(m=>asmTwins(a,m).forEach(o=>tw.push(`${asmMName(m)} ${asmTn(a)[m]} : ${o.code}`)));
    if(tw.length&&td)td.insertAdjacentHTML("beforeend",`<div class="asmtw" title="${esc(t("apkTwin",asmTn(a)[Object.keys(asmTn(a))[0]],"",""))}">${esc(t("apkTwinS",tw.join(" · ")))}</div>`);
    const g=td&&!td.querySelector(".tg")?document.createElement("span"):null;if(g){g.className="asmgl";g.innerHTML=toolGlyph(a.tool&&a.tool.type);td.prepend(g)}})}}
let ASMDLG=null;{const d0=asmDialog;asmDialog=function(a){ASMDLG=a||null;return d0.apply(this,arguments)}}
document.addEventListener("change",e=>{const el=e.target;if(!el||!el.matches||!el.matches(".asmtn [data-tnm]"))return;const v=normT(el.value),mid=el.dataset.tnm;const box=el.closest(".asmtn");let n=box.querySelector(".tnw");
  const o=v&&asmList().find(x=>x!==ASMDLG&&asmTn(x)[mid]===v);if(!o){if(n)n.remove();return}if(!n){n=document.createElement("p");n.className="tnw";box.append(n)}n.textContent=t("apkTwinTn",asmMName(mid),v,o.code)});
// the T picker stays while you are on its row, and goes when you move to another row
document.addEventListener("focusin",e=>{if(!APK||APK.mode!=="t")return;const el=e.target;if(APK.el.contains(el))return;const tr=el.closest&&el.closest("#rows tr[data-i]");if(!tr||+tr.dataset.i!==APK.i)apkClose()});
