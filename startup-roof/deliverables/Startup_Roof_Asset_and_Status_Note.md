# Startup Roof: asset and status note

Internal note for the project team. Do not share it with the presentation or the brochure.

Prepared 10 October 2026.

## Deliverables

| File | Format | Notes |
|---|---|---|
| `Startup_Roof_General_Presentation.pptx` | 20 slides, 16:9, editable | Diagrams, tables and charts are native PowerPoint shapes. Presenter notes are on every slide. |
| `Startup_Roof_General_Presentation.pdf` | 20 pages, 16:9 | Exported from the PPTX. Fonts are embedded. |
| `Startup_Roof_Project_Brochure.pdf` | 12 pages, A4 portrait | Written for portrait reading, not resized slides. It suits WhatsApp, email and print. |

The source files are in `../src/` (`build_deck.py`, `pptx_kit.py`, `brochure.html` and `build_brochure.py`). You can edit the text there and regenerate both files.

## 1. Missing assets and inputs

| Item | Status | What was done instead | Action needed |
|---|---|---|---|
| **Approved Startup Roof logo** | Not supplied | A typographic wordmark, “STARTUP **ROOF**”, set in Inter Bold. It is not presented as an official logo. | Supply the approved logo files (SVG or PNG, light and dark). Swap them in for the wordmark on the cover, the footers and the closing page. |
| **Website review (startuproof.com)** | **Could not be reached.** The domain did not resolve from the production environment on 10 Oct 2026. | No terminology, screenshots or claims were taken from the website. Every product screen is an illustrative concept. | Check that the site is live and that the content matches the materials. Send public-page screenshots if you want real screens used. |
| **Photography** | Not used. The stock-photo libraries were unreachable from the production environment. | Editable diagrams and a restrained graphic of a roof over four pillars. Dubai appears through the text (“UAE first”, the Dubai scenario), not through imagery. | Optional: add licensed photos of founders, working sessions or a Dubai business setting to the cover, slides 2, 10 and 19, and brochure pages 2, 6 and 11. Keep the licence records. |
| **Contact details** | Not supplied | The website and QR code are the only contact route. Ritesh Kumar appears by name and role only, with no personal details. | Supply a project email or contact form URL if one should be shown. |
| **Pilot registration form** | Not confirmed live | The materials say “express interest” and do not claim that a sign-up form exists. | Confirm whether a form exists and send its URL. A dedicated QR code can then point to it. |
| **Fonts** | Inter is used throughout | It is embedded in both PDFs. | PowerPoint users without Inter will see a substitute font. Install Inter (free, SIL Open Font License) or change the theme font before editing the PPTX. |

## 2. Facts to confirm before wider distribution

- **“Startup Roof Radar”** is used as the name of the planned insights feature. Confirm the name.
- **Milestones.** The materials state a launch-event threshold of 10,000 free users, a tentative target of March 2027 (subject to readiness) and a wider ambition of 100,000 free users. All three are labelled as targets, not traction. Confirm that they can be shared publicly.
- **“Ritesh Kumar, Project Initiator”** appears on slide 19 and brochure page 11. Confirm the wording.
- **The four-layer model** is labelled as proposed. It includes no prices, equity terms or fund size.

## 3. Sources for external claims

**No external statistics or market figures are used.** The deck and brochure make no claims about market size, funding volumes or ecosystem rankings. The six founder pain points (slide 2 and brochure page 2) are framed as working hypotheses to test in founder interviews, not as research findings. Nothing needs a citation.

One web search for “Startup Roof” (10 Oct 2026) found no third-party coverage of the project. Nothing from that search was used.

## 4. Illustrative and proposed content

| Location | Content | Label shown in the materials |
|---|---|---|
| Slide 7; brochure p.4 | Founder OS dashboard mock-up | “Illustrative product concept — not a live screen.” and “Planned capability” |
| Slide 8; brochure p.5 | Healthy-snack founder scenario | “Illustrative scenario” and “not a real customer case” |
| Slide 6; brochure p.9 | Four-layer model | “Proposed model” |
| Slide 9; brochure p.5 | AI with human support | “Proposed approach”, stating that no AI feature is presented as live |
| Slide 11; brochure p.6 | Founder Academy themes | “Proposed themes”, stating that no course catalogue exists yet |
| Slide 13; brochure p.7 | Startup Roof Radar | “Planned” |
| Slide 14; brochure p.8 | Example incubation plans | “Example support plans” |
| Slide 18; brochure p.10 | Milestones | “Targets and timing will be refined through the pilot. These are ambitions, not current traction.” |

The interface concepts contain no user counts, revenue, investor names or founder activity data.

## 5. Pre-export review checklist

- [x] The names **Startup Roof** (the ecosystem) and **Founder OS** (the digital workspace) are used consistently, and their relationship is explained on slide 3 and brochure page 3.
- [x] The current stage is described as shaping the platform and testing the experience through an initial collaboration and pilot phase.
- [x] No invented traction, users, revenue, investors, partnerships, testimonials, awards or endorsements.
- [x] No fund or investment promises. Slide 15 and brochure page 8 say what Startup Roof does not do.
- [x] No founding-team appointments, executive titles or equity allocations. Roles are described as to be considered later, based on contribution.
- [x] No legacy event names, ticket packages, schedules or confidential event concepts.
- [x] No supplier or partner logos.
- [x] No placeholders. An automated text scan of both PDFs found no “TBD”, “insert”, “guarantee”, “unicorn”, “world’s first” or “largest”.
- [x] Both QR codes (slide 20 and brochure page 12) were decoded from the exported PDFs and resolve to `https://startuproof.com`. The site itself could not be reached during production; see section 1.
- [x] Each brochure page was checked automatically for content overflowing into the footer. All slides were checked visually for clipping.
- [x] Minimum body text is about 11 pt on the slides. Footers and captions are 8.5–10 pt. Brochure body text is 11 pt and secondary text is 10 pt.
