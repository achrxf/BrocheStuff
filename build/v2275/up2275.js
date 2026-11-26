/* ===================== 2.27.5: Print follows the page — PDF or Excel ===================== */
Object.assign(I18N.fr,{prPdfT:"Imprimer la fiche PDF (un outil par ligne)",prXlT:"Imprimer l’Excel (les lignes comme dans l’Excel, répétitions comprises)",prXlDo:"Impression de l’Excel…"});
Object.assign(I18N.en,{prPdfT:"Print the PDF sheet (one line per tool)",prXlT:"Print the Excel (the rows as in the Excel, repeats included)",prXlDo:"Printing the Excel…"});
// which one: the Excel tab, or the Excel preview while typing → the Excel; otherwise the PDF
function printKind(){if(route.view!=="article")return"pdf";if(edMode==="excel")return"xlsx";if(edMode==="pdf")return"pdf";return pvOn&&pvMode==="xlsx"?"xlsx":"pdf"}
function printBtnDraw(){const b=$("#b-print");if(!b)return;const k=route.view==="article"?printKind():"pdf";let s=b.querySelector(".pmode");
  if(route.view!=="article"){if(s)s.remove();return}
  if(!s){s=document.createElement("span");s.className="pmode";b.append(s)}s.textContent=k==="xlsx"?"Excel":"PDF";s.classList.toggle("xl",k==="xlsx");b.title=t(k==="xlsx"?"prXlT":"prPdfT")}
{const r0=render;render=function(){const r=r0.apply(this,arguments);try{printBtnDraw()}catch(_){}return r}}
{const s0=setEdMode;setEdMode=function(){s0.apply(this,arguments);try{printBtnDraw()}catch(_){}}}
document.addEventListener("click",e=>{if(e.target.closest&&e.target.closest("[data-pvm],#b-pv"))setTimeout(printBtnDraw,0)});
// the Excel as it looks in the preview, without the A B C / 1 2 3 headers, fitted to the A4 width
async function printExcel(art){toast(t("prXlDo"));
  const host=document.createElement("div");host.style.cssText="position:fixed;left:-30000px;top:0;visibility:hidden";host.innerHTML=xlPreviewHTML(art);document.body.append(host);
  try{await xlFillImgs(host,art)}catch(_){}
  const tb=host.querySelector("table.xlpv"),thH=(tb.tHead&&tb.tHead.offsetHeight)||21,W=Math.max(1,tb.offsetWidth-30),H=tb.offsetHeight-thH;
  const pW=733,lW=1062,land=W>pW*1.25,aW=land?lW:pW,aH=(land?pW:lW)-4;let z=Math.min(1,aW/W);if(H*z>aH&&H*z<=aH*1.3)z=aH/H;   // a one-page sheet stays on one page
  const wrap=host.querySelector(".xlwrap");wrap.style.setProperty("--xlth",thH+"px");const body=host.innerHTML;host.remove();
  let css="";const want=/xlpv|xlwrap|xlimg/;
  for(const sh of document.styleSheets){let rules;try{rules=sh.cssRules}catch(_){continue}for(const r of rules){if(r.type===5&&/IBM Plex|Barlow/i.test(r.cssText))css+=r.cssText;else if(r.selectorText&&want.test(r.selectorText))css+=r.cssText}}
  css+=`@page{margin:8mm}body{background:#fff}.xlout{overflow:hidden;width:${Math.ceil(W*z)+2}px}.xlin{zoom:${z.toFixed(4)}}
    .xlwrap{position:relative;margin:-${thH}px 0 0 -30px}table.xlpv th.xlc,table.xlpv th.xlr{visibility:hidden;border-color:transparent!important}
    table.xlpv tr{break-inside:avoid}.xlimg{position:absolute}*{-webkit-print-color-adjust:exact;print-color-adjust:exact}`;
  await printHTML({css,body:`<div class="xlout"><div class="xlin">${body}</div></div>`},land)}
document.addEventListener("click",e=>{const b=e.target.closest&&e.target.closest("#b-print");if(!b||route.view!=="article")return;if(printKind()!=="xlsx")return;
  e.stopImmediatePropagation();e.preventDefault();try{flushEditor()}catch(_){}const art=A(route.id);if(art)printExcel(art)},true);
window.addEventListener("hashchange",()=>setTimeout(printBtnDraw,60));
