import { test, expect } from '@playwright/test';
import { builtRoutes } from '../pages';

const routes = builtRoutes();

test.describe('every built page', () => {
  for (const route of routes) {
    test(`${route} renders with complete metadata and no overflow`, async ({ page }) => {
      const errors: string[] = [];
      page.on('pageerror', (e) => errors.push(e.message));
      page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
      await page.setViewportSize({ width: 360, height: 800 });
      const res = await page.goto(route);
      expect(res?.status(), 'HTTP status').toBe(200);
      expect(res?.headers()['content-type']).toContain('text/html');
      const title = await page.title();
      expect(title.length).toBeGreaterThan(10);
      await expect(page.locator('h1')).toHaveCount(1);
      expect(await page.locator('meta[name="description"]').getAttribute('content')).toBeTruthy();
      const canonical = await page.locator('link[rel="canonical"]').getAttribute('href');
      expect(canonical).toBe(`https://startuproof.com${route}`);
      expect(await page.locator('meta[name="robots"]').getAttribute('content')).toContain('noindex');
      expect(await page.locator('meta[property="og:image"]').getAttribute('content')).toMatch(/^https:\/\/startuproof\.com\/og\/.+\.png$/);
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      expect(overflow, 'horizontal overflow at 360px').toBeLessThanOrEqual(0);
      const imgsWithoutAlt = await page.locator('img:not([alt])').count();
      expect(imgsWithoutAlt).toBe(0);
      expect(errors.filter((e) => !/Failed to load resource.*\/api\//.test(e)), 'console errors').toEqual([]);
    });
  }
});

test('page titles and descriptions are unique across the build', async () => {
  const { readFileSync } = await import('node:fs');
  const seenT = new Map<string, string>(); const seenD = new Map<string, string>();
  for (const r of routes) {
    const html = readFileSync(`dist${r}index.html`, 'utf8');
    const t = html.match(/<title>([^<]*)<\/title>/)?.[1] ?? '';
    const d = html.match(/<meta name="description" content="([^"]*)"/)?.[1] ?? '';
    expect(seenT.get(t), `duplicate title "${t}" on ${r} and ${seenT.get(t)}`).toBeUndefined();
    expect(seenD.get(d), `duplicate description on ${r} and ${seenD.get(d)}`).toBeUndefined();
    seenT.set(t, r); seenD.set(d, r);
  }
});

test('unknown routes return a real 404 page, not a soft 200', async ({ request }) => {
  for (const p of ['/does-not-exist/', '/radar/item/not-a-real-story/', '/startups/not-a-startup/', '/tv/shows/nope/e1/']) {
    const r = await request.get(p);
    expect(r.status(), p).toBe(404);
    expect(await r.text()).toContain("We couldn't find that page");
  }
});

test('robots, sitemaps and search index are served with correct types', async ({ request }) => {
  const robots = await request.get('/robots.txt');
  expect(robots.headers()['content-type']).toContain('text/plain');
  expect(await robots.text()).toContain('Disallow: /');
  const sm = await request.get('/sitemap.xml');
  expect(sm.headers()['content-type']).toContain('xml');
  const pages = await (await request.get('/sitemap-pages.xml')).text();
  expect(pages).toContain('https://startuproof.com/radar/uae/');
  expect(pages, 'demo profiles must not be in sitemaps').not.toContain('/startups/nimbus-ledger/');
  expect(pages, 'account pages must not be in sitemaps').not.toContain('/app/');
  const radar = await (await request.get('/sitemap-radar.xml')).text();
  expect(radar).toContain('/radar/item/erad-22m-series-a-mevp/');
  const idx = await request.get('/search-index.json');
  expect(idx.headers()['content-type']).toContain('application/json');
  const docs = await idx.json() as { u: string }[];
  expect(docs.some((d) => /^\/(startups|investors|mentors)\/[a-z]/.test(d.u)), 'demo profiles excluded from search').toBe(false);
});
