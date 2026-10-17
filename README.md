# Tool Manager · Tool List Maker

**Try it in your browser (nothing to install):**
### 👉 https://achrxf.github.io/ToolManager/WebVersion-Demo/

**Windows program:** [Program/ToolListMaker-Windows.zip](Program/ToolListMaker-Windows.zip)

---

Tool Manager keeps every CNC machine, its articles and their tools in one place, and prints a clean **tool list sheet** (A4 PDF) for each article. A **tool crib** keeps every tool code (F… / M…) with its details and stock.

Built for a machining shop where articles had no tool lists: one place per machine, one sheet per article, and tool prep can see what is on the shelf.

## What it does

**Machines and articles**
- One card per machine, with how many of its articles are done.
- Each machine has its articles: number, index, designation, program, material.
- Each article has its tools: tool number, type, Ø, R / ∠, LS (stick-out), Z, holder, code.
- Paste the tool rows straight from Excel.
- Status per article (Not started / In progress / Done) with a progress bar, and filters.
- Search by article, program, or by tool code: `F241` lists every article that uses it and in which pocket.
- Copy an article to make a new index or put it on another machine.

**Tool list sheet**
- A4 PDF with the article, the tool table and a sign-off block, ready to print.
- Live preview while you type (can be switched off).
- Your logo on every sheet.

**Tool crib**
- One card per tool code: type, Ø, R / ∠, Z, cut length, overall length, usual LS, grade/coating, brand & reference, supplier, location, notes.
- Stock with − / +, minimum, count correction and a history of every movement.
- Shows every article that uses the code.
- Codes used in articles but missing from the crib can be added in one click.
- **Tool prep** per article: what to take out, with stock and location, and "take from stock" in one click.
- Order list (CSV) of the codes at or below their minimum.

**Languages:** English and French (the sheet follows the language too).

## Your data

Everything stays on the computer that uses it.
- **Web version:** saved in that browser. Use **Back up** to save it to a file, **Restore** to load it on another PC or browser.
- **Windows program:** saved in `Documents\Tool List Maker`, with an automatic backup copy every day.

Nothing is sent anywhere. People opening the demo link start with an empty program and never see anyone else's work.

## Folders

| Folder | What's inside |
|---|---|
| `WebVersion-Demo/` | The web version. `index.html` plus its `css/`, `js/`, `lib/` and `fonts/`. Works on GitHub Pages, or by opening `index.html` from the folder. |
| `Program/` | The Windows program, zipped. Unzip and run `Tool List Maker.exe` (Windows 10/11, 64-bit). |

## Windows program

1. Download [ToolListMaker-Windows.zip](Program/ToolListMaker-Windows.zip) and unzip it.
2. Keep `Tool List Maker.exe` and `resources.neu` together, and double-click the exe.
3. The first time, Windows may say "Windows protected your PC" (the program isn't signed): click **More info → Run anyway**.

To move your web data into the program: **Back up** in the web version, then **Restore** in the program.

## Built with

[jsPDF](https://github.com/parallax/jsPDF) (PDF sheets) · [PDF.js](https://github.com/mozilla/pdf.js) (live preview) · [Neutralinojs](https://neutralino.js.org) (Windows program) · fonts: Barlow Semi Condensed and IBM Plex (SIL Open Font License).

---

## En français

**Essayer dans le navigateur :** https://achrxf.github.io/ToolManager/WebVersion-Demo/ · **Programme Windows :** [Program/ToolListMaker-Windows.zip](Program/ToolListMaker-Windows.zip)

Tool Manager regroupe les machines CNC, leurs articles et leurs outils, et produit une **fiche outils** A4 (PDF) pour chaque article. Le **magasin outils** garde chaque code outil (F… / M…) avec ses caractéristiques et son stock : entrées / sorties, minimum, historique, préparation des outils par article et liste de commande.

Les données restent sur l'ordinateur qui les utilise (navigateur, ou `Documents\Tool List Maker` pour le programme). Utilisez **Sauvegarder** / **Restaurer** pour les déplacer. Choisissez EN / FR en haut de l'écran.
