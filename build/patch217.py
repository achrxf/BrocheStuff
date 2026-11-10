import sys
R=[
# --- the dialog: sort option + duplicate review before importing tools ---
('''  let si=0,hdr,map,mode="add";''','''  let si=0,hdr,map,mode="add",sortT=false;try{sortT=localStorage.getItem("bs.impsort")==="1"}catch(e){}'''),
('''      <h4 class="imph">${esc(t("impMap"))}</h4>''','''      ${kind==="tools"||kind==="articles"?`<label class="chk"><input type="checkbox" id="imp-sort" ${sortT?"checked":""}> ${esc(t("impSortT"))}</label>`:""}
      <h4 class="imph">${esc(t("impMap"))}</h4>'''),
('''    $("#impbody").querySelectorAll("[data-mode]").forEach(b=>b.onclick=()=>{mode=b.dataset.mode;draw()});
  };''','''    $("#impbody").querySelectorAll("[data-mode]").forEach(b=>b.onclick=()=>{mode=b.dataset.mode;draw()});
    $("#imp-sort")&&($("#imp-sort").onchange=e=>{sortT=e.target.checked;try{localStorage.setItem("bs.impsort",sortT?"1":"0")}catch(x){}});
  };'''),
('''    const rows=dataRows();if(!rows.length){err(t("impEmpty"));return}
    const r=applyImport(kind,ctx,rows,val,mode,err);if(!r)return;''','''    const rows=dataRows();if(!rows.length){err(t("impEmpty"));return}
    ctx.sortT=sortT;
    // tool sheet: the same tool twice (in the file, or already on the sheet) → ask which to keep
    if(kind==="tools"&&!ctx.plan){const groups=impDupGroups(mode==="replace"?[]:cur.tools,rows,val,hdr);
      if(groups.length){impDupStep(groups,()=>{ctx.plan=groups;$("#d-imp").onclick=go;go()},()=>{draw();$("#d-imp").onclick=go});return}}
    const r=applyImport(kind,ctx,rows,val,mode,err);delete ctx.plan;if(!r)return;'''),
('''  $("#d-imp").onclick=()=>{
    const err=m=>{const e=$("#imp-err");''','''  const go=$("#d-imp").onclick=()=>{
    const err=m=>{const e=$("#imp-err");if(!e){toast(m);return}'''),
# --- applying ---
('''  if(kind==="tools"){
    const list=rows.map(toolOf).filter(hasTool);
    list.forEach((x,i)=>{if(!x.t)x.t="T"+String(i+1).padStart(2,"0")});
    if(mode==="replace")cur.tools=list.length?list:[{t:"T01"}];
    else{cur.tools=cur.tools.filter(x=>hasTool(x));let n=cur.tools.length;list.forEach(x=>{if(!x.t)x.t="T"+String(++n).padStart(2,"0")});cur.tools.push(...list);if(!cur.tools.length)cur.tools=[{t:"T01"}]}
    return t("impDoneTools",list.length);
  }''','''  if(kind==="tools"){
    const base=mode==="replace"?[]:cur.tools.filter(x=>hasTool(x));
    const list=rows.map(toolOf).map((x,i)=>hasTool(x)?x:null);
    // the user's choices for the doubles: keep one copy (in the place of the first) or keep them all
    let dropped=0;
    if(ctx.plan){const all=[...base.map((x,i)=>({x,s:"sheet",i})),...list.map((x,i)=>({x,s:"file",i}))];
      ctx.plan.forEach(g=>{if(g.choice===-1)return;const keep=g.copies[g.choice],first=g.copies[0];
        g.copies.forEach(c=>{if(c===first)return;(c.src==="sheet"?base:list)[c.i]=null;dropped++});
        (first.src==="sheet"?base:list)[first.i]=keep.tool})}
    const got=list.filter(Boolean),keepB=base.filter(Boolean);let n=keepB.length;
    got.forEach(x=>{if(!x.t)x.t="T"+String(++n).padStart(2,"0")});
    let out=[...keepB,...got];
    if(ctx.sortT)out=sortByT(out);
    cur.tools=out.length?out:[{t:"T01"}];
    return t("impDoneTools",got.length)+(dropped?" · "+t("impDupOut",dropped):"");
  }'''),
('''    db.articles.forEach(a=>{if(touched.has(a.id)){if(!a.tools.length)a.tools=[{t:"T01"}];delete a._new;delete a._keepTools}});''','''    db.articles.forEach(a=>{if(touched.has(a.id)){if(ctx.sortT&&!a._keepTools)a.tools=sortByT(a.tools);if(!a.tools.length)a.tools=[{t:"T01"}];delete a._new;delete a._keepTools}});'''),
('''/* applying the rows */''','''/* tools in T order (T1, T2 … T10); tools without a number keep their place at the end */
const tNum=v=>{const m=/^\\s*T?\\s*0*(\\d+)/i.exec(String(v||""));return m?+m[1]:null};
function sortByT(list){return list.map((x,i)=>({x,i,n:tNum(x.t)})).sort((a,b)=>(a.n==null)-(b.n==null)||(a.n-b.n)||(a.i-b.i)).map(o=>o.x)}
/* the same tool more than once: same T number (T5 = T05), or the very same row when there is no T */
function impDupGroups(sheetTools,rows,val,hdr){
  const real=x=>COLS.some(k=>k!=="t"&&clean(x[k]));
  const tool=r=>{const x={};TOOLF.forEach(([f])=>{const v=val(r,f);if(v)x[f]=v});return x};
  const key=x=>{const n=tNum(x.t);if(clean(x.t)&&n!=null)return "T"+n;return "="+JSON.stringify(TOOLF.map(([f])=>clean(x[f]).toLowerCase()))};
  const G=new Map(),add=(c)=>{const k=key(c.tool);if(!G.has(k))G.set(k,[]);G.get(k).push(c)};
  sheetTools.forEach((x,i)=>{if(real(x))add({src:"sheet",i,tool:x})});
  rows.forEach((r,i)=>{const x=tool(r);if(real(x))add({src:"file",i,row:hdr+2+i,tool:x})});
  const same=cs=>cs.every(c=>TOOLF.every(([f])=>clean(c.tool[f]).toLowerCase()===clean(cs[0].tool[f]).toLowerCase()));
  return [...G.entries()].filter(([,cs])=>cs.length>1).map(([k,cs])=>({label:k[0]==="="?(clean(cs[0].tool.code)||clean(cs[0].tool.type)||"—"):"T"+String(+k.slice(1)).padStart(2,"0"),copies:cs,same:same(cs),choice:0,n:k[0]==="T"?+k.slice(1):1e9})).sort((a,b)=>a.n-b.n)}
function impDupStep(groups,done,back){
  const ft=$(".dlg .ft");const oldFt=ft.innerHTML;
  const draw=()=>{
    $("#impbody").innerHTML=`<h4 class="imph">${esc(t("dupT",groups.length))}</h4><p class="note" style="margin:0">${esc(t("dupP"))}</p>
      <div class="admact"><button class="btn" id="dup-one">${esc(t("dupOneAll"))}</button><button class="btn ghost" id="dup-all">${esc(t("dupAllAll"))}</button></div>
      <div class="duplist">${groups.map((g,gi)=>{const F=TOOLF.filter(([f])=>g.copies.some(c=>clean(c.tool[f])));
        const dif=f=>new Set(g.copies.map(c=>f==="t"&&tNum(c.tool.t)!=null?tNum(c.tool.t):clean(c.tool[f]).toLowerCase())).size>1;
        return `<div class="dupg"><div class="duph"><b>${esc(g.label)}</b><span class="dtag ${g.same?"same":"diff"}">${esc(g.same?t("dupSame",g.copies.length):t("dupDiff",F.filter(([f])=>dif(f)).map(([,l])=>t(l)).join(", ")))}</span></div>
          <div class="tw"><table class="lt duptab"><thead><tr><th></th>${F.map(([f,l])=>`<th class="${dif(f)?"dif":""}">${esc(t(l))}</th>`).join("")}</tr></thead><tbody>
          ${g.copies.map((c,ci)=>`<tr class="${g.choice===-1||g.choice===ci?"keep":"drop"}"><td><label class="chk"><input type="radio" name="dup${gi}" data-g="${gi}" value="${ci}" ${g.choice===ci?"checked":""}> ${esc(c.src==="sheet"?t("dupOnSheet"):t("dupInFile",c.row))}</label></td>${F.map(([f])=>`<td class="${dif(f)?"dif":""}">${esc(clean(c.tool[f])||"—")}</td>`).join("")}</tr>`).join("")}
          </tbody></table></div>
          <label class="chk"><input type="radio" name="dup${gi}" data-g="${gi}" value="-1" ${g.choice===-1?"checked":""}> ${esc(t("dupKeepAll",g.copies.length))}</label></div>`}).join("")}</div>`;
    $("#impbody").querySelectorAll("input[data-g]").forEach(r=>r.onchange=()=>{groups[+r.dataset.g].choice=+r.value;draw()});
    $("#dup-one").onclick=()=>{groups.forEach(g=>g.choice=0);draw()};$("#dup-all").onclick=()=>{groups.forEach(g=>g.choice=-1);draw()};
    const n=groups.reduce((s,g)=>s+(g.choice===-1?0:g.copies.length-1),0);$("#dup-go").textContent=n?t("dupGo",n):t("dupGoAll");
  };
  ft.innerHTML=`<button class="btn ghost" id="dup-back">${esc(t("back"))}</button><button class="btn red" id="dup-go"></button>`;
  $("#dup-back").onclick=()=>{ft.innerHTML=oldFt;$("#d-cancel").onclick=closeDlg;back()};
  $("#dup-go").onclick=()=>{ft.innerHTML=oldFt;$("#d-cancel").onclick=closeDlg;done()};
  draw();$(".dlg .bd").scrollTop=0}

/* applying the rows */'''),
# --- texts ---
('impAdd:"Add to the list",','impSortT:"Put the tools in T order (T1, T2, T3…)", dupT:n=>`${n} ${pl(n,"tool appears","tools appear")} more than once`, dupP:"For each one, choose the copy to keep, or keep them all. Boxes that differ between the copies are highlighted.", dupOneAll:"Keep one of each", dupAllAll:"Keep everything", dupSame:n=>`${n} identical copies`, dupDiff:s=>`Differs: ${s}`, dupOnSheet:"Already on the sheet", dupInFile:n=>`File, row ${n}`, dupKeepAll:n=>`Keep all ${n}`, dupGo:n=>`Import without ${n} ${pl(n,"double","doubles")}`, dupGoAll:"Import everything", impDupOut:n=>`${n} ${pl(n,"double","doubles")} left out`, impAdd:"Add to the list",'),
('impAdd:"Ajouter à la liste",','impSortT:"Mettre les outils dans l’ordre T (T1, T2, T3…)", dupT:n=>`${n} ${pl(n,"outil apparaît","outils apparaissent")} plusieurs fois`, dupP:"Pour chacun, choisissez la copie à garder, ou gardez tout. Les cases qui diffèrent entre les copies sont surlignées.", dupOneAll:"Garder un seul de chaque", dupAllAll:"Tout garder", dupSame:n=>`${n} copies identiques`, dupDiff:s=>`Diffère : ${s}`, dupOnSheet:"Déjà sur la fiche", dupInFile:n=>`Fichier, ligne ${n}`, dupKeepAll:n=>`Garder les ${n}`, dupGo:n=>`Importer sans ${n} ${pl(n,"double","doubles")}`, dupGoAll:"Tout importer", impDupOut:n=>`${n} ${pl(n,"double écarté","doubles écartés")}`, impAdd:"Ajouter à la liste",'),
# --- style ---
('''#impbody{display:flex;flex-direction:column;gap:10px}''','''#impbody{display:flex;flex-direction:column;gap:10px}
.duplist{display:flex;flex-direction:column;gap:12px}
.dupg{border:1px solid var(--hair);border-radius:10px;padding:10px 12px;display:flex;flex-direction:column;gap:8px}
.duph{display:flex;align-items:center;gap:10px;flex-wrap:wrap}.duph b{font-size:15px}
.dtag{font-size:12px;padding:2px 8px;border-radius:99px}.dtag.same{background:var(--fill);color:var(--mid)}.dtag.diff{background:var(--low-bg);color:var(--low-ink)}
.duptab td,.duptab th{padding:6px 9px;font-size:13px;white-space:nowrap}
.duptab td.dif,.duptab th.dif{background:var(--low-bg);color:var(--low-ink);font-weight:600}
.duptab tr.drop td{opacity:.45;text-decoration:line-through}.duptab tr.drop td:first-child{text-decoration:none}'''),
]
for f in sys.argv[1:]:
  s=open(f).read()
  for a,b in R:
    assert s.count(a)==1,(f,s.count(a),a[:90])
    s=s.replace(a,b)
  open(f,'w').write(s);print("patched",f)
