// BrocheStuff adapter: language → service → real work on every page, new Atelier look, day/night, classic switch, cabinet map
const vis = async (page, sel) => { try { return await page.locator(sel).first().isVisible({ timeout: 300 }); } catch (e) { return false; } };
const clickRand = async (page, p, sel) => {
  const n = await page.locator(sel + ":visible").count(); if (!n) return false;
  await page.locator(sel + ":visible").nth(Math.floor(p.r() * n)).click({ timeout: 2500 }); return true;
};
module.exports = {
  styles: [["focused", 38], ["explorer", 22], ["chaotic", 13], ["struggler", 10], ["quitter", 9], ["keyboard", 8]],
  locales: [["fr-FR", 70], ["en-US", 30]],
  async setup(page, p) {
    p.state = { n: 0 };
    // a fifth start in the classic look, a fifth in night mode
    const cls = p.r() < 0.2, night = p.r() < 0.25;
    if (cls || night) { await page.evaluate(([c, n]) => { try { if (c) localStorage.setItem("bs.skin", "classic"); if (n) localStorage.setItem("demo.toolmanager.theme", "dark"); } catch (e) {} }, [cls, night]); await page.reload(); await page.waitForTimeout(600); }
  },
  async step(page, p) {
    p.state.n++;
    if (await vis(page, ".langdlg")) { await page.click(`[data-pick=${p.locale.startsWith("fr") ? "fr" : "en"}]`); return "picked language"; }
    if (await vis(page, ".gate")) {
      if (await vis(page, ".gate input")) { await page.locator(".gate input:visible").first().fill(p.r() < 0.8 ? "Achraf" : ""); await page.keyboard.press("Enter"); return "typed name"; }
      const roles = ["methode", "methode", "outil", "outil", "prod", "admin"];
      await page.click(`.gate [data-role=${roles[Math.floor(p.r() * roles.length)]}]`); return "chose a service";
    }
    if (await vis(page, ".overlay:not([hidden]) .dlg")) {
      if (p.r() < 0.5) { await page.keyboard.press("Escape"); return "closed dialog (Esc)"; }
      const ok = await clickRand(page, p, ".overlay:not([hidden]) .dlg footer .btn, .overlay:not([hidden]) .dlg .btn"); return ok ? "answered dialog" : false;
    }
    const r = p.r(), hash = await page.evaluate(() => location.hash);
    if (r < 0.06) { const dn = await page.locator(".daynight:visible [data-dn]").count(); if (dn) { await clickRand(page, p, ".daynight [data-dn]"); return "switched day/night"; } }
    if (r < 0.09) { if (await vis(page, "#b-more")) { await page.click("#b-more"); await page.waitForTimeout(200); if (await vis(page, "#b-skin")) { await page.click("#b-skin"); return "switched skin (menu)"; } } else if (await vis(page, "#b-skin")) { await page.click("#b-skin"); return "switched skin"; } }
    if (r < 0.13 && await vis(page, "#b-find")) { await page.click("#b-find"); await page.keyboard.type(["F27", "Armoire B", "5714", "HSK63", "zzz"][Math.floor(p.r() * 5)], { delay: 25 }); await page.waitForTimeout(250); await page.keyboard.press(p.r() < 0.6 ? "Enter" : "Escape"); return "global search"; }
    // page-specific work
    if (/^#crib/.test(hash)) {
      if (await vis(page, ".plan")) {
        const x = p.r();
        if (x < 0.5) { await clickRand(page, p, ".plan .drw"); return "opened a drawer"; }
        if (x < 0.65) { await clickRand(page, p, "#cres [data-cf]"); return "filtered the crib"; }
        if (x < 0.75 && await page.locator(".plan .it .cd:visible").count()) { await clickRand(page, p, ".plan .it .cd"); return "opened a tool from the drawer"; }
        if (x < 0.82 && await vis(page, ".plan [data-nl]")) { await clickRand(page, p, ".plan [data-nl]"); return "tool without location"; }
        if (x < 0.9) { await page.click("[data-cview=list]"); return "back to list"; }
        if (await vis(page, "#pl-list")) { await page.click("#pl-list"); return "drawer → list"; }
      } else if (await vis(page, "[data-cview=plan]") && p.r() < 0.5) { await page.click("[data-cview=plan]"); return "opened cabinet map"; }
      else if (await page.locator("#crows [data-sd]:visible").count()) { await clickRand(page, p, "#crows [data-sd]"); return "stock +/-"; }
    }
    if ((hash === "" || hash === "#") && await page.locator(".mc[data-m]:visible").count() && p.r() < 0.6) { await clickRand(page, p, ".mc[data-m]"); return "opened a machine"; }
    if (/^#m-/.test(hash) && await page.locator("tr.row[data-a]:visible").count() && p.r() < 0.6) { await clickRand(page, p, "tr.row[data-a] td.cl"); return "opened an article"; }
    if (/^#a-/.test(hash)) {
      const f = page.locator(".tt td input:not([disabled]):visible");
      if (await f.count() && p.r() < 0.5) { const i = Math.floor(p.r() * Math.min(20, await f.count())); await f.nth(i).click(); await page.keyboard.type(p.accuracy > p.r() ? "12" : "Ø12,5 ' \"", { delay: 20 }); await page.keyboard.press("Tab"); return "typed in the tool table"; }
      if (await vis(page, "[data-mode]") && p.r() < 0.4) { await clickRand(page, p, "[data-mode]"); return "switched Saisie/PDF/Excel"; }
    }
    if (await page.locator(".mainnav button[data-nav]:visible").count() && p.r() < 0.55) { await clickRand(page, p, ".mainnav button[data-nav]"); return "went to another page"; }
    if (await page.locator("#b-menu:visible").count() && p.r() < 0.3) { await page.click("#b-menu"); await page.waitForTimeout(200); if (await page.locator(".mainnav button[data-nav]:visible").count()) { await clickRand(page, p, ".mainnav button[data-nav]"); return "menu → page"; } }
    return false;
  },
  prefer(ts, p) { return null; },
  async check(page, p) {
    const s = await page.evaluate(() => {
      const out = [], v = document.querySelector("#view"); if (!v || !window.db) return out;
      const txt = v.innerText;
      if (/\bNaN\b|undefined|\[object Object\]/.test(txt)) out.push({ title: "NaN / undefined shown on screen", detail: (txt.match(/.{0,40}(NaN|undefined|\[object Object\]).{0,40}/) || [""])[0], severity: "high" });
      const at = document.documentElement.classList.contains("at"); let want = true; try { want = localStorage.getItem("bs.skin") !== "classic"; } catch (e) {}
      if (at !== want) out.push({ title: "Look (Atelier/classic) does not match the saved choice", severity: "medium" });
      const dn = document.querySelector("#b-dn [aria-pressed=true]");
      if (at && dn && getComputedStyle(document.querySelector("#b-dn")).display !== "none" && dn.dataset.dn !== curTheme()) out.push({ title: "Day/night switch shows the wrong mode", detail: dn.dataset.dn + " vs " + curTheme(), severity: "medium" });
      const plan = v.querySelector(".plan .cabs");
      if (plan) {
        const sum = [...plan.querySelectorAll(".drw small")].reduce((a, e) => a + (+e.textContent || 0), 0);
        const want2 = (db.catalog || []).filter(c => clean(c.location)).length;
        if (sum !== want2) out.push({ title: "Cabinet map: drawer counts do not add up to the tools with a location", detail: sum + " vs " + want2, severity: "high" });
        if (plan.querySelectorAll(".drw.on").length > 1) out.push({ title: "Cabinet map: more than one drawer selected", severity: "medium" });
        const side = v.querySelector("#planside .its"), on = plan.querySelector(".drw.on small");
        if (side && on && side.children.length !== +on.textContent) out.push({ title: "Cabinet map: drawer panel lists a different number of tools than the drawer", detail: side.children.length + " vs " + on.textContent, severity: "high" });
      }
      const codes = (db.assemblies || []).map(a => a.code); if (new Set(codes).size !== codes.length) out.push({ title: "Two assemblies with the same code", severity: "high" });
      for (const a of (db.assemblies || [])) for (const [m, tn] of Object.entries(a.tnum || {})) if (!/^T\d+$/.test(tn) || !db.machines.some(x => x.id === m)) { out.push({ title: "Assembly T per machine is invalid", detail: a.code + " " + m + " " + tn, severity: "high" }); break; }
      const t = v.querySelector('.tile4[data-cf="all"] b'); if (t && !document.documentElement.classList.contains("navin") && +t.textContent !== (db.catalog || []).length) out.push({ title: "Crib tile count wrong", detail: t.textContent + " vs " + db.catalog.length, severity: "high" });
      return out;
    });
    return s;
  },
};
