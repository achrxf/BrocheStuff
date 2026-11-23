import sys,re,base64
# 2.26.0: Atelier interface (default) + classic interface kept one click away, day/night switch,
# motion everywhere (page entrance, rows, gauges, dialogs, counters), and the cabinet map in the tool crib.
W="/home/claude/w/"
CSS=open(W+"atelier.css").read()
JS=open(W+"atelier.js").read()
F="/tmp/fonts/"
arch=base64.b64encode(open(F+"fontsource-variable-archivo-5.3.0/files/archivo-latin-wdth-normal.woff2","rb").read()).decode()
grenze=base64.b64encode(open(F+"fontsource-grenze-gotisch-5.3.0/files/grenze-gotisch-latin-700-normal.woff2","rb").read()).decode()
FONTS=('@font-face{font-family:"ArchivoV";font-style:normal;font-weight:100 900;font-stretch:62% 125%;font-display:swap;src:url(data:font/woff2;base64,'+arch+') format("woff2")}\n'
       '@font-face{font-family:"Grenze";font-style:normal;font-weight:700;font-display:swap;src:url(data:font/woff2;base64,'+grenze+') format("woff2")}\n')


GFR='''["look","Nouvelle interface, jour et nuit",["BrocheStuff s’ouvre dans l’interface Atelier : les titres comme un cartouche de plan, les états en tampons, les emplacements comme des étiquettes de bac, l’avancement en graduations.","« Jour / Nuit » en haut à droite : papier clair le jour, graphite la nuit. Le choix est gardé pour la prochaine fois.","L’ancienne interface reste là : menu ⋯ → « Interface classique ». Le même menu ramène à la nouvelle. Rien n’est perdu en changeant.","Magasin outils → « Plan des armoires » : chaque armoire vue de face avec ses tiroirs. Cliquez un tiroir pour voir ses outils et leur stock ; ▼ veut dire qu’un outil du tiroir est à recompléter. Les filtres (stock bas, rupture, recherche) éclairent les tiroirs concernés.","Les outils sans emplacement sont listés sous le plan : cliquez un code pour lui donner sa place. « Imprimer l’étiquette » imprime l’étiquette du tiroir choisi."]],
   '''
GEN='''["look","New look, day and night",["BrocheStuff opens in the Atelier look: titles like a drawing title block, statuses as stamps, locations as bin labels, progress as tick marks.","“Day / Night” at the top right: light paper by day, graphite at night. The choice is kept for next time.","The old look is still there: ⋯ menu → “Classic look”. The same menu brings the new one back. Nothing is lost when you switch.","Tool crib → “Cabinet map”: every cabinet seen from the front with its drawers. Click a drawer to see its tools and their stock; ▼ means a tool in that drawer needs refilling. The filters (low stock, out of stock, search) light up the drawers concerned.","Tools without a location are listed under the map: click a code to give it its place. “Print the label” prints the chosen drawer’s label."]],
   '''

def top_rules(css):
  """top-level rules only (skip @media / @keyframes blocks)"""
  out=[];i=0;n=len(css)
  while i<n:
    j=css.find("{",i)
    if j<0:break
    sel=css[i:j].strip()
    if sel.startswith("@"):
      d=0;k=j
      while k<n:
        if css[k]=="{":d+=1
        elif css[k]=="}":
          d-=1
          if d==0:break
        k+=1
      i=k+1;continue
    k=css.find("}",j);out.append((sel,css[j+1:k]));i=k+1
  return out
def prefix(sel):
  r=[]
  for s in sel.split(","):
    s=s.strip()
    if not s:continue
    s=re.sub(r"/\*.*?\*/","",s).strip()
    if s.startswith(":root"):r.append(":root.at"+s[5:])
    elif s.startswith("html"):r.append("html.at"+s[4:])
    else:r.append("html.at "+s)
  return ",".join(r)

def generated(appcss):
  css=re.sub(r"/\*.*?\*/","",re.sub(r"url\(data:[^)]*\)","url()",appcss),flags=re.S)
  rad=[];disp=[]
  for sel,body in top_rules(css):
    if "@font-face" in sel or not sel:continue
    m=re.search(r"border-radius:\s*([0-9.]+)px(?:\s+[0-9.]+px){0,3}\s*(?:;|$)",body)
    if m and 3<=float(m.group(1))<=16:rad.append(prefix(sel))
    if "var(--display" in body:disp.append(prefix(sel))
  return ("/* generated: square corners and condensed titles for every component */\n"
    +"".join(s+"{border-radius:2px}\n" for s in rad)
    +"".join(s+"{font-stretch:76%}\n" for s in disp))

for f in sys.argv[1:]:
  s=open(f).read()
  assert "ATELIER skin (2.26)" not in s,"already patched "+f
  i=s.find("<style>");j=s.find("</style>",i);assert 0<i<j<1000000
  gen=generated(s[i:j])
  s=s[:j]+"\n"+FONTS+gen+CSS+"\n"+s[j:]
  # class set before anything paints
  a="<body>\n<header class=\"top\">"
  assert s.count(a)==1
  s=s.replace(a,"<body>\n<script>try{if(localStorage.getItem(\"bs.skin\")!==\"classic\")document.documentElement.classList.add(\"at\")}catch(e){document.documentElement.classList.add(\"at\")}</script>\n<header class=\"top\">")
  a='const items=()=>["#b-theme",".lang",'
  assert s.count(a)==1,(f,s.count(a))
  s=s.replace(a,'const items=()=>["#b-theme","#b-skin",".lang",')
  e="})();\n</script>\n</body></html>"
  assert s.endswith(e+"\n") or s.endswith(e),f
  k=s.rfind(e)
  s=s[:k]+"})();\n"+JS+"\n</script>\n</body></html>\n"
  a='function asmCopy(code){try{navigator.clipboard.writeText(code)}catch(e){}'
  assert s.count(a)==1,(f,"asmCopy")
  s=s.replace(a,'function asmCopy(code){try{const q=navigator.clipboard&&navigator.clipboard.writeText(code);if(q&&q.catch)q.catch(()=>{})}catch(e){}')
  for a,g in [('["search","Rechercher partout",[',GFR),('["search","Search everywhere",[',GEN)]:
    assert s.count(a)==1,(f,a);s=s.replace(a,g+a)
  open(f,"w").write(s);print("patched",f,"rad/disp rules:",gen.count("border-radius"),gen.count("font-stretch"))
