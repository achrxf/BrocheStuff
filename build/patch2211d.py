import sys
R=[
# Columns window: a renamed title redraws the list after the click that follows (the click and what is being typed are kept)
('''      i.onchange=()=>{if(k.startsWith("x_")&&!i.value.trim()){i.value=buf.extra.find(e=>xKey(e.id)===k)?.label||""}redraw()}});''',
 '''      i.onchange=()=>{if(k.startsWith("x_")&&!i.value.trim()){i.value=buf.extra.find(e=>xKey(e.id)===k)?.label||""}
        const later=()=>{const a=document.activeElement,nv=$("#col-new")?.value||"",fid=a&&a.id,fct=a&&a.dataset&&a.dataset.ct;redraw();
          if($("#col-new"))$("#col-new").value=nv;const back=fid?document.getElementById(fid):fct?document.querySelector(`[data-ct="${fct}"]`):null;if(back&&back.focus)back.focus()};
        if(window.__colPtr)document.addEventListener("pointerup",()=>setTimeout(later,0),{once:true});else setTimeout(later,0)}});'''),
('''/* ---------- 4. reports ---------- */''','''document.addEventListener("pointerdown",()=>{window.__colPtr=1},true);document.addEventListener("pointerup",()=>{setTimeout(()=>{window.__colPtr=0},0)},true);
/* ---------- 4. reports ---------- */'''),
]
for f in sys.argv[1:]:
  s=open(f).read()
  for a,b in R:
    assert s.count(a)==1,(f,s.count(a),a[:80]);s=s.replace(a,b)
  open(f,'w').write(s);print("patched",f)
