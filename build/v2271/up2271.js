/* ===================== 2.27.1: everything in capitals (unless you turn it off) ===================== */
Object.assign(I18N.fr,{upOn:"Majuscules automatiques",upOnT:"Les types, porte-outils, codes, plaquettes, opérations et vos colonnes s’écrivent en MAJUSCULES. Cliquez pour l’arrêter.",
  upOff:"Majuscules : comme tapé",upOffT:"Ce que vous tapez reste comme vous l’écrivez. Cliquez pour tout remettre en MAJUSCULES.",
  upDone:n=>`Tout est en MAJUSCULES${n?` · ${n} ${pl(n,"fiche mise à jour","fiches mises à jour")}`:""}`,upStop:"Majuscules automatiques arrêtées : ce que vous tapez reste comme vous l’écrivez"});
Object.assign(I18N.en,{upOn:"Automatic capitals",upOnT:"Types, holders, codes, inserts, operations and your own columns are written in CAPITALS. Click to stop it.",
  upOff:"Capitals: as typed",upOffT:"What you type stays as you write it. Click to put everything back in CAPITALS.",
  upDone:n=>`Everything is in CAPITALS${n?` · ${n} ${pl(n,"sheet","sheets")} updated`:""}`,upStop:"Automatic capitals stopped: what you type stays as you write it"});
const UPK=["type","insert","holder","code","op","asm"];
const upOn=()=>!(db&&db.noUpper);
const upKey=k=>UPK.includes(k)||String(k).startsWith("x_");
const upStr=v=>String(v).toLocaleUpperCase("fr").replace(/Μ/g,"µ");   // keep µ (µm) as it is
function upTool(x){let ch=false;if(!x||typeof x!=="object")return false;Object.keys(x).forEach(k=>{if(upKey(k)&&typeof x[k]==="string"){const u=upStr(x[k]);if(u!==x[k]){x[k]=u;ch=true}}});return ch}
// every sheet that is not validated (validated ones are locked), the crib's types and the assemblies
function upAll(){let n=0;(db.articles||[]).forEach(ar=>{if(asmLocked(ar)||!Array.isArray(ar.tools))return;let ch=false;ar.tools.forEach(x=>{if(upTool(x))ch=true});if(ch){n++}});
  (db.catalog||[]).forEach(c=>{["type","insert"].forEach(k=>{if(typeof c[k]==="string"){const u=upStr(c[k]);if(u!==c[k])c[k]=u}})});
  asmList().forEach(a=>{if(upTool(a.tool))a.sig=asmSig(a.tool)});return n}
function upClass(){document.documentElement.classList.toggle("noup",!upOn())}
function drawUpBtn(){const b=$("#b-upper");if(!b)return;const on=upOn();
  b.innerHTML=`<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 18 8.5 6 13 18M5.7 14h5.6"/><path d="M15 18V6h3.2a2.8 2.8 0 0 1 0 5.6H15M15 11.6h3.8a3.2 3.2 0 0 1 0 6.4H15"/></svg><span class="lbl">${esc(on?t("upOn"):t("upOff"))}</span>${on?'<span class="upck" aria-hidden="true">✓</span>':""}`;
  b.title=on?t("upOnT"):t("upOffT");b.setAttribute("aria-pressed",on)}
(function(){const top=$("header.top");if(!top||$("#b-upper"))return;const b=document.createElement("button");b.className="tb";b.id="b-upper";b.type="button";
  const a=$("#b-skin")||$("#b-theme");a?a.after(b):top.appendChild(b);
  b.onclick=()=>{if(!can("article")&&!hasRight("cribEdit")){toast(t("noRight"));return}
    if(upOn()){db.noUpper=1;saveDB();upClass();drawUpBtn();toast(t("upStop"))}
    else{delete db.noUpper;flushEditor();const n=upAll();saveDB();upClass();drawUpBtn();try{render()}catch(_){}toast(t("upDone",n))}};
  upClass();drawUpBtn()})();
{const c0=chrome;chrome=function(){c0.apply(this,arguments);drawUpBtn();upClass()}}
// typing: what you see is in capitals at once, and it is saved in capitals when you leave the box (before the crib/assembly look-ups)
document.addEventListener("change",e=>{const el=e.target;if(!upOn()||!el||!el.matches)return;
  const tr=el.closest&&el.closest("#rows tr[data-i]"),k=el.dataset&&el.dataset.k;
  if(tr&&k&&upKey(k)&&cur){if(typeof el.value==="string"&&el.value!==upStr(el.value))el.value=upStr(el.value);const x=cur.tools[+tr.dataset.i];if(!x)return;
    // only when the sheet already holds this text (a box being thrown away by a redraw can fire a late "change" with an old value)
    const mtd=el.closest("td.mlc");const v=mtd?cellVal(mtd):el.value;if(typeof v==="string"&&typeof x[k]==="string"&&upStr(x[k])===upStr(v))x[k]=upStr(v);return}
  if(el.matches('input[list="types"],[data-af="type"],[data-af="insert"],[data-af="holder"],[data-af="code"]')&&typeof el.value==="string"){const u=upStr(el.value);if(u!==el.value)el.value=u}},true);
// paste, import, "Read a program", copied rows…: the sheet is put in capitals a moment after any change
{const l0=asmLater;asmLater=function(){l0.apply(this,arguments);clearTimeout(asmLater._u);asmLater._u=setTimeout(()=>{if(!cur||!upOn()||asmLocked(cur))return;
  const a=document.activeElement,typing=a&&a.closest&&a.closest("#rows");let ch=false;cur.tools.forEach((x,i)=>{if(typing&&a.closest(`tr[data-i="${i}"]`))return;if(upTool(x))ch=true});
  if(ch){saveDB();if(route.view==="article")upShow()}},700)}}
// put the capitals in the boxes on screen without redrawing the table (a redraw would throw away the box being typed in)
function upShow(){document.querySelectorAll("#rows tr[data-i]").forEach(tr=>{const x=cur&&cur.tools[+tr.dataset.i];if(!x)return;
  tr.querySelectorAll("[data-k]").forEach(el=>{const k=el.dataset.k;if(!upKey(k)||el===document.activeElement||typeof x[k]!=="string")return;
    if("value" in el&&el.tagName!=="TD"&&!el.closest("td.mlc")){if(el.value!==x[k]&&upStr(el.value)===x[k])el.value=x[k]}})})}
{const ai0=applyImport;applyImport=function(){const r=ai0.apply(this,arguments);try{if(r&&upOn())upAll()}catch(_){}return r}}
// first start with 2.27.1: what is already there goes in capitals too (validated sheets keep what was signed)
{const b0=asmBoot;asmBoot=function(){b0.apply(this,arguments);try{if(db&&Array.isArray(db.articles)&&!db.up271){db.up271=1;if(upOn()){upAll()}saveDB()}}catch(_){}}}
