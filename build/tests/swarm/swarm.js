#!/usr/bin/env node
// User swarm: many simulated people use a web app at once, each with their own device, pace and habits.
// Every crash, dead end, stuck screen, layout break and slow moment is recorded once, with a screenshot.
//
//   node swarm.js --app <url or path to .html> [--users 1000] [--concurrency 8] [--actions 40]
//                 [--adapter ./my-adapter.js] [--out ./swarm-report] [--seed 1] [--block-external]
//
// An adapter (optional) teaches the swarm the app's main goal, e.g. "finish a lesson" (see the end of this file).
const fs = require("fs"), path = require("path");
const { chromium } = require("playwright");

const args = Object.fromEntries(process.argv.slice(2).reduce((a, x, i, all) => {
  if (x.startsWith("--")) a.push([x.slice(2), all[i + 1] && !all[i + 1].startsWith("--") ? all[i + 1] : true]);
  return a;
}, []));
if (!args.app) { console.error("usage: node swarm.js --app <url|file.html> [--users N] [--concurrency N] [--actions N] [--adapter file] [--out dir]"); process.exit(1); }
const APP = /^https?:|^file:/.test(args.app) ? args.app : "file://" + path.resolve(args.app);
const ONLY = args.only != null ? String(args.only).split(",").map(Number) : null;
const USERS = +(args.users || 200), CONC = +(args.concurrency || 6), ACTIONS = +(args.actions || 40), SEED = +(args.seed || 1);
const OUT = path.resolve(args.out || "swarm-report"), SHOTS = path.join(OUT, "shots");
fs.mkdirSync(SHOTS, { recursive: true });
const adapter = args.adapter ? require(path.resolve(args.adapter)) : {};

/* ---------- personas ---------- */
function rng(seed) { let a = seed >>> 0; return () => { a |= 0; a = (a + 0x6d2b79f5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
const pickW = (r, items) => { const tot = items.reduce((s, x) => s + x[1], 0); let v = r() * tot; for (const [x, w] of items) { v -= w; if (v <= 0) return x; } return items[0][0]; };
const DEVICES = { "small phone":{ w:360, h:640, mobile:true }, phone:{ w:390, h:844, mobile:true }, "large phone":{ w:430, h:932, mobile:true }, tablet:{ w:820, h:1180, mobile:true }, laptop:{ w:1280, h:800, mobile:false } };
function makePersona(i) {
  const r = rng(SEED * 100003 + i);
  const style = pickW(r, adapter.styles || [["focused", 35], ["explorer", 25], ["chaotic", 12], ["struggler", 12], ["quitter", 10], ["keyboard", 6]]);
  const device = pickW(r, [["small phone", 18], ["phone", 42], ["large phone", 20], ["tablet", 8], ["laptop", 12]]);
  return {
    id:i, style, device, ...DEVICES[device],
    scheme:r() < 0.35 ? "dark" : "light",
    locale:pickW(r, adapter.locales || [["en-US", 40], ["fr-FR", 20], ["es-ES", 10], ["de-DE", 10], ["nl-NL", 10], ["it-IT", 10]]),
    reducedMotion:r() < 0.12,
    pace:style === "chaotic" ? 40 + r() * 80 : style === "struggler" ? 600 + r() * 900 : 120 + r() * 500,
    accuracy:style === "struggler" ? 0.3 : style === "focused" ? 0.9 : 0.7,
    mic:r() < 0.7,
    offlineAt:r() < 0.08 ? Math.floor(r() * ACTIONS) : -1,
    reloadAt:r() < 0.15 ? Math.floor(r() * ACTIONS) : -1,
    actions:style === "quitter" ? Math.ceil(ACTIONS * (0.2 + r() * 0.4)) : ACTIONS,
    r,
  };
}

/* ---------- findings ---------- */
const issues = new Map(); // signature -> issue
let shotN = 0;
async function report(page, p, kind, severity, title, detail = "", sigExtra = "") {
  const sig = kind + "|" + title + "|" + sigExtra;
  let it = issues.get(sig);
  if (it) { it.count++; if (it.users.length < 12 && !it.users.includes(p.id)) it.users.push(p.id); return; }
  it = { kind, severity, title, detail: String(detail).slice(0, 600), count:1, users:[p.id], persona:describe(p), trail:p.trail.slice(-8), shot:null };
  issues.set(sig, it);
  try { const f = `${String(++shotN).padStart(3, "0")}-${kind}.png`; await page.screenshot({ path:path.join(SHOTS, f), timeout:4000 }); it.shot = "shots/" + f; } catch (e) {}
}
const describe = (p) => `#${p.id} ${p.style}, ${p.device} ${p.w}×${p.h}, ${p.scheme}, ${p.locale}${p.reducedMotion ? ", reduced motion" : ""}${p.mic ? "" : ", no mic"}`;

/* ---------- what can be tapped right now ---------- */
async function targets(page) {
  return page.evaluate(() => {
    const sel = "button,a[href],[role=button],[role=tab],[role=link],input,select,textarea,summary,[data-act],[onclick],[tabindex]:not([tabindex='-1'])";
    const seen = new Set(), out = [];
    const all = [...document.querySelectorAll(sel)];
    document.querySelectorAll("div,span,li,img,svg").forEach((e) => { if (getComputedStyle(e).cursor === "pointer" && !(e.parentElement && e.parentElement.closest(sel))) all.push(e); });
    for (const el of all) {
      if (seen.has(el)) continue; seen.add(el);
      const r = el.getBoundingClientRect();
      if (r.width < 2 || r.height < 2 || r.bottom < 0 || r.right < 0 || r.top > innerHeight || r.left > innerWidth) continue;
      if (el.disabled || el.getAttribute("aria-disabled") === "true" || el.closest("[hidden],[inert]")) continue;
      const cs = getComputedStyle(el); if (cs.visibility === "hidden" || +cs.opacity === 0 || cs.pointerEvents === "none") continue;
      const cx = Math.min(innerWidth - 1, Math.max(0, r.left + r.width / 2)), cy = Math.min(innerHeight - 1, Math.max(0, r.top + r.height / 2));
      const top = document.elementFromPoint(cx, cy); if (!top || !(el === top || el.contains(top) || top.contains(el))) continue; // covered
      const name = (el.getAttribute("aria-label") || el.innerText || el.value || el.title || el.getAttribute("alt") || "").trim().replace(/\s+/g, " ").slice(0, 50);
      out.push({ x:cx, y:cy, w:r.width, h:r.height, tag:el.tagName.toLowerCase(), type:el.type || "", name, act:el.dataset ? el.dataset.act || "" : "",
        unnamed:!name && !el.querySelector("img[alt]") && /^(button|a)$/i.test(el.tagName) });
    }
    return out;
  });
}
const pageSig = (page) => page.evaluate(() => location.href + "|" + document.body.innerText.length + "|" + document.querySelectorAll("*").length).catch(() => "x");

/* ---------- one simulated user ---------- */
async function runUser(browser, p) {
  const ctx = await browser.newContext({ viewport:{ width:p.w, height:p.h }, deviceScaleFactor:1, isMobile:p.mobile, hasTouch:p.mobile, locale:p.locale,
    colorScheme:p.scheme, reducedMotion:p.reducedMotion ? "reduce" : "no-preference", permissions:p.mic ? ["microphone"] : [] });
  if (args["block-external"]) await ctx.route(/^https?:\/\/(?!localhost|127\.0\.0\.1)/, (r) => r.abort());
  if (adapter.route) await adapter.route(ctx);
  const page = await ctx.newPage(); p.page = page;
  page.setDefaultTimeout(+(args.timeout || 3000));
  p.trail = [];
  if (process.env.TRACE) { const push = p.trail.push.bind(p.trail); p.trail.push = (x) => { console.log(new Date().toISOString().slice(11,23), x); return push(x); }; }
  const tU = Date.now(), budget = +(args["user-seconds"] || 120) * 1000;
  page.on("pageerror", (e) => report(page, p, "crash", "high", "Script error: " + e.message.split("\n")[0], e.stack || ""));
  page.on("console", (m) => { if (m.type() === "error" && !/favicon|net::ERR|Failed to load resource/.test(m.text())) report(page, p, "console", "medium", "Console error: " + m.text().slice(0, 140)); });
  page.on("dialog", (d) => { report(page, p, "ux", "medium", "Browser dialog popped up: " + d.message().slice(0, 80)); d.dismiss().catch(() => {}); });
  page.on("crash", () => report(page, p, "crash", "high", "The page crashed (tab died)"));
  await page.addInitScript(() => { window.__long = []; try { new PerformanceObserver((l) => l.getEntries().forEach((e) => window.__long.push(e.duration))).observe({ type:"longtask", buffered:true }); } catch (e) {} });
  const t0 = Date.now();
  try {
    await page.goto(APP, { waitUntil:"load", timeout:30000 });
    const loadMs = Date.now() - t0;
    if (loadMs > 5000) await report(page, p, "perf", "medium", "Slow first load", `${loadMs} ms on ${p.device}`);
    if (adapter.setup) await adapter.setup(page, p);
    await page.waitForTimeout(400);
    let same = 0, last = await pageSig(page);
    const smallSeen = new Set();
    for (let k = 0; k < p.actions && Date.now() - tU < budget; k++) {
      if (k === p.offlineAt) { await ctx.setOffline(true); p.trail.push("went offline"); }
      if (k === p.reloadAt) { p.trail.push("reloaded the page"); await page.reload({ waitUntil:"load" }); await page.waitForTimeout(500); continue; }
      const handled = adapter.step && p.style !== "explorer" && p.style !== "keyboard" ? await adapter.step(page, p).catch((e) => { p.trail.push("adapter error: " + e.message.replace(/\u001b\[\d+m/g, "").replace(/\s+/g, " ").slice(0, 220)); if (args.debug) console.log("#" + p.id, e.message.replace(/\u001b\[\d+m/g, "").slice(0, 900)); return false; }) : false;
      if (!handled) {
        if (p.style === "keyboard") {
          const key = pickW(p.r, [["Tab", 6], ["Enter", 3], ["Space", 1], ["Escape", 1], ["ArrowDown", 1], ["Shift+Tab", 1]]);
          await page.keyboard.press(key); p.trail.push("pressed " + key);
        } else {
          const ts = await targets(page);
          for (const t of ts) if ((t.w < 24 || t.h < 24) && !smallSeen.has(t.name)) { smallSeen.add(t.name); await report(page, p, "a11y", "low", "Tap target smaller than 24×24 px", `"${t.name || t.tag}" is ${Math.round(t.w)}×${Math.round(t.h)} px on ${p.device}`, t.name || t.tag); }
          for (const t of ts) if (t.unnamed) await report(page, p, "a11y", "low", "Button without a name for screen readers", `${t.tag} at ${Math.round(t.x)},${Math.round(t.y)}`, t.tag + Math.round(t.w));
          const chaos = p.style === "chaotic" && p.r() < 0.25;
          if (chaos) {
            const g = pickW(p.r, [["back", 2], ["swipeUp", 3], ["swipeDown", 1], ["mash", 3]]);
            p.trail.push("chaos: " + g);
            if (g === "back") {
              const before = page.url(); await page.goBack({ timeout:3000 }).catch(() => {});
              if (new URL(page.url()).origin !== new URL(before).origin || page.url() === "about:blank") {
                await report(page, p, "ux", "medium", "Phone Back button leaves the app", "Pressing Back closed the app instead of going back a screen (no history entries for in-app screens).");
                await page.goto(APP, { waitUntil:"load" }); if (adapter.setup) await adapter.setup(page, p); await page.waitForTimeout(400);
              }
            }
            else if (g.startsWith("swipe")) { const up = g === "swipeUp"; await page.mouse.move(p.w / 2, up ? p.h * 0.8 : p.h * 0.25); await page.mouse.down(); await page.mouse.move(p.w / 2, up ? p.h * 0.2 : p.h * 0.85, { steps:6 }); await page.mouse.up(); }
            else if (ts.length) { const t = ts[Math.floor(p.r() * ts.length)]; for (let m = 0; m < 4; m++) await page.mouse.click(t.x, t.y); }
          } else if (!ts.length) {
            // a real person would try tapping outside, then scrolling
            const before = await pageSig(page);
            await page.mouse.click(p.w / 2, 30); await page.waitForTimeout(400);
            if ((await pageSig(page)) !== before) { await report(page, p, "ux", "medium", "No visible way out: only tapping outside closes this", "Nothing on screen is tappable; it only went away after tapping the dimmed area.", p.trail[p.trail.length - 1].replace(/"[^"]*"/g, "")); p.trail.push("tapped outside to close"); }
            else { await report(page, p, "deadend", "high", "Dead end: nothing on screen can be tapped", "", (await page.title()) + p.device); await page.mouse.wheel(0, 400); p.trail.push("scrolled (no targets)"); }
          } else {
            const pref = adapter.prefer ? adapter.prefer(ts, p) : null;
            const t = pref || ts[Math.floor(p.r() * ts.length)];
            p.trail.push(`tapped ${t.tag}${t.act ? "[" + t.act + "]" : ""} "${t.name}"`);
            if (t.tag === "input" && /text|search|email|number|^$/.test(t.type)) { await page.mouse.click(t.x, t.y); await page.keyboard.type(p.r() < 0.3 ? "🙂 ' \" <b> test" : "hello", { delay:20 }); }
            else if (t.tag === "select") await page.mouse.click(t.x, t.y);
            else await page.mouse.click(t.x, t.y);
            if (p.r() < 0.15) { await page.mouse.wheel(0, (p.r() - 0.3) * 900); }
          }
        }
      } else p.trail.push(handled === true ? "did the main task step" : String(handled));
      await page.waitForTimeout(p.pace);
      // checks after every action
      const st = await page.evaluate(() => ({ ow:document.scrollingElement.scrollWidth - innerWidth, lt:(window.__long || []).splice(0).filter((d) => d > 200) })).catch(() => null);
      if (st) {
        if (st.ow > 4) await report(page, p, "layout", "medium", "Page scrolls sideways (content wider than the screen)", `${st.ow}px too wide on ${p.device} ${p.w}px`, p.device);
        for (const d of st.lt) await report(page, p, "perf", d > 500 ? "medium" : "low", `Main thread blocked ${d > 500 ? "over 500" : "200–500"} ms`, `${Math.round(d)} ms long task on ${p.device}; last: ${p.trail[p.trail.length - 1]}`, p.trail[p.trail.length - 1].replace(/"[^"]*"/, ""));
      }
      if (adapter.check) for (const f of (await adapter.check(page, p).catch(() => [])) || []) await report(page, p, f.kind || "logic", f.severity || "high", f.title, f.detail || "", f.sig || "");
      const sig = await pageSig(page);
      same = sig === last && !/listen|play|speak|audio|🔊/i.test(p.trail[p.trail.length - 1] || "") ? same + 1 : 0; last = sig;
      if (same === 8 && !(p.style === "keyboard" && !/Enter|Space/.test(p.trail.slice(-8).join(" ")))) await report(page, p, "stuck", "medium", "Stuck: 8 actions in a row changed nothing", "", (await page.evaluate(() => (document.querySelector("[aria-current],.on,.active,h1,h2") || {}).innerText || "").catch(() => "")).slice(0, 40));
    }
  } catch (e) {
    await report(page, p, "harness", "medium", "Session aborted: " + e.message.split("\n")[0].slice(0, 120), e.stack || "");
  }
  await ctx.close().catch(() => {});
}

/* ---------- run everyone ---------- */
(async () => {
  const browser = await chromium.launch({ args:["--autoplay-policy=no-user-gesture-required", "--use-fake-device-for-media-stream", "--use-fake-ui-for-media-stream"] });
  const t0 = Date.now(); let next = 0, done = 0;
  const styleCount = {};
  const worker = async () => {
    while (next < USERS) {
      const id = next++; if (ONLY && !ONLY.includes(id)) continue;
      const p = makePersona(id); styleCount[p.style] = (styleCount[p.style] || 0) + 1;
      let wd; await Promise.race([runUser(browser, p).finally(() => clearTimeout(wd)), new Promise(res => wd = setTimeout(() => { const it = { kind:"hang", severity:"high", title:"User session hung (no progress for budget+40s)", detail:"", count:1, users:[p.id], persona:describe(p), trail:(p.trail||[]).slice(-10), shot:null }; issues.set("hang|"+p.id, it); console.log("HANG", p.id, JSON.stringify(it.trail));
          (async () => { try { const cdp = await p.page.context().newCDPSession(p.page); await cdp.send("Debugger.enable");
            cdp.on("Debugger.paused", e => { console.log("PAUSED:", e.callFrames.slice(0, 12).map(f => f.functionName + "@" + f.location.lineNumber + ":" + f.location.columnNumber).join(" < ")); });
            await cdp.send("Debugger.pause"); await new Promise(r => setTimeout(r, 4000)); } catch (e) { console.log("cdp fail", e.message); } res(); })(); }, (+(args["user-seconds"] || 120)) * 1000 + 40000))]); done++;
      if (done % Math.max(1, Math.round(USERS / 40)) === 0 || done === USERS) process.stdout.write(`${done}/${USERS} users, ${issues.size} distinct issues, ${Math.round((Date.now() - t0) / 1000)}s\n`);
    }
  };
  await Promise.all(Array.from({ length:CONC }, worker));
  await browser.close();
  const sev = { high:0, medium:1, low:2 };
  const list = [...issues.values()].sort((a, b) => sev[a.severity] - sev[b.severity] || b.count - a.count);
  const meta = { app:APP, users:USERS, actionsPerUser:ACTIONS, seconds:Math.round((Date.now() - t0) / 1000), styles:styleCount, date:new Date().toISOString() };
  fs.writeFileSync(path.join(OUT, "report.json"), JSON.stringify({ meta, issues:list }, null, 1));
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;" })[c]);
  fs.writeFileSync(path.join(OUT, "report.html"), `<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Swarm report</title>
<style>body{font:15px/1.5 system-ui,sans-serif;margin:0;background:#f6f5f2;color:#1f201d}main{max-width:980px;margin:0 auto;padding:24px 16px}h1{margin:0 0 4px}.meta{color:#5c5c58}
.i{background:#fff;border-radius:14px;padding:16px;margin:14px 0;display:grid;grid-template-columns:1fr 180px;gap:16px}.i img{width:180px;border-radius:8px;border:1px solid #ddd}
.sev{display:inline-block;font-size:12px;font-weight:600;border-radius:99px;padding:2px 8px;margin-right:6px}.high{background:#fdecea;color:#7a1d14}.medium{background:#fff4d6;color:#7a5200}.low{background:#e8eef6;color:#29425f}
.k{color:#5c5c58;font-size:13px}ol{margin:6px 0 0;padding-left:20px;color:#5c5c58;font-size:13px}pre{white-space:pre-wrap;font-size:12px;color:#5c5c58;margin:6px 0 0}
@media(max-width:640px){.i{grid-template-columns:1fr}.i img{width:100%}}</style><main>
<h1>Swarm report</h1><p class="meta">${meta.users} simulated users × up to ${meta.actionsPerUser} actions · ${meta.seconds}s · ${esc(Object.entries(styleCount).map(([k, v]) => `${v} ${k}`).join(", "))}<br>${esc(APP)}</p>
<p><b>${list.filter((x) => x.severity === "high").length}</b> high · <b>${list.filter((x) => x.severity === "medium").length}</b> medium · <b>${list.filter((x) => x.severity === "low").length}</b> low</p>
${list.map((x) => `<div class="i"><div><span class="sev ${x.severity}">${x.severity}</span><span class="k">${esc(x.kind)} · hit ${x.count}× by users ${x.users.join(", ")}</span><h3 style="margin:6px 0">${esc(x.title)}</h3>
${x.detail ? `<pre>${esc(x.detail)}</pre>` : ""}<p class="k" style="margin:8px 0 0">First seen: ${esc(x.persona)}</p><ol>${x.trail.map((s) => `<li>${esc(s)}</li>`).join("")}</ol></div>${x.shot ? `<a href="${x.shot}"><img src="${x.shot}" alt=""></a>` : "<div></div>"}</div>`).join("")}
</main>`);
  console.log(`\nDone: ${list.length} distinct issues → ${path.join(OUT, "report.html")}`);
  for (const x of list.slice(0, 30)) console.log(`[${x.severity}] ${x.kind}: ${x.title} (${x.count}×)`);
})();
