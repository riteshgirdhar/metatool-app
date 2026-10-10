// Captures after-state screenshots of every template and a width matrix. Requires `node scripts/serve.mjs` on :4321.
import { chromium } from '@playwright/test';
import { mkdirSync } from 'node:fs';

const base = process.env.BASE ?? 'http://localhost:4321';
const out = new URL('../docs/screenshots/after/', import.meta.url).pathname;
mkdirSync(`${out}desktop`, { recursive: true }); mkdirSync(`${out}mobile`, { recursive: true }); mkdirSync(`${out}widths`, { recursive: true });
const { TEMPLATES } = await import('../tests/e2e/pages.ts');
const browser = await chromium.launch({ executablePath: process.env.PW_CHROMIUM ?? '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });

async function shot(url, file, viewport, opts = {}) {
  const ctx = await browser.newContext({ viewport, deviceScaleFactor: 1, isMobile: viewport.width < 600, hasTouch: viewport.width < 600, reducedMotion: 'reduce' });
  const page = await ctx.newPage();
  await page.goto(base + url, { waitUntil: 'networkidle' });
  if (opts.action) await opts.action(page);
  await page.screenshot({ path: file.replace(/\.png$/, '.jpg'), type: 'jpeg', quality: 72, fullPage: opts.fullPage ?? true });
  await ctx.close();
}

for (const [name, url] of Object.entries(TEMPLATES)) {
  await shot(url, `${out}desktop/${name}.png`, { width: 1440, height: 900 });
  await shot(url, `${out}mobile/${name}.png`, { width: 390, height: 844 });
}
for (const w of [320, 360, 390, 430, 768, 1024, 1280, 1440, 1920]) await shot('/', `${out}widths/home-${w}.png`, { width: w, height: 900 }, { fullPage: false });
await shot('/', `${out}widths/home-landscape-844x390.png`, { width: 844, height: 390 }, { fullPage: false });
await shot('/', `${out}widths/menu-open-1280.png`, { width: 1280, height: 800 }, { fullPage: false, action: (p) => p.getByRole('button', { name: 'Platform' }).click() });
await shot('/', `${out}widths/drawer-open-390.png`, { width: 390, height: 844 }, { fullPage: false, action: (p) => p.locator('[data-drawer-open]').click() });
await browser.close();
console.log('screenshots written to docs/screenshots/after');
