import type { APIRoute } from 'astro';
import { SITE } from '../config/site';
export const GET: APIRoute = () => {
  const body = SITE.indexable
    ? `User-agent: *\nDisallow: /app/\nDisallow: /auth/\nDisallow: /api/\n\nSitemap: ${SITE.canonicalOrigin}/sitemap.xml\n`
    : `# Preview build: not for indexing until the domain migration is approved.\nUser-agent: *\nDisallow: /\n`;
  return new Response(body, { headers: { 'content-type': 'text/plain; charset=utf-8' } });
};
