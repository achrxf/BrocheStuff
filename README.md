# BrocheStuff

Tool lists, tool crib and holders for a CNC machining shop: every machine, its articles and their tools in one place, a clean A4 **Fiche outils** for each article, and the stock of every tool code and holder.

| | Open | What it is |
|---|---|---|
| **Web** | [achrxf.github.io/BrocheStuff/Web](https://achrxf.github.io/BrocheStuff/Web/) | The program in the browser. Starts empty; your data stays in your browser. |
| **Demo** | [achrxf.github.io/BrocheStuff/Demo](https://achrxf.github.io/BrocheStuff/Demo/) | The same program filled with a made-up workshop: 20 machines (3, 4 and 5 axes; BT30 / BT40 / BT50 / HSK63), 500 articles, ~500 tool codes, ~130 holders and a month of stock moves. |
| **App** | [App/BrocheStuff-Windows.zip](https://github.com/achrxf/BrocheStuff/raw/main/App/BrocheStuff-Windows.zip) | The Windows program (10/11, 64-bit). Unzip, keep `BrocheStuff.exe` and `resources.neu` together, double-click. See [`App/README.txt`](App/README.txt). |

The web version has a **Download the app** button at the top right. The demo stands on its own: it has no link to the real version and no download, so it can be shared safely.

## Folders

```
Web/   index.html   the web version (one file, works offline once opened)
Demo/  index.html   the web version with demo data (kept apart from your real data)
App/   BrocheStuff-Windows.zip + README.txt
```

## What it does

**Services.** On opening, each person picks a service: *Préparateur méthode* (machines, articles, tool sheets), *Préparateur outil* (tool crib, holders, stock log), *Production* (find a tool, a holder or an article, read the sheet, take or return a tool, leave a comment) or *Admin* (everything). Stock moves are logged with the person's name and time.

**Machines and articles.** Machine cards with spindle taper (BT40 / BT50 / …) and progress; articles with number, index, designation, reference, program, material; the tool list (T, type, Ø, R / ∠, LS, LT, Z, holder, code) with a drawing that explains each box, Excel paste, live PDF preview, **print** and **PDF**. A holder of the wrong taper for the machine is flagged.

**Tool crib.** Every tool code (your own coding, whatever it is) with its details, sketch or photo, stock with − / +, minimum, history, where it is used, order list (CSV). Coded references (`FR-2T-ALU-D16,00-CAR-R2,000-Z03-LU32-LT100`) fill the card by themselves.

**Holders.** Every holder by taper (BT40 blue, BT50 amber), type, clamping, nose Ø, length, stock and where it is used. References like `PER-50-25-42-130` are read automatically.

**Production.** One search box for codes, holders and articles; the location in big letters, the stock, the tool list and the sheet; comments saved in the stock log.

**Excel models** (download, preview, print on A4: `1_Machines_Template.xlsx` … `5_Holders_Template.xlsx`) for machines, tool crib, holders, articles and a blank tool sheet to fill by hand. Imports read the columns by their titles (French or English) with a preview first. Every table can be resized like Excel (drag the column edge). French and English (asked the first time, then remembered for each person), light and dark mode.

## Your data

Nothing is sent anywhere.
- **Web:** saved in the browser that uses it. **Sauvegarder / Back up** writes a file; **Restaurer / Restore** reads it on another PC.
- **Windows program:** saved in `Documents\BrocheStuff` with a daily backup copy.
- **Demo:** kept separately from the web version, with its own made-up company logo and a **Reset the demo** button.

Each PC keeps its own data: to share one database between several PCs, a shared folder or a small server is the next step.

## Built with

[SheetJS](https://sheetjs.com) · [jsPDF](https://github.com/parallax/jsPDF) · [PDF.js](https://github.com/mozilla/pdf.js) · [Neutralinojs](https://neutralino.js.org) · fonts Barlow Semi Condensed and IBM Plex (SIL Open Font License).

---

## En français

BrocheStuff regroupe les machines CNC, leurs articles et leurs outils, produit une **fiche outils** A4 pour chaque article, et suit le stock des codes outils et des porte-outils.

- **Web** : https://achrxf.github.io/BrocheStuff/Web/ — le programme dans le navigateur, vide au départ.
- **Démo** : https://achrxf.github.io/BrocheStuff/Demo/ — atelier fictif de 20 machines et 500 articles.
- **Programme Windows** : [App/BrocheStuff-Windows.zip](https://github.com/achrxf/BrocheStuff/raw/main/App/BrocheStuff-Windows.zip) — décompressez, gardez `BrocheStuff.exe` et `resources.neu` ensemble, double-cliquez (voir `README.txt`).

Au démarrage, choisissez votre service : Préparateur méthode, Préparateur outil, Production, ou Accès admin. Les données restent sur l'ordinateur qui les utilise (navigateur, ou `Documents\BrocheStuff` pour le programme). **Sauvegarder / Restaurer** pour les déplacer.
