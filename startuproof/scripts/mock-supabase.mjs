// TEST-ONLY mock of the Supabase Auth REST API (the subset supabase-js uses), mounted at /mock-supabase by
// scripts/serve.mjs when SR_MOCK_SUPABASE=1. Refuses to load on Netlify. Lets e2e tests exercise signup,
// email verification (PKCE), resend, login, logout, password reset, expired sessions and investor verification
// without real credentials or sending email. Verification/reset links are exposed via /_test endpoints.
import { createHash, randomUUID } from 'node:crypto';

if (process.env.NETLIFY || process.env.CONTEXT) throw new Error('mock-supabase must never run on Netlify');

const users = new Map(); // email -> user
const tokens = new Map(); // access token -> { userId, exp }
const refresh = new Map(); // refresh token -> userId
const codes = new Map(); // auth code -> { userId, challenge, kind }
const links = new Map(); // email -> last link
const byId = (id) => [...users.values()].find((u) => u.id === id);
const now = () => Math.floor(Date.now() / 1000);
const s256 = (v) => createHash('sha256').update(v).digest('base64url');

function publicUser(u) {
  return { id: u.id, aud: 'authenticated', role: 'authenticated', email: u.email, email_confirmed_at: u.confirmedAt, phone: '', confirmed_at: u.confirmedAt,
    app_metadata: { provider: 'email', providers: ['email'], ...u.app }, user_metadata: u.meta, identities: [], created_at: u.createdAt, updated_at: new Date().toISOString() };
}
function session(u, ttl = 3600) {
  const access = `at_${randomUUID()}`; const rt = `rt_${randomUUID()}`;
  tokens.set(access, { userId: u.id, exp: now() + ttl }); refresh.set(rt, u.id);
  return { access_token: access, token_type: 'bearer', expires_in: ttl, expires_at: now() + ttl, refresh_token: rt, user: publicUser(u) };
}
function err(status, code, msg) { return { status, body: { code: status, error_code: code, msg, message: msg } }; }
function auth(headers) {
  const t = (headers.authorization ?? '').replace(/^Bearer\s+/i, '');
  const rec = tokens.get(t);
  if (!rec || rec.exp < now()) return null;
  return byId(rec.userId) ?? null;
}

export function mockSupabase({ method, path, query, headers, body, origin }) {
  if (headers.apikey !== 'test-anon-key' && !path.startsWith('/_test/')) return err(401, 'no_api_key', 'Invalid API key');
  // ----- test controls -----
  if (path === '/_test/last-link') return { status: 200, body: { link: links.get(query.get('email')) ?? null } };
  if (path === '/_test/verify-investor' && method === 'POST') { const u = users.get(body.email); if (!u) return err(404, 'nf', 'no user'); u.app.investor_verified = true; return { status: 200, body: { ok: true } }; }
  if (path === '/_test/expire-all' && method === 'POST') { for (const v of tokens.values()) v.exp = 0; return { status: 200, body: { ok: true } }; }
  if (path === '/_test/reset' && method === 'POST') { users.clear(); tokens.clear(); refresh.clear(); codes.clear(); links.clear(); return { status: 200, body: { ok: true } }; }
  if (path === '/_test/down' && method === 'POST') { globalThis.__mockDown = Boolean(body.down); return { status: 200, body: { ok: true } }; }
  if (globalThis.__mockDown) return { status: 503, body: { message: 'Service unavailable' } };

  if (path === '/auth/v1/signup' && method === 'POST') {
    if (users.has(body.email)) { // Supabase returns an obfuscated user to avoid enumeration
      return { status: 200, body: { id: randomUUID(), email: body.email, identities: [], user_metadata: {}, app_metadata: {} } };
    }
    if ((body.password ?? '').length < 10) return err(422, 'weak_password', 'Password should be at least 10 characters.');
    const u = { id: randomUUID(), email: body.email, password: body.password, confirmedAt: null, createdAt: new Date().toISOString(), meta: body.data ?? {}, app: {} };
    users.set(u.email, u);
    const code = randomUUID(); codes.set(code, { userId: u.id, challenge: body.code_challenge, kind: 'signup' });
    const redirect = new URL(query.get('redirect_to') ?? `${origin}/auth/callback/`);
    redirect.searchParams.set('code', code); links.set(u.email, redirect.toString());
    return { status: 200, body: publicUser(u) };
  }
  if (path === '/auth/v1/resend' && method === 'POST') {
    const u = users.get(body.email);
    if (u && !u.confirmedAt) {
      const code = randomUUID(); codes.set(code, { userId: u.id, challenge: body.code_challenge, kind: 'signup' });
      const redirect = new URL(body.options?.email_redirect_to ?? query.get('redirect_to') ?? `${origin}/auth/callback/`);
      redirect.searchParams.set('code', code); links.set(u.email, redirect.toString());
    }
    return { status: 200, body: {} };
  }
  if (path === '/auth/v1/recover' && method === 'POST') {
    const u = users.get(body.email);
    if (u) {
      const code = randomUUID(); codes.set(code, { userId: u.id, challenge: body.code_challenge, kind: 'recovery' });
      const redirect = new URL(query.get('redirect_to') ?? `${origin}/reset/`);
      redirect.searchParams.set('code', code); links.set(u.email, redirect.toString());
    }
    return { status: 200, body: {} };
  }
  if (path === '/auth/v1/token' && method === 'POST') {
    const grant = query.get('grant_type');
    if (grant === 'password') {
      const u = users.get(body.email);
      if (!u || u.password !== body.password) return err(400, 'invalid_credentials', 'Invalid login credentials');
      if (!u.confirmedAt) return err(400, 'email_not_confirmed', 'Email not confirmed');
      return { status: 200, body: session(u) };
    }
    if (grant === 'pkce') {
      const c = codes.get(body.auth_code);
      if (!c) return err(403, 'flow_state_not_found', 'invalid flow state, no valid flow state found');
      if (c.challenge && s256(body.code_verifier) !== c.challenge) return err(403, 'bad_code_verifier', 'code challenge does not match');
      codes.delete(body.auth_code);
      const u = byId(c.userId); if (!u.confirmedAt) u.confirmedAt = new Date().toISOString();
      return { status: 200, body: session(u) };
    }
    if (grant === 'refresh_token') {
      const id = refresh.get(body.refresh_token); if (!id) return err(400, 'refresh_token_not_found', 'Invalid Refresh Token');
      refresh.delete(body.refresh_token); return { status: 200, body: session(byId(id)) };
    }
  }
  if (path === '/auth/v1/user' && method === 'GET') {
    const u = auth(headers); if (!u) return err(401, 'bad_jwt', 'invalid JWT');
    return { status: 200, body: publicUser(u) };
  }
  if (path === '/auth/v1/user' && method === 'PUT') {
    const u = auth(headers); if (!u) return err(401, 'bad_jwt', 'invalid JWT');
    if (body.password) { if (body.password.length < 10) return err(422, 'weak_password', 'Password should be at least 10 characters.'); u.password = body.password; }
    if (body.data) u.meta = { ...u.meta, ...body.data }; // user_metadata only; app_metadata cannot be changed by users
    return { status: 200, body: publicUser(u) };
  }
  if (path === '/auth/v1/logout' && method === 'POST') {
    const t = (headers.authorization ?? '').replace(/^Bearer\s+/i, ''); tokens.delete(t); return { status: 204, body: null };
  }
  return err(404, 'not_found', `mock: ${method} ${path} not implemented`);
}
