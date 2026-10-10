import { test, expect } from '@playwright/test';
import { writeFileSync, mkdirSync } from 'node:fs';
import { builtRoutes } from '../pages';

/**
 * Crawls every built page, collects same-origin links, assets and anchors, and checks each one:
 * status, MIME type vs extension, and that #fragments exist on the target page.
 * External links are inventoried but not fetched (this environment blocks outbound requests).
 */
test('all internal links, assets and anchors resolve with correct MIME types', async ({ page, request }) => {
  test.setTimeout(240_000);
  const routes = builtRoutes();
  const links = new Map<string, Set<string>>();
  const external = new Map<string, Set<string>>();
  const ids = new Map<string, Set<string>>();
  for (const r of routes) {
    await page.goto(r);
    const found = await page.evaluate(() => ({
      hrefs: [...document.querySelectorAll<HTMLAnchorElement>('a[href]')].map((a) => a.getAttribute('href')!),
      assets: [...document.querySelectorAll('link[href]:not([rel="canonical"]), script[src], img[src]')].map((e) => e.getAttribute('href') ?? e.getAttribute('src')!),
      ids: [...document.querySelectorAll('[id]')].map((e) => e.id),
      buttonsWithoutName: [...document.querySelectorAll('button')].filter((b) => !(b.textContent?.trim() || b.getAttribute('aria-label') || b.querySelector('.visually-hidden'))).length,
    }));
    expect(found.buttonsWithoutName, `${r}: buttons without accessible names`).toBe(0);
    ids.set(r, new Set(found.ids));
    for (const h of [...found.hrefs, ...found.assets]) {
      if (/^(mailto:|tel:|javascript:)/.test(h)) continue;
      const u = new URL(h, `http://localhost:4321${r}`);
      if (u.host !== 'localhost:4321') { if (u.protocol.startsWith('http')) (external.get(u.href) ?? external.set(u.href, new Set()).get(u.href)!).add(r); continue; }
      const key = u.pathname + u.search + u.hash;
      (links.get(key) ?? links.set(key, new Set()).get(key)!).add(r);
    }
  }
  const problems: string[] = [];
  const MIME: Record<string, RegExp> = { '.css': /text\/css/, '.js': /javascript/, '.png': /image\/png/, '.svg': /image\/svg/, '.woff2': /font\/woff2/, '.csv': /text\/csv/, '.md': /text\/markdown/, '.json': /application\/json/, '.xml': /xml/, '.txt': /text\/plain/, '.ics': /text\/calendar/ };
  for (const [href, from] of links) {
    const u = new URL(href, 'http://localhost:4321');
    const res = await request.get(u.pathname + u.search, { maxRedirects: 3 });
    const ext = (u.pathname.match(/\.[a-z0-9]+$/) ?? [''])[0];
    const ct = res.headers()['content-type'] ?? '';
    if (res.status() !== 200) problems.push(`${res.status()} ${href} (from ${[...from][0]})`);
    else if (ext && MIME[ext] && !MIME[ext].test(ct)) problems.push(`MIME ${ct} for ${href}`);
    else if (!ext && !/text\/html/.test(ct)) problems.push(`Expected HTML for ${href}, got ${ct}`);
    if (u.hash && u.hash.length > 1) {
      const target = u.pathname.endsWith('/') ? u.pathname : `${u.pathname}/`;
      const set = ids.get(target);
      if (set && !set.has(decodeURIComponent(u.hash.slice(1)))) problems.push(`Broken anchor ${href} (from ${[...from][0]})`);
    }
  }
  mkdirSync('reports', { recursive: true });
  writeFileSync('reports/link-report.json', JSON.stringify({
    checkedAt: new Date().toISOString(), pages: routes.length, internalTargets: links.size, problems,
    external: [...external].map(([href, from]) => ({ href, foundOn: [...from].slice(0, 5), checked: false, note: 'Outbound network blocked in test environment; not fetched.' })),
  }, null, 2));
  expect(problems).toEqual([]);
});
