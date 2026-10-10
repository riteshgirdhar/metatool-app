# Feature parity and status matrix

Status: **Preserved** (kept, equivalent), **Repaired** (kept and fixed), **Deferred** (intentionally not built yet,
with a placeholder that says so), **Blocked** (needs access, credentials or a decision).

| Feature | Old site (from brief/backend) | Rebuild | Status | Notes |
|---|---|---|---|---|
| Positioning & homepage | Concept-heavy, posters, empty proof | 12-part homepage, product preview, real actions | Repaired | |
| Navigation & mobile menu | Hidden/aria mismatch, duplicate labels | Shared config, synced ARIA, focus-trapped drawer | Repaired | |
| Founder OS | Workspace (Founder OS tables exist, 0 rows) | Explainer page + signup → onboarding → member area | Repaired / Deferred | Readiness scoring engine not rebuilt; onboarding stores profile; dashboard shows next steps |
| Signup / login / reset / verify | Browser fallbacks reported | Supabase Auth only, no fallback, full journeys tested | Repaired | Needs Supabase env vars to go live |
| Role-specific onboarding | — | Founder / investor / mentor / partner / other | Repaired | |
| Investor verification | Self-selected role | Application + server-side `app_metadata` flag | Repaired | Admin review tooling: Blocked (needs backend decision) |
| Startup / investor / mentor directories | Demo data, signup-only profiles | Public detail pages, member API, filters | Repaired | Content is still demo — real profiles Blocked on onboarding |
| Introductions & mentor requests | — | Auth-only form, stored with reference | Repaired | Routing to recipients: Deferred |
| Radar feeds & editions | Misclassified, wrong geography | One model, corrected dataset, 6 editions, detail pages | Repaired | Automated ingestion not rebuilt (see backend notes) |
| Radar submissions | `radar-submit` function | Durable form, editorial queue | Repaired | |
| Radar save / share | `radar_saves` table | Share (Web Share/clipboard); save on device | Repaired | Server-side saves: Deferred |
| Radar sitemap | `radar-sitemap` function | Static `sitemap-radar.xml` | Preserved | |
| Opportunities & calendars | Sample listings; broken `.ics` | 2 genuine calls; RFC 5545 generator for confirmed dates | Repaired | |
| Academy | 9 tracks, 45 modules | 9 tracks, 5 full guides | Repaired / Deferred | Remaining modules: Deferred (content) |
| Toolkit | 29 products in DB | 8 real downloadable templates | Repaired | Others: Deferred (content not available) |
| Startup Roof TV | Sample streams, concept art, E1 numbering | Working-title shows, sequential planned episodes, hash redirects | Repaired / Deferred | Real episodes, captions, entitlements: Blocked (no licensed content) |
| TV learning / watchlist / progress | Planned | Page + empty state | Deferred | |
| Live | Planned | Page + empty state | Deferred | |
| Community | Planned | Explainer, distinct from Stories | Deferred | |
| Stories / media | Mixed with Community | Editorial section (3 real posts) | Repaired | |
| Marketplace | — | Provider application + empty state | Deferred | No approved providers |
| Referrals | `referral-code` function, tables | Server-side codes, attribution, qualification | Repaired | Rewards: Blocked (terms not approved) |
| Founder Festival | Inconsistent counts/prices | Planning-status page from central config | Repaired | Venue, zones, tickets: Blocked (pending decisions) |
| Pitch / exhibitors / sponsors | Forms | Durable forms | Repaired | |
| Accelerator / incubator | Programme pages | Interest registration | Deferred | Programme details pending |
| Partners | Placeholder logos | No logos; enquiry form | Repaired | |
| Pricing | Pending, inconsistent | Central config, all pending except free | Repaired | |
| Contact / support | Inboxes "being configured" | Durable form with reference; Help centre | Repaired | Inbox notification: Blocked (no mail provider) |
| Legal pages | Placeholders | Factual drafts, labelled, noindex | Repaired / Blocked | Counsel review required |
| Search | Hard-coded list | Content-model index | Repaired | Member search: Deferred |
| AI companion | `ai-companion` function | Not rebuilt | Deferred | Out of scope; needs product decision |
| Ambassador applications | Table exists | Not rebuilt | Deferred | |
| Payments / subscriptions | Tables, not active | Not built | Blocked | No approved prices; no charges |
