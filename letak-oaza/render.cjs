// Export letaku: node render.cjs  ->  vystup/ (PDF A4, PDF so spadavkou 3 mm, PNG 300 dpi, JPG na web)
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

const dir = __dirname;
const out = path.join(dir, 'vystup');
fs.mkdirSync(out, { recursive: true });
const url = 'file://' + path.join(dir, 'letak.html');

(async () => {
  const browser = await chromium.launch();
  const open = async (opts = {}, bleed = false) => {
    const page = await browser.newPage(opts);
    await page.goto(url, { waitUntil: 'load' });
    if (bleed) await page.evaluate(() => document.documentElement.classList.add('bleed'));
    await page.evaluate(() => document.fonts.ready);
    return page;
  };

  let page = await open();
  await page.pdf({ path: path.join(out, 'vikendova-oaza-A4.pdf'), width: '210mm', height: '297mm', printBackground: true });
  await page.close();

  page = await open({}, true);
  await page.pdf({ path: path.join(out, 'vikendova-oaza-A4-spadavka-3mm.pdf'), width: '216mm', height: '303mm', printBackground: true });
  await page.close();

  // A4 pri 300 dpi = 2480 x 3508 px (A4 má 793.7 x 1122.5 CSS px; okno 794 x 1123 px, pozadie siaha až po okraj)
  page = await open({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 2480 / 794 });
  await page.screenshot({ path: path.join(out, 'vikendova-oaza-A4-300dpi.png') });
  await page.close();

  // rovnaký rozmer ako pôvodný leták (1414 x 2000 px)
  page = await open({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 1414 / 794 });
  await page.screenshot({ path: path.join(out, 'vikendova-oaza-web.jpg'), type: 'jpeg', quality: 92 });
  await page.close();

  await browser.close();
})();
