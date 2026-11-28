// Renders scene.html to MP4 (or to PNG stills for review).
//
//   node render.js <comp> <ar> [out.mp4]            full video, 30 fps
//   node render.js <comp> <ar> --stills 1,2.5,9     PNG stills into ./stills
//   add --v a for the Lina-first feed (fd only; default b = Nami first)
//
// comp: fd | intro    ar: 169 | 916
'use strict';
const http = require('http');
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');
const { chromium } = require('playwright');

const ROOT = __dirname;
const FPS = 30;
const TYPES = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.woff2': 'font/woff2' };

function serve() {
  return new Promise((resolve) => {
    const srv = http.createServer((req, res) => {
      const p = path.normalize(path.join(ROOT, decodeURIComponent(new URL(req.url, 'http://x').pathname)));
      if (!p.startsWith(ROOT) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
      res.writeHead(200, { 'Content-Type': TYPES[path.extname(p)] || 'application/octet-stream' });
      fs.createReadStream(p).pipe(res);
    });
    srv.listen(0, '127.0.0.1', () => resolve(srv));
  });
}

async function main() {
  const [comp, ar, ...rest] = process.argv.slice(2);
  if (!['fd', 'intro'].includes(comp) || !['169', '916'].includes(ar)) {
    console.error('usage: node render.js <fd|intro> <169|916> [out.mp4 | --stills t1,t2] [--v a|b]');
    process.exit(2);
  }
  const stillsIdx = rest.indexOf('--stills');
  const stills = stillsIdx >= 0 ? rest[stillsIdx + 1].split(',').map(Number) : null;
  const vIdx = rest.indexOf('--v');
  const variant = vIdx >= 0 ? rest[vIdx + 1] : 'b';
  if (!['a', 'b'].includes(variant)) { console.error('--v must be a or b'); process.exit(2); }
  const out = stills ? null : (rest[0] && !rest[0].startsWith('--') ? rest[0] : path.join(ROOT, 'out', `${comp}-${ar}.mp4`));

  const srv = await serve();
  const url = `http://127.0.0.1:${srv.address().port}/scene.html?comp=${comp}&ar=${ar}&v=${variant}`;
  const [W, H] = ar === '169' ? [1920, 1080] : [1080, 1920];
  const browser = await chromium.launch();
  try {
    const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
    page.on('pageerror', (e) => { console.error('page error:', e.message); process.exitCode = 1; });
    await page.goto(url);
    await page.evaluate(() => window.ready);
    const dur = await page.evaluate(() => window.DURATION);
    const stage = await page.$('#stage');

    if (stills) {
      fs.mkdirSync(path.join(ROOT, 'stills'), { recursive: true });
      for (const t of stills) {
        await page.evaluate((t) => window.render(t), t);
        await stage.screenshot({ path: path.join(ROOT, 'stills', `${comp}-${ar}-${t.toFixed(2)}.png`) });
      }
      return;
    }

    const frames = Math.round(dur * FPS);
    fs.mkdirSync(path.dirname(out), { recursive: true });
    const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'png', '-i', '-',
      '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', String(FPS), '-movflags', '+faststart', out],
      { stdio: ['pipe', 'inherit', 'inherit'] });
    const done = new Promise((res, rej) => ff.on('close', (c) => (c === 0 ? res() : rej(new Error('ffmpeg exited ' + c)))));
    for (let i = 0; i < frames; i++) {
      await page.evaluate((t) => window.render(t), i / FPS);
      const buf = await stage.screenshot({ type: 'png' });
      if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r));
    }
    ff.stdin.end();
    await done;
    console.log(`wrote ${out} (${frames} frames)`);
  } finally {
    await browser.close();
    srv.close();
  }
}

main().catch((e) => { console.error(e); process.exit(1); });
