// Page audit for any site (the clone or the original): console errors, failed requests, broken
// images, missing alt text, sideways scrolling, small tap targets, heading
// order, duplicate ids, unlabeled form fields and links with no name.
//   node page_audit.mjs <pages.json> [desktop|phone|both] [--json out.json]
// pages.json: [{"id":"home","url":"http://localhost:8080/","ignore":["text to skip"],"wait":3500,"js":"optional script to run first"}]
// Needs Node 22+ (built-in WebSocket) and Chrome/Chromium/Edge (set CHROME_PATH if not found).
// Read-only: opens pages, never submits forms.
import { spawn } from 'node:child_process';
import { readFileSync, mkdtempSync, existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const args = process.argv.slice(2);
const jsonOut = args.includes('--json') ? args[args.indexOf('--json') + 1] : '';
const [listFile, which = 'both'] = args.filter((x, i) => x !== '--json' && args[i - 1] !== '--json');
const pages = JSON.parse(readFileSync(listFile, 'utf8'));
const devices = which === 'both' ? ['desktop', 'phone'] : [which];
const CHROME = findChrome();
function findChrome() {
  if (process.env.CHROME_PATH) return process.env.CHROME_PATH;
  const local = process.env.LOCALAPPDATA || '';
  const list = [
    'C:/Program Files/Google/Chrome/Application/chrome.exe',
    'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
    local + '/Google/Chrome/Application/chrome.exe',
    'C:/Program Files/Microsoft/Edge/Application/msedge.exe',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Chromium.app/Contents/MacOS/Chromium',
    '/usr/bin/google-chrome', '/usr/bin/google-chrome-stable', '/usr/bin/chromium', '/usr/bin/chromium-browser',
  ];
  const hit = list.find((p) => { try { return existsSync(p); } catch { return false; } });
  if (!hit) throw new Error('Chrome not found. Set CHROME_PATH to a Chrome, Chromium or Edge binary.');
  return hit;
}
const PORT = 9300 + Math.floor(Math.random() * 500);
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const UA = {
  desktop: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
  phone: 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1',
};

const chrome = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${mkdtempSync(join(tmpdir(), 'cbw-audit-'))}`, '--no-first-run', '--hide-scrollbars', 'about:blank'], { stdio: 'ignore' });
let ver;
for (let i = 0; i < 50 && !ver; i++) { try { ver = await (await fetch(`http://127.0.0.1:${PORT}/json/version`)).json(); } catch { await sleep(200); } }
const ws = new WebSocket(ver.webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener('open', r, { once: true }));
let seq = 0;
const pending = new Map();
const listeners = [];
ws.addEventListener('message', (ev) => {
  const m = JSON.parse(ev.data);
  if (m.id && pending.has(m.id)) { const { res, rej } = pending.get(m.id); pending.delete(m.id); m.error ? rej(new Error(m.error.message)) : res(m.result); }
  else if (m.method) for (const l of listeners) l(m);
});
const send = (method, params = {}, sessionId) => new Promise((res, rej) => { const id = ++seq; pending.set(id, { res, rej }); ws.send(JSON.stringify({ id, method, params, sessionId })); });

// Runs inside the page.
const CHECKS = `(() => {
  const out = [];
  const vis = (e) => { const r = e.getBoundingClientRect(); const s = getComputedStyle(e); return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none'; };
  const name = (e) => (e.getAttribute('aria-label') || e.getAttribute('title') || e.innerText || (e.querySelector('img[alt]') && e.querySelector('img[alt]').alt) || (e.querySelector('svg title') && e.querySelector('svg title').textContent) || '').trim();
  const desc = (e) => e.tagName.toLowerCase() + (e.id ? '#' + e.id : '') + (e.className && typeof e.className === 'string' ? '.' + e.className.trim().split(/\\s+/).slice(0, 2).join('.') : '');
  // sideways scroll
  const sw = document.documentElement.scrollWidth, cw = document.documentElement.clientWidth;
  if (sw > cw + 1) {
    const wide = [...document.querySelectorAll('body *')].filter((e) => { const r = e.getBoundingClientRect(); return r.right > cw + 1 && vis(e) && getComputedStyle(e).position !== 'fixed'; }).slice(0, 4).map(desc);
    out.push(['overflow-x', 'page is ' + sw + 'px wide in a ' + cw + 'px window: ' + wide.join(', ')]);
  }
  // images
  for (const img of document.images) {
    if (img.complete && img.naturalWidth === 0 && img.src && !img.src.startsWith('data:')) out.push(['broken-img', img.src.slice(0, 120)]);
    if (!img.hasAttribute('alt')) out.push(['img-no-alt', desc(img) + ' ' + (img.currentSrc || img.src).split('/').pop().slice(0, 60)]);
  }
  // links/buttons with no name
  for (const e of document.querySelectorAll('a[href], button')) { if (vis(e) && !name(e) && !e.closest('[aria-hidden=true]')) out.push(['no-name', desc(e) + ' ' + (e.getAttribute('href') || '').slice(0, 60)]); }
  // form fields without labels
  for (const f of document.querySelectorAll('input:not([type=hidden]):not([type=submit]):not([type=button]), select, textarea')) {
    if (!vis(f)) continue;
    const ok = f.labels && f.labels.length || f.getAttribute('aria-label') || f.getAttribute('aria-labelledby') || f.getAttribute('title');
    if (!ok) out.push(['field-no-label', desc(f) + ' name=' + f.name]);
  }
  // duplicate ids
  const seen = {};
  for (const e of document.querySelectorAll('[id]')) seen[e.id] = (seen[e.id] || 0) + 1;
  for (const [id, n] of Object.entries(seen)) if (n > 1) out.push(['dup-id', id + ' x' + n]);
  // headings
  const hs = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].filter(vis);
  const h1 = hs.filter((h) => h.tagName === 'H1').length;
  if (h1 !== 1) out.push(['h1-count', h1 + ' visible h1']);
  let prev = 0;
  for (const h of hs) { const l = +h.tagName[1]; if (prev && l > prev + 1) out.push(['heading-skip', 'h' + prev + ' -> h' + l + ' "' + h.innerText.trim().slice(0, 40) + '"']); prev = l; }
  // small tap targets on phones
  if (innerWidth < 600) {
    for (const e of document.querySelectorAll('a[href], button, input:not([type=hidden]), select, summary')) {
      // Links inside running text are exempt from the WCAG 2.2 target-size rule.
      if (!vis(e) || e.closest('p, td, [aria-label=breadcrumb], [aria-label=Breadcrumb], .breadcrumb, .breadcrumbs, .woocommerce-breadcrumb')) continue;
      const r = e.getBoundingClientRect();
      if ((r.width < 24 || r.height < 24) && r.width > 0) out.push(['tap-small', desc(e) + ' ' + Math.round(r.width) + 'x' + Math.round(r.height) + ' "' + name(e).slice(0, 30) + '"']);
    }
  }
  // lang + title
  if (!document.documentElement.lang) out.push(['no-lang', '']);
  if (!document.title.trim()) out.push(['no-title', '']);
  return out;
})()`;

const results = [];
for (const device of devices) {
  for (const pg of pages) {
    const phone = device === 'phone';
    const { targetId } = await send('Target.createTarget', { url: 'about:blank' });
    const { sessionId: sid } = await send('Target.attachToTarget', { targetId, flatten: true });
    const issues = [];
    const reqs = new Map();
    const onMsg = (m) => {
      if (m.sessionId !== sid) return;
      if (m.method === 'Runtime.exceptionThrown') issues.push(['js-error', (m.params.exceptionDetails.exception?.description || m.params.exceptionDetails.text).split('\n')[0].slice(0, 160)]);
      if (m.method === 'Runtime.consoleAPICalled' && m.params.type === 'error') issues.push(['console-error', m.params.args.map((a) => a.value ?? a.description ?? '').join(' ').slice(0, 160)]);
      if (m.method === 'Log.entryAdded' && m.params.entry.level === 'error') issues.push(['log-error', (m.params.entry.text + ' ' + (m.params.entry.url || '')).slice(0, 180)]);
      if (m.method === 'Network.requestWillBeSent') reqs.set(m.params.requestId, m.params.request.url);
      if (m.method === 'Network.responseReceived' && m.params.response.status >= 400) issues.push(['http-' + m.params.response.status, m.params.response.url.slice(0, 140)]);
      if (m.method === 'Network.loadingFailed' && !m.params.canceled) issues.push(['req-failed', (reqs.get(m.params.requestId) || '').slice(0, 140) + ' ' + m.params.errorText]);
    };
    listeners.push(onMsg);
    for (const d of ['Page', 'Runtime', 'Network', 'Log']) await send(d + '.enable', {}, sid);
    await send('Emulation.setDeviceMetricsOverride', { width: phone ? 390 : 1440, height: phone ? 844 : 900, deviceScaleFactor: 1, mobile: phone }, sid);
    await send('Network.setUserAgentOverride', { userAgent: UA[device] }, sid);
    await send('Page.navigate', { url: pg.url }, sid);
    await sleep(pg.wait ?? 3500);
    if (pg.js) { await send('Runtime.evaluate', { expression: pg.js, awaitPromise: true }, sid); await sleep(1500); }
    const r = await send('Runtime.evaluate', { expression: CHECKS, returnByValue: true }, sid);
    for (const i of r.result.value || []) issues.push(i);
    listeners.splice(listeners.indexOf(onMsg), 1);
    await send('Target.closeTarget', { targetId });
    const ignore = pg.ignore || [];
    const kept = issues.filter(([k, v]) => !ignore.some((x) => (k + ' ' + v).includes(x)));
    results.push({ page: pg.id, device, issues: kept });
    console.log(`\n== ${pg.id} [${device}] ${kept.length} issue(s)`);
    const grouped = {};
    for (const [k, v] of kept) (grouped[k] = grouped[k] || new Set()).add(v);
    for (const [k, vs] of Object.entries(grouped)) { const arr = [...vs]; console.log(`  ${k} (${arr.length}): ${arr.slice(0, 5).join(' | ')}`); }
  }
}
if (jsonOut) { const { writeFileSync } = await import('node:fs'); writeFileSync(jsonOut, JSON.stringify(results, null, 1)); }
const clean = results.filter((r) => !r.issues.length).length;
console.log(`
${clean} of ${results.length} page checks clean`);
ws.close();
chrome.kill();
