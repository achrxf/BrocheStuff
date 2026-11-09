# Build files

- `BrocheStuff.nsi` + `app.ico`: Windows installer (`makensis -DVER=x.y.z BrocheStuff.nsi`, with the program files in `pkg/BrocheStuff/`).
- The update file `.neu` is an asar archive: `npx @electron/asar extract` / `pack`.
- `patch*.py`: changes applied to the built pages (Web, Demo and the program's `resources/index.html`).
- `tests/`: Playwright tests for the web version (serve the page at http://127.0.0.1:8765/ToolManager.html).
