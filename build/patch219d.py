import sys
R=[
('''<div class="rowbar"><button class="btn" id="b-add">''','''<div class="rowbar"><div class="rbg"><button class="btn" id="b-add">'''),
('''</select></label><label class="laysel" title="${esc(t("laySelT"))}">''','''</select></label></div><div class="rbg"><label class="laysel" title="${esc(t("laySelT"))}">'''),
('''<button class="btn ghost" id="b-prep" title="${esc(t("prepT"))}">''','''</div><div class="rbg"><button class="btn ghost" id="b-prep" title="${esc(t("prepT"))}">'''),
('''${tplBtn("tools")}<span class="note">${t("excelNote")}</span></div>''','''${tplBtn("tools")}</div><span class="note">${t("excelNote")}</span></div>'''),
('''const DEFW={t:44,''','''const DEFW={t:50,'''),
('''.rowbar .laysel.sortsel select{min-width:0}''','''.rowbar{flex-direction:column;align-items:stretch;gap:8px}
.rowbar .rbg{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.rowbar .rbg+.rbg{padding-top:8px;border-top:1px dashed var(--hair)}
.rowbar .laysel.sortsel{position:relative;padding:0 12px 0 14px;height:36px;cursor:pointer}
.rowbar .laysel.sortsel:hover{border-color:var(--ink)}
.rowbar .laysel.sortsel span{color:var(--ink);font:500 13.5px var(--body);display:inline-flex;align-items:center;gap:6px}
.rowbar .laysel.sortsel span::before{content:"";width:14px;height:14px;background:currentColor;-webkit-mask:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M7 4v16M3 8l4-4 4 4M17 20V4M13 16l4 4 4-4'/%3E%3C/svg%3E") center/contain no-repeat;mask:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M7 4v16M3 8l4-4 4 4M17 20V4M13 16l4 4 4-4'/%3E%3C/svg%3E") center/contain no-repeat}
.rowbar .laysel.sortsel span::after{content:"▾";font-size:11px;color:var(--mid)}
.rowbar .laysel.sortsel select{position:absolute;inset:0;width:100%;height:100%;max-width:none;opacity:0;cursor:pointer}
.asmc{font-size:9px!important;letter-spacing:-.02em;padding:0 3px!important;max-width:100%;overflow:hidden;text-overflow:clip;margin-left:auto!important;margin-right:auto!important}'''),
]
for f in sys.argv[1:]:
  s=open(f).read()
  for a,b in R:
    assert s.count(a)==1,(f,s.count(a),a[:90]);s=s.replace(a,b)
  open(f,'w').write(s);print("patched",f)
