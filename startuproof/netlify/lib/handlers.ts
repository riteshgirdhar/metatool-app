import { z } from 'zod';
import { FORM_SCHEMAS, AUTH_REQUIRED, MIN_FILL_MS, isFormType, type FormType } from '../../src/lib/forms.ts';
import { HttpError, json, readJson, sha256, clientIp, sameOrigin } from './http.ts';
import { requirePrincipal, authConfigured, type AuthDeps, type Principal } from './auth.ts';
import type { KV } from './store.ts';
import { PRIVATE_STARTUPS, PRIVATE_INVESTORS, MEMBERS_ONLY_INVESTORS, PRIVATE_MENTORS } from './directory-private.ts';

export interface Deps extends AuthDeps {
  submissions: KV; meta: KV; referrals: KV;
  now?: () => number; allowedOrigins?: string[]; salt?: string;
}
const RATE_LIMIT = 8; // per IP hash, per form type, per hour

function errorResponse(e: unknown) {
  if (e instanceof HttpError) return json(e.status, { ok: false, error: e.code, message: e.message, details: e.details });
  console.error('unhandled', e);
  return json(500, { ok: false, error: 'server_error', message: 'Something went wrong on our side. Your details were not saved — please try again.' });
}

function reference(type: FormType) {
  const alphabet = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
  const bytes = crypto.getRandomValues(new Uint8Array(8));
  const code = [...bytes].map((b) => alphabet[b % alphabet.length]).join('');
  return `SR-${type.replace(/[^a-z]/g, '').slice(0, 3).toUpperCase()}-${code}`;
}

const Envelope = z.object({
  type: z.string(),
  idempotencyKey: z.string().regex(/^[A-Za-z0-9-]{16,64}$/),
  elapsedMs: z.number().int().nonnegative().max(86_400_000),
  hp: z.string().optional(),
  fields: z.record(z.string(), z.unknown()),
});

export async function handleSubmit(req: Request, d: Deps): Promise<Response> {
  try {
    if (req.method !== 'POST') return json(405, { ok: false, error: 'method_not_allowed', message: 'Use POST.' }, { allow: 'POST' });
    if (!sameOrigin(req, d.allowedOrigins ?? [])) throw new HttpError(403, 'bad_origin', 'Submissions must come from this site.');
    const env = Envelope.safeParse(await readJson(req));
    if (!env.success) throw new HttpError(400, 'invalid_request', 'The form could not be read. Please reload the page and try again.');
    const { type, idempotencyKey, elapsedMs, hp, fields } = env.data;
    if (!isFormType(type)) throw new HttpError(400, 'unknown_form', 'Unknown form.');
    const now = (d.now ?? Date.now)();

    // Idempotent replay: same key returns the original reference without writing again.
    const idemKey = `idem/${type}/${idempotencyKey}`;
    const prior = await d.meta.get(idemKey) as { reference: string } | null;
    if (prior?.reference) return json(200, { ok: true, reference: prior.reference, replayed: true });

    // Spam controls: honeypot and minimum fill time. Respond like a validation failure, never as success.
    if (hp) throw new HttpError(400, 'rejected', 'Your submission could not be accepted.');
    if (elapsedMs < MIN_FILL_MS) throw new HttpError(429, 'too_fast', 'That was quicker than expected. Please wait a moment and submit again.');

    let principal: Principal | null = null;
    if (AUTH_REQUIRED.has(type)) principal = await requirePrincipal(req, d);

    const parsed = FORM_SCHEMAS[type].safeParse(fields);
    if (!parsed.success) {
      const details: Record<string, string> = {};
      for (const issue of parsed.error.issues) { const k = String(issue.path[0] ?? '_'); details[k] ??= issue.message; }
      throw new HttpError(422, 'validation_failed', 'Please correct the highlighted fields.', details);
    }

    // Rate limit per hashed IP (raw IPs are never stored).
    const ipHash = (await sha256(`${d.salt ?? 'sr'}:${clientIp(req)}`)).slice(0, 24);
    const hour = Math.floor(now / 3_600_000);
    const rlKey = `rl/${type}/${ipHash}/${hour}`;
    const count = ((await d.meta.get(rlKey)) as number | null) ?? 0;
    if (count >= RATE_LIMIT) throw new HttpError(429, 'rate_limited', 'Too many submissions from this connection. Please try again in an hour.');

    const ref = reference(type);
    const record = {
      reference: ref, type, receivedAt: new Date(now).toISOString(), status: 'received',
      fields: parsed.data, account: principal ? { id: principal.id, email: principal.email } : null,
      meta: { ipHash, userAgent: (req.headers.get('user-agent') ?? '').slice(0, 200), page: (req.headers.get('referer') ?? '').slice(0, 300) },
    };
    const month = record.receivedAt.slice(0, 7);
    // Durable write first; success is only reported after it completes.
    await d.submissions.set(`${type}/${month}/${ref}`, record);
    const created = await d.meta.create(idemKey, { reference: ref, at: record.receivedAt });
    if (!created) {
      const winner = await d.meta.get(idemKey) as { reference: string } | null;
      if (winner?.reference) return json(200, { ok: true, reference: winner.reference, replayed: true });
    }
    await d.meta.set(rlKey, count + 1);
    return json(201, { ok: true, reference: ref });
  } catch (e) { return errorResponse(e); }
}

export async function handleMe(req: Request, d: Deps): Promise<Response> {
  try {
    const p = await requirePrincipal(req, d);
    return json(200, { ok: true, user: { id: p.id, email: p.email, investorVerified: p.investorVerified, requestedRole: p.requestedRole } });
  } catch (e) { return errorResponse(e); }
}

/** Members see member fields; verified investors additionally see investor-restricted fields. */
export async function handleDirectory(req: Request, d: Deps): Promise<Response> {
  try {
    const url = new URL(req.url);
    const type = url.searchParams.get('type');
    const slug = url.searchParams.get('slug');
    if (!['startups', 'investors', 'mentors'].includes(type ?? '')) throw new HttpError(400, 'bad_type', 'Unknown directory.');
    const p = await requirePrincipal(req, d);
    if (type === 'startups') {
      const rows = PRIVATE_STARTUPS.map(({ investorOnly, ...member }) => ({ ...member, ...(p.investorVerified ? { investorOnly } : { investorOnly: null }) }));
      return json(200, { ok: true, viewer: { investorVerified: p.investorVerified }, items: slug ? rows.filter((r) => r.slug === slug) : rows });
    }
    if (type === 'investors') {
      const rows = [...PRIVATE_INVESTORS, ...MEMBERS_ONLY_INVESTORS];
      return json(200, { ok: true, viewer: { investorVerified: p.investorVerified }, items: slug ? rows.filter((r) => r.slug === slug) : rows });
    }
    return json(200, { ok: true, viewer: { investorVerified: p.investorVerified }, items: slug ? PRIVATE_MENTORS.filter((r) => r.slug === slug) : PRIVATE_MENTORS });
  } catch (e) { return errorResponse(e); }
}

/**
 * Referrals: codes and attributions are stored server-side. A referral "qualifies" only when the referred account
 * has a verified email and completes onboarding (reported by the onboarding call). No rewards are computed because
 * reward terms are not approved.
 */
export async function handleReferrals(req: Request, d: Deps): Promise<Response> {
  try {
    const p = await requirePrincipal(req, d);
    const url = new URL(req.url);
    const action = url.searchParams.get('action') ?? 'summary';
    const userKey = `user/${p.id}`;
    let mine = await d.referrals.get(userKey) as { code: string; createdAt: string } | null;
    if (!mine) {
      const code = (await sha256(`${d.salt ?? 'sr'}:ref:${p.id}`)).slice(0, 8).toUpperCase();
      mine = { code, createdAt: new Date((d.now ?? Date.now)()).toISOString() };
      await d.referrals.create(userKey, mine);
      await d.referrals.create(`code/${code}`, { owner: p.id });
      mine = await d.referrals.get(userKey) as { code: string; createdAt: string };
    }
    if (req.method === 'GET' && action === 'summary') {
      const keys = await d.referrals.list(`attr/by-referrer/${p.id}/`);
      const items = await Promise.all(keys.map((k) => d.referrals.get(k))) as { status: string }[];
      return json(200, { ok: true, code: mine.code, referred: items.length, qualified: items.filter((i) => i.status === 'qualified').length, rewards: null, rewardTerms: 'pending_approval' });
    }
    if (req.method === 'POST' && action === 'attribute') {
      const body = z.object({ code: z.string().regex(/^[A-F0-9]{8}$/) }).safeParse(await readJson(req, 1000));
      if (!body.success) throw new HttpError(422, 'bad_code', 'That referral code is not valid.');
      const owner = await d.referrals.get(`code/${body.data.code}`) as { owner: string } | null;
      if (!owner) throw new HttpError(404, 'unknown_code', 'That referral code was not found.');
      if (owner.owner === p.id) throw new HttpError(422, 'self_referral', 'You cannot use your own referral code.');
      const rec = { referrer: owner.owner, referred: p.id, status: 'pending', at: new Date((d.now ?? Date.now)()).toISOString() };
      const first = await d.referrals.create(`attr/by-referred/${p.id}`, rec);
      if (!first) return json(200, { ok: true, status: 'already_attributed' });
      await d.referrals.set(`attr/by-referrer/${owner.owner}/${p.id}`, rec);
      return json(201, { ok: true, status: 'pending' });
    }
    if (req.method === 'POST' && action === 'qualify') {
      const rec = await d.referrals.get(`attr/by-referred/${p.id}`) as { referrer: string; status: string } | null;
      if (!rec) return json(200, { ok: true, status: 'none' });
      if (rec.status !== 'qualified') {
        const upd = { ...rec, status: 'qualified', qualifiedAt: new Date((d.now ?? Date.now)()).toISOString() };
        await d.referrals.set(`attr/by-referred/${p.id}`, upd);
        await d.referrals.set(`attr/by-referrer/${rec.referrer}/${p.id}`, upd);
      }
      return json(200, { ok: true, status: 'qualified' });
    }
    throw new HttpError(400, 'bad_action', 'Unknown action.');
  } catch (e) { return errorResponse(e); }
}

export function handleHealth(d: Deps) {
  return json(200, { ok: true, auth: authConfigured(d) ? 'configured' : 'not_configured' });
}
