# Outstanding dependencies

| # | Dependency | Blocks | Who | How to resolve |
|---|---|---|---|---|
| 1 | **Network access from the build session** to `netlify-mcp.netlify.app`, `api.netlify.com`, `netlify.app`, `startuproof.com` | Deploying to the new Netlify project; crawling/screenshotting the live site for the before-audit | Account owner | Session environment → Network access → add those domains (or use "Full" access) and re-run. **Alternative for deploy:** in Netlify, open project `startuproof-rebuild` → Link repository → `riteshgirdhar/metatool-app`, branch `claude/startup-roof-redesign-launch-vxlheu`, base directory `startuproof` (build settings come from `startuproof/netlify.toml`). |
| 2 | Supabase project for the new site's auth | Live signup/login on the preview | Owner decision | Pick staging project; set `PUBLIC_SUPABASE_URL` + `PUBLIC_SUPABASE_ANON_KEY`; configure redirect URLs (see migration checklist). Until then auth pages honestly say sign-in is unavailable. |
| 3 | Email provider (SMTP) for Supabase Auth and form notifications | Reliable verification emails; team notification of submissions | Owner | Configure SMTP in Supabase; add a notification function if desired. |
| 4 | Review of `supabase/proposed/…sql` | Fixing the live site's self-selected investor role and exposed view | Owner + developer | Apply on a branch, test, then production. |
| 5 | Approved logo files and brand guidelines | Final brand assets | Owner | Replace `Logo.astro`, `favicon.svg`, `og/*`. |
| 6 | Genuine photography with consent | Imagery on primary pages | Owner | See image manifest. |
| 7 | Approved prices, Festival venue/zones/tickets, programme terms, referral reward terms | Pricing, Festival, programmes, referrals | Owner | Edit `src/config/site.ts` and `src/data/content.ts`. |
| 8 | Legal review | Privacy, terms, cookies, conduct, acceptable use, disclaimer | Counsel | Replace drafts; remove "Draft" banner and `noindex` on legal pages. |
| 9 | Real member profiles and investor verification process | Directory content, verified badges | Operations | Onboard members; admin sets `app_metadata.investor_verified`. |
| 10 | Licensed TV content, captions, entitlements | TV playback | Content | Add episodes with stream URLs and captions; lazy-load a player only on episode pages; enforce premium access server-side. |
| 11 | Old Radar item URL format | Exact 301s | Developer | Crawl live site (needs #1). |
| 12 | Firefox/WebKit and real-device testing; screen-reader manual pass | Cross-engine evidence | QA | Run `npx playwright test` with those engines installed; manual VoiceOver/NVDA pass. |
