# Original → new route map and domain migration checklist

Full per-route list: [`route-inventory.csv`](route-inventory.csv).

## Route map (summary)

| Original | New | Mechanism |
|---|---|---|
| `/`, `/founder-os`, `/startups`, `/investors`, `/mentors`, `/opportunities`, `/academy`, `/toolkit`, `/community`, `/marketplace`, `/referrals`, `/festival`, `/partners`, `/sponsors`, `/exhibitors`, `/pitch`, `/accelerator`, `/incubator`, `/about`, `/contact`, `/faq`, `/pricing`, `/privacy`, `/terms`, `/cookie`, `/conduct`, `/acceptable-use`, `/investment-disclaimer`, `/signup`, `/login`, `/forgot`, `/app/` | Same path with trailing slash | Netlify pretty URLs (301 to slash) |
| `/media` (mixed news/community) | `/media/` = Startup Roof editorial; third-party news → `/radar/` | Content split |
| Radar country pages | `/radar/{uae,saudi,qatar,egypt,india,global}/` | Static pages |
| Radar items (served by `radar-item` function) | `/radar/item/<slug>/` | **Old item URL format unknown** — confirm and add `[[redirects]]` once the live site can be crawled |
| `/tv/#…` hash states | `/tv/shows/<show>/`, `/tv/shows/<show>/<episode>/`, `/tv/learning/`, `/tv/live/` | Client-side redirect script on `/tv/` |
| Legacy aliases (assumed) `/forgot-password`, `/register`, `/help`, `/cookies`, `/news`, `/dashboard`, `/tv/watch/*` | `/forgot/`, `/signup/`, `/support/`, `/cookie/`, `/radar/`, `/app/`, `/tv/` | 301 in `netlify.toml` |

## Domain migration checklist (do not start until approved)

**Before**
- [ ] Crawl the current site (allow `startuproof.com` in the session network policy) and diff its URLs against `route-inventory.csv`; add 301s for every URL with traffic or backlinks, especially Radar item URLs.
- [ ] Choose the Supabase project for production auth; apply and test `supabase/proposed/20261010_harden_roles_and_views.sql` on a branch first.
- [ ] Set environment variables on the new Netlify project (see README).
- [ ] Supabase Auth → URL configuration: Site URL `https://startuproof.com`; additional redirect URLs `https://startuproof.com/auth/callback/`, `https://startuproof.com/reset/`, plus the netlify.app URL for preview.
- [ ] Supabase email templates: use the PKCE `{{ .ConfirmationURL }}`; configure a real SMTP provider (built-in sender is rate-limited).
- [ ] Confirm legal pages with counsel; replace interim logo; add approved photography.
- [ ] Decide on the old site's functions (`diag`, `direct`, `mig`, `sweep*`): remove from production.

**Switch**
- [ ] Set `SITE_INDEXABLE=true` and remove the `X-Robots-Tag` header block in `netlify.toml`; redeploy. Verify `robots.txt` now allows crawling and lists `sitemap.xml`.
- [ ] Canonicals already point to `https://startuproof.com/…` — verify after DNS.
- [ ] In Netlify: add `startuproof.com` + `www` as domains on `startuproof-rebuild`, **after** removing them from `kaleidoscopic-tarsier-24d467`. Keep the old project (unpublished) for rollback.
- [ ] Update `connect-src` in the CSP if the Supabase URL changes; add any analytics origin deliberately.
- [ ] `SR_ALLOWED_ORIGINS=https://startuproof.com,https://www.startuproof.com`.

**After (smoke tests on the live domain)**
- [ ] `GET /api/health` → `{"auth":"configured"}`.
- [ ] Real signup with a team mailbox: email arrives, link opens `/auth/callback/`, lands on onboarding.
- [ ] Login/logout, password reset, resend verification, expired link.
- [ ] Submit contact + pitch forms; confirm records in Netlify Blobs (`submissions` store) and references shown.
- [ ] Investor account: confirm no investor-only data until `app_metadata.investor_verified` is set.
- [ ] `curl -I` a sample of old URLs → 301 to the right new URL; unknown URL → 404.
- [ ] Submit `sitemap.xml` in Search Console; check coverage for demo/private pages being excluded.
- [ ] Monitor field Core Web Vitals and function error logs for two weeks.
