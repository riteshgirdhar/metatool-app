// Local preview server that mimics Netlify for tests: serves dist/ with pretty URLs and a real 404,
// applies netlify.toml headers/redirects (simplified), and routes /api/* to the function handlers.
// Uses an in-memory store (SR_LOCAL_MEMORY_STORE=1) — never used on Netlify (see netlify/lib/store.ts).
import { createServer } from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import { createGzip } from 'node:zlib';
import { extname, join, normalize } from 'node:path';

process.env.SR_LOCAL_MEMORY_STORE = '1';
const { handleSubmit, handleMe, handleDirectory, handleReferrals, handleHealth } = await import('../netlify/lib/handlers.ts');
const { memoryKV } = await import('../netlify/lib/store.ts');

const root = new URL(`../${process.env.DIST ?? 'dist'}/`, import.meta.url).pathname;
const port = Number(process.env.PORT ?? 4321);
const mock = process.env.SR_MOCK_SUPABASE === '1' ? (await import('./mock-supabase.mjs')).mockSupabase : null;
if (mock) { process.env.PUBLIC_SUPABASE_URL = `http://localhost:${port}/mock-supabase`; process.env.PUBLIC_SUPABASE_ANON_KEY = 'test-anon-key'; }
const deps = {
  submissions: memoryKV('submissions'), meta: memoryKV('meta'), referrals: memoryKV('referrals'),
  supabaseUrl: process.env.PUBLIC_SUPABASE_URL, anonKey: process.env.PUBLIC_SUPABASE_ANON_KEY, salt: 'local',
};
const TYPES = { '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.json': 'application/json', '.xml': 'application/xml', '.txt': 'text/plain; charset=utf-8', '.svg': 'image/svg+xml', '.png': 'image/png', '.woff2': 'font/woff2', '.csv': 'text/csv; charset=utf-8', '.md': 'text/markdown; charset=utf-8', '.ics': 'text/calendar; charset=utf-8' };
const REDIRECTS = { '/forgot-password': '/forgot/', '/register': '/signup/', '/help': '/support/', '/cookies': '/cookie/', '/news': '/radar/', '/dashboard': '/app/' };
const BASE_HEADERS = { 'x-robots-tag': 'noindex, nofollow', 'x-content-type-options': 'nosniff', 'referrer-policy': 'strict-origin-when-cross-origin', 'x-frame-options': 'DENY' };

async function tryFile(p) { try { const s = await stat(p); return s.isFile() ? p : null; } catch { return null; } }

createServer(async (req, res) => {
  const url = new URL(req.url, `http://localhost:${port}`);
  const send = (status, headers, body) => {
    const h = { ...BASE_HEADERS, ...headers };
    const gz = /gzip/.test(req.headers['accept-encoding'] ?? '') && /text|json|xml|javascript|svg/.test(h['content-type'] ?? '');
    if (gz) { h['content-encoding'] = 'gzip'; res.writeHead(status, h); const z = createGzip(); z.pipe(res); z.end(body); }
    else { res.writeHead(status, h); res.end(body); }
  };
  if (mock && url.pathname.startsWith('/mock-supabase/')) {
    const chunks = []; for await (const c of req) chunks.push(c);
    let body = {}; try { body = chunks.length ? JSON.parse(Buffer.concat(chunks).toString()) : {}; } catch { /* ignore */ }
    const r = mock({ method: req.method, path: url.pathname.replace('/mock-supabase', ''), query: url.searchParams, headers: req.headers, body, origin: `http://localhost:${port}` });
    res.writeHead(r.status, { 'content-type': 'application/json', 'access-control-allow-origin': '*' });
    return res.end(r.body === null ? '' : JSON.stringify(r.body));
  }
  if (url.pathname.startsWith('/api/')) {
    const chunks = []; for await (const c of req) chunks.push(c);
    const request = new Request(url, { method: req.method, headers: req.headers, body: ['GET', 'HEAD'].includes(req.method) ? undefined : Buffer.concat(chunks) });
    const route = { '/api/submit': handleSubmit, '/api/me': handleMe, '/api/directory': handleDirectory, '/api/referrals': handleReferrals, '/api/health': () => handleHealth(deps) }[url.pathname];
    if (!route) return send(404, { 'content-type': 'application/json' }, '{"ok":false,"error":"not_found"}');
    const r = await route(request, deps);
    return send(r.status, Object.fromEntries(r.headers), Buffer.from(await r.arrayBuffer()));
  }
  const clean = url.pathname.replace(/\/+$/, '');
  if (REDIRECTS[clean]) { res.writeHead(301, { location: REDIRECTS[clean] }); return res.end(); }
  const rel = normalize(decodeURIComponent(url.pathname)).replace(/^(\.\.[/\\])+/, '');
  let file = await tryFile(join(root, rel));
  if (!file && !extname(rel)) {
    if (!url.pathname.endsWith('/') && await tryFile(join(root, rel, 'index.html'))) { res.writeHead(301, { location: `${url.pathname}/${url.search}` }); return res.end(); }
    file = await tryFile(join(root, rel, 'index.html'));
  }
  if (!file) return send(404, { 'content-type': TYPES['.html'] }, await readFile(join(root, '404.html')));
  const headers = { 'content-type': TYPES[extname(file)] ?? 'application/octet-stream' };
  if (file.includes('/_astro/') || file.includes('/fonts/')) headers['cache-control'] = 'public, max-age=31536000, immutable';
  if (file.includes('/downloads/')) headers['content-disposition'] = 'attachment';
  send(200, headers, await readFile(file));
}).listen(port, () => console.log(`serving dist on http://localhost:${port}`));
