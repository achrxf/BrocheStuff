/* ===================== 2.27.4: read a program into a sheet that already has its tools ===================== */
Object.assign(I18N.fr,{pgT:"Lire le programme dans cette fiche",
  pgIntro:(n,p)=>`Cette fiche a déjà ${n} ${pl(n,"outil","outils")}. Le programme fait ${p} ${pl(p,"changement d’outil","changements d’outil")}.`,
  pgHow:"Les lignes sont remises dans l’ordre du programme, un outil utilisé deux fois donne deux lignes. Ce que vous avez déjà tapé (porte-outil, LS, code, Ø, assemblage…) est gardé et recopié sur chaque répétition ; le programme ne remplit que les cases vides.",
  pgKeep:n=>`${n} ${pl(n,"outil de la fiche n’est pas","outils de la fiche ne sont pas")} dans le programme : ${pl(n,"gardé","gardés")} à la fin.`,
  pgFrom:"de la fiche",pgNew:"nouveau (programme)",pgKept:"pas dans le programme",
  pgOps:"Afficher les noms d’opération",pgGo:"Suivre le programme",pgOther:"Autres choix (ajouter / remplacer)…",
  pgDone:(n,k)=>`${n} ${pl(n,"ligne","lignes")} dans l’ordre du programme${k?` · ${k} ${pl(k,"outil gardé","outils gardés")} à la fin`:""}`,pgUndo:"Annuler",pgUndone:"Fiche remise comme avant"});
Object.assign(I18N.en,{pgT:"Read the program into this sheet",
  pgIntro:(n,p)=>`This sheet already has ${n} ${pl(n,"tool","tools")}. The program has ${p} ${pl(p,"tool change","tool changes")}.`,
  pgHow:"The lines are put in the program's order; a tool used twice gives two lines. What you already typed (holder, LS, code, Ø, assembly…) is kept and copied onto every repeat; the program only fills empty boxes.",
  pgKeep:n=>`${n} ${pl(n,"tool of the sheet is","tools of the sheet are")} not in the program: kept at the end.`,
  pgFrom:"from the sheet",pgNew:"new (program)",pgKept:"not in the program",
  pgOps:"Show the operation names",pgGo:"Follow the program",pgOther:"Other choices (add / replace)…",
  pgDone:(n,k)=>`${n} ${pl(n,"line","lines")} in the program's order${k?` · ${k} ${pl(k,"tool","tools")} kept at the end`:""}`,pgUndo:"Undo",pgUndone:"Sheet put back as it was"});
// the sheet's lines in the program's order: sheet data wins, the program fills the gaps and names the operation
function pgMerge(tools,seq){const have=realTools(tools),byT=new Map();have.forEach(x=>{const k=normT(x.t);if(!byT.has(k))byT.set(k,[]);byT.get(k).push(x)});
  const used=new Set(),out=[],inProg=new Set();
  seq.forEach(p=>{const k=normT(p.t);inProg.add(k);const list=byT.get(k)||[];let src=list.find(x=>!used.has(x));if(src)used.add(src);const base=src||list[0];
    let line;if(base){line=JSON.parse(JSON.stringify(base));Object.keys(p).forEach(f=>{if(f==="t"||f==="op")return;if(!clean(line[f])&&clean(p[f]))line[f]=p[f]});if(clean(p.op))line.op=p.op;line._pg=src?"sheet":"copy"}
    else{line={...p};line._pg="new"}
    out.push(line)});
  const kept=have.filter(x=>!used.has(x)&&!inProg.has(normT(x.t))).map(x=>({...JSON.parse(JSON.stringify(x)),_pg:"kept"}));
  return{lines:[...out,...kept],kept:kept.length}}
function pgDialog(sheet,ctx,fname,sheets,goOther){const A=cur,seq=sheet.nc.seqTools,have=realTools(A.tools),M0=pgMerge(A.tools,seq);
  const tag=x=>x._pg==="new"?`<span class="pgn">${esc(t("pgNew"))}</span>`:x._pg==="kept"?`<span class="pgk">${esc(t("pgKept"))}</span>`:`<span class="pgs">${esc(t("pgFrom"))}</span>`;
  const rows=M0.lines.map((x,i)=>`<tr${x._pg==="kept"?' class="kp"':""}><td>${i+1}</td><td><b>${esc(x.t||"")}</b></td><td>${esc(x.op||"")}</td><td>${esc([x.type,x.diameter?"Ø"+x.diameter:""].filter(Boolean).join(" "))}</td><td>${esc(linesOf_(x.holder||"")[0]||"")}</td><td>${tag(x)}</td></tr>`).join("");
  const ov=dialog(esc(t("pgT")),`<p style="margin:0 0 6px">${esc(t("pgIntro",have.length,seq.length))}</p><p class="note" style="margin:0 0 10px">${esc(t("pgHow"))}</p>
    ${M0.kept?`<p class="note" style="margin:0 0 10px;color:var(--warn,#b45309)">${esc(t("pgKeep",M0.kept))}</p>`:""}
    <div class="pgtw"><table class="pgt"><thead><tr><th>#</th><th>T</th><th>${esc(t("colOp"))}</th><th>${esc(LANG==="fr"?"Outil":"Tool")}</th><th>${esc(LANG==="fr"?"Porte-outil":"Holder")}</th><th></th></tr></thead><tbody>${rows}</tbody></table></div>
    <label class="pgo"><input type="checkbox" id="pg-ops"> ${esc(t("pgOps"))}</label>`,
    `<button class="btn ghost" id="pg-other">${esc(t("pgOther"))}</button><span style="flex:1"></span><button class="btn ghost" id="pg-no">${esc(t("cancel"))}</button><button class="btn red" id="pg-go">${esc(t("pgGo"))}</button>`);
  ov.querySelector(".dlg").classList.add("wide");ov.querySelector(".dlg").style.width="min(760px,96vw)";
  $("#pg-no").onclick=closeDlg;$("#pg-other").onclick=()=>{closeDlg();goOther()};
  $("#pg-go").onclick=()=>{if(cur!==A){closeDlg();return}flushEditor();const before=JSON.parse(JSON.stringify(A.tools)),opsBefore=A.ops;
    A.tools=M0.lines.map(x=>{const y={...x};delete y._pg;try{if(upOn())upTool(y)}catch(_){}return y});if(!A.tools.length)A.tools=[{t:"T01"}];
    if($("#pg-ops").checked)A.ops=true;
    const nc=sheet.nc;if(nc&&nc.program&&!clean(A.article.program)){A.article.program=nc.program}
    closeDlg();edited();try{refreshCols(A)}catch(_){}renderEditor(A);try{asmLater()}catch(_){}
    toast(t("pgDone",M0.lines.length-M0.kept,M0.kept),{label:t("pgUndo"),fn:()=>{if(!db.articles.includes(A))return;A.tools=before;if(opsBefore===undefined)delete A.ops;else A.ops=opsBefore;edited();try{refreshCols(A)}catch(_){}if(cur===A)renderEditor(A);toast(t("pgUndone"))}})}}
{const d0=importDialog;importDialog=function(kind,ctx,fname,sheets){const a=arguments,self=this;
  try{const s=sheets&&sheets.find(x=>x.nc&&x.nc.seqTools&&x.nc.seqTools.length);
    if(kind==="tools"&&ctx&&!ctx.plan&&s&&cur&&route.view==="article"&&realTools(cur.tools).length&&!asmLocked(cur)){pgDialog(s,ctx,fname,sheets,()=>d0.apply(self,a));return}}catch(e){console.error(e)}
  return d0.apply(this,arguments)}}
