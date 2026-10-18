# BrocheStuff

Tool lists, tool crib and holders for a CNC machining shop: every machine, its articles and their tools in one place, a clean A4 **Fiche outils** for each article, and the stock of every tool code and holder.

| | Open | What it is |
|---|---|---|
| **Web** | [achrxf.github.io/BrocheStuff/Web](https://achrxf.github.io/BrocheStuff/Web/) | The program in the browser. Starts empty; your data stays in your browser. |
| **Demo** | [achrxf.github.io/BrocheStuff/Demo](https://achrxf.github.io/BrocheStuff/Demo/) | The same program filled with a made-up workshop: 20 machines (3, 4 and 5 axes; BT30 / BT40 / BT50 / HSK63), 500 articles, ~500 tool codes, ~130 holders and a month of stock moves. |
| **App** | [App/BrocheStuff-Setup-2.2.1.exe](https://github.com/achrxf/BrocheStuff/raw/main/App/BrocheStuff-Setup-2.2.1.exe) | The Windows program (10/11, 64-bit) with sign-in accounts and a shared data folder. Run the installer (no admin rights needed), then open BrocheStuff from the Start menu; first sign-in **admin / admin**. Portable version: [BrocheStuff-Windows.zip](https://github.com/achrxf/BrocheStuff/raw/main/App/BrocheStuff-Windows.zip). See [`App/README.txt`](App/README.txt). |

The web version has a **Download the app** button at the top right. The demo stands on its own: it has no link to the real version and no download, so it can be shared safely.

## Folders

```
Web/   index.html   the web version (one file, works offline once opened)
Demo/  index.html   the web version with demo data (kept apart from your real data)
App/   BrocheStuff-Setup-2.2.1.exe (installer), BrocheStuff-Windows.zip (portable), README.txt, FOR_IT.txt, checksums
```

## What it does

**Services.** On opening, each person picks a service: *Préparateur méthode* (machines, articles, tool sheets), *Préparateur outil* (tool crib, holders, stock log), *Production* (find a tool, a holder or an article, read the sheet, take or return a tool, leave a comment) or *Admin* (everything). Stock moves are logged with the person's name and time.

**Machines and articles.** Machine cards with spindle taper (BT40 / BT50 / …) and progress; articles with number, index, designation, reference, program, material; the tool list (T, type, Ø, R / ∠, LS, LT, Z, holder, code) with a drawing that explains each box, Excel paste, live PDF preview, **print** and **PDF**. A holder of the wrong taper for the machine is flagged.

**Tool crib.** Every tool code (your own coding, whatever it is) with its details, sketch or photo, stock with − / +, minimum, history, where it is used, order list (CSV). Coded references (`FR-2T-ALU-D16,00-CAR-R2,000-Z03-LU32-LT100`) fill the card by themselves.

**Holders.** Every holder by taper (BT40 blue, BT50 amber), type, clamping, nose Ø, length, stock and where it is used. References like `PER-50-25-42-130` are read automatically.

**Production.** One search box for codes, holders and articles; the location in big letters, the stock, the tool list and the sheet; comments saved in the stock log.

**Validated sheets and history.** *Validate the sheet* locks it (nothing can be typed) and the PDF shows a green **VALIDATED · date · name** band; unfinished sheets print **IN PROGRESS**. To change a validated sheet, make a **new index** (A → B → C…): the old index stays in the history with its PDF. Only the admin can type an index, and an index already used can't be used again. Every change is kept in the history (who, when, which fields and tools).

**CNC programs and CAM.** Import CNC programs (Fanuc, Haas, Mazak, Okuma, Heidenhain `TOOL CALL`, Siemens; `.nc .tap .min .mpf .h .eia .iso .txt`…): one article per program, with the tool list read from the T numbers, the tool comments and the Mastercam tool table at the top of the program. Tool lists exported from Mastercam or other CAM software (Excel / CSV) and Fusion 360 / Inventor CAM tool libraries (`.json`) can be imported into a sheet. Mastercam's own `.tooldb` files can't be read: export the tool list to Excel/CSV first.

**Machine magazines** (methods and tool planners). What is loaded in each machine now, pocket by pocket, with who changed it. Compare the magazine with an article to see what to load or swap, and load it in one click.

**Reports** (tool planner). Tools taken per month, most-taken tools, per machine and per person, codes used in the most sheets, unused codes, codes that didn't move for 90 days, sheets per machine; export to CSV.

**Stock alert.** When the tool planner logs in, a list of tools and holders out of stock or low comes up right away, with the order list.

**Excel models** (download, preview, print on A4: `1_Machines_Template.xlsx` … `5_Holders_Template.xlsx`) for machines, tool crib, holders, articles and a blank tool sheet to fill by hand. Imports read the columns by their titles (French or English) with a preview first. Every table can be resized like Excel (drag the column edge). French and English (asked the first time, then remembered for each person), light and dark mode.

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
- **Programme Windows** : [App/BrocheStuff-Setup-2.2.1.exe](https://github.com/achrxf/BrocheStuff/raw/main/App/BrocheStuff-Setup-2.2.1.exe) — installez-le (sans droits administrateur), ouvrez BrocheStuff depuis le menu Démarrer, première connexion **admin / admin**. Comptes par personne, dossier de données partagé en réseau, page Administration, démo intégrée (voir `README.txt`).

Au démarrage, choisissez votre service : Préparateur méthode, Préparateur outil, Production, ou Accès admin. Les données restent sur l'ordinateur qui les utilise (navigateur, ou `Documents\BrocheStuff` pour le programme). **Sauvegarder / Restaurer** pour les déplacer ; une copie automatique est gardée toutes les 5 minutes.

Nouveau : fiches **validées** (verrouillées, bande verte sur le PDF, nouvel indice pour modifier, historique des versions), import des **programmes CN** et des listes d'outils **Mastercam / FAO**, **magasins des machines** (poche par poche, comparaison avec un article), **rapports** de consommation, **alerte stock** pour le préparateur outil.
