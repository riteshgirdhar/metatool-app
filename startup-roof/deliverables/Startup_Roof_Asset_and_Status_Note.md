# Startup Roof: asset and status note

Internal note for the project team. Do not share it with the presentation or the brochure.

Updated 10 October 2026, after the full edition was produced.

## Deliverables

| File | Format | Purpose |
|---|---|---|
| `Startup_Roof_Full_Presentation.pptx` / `.pdf` | **77 slides**, 16:9. 8 chapters, each with a divider slide. | The full edition. It has native, editable PowerPoint charts, infographics, illustrative product screens and presenter notes on every slide. |
| `Startup_Roof_Full_Brochure.pdf` | **34 pages**, A4 portrait | The full brochure: data pages, stage checklists, Founder OS screens, model, pilot, risks, FAQ, glossary and sources. |
| `Startup_Roof_General_Presentation.pptx` / `.pdf` | 20 slides, 16:9 | The short version, for meetings. |
| `Startup_Roof_Project_Brochure.pdf` | 12 pages, A4 | The short brochure, for WhatsApp. |

**Contents of the full edition:**
1. Why founders need a roof (the founder problem, failure reasons, survival, evidence for support, MENA funding, UAE context, UAE founders, AI adoption)
2. The concept (ecosystem, four pillars, audiences, sectors, personas, value exchange, four-layer model)
3. The founder journey (six stages with checklists, startup metrics, funding options, funding stages)
4. Founder OS (onboarding, next-step engine, scenario, matching, opportunities, service requests, milestones, architecture, trust, build priorities)
5. Ecosystem services (AI with human support, community, year-round rhythm, mentoring, Academy and curriculum, expert services and catalogue, insights, incubation, investor readiness)
6. Value for investors, partners, universities and corporates
7. Model, pilot and roadmap (commercial model, revenue matrix, service economics, pilot design, KPIs, roadmap, milestone path, risks)
8. People and participation (capabilities, ways to contribute, FAQ, glossary, sources, invitation)

The generator sources are in `../src/`. The short deck is built by `build_deck.py`, the full deck by `build_full.py`, and the full brochure by `build_brochure_full.py`.

## 1. Websites: not reachable

| Site | Result on 10 Oct 2026 |
|---|---|
| startuproof.com / www.startuproof.com | **No public DNS record.** Both the session network and the web-fetch service return "ENOTFOUND". |
| startuproof.app / www.startuproof.app | **No public DNS record**, same result. |

Neither domain appears in the connected Vercel account, whose projects are `project-ph139` (rineinteract.com) and a v0 project. Neither appears in the connected GitHub repositories either.

**Consequences:**
- No website content, screenshots or terminology were used.
- All product screens are illustrative concepts.
- Both QR codes (deck and brochure) decode correctly to `https://startuproof.com`, but **that URL currently goes nowhere.** Point the domain at a live page before distributing anything with a QR code.

**Possible name conflict.** A web search found a separate organisation called "Startup Roof", described as a technology park in Lucknow (startuproof.in), and an @StartupRoof account on X. "FounderOS / StartupOS" is also the name of an unrelated US product (TechCrunch, 2022). **A trademark and name-availability check is recommended before public launch.**

Search sources: [Startup Roof on X](https://x.com/startuproof), [TechCrunch: StartupOS launch](https://techcrunch.com/2022/11/30/startupos-launch/), [CB Insights comparison](https://www.cbinsights.com/compare/foundertrac-vs-startupos).

## 2. Missing assets and inputs

| Item | Status | What was done instead | Action needed |
|---|---|---|---|
| **Photography** | Not available. Stock-photo sites (Unsplash, Pexels, Pixabay, Flickr, Wikimedia) are blocked by this environment's network policy. The connected Higgsfield account has 0 credits, so images could not be generated. | Photo slots are built into three full-width statement slides and two brochure banners. Editable vector illustrations stand in until photos arrive: a group of founders and a Dubai-style skyline. | Add licensed photos to `startup-roof/photos/` (see `photos/README.md`) and rebuild; they are placed automatically. Alternatively, allow the photo hosts in the environment's network settings, or top up Higgsfield credits, and ask for them to be added. |
| **Approved logo** | Not supplied | A typographic wordmark, "STARTUP **ROOF**". It is not presented as an official logo. | Supply the logo files (SVG or PNG, light and dark). |
| **Live website** | Not live (see section 1) | Text and QR code point to startuproof.com | Publish at least a landing page with a contact or interest form. |
| **Contact details** | Not supplied | The website and QR code are the only contact route. Ritesh Kumar is named only as Project Initiator. | Supply a project email or form URL. |
| **Pilot registration form** | Not confirmed | The materials say "express interest" and do not claim a live form. | Send the URL if a form exists. |
| **Fonts** | Inter | Embedded in all PDFs. | Install Inter (free, OFL) before editing the PPTX files. |

## 3. Facts to confirm before distribution

- The name "Startup Roof Radar".
- The milestones: 10,000 free users as the launch-event threshold, March 2027 as a tentative date, and 100,000 free users as the wider ambition. All are labelled as targets, not traction.
- The wording "Ritesh Kumar, Project Initiator".
- The proposed pilot formats, mentoring session length (30–60 minutes) and year-round rhythm. All are labelled as proposed.

## 4. Sources for external claims

**Important:** the research ran in an environment that could not open most source pages directly. Figures were checked against search-result excerpts of the named pages, and only high-confidence figures were used. **Before external distribution, someone should open each source and confirm the figure.**

| Figure used | Where | Source | Confidence |
|---|---|---|---|
| Ran out of cash or failed to raise 38%; no market need 35%; outcompeted 20% (111 post-mortems) | Deck "Why startups struggle"; brochure p.4 | CB Insights, "The Top 12 Reasons Startups Fail" (2021): https://www.cbinsights.com/research/report/startup-failure-reasons-top/ | 35% and 20% high. **38% medium: please verify.** |
| Survival 79.6% after 1 year, 49.6% after 5, 33.6% after 10 (March 1994 cohort) | Survival slide; brochure p.4 | US BLS research paper: https://www.bls.gov/osmr/research-papers/2004/pdf/st040060.pdf | High |
| 34.7% of establishments born in 2013 still operating in 2023 | Same | BLS TED 2024: https://www.bls.gov/opub/ted/2024/34-7-percent-of-business-establishments-born-in-2013-were-still-operating-in-2023.htm | High |
| About 50% of start-ups survive 5 years (OECD) | Same | Calvino, Criscuolo & Menon (2015), OECD STI Policy Paper: https://ideas.repec.org/p/oec/stiaaa/2015-6-en.html | High |
| 33% of mentored NYC founders were top performers, over 3× others | Evidence slide; brochure p.5 | Endeavor Insight via TechCrunch (2015): https://techcrunch.com/2015/03/22/mentors-are-the-secret-weapons-of-successful-startups | High (correlational) |
| 2× likelihood of becoming a top performer for connected companies | Same | Endeavor, "The Power of Entrepreneur Networks" | High |
| Accelerator companies raised 47–171% more funding | Same | Hallen, Cohen & Bingham (2020), Organization Science: https://papers.ssrn.com/abstract=2719810 | High (paper); exact range taken from the UNC summary |
| MENA startup funding: 2020 $0.654bn; 2021 $2.8bn; 2022 $3.94bn; 2023 ~$4.0bn (incl. $1.77bn debt); 2024 $2.3bn; 2025 $7.5bn (647 startups) | MENA funding chart; brochure p.6 | Wamda annual reviews: wamda.com 2021/01, 2021 review PDF, 2023/01, 2024/01, 2025/01, 2026/01 | High, except **2021 medium (reported as "$2.8 billion")** |
| UAE startups raised $1.1bn across 207 deals in 2024, ranked first | Same | Wamda 2024 review: https://wamda.com/2025/01/2024-review-mena-startup-investments | High |
| 1.2% of MENA funding went to female-founded startups (2024) | Same; brochure p.7 | Wamda 2024 review | High |
| UAE ranked #1 in the GEM National Entrepreneurship Context Index, fifth consecutive year | UAE context | WAM / Ministry of Economy (GEM 2025/26): https://www.moet.gov.ae/en/-/uae-ranks-first-globally-in-the-gem-2025-2026-global-report-for-the-fifth-consecutive-year | High |
| SMEs are 63.5% of non-oil GDP and 94.4% of companies | Same | Gulf Today citing the Central Bank; MoE SME page: https://www.moet.gov.ae/en/entrepreneurs-and-smes | High (year stated as "latest reported") |
| 557,000 SMEs at end-2022; target of 1 million by 2030 | Same | Gulf News quoting the Minister of Economy: https://gulfnews.com/business/557000-smes-operated-in-uae-at-end-of-2022-minister-of-economy-1.94976713 | High |
| D33: 30 companies to become global unicorns; 400 high-potential companies | Same | Dubai Media Office, D33 launch (Jan 2023): https://www.mediaoffice.ae/en/news/2023/January/04-01/Mohammed-bin-Rashid-launches-Dubai-Economic-Agenda-D33 | High |
| 20 unicorns by 2031 ("Entrepreneurial Nation") | Same | MoE: https://www.moet.gov.ae/en/-/moe-launches-phase-ii-of-the-entrepreneurial-nation | High |
| Dubai #19 among global emerging ecosystems | Same | Startup Genome GSER 2025: https://startupgenome.com/insights/menas-innovation-ecosystems-accelerate-in-gser-2025 | High |
| 1 in 5 UAE adults starting or running a new business (2025); about 9 in 10 see opportunities; over half deterred by fear of failure | UAE founders slide; brochure p.7 | GEM UAE country profile: https://www.gemconsortium.org/country-profile/130 | High (stated qualitatively, as GEM words it) |
| 31% of SMEs use generative AI (7 OECD countries, late 2024) | AI slide; brochure p.5 | OECD (2025), "Generative AI and the SME Workforce" | High |
| US firms using AI rose from 4.6% (early 2024) to 10% (Sept 2025) | Same | US Census Bureau BTOS: https://census.gov/library/stories/2026/05/ai-use-businesses.html | High |
| UAE Personal Data Protection Law, Federal Decree-Law No. 45 of 2021 | Trust slide; brochure p.17 | UAE federal legislation | High; check before launch |

**Deliberately left out:** the MAGNiTT series (methods differ from Wamda), UAE dollar totals for 2021–2023, exact GEM percentages for 2022–2024, and the SBA/UPS "70% of mentored businesses survive" claim (weak methodology).

## 5. Illustrative, proposed and planned content

Every item below carries a visible label in the materials, such as "Illustrative product concept — not a live screen", "Planned capability", "Proposed", "Illustrative scenario/personas", "Hypotheses" or "Targets, not traction".

- **Founder OS screens:** dashboard, onboarding, People (matching), Radar (opportunities), My plan (milestones). The Radar items are marked as samples and refer to no real programmes. No real people, users or metrics appear.
- **Other illustrative or proposed content:** personas, the healthy-snack scenario, sample curriculum, service catalogue, pilot design, year-round rhythm, mentoring model, revenue matrix, unit-economics framework, KPIs, architecture and MoSCoW build priorities.
- **Vector illustrations:** the founder-group and skyline illustrations are placeholders for photography and show no real people or places.

## 6. Pre-export review checklist

- [x] Startup Roof (ecosystem) and Founder OS (digital workspace) are named consistently and the relationship is explained.
- [x] The current stage is stated accurately. No invented traction, users, revenue, investors, partnerships, testimonials, awards or endorsements.
- [x] No fund or investment promises. No equity terms or prices. No founding-team titles.
- [x] No legacy event names, ticket packages, schedules or confidential event concepts.
- [x] All external figures are sourced on the slide and in the sources slide and page.
- [x] Automated text scan of all PDFs: no "TBD", placeholders, "guaranteed", "world's first" or "largest".
- [x] All four QR codes decode to `https://startuproof.com`. The domain is not live; see section 1.
- [x] Every page of all four PDFs was reviewed visually. The brochure pages were also checked automatically for content running into the footer.
- [x] Slide numbers are automatic fields, so they stay correct when slides are reordered in PowerPoint.
