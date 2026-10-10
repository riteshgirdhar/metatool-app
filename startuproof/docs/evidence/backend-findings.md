# Backend evidence (read-only inspection, 2026-10-10)

All queries were read-only (`SELECT`, catalog queries, Supabase security advisors) run through the
authenticated Supabase connector. No data or schema was modified.

## Projects discovered

| Supabase project | Ref | Created | Role inferred |
|---|---|---|---|
| `startup-roof` | `nxtzbidikgkasfhswhen` | 2026-10-07 | Platform core: profiles, directories, Academy, events, forms (6 migrations) |
| `startuproof` | `zxhgrxfuqfbfwxgxejqa` | 2026-10-08 | Radar, referrals, TV, Founder OS tables (no migrations recorded — schema applied ad hoc) |

Netlify: production site `kaleidoscopic-tarsier-24d467` (startuproof.com), deploy `6aca61af151141a66e773183`
("Final: TV/Academy alignment (static tv page)"), CLI deploy, no linked Git repository, `has_source_zip: false`,
44 redirect rules, 6 header rules, 15 functions (`ai-companion`, `applications`, `diag`, `direct`, `entitlements`,
`mig`, `radar-collect`, `radar-item`, `radar-run`, `radar-sitemap`, `radar-submit`, `referral-code`, `sweep`,
`sweep2`, `waitlist`). Functions `diag`, `direct`, `mig`, `sweep`, `sweep2` (~173 KB each) look like
maintenance/diagnostic utilities left deployed in production — **observed name/size only; behaviour not inspected**.

## Directory data (startup-roof)

- `startups`: 9 rows — 8 `is_demo=true` (Nimbus Ledger, Saffron Health, Dune Robotics, Majlis Learn, Portside,
  Verdant Grid, Kahwa Club, Falcon Stack) + 1 empty QA row (`QA Co`).
- `investors`: 9 rows — 8 `is_demo=true` + 1 QA row (`QA Investor`).
- `mentors`: 6 rows, all `is_demo=true`.
- `partners`: 6 rows, all placeholders (`Title Sponsor`, `Media Partner` …), `is_confirmed=false`.
- `opportunities`: 12 rows — 10 `is_demo=true` ("SAMPLE opportunity for illustration", `apply_url=https://example.com`),
  2 genuine Startup Roof calls (Founder Festival Pitch Studio 2027, Startup Market 2027).
- `events`: Founder Festival Dubai 2027 stored as 26–28 Mar 2027, venue "to be announced"; Capital Night 25 Mar 2027;
  5 further rows are `is_demo=true`.
- `learning_tracks`: 9 published tracks (non-demo titles/outcomes), 45 modules.

**Implication:** there are no genuine approved member profiles to publish. The rebuild renders demo records only
under explicit "Demo profile" labelling, excluded from sitemap and search indexing.

## Authorization findings (startup-roof)

1. **Self-selected investor role (HIGH, observed in function source).** `public.handle_new_user()` reads
   `new.raw_user_meta_data->>'role'` — user-supplied at signup — and writes `investor`/`mentor`/`partner`/`corporate`
   straight into `profiles.role`. `investors insert own` RLS then allows that user to create an investor record, and
   `my_role()` drives gated reads. Choosing "Investor" therefore grants investor-tier access without verification.
   Fix: always create `founder`/`member`, store the *requested* role separately, and grant `investor_verified` only via an
   admin-controlled table or `app_metadata`.
2. **`profiles_admin` view exposes `auth.users` to `anon` (ERROR, Supabase advisor `0002_auth_users_exposed`)** and is
   `SECURITY DEFINER` (`0010`). Same for `deal_desk_matches_investor`.
3. `is_admin()`, `my_role()`, `protect_admin_columns()`, `admin_metrics()` and public submit RPCs are `SECURITY DEFINER`
   and executable by `anon`/`authenticated` (advisor `0028`/`0029`, WARN). Submit RPCs are intentionally public but
   carry a client-supplied `p_rl_key` rate-limit key — rate limiting keyed on a client value is bypassable.
4. Leaked-password protection disabled (advisor WARN).
5. Positive: RLS enabled on every table; `protect_admin_columns` trigger blocks non-admins from changing
   `role`, `is_demo`, `is_featured`, `owner_id`; `profiles update own` pins `role`.

## Radar data quality (startuproof)

119 rows in `radar_items` (≈48 `published`, the rest `pending_review`). Observations on published rows:

| Defect | Example evidence |
|---|---|
| Wrong edition geography | `country=uae`: "EFG Holding secures $40 million EBRD loan … in Egypt", "NVIDIA, RiseUp host Cairo reception", "Beltone, Amtaar plan $38 million … fund" (Egypt) |
| Unrelated general news published | "Iraq's Al Sadr seeks statesmanship…", "Israel holding 49 Syrians…", "Cristiano Ronaldo hits 980th career goal", "From Bhuvneshwar Kumar to Mitchell Starc…", "UAE begins food aid airlift to Gaza", "Middle East latest: … Yemen", "Long live the mechanical keyboard" |
| Misclassified financing | "US-Russia energy deal opens up diesel can of worms" stored `kind=funding_round`, `category=funding` |
| Financing type never set | Every funding row has `financing_type='undisclosed'` even when `amount_original` is "$22 million", "$100 million" |
| Investment plan / fund / debt treated as rounds | Huspy "$86 million investment plan" (stored as `policy`), EFG "$40 million EBRD loan" (debt, stored as funding round), Endeavor Catalyst "$320 million" fund close (stored as funding round), "MENA startup funding surges to $1.1 billion" (market report stored as round, `country=saudi`) |
| Publisher ≠ story country | Feed "The National — Technology" pulls the whole site (sport, politics) and tags it UAE |
| Dates | `published_at = 2026-10-10` (collection day) while source URLs carry `/2026/09/`; publication date not verified from source metadata |
| Missing fields | `hq_country`, `market_country`, `why_it_matters` null on all published rows inspected |
| Mis-categorised | "Elon Musk intensifies attack on Ambani…" stored `category=grants`; "US tech roared back…" stored `kind=event` |
