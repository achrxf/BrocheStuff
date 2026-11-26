/* ===================== 2.28.0 · Check the sheet: everything that is wrong or missing, with a button to go there ===================== */
Object.assign(I18N.fr,{ckBtn:"Vérifier la fiche",ckBtnN:n=>`Vérifier · ${n}`,ckBtnOk:"Fiche vérifiée",ckBtnT:"Ce qui manque ou ne va pas dans cette fiche, avec un bouton pour y aller",
  ckTitle:"Vérifier la fiche",ckAllOk:"Rien à signaler : la fiche est complète et cohérente.",ckIntro:n=>`${n} ${pl(n,"point à regarder","points à regarder")}. Rien n’est changé sans vous : chaque bouton vous emmène à l’endroit, ou propose la correction.`,
  ckGo:"Y aller",ckFix:"Corriger",ckUse:c=>`Utiliser ${c}`,ckUpd:c=>`Mettre à jour ${c}`,ckSev:{bad:"À corriger",warn:"À vérifier",info:"Pour info"},
  ckArt:L=>`Infos de la fiche : ${L} ${L.includes(",")?"manquent":"manque"}`,ckNoT:i=>`Ligne ${i} : pas de numéro d’outil (T)`,ckMiss:(T,L)=>`${T} : ${L} ${L.includes(",")?"manquent":"manque"}`,
  ckRepBad:(T,n,L)=>`${T} sur ${n} lignes, mais pas le même outil (${L})`,ckRepMiss:(T,n,L)=>`${T} sur ${n} lignes : ${L} ${L.includes(",")?"vides":"vide"} sur certaines`,
  ckAsmDiff:(T,c,L)=>`${T} ne correspond plus à l’assemblage ${c} (${L})`,ckAsmGone:(T,c)=>`${T} : l’assemblage ${c} n’existe pas`,ckAsmSug:(T,c)=>`${T} est identique à l’assemblage ${c}, sans être relié`,
  ckAsmTwoT:(c,L)=>`L’assemblage ${c} est sur plusieurs T dans cette fiche (${L})`,ckCone:(T,c,m)=>`${T} : porte-outil ${c} sur une machine ${m}`,ckCrib:(T,c)=>`${T} : le code ${c} n’est pas dans le magasin`,
  ckTnOther:(T,c,tn,m)=>`${T} : l’assemblage ${c} est d’habitude en ${tn} sur ${m}`,ckVal:n=>`${n} ${pl(n,"point","points")} à regarder avant de valider`,ckValSee:"Voir"});
Object.assign(I18N.en,{ckBtn:"Check the sheet",ckBtnN:n=>`Check · ${n}`,ckBtnOk:"Sheet checked",ckBtnT:"What is missing or wrong in this sheet, with a button to go there",
  ckTitle:"Check the sheet",ckAllOk:"Nothing to report: the sheet is complete and consistent.",ckIntro:n=>`${n} ${pl(n,"thing","things")} to look at. Nothing is changed without you: each button takes you there, or offers the fix.`,
  ckGo:"Go there",ckFix:"Fix",ckUse:c=>`Use ${c}`,ckUpd:c=>`Update ${c}`,ckSev:{bad:"To fix",warn:"To check",info:"For information"},
  ckArt:L=>`Sheet info: ${L} missing`,ckNoT:i=>`Line ${i}: no tool number (T)`,ckMiss:(T,L)=>`${T}: ${L} missing`,
  ckRepBad:(T,n,L)=>`${T} on ${n} lines, but not the same tool (${L})`,ckRepMiss:(T,n,L)=>`${T} on ${n} lines: ${L} empty on some`,
  ckAsmDiff:(T,c,L)=>`${T} no longer matches assembly ${c} (${L})`,ckAsmGone:(T,c)=>`${T}: assembly ${c} does not exist`,ckAsmSug:(T,c)=>`${T} is identical to assembly ${c} but not linked`,
  ckAsmTwoT:(c,L)=>`Assembly ${c} is on several T in this sheet (${L})`,ckCone:(T,c,m)=>`${T}: ${c} holder on a ${m} machine`,ckCrib:(T,c)=>`${T}: code ${c} is not in the crib`,
  ckTnOther:(T,c,tn,m)=>`${T}: assembly ${c} is usually ${tn} on ${m}`,ckVal:n=>`${n} ${pl(n,"thing","things")} to look at before validating`,ckValSee:"See"});
function ckIssues(art){const out=[],tools=art.tools,R=(typeof reqTool==="function"?reqTool(art):[]),mid=art.machineId,mN=asmMName(mid);
  const afl=k=>{const el=$("#a-"+k),l=el&&el.closest("label");const s=l?[...l.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent).join("").trim():"";return s||t(k)||k};
  const am=REQ_ART.filter(k=>!clean(art.article[k]));if(am.length)out.push({sev:"warn",txt:t("ckArt",am.map(afl).join(", ")),go:{af:am[0]}});
  const G0=rpGroups(tools),seenCrib=new Set();
  tools.forEach((x,i)=>{if(!realTools([x]).length)return;const T=normT(x.t)||`L${i+1}`;
    if(!clean(x.t))out.push({sev:"bad",txt:t("ckNoT",i+1),go:{i,k:"t"}});
    // a box empty here but filled on another line with the same T is reported once, with the repeated T
    const sib=clean(x.t)?(G0.get(normT(x.t))||[]).filter(j=>j!==i).map(j=>tools[j]):[];
    const m=R.filter(k=>!clean(x[k])&&!sib.some(y=>clean(y[k])));if(m.length)out.push({sev:"warn",txt:t("ckMiss",T,m.map(k=>colLabel(k)).join(", ")),go:{i,k:m[0]}});
    const v=clean(x.asm);if(v){const a=asmFind(v);if(!a)out.push({sev:"bad",txt:t("ckAsmGone",T,asmKey(v)||v.toUpperCase()),go:{i,k:"asm"}});
      else{const d=asmDiffs(x);if(d&&d.length)out.push({sev:"warn",txt:t("ckAsmDiff",T,a.code,d.map(k=>colLabel(k)).join(", ")),go:{i,k:d[0]},fix:{upd:a.code,i}});
        const tn=asmTn(a)[mid];if(tn&&clean(x.t)&&normT(x.t)!==tn)out.push({sev:"info",txt:t("ckTnOther",T,a.code,tn,mN),go:{i,k:"t"}})}}
    else{try{const L=asmFits(x);if(L.length===1)out.push({sev:"info",txt:t("ckAsmSug",T,L[0].code),go:{i,k:"asm"},fix:{use:L[0].code,i}})}catch(_){}}
    try{const c=coneClash(x.holder);if(c)out.push({sev:"warn",txt:t("ckCone",T,c,normCone(M(mid).cone)),go:{i,k:"holder"}})}catch(_){}
    try{if(clean(x.code)&&(db.catalog||[]).length&&!asmKey(x.code)&&!seenCrib.has(normCode(x.code))&&!C_(x.code)&&seenCrib.add(normCode(x.code)))out.push({sev:"info",txt:t("ckCrib",T,normCode(x.code)),go:{i,k:"code"}})}catch(_){}});
  G0.forEach((idx,T)=>{if(idx.length<2)return;const st=rpState(tools,idx);
    if(st.bad.length)out.push({sev:"bad",txt:t("ckRepBad",T,idx.length,st.bad.map(rpLab).join(", ")),go:{i:idx[0],k:"t"},fix:{rep:T}});
    else if(st.miss.length)out.push({sev:"warn",txt:t("ckRepMiss",T,idx.length,st.miss.map(rpLab).join(", ")),go:{i:idx[0],k:"t"},fix:{rep:T}})});
  const byA=new Map();realTools(tools).forEach(x=>{const a=clean(x.asm)&&asmFind(x.asm);if(!a||!clean(x.t))return;if(!byA.has(a.code))byA.set(a.code,new Set());byA.get(a.code).add(normT(x.t))});
  byA.forEach((s,c)=>{if(s.size>1){const i=tools.findIndex(x=>clean(x.asm)&&asmFind(x.asm)&&asmFind(x.asm).code===c);out.push({sev:"warn",txt:t("ckAsmTwoT",c,[...s].join(", ")),go:{i,k:"t"}})}});
  const W={bad:0,warn:1,info:2},seen=new Set();return out.filter(x=>!seen.has(x.txt)&&seen.add(x.txt)).sort((p,q)=>W[p.sev]-W[q.sev])}
function ckBtnDraw(){if(!cur||route.view!=="article")return;const td=$("#b-ops2")||$("#b-tdtog");if(!td)return;let b=$("#b-chk");
  if(!b){b=document.createElement("button");b.type="button";b.id="b-chk";b.className="btn sm ckbtn";td.before(b)}
  const L=ckIssues(cur),n=L.filter(x=>x.sev!=="info").length,bad=L.some(x=>x.sev==="bad");
  b.className="btn sm ckbtn "+(bad?"bad":n?"warn":"ok");b.innerHTML=`<i aria-hidden="true">${bad||n?"!":"✓"}</i>${esc(n?t("ckBtnN",n):t("ckBtnOk"))}`;b.title=t("ckBtnT")}
let CKT=null;const ckLater=()=>{clearTimeout(CKT);CKT=setTimeout(()=>{try{ckBtnDraw()}catch(_){}},500)};
{const r0=renderEditor;renderEditor=function(){r0.apply(this,arguments);try{ckBtnDraw()}catch(_){}}}
{const e0=edited;edited=function(){const r=e0.apply(this,arguments);ckLater();return r}}
document.addEventListener("click",e=>{if(e.target.closest&&e.target.closest("#b-chk")){flushEditor();ckPanel()}});
function ckGo(g){closeDlg();if(!g)return;if(g.af){const el=$("#a-"+g.af);if(el){el.scrollIntoView({behavior:"smooth",block:"center"});setTimeout(()=>{try{el.focus()}catch(_){}},250)}return}
  const tr=$(`#rows tr[data-i="${g.i}"]`);if(!tr)return;if(edMode!=="saisie")setEdMode("saisie");tr.scrollIntoView({behavior:"smooth",block:"center"});tr.classList.remove("ckflash");void tr.offsetWidth;tr.classList.add("ckflash");
  setTimeout(()=>{const el=tr.querySelector(`[data-k="${g.k}"]:not([disabled])`)||tr.querySelector("input:not([disabled])");if(el)try{el.focus({preventScroll:true})}catch(_){}},300)}
function ckPanel(){if(!cur)return;const A=cur,L=ckIssues(A),locked=asmLocked(A)||!can("article");const n=L.filter(x=>x.sev!=="info").length;
  const sec=s=>{const G=L.filter(x=>x.sev===s);if(!G.length)return"";return`<div class="cks ${s}"><h4>${esc(t("ckSev")[s])} <span>${G.length}</span></h4>${G.map(x=>{const k=L.indexOf(x);
    const fx=x.fix&&!locked?(x.fix.rep?`<button class="btn sm" data-ckfix="${k}">${esc(t("ckFix"))}</button>`:x.fix.use?`<button class="btn sm" data-ckfix="${k}">${esc(t("ckUse",x.fix.use))}</button>`:x.fix.upd?`<button class="btn sm ghost" data-ckfix="${k}">${esc(t("ckUpd",x.fix.upd))}</button>`:""):"";
    return`<div class="cki"><span class="ckd"></span><p>${esc(x.txt)}</p><div class="ckb">${fx}${x.go?`<button class="btn sm ghost" data-ckgo="${k}">${esc(t("ckGo"))}</button>`:""}</div></div>`}).join("")}</div>`};
  const ov=dialog(esc(t("ckTitle")),L.length?`<p class="note" style="margin:0 0 12px">${esc(t("ckIntro",L.length))}</p>${sec("bad")}${sec("warn")}${sec("info")}`:`<p class="rpok">✓ ${esc(t("ckAllOk"))}</p>`,`<button class="btn" id="ck-ok">${esc(t("close"))}</button>`);
  ov.querySelector(".dlg").classList.add("wide");ov.querySelector(".dlg").style.width="min(720px,96vw)";$("#ck-ok").onclick=closeDlg;
  ov.querySelectorAll("[data-ckgo]").forEach(b=>b.onclick=()=>ckGo(L[+b.dataset.ckgo].go));
  ov.querySelectorAll("[data-ckfix]").forEach(b=>b.onclick=()=>{const f=L[+b.dataset.ckfix].fix;if(cur!==A){closeDlg();return}
    if(f.rep){closeDlg();setTimeout(()=>rpPanel(f.rep),60);return}
    if(f.use){const a=asmFind(f.use),x=A.tools[f.i];closeDlg();if(a&&x){x.asm=a.code;x.asmAuto=0;rowFill(f.i,a.tool,ASMF,"asm",a.code)}setTimeout(ckBtnDraw,400);return}
    if(f.upd){const a=asmFind(f.upd),x=A.tools[f.i];closeDlg();if(a&&x)asmUpdateFrom(a,x);setTimeout(ckBtnDraw,400)}})}
// validating: the check is shown in the validation window
{const v0=validateArticle;validateArticle=function(){const r=v0.apply(this,arguments);try{if(!cur)return r;const L=ckIssues(cur).filter(x=>x.sev!=="info");if(!L.length)return r;
  const body=document.querySelector("#ov .dlg .bd")||document.querySelector("#ov .dlg");if(!body)return r;const p=document.createElement("div");p.className="ckval"+(L.some(x=>x.sev==="bad")?" bad":"");
  p.innerHTML=`<span>${esc(t("ckVal",L.length))}</span><button class="btn sm ghost" type="button">${esc(t("ckValSee"))}</button>`;p.querySelector("button").onclick=()=>{closeDlg();setTimeout(ckPanel,60)};
  body.append(p)}catch(_){}return r}}
