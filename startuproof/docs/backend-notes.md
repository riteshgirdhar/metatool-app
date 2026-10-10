# Backend and API notes

## Architecture choice

**Astro 7 + TypeScript, fully static output, plus Netlify Functions (v2).** The old site's source was not
available, so there was no framework to preserve. Public pages are content-heavy and SEO-critical; static generation
gives complete initial HTML, unique metadata per URL and near-zero JavaScript. Interactivity is small, per-page
vanilla TypeScript; the Supabase SDK is code-split and loaded only when a session is needed. Server logic lives in
`netlify/lib/` as pure, unit-testable handlers; `netlify/functions/*.mts` are thin entry points.

## Functions

| Endpoint | Method | Auth | Purpose |
|---|---|---|---|
| `/api/submit` | POST | Public forms: none. `intro-request`, `investor-verification`: Bearer token, verified email | Validate (Zod), honeypot, minimum fill time, rate limit (salted IP hash, 8/h/form), idempotency key, durable write to Netlify Blobs, return `{reference}` |
| `/api/me` | GET | Bearer | Returns id, email, `investorVerified` (from `app_metadata`), requested role (informational) |
| `/api/directory?type=&slug=` | GET | Bearer | Member-only directory fields; investor-only fields only when `app_metadata.investor_verified === true` |
| `/api/referrals?action=summary\|attribute\|qualify` | GET/POST | Bearer | Server-side referral codes, single attribution per account, self-referral blocked, qualification after onboarding; `rewards: null` (terms pending) |
| `/api/health` | GET | none | Reports whether auth is configured (boolean only) |

Request envelope for `/api/submit`:
`{ type, idempotencyKey (16–64 chars), elapsedMs, hp, fields: {...} }`. Responses: `201 {ok, reference}`,
`200 {ok, reference, replayed:true}`, `400/422 {error, message, details}`, `401/403` auth, `429` rate/too fast,
`503` auth unavailable, `500` storage failure (never with a reference).

## Storage

Netlify Blobs (strong consistency): `submissions` (`<type>/<YYYY-MM>/<reference>`), `submission-meta`
(idempotency + rate-limit counters), `referrals`. The in-memory store is test-only and refused when running on
Netlify (unit-tested). To read submissions: Netlify UI → project → Blobs, or `netlify blobs:list submissions`.
A small admin/inbox view and email notifications (via an email provider) are recommended next steps.

## Authorization rules

- Identity: Supabase Auth only. Tokens verified server-side via `GET {SUPABASE_URL}/auth/v1/user`.
- Unverified emails are refused by protected endpoints.
- Decisions use **only** `app_metadata` (`investor_verified`, `sr_admin`), which users cannot edit.
  `user_metadata` (name, requested role, onboarding answers, referral code) is informational.
- Privileged Supabase keys are never used by the site; no service-role key is required by the current functions.

## Existing Supabase backends (unchanged)

The rebuild does not write to either existing Supabase project. Recommended path:
1. Create a staging project or branch; apply `supabase/proposed/20261010_harden_roles_and_views.sql`; run the
   cross-user and unverified-investor checks from `tests/e2e/journeys` against it.
2. Point `PUBLIC_SUPABASE_URL`/`PUBLIC_SUPABASE_ANON_KEY` at it for the preview.
3. Decide whether directory, Radar and Academy content should be read from Supabase at build time (adapter:
   replace the arrays in `src/data/*.ts` with a fetch in a build script, keeping the Zod schemas as the contract).

## Radar ingestion

The old site ingested feeds automatically (`radar-collect`, `radar-run`). The rebuild publishes an editor-reviewed
snapshot (`src/data/radar.ts`) because automatic ingestion produced the defects in the audit. To re-enable
ingestion safely: fetch only permitted feeds, write to a `pending_review` queue, classify with the `RadarItem` schema
(story geography, financing kind, amount basis), verify publication dates from source metadata, and publish only
after editorial approval. Do not ingest whole-site feeds (e.g. a newspaper's main RSS).

## Dependencies remaining

See [outstanding-dependencies.md](outstanding-dependencies.md).
