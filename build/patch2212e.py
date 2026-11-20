import sys
R=[
# history: the PDF button goes before the date, so every date lines up on the right
('''<span class="dim">${when(h.ts)} ${hhmm(h.ts)}${h.snap?` <button class="btn sm" data-hpdf="${i}">${esc(t("hPdf"))}</button>`:""}</span></li>`''','''<span class="dim">${h.snap?`<button class="btn sm" data-hpdf="${i}">${esc(t("hPdf"))}</button> `:""}${when(h.ts)} ${hhmm(h.ts)}</span></li>`'''),
('''.histlist .btn.sm{padding:2px 8px;font-size:11.5px;margin-left:6px}''','''.histlist .btn.sm{padding:2px 8px;font-size:11.5px;margin-right:8px;vertical-align:1px}'''),
# read-only sheet: the status sits with the machine; Preparation sits on the tabs' line
('''<span class="mtag">${esc(mShort(m))}</span>${coneTag(m&&m.cone)}<span>${esc(m?m.name:"")}</span></div>
      <div class="sub" style="margin:0">${esc([a.reference,a.designation].filter(Boolean).join(" · "))}</div>${phRouteHTML(art)}</div></div><span class="sp"></span>
      <span class="ast ast-${s}">${esc(t(s==="done"?"done":s==="progress"?"inProgress":"notStarted"))}</span></div>''','''<span class="mtag">${esc(mShort(m))}</span>${coneTag(m&&m.cone)}<span>${esc(m?m.name:"")}</span><span class="ast ast-${s}">${esc(t(s==="done"?"done":s==="progress"?"inProgress":"notStarted"))}</span></div>
      <div class="sub" style="margin:0">${esc([a.reference,a.designation].filter(Boolean).join(" · "))}</div>${phRouteHTML(art)}</div></div></div>'''),
('''    ${canStock()&&realTools(art.tools).some(x=>clean(x.code))?`<div class="avacts"><button class="btn red" id="av-prep">${esc(t("prep"))}</button></div>`:""}<div class="seg avtabs" role="tablist"><button data-av="list" aria-pressed="${avTab==="list"}">${esc(t("listTab"))}</button><button data-av="pdf" aria-pressed="${avTab==="pdf"}">${esc(t("sheetTab"))}</button><button data-av="ix" aria-pressed="${avTab==="ix"}">${esc(t("ixT"))}</button></div>''','''    <div class="avbar"><div class="seg avtabs" role="tablist"><button data-av="list" aria-pressed="${avTab==="list"}">${esc(t("listTab"))}</button><button data-av="pdf" aria-pressed="${avTab==="pdf"}">${esc(t("sheetTab"))}</button><button data-av="ix" aria-pressed="${avTab==="ix"}">${esc(t("ixT"))}</button></div><span class="sp"></span>${canStock()&&realTools(art.tools).some(x=>clean(x.code))?`<button class="btn red" id="av-prep">${esc(t("prep"))}</button>`:""}</div>'''),
('''/* tables inside small cards wrap instead of scrolling */''','''.avbar{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:4px 0}.avbar .sp{flex:1}.avbar .avtabs{margin:0}
/* number boxes inside tables (preparation quantities…) look like every other box */
.dlg td input.ppq,.dlg td input[type="number"]{width:64px;height:32px;border:1px solid var(--line2);border-radius:7px;background:var(--inbg);color:var(--ink);padding:0 8px;font:600 14px var(--mono)}
.dlg td input.ppq:focus,.dlg td input[type="number"]:focus{outline:none;border-color:var(--red);box-shadow:0 0 0 3px var(--ring)}
.dlg td input.ppq:disabled{opacity:.45}
/* tables inside small cards wrap instead of scrolling */'''),
# the box next to "PDF" over the tool number is the assembly code's: say so
('''${asmUnderT(sheetCfg())?` <input type="checkbox" class="prck" data-pr="asm" ${prOn(cur,"asm")?"checked":""} tabindex="-1" title="${esc(t("prT")+" : "+colLabel("asm"))}">`:""}</th>`''','''${asmUnderT(sheetCfg())?`<label class="asmpr" title="${esc(t("prT")+" : "+colLabel("asm"))}"><input type="checkbox" class="prck" data-pr="asm" ${prOn(cur,"asm")?"checked":""} tabindex="-1">AS</label>`:""}</th>`'''),
('''.tt thead tr.prrow th.prlab .prck{margin-left:4px}''','''.tt thead tr.prrow th.prlab{white-space:nowrap;padding-left:8px!important;padding-right:2px!important;text-overflow:clip!important;font-size:9.5px!important}
.tt thead tr.prrow .asmpr{display:inline-flex;align-items:center;gap:2px;margin-left:4px;font:600 9px/1 var(--mono);color:var(--mid);letter-spacing:0;cursor:pointer;vertical-align:middle}'''),
]
for f in sys.argv[1:]:
  s=open(f).read()
  for a,b in R:
    assert s.count(a)==1,(f,s.count(a),a[:90]);s=s.replace(a,b)
  open(f,'w').write(s);print("patched",f)
