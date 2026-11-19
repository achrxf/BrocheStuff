import sys
JS=r'''
/* top bar on computers: the rarely used buttons (theme, language, logo, backup, restore, Windows program) sit in one "⋯" menu;
   on phones they stay in the phone menu as before */
(function(){const top=document.querySelector("header.top"),anchor=document.getElementById("f-restore");if(!top||!anchor)return;
  const wrap=document.createElement("div");wrap.className="topmore";
  wrap.innerHTML=`<button class="tb" id="b-more" aria-haspopup="true" aria-expanded="false"><svg viewBox="0 0 24 24" fill="currentColor"><circle cx="5" cy="12" r="1.9"/><circle cx="12" cy="12" r="1.9"/><circle cx="19" cy="12" r="1.9"/></svg></button><div class="moremenu" id="moremenu" hidden></div>`;
  top.insertBefore(wrap,anchor);
  const mm=wrap.querySelector(".moremenu"),btn=wrap.querySelector("#b-more"),mq=matchMedia("(min-width:761px)");
  const items=()=>["#b-theme",".lang","#b-getapp","#b-logo","#b-backup","#b-restore"].map(s=>top.querySelector(s)).filter(Boolean);
  const place=()=>{const L=items();if(mq.matches)L.forEach(e=>mm.appendChild(e));else L.forEach(e=>top.insertBefore(e,wrap));wrap.hidden=!mq.matches};
  const open=v=>{mm.hidden=!v;btn.setAttribute("aria-expanded",String(v));btn.title=(typeof LANG!=="undefined"&&LANG==="fr")?"Plus d’options":"More options"};
  place();open(false);mq.addEventListener?mq.addEventListener("change",place):mq.addListener(place);
  btn.onclick=e=>{e.stopPropagation();open(mm.hidden)};
  document.addEventListener("click",e=>{if(!mm.hidden&&!e.target.closest("#moremenu"))open(false)});
  mm.addEventListener("click",e=>{if(e.target.closest("#b-getapp,#b-logo,#b-backup,#b-restore"))setTimeout(()=>open(false),0)});
  document.addEventListener("keydown",e=>{if(e.key==="Escape"&&!mm.hidden)open(false)});
})();

/* ---------- 4. reports ---------- */'''
CSS=r'''.top .rolechip .gi svg{width:18px;height:18px}
.topmore{position:relative;display:inline-flex}
.topmore[hidden]{display:none}
.moremenu{position:absolute;right:0;top:calc(100% + 9px);z-index:80;min-width:250px;background:var(--paper);color:var(--ink);border:1px solid var(--hair);border-radius:11px;box-shadow:0 14px 40px rgba(0,0,0,.22);padding:6px;display:flex;flex-direction:column;gap:1px}
.moremenu[hidden]{display:none}
.top .moremenu .tb{display:flex!important;width:100%!important;height:38px!important;min-width:0;justify-content:flex-start!important;gap:10px;padding:0 10px!important;border:0!important;border-radius:7px!important;background:transparent!important;color:var(--ink)!important;font:500 13.5px/1 var(--body)!important;text-decoration:none}
.top .moremenu .tb[hidden]{display:none!important}
.top .moremenu .tb:hover{background:var(--fill)!important}
.top .moremenu .tb svg{width:17px;height:17px;color:var(--mid)}
.top .moremenu .tb .lbl{display:inline!important}
.top .moremenu #b-theme::after{content:attr(aria-label)}
.top .moremenu .lang{display:flex!important;order:-1;height:34px;margin:2px 2px 6px;border:1px solid var(--hair);border-radius:8px;overflow:hidden}
.top .moremenu .lang button{flex:1;padding:0;color:var(--mid)}
.top .moremenu .lang button+button{border-left:1px solid var(--hair)}
.top .moremenu .lang button[aria-pressed="true"]{background:var(--ink);color:var(--paper)}
.top .moremenu #b-theme{order:-1}
.top .moremenu #b-getapp{border-top:1px solid var(--hair)!important;border-radius:0 0 7px 7px!important;margin-top:4px}'''
R=[('''
/* ---------- 4. reports ---------- */''',JS),('''.top .rolechip .gi svg{width:18px;height:18px}''',CSS)]
for f in sys.argv[1:]:
  s=open(f).read()
  for a,b in R:
    assert s.count(a)==1,(f,s.count(a),a[:80]);s=s.replace(a,b)
  open(f,'w').write(s);print("patched",f)
