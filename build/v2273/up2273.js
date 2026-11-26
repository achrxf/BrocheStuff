/* ===================== 2.27.3: operation columns only when you ask, and a switch next to "Masquer le schéma" ===================== */
// reading a program keeps every tool change and its operation name, but no longer switches the operation columns on
{const ai0=applyImport;applyImport=function(){const A=cur,was=A?A.ops:undefined;const r=ai0.apply(this,arguments);
  try{if(A&&A.ops===true&&was!==true){if(was===undefined)delete A.ops;else A.ops=was;refreshCols(A);const B=A;setTimeout(()=>{if(cur===B&&route.view==="article")renderEditor(B)},0)}}catch(_){}return r}}
// once: sheets that got the columns by themselves in 2.27 lose them (the operation names stay in the sheet)
{const b0=asmBoot;asmBoot=function(){b0.apply(this,arguments);try{if(db&&Array.isArray(db.articles)&&!db.ops273){db.ops273=1;db.articles.forEach(a=>{if(a.ops===true)delete a.ops});saveDB()}}catch(_){}}}
// the switch in the tools header, next to "Masquer le schéma"
function opsHdrBtn(){const td=$("#b-tdtog");if(!td||!cur)return;let b=$("#b-ops2");if(!b){b=document.createElement("button");b.type="button";b.id="b-ops2";b.className="btn sm ghost";td.before(b)}
  const on=opsVis();b.textContent=on?t("opsOff"):t("opsBtn");b.title=t("opsBtnT");b.setAttribute("aria-pressed",on)}
{const r0=renderEditor;renderEditor=function(){r0.apply(this,arguments);try{opsHdrBtn()}catch(_){}}}
document.addEventListener("click",e=>{const b=e.target.closest&&e.target.closest("#b-ops2");if(!b||!cur)return;e.stopImmediatePropagation();
  cur.ops=opsVis()?false:true;edited();try{refreshCols(cur)}catch(_){}renderEditor(cur)},true);
// CNC files saved by older posts/editors are often not UTF-8: read them as Windows text so É, Ø, ° show right
async function ncText(f){const buf=await f.arrayBuffer();try{return new TextDecoder("utf-8",{fatal:true}).decode(buf)}catch(_){try{return new TextDecoder("windows-1252").decode(buf)}catch(__){return new TextDecoder().decode(buf)}}}
