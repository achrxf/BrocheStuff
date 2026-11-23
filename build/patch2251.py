import sys
# 2.25.1: translation fixes + tutorial up to date (locations, labels, pick list, search everywhere, operations and modes)
FR_LOC='''["loc","Emplacements",["La colonne Emplacement de la fiche outils vient du magasin outils : elle s’affiche sous le code (ou dans sa propre colonne), sur le PDF et dans l’Excel. Elle est toujours à jour.","Un outil sans emplacement affiche « + emplacement » sous son code : cliquez, tapez l’étagère ou le tiroir (ou choisissez un emplacement déjà utilisé), et c’est enregistré au magasin pour toutes les fiches. Cliquez sur un emplacement pour le changer.","Magasin outils : le filtre « Sans emplacement » liste ce qu’il reste à ranger, avec « + emplacement » sur chaque ligne. La fiche d’un outil montre son emplacement en haut.","« Étiquettes d’emplacement » (magasin outils) imprime une étiquette par étagère ou tiroir, avec les outils et porte-outils qui y sont rangés.","Préparation : « Par emplacement » met la liste dans l’ordre du magasin et « Imprimer la liste » l’imprime avec des cases à cocher et « Préparé par ». Une option de mise en page ajoute l’emplacement du porte-outil."]],
   ["search","Rechercher partout",["Ctrl+K (ou « Rechercher » en haut) cherche dans tout le programme : codes outils avec leur emplacement et leur stock, fiches outils (même celles qui utilisent un code), porte-outils, assemblages et machines.","↑ ↓ pour choisir, Entrée pour ouvrir, Échap pour fermer. Tapez un emplacement (par exemple « Armoire B ») pour voir ce qui y est rangé."]],
   '''
EN_LOC='''["loc","Locations",["The Location column of the tool sheet comes from the tool crib: it shows under the code (or in its own column), on the PDF and in the Excel, and is always up to date.","A tool with no location shows “+ location” under its code: click it, type the shelf or drawer (or pick one already used) and it is saved in the crib for every sheet. Click a location to change it.","Tool crib: the “No location” filter lists what is left to put away, with “+ location” on each line. A tool’s card shows its location at the top.","“Location labels” (tool crib) prints one label per shelf or drawer, with the tools and holders kept there.","Tool prep: “By location” puts the list in the crib’s order and “Print the list” prints it with boxes to tick and “Prepared by”. A layout option adds the holder’s location."]],
   ["search","Search everywhere",["Ctrl+K (or “Search” at the top) searches the whole program: tool codes with their location and stock, tool sheets (also the ones that use a code), holders, assemblies and machines.","↑ ↓ to choose, Enter to open, Esc to close. Type a location (for example “Cabinet B”) to see what is kept there."]],
   '''
FR_MODES='''["sort","Opérations : Saisie, PDF et Excel",["Une fiche peut avoir une ligne par opération. « + Colonnes d’opération » (sous le tableau) ajoute Opération, Temps et Vie outil à cette fiche ; l’admin peut aussi les mettre dans une mise en page.","Le + bleu au bout d’une ligne ajoute une opération juste dessous, pour le même T, avec les données de l’outil recopiées : il ne reste que l’opération, le temps et la vie outil à taper.","Les temps se tapent 12:30 (min:s) ou 02:54:12 (h:min:s) ; un nombre seul compte en minutes. Un temps mal tapé est entouré de rouge.","Un T utilisé sur plusieurs lignes a un point bleu. Un point rouge veut dire que l’outil n’est pas le même sur toutes ses lignes (passez la souris dessus pour voir ce qui diffère) : le PDF prend la première ligne.","Onglet Saisie : tout ce que vous tapez, dans l’ordre du programme. Onglet PDF : une ligne par outil, temps et vie outil additionnés, l’ordre du PDF (par T, type, Ø, porte-outil, code, emplacement…) et ses colonnes. Trier ne change que le PDF : la saisie garde son ordre (flèches ↑ ↓ pour la changer).","Onglet Excel : toutes les opérations avec le total à la fin, ou la même liste que le PDF ; dans l’ordre de saisie ou comme le PDF, avec ses propres colonnes.","La fiche en lecture seule de la production et la Préparation montrent une ligne par outil."]],
   '''
EN_MODES='''["sort","Operations: Entry, PDF and Excel",["A sheet can have one line per operation. “+ Operation columns” (under the table) adds Operation, Time and Tool life to that sheet; the admin can also put them in a layout.","The blue + at the end of a line adds an operation right below it, for the same T, with the tool’s data copied: only the operation, time and tool life are left to type.","Times are typed 12:30 (min:s) or 02:54:12 (h:min:s); a plain number counts as minutes. A time typed wrong gets a red outline.","A T used on several lines has a blue dot. A red dot means the tool is not the same on all its lines (hover over it to see what differs): the PDF takes the first line.","Entry tab: everything you type, in program order. PDF tab: one line per tool, times and tool life added up, the PDF’s order (by T, type, Ø, holder, code, location…) and its columns. Sorting only changes the PDF: the entry keeps its order (↑ ↓ arrows to change it).","Excel tab: every operation with the total at the end, or the same list as the PDF; in entry order or like the PDF, with its own columns.","Production’s read-only sheet and the tool prep show one line per tool."]],
   '''
R=[
('''function tplRead(tp){
  if(tplCache[tp.f])return tplCache[tp.f];
  const wb=XLSX.read(tplBytes(tp.f),''','''function tplRead(tp){const F=tplF(tp);
  if(tplCache[F])return tplCache[F];
  const wb=XLSX.read(tplBytes(F),'''),
('''return tplCache[tp.f]={head,n,ex,guide,cols};''','''return tplCache[F]={head,n,ex,guide,cols};'''),
('''const g=wb.Sheets["Mode d'emploi"];''','''const g=wb.Sheets["Mode d'emploi"]||wb.Sheets["How to fill it in"];'''),
('''<th class="${tp.req.includes(h)?"req":""}">''','''<th class="${tplReq(tp).includes(h)?"req":""}">'''),
('''esc(tp.req.join(", ")||"—")''','''esc(tplReq(tp).join(", ")||"—")'''),
('''new Blob([tplBytes(tp.f)],''','''new Blob([tplBytes(tplF(tp))],'''),
('''${k!=="t"&&!prOn(cur,k)?" np":""}''','''${k!=="t"&&k!=="op"&&!prOn(cur,k)?" np":""}'''),
('''if(th)th.classList.toggle("np",!c.checked)}prStyle()''','''if(th)th.classList.toggle("np",!c.checked&&k!=="op")}prStyle()'''),
# translations
('''mSaisie:"Saisie",mSaisieT:"Everything you type, one line per operation"''','''mSaisie:"Entry",mSaisieT:"Everything you type, one line per operation"'''),
('''convNoTools:"No tool list found in this file: the table needs titles like Outil, Type, Ø, LS, Porte-outil."''','''convNoTools:"No tool list found in this file: the table needs titles like Tool, Type, Ø, LS, Holder (or the French ones: Outil, Porte-outil)."'''),
('''["Désignation",a.designation]''','''[EN?"Designation":"Désignation",a.designation]'''),
('''locHol:"H",locAdd''','''locHol:"Holder",locAdd'''),
('''(LANG==="fr"?"Prép. Monté":"Prep Set")''','''(LANG==="fr"?"Prép. Monté":"Prep Mount")'''),
# the ⋯ button's tooltip follows the language
('''// "+ operation columns" on one sheet''','''// Excel models: English files in English
function tplF(tp){const e=tp.f.replace(".xlsx","_EN.xlsx");return LANG==="en"&&TPLDATA[e]?e:tp.f}
function tplReq(tp){return LANG==="en"?tp.req.map(x=>({"Abréviation":"Abbreviation","Nom de la machine":"Machine name","Référence":"Reference"})[x]||x):tp.req}
{const c0=chrome;chrome=function(){c0.apply(this,arguments);const b=$("#b-more");if(b)b.title=LANG==="fr"?"Plus d’options":"More options"}}
try{const b=$("#b-more");if(b)b.title=LANG==="fr"?"Plus d’options":"More options"}catch(_){}
// "+ operation columns" on one sheet'''),
# tutorial
(''' Réglage sur la page Admin."]],
   ''',''' Réglage sur la page Admin.","Les titres des colonnes restent en haut quand vous descendez dans une longue fiche ; « Masquer le schéma » laisse plus de place au tableau. Tirez le bord d’un titre pour élargir une colonne : les autres font la place."]],
   '''),
(''' Setting on the Admin page."]],
   ''',''' Setting on the Admin page.","Column titles stay at the top when you scroll down a long sheet; “Hide the drawing” gives the table more room. Drag the edge of a title to widen a column: the others make room."]],
   '''),
('''["holders","Porte-outils",["Chaque porte-outil par cône''',FR_LOC+'''["holders","Porte-outils",["Chaque porte-outil par cône'''),
('''["holders","Holders",["Every holder by taper''',EN_LOC+'''["holders","Holders",["Every holder by taper'''),
('''["sort","Trier une fiche",["Sous le tableau des outils, « Trier » remet les lignes dans l’ordre voulu : numéro T, correcteur, type, Ø, porte-outil, code outil ou LS. Le PDF suit. « Annuler » revient à l’ordre d’avant."]],
   ''',FR_MODES),
('''["sort","Sorting a sheet",["Under the tools table, “Sort” puts the rows in the order you want: T number, corrector, type, Ø, holder, tool code or LS. The PDF follows. “Undo” goes back to the order before."]],
   ''',EN_MODES),
('''La colonne Assemblage n’est pas imprimée par défaut."]],''','''La colonne Assemblage n’est pas imprimée par défaut.","Les onglets PDF et Excel au-dessus du tableau montrent aussi ces cases : l’Excel peut avoir ses propres colonnes, différentes du PDF."]],'''),
('''The Assembly column is not printed by default."]],''','''The Assembly column is not printed by default.","The PDF and Excel tabs above the table show these boxes too: the Excel can have its own columns, different from the PDF."]],'''),
]
import base64,glob,os
EN={os.path.basename(x):base64.b64encode(open(x,"rb").read()).decode() for x in glob.glob("/home/claude/w/tpl_en/*_EN.xlsx")}
assert len(EN)==5
for f in sys.argv[1:]:
  s=open(f).read()
  i=s.find('const TPLDATA={');assert i>0
  s=s[:i]+'const TPLDATA={'+"".join(f'"{k}":"{v}",' for k,v in EN.items())+s[i+len('const TPLDATA={'):]
  for a,b in R:
    assert s.count(a)==1,(f,s.count(a),a[:90]);s=s.replace(a,b)
  open(f,'w').write(s);print("patched",f)
