"""Full edition: context slides built on sourced external data (see status note for full citations)."""
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

from pptx_kit import *  # noqa: F401,F403
import build_deck as bd

B = lambda t, **o: (t, dict(bold=True, **o))  # noqa: E731


def P():
    return bd.prs


def s_why_fail():
    s = blank(P())
    header(s, 0, "Why startups struggle", "Most failures come back to the market, cash and competition.", title_size=27)
    bar_chart(s, ML - 0.1, 2.05, 7.2, 4.3, ["Ran out of cash or\nfailed to raise", "No market need", "Got outcompeted"],
              [("Share of post-mortems", [0.38, 0.35, 0.20], BLUE)], kind="bar", fmt='0%', size=12, gap=55, max_v=0.45)
    text(s, ML, 6.35, 7, 0.3, "% of 111 startup post-mortems citing each reason (multiple reasons allowed).", size=10, color=MUTED)
    rx = 7.75
    text(s, rx, 2.15, 4.9, 0.3, "HOW STARTUP ROOF RESPONDS", size=9.5, color=BLUE, bold=True, spacing=1.3)
    rs = [("Market need", "Validation comes first: customer conversations and price tests before building."),
          ("Cash", "Margins, runway and funding options are taught early — not only at fundraising time."),
          ("Competition", "Radar insights, sector mentors and peer groups keep founders aware of the market.")]
    for k, (a, b_) in enumerate(rs):
        yy = 2.55 + k * 1.2
        line(s, rx, yy, W - ML, yy, color=LINE)
        text(s, rx, yy + 0.14, 4.9, 0.35, a, size=14, color=NAVY, bold=True)
        text(s, rx, yy + 0.5, 4.9, 0.7, b_, size=11.5, color=TEXT, line=1.2)
    source(s, "Source: CB Insights, “The Top 12 Reasons Startups Fail”, 2021.")
    footer(s)
    notes(s, "CB Insights analysed 111 startup post-mortems in 2021. Founders could cite several reasons. Two of the top three — no market need and running out of cash — are exactly what disciplined validation and early financial literacy address.")


def s_survival():
    s = blank(P())
    header(s, 0, "The survival challenge", "About half of new businesses are gone within five years.", title_size=27)
    line_chart(s, ML - 0.1, 2.05, 7.4, 4.2, ["Start", "After 1 year", "After 5 years", "After 10 years"],
               [("Still operating", [1.0, 0.796, 0.496, 0.336], BLUE)], fmt='0.0%', size=12, max_v=1.15)
    text(s, ML, 6.3, 7.2, 0.3, "Share of US private-sector establishments opened in March 1994 that were still operating.", size=10, color=MUTED)
    rx = 7.85
    tiles = [("34.7%", "of US establishments born in 2013 were still operating in 2023.", "US BLS, 2024"),
             ("≈ 50%", "of start-ups survive five years across OECD countries studied.", "OECD, 2015"),
             ("1 in 2", "is the simple takeaway: support in the early years matters.", "")]
    for k, (n, d, src) in enumerate(tiles):
        yy = 2.15 + k * 1.45
        rect(s, rx, yy, W - ML - rx, 1.3, fill=(NAVY if k == 2 else PALE))
        dk = k == 2
        text(s, rx + 0.25, yy + 0.15, 1.7, 0.6, n, size=26, color=(WHITE if dk else BLUE), bold=True)
        text(s, rx + 1.95, yy + 0.18, W - ML - rx - 2.15, 0.9, d, size=11.5, color=("C9D6E8" if dk else TEXT), line=1.2)
        if src:
            text(s, rx + 0.25, yy + 0.88, 1.6, 0.3, src, size=8.5, color=MUTED)
    source(s, "Sources: US Bureau of Labor Statistics, Business Employment Dynamics (1994 cohort; TED 2024 for the 2013 cohort); Calvino, Criscuolo & Menon, OECD STI Policy Paper, 2015.")
    footer(s)
    notes(s, "These are US and OECD figures — comparable UAE survival data is not published in the same way. The pattern is consistent internationally: a sharp drop in year one and roughly half surviving five years.")


def s_support_evidence():
    s = blank(P())
    header(s, 0, "Evidence that support helps", "Mentors, networks and structured programmes are linked to better outcomes.", title_size=26)
    stats = [("33%", "of New York tech founders mentored by successful entrepreneurs became top performers — over three times the rate of other firms.", "Endeavor Insight, 2015 (study of ~700 founders)"),
             ("2×", "Companies connected to a top-performing company were twice as likely to become top performers themselves.", "Endeavor Insight, “The Power of Entrepreneur Networks”"),
             ("47–171%", "more funding raised by accelerator companies than near-miss peers in three of four cohorts studied.", "Hallen, Cohen & Bingham, Organization Science, 2020")]
    cw = (W - 2 * ML - 0.4) / 3
    for i, (n, d, src) in enumerate(stats):
        x = ML + i * (cw + 0.2)
        rect(s, x, 2.2, cw, 3.7, fill=(NAVY if i == 0 else PALE))
        dk = i == 0
        text(s, x + 0.3, 2.45, cw - 0.6, 0.9, n, size=40, color=(WHITE if dk else BLUE), bold=True)
        text(s, x + 0.3, 3.5, cw - 0.6, 1.6, d, size=12.5, color=("DCE6F5" if dk else TEXT), line=1.25)
        text(s, x + 0.3, 5.2, cw - 0.6, 0.6, src, size=9, color=("8EA0B8" if dk else MUTED), line=1.15)
    text(s, ML, 6.15, W - 2 * ML, 0.6,
         "These studies show associations, not guarantees. They support Startup Roof’s design choice: combine mentoring, peer networks and structured programmes — then measure outcomes.",
         size=11, color=MUTED, line=1.25)
    footer(s)
    notes(s, "Be careful with causality: mentored founders may differ in other ways. But the pattern across studies is consistent enough to justify building support around mentors, networks and structure — and to measure our own outcomes.")


def s_mena_funding():
    s = blank(P())
    header(s, 0, "Regional momentum", "Startup funding in MENA reached a record in 2025.", title_size=27)
    bar_chart(s, ML - 0.1, 2.0, 7.6, 4.3, ["2020", "2021", "2022", "2023", "2024", "2025"],
              [("MENA startup funding, $bn", [0.654, 2.8, 3.94, 4.0, 2.3, 7.5], BLUE)], fmt='"$"0.0"bn"', size=12, gap=45, max_v=8.6)
    text(s, ML, 6.3, 7.4, 0.3, "Total startup funding raised in MENA, US$ billions (includes debt financing).", size=10, color=MUTED)
    rx = 8.0
    tiles = [("$7.5bn", "raised by 647 MENA startups in 2025 — a record year."),
             ("$1.1bn", "raised by UAE startups across 207 deals in 2024, ranking first in MENA that year."),
             ("1.2%", "of MENA funding went to female-founded startups in 2024 — a gap worth closing.")]
    for k, (n, d) in enumerate(tiles):
        yy = 2.15 + k * 1.42
        line(s, rx, yy, W - ML, yy, color=NAVY if k == 0 else LINE)
        text(s, rx, yy + 0.14, 1.7, 0.6, n, size=24, color=BLUE, bold=True)
        text(s, rx + 1.75, yy + 0.18, W - ML - rx - 1.75, 1.1, d, size=11.5, color=TEXT, line=1.2)
    source(s, "Source: Wamda annual MENA investment reviews (2020–2025). 2023 includes $1.77bn of debt; 2021 total as reported in Wamda’s 2021 review.")
    footer(s)
    notes(s, "Wamda figures include debt financing, which inflates 2023 and 2025. MAGNiTT, which excludes debt and mega-deals, reports lower totals (for example $3.8bn in 2025). The direction is the same: capital is available, and founders who are prepared are better placed to access it.")


def s_uae_context():
    s = blank(P())
    header(s, 0, "Why the UAE", "A national ambition to become a home for entrepreneurs.", title_size=27)
    rect(s, ML, 2.1, 4.2, 4.7, fill=NAVY)
    skyline(s, ML, 4.0, 4.2, 2.8, seed=11, sun=False)
    text(s, ML + 0.3, 2.35, 3.6, 0.3, "UAE FIRST", size=10, color=MID, bold=True, spacing=1.4)
    text(s, ML + 0.3, 2.7, 3.6, 1.4, "Starting where policy, capital and founders are converging.", size=16, color=WHITE, bold=True, line=1.2)
    facts = [("#1", "globally in the GEM National Entrepreneurship Context Index — for the fifth consecutive year.", "GEM 2025/2026"),
             ("63.5%", "of non-oil GDP comes from SMEs, which make up 94.4% of UAE companies.", "UAE Ministry of Economy / Central Bank"),
             ("557k → 1m", "SMEs at end-2022, with a national target of one million by 2030.", "UAE Minister of Economy, 2023"),
             ("30", "companies to grow into global unicorns under Dubai’s D33 agenda, plus 400 high-potential firms identified.", "Dubai Economic Agenda D33, 2023"),
             ("20", "unicorns targeted by 2031 under the national “Entrepreneurial Nation” initiative.", "UAE Ministry of Economy"),
             ("#19", "Dubai’s rank among global emerging startup ecosystems.", "Startup Genome GSER 2025")]
    gx = 5.15
    cw = (W - ML - gx - 0.2) / 2
    for i, (n, d, src) in enumerate(facts):
        col, row = i % 2, i // 2
        x = gx + col * (cw + 0.2)
        y = 2.1 + row * 1.6
        line(s, x, y, x + cw, y, color=NAVY if row == 0 else LINE)
        text(s, x, y + 0.12, cw, 0.5, n, size=22, color=BLUE, bold=True)
        text(s, x, y + 0.62, cw, 0.65, d, size=11, color=TEXT, line=1.17)
        text(s, x, y + 1.25, cw, 0.25, src, size=8.5, color=MUTED)
    footer(s)
    notes(s, "Every figure here is from official or established sources (listed in the sources slide). The message: the UAE has deliberately built an entrepreneur-friendly environment, which makes it the right place to start — and a credible base for a global ambition.")


def s_uae_founders():
    s = blank(P())
    header(s, 0, "UAE founders today", "High ambition, real opportunity — and a fear of failure to address.", title_size=26)
    panels = [("1 in 5", "adults in the UAE were starting or running a new business in 2025 — up from about one in seven in 2024.", 5, 1),
              ("9 in 10", "adults see good opportunities to start a business, among the highest of all economies surveyed.", 10, 9),
              ("Over half", "of those who see opportunities say fear of failure would stop them starting.", 2, 1)]
    cw = (W - 2 * ML - 0.4) / 3
    for i, (n, d, tot, hi) in enumerate(panels):
        x = ML + i * (cw + 0.2)
        rect(s, x, 2.15, cw, 4.0, fill=PALE)
        sz = 0.42 if tot <= 5 else 0.34
        gap = (cw - 0.5) / tot
        for k in range(tot):
            person(s, x + 0.25 + gap * (k + 0.5), 2.45, sz, fill=(BLUE if k < hi else "C4D8F6"))
        text(s, x + 0.3, 3.25, cw - 0.6, 0.7, n, size=30, color=NAVY, bold=True)
        text(s, x + 0.3, 4.0, cw - 0.6, 1.5, d, size=12.5, color=TEXT, line=1.25)
    rect(s, ML, 6.25, W - 2 * ML, 0.5, fill=NAVY)
    text(s, ML + 0.25, 6.3, W - 2 * ML - 0.5, 0.4,
         "Practical support, peer networks and small, low-risk first steps are a direct answer to fear of failure.", size=12, color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    source(s, "Source: Global Entrepreneurship Monitor (GEM), UAE country profile, 2025.", y=6.82)
    footer(s)
    notes(s, "GEM’s adult population survey shows high entrepreneurial intent in the UAE. The fear-of-failure finding is the most relevant for Startup Roof: structured validation and community make the first steps feel less risky.")


def s_ai_adoption():
    s = blank(P())
    header(s, 0, "AI is arriving in small businesses", "Founders are already using AI tools — guidance on using them well is the gap.", title_size=26)
    donut(s, ML, 2.2, 3.4, 3.4, ["Use generative AI", "Do not"], [0.31, 0.69], [BLUE, "DCE8FB"], hole=68)
    text(s, ML, 3.55, 3.4, 0.6, "31%", size=30, color=NAVY, bold=True, align=PP_ALIGN.CENTER)
    text(s, ML, 5.7, 3.4, 0.7, "of SMEs surveyed in seven OECD countries use generative AI (late 2024).", size=11.5, color=TEXT, align=PP_ALIGN.CENTER, line=1.2)
    bar_chart(s, 4.4, 2.15, 3.9, 3.5, ["Early 2024", "Sept 2025"], [("US firms using AI", [0.046, 0.10], "1F4A85")], fmt='0.0%', size=12, gap=70, max_v=0.13)
    text(s, 4.5, 5.7, 3.7, 0.7, "of US firms used AI to produce goods or services — doubling in under two years.", size=11.5, color=TEXT, align=PP_ALIGN.CENTER, line=1.2)
    rx = 8.75
    rect(s, rx, 2.2, W - ML - rx, 4.2, fill=NAVY)
    text(s, rx + 0.3, 2.45, 3.4, 0.3, "WHAT THIS MEANS", size=9.5, color=MID, bold=True, spacing=1.3)
    text(s, rx + 0.3, 2.85, 3.35, 3.4,
         [[B("AI as a founder tool, not a replacement for judgement.", color=WHITE)],
          {"runs": [("Founder Academy covers practical AI and automation. Founder OS plans AI-assisted guidance — always with human support for important decisions.", {"color": "C9D6E8", "size": 12})], "before": 8}],
         size=15, line=1.28)
    source(s, "Sources: OECD, “Generative AI and the SME Workforce”, 2025; US Census Bureau, Business Trends and Outlook Survey (2024–2025).")
    footer(s)
    notes(s, "The OECD survey covers more than 5,000 SMEs in seven countries. The US Census figure measures firms using AI to produce goods or services — a stricter definition. Both show quick adoption, which makes practical AI guidance valuable.")


def s_sources():
    s = blank(P())
    header(s, 0, "Sources and notes", "External data used in this presentation.", title_size=26)
    src = [
        "CB Insights, “The Top 12 Reasons Startups Fail” (2021) — analysis of 111 startup post-mortems.",
        "US Bureau of Labor Statistics, Business Employment Dynamics establishment survival data; “The Economics Daily”, 2024 (2013 cohort).",
        "Calvino, F., Criscuolo, C. & Menon, C. (2015), “Cross-country evidence on start-up dynamics”, OECD STI Policy Papers.",
        "Endeavor Insight (2015), research on New York City tech founders; “The Power of Entrepreneur Networks”.",
        "Hallen, B., Cohen, S. & Bingham, C. (2020), “Do Accelerators Work? If So, How?”, Organization Science 31(2).",
        "Wamda, annual MENA startup investment reviews, 2020–2025 (figures include debt financing).",
        "Global Entrepreneurship Monitor: 2025/2026 Global Report (NECI ranking) and UAE country profile, 2025.",
        "UAE Ministry of Economy; Central Bank of the UAE (SME share of non-oil GDP and of companies); Minister of Economy statement on SME numbers (2023).",
        "Dubai Media Office, launch of the Dubai Economic Agenda D33 (January 2023).",
        "UAE Ministry of Economy, “The Entrepreneurial Nation” initiative.",
        "Startup Genome, Global Startup Ecosystem Report 2025.",
        "OECD (2025), “Generative AI and the SME Workforce”; US Census Bureau, Business Trends and Outlook Survey.",
    ]
    for i, t in enumerate(src):
        col, row = i // 6, i % 6
        x = ML + col * 6.1
        y = 2.1 + row * 0.72
        text(s, x, y, 0.4, 0.3, f"{i + 1}", size=11, color=BLUE, bold=True)
        text(s, x + 0.4, y, 5.5, 0.7, t, size=10.5, color=TEXT, line=1.18)
    text(s, ML, 6.5, W - 2 * ML, 0.35,
         "Figures are reported as published by each source and year. Startup Roof’s own targets are ambitions, not results.", size=10, color=MUTED)
    footer(s)
    notes(s, "All external figures used in the deck, with source and year. Startup Roof has no traction data to report yet; the deck is clear about this throughout.")
