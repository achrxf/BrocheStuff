# BrocheStuff

Tool lists, tool crib and holders for a CNC machining shop: every machine, its articles and their tools in one place, a clean A4 **Fiche outils** for each article, and the stock of every tool code and holder.

| | Open | What it is |
|---|---|---|
| **Web** | [achrxf.github.io/BrocheStuff/Web](https://achrxf.github.io/BrocheStuff/Web/) | The program in the browser. Starts empty; your data stays in your browser. |
| **Demo** | [achrxf.github.io/BrocheStuff/Demo](https://achrxf.github.io/BrocheStuff/Demo/) | The same program filled with a made-up workshop, with a step-by-step tutorial (French / English) linked at the bottom of every page: 20 machines (3, 4 and 5 axes; BT30 / BT40 / BT50 / HSK63), 500 articles, ~500 tool codes, ~130 holders and a month of stock moves. |
| **App** | [App/BrocheStuff-Setup-2.27.5.exe](https://github.com/achrxf/BrocheStuff/raw/main/App/BrocheStuff-Setup-2.27.5.exe) | The Windows program (10/11, 64-bit) with sign-in accounts and a shared data folder. Run the installer (no admin rights needed), then open BrocheStuff from the Start menu; first sign-in **admin / admin**. Portable version: [BrocheStuff-Windows.zip](https://github.com/achrxf/BrocheStuff/raw/main/App/BrocheStuff-Windows.zip). See [`App/README.txt`](App/README.txt). |

The web version has a **Download the app** button at the top right. The demo stands on its own: it has no link to the real version and no download, so it can be shared safely.

## Folders

```
Web/   index.html   the web version (one file, works offline once opened)
Demo/  index.html   the web version with demo data (kept apart from your real data)
App/   BrocheStuff-Setup-2.27.5.exe (installer), BrocheStuff-Windows.zip (portable), README.txt, FOR_IT.txt, checksums
```

## What it does

**Services.** On opening, each person picks a service: *Préparateur méthode* (machines, articles, tool sheets), *Préparateur outil* (tool crib, holders, stock log), *Production* (find a tool, a holder or an article, read the sheet, take a tool out of stock one at a time, leave a comment) or *Admin* (everything). Stock moves are logged with the person's name and time.

**Machines and articles.** Machine cards with spindle taper (BT40 / BT50 / …) and progress; articles with number, index, designation, reference, program, material; the tool list (T, H / D offsets, type, Ø, R / ∠, insert reference, LS, LT, Z, holder, code) with a drawing that explains each box, Excel paste, live **PDF / Excel preview**, **print**, **PDF** and an editable **Excel** file (same look as the PDF, imports back), a **PDF ⇄ Excel** converter, **several lines in any cell** (Shift+Enter), **your own columns** and renamed column titles saved as **layouts** (a default for new sheets, any layout per sheet), and **page / column widths** you drag to size. A holder of the wrong taper for the machine is flagged.

**Operations, and three modes.** A sheet can hold one line per operation: the same T on several lines, with **Operation**, **Time** (12:30 or 02:54:12) and **Tool life** columns ("+ Operation columns" on a sheet, or in a layout). "+" on a line adds an operation for the same tool with its data copied. Repeated T numbers get a blue dot; a red one when the tool data differ between the lines. The sheet has three modes: **Saisie** (everything, one line per operation), **PDF** (one line per tool, times and tool life added up, your order and columns) and **Excel** (every operation with the total at the end, or the same list as the PDF, its own columns and order). Sorting only changes the PDF (and the Excel if you ask). The read-only sheet and the tool prep show one line per tool.

**Look: Atelier or classic, day or night.** The program opens in the **Atelier** look, built from the shop's own language: titles laid out like a drawing title block, the index as a revision triangle, statuses as inspection stamps, progress as tick gauges, locations as bin labels, Archivo for words and IBM Plex Mono for every T, code and size. A **Day / Night** switch sits at the top right (light drafting paper or graphite). The previous look is kept as **Classic look** in the ⋯ menu, one click either way, nothing lost. Motion is used where it explains something (pages coming in, gauges filling, counters, dialogs, the drawer you open) and turns off when the computer asks for reduced motion.

**Cabinet map.** In the tool crib, **List | Cabinet map**: every cabinet drawn from the front with its drawers, built from the locations you already have (`Armoire B - 2B` → cabinet *Armoire B*, drawer *2B*). Each drawer shows how many tools it holds and ▼ when one needs refilling; the crib filters and search light up the drawers concerned. Click a drawer to see its tools, their stock against the minimum, open a tool, print the drawer's label or jump to the list. Tools without a location wait under the map, one click to give them a place.

**Reading a CNC program.** "Read a program" gives every tool change in the program's order, a line per call: a tool used twice gives two lines (two operations), named from the comment written before the tool change (`(CONTOURNAGE EBAUCHE)`, `; PERCAGE`). Compressed blocks (`N30T1M6`, `M06T12`) are read too. The operation columns switch on by themselves, the PDF keeps one line per tool with the times added up.

**Assemblies with their T number per machine.** An assembly (tool + holder, code AS0001…) is no longer made by itself while you type: "Make the assemblies" under a sheet's table makes them for its complete rows, or "+ New assembly" on the Assemblies page. Each assembly keeps its **T number on each machine**: typing its code in a sheet fills the row and the T for that machine; changing the T in a sheet changes the assembly's T for that machine; another machine can have another T. Changing an assembly updates every sheet that uses it (validated sheets keep theirs); changing a linked row offers to update the assembly. "Delete the unused ones" clears the old automatic ones nobody uses.

**Print follows the page.** On a sheet, Print prints the PDF (one line per tool) or the Excel (the rows as in the Excel, repeats included), depending on where you are: the Excel tab, or the Excel preview while typing, prints the Excel; anywhere else the PDF. The button shows PDF or Excel next to it.

**Reading a program into a sheet that is already filled.** The sheet is put in the program's order, a tool used twice gives two lines, and everything you typed (holder, LS, code, Ø, assembly…) is kept and copied onto each repeat; the program only fills empty boxes. Tools that are not in the program stay at the end. A preview shows the result first, and Undo puts the sheet back.

**Everything in capitals.** Types, holders, tool codes, inserts, operations, assembly codes and your own columns are written in CAPITALS as you type, and everything already in the sheets and the crib was put in capitals once (validated sheets keep what was signed). To write as typed instead, switch off "Automatic capitals" in the ⋯ menu; switching it back on puts everything in capitals again.

**Where each tool is.** The tool sheet has a **Location** column filled from the tool crib (and, as an option, the holder's location): by default it sits under the tool code, on the screen, the PDF and the Excel. A tool with no location yet shows "+ location" right in the sheet to add it on the spot. Sheets can be sorted by location, and the tool prep list can be taken out in shop order (by location). Layout options: row height, check boxes for the tool prep (Ready, or Prepared · Mounted).

**Labels and pick list.** The tool crib prints **location labels** (one per shelf or drawer, with the tools and holders kept there) and has a **No location** filter with "+ location" on each line, so the locations are quick to fill in. The tool card shows its location at the top. The tool prep window prints a **pick list** in shop order (by location), with boxes to tick.

**Search everywhere.** Ctrl+K (or the magnifier in the top bar) finds tool codes with their location and stock, sheets (also the ones that use a code), holders, assemblies and machines.

**Tool crib.** Every tool code (your own coding, whatever it is) with its details, sketch or photo, stock with − / +, minimum, history, where it is used, order list (CSV). Coded references (`FR-2T-ALU-D16,00-CAR-R2,000-Z03-LU32-LT100`) fill the card by themselves.

**Holders.** Every holder by taper (BT40 blue, BT50 amber), type, clamping, nose Ø, length, stock and where it is used. References like `PER-50-25-42-130` are read automatically.

**Production.** One search box for codes, holders and articles; the location in big letters, the stock, the tool list and the sheet. Production takes tools out one at a time ("Sortir 1", with a confirmation and the article, undo right after); putting tools back is the tool planner's job. Comments are saved in the stock log, and every log line opens in full.

**Validated sheets and history.** *Validate the sheet* locks it (nothing can be typed) and the PDF shows a green **VALIDATED · date · name** band; unfinished sheets print **IN PROGRESS**. To change a validated sheet, make a **new index** (A → B → C…): the old index stays in the history with its PDF. Only the admin can type an index, and an index already used can't be used again. Every change is kept in the history (who, when, which fields and tools).

**CNC programs and CAM.** Import CNC programs (Fanuc, Haas, Mazak, Okuma, Heidenhain `TOOL CALL`, Siemens; `.nc .tap .min .mpf .h .eia .iso .txt`…): one article per program, with the tool list read from the T numbers, the tool comments and the Mastercam tool table at the top of the program. Tool lists exported from Mastercam or other CAM software (Excel / CSV) and Fusion 360 / Inventor CAM tool libraries (`.json`) can be imported into a sheet. Mastercam's own `.tooldb` files can't be read: export the tool list to Excel/CSV first.

**Machine magazines** (methods and tool planners). What is loaded in each machine now, pocket by pocket, with who changed it. Compare the magazine with an article to see what to load or swap, and load it in one click.

**Reports** (tool planner). Tools taken per month, most-taken tools, per machine and per person, codes used in the most sheets, unused codes, codes that didn't move for 90 days, sheets per machine; export to CSV.

**Stock alert.** When the tool planner logs in, a list of tools and holders out of stock or low comes up right away, with the order list.

**Excel models** — each page has its own (download, preview, print on A4: `1_Machines_Template.xlsx` … `5_Holders_Template.xlsx`) for machines, tool crib, holders, articles and a blank tool sheet to fill by hand. Imports read the columns by their titles (French or English) with a preview first. Every table can be resized like Excel (drag the column edge). French and English (asked the first time, then remembered for each person), light and dark mode.

## Windows program only

- **Accounts:** everyone signs in with a name (or code) and a password. The admin creates the accounts, gives each one a service (several people per service), disables or deletes them, resets passwords, and sees the sign-in log. Passwords are stored as PBKDF2 hashes. Optional automatic sign-out after inactivity.
- **Shared data folder:** the admin chooses where the data live — on the PC, or a network folder shared by several PCs. Changes made at the same time on different PCs are merged (two people taking tools at once are both counted).
- **Administration page:** accounts, data folder, backups, security, sign-in log, program info, and a button to open the demo (made-up data, real data untouched).

## For IT

The Windows installer works per user, needs no admin rights (only the usual HKCU uninstall entry) and the program makes no internet connection; its local window server listens on 127.0.0.1 only and uses a one-time token. Details in [App/FOR_IT.txt](App/FOR_IT.txt), checksums in [App/SHA256SUMS.txt](App/SHA256SUMS.txt).

## Your data

Nothing is sent anywhere.
- **Web:** saved in the browser that uses it. **Sauvegarder / Back up** writes a file; **Restaurer / Restore** reads it on another PC.
- **Windows program:** saved in `Documents\BrocheStuff` with a daily backup copy.
- **Automatic copies:** every 5 minutes, when something changed, a copy is kept (last 24, in the browser or in `Documents\BrocheStuff\Backups\auto`). **Restaurer / Restore** lists them.
- **Demo:** kept separately from the web version, with its own made-up company logo and a **Reset the demo** button.

Each PC keeps its own data: to share one database between several PCs, a shared folder or a small server is the next step.

## Built with

[SheetJS](https://sheetjs.com) · [jsPDF](https://github.com/parallax/jsPDF) · [PDF.js](https://github.com/mozilla/pdf.js) · [Neutralinojs](https://neutralino.js.org) · fonts Barlow Semi Condensed and IBM Plex (SIL Open Font License).

---

## En français

BrocheStuff regroupe les machines CNC, leurs articles et leurs outils, produit une **fiche outils** A4 pour chaque article, et suit le stock des codes outils et des porte-outils.

- **Web** : https://achrxf.github.io/BrocheStuff/Web/ — le programme dans le navigateur, vide au départ.
- **Démo** : https://achrxf.github.io/BrocheStuff/Demo/ — atelier fictif de 20 machines et 500 articles.
- **Programme Windows** : [App/BrocheStuff-Setup-2.27.5.exe](https://github.com/achrxf/BrocheStuff/raw/main/App/BrocheStuff-Setup-2.27.5.exe) — installez-le (sans droits administrateur), ouvrez BrocheStuff depuis le menu Démarrer, première connexion **admin / admin**. Comptes par personne, dossier de données partagé en réseau, page Administration, démo intégrée (voir `README.txt`).

Au démarrage, choisissez votre service : Préparateur méthode, Préparateur outil, Production, ou Accès admin. Les données restent sur l'ordinateur qui les utilise (navigateur, ou `Documents\BrocheStuff` pour le programme). **Sauvegarder / Restaurer** pour les déplacer ; une copie automatique est gardée toutes les 5 minutes.

Nouveau en 2.27 : « Lire un programme » donne tous les outils dans l’ordre des opérations, répétitions comprises ; les assemblages ne se créent plus tout seuls, se modifient vraiment (les fiches suivent) et gardent leur **numéro T par machine**. Les colonnes d’opération ne s’affichent que si vous les demandez (bouton à côté de « Masquer le schéma »). Lire un programme dans une fiche déjà remplie la remet dans l’ordre du programme (répétitions comprises) en gardant tout ce que vous aviez tapé ; les outils absents du programme restent à la fin, et « Annuler » remet la fiche comme avant. « Imprimer » imprime le PDF ou l’Excel selon l’onglet où vous êtes (Excel = les lignes répétées comme dans les opérations).

Nouveau en 2.27.1 : **tout en MAJUSCULES** (types, porte-outils, codes, plaquettes, opérations, vos colonnes), y compris ce qui existait déjà, sauf les fiches validées. Pour écrire comme tapé, désactivez « Majuscules automatiques » dans le menu ⋯.

En 2.26 : l'interface **Atelier** (cartouches de plan, tampons, étiquettes de bac, graduations), un interrupteur **Jour / Nuit**, l'**interface classique** toujours disponible dans le menu ⋯, des animations utiles, et le **plan des armoires** au magasin outils (chaque armoire vue de face, ses tiroirs, leur contenu et leur stock).

Nouveau : fiches **validées** (verrouillées, bande verte sur le PDF, nouvel indice pour modifier, historique des versions), **référence plaquette** et **correcteurs H / D** sur chaque outil (repris des G43 H et G41 / G42 D à la lecture d'un programme), import des **programmes CN** et des listes d'outils **Mastercam / FAO**, **magasins des machines** (poche par poche, comparaison avec un article), **rapports** de consommation, **alerte stock** pour le préparateur outil.
