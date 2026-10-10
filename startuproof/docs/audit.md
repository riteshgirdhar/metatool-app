# Startup Roof — audit of the current site (startuproof.com)

Date: 10 October 2026 · Auditor: Claude Code (remote session)

## 1. Scope and what could actually be inspected

| Source | Access | Result |
|---|---|---|
| Live site `https://startuproof.com` (HTML, JS, assets, sitemaps, robots) | **Blocked.** The session's outbound network policy denies `startuproof.com`, `*.netlify.app` and `api.netlify.com` (proxy `CONNECT 403`). WebFetch also failed (DNS). | No browser crawl, no screenshots of the live site, no inspection of the published JavaScript. |
| Original source / Genspark export | None supplied. No Startup Roof repository exists in the connected GitHub account (only `dugasta-inventory`, `rine-talks`, `metatool-app`). | Original frontend source not recovered. |
| Netlify (authenticated connector, read-only) | Available | Production project identified, deploy metadata, function list, redirect/header counts. |
| Supabase (authenticated connector, read-only SQL + advisors) | Available | Two backend projects inspected: schemas, row counts, RLS policies, signup trigger, Radar data. |

**Consequence:** this audit is backend-evidence-based. Findings marked **Observed** were verified directly in the
database, function source or Netlify metadata. Findings marked **Reported (not re-verified)** come from the brief and
could not be re-checked against the live frontend from this environment. Nothing here claims a complete
functional test of the current site.

Raw evidence: [`evidence/backend-findings.md`](evidence/backend-findings.md).

## 2. Infrastructure observed

- Netlify production project `kaleidoscopic-tarsier-24d467` → `startuproof.com`; latest deploy
  `6aca61af151141a66e773183` "Final: TV/Academy alignment (static tv page)", CLI deploy, no Git link, 44 redirect
  rules, 6 header rules, Netlify Forms not enabled.
- 15 Netlify Functions including `diag`, `direct`, `mig`, `sweep`, `sweep2` (~173 KB each) whose names suggest
  diagnostics/migration utilities left deployed in production.
- Also in the team: `startuproof-v2`, `startuproof-staging`, `startuproof-founder-os` (untouched).
- Supabase `startup-roof` (core, 6 migrations) and `startuproof` (Radar/referrals/TV, no recorded migrations).

## 3. Issues

Priority: P0 security/data loss · P1 broken journey or misleading content · P2 quality · P3 polish.

| # | Area | URL / component | Priority | Status | Evidence | Impact | Correction in rebuild |
|---|---|---|---|---|---|---|---|
| A1 | Auth | Signup trigger `public.handle_new_user()` | P0 | **Observed** | Function source assigns `profiles.role` from `raw_user_meta_data->>'role'` (user-supplied at signup). | Selecting "Investor" grants investor role; investor-gated RLS (`investors insert own`, financials reads via `my_role()`) then applies without verification. | Rebuild never trusts user metadata: authorization reads only server-controlled `app_metadata.investor_verified` (`netlify/lib/auth.ts`). Proposed DB fix in `supabase/proposed/20261010_harden_roles_and_views.sql`. Tested: `journeys/auth.spec.ts` "choosing Investor at signup does not unlock…". |
| A2 | Auth | View `public.profiles_admin` | P0 | **Observed** (Supabase advisor ERROR 0002/0010) | View exposes `auth.users` and is SECURITY DEFINER, reachable by `anon`. | Possible exposure of account data via REST. | Proposed migration revokes access and sets `security_invoker`. |
| A3 | Auth | Browser fallback signup storing plaintext passwords in `localStorage`; local login fallback; browser-stored roles | P0 | **Reported (not re-verified)** — published JS not reachable | Brief. | Credential exposure; fake accounts; client-side privilege. | No local fallback exists. When the identity provider is not configured or down, forms are disabled with an explanation. Tests assert no password in storage and no session on outage. |
| A4 | Auth | Anonymous-executable SECURITY DEFINER functions (`is_admin`, `my_role`, `protect_admin_columns`, …) | P2 | **Observed** (advisor WARN 0028/0029) | | Information leakage; larger attack surface. | Proposed `revoke execute`. |
| A5 | Auth | Rate limiting in submit RPCs keyed on client-supplied `p_rl_key` | P2 | **Observed** (function signatures) | | Bypassable throttling. | Rebuild rate-limits on a salted server-side hash of the client IP. |
| A6 | Auth | Leaked-password protection disabled | P2 | **Observed** (advisor) | | Weak passwords accepted. | Dashboard toggle listed in migration notes. |
| F1 | Forms | Handlers reporting success after failed requests or local-only storage | P0 | **Reported (not re-verified)** | Brief. Contact table holds 7 rows, waitlist 7 — some submissions do reach the DB. | Lost enquiries; false confirmation. | Success shown only after a 2xx response containing a server reference, produced after the durable write. Tested with 500, network abort, slow, 422 and replay cases. |
| N1 | Navigation | Ecosystem/Resources panels visible while `aria-expanded=false`; CSS `display` overriding `hidden` | P1 | **Reported (not re-verified)** | Brief. | Overlapping menus, screen-reader mismatch. | Global `[hidden]{display:none!important}`; one function writes `hidden` and `aria-expanded` together. Tested. |
| N2 | Navigation | Two "Community" links to `/media` and `/community`; "Help Centre" → `/contact` | P2 | **Reported** | Brief. | Mislabelled destinations. | Community → `/community/`; Stories (editorial) → `/media/`; Help centre → `/support/`. Tested. |
| H1 | Homepage | Repeated diagrams, poster collection, empty proof sections, "BACK TO CONTENTS" captions | P1 | **Reported** | Brief. | Unfinished impression; weak hierarchy. | New homepage follows the 12-part brief; posters and concept material removed from primary pages; empty proof/team sections omitted. |
| R1 | Radar | UAE edition contains Egypt stories | P1 | **Observed** | `country=uae` on EFG/EBRD Egypt loan, NVIDIA×RiseUp Cairo, Beltone/Amtaar Egypt fund. | Wrong geography. | Items carry `storyGeography`; cross-border inclusion needs a stated `connectionNote`. Unit + e2e tests. |
| R2 | Radar | Unrelated general news published (politics, conflict, sport, consumer gadgets) | P1 | **Observed** | 19 published items (Iraq, Syria, Gaza aid, Yemen, Ronaldo, cricket, Nol tickets, keyboards…). Feed "The National — Technology" ingests the whole site. | Credibility. | Excluded with reasons (`EXCLUDED` in `src/data/radar.ts`). |
| R3 | Radar | US–Russia energy article stored as `funding_round` | P1 | **Observed** | | Misleading funding tracker. | Excluded; financing kinds are explicit. |
| R4 | Radar | `financing_type = 'undisclosed'` on every funding row, including disclosed amounts | P1 | **Observed** | e.g. erad $22M Series A. | Data unusable for filtering. | Distinct kinds: equity round, undisclosed investment, debt, acquisition, investment plan, fund close, fund target, secondary, market data. Amount carries a `basis`. |
| R5 | Radar | Investment plans, loans, fund closes and market totals presented as rounds | P1 | **Observed** | Huspy $86M plan, EFG $40M loan, Endeavor $320M fund, "$1.1B September" total. | Overstated activity. | Reclassified; summaries say what the figure is. |
| R6 | Radar | `published_at` = collection day while URLs show `/2026/09/` | P1 | **Observed** | | Wrong dates. | Show "Collected" date; publication date shown only when verified; URL month shown as a hint only. |
| R7 | Radar | Generic initial HTML title/description on article URLs | P1 | **Reported** | Brief; `radar-item` function exists. | Poor sharing and SEO. | Every Radar item is statically rendered with unique title, description, canonical and OG. Tested on every built page. |
| D1 | Directories | "View profile" links to signup; no public detail pages | P1 | **Reported** | Brief. | Dead-end journeys. | Public detail pages for every listed profile; member-only fields served by an authenticated API. |
| D2 | Directories | All startups, investors, mentors and partners are demo data; mentors show VERIFIED and DEMO together | P1 | **Observed** (all `is_demo=true`) / badge **Reported** | | Misrepresentation. | "Demo profile" label everywhere, noindex, excluded from sitemap/search, no verification badges; lint forbids `VERIFIED`. |
| D3 | Directories | Partner "logos" are placeholders (`Title Sponsor`, `Media Partner`…) | P1 | **Observed** (`is_confirmed=false`) | | Invented partners. | No partner or sponsor logos shown. |
| O1 | Opportunities | 10 of 12 opportunities are "SAMPLE … for illustration" with `example.com` apply links | P1 | **Observed** | | Dead links, false opportunities. | Only the 2 genuine Startup Roof calls are listed. |
| O2 | Calendars | `.ics` downloads lack date and identifier fields | P1 | **Reported** | Brief. | Calendar imports fail. | RFC 5545 generator with UID, DTSTAMP, all-day DTSTART/DTEND, escaping and folding (unit-tested); offered only for confirmed dates. |
| T1 | TV | Catalogue uses third-party sample streams and concept art; later episodes labelled E1 | P1 | **Reported** | Brief; `videos`, `content_series` tables are empty (0 rows). | Misrepresents original programming. | No sample streams. Working-title shows with sequential planned episodes, honest unavailable state, no player libraries loaded. |
| C1 | Commercial | Prices/payment pending; price ranges and Festival zone counts differ between pages | P1 | **Reported** | `subscription_plans` has 4 rows (contents not reviewed). | Conflicting commitments. | Single config `src/config/site.ts`; unapproved values are `null` and render as pending. |
| C2 | Trust | Inboxes "being configured"; legal pages placeholders; empty team cards | P1 | **Reported** | | Low trust. | Contact via durable form with reference; legal pages factual and marked "Draft — pending legal review" (noindex); team section states profiles will be published with consent. |
| S1 | Search | Hard-coded small page list | P2 | **Reported** | | Search misses content. | Build-time index from the same content model (pages, Radar, Academy, Toolkit, Stories, opportunities). |
| X1 | Ops | Diagnostic-looking functions (`diag`, `direct`, `mig`, `sweep`, `sweep2`) in production | P2 | **Observed (names only)** | Netlify deploy metadata. | Possible unintended admin surface. | Not carried over. Recommend reviewing/removing on the current site. |

## 4. Coverage that could not be performed (and why)

Live crawl of every route, interaction testing of the current site (menus, drawers, forms, auth, downloads, TV
playback, Radar country pages), before-screenshots, live Lighthouse baselines, external-link checks and inspection of
the published JavaScript were **not possible** because outbound access to the live site is blocked in this
environment. The route inventory therefore lists original routes from the brief and the backend, marked
"not crawled". See [outstanding dependencies](outstanding-dependencies.md) for how to complete this.

## 5. Verified behaviour of the replacement

See [test-and-performance-report.md](test-and-performance-report.md) and
[interaction-evidence.md](interaction-evidence.md).
