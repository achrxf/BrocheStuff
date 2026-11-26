import sys
JS=open("/home/claude/w/up2274.js").read()
CSS=r"""
/* 2.27.4: read a program into a filled sheet */
.pgtw{max-height:46vh;overflow:auto;border:1px solid var(--hair,#ddd)}
.pgt{width:100%;border-collapse:collapse;font-size:13px}
.pgt th{position:sticky;top:0;background:var(--fill,#f3f1ec);text-align:left;font:700 11px var(--display,inherit);letter-spacing:.05em;text-transform:uppercase;padding:6px 8px;color:var(--mid,#666)}
.pgt td{padding:5px 8px;border-top:1px solid var(--hair,#e5e5e5);vertical-align:top}
.pgt td:first-child{color:var(--mid,#888);font:12px var(--mono,monospace)}
.pgt td b{color:var(--red,#b00);font-family:var(--mono,monospace)}
.pgt tr.kp td{opacity:.65}
.pgt .pgs,.pgt .pgn,.pgt .pgk{font-size:11px;white-space:nowrap;padding:1px 6px;border:1px solid var(--line2,#ccc)}
.pgt .pgn{border-color:#2563eb;color:#2563eb}
.pgt .pgk{border-style:dashed}
.pgo{display:flex;gap:8px;align-items:center;margin-top:10px;font-size:13.5px}
"""
for f in sys.argv[1:]:
  s=open(f).read();assert "2.27.4: read a program into" not in s
  i=s.find("<style>");j=s.find("</style>",i);s=s[:j]+CSS+s[j:]
  e="\n</script>\n</body></html>";k=s.rfind(e);assert k>0
  s=s[:k]+"\n"+JS+s[k:];open(f,"w").write(s);print("patched",f)
