# Startup Roof — rebuilt public site

A rebuild of [startuproof.com](https://startuproof.com) as a separate project: static Astro + TypeScript pages,
Netlify Functions for forms, membership and referrals, and Supabase Auth for identity. It is designed to be
deployed to its own Netlify project (`startuproof-rebuild`) and kept **noindex** until the domain migration is
approved.

> This directory lives on branch `claude/startup-roof-redesign-launch-vxlheu` of `riteshgirdhar/metatool-app`.
> It is self-contained and does not depend on the rest of that repository.

## Documents

| | |
|---|---|
| Audit of the current site | [docs/audit.md](docs/audit.md) · raw evidence [docs/evidence/backend-findings.md](docs/evidence/backend-findings.md) |
| Route inventory | [docs/route-inventory.csv](docs/route-inventory.csv) |
| Link & interaction evidence | [docs/interaction-evidence.md](docs/interaction-evidence.md) |
| Tests & performance | [docs/test-and-performance-report.md](docs/test-and-performance-report.md) |
| Screenshots (after) | `docs/screenshots/after/{desktop,mobile,widths}/` |
| Image rights manifest | [docs/image-manifest.md](docs/image-manifest.md) |
| Feature parity | [docs/feature-parity.md](docs/feature-parity.md) |
| Backend / API notes | [docs/backend-notes.md](docs/backend-notes.md) |
| Route map & migration checklist | [docs/route-map-and-migration.md](docs/route-map-and-migration.md) |
| Outstanding dependencies | [docs/outstanding-dependencies.md](docs/outstanding-dependencies.md) |
| Proposed DB hardening (not applied) | [supabase/proposed/](supabase/proposed/) |

## Setup

Requires Node 22.

```bash
cd startuproof
npm ci
cp .env.example .env      # optional: add Supabase URL + anon key to enable sign-in locally
npm run dev               # http://localhost:4321 (pages only; functions need `netlify dev` or the preview server)
```

## Build, preview, test

```bash
npm run build             # dist/ + sitemaps (postbuild)
npm run preview           # Netlify-like server with real 404s and /api/* functions (in-memory store, test only)
npm run check             # TypeScript / Astro
npm run lint              # project rules: no password storage, no demo logins, pinned deps, …
npm run test:unit         # handlers, auth rules, Radar rules, ICS, leak scan (needs a prior build)
npm run test:e2e          # builds prod + e2e variants, then Playwright (Chromium) incl. auth journeys via a local mock
node scripts/serve.mjs & bash scripts/lighthouse.sh   # lab Lighthouse
node scripts/serve.mjs & node scripts/screenshots.mjs # regenerate screenshots
npm run og                # regenerate social preview images
```

Playwright uses Chromium at `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`; set `PW_CHROMIUM` to use another binary.

## Deployment (Netlify)

`netlify.toml` defines the build (`npm ci && npm run build`), publish dir `dist`, functions dir `netlify/functions`,
security headers (CSP, HSTS, `X-Robots-Tag: noindex`), caching and redirects. There is **no SPA catch-all**:
missing paths return the 404 page with HTTP 404.

Project: `startuproof-rebuild` (team `riteshgirdhar`, site id `d19c1a70-3c9e-4978-91ee-7dc3c06c4e2c`), URL
`https://startuproof-rebuild.netlify.app`. The production site `kaleidoscopic-tarsier-24d467` is not touched.

Deploy options:
1. **Git (recommended):** Netlify → `startuproof-rebuild` → Link repository → `riteshgirdhar/metatool-app`,
   branch `claude/startup-roof-redesign-launch-vxlheu`, base directory `startuproof`. The repo stays authoritative.
2. **CLI:** `npx netlify-cli@latest deploy --build --site d19c1a70-3c9e-4978-91ee-7dc3c06c4e2c` (preview), then add
   `--prod`. Add `.netlify` to `.gitignore` (already done).

### Environment variables (names only)

| Name | Scope | Required | Notes |
|---|---|---|---|
| `PUBLIC_SUPABASE_URL` | build + functions | for sign-in | Supabase project URL (public) |
| `PUBLIC_SUPABASE_ANON_KEY` | build + functions | for sign-in | Anon/publishable key (public by design; RLS enforced) |
| `SR_HASH_SALT` | functions, **secret** | yes | Set on `startuproof-rebuild` (all contexts) |
| `SR_ALLOWED_ORIGINS` | functions | no | Extra allowed form origins |
| `SITE_INDEXABLE` | build | no | `true` only after migration approval |

Without the Supabase variables the site works fully except sign-in, which shows an honest "temporarily
unavailable" message — there is no local fallback.

## Editing content

| What | Where |
|---|---|
| Prices, payment status, feature Live/Beta/Planned/Demo labels, Festival dates/venue/zones, navigation | `src/config/site.ts` |
| Radar items (schema-validated at build; excluded items with reasons) | `src/data/radar.ts` |
| Directory public fields | `src/data/directory.ts`; member/investor-only fields: `netlify/lib/directory-private.ts` |
| Opportunities, Academy tracks & guides, Toolkit list, TV shows, Stories | `src/data/content.ts` |
| Toolkit files | `public/downloads/` |
| Form fields and validation | `src/lib/forms.ts` (server-authoritative) + the page's `<Field>` components |

Rules: never set a price, date, venue or zone count that is not approved — leave it `null`. Opportunity calendar
files are produced only when `dateStatus: 'confirmed'` and a timezone is known. Radar items need a source, a
`storyGeography`, and a `connectionNote` for any cross-border edition.

## Replacing images

See [docs/image-manifest.md](docs/image-manifest.md). Put originals in `src/assets/photos/`, use `<Picture>` with
AVIF/WebP, `sizes`, intrinsic dimensions and `alt`; eager-load only the hero.

## Project layout

```
src/config/site.ts        central facts, nav, statuses
src/data/                 content model (Radar, directory, content)
src/lib/                  forms schemas, ICS generator
src/components/           layout pieces, forms, previews
src/pages/                routes (static), *.ts endpoints (robots, search index, ics)
src/scripts/              small client scripts (nav, forms, auth, member area)
netlify/functions/        function entry points (/api/*)
netlify/lib/              handlers, auth verification, storage
scripts/                  postbuild, preview server, auth mock (test-only), screenshots, lighthouse, og, lint
tests/unit, tests/e2e     node:test and Playwright suites
```
