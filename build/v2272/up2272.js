/* ===================== 2.27.2: the operation columns always obey the sheet's button ===================== */
// a sheet can say "show" (ops true), "hide" (ops false) or nothing (the layout decides).
// "Hide" now wins even when the layout or the Excel template shows Operation / Time / Tool life.
{const OPH=c=>c?{...c,hidden:[...new Set([...(c.hidden||[]),...OPK])],joinTo:Object.fromEntries(Object.entries(c.joinTo||{}).filter(([k,to])=>!OPK.includes(k)&&!OPK.includes(to)))}:c;
  const c0=cfgOf;cfgOf=function(art){const c=c0.apply(this,arguments);return art&&art.ops===false?OPH(c):c};
  const c1=cfgXlOf;cfgXlOf=function(art){const c=c1.apply(this,arguments);return art&&art.ops===false?OPH(c):c}}
// the button says what it will do, from what is really on screen
function opsBtnDraw(){const b=$("#b-ops");if(!b||!cur)return;const on=opsVis();b.textContent=on?t("opsOff"):t("opsBtn");b.setAttribute("aria-pressed",on)}
{const r0=renderEditor;renderEditor=function(){r0.apply(this,arguments);try{opsBtnDraw()}catch(_){}}}
document.addEventListener("click",e=>{const b=e.target.closest&&e.target.closest("#b-ops");if(!b||!cur)return;e.stopImmediatePropagation();
  cur.ops=opsVis()?false:true;edited();try{refreshCols(cur)}catch(_){}renderEditor(cur)},true);
