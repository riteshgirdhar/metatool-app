import { test } from 'node:test';
import assert from 'node:assert/strict';
import { handleSubmit, handleDirectory, handleReferrals, handleMe } from '../../netlify/lib/handlers.ts';
import { memoryKV, openKV, resetMemory } from '../../netlify/lib/store.ts';
import { principalFromUser } from '../../netlify/lib/auth.ts';

const deps = (extra = {}) => ({ submissions: memoryKV(`s${Math.random()}`), meta: memoryKV(`m${Math.random()}`), referrals: memoryKV(`r${Math.random()}`), ...extra });
const post = (body, headers = {}) => new Request('http://x/api/submit', { method: 'POST', body: JSON.stringify(body), headers: { 'content-type': 'application/json', ...headers } });
const contact = (k, extra = {}) => ({ type: 'contact', idempotencyKey: k, elapsedMs: 5000, fields: { name: 'Ana', email: 'ana@example.com', topic: 'general', message: 'Hello from the unit tests' }, ...extra });

test('valid submission is stored durably before success is returned', async () => {
  const d = deps();
  const r = await handleSubmit(post(contact('key-aaaaaaaaaaaaaaaa')), d);
  assert.equal(r.status, 201);
  const { reference } = await r.json();
  assert.match(reference, /^SR-CON-[A-Z2-9]{8}$/);
  const keys = await d.submissions.list('contact/');
  assert.equal(keys.length, 1);
  const rec = await d.submissions.get(keys[0]);
  assert.equal(rec.reference, reference);
  assert.equal(rec.fields.email, 'ana@example.com');
  assert.ok(!JSON.stringify(rec).includes('127.0.0.1'), 'raw IP must not be stored');
});

test('storage failure returns 500 and never a reference', async () => {
  const broken = { ...memoryKV('x'), set: async () => { throw new Error('disk full'); } };
  const r = await handleSubmit(post(contact('key-bbbbbbbbbbbbbbbb')), deps({ submissions: broken }));
  assert.equal(r.status, 500);
  const body = await r.json();
  assert.equal(body.ok, false);
  assert.equal(body.reference, undefined);
});

test('idempotent replay returns the same reference without a second record', async () => {
  const d = deps();
  const a = await (await handleSubmit(post(contact('key-cccccccccccccccc')), d)).json();
  const r2 = await handleSubmit(post(contact('key-cccccccccccccccc')), d);
  assert.equal(r2.status, 200);
  assert.equal((await r2.json()).reference, a.reference);
  assert.equal((await d.submissions.list('contact/')).length, 1);
});

test('spam controls: honeypot, too fast, rate limit', async () => {
  const d = deps();
  assert.equal((await handleSubmit(post(contact('key-dddddddddddddddd', { hp: 'x' })), d)).status, 400);
  assert.equal((await handleSubmit(post(contact('key-eeeeeeeeeeeeeeee', { elapsedMs: 100 })), d)).status, 429);
  let last;
  for (let i = 0; i < 9; i++) last = await handleSubmit(post(contact(`key-rate-${i}-aaaaaaaaaaaa`)), d);
  assert.equal(last.status, 429);
  assert.equal((await last.json()).error, 'rate_limited');
});

test('validation errors are per-field', async () => {
  const r = await handleSubmit(post(contact('key-ffffffffffffffff', { fields: { name: 'A', email: 'bad', topic: 'nope', message: 'hi' } })), deps());
  assert.equal(r.status, 422);
  const { details } = await r.json();
  assert.ok(details.name && details.email && details.topic && details.message);
});

test('auth-only forms refuse without identity provider or token', async () => {
  const body = { type: 'intro-request', idempotencyKey: 'key-gggggggggggggggg', elapsedMs: 5000, fields: { targetType: 'startup', targetSlug: 'nimbus-ledger', message: 'Would like to talk about a pilot.' } };
  assert.equal((await handleSubmit(post(body), deps())).status, 503);
  const fetchStub = async () => new Response('{}', { status: 401 });
  assert.equal((await handleSubmit(post(body), deps({ supabaseUrl: 'https://sb.test', anonKey: 'k', fetch: fetchStub }))).status, 401);
  const noToken = await handleSubmit(post({ ...body, idempotencyKey: 'key-hhhhhhhhhhhhhhhh' }), deps({ supabaseUrl: 'https://sb.test', anonKey: 'k', fetch: fetchStub }));
  assert.equal(noToken.status, 401);
});

test('authorization ignores user-editable metadata', () => {
  const p = principalFromUser({ id: 'u1', email: 'a@b.c', email_confirmed_at: '2026-01-01', user_metadata: { investor_verified: true, sr_admin: true, requested_role: 'investor' }, app_metadata: {} });
  assert.equal(p.investorVerified, false);
  assert.equal(p.admin, false);
  assert.equal(p.requestedRole, 'investor');
  const v = principalFromUser({ id: 'u2', email: 'a@b.c', email_confirmed_at: '2026-01-01', user_metadata: {}, app_metadata: { investor_verified: true } });
  assert.equal(v.investorVerified, true);
});

const userFetch = (user) => async () => new Response(JSON.stringify(user), { status: 200 });
const member = { id: 'm1', email: 'm@x.io', email_confirmed_at: '2026-01-01', app_metadata: {}, user_metadata: { investor_verified: true } };
const verifiedInvestor = { id: 'i1', email: 'i@x.io', email_confirmed_at: '2026-01-01', app_metadata: { investor_verified: true }, user_metadata: {} };
const unverifiedEmail = { id: 'n1', email: 'n@x.io', email_confirmed_at: null, app_metadata: {}, user_metadata: {} };
const authed = (path) => new Request(`http://x${path}`, { headers: { authorization: 'Bearer t' } });

test('directory: member sees member fields but not investor-only fields', async () => {
  const r = await handleDirectory(authed('/api/directory?type=startups&slug=portside'), deps({ supabaseUrl: 'https://sb.test', anonKey: 'k', fetch: userFetch(member) }));
  const b = await r.json();
  assert.equal(r.status, 200);
  assert.equal(b.items[0].investorOnly, null);
  assert.match(b.items[0].traction, /GMV/);
});

test('directory: verified investor sees investor-only fields', async () => {
  const b = await (await handleDirectory(authed('/api/directory?type=startups&slug=portside'), deps({ supabaseUrl: 'https://sb.test', anonKey: 'k', fetch: userFetch(verifiedInvestor) }))).json();
  assert.ok(b.items[0].investorOnly);
});

test('directory: unverified email is refused', async () => {
  const r = await handleDirectory(authed('/api/directory?type=startups'), deps({ supabaseUrl: 'https://sb.test', anonKey: 'k', fetch: userFetch(unverifiedEmail) }));
  assert.equal(r.status, 403);
});

test('identity provider outage surfaces as 503, not success', async () => {
  const down = async () => { throw new TypeError('fetch failed'); };
  const r = await handleMe(authed('/api/me'), deps({ supabaseUrl: 'https://sb.test', anonKey: 'k', fetch: down }));
  assert.equal(r.status, 503);
});

test('referrals: one attribution per account, no self-referral, qualification tracked', async () => {
  const d = deps({ supabaseUrl: 'https://sb.test', anonKey: 'k' });
  const as = (u) => ({ ...d, fetch: userFetch(u) });
  const A = { id: 'A', email: 'a@x.io', email_confirmed_at: '2026-01-01', app_metadata: {}, user_metadata: {} };
  const B = { ...A, id: 'B', email: 'b@x.io' };
  const sumA = await (await handleReferrals(authed('/api/referrals'), as(A))).json();
  const attr = (u, code) => handleReferrals(new Request('http://x/api/referrals?action=attribute', { method: 'POST', headers: { authorization: 'Bearer t' }, body: JSON.stringify({ code }) }), as(u));
  assert.equal((await attr(A, sumA.code)).status, 422);
  assert.equal((await attr(B, sumA.code)).status, 201);
  assert.equal((await (await attr(B, sumA.code)).json()).status, 'already_attributed');
  await handleReferrals(new Request('http://x/api/referrals?action=qualify', { method: 'POST', headers: { authorization: 'Bearer t' }, body: '{}' }), as(B));
  const after = await (await handleReferrals(authed('/api/referrals'), as(A))).json();
  assert.equal(after.referred, 1); assert.equal(after.qualified, 1); assert.equal(after.rewards, null);
});

test('memory store is refused on Netlify: Blobs is required even if the local flag is set', () => {
  resetMemory();
  // Without a Blobs context, demanding Blobs throws — proving no silent fallback to non-durable memory.
  assert.throws(() => openKV('x', { SR_LOCAL_MEMORY_STORE: '1', NETLIFY: 'true' }), /Netlify Blobs/);
  assert.equal(typeof openKV('x', { SR_LOCAL_MEMORY_STORE: '1' }).get, 'function');
});
