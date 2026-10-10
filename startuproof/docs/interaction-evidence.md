# Link and interaction evidence — replacement site

All checks ran on 10 October 2026 against the production build (`dist/`) served by `scripts/serve.mjs`, which mimics
Netlify (pretty URLs, real 404s, content types, function routing). **Browser engine actually used: Chromium 141
(Playwright 1.64).** Firefox and WebKit were not available in this environment and were not run.

Machine-readable outputs: `reports/e2e-results.json`, `reports/link-report.json`, `reports/axe/*.json`,
`reports/lighthouse/*.json`, `reports/lighthouse-summary.json`.

## Links, assets and anchors

| Check | Result |
|---|---|
| Built HTML routes crawled | 132 |
| Unique internal targets (pages, CSS, JS, fonts, images, downloads, JSON, XML) | 325 |
| Non-200 responses | 0 |
| MIME mismatches (e.g. HTML served for JS/JSON) | 0 |
| Broken `#anchors` | 0 |
| Buttons without accessible names | 0 |
| Unknown routes (`/does-not-exist/`, unknown Radar item, startup, episode) | Return **HTTP 404** with the 404 page (no soft 200) |
| External links | Inventoried in `link-report.json` (Wamda and Inc42 source articles). **Not fetched** — outbound requests are blocked here; an automated block would not prove a link broken anyway. |

## Interaction matrix (all automated, all passing)

| Interaction | Desktop | Mobile (Pixel 7 emulation) | Spec |
|---|---|---|---|
| Dropdown menus: `hidden` and `aria-expanded` in sync, one open at a time, Escape returns focus, outside click closes | ✔ | n/a | `public/nav.spec.ts` |
| Keyboard: ArrowDown into menu, arrow navigation, Tab-out closes | ✔ | n/a | `public/nav.spec.ts` |
| Accurate labels: Community → /community/, Stories → /media/, Help centre → /support/ | ✔ | n/a | `public/nav.spec.ts` |
| Active section indication | ✔ | n/a | `public/nav.spec.ts` |
| Mobile drawer: open, focus trap, Escape, focus return, touch navigation | ✔ | ✔ | `public/nav.spec.ts` |
| Touch targets ≥ 40 px (44 px design) in header and drawer | ✔ | ✔ | `public/nav.spec.ts` |
| Forms: success only with server reference | ✔ | ✔ | `public/forms.spec.ts` |
| Forms: 500 error → "Not sent", input kept, retry reuses idempotency key | ✔ | ✔ | `public/forms.spec.ts` |
| Forms: network failure, slow request pending state, client & server validation | ✔ | ✔ | `public/forms.spec.ts` |
| API: honeypot, too-fast, duplicate replay, invalid payload, unknown form | ✔ | ✔ | `public/forms.spec.ts` |
| Radar filters in shareable URLs, empty state, UAE edition relevance | ✔ | — | `public/forms.spec.ts` |
| Directory filter by URL | ✔ | — | `public/forms.spec.ts` |
| Auth unavailable: signup/login disabled, no local accounts, nothing stored | ✔ | — | `public/auth-unavailable.spec.ts` |
| Protected APIs refuse anonymous and forged tokens | ✔ | — | `public/auth-unavailable.spec.ts` |
| Gated intro request keeps the draft and links to login with `next` + `intent` | ✔ | — | `public/auth-unavailable.spec.ts` |
| Private directory data absent from public HTML | ✔ | — | `public/auth-unavailable.spec.ts` + `unit/content.test.mjs` |
| TV legacy hash links → path URLs; sequential episodes; unavailable stream, no player loaded | ✔ | — | `public/auth-unavailable.spec.ts` |
| Calendar file not offered for provisional dates (404 for `.ics`) | ✔ | — | `public/auth-unavailable.spec.ts` |
| Every page: 200, one `h1`, description, canonical, noindex, OG image, no overflow at 360 px, no console errors | ✔ (132 pages) | — | `public/routes.spec.ts` |
| Unique titles and descriptions across the build | ✔ | — | `public/routes.spec.ts` |
| Sitemaps exclude demo/private pages; search index excludes demo profiles | ✔ | — | `public/routes.spec.ts` |

## Critical journeys (test build wired to a local Supabase Auth mock)

The mock (`scripts/mock-supabase.mjs`) implements the Supabase Auth REST endpoints used by `supabase-js`
(signup, PKCE code exchange, password grant, recover, resend, user get/update, logout). It is loaded only by the
local server and refuses to run on Netlify. Both the browser SDK and the server functions talk to it, so the
server-side authorization path is exercised for real.

| Journey | Result |
|---|---|
| Founder: signup → "check your email" → verification link → onboarding → member area → logout → login | ✔ |
| Password never written to browser storage during signup | ✔ |
| Login preserves destination and pending action (intro request draft restored and submitted) | ✔ |
| Member sees member-only fields; investor-only fields withheld | ✔ |
| Unverified email cannot log in; resend issues a fresh link | ✔ |
| Wrong password: clear error, no session | ✔ |
| Reused / expired verification link handled | ✔ |
| Password reset: request → link → new password → login with new password | ✔ |
| Forgot password does not reveal whether an account exists | ✔ |
| Expired reset link shows recovery path | ✔ |
| Server-detected session expiry → local session cleared → login | ✔ |
| Investor at signup gets **no** investor access; self-editing `user_metadata` has no effect; only server-side `app_metadata` change grants access | ✔ |
| Investor verification submission stored with reference | ✔ |
| Members see members-only investors; anonymous API call refused | ✔ |
| Referrals: self-referral blocked, one attribution per account, qualification after onboarding, counts shown to referrer only | ✔ |
| Identity-provider outage: login fails visibly, no session created | ✔ |

## Viewports, zoom, motion

| Check | Result |
|---|---|
| 320 px reflow on all 56 template URLs | No horizontal overflow |
| 360 px on all 132 pages | No horizontal overflow |
| 640 px CSS viewport (≈200% zoom at 1280) on 5 key pages | No horizontal overflow |
| Screenshots at 320, 360, 390, 430, 768, 1024, 1280, 1440, 1920 + 844×390 landscape | `docs/screenshots/after/widths/` (inspected) |
| Reduced motion | Animations reduced to ~0 (asserted) |
| Skip link and visible focus | Asserted |

## Not covered

- Real email delivery, real Supabase project and real Netlify Blobs (no credentials/network). Covered by the mock
  and in-memory store locally; must be smoke-tested after deploy (see `route-map-and-migration.md`).
- Firefox and Safari/WebKit engines; real touch devices; screen-reader manual pass (VoiceOver/NVDA).
- The original live site (network blocked).
