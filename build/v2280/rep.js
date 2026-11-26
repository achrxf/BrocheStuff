/* ===================== 2.28.0 · the same T on several lines: every box is compared, and you can make them match ===================== */
Object.assign(I18N.fr,{rpOk:(T,n)=>`${T} : ${n} lignes, le même outil partout. Cliquez pour voir.`,rpMiss:(T,L)=>`${T} : des cases sont vides sur certaines lignes (${L}). Cliquez pour compléter.`,
  rpBad:(T,L)=>`${T} : pas le même outil sur toutes les lignes (${L}). Cliquez pour choisir.`,rpTitle:(T,n)=>`${T} · ${n} lignes`,rpIntro:"Ces lignes ont le même numéro d’outil : c’est le même outil, utilisé pour plusieurs opérations. Pour chaque case qui diffère, choisissez la bonne valeur ; elle sera mise sur toutes les lignes.",
  rpField:"Case",rpLine:i=>`Ligne ${i}`,rpEmpty:"vide",rpAllOk:"Toutes les cases sont pareilles sur ces lignes.",rpShowAll:"Voir aussi les cases pareilles",rpApply:n=>`Mettre la même chose sur les ${n} lignes`,
  rpDone:(T,n)=>`${T} : ${n} ${pl(n,"case mise","cases mises")} à jour`,rpUndo:"Annuler",rpUndone:"Remis comme avant",rpNot:"Pas le même outil ? Changez le T d’une des lignes.",rpLocked:"Fiche validée : rien ne peut être changé."});
Object.assign(I18N.en,{rpOk:(T,n)=>`${T}: ${n} lines, the same tool everywhere. Click to see.`,rpMiss:(T,L)=>`${T}: some boxes are empty on some lines (${L}). Click to complete.`,
  rpBad:(T,L)=>`${T}: not the same tool on every line (${L}). Click to choose.`,rpTitle:(T,n)=>`${T} · ${n} lines`,rpIntro:"These lines have the same tool number: it is the same tool, used for several operations. For each box that differs, pick the right value; it goes on every line.",
  rpField:"Box",rpLine:i=>`Line ${i}`,rpEmpty:"empty",rpAllOk:"Every box is the same on these lines.",rpShowAll:"Also show the boxes that match",rpApply:n=>`Put the same on the ${n} lines`,
  rpDone:(T,n)=>`${T}: ${n} ${pl(n,"box","boxes")} updated`,rpUndo:"Undo",rpUndone:"Put back as it was",rpNot:"Not the same tool? Change the T of one of the lines.",rpLocked:"Validated sheet: nothing can be changed."});
// the boxes that describe the tool (not the operation): the standard ones, the assembly, and your own columns
const RPSKIP=new Set(["t","op","time","life","asmAuto","_pg"]);
function rpFields(L){const ks=[...IDK,"asm"];L.forEach(x=>Object.keys(x).forEach(k=>{if(k.startsWith("x_")&&!ks.includes(k))ks.push(k)}));
  // only columns that are on the sheet (or hold something)
  let vis=null;try{const c=sheetCfg();vis=new Set(edCols(c));if(vis.has("corr")){vis.add("corrH");vis.add("corrD")}if(typeof asmUnderT==="function"&&asmUnderT(c))vis.add("asm")}catch(_){}
  return ks.filter(k=>!RPSKIP.has(k)&&(!vis||vis.has(k)))}
const rpNorm=(k,v)=>{v=clean(v);if(!v)return"";if(k==="asm")return asmKey(v)||v.toUpperCase();return cmpV(k,String(v).replace(/\n/g," "))};
function rpGroups(tools){const G=new Map();tools.forEach((x,i)=>{if(!clean(x.t)||!realTools([x]).length)return;const k=normT(x.t);if(!G.has(k))G.set(k,[]);G.get(k).push(i)});return G}
function rpState(tools,idx){const L=idx.map(i=>tools[i]),bad=[],miss=[],same=[];
  rpFields(L).forEach(k=>{const v=L.map(x=>rpNorm(k,x[k])),f=v.filter(Boolean);if(!f.length)return;const d=new Set(f).size;if(d>1)bad.push(k);else if(f.length<v.length)miss.push(k);else same.push(k)});return{bad,miss,same}}
const rpLab=k=>k==="corrH"?"H":k==="corrD"?"D":k==="asm"?t("colAsm"):colLabel(k,sheetCfg());
// the dot on the T: blue = same tool everywhere, orange = boxes missing on some lines, red = different values
tDupMark=function(){if(!cur)return;const G=rpGroups(cur.tools),S=new Map();
  document.querySelectorAll("#rows tr[data-i]").forEach(tr=>{const i=+tr.dataset.i,x=cur.tools[i],el=tr.querySelector('input[data-k="t"]');if(!x||!el)return;
    el.classList.remove("warn","opg","opbad");const k=normT(x.t),g=clean(x.t)?G.get(k):null,n=g?g.length:0;const td=el.closest("td");let b=td.querySelector(".tdot");
    tr.classList.toggle("oprow",n>1&&g[0]!==i);
    if(n<2){if(b)b.remove();el.title="";return}
    let st=S.get(k);if(!st){st=rpState(cur.tools,g);S.set(k,st)}
    const cls=st.bad.length?"bad":st.miss.length?"miss":"ok";
    if(!b){b=document.createElement("button");b.type="button";b.className="tdot";td.style.position="relative";td.append(b)}
    b.className="tdot "+cls;b.dataset.tdot=k;const L=cls==="bad"?st.bad.map(f=>`${rpLab(f)} ${[...new Set(g.map(j=>clean(cur.tools[j][f])).filter(Boolean))].map(v=>String(v).replace(/\n/g," ")).join(" / ")}`).join(" · "):st.miss.map(rpLab).join(", ");
    b.title=cls==="bad"?t("rpBad",k,L):cls==="miss"?t("rpMiss",k,L):t("rpOk",k,n);b.setAttribute("aria-label",b.title);el.title=b.title})};
document.addEventListener("click",e=>{const b=e.target.closest&&e.target.closest("#rows .tdot");if(!b||!cur)return;e.preventDefault();e.stopPropagation();rpPanel(b.dataset.tdot)});
{const r0=renderRows;renderRows=function(){const r=r0.apply(this,arguments);try{tDupMark()}catch(_){}return r}}
// the window: one line per box that differs, one column per line; click the right value
function rpPanel(T,showAll){if(!cur)return;const A=cur,G=rpGroups(A.tools),idx=G.get(T);if(!idx||idx.length<2)return;const L=idx.map(i=>A.tools[i]),st=rpState(A.tools,idx),locked=asmLocked(A)||!can("article");
  const ks=showAll?[...st.bad,...st.miss,...st.same]:[...st.bad,...st.miss],pick={};
  ks.forEach(k=>{const cnt=new Map();L.forEach((x,j)=>{const v=rpNorm(k,x[k]);if(v)cnt.set(v,(cnt.get(v)||[]).concat(j))});let best=null;cnt.forEach((js,v)=>{if(!best||js.length>best[1].length)best=[v,js]});pick[k]=best?best[1][0]:-1});
  const show=(k,v)=>{v=clean(v);if(!v)return`<i class="rpe">${esc(t("rpEmpty"))}</i>`;return esc(String(v).replace(/\n/g," · "))};
  const head=L.map((x,j)=>`<th><span>${esc(t("rpLine",idx[j]+1))}</span>${clean(x.op)?`<small>${esc(x.op)}</small>`:""}</th>`).join("");
  const body=ks.map(k=>{const bad=st.bad.includes(k),miss=st.miss.includes(k);return`<tr class="${bad?"b":miss?"m":"s"}" data-rk="${k}"><th>${esc(rpLab(k))}</th>${L.map((x,j)=>{const has=clean(x[k]);
    return`<td>${has&&!locked&&(bad||miss)?`<button type="button" class="rpv${pick[k]===j||rpNorm(k,x[k])===rpNorm(k,L[pick[k]]&&L[pick[k]][k])?" on":""}" data-rj="${j}">${show(k,x[k])}</button>`:`<span class="rpv ro">${show(k,x[k])}</span>`}</td>`}).join("")}</tr>`}).join("");
  const ov=dialog(esc(t("rpTitle",T,L.length)),`<p class="note" style="margin:0 0 10px">${esc(t("rpIntro"))}</p>
    ${ks.length?`<div class="rptw"><table class="rpt"><thead><tr><th>${esc(t("rpField"))}</th>${head}</tr></thead><tbody>${body}</tbody></table></div>`:`<p class="rpok">✓ ${esc(t("rpAllOk"))}</p>`}
    <div class="rpfoot"><label class="chk"><input type="checkbox" id="rp-all" ${showAll?"checked":""}> ${esc(t("rpShowAll"))}</label><span class="dim small">${esc(locked?t("rpLocked"):t("rpNot"))}</span></div>`,
    `<button class="btn ghost" id="rp-no">${esc(t("close"))}</button>${!locked&&(st.bad.length||st.miss.length)?`<button class="btn red" id="rp-go">${esc(t("rpApply",L.length))}</button>`:""}`);
  ov.querySelector(".dlg").classList.add("wide");ov.querySelector(".dlg").style.width="min(860px,96vw)";
  $("#rp-no").onclick=closeDlg;$("#rp-all").onchange=e=>{closeDlg();rpPanel(T,e.target.checked)};
  ov.querySelectorAll(".rpt tr[data-rk]").forEach(tr=>tr.addEventListener("click",e=>{const b=e.target.closest(".rpv[data-rj]");if(!b)return;const k=tr.dataset.rk,j=+b.dataset.rj;pick[k]=j;
    tr.querySelectorAll(".rpv[data-rj]").forEach(o=>o.classList.toggle("on",rpNorm(k,L[+o.dataset.rj][k])===rpNorm(k,L[j][k])))}));
  const go=$("#rp-go");if(go)go.onclick=()=>{if(cur!==A){closeDlg();return}flushEditor();const before=JSON.parse(JSON.stringify(A.tools));let n=0;
    [...st.bad,...st.miss].forEach(k=>{const j=pick[k];if(j==null||j<0)return;const v=L[j][k];L.forEach(x=>{if(String(x[k]||"")!==String(v)){x[k]=v;n++}});if(k==="asm")L.forEach(x=>x.asmAuto=0)});
    closeDlg();renderRows();edited();toast(t("rpDone",T,n),{label:t("rpUndo"),fn:()=>{if(!db.articles.includes(A))return;A.tools=before;edited();if(cur===A)renderRows();toast(t("rpUndone"))}})}}
