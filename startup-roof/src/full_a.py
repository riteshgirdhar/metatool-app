"""Full edition, part A: overview, concept, founder journey and Founder OS deep dives."""
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

from pptx_kit import *  # noqa: F401,F403
import build_deck as bd

B = lambda t, **o: (t, dict(bold=True, **o))  # noqa: E731


def P():
    return bd.prs


# ---------------------------------------------------------------- AT A GLANCE
def s_glance():
    s = blank(P())
    header(s, 0, "Startup Roof at a glance", "A practical ecosystem around the founder — on one page.")
    rect(s, ML, 2.15, 4.3, 4.65, fill=NAVY)
    text(s, ML + 0.35, 2.4, 3.7, 0.3, "IN ONE SENTENCE", size=9.5, color=MID, bold=True, spacing=1.3)
    text(s, ML + 0.35, 2.8, 3.65, 2.6,
         "Startup Roof brings practical guidance, useful tools and meaningful connections together to help founders take their next step.",
         size=17, color=WHITE, bold=True, line=1.25)
    text(s, ML + 0.35, 5.35, 3.7, 1.2,
         [[B("Startup Roof", color=WHITE), (" is the ecosystem.", {"color": "C9D6E8"})],
          [B("Founder OS", color=MID), (" is the digital workspace inside it.", {"color": "C9D6E8"})]],
         size=12.5, line=1.35)
    tiles = [("WHAT", "A year-round founder ecosystem", "Community, programmes, services and a guided digital workspace."),
             ("FOR WHOM", "Founders first", "Aspiring, early-stage and growing founders — tech and non-tech."),
             ("HOW", "Build · Learn · Connect · Grow", "Next steps, practical learning, relevant people and opportunities."),
             ("WHERE", "UAE first, global ambition", "Starting in the UAE and widening coverage over time."),
             ("STAGE", "Shaping and pilot phase", "Testing the founder experience with an initial group of contributors."),
             ("NEXT", "A small, measured pilot", "Useful sessions, onboarding and follow-up — then expand what works.")]
    gx, gy = 5.3, 2.15
    tw, th = 2.4, 2.22
    for i, (k, t, d) in enumerate(tiles):
        col, row = i % 3, i // 3
        x = gx + col * (tw + 0.14)
        y = gy + row * (th + 0.2)
        rect(s, x, y, tw, th, fill=PALE if (i % 2 == 0) else WHITE, line=None if i % 2 == 0 else LINE)
        text(s, x + 0.22, y + 0.22, tw - 0.4, 0.3, k, size=9, color=BLUE, bold=True, spacing=1.3)
        text(s, x + 0.22, y + 0.55, tw - 0.4, 0.8, t, size=14, color=NAVY, bold=True, line=1.1)
        text(s, x + 0.22, y + 1.3, tw - 0.4, 0.9, d, size=11, color=TEXT, line=1.2)
    footer(s)
    notes(s, "Use this as the one-page summary for anyone who only reads one slide. It answers what, for whom, how, where, the current stage and what happens next.")


# ---------------------------------------------------------------- CONTENTS
CHAPTERS = [
    ("Why founders need a roof", "The founder experience, why startups struggle and the UAE context"),
    ("The Startup Roof concept", "Ecosystem, pillars, audiences, sectors and the proposed model"),
    ("The founder journey", "Six stages, practical checklists, key metrics and funding options"),
    ("Founder OS", "The planned digital workspace, illustrative screens and principles"),
    ("Ecosystem services", "Community, mentoring, Academy, expert services, insights and incubation"),
    ("Value for the ecosystem", "Investors, universities, corporates and service partners"),
    ("Model, pilot and roadmap", "Commercial hypotheses, pilot design, measurement, milestones and risks"),
    ("People and participation", "Capabilities, contribution, FAQ, glossary and invitation"),
]


def s_contents():
    s = blank(P())
    header(s, 0, "Contents", "What this presentation covers.")
    for i, (t, d) in enumerate(CHAPTERS):
        col, row = i // 4, i % 4
        x = ML + col * 6.1
        y = 2.15 + row * 1.15
        line(s, x, y, x + 5.75, y, color=NAVY if row == 0 else LINE, w=1.0)
        text(s, x, y + 0.15, 0.9, 0.6, f"{i + 1:02d}", size=26, color=BLUE, bold=True)
        text(s, x + 1.0, y + 0.17, 4.75, 0.4, t, size=16, color=NAVY, bold=True)
        text(s, x + 1.0, y + 0.55, 4.75, 0.5, d, size=11, color=MUTED, line=1.15)
    footer(s)
    notes(s, "Eight chapters. In a short meeting, use chapters 2, 4 and 8. The full deck is designed to be read without a presenter.")


# ---------------------------------------------------------------- THE OPPORTUNITY / GAP
def s_gap():
    s = blank(P())
    header(s, 0, "What this means", "Support exists. Joining it up around the founder is the opportunity.", title_size=27)
    cols = [("WHAT IS GROWING", BLUE, ["Startup programmes and incubators", "Venture capital and angel activity", "Government focus on SMEs and entrepreneurship", "Online content, tools and AI assistants"]),
            ("WHAT FOUNDERS STILL REPORT", NAVY, ["Support is scattered and hard to compare", "Little continuity between programmes", "Advice is generic, not sector-relevant", "Few introductions lead to real outcomes"])]
    for i, (t, c, its) in enumerate(cols):
        x = ML + i * 4.3
        rect(s, x, 2.2, 3.95, 0.08, fill=c)
        text(s, x, 2.42, 3.95, 0.3, t, size=10, color=c, bold=True, spacing=1.3)
        for k, it in enumerate(its):
            yy = 2.85 + k * 0.72
            line(s, x, yy, x + 3.95, yy, color=LINE)
            text(s, x, yy + 0.14, 3.95, 0.5, it, size=13, color=TEXT, line=1.15)
    p = rect(s, 9.15, 2.2, 3.53, 4.2, fill=PALE)
    text(s, 9.45, 2.42, 3.0, 0.3, "STARTUP ROOF’S ROLE", size=10, color=BLUE, bold=True, spacing=1.3)
    text(s, 9.45, 2.85, 2.95, 3.4,
         [[B("Join it up.", color=NAVY, size=18)],
          {"runs": [("Connect founders to the right guidance, people and opportunities at the right stage — and follow up so it leads somewhere.", {"color": TEXT, "size": 12.5})], "before": 8}],
         size=18, line=1.28)
    line(s, 8.55, 4.3, 9.05, 4.3, color=BLUE, w=2, arrow=True)
    text(s, ML, 6.45, 8.3, 0.4, "Based on the project team’s experience; to be tested through founder interviews in the pilot.", size=10.5, color=MUTED)
    footer(s)
    notes(s, "The point is not that support is missing — the UAE has strong momentum. The opportunity is continuity and relevance: joining existing support up around each founder and following through.")


# ---------------------------------------------------------------- FOUR PILLARS
def s_pillars():
    s = blank(P())
    header(s, 0, "Build · Learn · Connect · Grow", "Four things founders need, under one roof.")
    bx, bw = ML, W - 2 * ML
    polyline(s, [(bx + 0.4, 2.85), (bx + bw / 2, 2.05), (bx + bw - 0.4, 2.85)], color=NAVY, w=3)
    pillars = [("BUILD", "Turn an idea into a working business.", "Next-step plans, templates, product and setup guidance.", "Tasks and templates", "1A3358"),
               ("LEARN", "Gain practical skills, quickly.", "Founder Academy sessions that end in an action.", "Learning progress", "1C3D6B"),
               ("CONNECT", "Reach the right people.", "Consent-based introductions, mentors, peers and specialists.", "Discovery and requests", "1F4A85"),
               ("GROW", "Find customers, capability and capital.", "Go-to-market support, expert services, readiness and opportunities.", "Opportunities and progress", BLUE)]
    cw = (bw - 0.6) / 4
    for i, (t, a, b_, osf, col) in enumerate(pillars):
        x = bx + 0.15 + i * (cw + 0.1)
        rect(s, x, 3.0, cw, 0.55, fill=col)
        text(s, x, 3.1, cw, 0.35, t, size=14, color=WHITE, bold=True, align=PP_ALIGN.CENTER, spacing=1.5)
        rect(s, x, 3.55, cw, 3.2, fill=PALE)
        text(s, x + 0.2, 3.72, cw - 0.4, 0.75, a, size=13.5, color=NAVY, bold=True, line=1.15)
        text(s, x + 0.2, 4.5, cw - 0.4, 0.3, "HOW STARTUP ROOF HELPS", size=8.5, color=BLUE, bold=True, spacing=1.0)
        text(s, x + 0.2, 4.78, cw - 0.4, 1.0, b_, size=11.5, color=TEXT, line=1.2)
        line(s, x + 0.2, 5.85, x + cw - 0.2, 5.85, color="C4D8F6")
        text(s, x + 0.2, 5.95, cw - 0.4, 0.3, "IN FOUNDER OS", size=8.5, color=BLUE, bold=True, spacing=1.0)
        text(s, x + 0.2, 6.22, cw - 0.4, 0.4, osf, size=11.5, color=NAVY, bold=True)
    footer(s)
    notes(s, "The four pillars organise everything Startup Roof offers. Each pillar has an ecosystem service (people, sessions, partners) and a matching Founder OS capability (the digital workspace).")


# ---------------------------------------------------------------- SECTORS
def s_sectors():
    s = blank(P())
    header(s, 0, "Sectors we serve", "Not only tech. Any commercially viable business with a founder.", title_size=27)
    secs = [("Technology", "Software, platforms, AI-enabled products", ["Product–market fit", "Technical choices and cost", "Recurring revenue", "Investor readiness"]),
            ("Consumer products", "Food, beauty, home and lifestyle brands", ["Unit economics and margin", "Manufacturing and sourcing", "Retail and e-commerce channels", "Brand building"]),
            ("Wellness", "Fitness, nutrition, mental wellbeing, care", ["Trust and credibility", "Licensing and compliance", "Repeat customers", "Community building"]),
            ("Retail", "Physical and online stores, marketplaces", ["Inventory and cash flow", "Location and channel mix", "Customer acquisition cost", "Operations at scale"]),
            ("Services", "Agencies, consultancies, B2B and local services", ["Pricing and packaging", "Productising expertise", "Pipeline and referrals", "Hiring and delivery"])]
    cw = (W - 2 * ML - 0.4) / 5
    for i, (t, d, ch) in enumerate(secs):
        x = ML + i * (cw + 0.1)
        rect(s, x, 2.2, cw, 0.07, fill=[NAVY, BLUE, "1A55AC", "17407F", MID][i])
        text(s, x, 2.42, cw - 0.1, 0.4, t, size=15, color=NAVY, bold=True)
        text(s, x, 2.85, cw - 0.15, 0.7, d, size=11, color=MUTED, line=1.15)
        text(s, x, 3.7, cw, 0.3, "TYPICAL CHALLENGES", size=8.5, color=BLUE, bold=True, spacing=1.0)
        for k, c in enumerate(ch):
            yy = 4.05 + k * 0.55
            rect(s, x, yy, cw - 0.05, 0.46, fill=PALE)
            text(s, x + 0.12, yy, cw - 0.25, 0.46, c, size=10.5, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, line=1.0)
    rect(s, ML, 6.35, W - 2 * ML, 0.48, fill=NAVY)
    text(s, ML + 0.25, 6.43, W - 2 * ML - 0.5, 0.35,
         "Venture funding is one route, not the goal. Many strong businesses grow from revenue — and Startup Roof is designed for them too.",
         size=11.5, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
    footer(s)
    notes(s, "Sector relevance is central. A consumer brand founder needs margin, sourcing and retail advice, not a SaaS playbook. The support and specialists will be matched by sector.")


# ---------------------------------------------------------------- PERSONAS
def s_personas():
    s = blank(P())
    header(s, 0, "Founders we design for", "Four example founders, four different next steps.", tag="ILLUSTRATIVE PERSONAS")
    ps = [("The aspiring founder", "Explore", "Has an idea and a full-time job; unsure where to start.", "Clarity on whether the idea is worth testing.", "Validation guide, peer group, first clinic."),
          ("The first-time brand owner", "Validate → Build", "Launching a consumer product with savings.", "Evidence that customers will buy at a viable margin.", "Pricing session, sourcing specialist, retail mentor."),
          ("The tech founder", "Launch", "Has a product and early users; needs traction.", "A repeatable way to acquire paying customers.", "GTM sprint, customer-acquisition mentor, tool credits."),
          ("The growing service business", "Grow", "Profitable agency, stuck at founder capacity.", "Systems, hiring and productised offers.", "Operations specialist, automation, peer group.")]
    cw = (W - 2 * ML - 0.45) / 4
    for i, (t, st, sit, need, help_) in enumerate(ps):
        x = ML + i * (cw + 0.15)
        rect(s, x, 2.15, cw, 4.65, fill=PALE)
        person(s, x + 0.55, 2.4, 0.6, fill=[NAVY, BLUE, "1F4A85", "17407F"][i])
        text(s, x + 1.05, 2.42, cw - 1.15, 0.6, t, size=13, color=NAVY, bold=True, line=1.1)
        pill(s, x + 1.05, 3.0, st.upper(), fill=WHITE, size=8)
        rows = [("SITUATION", sit), ("WHAT THEY NEED", need), ("HOW STARTUP ROOF HELPS", help_)]
        for k, (lab, v) in enumerate(rows):
            yy = 3.55 + k * 1.05
            line(s, x + 0.2, yy, x + cw - 0.2, yy, color="C4D8F6")
            text(s, x + 0.2, yy + 0.1, cw - 0.4, 0.25, lab, size=8.5, color=BLUE, bold=True, spacing=1.0)
            text(s, x + 0.2, yy + 0.36, cw - 0.4, 0.7, v, size=11, color=TEXT, line=1.18)
    footer(s)
    notes(s, "These personas are illustrative composites used for design, not real people. They show how the same ecosystem produces different next steps depending on stage and sector.")


# ---------------------------------------------------------------- VALUE EXCHANGE
def s_value_exchange():
    s = blank(P())
    header(s, 0, "How value flows", "Everyone gives something useful and gets something useful.", title_size=27)
    cx, cy = W / 2, 4.45
    core = rect(s, cx - 0.95, cy - 0.95, 1.9, 1.9, fill=NAVY, shape=MSO_SHAPE.OVAL)
    shape_text(core, [[B("Founder")], [("at the centre", {"size": 10, "color": "C9D6E8"})]], size=15, color=WHITE)
    nodes = [("Mentors and specialists", "Give: experience and judgement", "Get: purposeful impact, visibility, fit", -4.55, -1.6),
             ("Investors and angels", "Give: readiness feedback, sessions", "Get: better-prepared founders", 1.95, -1.6),
             ("Universities and incubators", "Give: talent, programmes, research", "Get: continuity for student founders", -4.55, 0.05),
             ("Corporates", "Give: challenges, pilots, expertise", "Get: early innovation and partners", 1.95, 0.05),
             ("Service and tool providers", "Give: services, tools, offers", "Get: relevant founder customers", -4.55, 1.7),
             ("Founder community", "Give: peer advice and accountability", "Get: support, network, momentum", 1.95, 1.7)]
    for t, g, gt, dx, dy in nodes:
        x, y = cx + dx, cy + dy - 0.55
        rect(s, x, y, 2.6, 1.1, fill=PALE)
        text(s, x + 0.18, y + 0.1, 2.3, 0.3, t, size=11.5, color=NAVY, bold=True)
        text(s, x + 0.18, y + 0.42, 2.35, 0.65, [[(g, {"color": TEXT})], [(gt, {"color": BLUE, "bold": True})]], size=9.5, line=1.15)
        ex = x + 2.6 if dx < 0 else x
        line(s, ex, y + 0.55, cx + (-0.95 if dx < 0 else 0.95) * 0.9, cy + dy * 0.35, color="B8CFEE", w=1.25)
    footer(s)
    notes(s, "An ecosystem only lasts if every participant gets real value. This map makes the exchange explicit — it is also the basis for partner conversations and for the commercial model.")


# ---------------------------------------------------------------- STAGE DEEP DIVES
STAGES = {
    "Explore": dict(goal="Decide whether an idea is worth testing.",
                    q=["Whose problem is this, and how painful is it?", "How do people solve it today?", "Why am I the right person to solve it?"],
                    check=["Write a one-line problem statement", "Describe the target customer", "List current alternatives", "Note your unfair advantages", "Pick three assumptions to test"],
                    signal="A clear, testable problem statement", support="Peer groups, idea clinics, the Explore templates"),
    "Validate": dict(goal="Prove that people want it — and will pay.",
                     q=["Will people pay, and how much?", "Who is the first, most eager customer?", "What is the smallest test I can run?"],
                     check=["Run 10–20 customer conversations", "Test a price with a pre-order or deposit", "Build a landing page or sample", "Record what you learned", "Decide: continue, change or stop"],
                     signal="Customers committing time or money", support="Validation clinic, interview guide, mentor feedback"),
    "Build": dict(goal="Create the simplest version people will pay for.",
                  q=["What is the minimum viable product?", "Which company structure and licence do I need?", "What will it cost to deliver?"],
                  check=["Define the first offer and scope", "Choose setup route and licence", "Estimate unit costs and margin", "Set up basic finance and contracts", "Line up first customers"],
                  signal="A first offer delivered to real customers", support="Setup, legal and product specialists; templates"),
    "Launch": dict(goal="Reach first customers in a repeatable way.",
                   q=["Which channel brings customers most efficiently?", "Is my pricing right?", "What do customers say after buying?"],
                   check=["Pick one acquisition channel to test", "Track cost per customer", "Collect reviews and feedback", "Refine pricing and packaging", "Build a simple sales process"],
                   signal="Repeat sales from a known channel", support="GTM sessions, marketing and sales specialists"),
    "Grow": dict(goal="Scale what works without breaking the business.",
                 q=["Where is the biggest bottleneck?", "Which roles or systems come next?", "How do I protect cash while growing?"],
                 check=["Map the operating bottleneck", "Automate repeat tasks", "Plan first key hires", "Review margins by product or client", "Set a 12-month cash plan"],
                 signal="Growth with healthy margins and cash", support="Operations, automation, finance and hiring support"),
    "Capital": dict(goal="Decide if external funding fits — and get ready.",
                    q=["Do I need outside money, and why?", "Which type of capital suits my business?", "What will investors ask to see?"],
                    check=["Define what the money is for", "Compare funding options", "Prepare core metrics and data room", "Sharpen the pitch and story", "Practise with experienced investors"],
                    signal="A funding decision made on evidence", support="Readiness review, pitch feedback, relevant introductions"),
}


def _stage_panel(s, x, w, name, idx, total_label):
    d = STAGES[name]
    rect(s, x, 2.15, w, 0.62, fill=NAVY if name == "Capital" else BLUE)
    text(s, x + 0.25, 2.24, w - 0.5, 0.45, [[B(f"STAGE {idx}", spacing=1.3, size=9.5, color=MID if name == "Capital" else "C9D6E8"), ("   " + (total_label or name), {"size": 16, "bold": True})]],
         size=16, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
    text(s, x, 2.95, w, 0.4, d["goal"], size=14, color=NAVY, bold=True)
    qw = w * 0.4
    text(s, x, 3.42, qw, 0.25, "KEY QUESTIONS", size=8.5, color=BLUE, bold=True, spacing=1.1)
    for k, q in enumerate(d["q"]):
        text(s, x, 3.72 + k * 0.7, qw - 0.1, 0.65, q, size=11, color=TEXT, line=1.15)
    cx = x + qw + 0.2
    cw = w - qw - 0.2
    text(s, cx, 3.42, cw, 0.25, "PRACTICAL CHECKLIST", size=8.5, color=BLUE, bold=True, spacing=1.1)
    for k, c in enumerate(d["check"]):
        yy = 3.72 + k * 0.44
        rect(s, cx, yy + 0.05, 0.16, 0.16, fill=None, line=BLUE, lw=1.25)
        text(s, cx + 0.28, yy, cw - 0.28, 0.4, c, size=10.5, color=TEXT)
    rect(s, x, 5.98, w, 0.82, fill=PALE)
    text(s, x + 0.2, 6.04, w - 0.4, 0.75,
         [[B("Sign of progress: ", color=NAVY), (d["signal"], {})], [B("Startup Roof support: ", color=BLUE), (d["support"], {})]],
         size=10.5, color=TEXT, line=1.25)


def _stage_slide(a, b, ia, ib, title, label_b=None):
    s = blank(P())
    header(s, 0, "The founder journey in practice", title, title_size=26)
    w = (W - 2 * ML - 0.5) / 2
    _stage_panel(s, ML, w, a, ia, None)
    _stage_panel(s, ML + w + 0.5, w, b, ib, label_b)
    footer(s)
    return s


def s_stage_1():
    s = _stage_slide("Explore", "Validate", 1, 2, "From idea to evidence.")
    notes(s, "Explore and Validate are where most founders lose time. The checklist turns vague intent into small, concrete tests. The key signal is commitment — customers giving time or money.")


def s_stage_2():
    s = _stage_slide("Build", "Launch", 3, 4, "From first offer to first customers.")
    notes(s, "Build means the simplest version people will pay for — not a perfect product. In the UAE, choosing the right setup route and licence is an early practical decision where specialists help.")


def s_stage_3():
    s = _stage_slide("Grow", "Capital", 5, 6, "From traction to scale — and capital where it fits.", label_b="Prepare for capital")
    notes(s, "Growth is about removing bottlenecks while protecting cash. Capital is optional: the first step is deciding whether outside money is needed at all, and which kind fits the business.")


# ---------------------------------------------------------------- KEY METRICS
def s_metrics():
    s = blank(P())
    header(s, 0, "Startup metrics, explained simply", "The numbers every founder should understand.", title_size=27)
    ms = [("MVP", "Minimum viable product", "The simplest version that real customers will use or pay for."),
          ("PMF", "Product–market fit", "Customers keep buying and recommending without heavy pushing."),
          ("CAC", "Customer acquisition cost", "Sales + marketing spend ÷ new customers won."),
          ("LTV", "Customer lifetime value", "Average gross profit per customer over the relationship."),
          ("GM", "Gross margin", "(Revenue − direct costs) ÷ revenue."),
          ("Burn", "Monthly net burn", "Cash out − cash in, per month."),
          ("Runway", "Months of cash left", "Cash in the bank ÷ monthly net burn."),
          ("Churn", "Customer churn", "Customers lost in a period ÷ customers at the start.")]
    cw, chh = (W - 2 * ML - 0.45) / 4, 2.05
    for i, (ab, nm, df) in enumerate(ms):
        col, row = i % 4, i // 4
        x = ML + col * (cw + 0.15)
        y = 2.15 + row * (chh + 0.2)
        rect(s, x, y, cw, chh, fill=NAVY if i in (2, 3) else PALE)
        dark = i in (2, 3)
        text(s, x + 0.22, y + 0.18, cw - 0.4, 0.55, ab, size=24, color=(WHITE if dark else BLUE), bold=True)
        text(s, x + 0.22, y + 0.8, cw - 0.4, 0.35, nm, size=12.5, color=(WHITE if dark else NAVY), bold=True)
        text(s, x + 0.22, y + 1.17, cw - 0.4, 0.8, df, size=11, color=("C9D6E8" if dark else TEXT), line=1.2)
    text(s, ML, 6.55, W - 2 * ML, 0.35,
         [[B("Rule of thumb many investors use: ", color=NAVY), ("LTV should comfortably exceed CAC — often cited as about 3×. Founder OS is planned to help track these simply.", {"color": MUTED})]],
         size=11)
    footer(s)
    notes(s, "These terms appear throughout startup conversations. Founder Academy will cover each one practically. The LTV:CAC ratio of around 3 is a widely used rule of thumb, not a law — it varies by sector and model.")


# ---------------------------------------------------------------- FUNDING OPTIONS
def s_funding_options():
    s = blank(P())
    header(s, 0, "Funding options compared", "There is more than one way to fund a business.", title_size=27)
    data = [["SOURCE", "BEST SUITED TO", "WHAT YOU GIVE UP", "WATCH OUT FOR"],
            ["Revenue and savings", "Businesses that can sell early", "Nothing — full control", "Slower growth; personal risk"],
            ["Friends and family", "Very early tests", "Sometimes equity", "Relationships if it goes wrong"],
            ["Grants and programmes", "Innovation, sector or social goals", "Time and reporting", "Eligibility and timelines"],
            ["Bank and SME finance", "Proven revenue and assets", "Repayments and collateral", "Cash-flow pressure"],
            ["Angel investors", "Early teams with potential to scale", "Equity", "Fit, terms and expectations"],
            ["Venture capital", "Fast-growing, large-market ventures", "Equity and some control", "Pressure for rapid scale"],
            ["Venture debt", "VC-backed companies with revenue", "Repayments and covenants", "Usually needs equity investors first"],
            ["Crowdfunding", "Consumer products with a community", "Rewards or equity", "Campaign effort; public scrutiny"]]
    table(s, ML, 2.1, W - 2 * ML, 4.5, data, [2.7, 3.35, 2.8, 3.18], size=11, header_size=9.5, row_h=0.48)
    text(s, ML, 6.62, W - 2 * ML, 0.3, "General guidance only — not financial advice. The right option depends on the business, its stage and the founder’s goals.", size=10, color=MUTED)
    footer(s)
    notes(s, "Many founders think funding means venture capital. This table widens the view. Revenue-funded growth is a legitimate and often better route for consumer, retail and service businesses.")


# ---------------------------------------------------------------- FUNDING LADDER
def s_funding_ladder():
    s = blank(P())
    header(s, 0, "How equity funding stages usually work", "Each round buys proof for the next step.", title_size=27)
    steps = [("Bootstrapped", "Own money and revenue", "A real problem and early demand"),
             ("Pre-seed", "Test and build the first version", "Team, insight and first signals"),
             ("Seed", "Find product–market fit", "Early traction and repeat usage"),
             ("Series A", "Build a repeatable growth engine", "Proven model and strong metrics"),
             ("Growth", "Scale into new markets", "Efficient, predictable growth")]
    n = len(steps)
    sw = (W - 2 * ML - 0.2) / n
    for i, (nm, purpose, evidence) in enumerate(steps):
        x = ML + i * (sw + 0.05)
        hgt = 0.9 + i * 0.4
        top = 6.35 - hgt
        rect(s, x, top, sw, hgt, fill=[PALE, "DCE8FB", "B8CFEE", BLUE, NAVY][i])
        dark = i >= 3
        text(s, x + 0.15, top + 0.12, sw - 0.3, 0.35, nm, size=14, color=(WHITE if dark else NAVY), bold=True)
        tx = 2.2
        text(s, x + 0.05, tx, sw - 0.15, 0.25, "USED TO", size=8.5, color=BLUE, bold=True, spacing=1.0)
        text(s, x + 0.05, tx + 0.27, sw - 0.15, 0.55, purpose, size=11, color=TEXT, line=1.15)
        text(s, x + 0.05, tx + 0.88, sw - 0.15, 0.25, "INVESTORS LOOK FOR", size=8.5, color=BLUE, bold=True, spacing=1.0)
        text(s, x + 0.05, tx + 1.15, sw - 0.15, 0.55, evidence, size=11, color=TEXT, line=1.15)
    rect(s, ML, 6.35, W - 2 * ML, 0.03, fill=NAVY)
    text(s, ML, 6.5, W - 2 * ML, 0.35, "Stage names and expectations vary by market and sector. Many businesses never raise equity — and that can be the right choice.", size=10.5, color=MUTED)
    footer(s)
    notes(s, "A simple explanation of equity rounds for founders who are new to the vocabulary. No amounts are shown because round sizes vary widely by market, sector and year.")


# ---------------------------------------------------------------- FOUNDER OS: SCREEN HELPERS
def _window(s, x, y, w, h, title="Founder OS"):
    rect(s, x, y, w, h, fill=WHITE, line="C9D6E8", lw=1)
    rect(s, x, y, w, 0.32, fill=PALE)
    for k in range(3):
        rect(s, x + 0.14 + k * 0.17, y + 0.11, 0.1, 0.1, fill="B8CFEE", shape=MSO_SHAPE.OVAL)
    text(s, x + 0.8, y + 0.07, 3, 0.2, title, size=8.5, color=MUTED, bold=True)
    text(s, x, y + h + 0.08, w, 0.25, "Illustrative product concept — not a live screen.", size=9, color=MUTED, italic=True)


def s_os_onboarding():
    s = blank(P())
    header(s, 0, "Founder OS · onboarding", "A five-minute profile that shapes everything after it.", tag="PLANNED CAPABILITY", title_size=27)
    ux, uy, uw, uh = ML, 2.15, 6.3, 4.35
    _window(s, ux, uy, uw, uh, "Founder OS · Create your profile")
    steps = ["About you", "Your business", "Stage", "Goals", "Support"]
    for i, st in enumerate(steps):
        x = ux + 0.35 + i * 1.18
        c = rect(s, x, uy + 0.55, 0.32, 0.32, fill=(BLUE if i <= 2 else "D9E5F6"), shape=MSO_SHAPE.OVAL)
        shape_text(c, str(i + 1), size=9, color=(WHITE if i <= 2 else MUTED), bold=True, margin=0)
        text(s, x - 0.25, uy + 0.92, 0.85, 0.25, st, size=8, color=(NAVY if i == 2 else MUTED), bold=(i == 2), align=PP_ALIGN.CENTER)
        if i < 4:
            line(s, x + 0.36, uy + 0.71, x + 1.14, uy + 0.71, color=("1765D1" if i < 2 else "D9E5F6"), w=1.5)
    text(s, ux + 0.35, uy + 1.35, 5.5, 0.35, "Which stage best describes your business today?", size=12.5, color=NAVY, bold=True)
    opts = ["Exploring an idea", "Validating demand", "Building a first offer", "Launched, finding customers", "Growing an established business"]
    for k, o in enumerate(opts):
        yy = uy + 1.85 + k * 0.45
        sel = k == 1
        rect(s, ux + 0.35, yy, 5.55, 0.37, fill=(PALE if sel else WHITE), line=(BLUE if sel else LINE), lw=1.0)
        rect(s, ux + 0.5, yy + 0.11, 0.15, 0.15, fill=(BLUE if sel else WHITE), line=(BLUE if sel else "B8CFEE"), shape=MSO_SHAPE.OVAL)
        text(s, ux + 0.8, yy + 0.07, 4.8, 0.3, o, size=10.5, color=(NAVY if sel else TEXT), bold=sel)
    gx = 7.4
    text(s, gx, 2.15, 5.3, 0.3, "WHAT THE PROFILE CAPTURES", size=9.5, color=BLUE, bold=True, spacing=1.3)
    caps = [("Founder", "Experience, skills, time available, location"), ("Business", "Sector, model, customers, team size"),
            ("Stage", "Explore, Validate, Build, Launch, Grow, Capital"), ("Goals", "What success looks like in the next 90 days"),
            ("Support", "Preferred formats and areas where help is needed"), ("Visibility", "What is shared, with whom — founder controls it")]
    for k, (a, b_) in enumerate(caps):
        yy = 2.55 + k * 0.66
        line(s, gx, yy, W - ML, yy, color=LINE)
        text(s, gx, yy + 0.13, 1.4, 0.4, a, size=12.5, color=NAVY, bold=True)
        text(s, gx + 1.45, yy + 0.13, 3.85, 0.5, b_, size=11.5, color=TEXT, line=1.15)
    footer(s)
    notes(s, "Onboarding is short and practical. The profile determines the stage-specific guidance, the sessions suggested and who a founder might be introduced to. Founders control their profile visibility.")


def s_os_engine():
    s = blank(P())
    header(s, 0, "Founder OS · the next-step engine", "How a founder’s next step is suggested.", tag="PLANNED CAPABILITY", title_size=27)
    cols = [("INPUTS", ["Profile and sector", "Current stage", "90-day goals", "Recent progress", "Time and budget"], PALE, NAVY),
            ("GUIDANCE", ["Stage playbooks", "Rules from mentors", "AI-assisted suggestions", "Human review for complex cases"], BLUE, WHITE),
            ("OUTPUTS", ["One clear next step", "A relevant resource", "A session to join", "A person to meet", "An opportunity to consider"], NAVY, WHITE)]
    cw = 3.35
    for i, (t, its, f, c) in enumerate(cols):
        x = ML + i * (cw + 0.75)
        rect(s, x, 2.2, cw, 3.65, fill=f)
        text(s, x + 0.3, 2.4, cw - 0.6, 0.3, t, size=10, color=(BLUE if f == PALE else MID if f == NAVY else "DCE6F5"), bold=True, spacing=1.4)
        for k, it in enumerate(its):
            text(s, x + 0.3, 2.85 + k * 0.56, cw - 0.6, 0.5, it, size=13, color=c, bold=(k == 0 and i == 2))
        if i < 2:
            line(s, x + cw + 0.08, 4.0, x + cw + 0.67, 4.0, color=BLUE, w=2.25, arrow=True)
    # feedback loop
    line(s, ML + 2 * (cw + 0.75) + cw / 2, 5.85, ML + 2 * (cw + 0.75) + cw / 2, 6.25, color="B8CFEE", w=1.5)
    line(s, ML + 2 * (cw + 0.75) + cw / 2, 6.25, ML + cw / 2, 6.25, color="B8CFEE", w=1.5)
    line(s, ML + cw / 2, 6.25, ML + cw / 2, 5.9, color="B8CFEE", w=1.5, arrow=True)
    text(s, ML + cw + 0.5, 6.32, 6, 0.3, "Progress recorded → the next suggestion improves", size=11, color=BLUE, bold=True, align=PP_ALIGN.CENTER)
    footer(s)
    notes(s, "The engine starts simple: stage playbooks and mentor-defined rules. AI assistance helps personalise and draft, and complex situations route to a human. Every completed step feeds the next suggestion.")


def s_os_matching():
    s = blank(P())
    header(s, 0, "Founder OS · mentor and specialist discovery", "Matched by need, stage and sector — not by chance.", tag="PLANNED CAPABILITY", title_size=26)
    ux, uy, uw, uh = ML, 2.15, 7.0, 4.35
    _window(s, ux, uy, uw, uh, "Founder OS · People")
    text(s, ux + 0.3, uy + 0.5, 6, 0.3, "Suggested for: pricing a consumer product", size=11, color=NAVY, bold=True)
    cards = [("Mentor", "Consumer brands · retail channels", "Match: sector, stage, need", "Request intro"),
             ("Specialist", "Pricing and unit economics", "Match: current challenge", "Book session"),
             ("Peer group", "Food and beverage founders", "Match: sector and stage", "Join group")]
    for k, (role, focus, why, cta) in enumerate(cards):
        y = uy + 0.95 + k * 1.1
        rect(s, ux + 0.3, y, uw - 0.6, 0.95, fill=WHITE, line=LINE)
        rect(s, ux + 0.48, y + 0.2, 0.55, 0.55, fill=[NAVY, BLUE, "1F4A85"][k], shape=MSO_SHAPE.OVAL)
        text(s, ux + 1.2, y + 0.13, 3.6, 0.3, role.upper(), size=8, color=BLUE, bold=True, spacing=1.0)
        text(s, ux + 1.2, y + 0.36, 3.7, 0.3, focus, size=12, color=NAVY, bold=True)
        text(s, ux + 1.2, y + 0.63, 3.7, 0.3, why, size=9.5, color=MUTED)
        b_ = rect(s, ux + uw - 1.95, y + 0.3, 1.45, 0.36, fill=BLUE, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.3)
        shape_text(b_, cta, size=9, color=WHITE, bold=True)
    gx = 8.1
    text(s, gx, 2.15, 4.6, 0.3, "MATCHING CRITERIA", size=9.5, color=BLUE, bold=True, spacing=1.3)
    crit = [("Need", "The founder’s current challenge"), ("Stage", "Where the business is today"), ("Sector", "Relevant industry experience"),
            ("Availability", "Real time the expert can give"), ("Consent", "Both sides agree before an introduction")]
    for k, (a, b_) in enumerate(crit):
        yy = 2.55 + k * 0.72
        line(s, gx, yy, W - ML, yy, color=LINE)
        text(s, gx, yy + 0.13, 1.5, 0.4, a, size=12.5, color=NAVY, bold=True)
        text(s, gx + 1.55, yy + 0.13, 3.0, 0.55, b_, size=11.5, color=TEXT, line=1.15)
    footer(s)
    notes(s, "Discovery suggests a small number of relevant people rather than a large directory. The founder requests; the expert accepts; only then is an introduction made. No real people are shown in this concept.")


def s_os_opps():
    s = blank(P())
    header(s, 0, "Founder OS · opportunities", "Relevant opportunities, with context and a next step.", tag="PLANNED CAPABILITY", title_size=27)
    ux, uy, uw, uh = ML, 2.15, 7.0, 4.35
    _window(s, ux, uy, uw, uh, "Founder OS · Radar")
    filters = ["All", "Programmes", "Funding", "Events", "Insights"]
    for k, f in enumerate(filters):
        p_ = rect(s, ux + 0.3 + k * 1.15, uy + 0.5, 1.05, 0.3, fill=(NAVY if k == 0 else PALE), shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
        shape_text(p_, f, size=8.5, color=(WHITE if k == 0 else NAVY), bold=True, margin=0)
    items = [("PROGRAMME", "Accelerator applications open — consumer and retail", "Why it matters: fits your stage and sector", "Closes in 3 weeks"),
             ("FUNDING", "Grant call for early-stage innovation projects", "Why it matters: non-dilutive; check eligibility", "Source linked"),
             ("INSIGHT", "Founder interview: lessons from a first retail launch", "Why it matters: you are entering retail next", "8-minute read")]
    for k, (cat, t, why, meta) in enumerate(items):
        y = uy + 1.0 + k * 1.05
        line(s, ux + 0.3, y, ux + uw - 0.3, y, color=LINE)
        text(s, ux + 0.3, y + 0.12, 1.4, 0.25, cat, size=8, color=BLUE, bold=True, spacing=1.0)
        text(s, ux + 0.3, y + 0.35, 5.0, 0.3, t, size=11.5, color=NAVY, bold=True)
        text(s, ux + 0.3, y + 0.65, 5.0, 0.3, why, size=9.5, color=MUTED)
        text(s, ux + uw - 1.75, y + 0.35, 1.45, 0.3, meta, size=9, color=MUTED, align=PP_ALIGN.RIGHT)
    gx = 8.1
    text(s, gx, 2.15, 4.6, 0.3, "EVERY ITEM SHOWS", size=9.5, color=BLUE, bold=True, spacing=1.3)
    sh = [("Relevance", "Why it fits this founder"), ("Source", "Credited and linked"), ("Date", "When it was published or closes"), ("Next step", "What to do about it")]
    for k, (a, b_) in enumerate(sh):
        yy = 2.55 + k * 0.82
        line(s, gx, yy, W - ML, yy, color=LINE)
        text(s, gx, yy + 0.14, 1.6, 0.4, a, size=13, color=NAVY, bold=True)
        text(s, gx + 1.65, yy + 0.14, 2.9, 0.5, b_, size=11.5, color=TEXT)
    text(s, gx, 5.95, 4.6, 0.6, "Sample items for illustration; they do not refer to real programmes.", size=10, color=MUTED, italic=True, line=1.2)
    footer(s)
    notes(s, "Radar inside Founder OS filters opportunities by a founder’s profile. Items are dated, credited and annotated. The examples on screen are samples, not real calls.")


def s_os_services():
    s = blank(P())
    header(s, 0, "Founder OS · service requests", "From “I need help” to a delivered, reviewed outcome.", tag="PLANNED CAPABILITY", title_size=27)
    flow = [("Request", "Founder describes the need in plain words."), ("Scope", "Need is clarified into a defined piece of work."),
            ("Match", "Suitable expert or partner is proposed."), ("Agree", "Scope, timing and price confirmed up front."),
            ("Deliver", "Work done; progress visible to the founder."), ("Review", "Founder rates the outcome; quality is tracked.")]
    fw = (W - 2 * ML) / 6
    for i, (a, b_) in enumerate(flow):
        x = ML + i * fw
        shp = MSO_SHAPE.PENTAGON if i == 0 else MSO_SHAPE.CHEVRON
        c = rect(s, x, 2.3, fw + 0.06, 0.65, fill=[PALE, PALE, BLUE, BLUE, NAVY, NAVY][i], shape=shp)
        shape_text(c, a, size=13, color=(NAVY if i < 2 else WHITE), bold=True)
        text(s, x + 0.15, 3.15, fw - 0.3, 1.0, b_, size=11.5, color=TEXT, line=1.2)
    rect(s, ML, 4.45, W - 2 * ML, 2.3, fill=PALE)
    text(s, ML + 0.3, 4.62, 6, 0.3, "QUALITY SAFEGUARDS UNDER TEST IN THE PILOT", size=9.5, color=BLUE, bold=True, spacing=1.3)
    sg = [("Clear scope first", "No open-ended engagements"), ("Transparent pricing", "Agreed before work starts"),
          ("Vetted providers", "Selected on track record"), ("Founder reviews", "Visible quality over time")]
    for k, (a, b_) in enumerate(sg):
        x = ML + 0.3 + k * 3.0
        text(s, x, 5.05, 2.8, 0.4, a, size=13.5, color=NAVY, bold=True)
        text(s, x, 5.45, 2.8, 0.8, b_, size=11.5, color=TEXT, line=1.2)
    footer(s)
    notes(s, "Service requests are a core paid-value hypothesis. The flow protects founders from vague, open-ended engagements. All safeguards will be tested in the pilot before scaling.")


def s_os_progress():
    s = blank(P())
    header(s, 0, "Founder OS · milestones and progress", "A simple plan that shows how far you have come.", tag="PLANNED CAPABILITY", title_size=27)
    ux, uy, uw, uh = ML, 2.15, 7.0, 4.35
    _window(s, ux, uy, uw, uh, "Founder OS · My plan")
    text(s, ux + 0.3, uy + 0.5, 5, 0.3, "90-day plan template · Validate stage", size=11.5, color=NAVY, bold=True)
    ms = [("Problem statement written", True), ("Interview guide prepared", True), ("Customer conversations", None),
          ("Price test with pre-orders", False), ("Decision: continue, change or stop", False)]
    for k, (m, st) in enumerate(ms):
        y = uy + 0.95 + k * 0.62
        fill = BLUE if st else (WHITE)
        rect(s, ux + 0.35, y + 0.08, 0.26, 0.26, fill=fill, line=(BLUE if st is not False else BLUE), lw=1.25, shape=MSO_SHAPE.OVAL)
        if st is None:
            rect(s, ux + 0.42, y + 0.15, 0.12, 0.12, fill=BLUE, shape=MSO_SHAPE.OVAL)
        text(s, ux + 0.8, y + 0.07, 4.2, 0.3, m, size=11.5, color=NAVY, bold=bool(st is None))
        tag_ = "Done" if st else ("In progress" if st is None else "Next")
        text(s, ux + uw - 1.6, y + 0.08, 1.3, 0.3, tag_, size=9.5, color=(BLUE if st is not False else MUTED), bold=True, align=PP_ALIGN.RIGHT)
        if k < 4:
            line(s, ux + 0.48, y + 0.36, ux + 0.48, y + 0.7, color="B8CFEE", w=1.25)
    gx = 8.1
    text(s, gx, 2.15, 4.6, 0.3, "WHY IT MATTERS", size=9.5, color=BLUE, bold=True, spacing=1.3)
    why = [("For founders", "Momentum and a record of decisions made."), ("For mentors", "Context before each conversation."),
           ("For readiness", "Evidence to share — only with consent."), ("For Startup Roof", "Measures whether support is useful.")]
    for k, (a, b_) in enumerate(why):
        yy = 2.55 + k * 0.85
        line(s, gx, yy, W - ML, yy, color=LINE)
        text(s, gx, yy + 0.13, 4.6, 0.3, a, size=13, color=NAVY, bold=True)
        text(s, gx, yy + 0.45, 4.6, 0.4, b_, size=11.5, color=TEXT)
    footer(s)
    notes(s, "Plans are templates by stage that founders adapt. Completed steps are the core measure of whether Startup Roof is helping. Shown as a template — not a real founder’s data.")


def s_os_architecture():
    s = blank(P())
    header(s, 0, "Founder OS · planned building blocks", "A simple, modular platform — built step by step.", tag="PLANNED ARCHITECTURE", title_size=27)
    layers = [("EXPERIENCE", "Web and mobile-friendly workspace · dashboard · notifications · community spaces", NAVY, WHITE),
              ("FOUNDER MODULES", "Profile · next steps · resources · learning · people · opportunities · services · progress", "17407F", WHITE),
              ("GUIDANCE LAYER", "Stage playbooks · mentor rules · AI-assisted drafting and suggestions · human escalation", BLUE, WHITE),
              ("DATA AND TRUST", "Consent records · visibility settings · secure storage · audit of introductions", "DCE8FB", NAVY),
              ("INTEGRATIONS", "Calendar and video · email and messaging · payments · partner tools, where rights allow", PALE, NAVY)]
    for i, (a, b_, f, c) in enumerate(layers):
        y = 2.15 + i * 0.86
        rect(s, ML, y, 2.6, 0.76, fill=f)
        text(s, ML + 0.2, y, 2.3, 0.76, a, size=11, color=c, bold=True, spacing=1.2, anchor=MSO_ANCHOR.MIDDLE)
        rect(s, ML + 2.7, y, W - 2 * ML - 2.7, 0.76, fill=WHITE, line=LINE)
        text(s, ML + 2.95, y, W - 2 * ML - 3.2, 0.76, b_, size=12.5, color=TEXT, anchor=MSO_ANCHOR.MIDDLE)
    text(s, ML, 6.55, W - 2 * ML, 0.3, "Technology choices will be made after the pilot confirms which capabilities founders actually use.", size=10.5, color=MUTED)
    footer(s)
    notes(s, "A conceptual architecture, not a technical specification. The important ideas are modularity, a guidance layer that combines rules, AI and people, and trust built into the data layer.")


def s_trust():
    s = blank(P())
    header(s, 0, "Trust, privacy and responsible AI", "Principles we intend to build in from day one.", title_size=27)
    pr = [("Consent first", "No introduction or data sharing without the founder’s agreement."),
          ("Founder-controlled visibility", "Founders decide what their profile shows, and to whom."),
          ("Data minimisation", "Collect only what improves the founder’s support."),
          ("Transparent AI", "AI-assisted content is labelled; founders can always ask a person."),
          ("Human escalation", "Complex legal, financial or personal matters go to qualified people."),
          ("Secure by design", "Access controls, encryption and audit trails as standard practice.")]
    cw = (W - 2 * ML - 0.4) / 3
    for i, (a, b_) in enumerate(pr):
        col, row = i % 3, i // 3
        x = ML + col * (cw + 0.2)
        y = 2.2 + row * 1.85
        rect(s, x, y, cw, 1.65, fill=(NAVY if i in (0, 4) else PALE))
        dark = i in (0, 4)
        text(s, x + 0.3, y + 0.25, cw - 0.6, 0.35, a, size=15, color=(WHITE if dark else NAVY), bold=True)
        text(s, x + 0.3, y + 0.7, cw - 0.6, 0.9, b_, size=12, color=("C9D6E8" if dark else TEXT), line=1.25)
    text(s, ML, 6.05, W - 2 * ML, 0.65,
         "Founder OS will be designed with the UAE Personal Data Protection Law (Federal Decree-Law No. 45 of 2021) and the rules of any other market it enters in mind; formal legal review will precede launch.",
         size=10.5, color=MUTED, line=1.25)
    footer(s)
    notes(s, "Trust is the foundation of any ecosystem that handles founder information. These are design principles; a formal privacy and legal review will be part of preparing the platform for launch.")


def s_os_mvp():
    s = blank(P())
    header(s, 0, "Founder OS · what to build first", "Start small, learn fast, then add depth.", title_size=27)
    cols = [("MUST HAVE", "Pilot", ["Founder profile and stage", "Next-step suggestions", "Resource and template library", "Session booking and requests", "Basic progress tracking"], BLUE),
            ("SHOULD HAVE", "After pilot", ["Mentor and specialist discovery", "Opportunities feed (Radar)", "Peer groups and discussions", "Service request workflow"], "1A55AC"),
            ("COULD HAVE", "Once proven", ["AI-assisted drafting and planning", "Partner tool integrations", "Learning paths with progress", "Mobile app experience"], "17407F"),
            ("LATER", "Separate decisions", ["Investor-readiness profiles", "Payments and marketplace", "Multi-market localisation", "Advanced analytics"], NAVY)]
    cw = (W - 2 * ML - 0.45) / 4
    for i, (t, when, its, c) in enumerate(cols):
        x = ML + i * (cw + 0.15)
        rect(s, x, 2.15, cw, 0.85, fill=c)
        text(s, x + 0.22, 2.25, cw - 0.4, 0.35, t, size=13, color=WHITE, bold=True, spacing=1.2)
        text(s, x + 0.22, 2.6, cw - 0.4, 0.3, when, size=10.5, color="DCE6F5")
        for k, it in enumerate(its):
            yy = 3.15 + k * 0.62
            rect(s, x, yy, cw, 0.54, fill=PALE)
            text(s, x + 0.2, yy + 0.06, cw - 0.35, 0.45, it, size=11.5, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    text(s, ML, 6.45, W - 2 * ML, 0.35, "Prioritisation will be confirmed with pilot founders; items may move between columns.", size=10.5, color=MUTED)
    footer(s)
    notes(s, "This prioritisation keeps the first version small and testable. The pilot can even start with simple tools behind the scenes — the point is to learn what founders use before building heavily.")
