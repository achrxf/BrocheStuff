import sys
JS=open("/home/claude/w/up2275.js").read()
CSS=r"""
/* 2.27.5: the print button says what it prints */
#b-print .pmode{font:700 10px var(--mono,monospace);letter-spacing:.04em;padding:1px 5px;border:1px solid currentColor;border-radius:2px;opacity:.75;margin-left:2px}
#b-print .pmode.xl{color:#1d6f42;border-color:#1d6f42;opacity:1}
html.at.dark #b-print .pmode.xl,html.dark #b-print .pmode.xl{color:#5fc48c;border-color:#5fc48c}
"""
for f in sys.argv[1:]:
  s=open(f).read();assert "2.27.5: Print follows" not in s
  i=s.find("<style>");j=s.find("</style>",i);s=s[:j]+CSS+s[j:]
  e="\n</script>\n</body></html>";k=s.rfind(e);assert k>0
  s=s[:k]+"\n"+JS+s[k:];open(f,"w").write(s);print("patched",f)
