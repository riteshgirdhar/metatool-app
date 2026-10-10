// Post-build: writes sitemap index + page and Radar sitemaps from the built HTML.
// Pages marked <meta name="sr-private"> (demo profiles, account pages, drafts) are excluded.
import { readdirSync, readFileSync, writeFileSync, statSync } from 'node:fs';
import { join, relative } from 'node:path';

const dist = new URL('../dist/', import.meta.url).pathname;
const ORIGIN = 'https://startuproof.com';
const today = new Date().toISOString().slice(0, 10);

function walk(dir, acc = []) {
  for (const f of readdirSync(dir)) {
    const p = join(dir, f);
    if (statSync(p).isDirectory()) walk(p, acc);
    else if (f === 'index.html') acc.push(p);
  }
  return acc;
}
const pages = walk(dist)
  .map((file) => ({ file, url: `/${relative(dist, file).replace(/index\.html$/, '')}` }))
  .filter(({ file }) => !readFileSync(file, 'utf8').includes('name="sr-private"'))
  .map(({ url }) => url)
  .sort();

const radar = pages.filter((u) => u.startsWith('/radar/item/'));
const rest = pages.filter((u) => !u.startsWith('/radar/item/'));
const urlset = (urls) => `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls.map((u) => `  <url><loc>${ORIGIN}${u}</loc></url>`).join('\n')}\n</urlset>\n`;
writeFileSync(join(dist, 'sitemap-pages.xml'), urlset(rest));
writeFileSync(join(dist, 'sitemap-radar.xml'), urlset(radar));
writeFileSync(join(dist, 'sitemap.xml'), `<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  <sitemap><loc>${ORIGIN}/sitemap-pages.xml</loc><lastmod>${today}</lastmod></sitemap>\n  <sitemap><loc>${ORIGIN}/sitemap-radar.xml</loc><lastmod>${today}</lastmod></sitemap>\n</sitemapindex>\n`);
console.log(`postbuild: ${rest.length} pages + ${radar.length} Radar items in sitemaps; ${walk(dist).length - pages.length} private pages excluded`);
