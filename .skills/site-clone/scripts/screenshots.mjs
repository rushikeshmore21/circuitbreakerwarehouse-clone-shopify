// Screenshots of any list of pages at desktop and phone sizes (live site or clone).
//   node screenshots.mjs <shots.json> <out-dir>
// shots.json: [{"id":"home-desktop","url":"https://example.com/","device":"desktop|phone","full":true,
//   "width":1440,"height":900,"wait":2500,"quality":70,"steps":[{"js":"window.scrollTo(0,800)","wait":600},{"type":"search text"}]}]
// Needs Node 22+ and Chrome/Chromium/Edge (set CHROME_PATH if not found).
// Drives the installed Chrome over the DevTools protocol (no npm packages).
// Read-only: it opens pages, runs the steps you give it (scrolling, typing into a search box) and never submits forms.
// Pages with smooth scrolling: add a step {"js":"document.documentElement.style.scrollBehavior='auto'"} before scrolling.
import { spawn } from 'node:child_process';
import { mkdirSync, writeFileSync, readFileSync, mkdtempSync, existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const [, , listFile, outDir] = process.argv;
const shots = JSON.parse(readFileSync(listFile, 'utf8'));
mkdirSync(outDir, { recursive: true });

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
const DESKTOP_UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36';
const PHONE_UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1';
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const profile = mkdtempSync(join(tmpdir(), 'cbw-shots-'));
const chrome = spawn(CHROME, [
  '--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`,
  '--no-first-run', '--no-default-browser-check', '--hide-scrollbars', '--mute-audio',
  '--disable-blink-features=AutomationControlled', 'about:blank',
], { stdio: 'ignore' });

let ver;
for (let i = 0; i < 50 && !ver; i++) {
  try { ver = await (await fetch(`http://127.0.0.1:${PORT}/json/version`)).json(); } catch { await sleep(200); }
}
if (!ver) throw new Error('Chrome did not start');

const ws = new WebSocket(ver.webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener('open', r, { once: true }));
let seq = 0;
const pending = new Map();
const waiters = [];
ws.addEventListener('message', (ev) => {
  const m = JSON.parse(ev.data);
  if (m.id && pending.has(m.id)) {
    const { res, rej } = pending.get(m.id);
    pending.delete(m.id);
    m.error ? rej(new Error(m.error.message)) : res(m.result);
  } else if (m.method) {
    for (const w of [...waiters]) if (w.method === m.method && w.sid === m.sessionId) { waiters.splice(waiters.indexOf(w), 1); w.res(m.params); }
  }
});
const send = (method, params = {}, sessionId) => new Promise((res, rej) => {
  const id = ++seq;
  pending.set(id, { res, rej });
  ws.send(JSON.stringify({ id, method, params, sessionId }));
});
const once = (method, sid, ms = 30000) => Promise.race([
  new Promise((res) => waiters.push({ method, sid, res })),
  sleep(ms),
]);

for (const s of shots) {
  const phone = s.device === 'phone';
  const width = s.width || (phone ? 390 : 1440);
  const height = s.height || (phone ? 844 : 900);
  const { targetId } = await send('Target.createTarget', { url: 'about:blank' });
  const { sessionId: sid } = await send('Target.attachToTarget', { targetId, flatten: true });
  await send('Page.enable', {}, sid);
  await send('Runtime.enable', {}, sid);
  await send('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: phone ? 2 : 1, mobile: phone }, sid);
  await send('Emulation.setTouchEmulationEnabled', { enabled: phone }, sid);
  await send('Network.setUserAgentOverride', { userAgent: phone ? PHONE_UA : DESKTOP_UA }, sid);
  if (s.cookies) {
    // Local test site only: a JSON array of cookies for a test account, e.g. to screenshot logged-in views.
    await send('Network.enable', {}, sid);
    const host = new URL(s.url).hostname;
    for (const c of JSON.parse(readFileSync(s.cookies, 'utf8'))) await send('Network.setCookie', { ...c, domain: host }, sid);
  }
  const loaded = once('Page.loadEventFired', sid);
  await send('Page.navigate', { url: s.url }, sid);
  await loaded;
  await sleep(s.wait ?? 2500);
  for (const step of s.steps || []) {
    if (step.js) {
      await send('Runtime.evaluate', { expression: step.js, awaitPromise: true }, sid);
    } else if (step.type) {
      for (const ch of step.type) {
        await send('Input.dispatchKeyEvent', { type: 'keyDown', text: ch }, sid);
        await send('Input.dispatchKeyEvent', { type: 'keyUp' }, sid);
        await sleep(60);
      }
    }
    await sleep(step.wait ?? 600);
  }
  const shot = await send('Page.captureScreenshot', {
    format: s.format || 'webp', quality: s.quality ?? 70,
    ...(s.full ? { captureBeyondViewport: true } : {}),
  }, sid);
  const file = join(outDir, `${s.id}.${s.format || 'webp'}`);
  writeFileSync(file, Buffer.from(shot.data, 'base64'));
  const title = await send('Runtime.evaluate', { expression: 'document.title', returnByValue: true }, sid);
  console.log(`${s.id}\t${Math.round(shot.data.length * 0.75 / 1024)} KB\t${title.result.value}`);
  await send('Target.closeTarget', { targetId });
}

ws.close();
chrome.kill();
