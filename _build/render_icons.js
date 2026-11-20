#!/usr/bin/env node
/* Rendert de PNG-iconen, favicon.ico-bronnen en de social-afbeelding opnieuw uit de SVG's.

   Gebruik (vanuit de root, na `python3 _build/brand.py`):
       node _build/render_icons.js && python3 _build/render_icons.py
   Vereist Playwright (chromium). De tekst op de social-afbeelding is gelijk aan de vorige versie. */
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');
const ROOT = path.resolve(__dirname, '..');
const IMG = path.join(ROOT, 'images');
const logo = fs.readFileSync(path.join(IMG, 'logo.svg'), 'utf8');
const sky = fs.readFileSync(path.join(IMG, 'grachtenpanden.svg'), 'utf8');
const mark = logo.replace(/<rect[^>]*\/>/g, '').replace('viewBox="0 0 512 512"', 'viewBox="40 46 432 432"');
const font = fs.readFileSync(path.join(ROOT, 'fonts', 'inter-latin-var.woff2')).toString('base64');
const b64 = s => 'data:image/svg+xml;base64,' + Buffer.from(s).toString('base64');

(async () => {
  const b = await chromium.launch();
  // app-iconen: volledig vierkant voor apple-touch (iOS rondt zelf af), afgerond voor de rest
  for (const [name, size, square] of [['icon-512.png', 512, 0], ['icon-192.png', 192, 0], ['apple-touch-icon.png', 180, 1], ['favicon-48.png', 48, 0], ['favicon-32.png', 32, 0], ['favicon-16.png', 16, 0]]) {
    const p = await b.newPage({ viewport: { width: size, height: size } });
    const svg = square ? logo.replace('rx="116"', 'rx="0"').replace(/<rect x="1.5"[^>]*\/>/, '') : logo;
    await p.setContent(`<body style="margin:0;background:${square ? '#000' : 'transparent'}"><img src="${b64(svg)}" width="${size}" height="${size}" style="display:block">`);
    await p.screenshot({ path: path.join(IMG, name), omitBackground: !square });
    await p.close();
  }
  // social-afbeelding 1200 x 630
  const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
  await p.setContent(`<style>
@font-face{font-family:Inter;font-weight:100 900;src:url(data:font/woff2;base64,${font}) format("woff2")}
*{box-sizing:border-box}body{margin:0;width:1200px;height:630px;background:#000;color:#f5f5f7;font-family:Inter,sans-serif;overflow:hidden;position:relative}
.sky{position:absolute;inset:0;background:radial-gradient(110% 70% at 50% -10%,rgba(41,151,255,.28),transparent 70%),radial-gradient(60% 46% at 50% 86%,rgba(41,151,255,.42),transparent 72%),radial-gradient(30% 22% at 50% 88%,rgba(255,159,10,.22),transparent 72%)}
.city{position:absolute;left:0;right:0;bottom:58px;height:128px;background:url(${b64(sky)}) 50% 100%/auto 100% repeat-x}
.quay{position:absolute;left:0;right:0;bottom:57px;height:1px;background:rgba(255,255,255,.3)}
.refl{position:absolute;left:0;right:0;bottom:-27px;height:128px;transform:scaleY(-.66);transform-origin:50% 0;translate:0 85px;background:url(${b64(sky)}) 50% 100%/auto 100% repeat-x;opacity:.5;filter:blur(1px);-webkit-mask-image:linear-gradient(to top,#000,transparent 90%)}
.edge{position:absolute;inset:0;background:linear-gradient(90deg,#000,transparent 12%,transparent 88%,#000)}
.in{position:absolute;left:84px;top:64px;right:84px}
.brand{display:flex;align-items:center;gap:14px;font-size:30px;font-weight:650;letter-spacing:-.02em}
.brand img{width:46px;height:46px}.brand b{color:#ffd60a;font-weight:650}
h1{margin:30px 0 0;font-size:106px;line-height:.98;font-weight:700;letter-spacing:-.045em}
h1 span{display:block;color:#a1a1a6}
.row{display:flex;align-items:center;gap:18px;margin-top:30px;font-size:30px;font-weight:550;letter-spacing:-.015em;color:#c9c9ce}
.pill{display:inline-flex;align-items:center;gap:12px;padding:10px 22px 10px 18px;border-radius:999px;background:rgba(255,255,255,.09);box-shadow:inset 0 1px 0 rgba(255,255,255,.25),inset 0 0 0 1px rgba(255,255,255,.1);color:#f5f5f7}
.pill i{width:13px;height:13px;border-radius:50%;background:#ffd60a;box-shadow:0 0 0 4px rgba(255,214,10,.18),0 0 16px 3px rgba(255,159,10,.8)}
.url{position:absolute;right:84px;top:72px;font-size:26px;font-weight:550;color:#a1a1a6;letter-spacing:-.01em}.url b{color:#ffd60a;font-weight:550}
</style><div class="sky"></div><div class="city"></div><div class="quay"></div><div class="refl"></div><div class="edge"></div>
<div class="in"><div class="brand"><img src="${b64(mark)}">Lachgasamsterdam <b>247</b></div>
<h1>Lachgas <span>Amsterdam</span></h1>
<div class="row"><span class="pill"><i></i>24/7 bezorgd</span>Alle stadsdelen · via WhatsApp</div></div>
<div class="url">lachgasamsterdam<b>-247.nl</b></div>`);
  await p.waitForTimeout(300);
  await p.screenshot({ path: path.join(IMG, 'opengraph-image.png') });
  await b.close();
  console.log('iconen en social-afbeelding gerenderd');
})();
