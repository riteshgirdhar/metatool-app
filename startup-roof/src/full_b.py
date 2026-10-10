"""Full edition, part B: services, stakeholders, model, pilot, people, FAQ and glossary."""
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

from pptx_kit import *  # noqa: F401,F403
import build_deck as bd

B = lambda t, **o: (t, dict(bold=True, **o))  # noqa: E731


def P():
    return bd.prs


# ---------------------------------------------------------------- PHOTO-LED STATEMENT SLIDES
def _statement(key, eyebrow, title, body, fallback, notes_txt, **fb):
    s = blank(P(), NAVY)
    photo(s, key, 6.35, 0, W - 6.35, H, fallback=fallback, **fb)
    rect(s, 0, 0, 0.18, H, fill=BLUE)
    text(s, ML + 0.1, 1.5, 5.3, 0.3, eyebrow, size=10, color=MID, bold=True, spacing=1.5)
    text(s, ML + 0.1, 1.95, 5.3, 2.4, title, size=32, color=WHITE, bold=True, line=1.05)
    text(s, ML + 0.1, 4.3, 5.1, 2.0, body, size=14, color="C9D6E8", line=1.35)
    wordmark(s, ML + 0.1, 6.85, size=9.5, dark=True)
    notes(s, notes_txt)
    return s


def s_photo_community():
    _statement("community", "COMMUNITY", "Founders do better together.",
               "Peer groups, office hours and small gatherings turn a lonely journey into a shared one — with accountability built in.",
               people_scene, "A visual pause before the services chapter. The image represents founders working together; the message is that community is the foundation of the ecosystem.",
               bg="DCE8FB", n=5)


def s_photo_dubai():
    _statement("dubai", "UAE FIRST · GLOBAL AMBITION", "Rooted in the UAE. Built to travel.",
               "Startup Roof starts where policy, capital and founders are converging — and is designed to extend to other markets over time.",
               skyline, "A visual pause on place. The UAE is the starting point; the model is designed to be repeatable in other markets once it works here.",
               bg="1A3358", fg=("10213B", "1C3D6B", "24467A"), seed=21)


def s_photo_learning():
    _statement("learning", "FOUNDER ACADEMY", "Learn it on Monday. Use it on Tuesday.",
               "Short, practical sessions where every founder leaves with a task to apply to their own business.",
               people_scene, "A visual pause before the Academy detail. The message: learning is practical and immediately applied.",
               bg=PALE, n=4, seed=9)


# ---------------------------------------------------------------- YEAR-ROUND RHYTHM
def s_rhythm():
    s = blank(P())
    header(s, 0, "A year-round rhythm", "Support that does not stop when a programme ends.", tag="PROPOSED RHYTHM", title_size=27)
    cx, cy = 3.6, 4.45
    rings = [(2.25, PALE, "ALWAYS ON"), (1.6, "DCE8FB", "MONTHLY"), (1.0, "B8CFEE", "WEEKLY")]
    for r, f, lab in rings:
        rect(s, cx - r, cy - r, 2 * r, 2 * r, fill=f, shape=MSO_SHAPE.OVAL)
    for r, f, lab in rings:
        text(s, cx - 1.2, cy - r + 0.1, 2.4, 0.3, lab, size=9, color=BLUE, bold=True, align=PP_ALIGN.CENTER, spacing=1.2)
    c = rect(s, cx - 0.55, cy - 0.3, 1.1, 0.75, fill=NAVY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.4)
    shape_text(c, "Founder", size=12, color=WHITE, bold=True)
    rows = [("Weekly", "Office hours · peer-group check-ins · new resources and opportunities in Founder OS", BLUE),
            ("Monthly", "Thematic clinics · Academy sessions · mentor rounds · small founder gatherings", "1A55AC"),
            ("Quarterly", "Progress reviews · showcase sessions · partner workshops · cohort intakes", "17407F"),
            ("Always on", "Founder OS workspace · community discussions · service requests · Radar insights", NAVY)]
    for k, (a, b_, col) in enumerate(rows):
        y = 2.2 + k * 1.1
        rect(s, 6.6, y, 0.08, 0.92, fill=col)
        text(s, 6.9, y + 0.02, 5.8, 0.35, a, size=15, color=NAVY, bold=True)
        text(s, 6.9, y + 0.42, 5.8, 0.55, b_, size=11.5, color=TEXT, line=1.2)
    text(s, 6.6, 6.6, 6, 0.3, "Formats and frequency will be set by founder demand and delivery capacity.", size=10, color=MUTED)
    footer(s)
    notes(s, "“Year-round” is a key difference from time-bound programmes. This is a proposed rhythm, not a published schedule; the pilot will test which formats founders value enough to attend.")


# ---------------------------------------------------------------- MENTOR MODEL
def s_mentor_model():
    s = blank(P())
    header(s, 0, "How mentoring works", "Focused conversations with follow-through.", tag="PROPOSED MODEL", title_size=27)
    flow = [("Prepare", "Founder states the question and shares context in Founder OS."),
            ("Match", "A mentor with relevant experience accepts the request."),
            ("Meet", "30–60 minutes focused on one decision or problem."),
            ("Commit", "Founder records one or two concrete actions."),
            ("Follow up", "Check-in on progress; next session only if useful.")]
    fw = (W - 2 * ML) / 5
    for i, (a, b_) in enumerate(flow):
        x = ML + i * fw
        c = rect(s, x + fw / 2 - 0.35, 2.2, 0.7, 0.7, fill=(NAVY if i == 4 else BLUE), shape=MSO_SHAPE.OVAL)
        shape_text(c, str(i + 1), size=16, color=WHITE, bold=True)
        if i < 4:
            line(s, x + fw / 2 + 0.42, 2.55, x + fw * 1.5 - 0.42, 2.55, color="B8CFEE", w=1.5, arrow=True)
        text(s, x + 0.1, 3.05, fw - 0.2, 0.35, a, size=14, color=NAVY, bold=True, align=PP_ALIGN.CENTER)
        text(s, x + 0.15, 3.45, fw - 0.3, 0.9, b_, size=11, color=TEXT, align=PP_ALIGN.CENTER, line=1.2)
    cols = [("MENTORS COMMIT TO", ["Honest, practical feedback", "Declaring any conflicts of interest", "Respecting confidentiality", "Agreed availability, not open-ended time"]),
            ("FOUNDERS COMMIT TO", ["Preparing a clear question", "Respecting the mentor’s time", "Acting on what was agreed", "Sharing progress and feedback"])]
    for k, (t, its) in enumerate(cols):
        x = ML + k * 6.1
        rect(s, x, 4.6, 5.9, 2.15, fill=(PALE if k == 0 else NAVY))
        dk = k == 1
        text(s, x + 0.3, 4.78, 5.3, 0.3, t, size=9.5, color=(MID if dk else BLUE), bold=True, spacing=1.3)
        for j, it in enumerate(its):
            text(s, x + 0.3 + (j % 2) * 2.75, 5.18 + (j // 2) * 0.7, 2.65, 0.65, it, size=12, color=(WHITE if dk else NAVY), bold=True, line=1.15)
    footer(s)
    notes(s, "Mentoring works best when it is focused and followed up. Both sides make clear commitments. Session length and frequency are proposals to test.")


# ---------------------------------------------------------------- ACADEMY CURRICULUM
def s_curriculum():
    s = blank(P())
    header(s, 0, "Founder Academy · sample curriculum", "Eight themes, each ending in a practical output.", tag="PROPOSED THEMES", title_size=26)
    data = [["THEME", "EXAMPLE SESSION", "FOUNDER LEAVES WITH"],
            ["Idea validation", "Running customer interviews that reveal the truth", "An interview guide and a list of 10 people to call"],
            ["Business models", "How your business actually makes money", "A one-page business model"],
            ["AI and automation", "Practical AI tools for a small team", "Three tasks automated or AI-assisted"],
            ["GTM and customer acquisition", "Choosing your first channel", "A 30-day acquisition test plan"],
            ["Pricing and unit economics", "Pricing with confidence; knowing your margin", "A pricing sheet and unit-cost model"],
            ["Pitch readiness", "Telling the story investors and partners need", "A 10-slide outline and practice feedback"],
            ["Legal and operational foundations", "Setup routes, contracts and compliance basics", "A setup checklist and key contract list"],
            ["Consumer-brand and retail development", "From product to shelf or online store", "A channel plan and retailer pitch"]]
    table(s, ML, 2.1, W - 2 * ML, 4.55, data, [3.4, 4.35, 4.28], size=11, header_size=9.5, row_h=0.5)
    footer(s)
    notes(s, "A sample curriculum to show the format, not a published course catalogue. Each session produces something a founder can use immediately. Content will be co-created with contributors and refined with pilot founders.")


# ---------------------------------------------------------------- SERVICE CATALOGUE
def s_catalogue():
    s = blank(P())
    header(s, 0, "Expert services · what founders typically need", "Common requests by category.", tag="POTENTIAL CATEGORIES", title_size=27)
    cats = [("Legal", "Company setup documents, shareholder agreements, contracts, IP basics"),
            ("Accounting and finance", "Bookkeeping, VAT registration, financial models, cash-flow planning"),
            ("Branding and design", "Name and identity, packaging, pitch design, website look and feel"),
            ("Technology and automation", "No-code builds, website and app scoping, workflow automation"),
            ("Marketing and sales", "Positioning, social and paid campaigns, sales scripts and CRM"),
            ("Customer communication", "WhatsApp and email journeys, support processes, reviews"),
            ("Business setup", "Licence route, free zone or mainland choice, banking and visas"),
            ("Product and retail guidance", "Sourcing, manufacturing, listings, retail and marketplace entry")]
    cw = (W - 2 * ML - 0.3) / 2
    for i, (a, b_) in enumerate(cats):
        col, row = i % 2, i // 2
        x = ML + col * (cw + 0.3)
        y = 2.15 + row * 1.08
        rect(s, x, y, 0.08, 0.9, fill=[BLUE, NAVY][(i + row) % 2])
        text(s, x + 0.3, y + 0.04, cw - 0.4, 0.35, a, size=14, color=NAVY, bold=True)
        text(s, x + 0.3, y + 0.42, cw - 0.4, 0.5, b_, size=11.5, color=TEXT, line=1.15)
    text(s, ML, 6.55, W - 2 * ML, 0.3, "Examples of founder needs. Providers, packages and prices will be validated in the pilot; no supplier is confirmed.", size=10.5, color=MUTED)
    footer(s)
    notes(s, "This shows the breadth of practical help founders ask for, especially in the UAE where setup, licensing and banking are early hurdles. Packaging these needs clearly is the basis of the service model.")


# ---------------------------------------------------------------- INVESTOR READINESS
def s_readiness():
    s = blank(P())
    header(s, 0, "Investor readiness checklist", "What founders should have in place before raising.", title_size=27)
    groups = [("BUSINESS", ["A clear problem and target customer", "Evidence of demand or traction"]),
              ("MODEL", ["Unit economics you understand", "A credible plan for the funds"]),
              ("TEAM", ["The right founding team and gaps known", "Advisers or mentors where useful"]),
              ("FINANCE", ["Up-to-date accounts and runway", "A simple financial model"]),
              ("LEGAL", ["Clean company and share structure", "IP and key contracts in order"])]
    cw = (W - 2 * ML - 0.6) / 5
    for i, (g, its) in enumerate(groups):
        x = ML + i * (cw + 0.15)
        rect(s, x, 2.15, cw, 0.5, fill=[BLUE, "1A55AC", "17407F", "1A3358", NAVY][i])
        text(s, x, 2.25, cw, 0.3, g, size=11, color=WHITE, bold=True, align=PP_ALIGN.CENTER, spacing=1.4)
        for k, it in enumerate(its):
            y = 2.8 + k * 1.3
            rect(s, x, y, cw, 1.15, fill=PALE)
            rect(s, x + 0.2, y + 0.2, 0.22, 0.22, fill=WHITE, line=BLUE, lw=1.5)
            text(s, x + 0.55, y + 0.15, cw - 0.7, 0.95, it, size=11.5, color=NAVY, bold=True, line=1.15)
    rect(s, ML, 5.6, W - 2 * ML, 1.15, fill=NAVY)
    text(s, ML + 0.3, 5.72, W - 2 * ML - 0.6, 0.95,
         [[B("How Startup Roof helps: ", color=WHITE), ("readiness reviews, pitch feedback, data-room templates and — where relevant and with consent — introductions to investors who match the founder’s sector and stage.", {"color": "C9D6E8"})]],
         size=12.5, line=1.3, anchor=MSO_ANCHOR.MIDDLE)
    footer(s)
    notes(s, "A practical checklist founders can work through in Founder OS. Readiness support is useful even for founders who decide not to raise — it makes the business stronger either way.")


# ---------------------------------------------------------------- UNIVERSITIES
def s_universities():
    s = blank(P())
    header(s, 0, "Universities and incubators", "Continuity for student and alumni founders.", title_size=27)
    path = [("Idea in class", "Course project, club or competition"), ("Programme", "University incubator or challenge"),
            ("Startup Roof", "Year-round guidance, mentors and tools"), ("Alumni founder", "Growth support and community")]
    fw = (W - 2 * ML) / 4
    for i, (a, b_) in enumerate(path):
        x = ML + i * fw
        shp = MSO_SHAPE.PENTAGON if i == 0 else MSO_SHAPE.CHEVRON
        c = rect(s, x, 2.25, fw + 0.06, 0.7, fill=(BLUE if i == 2 else PALE if i < 2 else NAVY), shape=shp)
        shape_text(c, a, size=13, color=(NAVY if i < 2 else WHITE), bold=True)
        text(s, x + 0.25, 3.1, fw - 0.5, 0.6, b_, size=11.5, color=TEXT, line=1.2)
    cols = [("WHAT UNIVERSITIES COULD GAIN", ["Support for founders after programmes end", "Practitioner mentors and specialists", "Visibility for student ventures", "Practical content for entrepreneurship courses"]),
            ("POSSIBLE COLLABORATION FORMATS", ["Guest clinics and workshops", "Joint founder challenges", "Mentor office hours on campus", "Access to Founder OS for student founders"])]
    for k, (t, its) in enumerate(cols):
        x = ML + k * 6.1
        text(s, x, 4.05, 5.9, 0.3, t, size=9.5, color=BLUE, bold=True, spacing=1.3)
        for j, it in enumerate(its):
            yy = 4.42 + j * 0.56
            line(s, x, yy, x + 5.85, yy, color=LINE)
            text(s, x, yy + 0.12, 5.85, 0.4, it, size=12.5, color=NAVY, bold=(j == 0))
    footer(s)
    notes(s, "Universities produce many founders but support often ends when a programme or course ends. Startup Roof can provide continuity. These are formats to explore; no university partnership is signed.")


# ---------------------------------------------------------------- CORPORATES & PROVIDERS
def s_corporates():
    s = blank(P())
    header(s, 0, "Corporates and service providers", "Practical ways to work with early-stage founders.", title_size=27)
    data = [["PARTNER TYPE", "WHAT THEY CAN OFFER", "WHAT THEY CAN GAIN", "STARTING FORMAT"],
            ["Corporate innovation teams", "Challenges, pilots, expertise, mentors", "Early access to new solutions and talent", "A themed founder challenge"],
            ["Professional firms", "Legal, finance, tax and setup advice", "Relationships with future clients", "Monthly office hours"],
            ["Technology providers", "Tools, credits, technical guidance", "Adoption by relevant founders", "A limited tool pilot"],
            ["Banks and financial institutions", "SME banking, finance education", "Better-prepared SME customers", "A founder finance clinic"],
            ["Venues and co-working spaces", "Space for sessions and gatherings", "Community activity and visibility", "Hosting a founder evening"],
            ["Media and content partners", "Reach, interviews, editorial expertise", "Founder stories and insights", "A co-created guide or series"]]
    table(s, ML, 2.1, W - 2 * ML, 4.3, data, [2.9, 3.1, 3.2, 2.83], size=11, header_size=9.5, row_h=0.6)
    text(s, ML, 6.55, W - 2 * ML, 0.3, "Illustrative formats for discussion. No partnerships are signed or implied.", size=10.5, color=MUTED)
    footer(s)
    notes(s, "Each partner type has a concrete, low-commitment way to start. The aim is mutual value that can be measured, then expanded.")


# ---------------------------------------------------------------- REVENUE MATRIX
def s_revenue_matrix():
    s = blank(P())
    header(s, 0, "Revenue hypotheses by phase", "What we expect to explore, test and scale — and when.", tag="HYPOTHESES", title_size=27)
    phases = ["NOW · SHAPE", "NEXT · PILOT", "THEN · EXPAND"]
    rows = [("Paid memberships or tools", [1, 2, 3]), ("Specialist support packages", [1, 2, 3]), ("Structured programmes", [1, 2, 3]),
            ("Partner and service revenue arrangements", [1, 1, 2]), ("Corporate or university programmes", [1, 2, 2]),
            ("Sponsorship of suitable activities", [0, 1, 2]), ("Selective incubation arrangements", [0, 1, 2])]
    lab = {0: ("—", WHITE, MUTED), 1: ("Explore", PALE, NAVY), 2: ("Test", "8DB4EA", NAVY), 3: ("Scale", NAVY, WHITE)}
    x0, y0, lw_, cw, rh = ML, 2.15, 4.4, 2.45, 0.5
    for j, p in enumerate(phases):
        text(s, x0 + lw_ + j * (cw + 0.08), y0, cw, 0.3, p, size=9.5, color=BLUE, bold=True, align=PP_ALIGN.CENTER, spacing=1.1)
    for i, (r, v) in enumerate(rows):
        y = y0 + 0.4 + i * (rh + 0.06)
        text(s, x0, y, lw_ - 0.1, rh, r, size=12, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        for j, val in enumerate(v):
            t, f, c = lab[val]
            b_ = rect(s, x0 + lw_ + j * (cw + 0.08), y, cw, rh, fill=f, line=(LINE if val == 0 else None))
            shape_text(b_, t, size=11, color=c, bold=True)
    text(s, ML, 6.6, W - 2 * ML, 0.3, "Sequencing is a working hypothesis and will change with pilot evidence. “Scale” means only after unit economics are proven.", size=10.5, color=MUTED)
    footer(s)
    notes(s, "Not every revenue idea should be tested at once. This matrix sets a sensible order: start with what founders most clearly value, test pricing in the pilot, and only scale what has proven unit economics.")


# ---------------------------------------------------------------- UNIT ECONOMICS FRAMEWORK
def s_unit_econ():
    s = blank(P())
    header(s, 0, "How each service must pay its way", "A simple test for every paid offer.", title_size=27)
    blocks = [("Price paid", "by founder or partner", PALE, NAVY), ("−", "", None, None), ("Delivery cost", "expert time, materials, venue", "DCE8FB", NAVY),
              ("−", "", None, None), ("Platform cost", "share of tools, support, admin", "B8CFEE", NAVY), ("=", "", None, None),
              ("Contribution", "what is left to sustain the ecosystem", NAVY, WHITE)]
    x = ML
    for a, b_, f, c in blocks:
        if f is None:
            text(s, x, 2.55, 0.5, 0.8, a, size=34, color=BLUE, bold=True, align=PP_ALIGN.CENTER)
            x += 0.5
            continue
        w = 2.4
        rect(s, x, 2.3, w, 1.35, fill=f)
        text(s, x + 0.2, 2.45, w - 0.4, 0.4, a, size=15, color=c, bold=True)
        text(s, x + 0.2, 2.9, w - 0.4, 0.7, b_, size=11, color=(c if c == NAVY else "C9D6E8"), line=1.15)
        x += w + 0.06
    text(s, ML, 4.05, 6, 0.3, "QUESTIONS THE PILOT MUST ANSWER", size=9.5, color=BLUE, bold=True, spacing=1.3)
    qs = ["What will founders pay for, and how much?", "How much expert time does each outcome really take?", "Which services can be delivered in groups to lower cost?",
          "Where do partners fund value for founders?", "What does free access cost per active founder?", "Which offers lead to repeat use?"]
    for i, q in enumerate(qs):
        col, row = i % 2, i // 2
        xx = ML + col * 6.1
        yy = 4.45 + row * 0.7
        rect(s, xx, yy + 0.1, 0.1, 0.1, fill=BLUE)
        text(s, xx + 0.28, yy, 5.7, 0.6, q, size=12.5, color=TEXT)
    footer(s)
    notes(s, "This is a framework, deliberately without numbers. Every paid service must cover its delivery and platform cost and contribute to the free layer. The pilot will put real numbers into this formula.")


# ---------------------------------------------------------------- PILOT DESIGN
def s_pilot():
    s = blank(P())
    header(s, 0, "Pilot design", "A small, measured test of the founder experience.", tag="PROPOSED", title_size=27)
    comps = [("Who", "A small group of founders across stages and sectors, including non-tech businesses."),
             ("What", "Onboarding, a validation or growth track, clinics, mentor sessions and follow-up."),
             ("How", "Simple tools first; Founder OS features introduced as they are ready."),
             ("Contributors", "Participants deliver sessions and support in roles that suit their time and skills."),
             ("Learning", "Founder interviews, feedback after every session, delivery cost tracked throughout.")]
    for i, (a, b_) in enumerate(comps):
        y = 2.15 + i * 0.86
        rect(s, ML, y, 1.9, 0.74, fill=(NAVY if i == 0 else BLUE if i < 3 else "1A55AC"))
        text(s, ML, y, 1.9, 0.74, a, size=13, color=WHITE, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        rect(s, ML + 1.95, y, 5.6, 0.74, fill=PALE)
        text(s, ML + 2.15, y, 5.3, 0.74, b_, size=11.5, color=TEXT, anchor=MSO_ANCHOR.MIDDLE, line=1.15)
    rx = 8.65
    rect(s, rx, 2.15, W - ML - rx, 4.18, fill=NAVY)
    text(s, rx + 0.3, 2.38, 3.5, 0.3, "THE PILOT SUCCEEDS IF", size=9.5, color=MID, bold=True, spacing=1.3)
    sc = ["Founders complete useful next steps", "They come back without being chased", "Sessions are rated as practical", "Contributors can deliver reliably", "We know the real cost to serve"]
    for k, it in enumerate(sc):
        yy = 2.8 + k * 0.68
        rect(s, rx + 0.3, yy + 0.08, 0.2, 0.2, fill=BLUE, shape=MSO_SHAPE.OVAL)
        text(s, rx + 0.65, yy, 3.2, 0.6, it, size=12.5, color=WHITE, bold=True, line=1.15)
    footer(s)
    notes(s, "The pilot is intentionally small. Its job is learning: what founders value, what contributors can deliver and what it costs. Cohort size and duration will be set once delivery capacity is confirmed.")


# ---------------------------------------------------------------- KPIs
def s_kpis():
    s = blank(P())
    header(s, 0, "How we will measure progress", "One north-star measure, supported by a few honest indicators.", title_size=26)
    ns = rect(s, ML, 2.15, 4.2, 4.6, fill=NAVY)
    text(s, ML + 0.35, 2.4, 3.5, 0.3, "NORTH-STAR MEASURE", size=9.5, color=MID, bold=True, spacing=1.3)
    text(s, ML + 0.35, 2.85, 3.5, 1.6, "Completed founder next steps", size=24, color=WHITE, bold=True, line=1.1)
    text(s, ML + 0.35, 4.55, 3.5, 2.0, "A next step counts when the founder confirms it is done — a test run, a decision made, a customer won. It measures usefulness, not activity.", size=12, color="C9D6E8", line=1.3)
    kp = [("Activation", "New founders who complete a profile and a first step"), ("Follow-through", "Agreed actions completed after sessions"),
          ("Return rate", "Founders active again within 30 days"), ("Useful introductions", "Introductions leading to a real conversation"),
          ("Session quality", "Founder rating of practical value"), ("Cost to serve", "Delivery cost per active founder"),
          ("Paid conversion", "Founders choosing an optional paid service"), ("Contributor reliability", "Sessions delivered as committed")]
    gx = 5.15
    cw = (W - ML - gx - 0.2) / 2
    for i, (a, b_) in enumerate(kp):
        col, row = i % 2, i // 2
        x = gx + col * (cw + 0.2)
        y = 2.15 + row * 1.15
        line(s, x, y, x + cw, y, color=NAVY if row == 0 else LINE)
        text(s, x, y + 0.12, cw, 0.35, a, size=13.5, color=BLUE, bold=True)
        text(s, x, y + 0.48, cw, 0.6, b_, size=11.5, color=TEXT, line=1.15)
    footer(s)
    notes(s, "Growth in sign-ups is easy to chase and easy to misread. The north-star measure keeps the focus on founder outcomes. Supporting indicators cover quality, retention, delivery and economics.")


# ---------------------------------------------------------------- GROWTH PATH
def s_growth_path():
    s = blank(P())
    header(s, 0, "The path to our milestones", "Each step must be earned by the one before it.", tag="TARGETS, NOT TRACTION", title_size=27)
    steps = [("Shape", "Today", "Concept, contributors and founder interviews", PALE, NAVY),
             ("Pilot", "Next", "Small cohort; prove usefulness and cost to serve", "DCE8FB", NAVY),
             ("10,000", "Launch threshold", "Free users — the threshold for a public launch event", BLUE, WHITE),
             ("March 2027", "Tentative target", "Target timing for launch, subject to readiness", "1A55AC", WHITE),
             ("100,000", "Wider ambition", "Free users across the UAE and beyond", NAVY, WHITE)]
    n = len(steps)
    sw = (W - 2 * ML - 0.2) / n
    for i, (a, b_, d, f, c) in enumerate(steps):
        x = ML + i * (sw + 0.05)
        hgt = 1.55 + i * 0.55
        top = 6.3 - hgt
        rect(s, x, top, sw, hgt, fill=f)
        text(s, x + 0.18, top + 0.15, sw - 0.36, 0.5, a, size=(20 if i >= 2 else 17), color=c, bold=True)
        text(s, x + 0.18, top + 0.62, sw - 0.36, 0.3, b_.upper(), size=8.5, color=(BLUE if c == NAVY else "DCE6F5"), bold=True, spacing=1.0)
        text(s, x + 0.18, max(top + 0.92, 2.0), sw - 0.36, 1.2, d, size=10.5, color=(TEXT if c == NAVY else "E3ECF8"), line=1.18)
    text(s, ML, 6.45, W - 2 * ML, 0.35, "All figures are targets to be refined through the pilot. None represents current users or traction.", size=10.5, color=MUTED)
    footer(s)
    notes(s, "This turns the milestones into a sequence. We do not move to the next step until the previous one is proven. The numbers are ambitions — not current traction.")


# ---------------------------------------------------------------- RISKS
def s_risks():
    s = blank(P())
    header(s, 0, "Risks and how we address them", "Being honest about what could go wrong.", title_size=27)
    data = [["RISK", "WHY IT MATTERS", "HOW WE ADDRESS IT"],
            ["Low founder engagement", "Without use, there is no ecosystem", "Small pilot, practical formats, measure return rate"],
            ["Inconsistent delivery", "Volunteer time can be unreliable", "Clear commitments; roles based on reliable delivery"],
            ["Quality of advice", "Poor advice harms founders and trust", "Vetted contributors, founder ratings, human escalation"],
            ["Cost to serve too high", "Free access must be sustainable", "Group formats, unit-economics test for every service"],
            ["Platform built too early", "Wasted effort on unused features", "Simple tools first; build what the pilot proves"],
            ["Data and privacy", "Founder trust is essential", "Consent-first design; UAE data-protection law review"],
            ["Over-promising", "Credibility with founders and partners", "Clear stage labels; no claims beyond evidence"]]
    table(s, ML, 2.1, W - 2 * ML, 4.6, data, [3.2, 3.85, 4.98], size=11, header_size=9.5, row_h=0.56)
    footer(s)
    notes(s, "Naming the risks openly builds credibility with investors, partners and contributors. Most mitigations come down to starting small, measuring honestly and building only what is proven.")


# ---------------------------------------------------------------- CONTRIBUTION MODEL
def s_contribution():
    s = blank(P())
    header(s, 0, "Ways to contribute", "Many roles, matched to experience and available time.", title_size=27)
    roles = [("Session lead", "Run a clinic, workshop or Academy session"), ("Mentor", "Give focused time to founders in your field"),
             ("Workstream contributor", "Help build part of the project — platform, content, partnerships"), ("Specialist", "Offer defined professional services"),
             ("Connector", "Introduce relevant organisations and people"), ("Content contributor", "Write guides, record interviews, share lessons")]
    cw = (W - 2 * ML - 0.4) / 3
    for i, (a, b_) in enumerate(roles):
        col, row = i % 3, i // 3
        x = ML + col * (cw + 0.2)
        y = 2.15 + row * 1.35
        rect(s, x, y, cw, 1.2, fill=PALE)
        text(s, x + 0.25, y + 0.18, cw - 0.5, 0.35, a, size=14, color=NAVY, bold=True)
        text(s, x + 0.25, y + 0.56, cw - 0.5, 0.6, b_, size=11.5, color=TEXT, line=1.15)
    rect(s, ML, 5.0, W - 2 * ML, 1.75, fill=NAVY)
    text(s, ML + 0.3, 5.18, 5, 0.3, "HOW LONGER-TERM ROLES WILL BE CONSIDERED", size=9.5, color=MID, bold=True, spacing=1.3)
    crit = ["Actual contribution", "Time commitment", "Responsibility taken", "Reliable delivery", "Value created"]
    cw2 = (W - 2 * ML - 0.6) / 5
    for k, c in enumerate(crit):
        x = ML + 0.3 + k * cw2
        text(s, x, 5.6, cw2 - 0.1, 0.4, f"{k + 1:02d}", size=13, color=MID, bold=True)
        text(s, x, 5.95, cw2 - 0.15, 0.6, c, size=13, color=WHITE, bold=True, line=1.1)
    footer(s)
    notes(s, "Contribution is open and flexible. Permanent roles, titles and any longer-term arrangements have not been set and will be considered later on these five criteria.")


# ---------------------------------------------------------------- FAQ
def s_faq():
    s = blank(P())
    header(s, 0, "Frequently asked questions", "Short answers to common questions.", title_size=27)
    qa = [("Is Startup Roof an accelerator or a fund?", "Neither today. It is a founder ecosystem with a planned digital workspace. Any investment activity would need its own structure."),
          ("Is Founder OS live?", "Not yet. It is planned and will be introduced step by step, starting in the pilot."),
          ("Do I need a tech startup to join?", "No. Consumer, wellness, retail and service businesses are equally welcome."),
          ("Will it cost money?", "Founder access starts free. Optional paid tools and services will be tested in the pilot."),
          ("Do I have to raise investment?", "No. Many businesses grow from revenue; capital is one option among several."),
          ("Is it only for the UAE?", "It starts in the UAE, with an ambition to extend to other markets."),
          ("How is my data used?", "Consent first: founders control what is shared, and introductions need agreement from both sides."),
          ("How can I get involved?", "Visit startuproof.com to express interest as a founder, mentor, partner, investor or contributor.")]
    cw = (W - 2 * ML - 0.4) / 2
    for i, (q, a) in enumerate(qa):
        col, row = i % 2, i // 2
        x = ML + col * (cw + 0.4)
        y = 2.1 + row * 1.15
        line(s, x, y, x + cw, y, color=NAVY if row == 0 else LINE)
        text(s, x, y + 0.1, cw, 0.35, q, size=13, color=NAVY, bold=True)
        text(s, x, y + 0.45, cw, 0.65, a, size=11.5, color=TEXT, line=1.18)
    footer(s)
    notes(s, "Useful for Q&A and for readers without a presenter. Answers stay consistent with the current stage.")


# ---------------------------------------------------------------- GLOSSARY
def s_glossary():
    s = blank(P())
    header(s, 0, "Glossary", "Startup terms used in this presentation.", title_size=27)
    g = [("Accelerator", "A time-bound programme supporting startups, often with investment."),
         ("Angel investor", "An individual who invests personal money in early startups."),
         ("Bootstrapping", "Funding a business from savings and revenue."),
         ("CAC", "Cost of acquiring one new customer."),
         ("Churn", "The rate at which customers stop buying."),
         ("Dilution", "Owning a smaller share after new shares are issued."),
         ("Free zone", "A UAE economic zone with its own licensing rules."),
         ("GTM", "Go-to-market: how a product reaches customers."),
         ("Incubator", "Support for very early ventures, often with space and mentoring."),
         ("LTV", "Gross profit expected from a customer over time."),
         ("MVP", "Minimum viable product — the simplest sellable version."),
         ("Pre-seed / Seed", "Early funding rounds to build and find product–market fit."),
         ("Product–market fit", "Strong, repeat demand from a clear market."),
         ("Runway", "Months a business can operate on current cash."),
         ("Unit economics", "Revenue and cost per unit, customer or order."),
         ("Venture capital", "Professional investment funds for high-growth companies.")]
    cw = (W - 2 * ML - 0.4) / 2
    for i, (t, d) in enumerate(g):
        col, row = i // 8, i % 8
        x = ML + col * (cw + 0.4)
        y = 2.05 + row * 0.58
        text(s, x, y, 1.95, 0.5, t, size=12, color=BLUE, bold=True)
        text(s, x + 2.0, y, cw - 2.0, 0.55, d, size=11.5, color=TEXT, line=1.12)
        line(s, x, y + 0.52, x + cw, y + 0.52, color="E6EEF9")
    footer(s)
    notes(s, "Plain-English definitions so that the deck works for first-time founders and non-specialist partners.")
