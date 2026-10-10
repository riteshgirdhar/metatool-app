# Test and performance report

Run date: 10 October 2026. Environment: Node 22.22, Astro 7.3.8, Playwright 1.64 with Chromium 141 (only engine
available), Lighthouse 13.5.0. All results are **lab** measurements on a local server — not field data.

## Summary

| Suite | Command | Result |
|---|---|---|
| Typecheck | `npm run check` (astro check) | 0 errors, 0 warnings |
| Project lint | `npm run lint` | 108 files clean; all dependencies pinned |
| Unit (handlers, auth rules, Radar rules, ICS, pricing/festival facts, leak scan) | `npm run test:unit` | 20 / 20 pass |
| Browser (public + journeys) | `npm run test:e2e` | 246 pass, 4 skipped (desktop-only menu tests in the mobile project), 0 fail |
| Accessibility (axe, WCAG 2.0/2.1/2.2 A+AA + best practice) | in e2e | 56 templates: 0 critical, 0 serious, 0 moderate |
| Links/assets/anchors | in e2e | 132 pages, 325 targets, 0 problems |
| Build | `npm run build` | 133 pages; 70 + 21 URLs in sitemaps; 41 private pages excluded |

## Defects found by the tests and fixed

| Defect | Fix |
|---|---|
| Horizontal overflow at 320–360 px (tables/previews widened grid columns) | `min-width: 0` on grid/flex children |
| Header crowding at ≤ 390 px (search icon not hidden; "Join free" wrapped) | Specificity fix, `nowrap`, wordmark visually hidden ≤ 374 px |
| Brand link touch target 28 px | `min-height: 44px` |
| Login loop when the server rejects a still-stored session | Local sign-out before redirecting to login |
| ICS semicolons not escaped | Escape fixed; unit-tested |
| Referral qualification could precede attribution | Attribute before onboarding |
| `opener` global collision (type error) | Module scope |
| Missing `h1` in signed-out member area; skipped heading levels on 4 pages | Structure fixed; axe gate raised to fail on moderate |

## Lighthouse (lab, local server, simulated throttling)

| Page | Form factor | Perf | A11y | Best practices | SEO (preview) | LCP | CLS | TBT | Transfer |
|---|---|---|---|---|---|---|---|---|---|
| Home | mobile | 100 | 100 | 100 | 66* | 1.2 s | 0 | 0 ms | 62 KiB |
| Home | desktop | 100 | 100 | 100 | 66* | 0.3 s | 0 | 0 ms | 62 KiB |
| Radar | mobile | 100 | 100 | 100 | 66* | 1.2 s | 0 | 0 ms | 62 KiB |
| Radar item | mobile | 100 | 100 | 100 | 66* | 1.2 s | 0 | 0 ms | 59 KiB |
| Academy guide | mobile | 100 | 100 | 100 | 66* | 1.2 s | 0 | 0 ms | 59 KiB |
| Startups | mobile | 100 | 100 | 100 | 66* | 1.2 s | 0 | 0 ms | 60 KiB |
| Festival | mobile | 100 | 100 | 100 | 66* | 1.4 s | 0 | 0 ms | 63 KiB |
| Contact | mobile | 100 | 100 | 100 | 66* | 1.4 s | 0 | 0 ms | 63 KiB |

Desktop runs for every page above scored 100/100/100 with LCP 0.3 s (full table: `reports/lighthouse-summary.json`).

\* SEO 66 is caused only by the `is-crawlable` audit — the intentional preview `noindex`. An otherwise identical
build with `SITE_INDEXABLE=true` scored **SEO 100** on Home, a Radar item and the Academy index.

Caveats: local server latency is near zero, so real-network LCP will be higher. Field Core Web Vitals (LCP ≤ 2.5 s,
INP ≤ 200 ms, CLS ≤ 0.1 at p75) can only be measured after launch with real traffic (CrUX or RUM).

## Payload budget

| Page | JS executed on load (gzip) | Notes |
|---|---|---|
| Home | ~1.2 KiB inline (menus) | No framework runtime |
| Radar | ~1.6 KiB | Filter script |
| Directory detail | ~6 KiB | Form + member gate; Supabase SDK (53 KiB gz) only if a stored session exists |
| Contact | ~4 KiB | Form controller |
| Login / signup | ~5.6 KiB + 53 KiB SDK on demand | SDK needed for authentication |
| CSS (all pages) | 5.3 KiB gzip | One stylesheet, fingerprinted |
| Font | 47 KiB woff2, preloaded, latin subset | Self-hosted Inter (OFL) |

No hero photograph is used (see image manifest), so there is no image LCP; the LCP element is the hero heading.

## Reproduce

```bash
npm ci
npm run build && npm run build:e2e
npx playwright test               # needs Chromium; set PW_CHROMIUM to another binary if required
npm run test:unit && npm run check && npm run lint
node scripts/serve.mjs & bash scripts/lighthouse.sh
```
