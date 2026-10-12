// Vyrenderuje SVG banner do PNG cez Chromium (Playwright).
// Použitie: node banner/render.mjs [mierka]   napr. 1 → 1920x1080, 2 → 3840x2160
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
// Playwright je nainštalovaný globálne (npm i -g playwright)
const require = createRequire(execSync('npm root -g').toString().trim() + '/');
const { chromium } = require('playwright');
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const dir = dirname(fileURLToPath(import.meta.url));
const scale = Number(process.argv[2] || 1);
const svg = readFileSync(join(dir, 'plodar-20-banner.svg'), 'utf8');

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: scale });
await page.setContent(`<html><body style="margin:0">${svg}</body></html>`);
const suffix = scale === 1 ? '' : `@${scale}x`;
await page.locator('svg').screenshot({ path: join(dir, `plodar-20-banner${suffix}.png`) });
await browser.close();
console.log(`plodar-20-banner${suffix}.png`);
