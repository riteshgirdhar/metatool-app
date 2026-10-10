"""Extra A4 pages for the full brochure, plus SVG chart builders (editable source, sourced data)."""

NAVY, BLUE, PALE, MID = "#10213B", "#1765D1", "#EDF4FE", "#4F8BE0"


def foot():
    return '<div class="foot"><span class="wm">STARTUP <b>ROOF</b></span><span>startuproof.com · <span class="pn"></span></span></div>'


def page(inner, cls=""):
    return f'<section class="page {cls}">{inner}{foot()}</section>\n'


# ---------------------------------------------------------------- SVG charts
def hbars(rows, w=170, max_v=0.45, fmt=lambda v: f"{v*100:.0f}%"):
    bh, gap, lw = 11, 7, 82
    h = len(rows) * (bh + gap)
    out = [f'<svg viewBox="0 0 {w} {h}" width="100%" xmlns="http://www.w3.org/2000/svg" font-family="Inter">']
    for i, (lab, v) in enumerate(rows):
        y = i * (bh + gap)
        bw = (w - lw - 18) * v / max_v
        out.append(f'<text x="{lw-3}" y="{y+bh/2+1.6}" text-anchor="end" font-size="4.6" fill="#253650">{lab}</text>')
        out.append(f'<rect x="{lw}" y="{y}" width="{bw:.1f}" height="{bh}" fill="{BLUE}"/>')
        out.append(f'<text x="{lw+bw+2:.1f}" y="{y+bh/2+1.5}" font-size="4.2" font-weight="700" fill="{NAVY}">{fmt(v)}</text>')
    out.append("</svg>")
    return "".join(out)


def columns(cats, vals, w=170, h=80, max_v=8.5, fmt=lambda v: f"${v:.1f}bn", color=BLUE, hl=None):
    n = len(cats)
    cw = (w - 10) / n
    bw = cw * 0.6
    base = h - 10
    out = [f'<svg viewBox="0 0 {w} {h}" width="100%" xmlns="http://www.w3.org/2000/svg" font-family="Inter">',
           f'<line x1="2" y1="{base}" x2="{w-2}" y2="{base}" stroke="#D5E2F3" stroke-width=".5"/>']
    for i, (c, v) in enumerate(zip(cats, vals)):
        x = 5 + i * cw + (cw - bw) / 2
        bh = (base - 10) * v / max_v
        col = NAVY if hl == i else color
        out.append(f'<rect x="{x:.1f}" y="{base-bh:.1f}" width="{bw:.1f}" height="{bh:.1f}" fill="{col}"/>')
        out.append(f'<text x="{x+bw/2:.1f}" y="{base-bh-2:.1f}" text-anchor="middle" font-size="4" font-weight="700" fill="{NAVY}">{fmt(v)}</text>')
        out.append(f'<text x="{x+bw/2:.1f}" y="{base+6}" text-anchor="middle" font-size="3.8" fill="#253650">{c}</text>')
    out.append("</svg>")
    return "".join(out)


def survival_line(w=170, h=78):
    pts = [("Start", 1.0), ("1 year", 0.796), ("5 years", 0.496), ("10 years", 0.336)]
    base, top = h - 12, 8
    xs = [12 + i * (w - 24) / 3 for i in range(4)]
    ys = [base - (base - top) * v for _, v in pts]
    out = [f'<svg viewBox="0 0 {w} {h}" width="100%" xmlns="http://www.w3.org/2000/svg" font-family="Inter">']
    for g in (0.25, 0.5, 0.75, 1.0):
        y = base - (base - top) * g
        out.append(f'<line x1="4" y1="{y:.1f}" x2="{w-4}" y2="{y:.1f}" stroke="#E6EEF9" stroke-width=".4"/>')
    out.append(f'<line x1="4" y1="{base}" x2="{w-4}" y2="{base}" stroke="#D5E2F3" stroke-width=".6"/>')
    area = " ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
    out.append(f'<polygon points="{xs[0]:.1f},{base} {area} {xs[-1]:.1f},{base}" fill="#EDF4FE"/>')
    out.append(f'<polyline points="{area}" fill="none" stroke="{BLUE}" stroke-width="1.6"/>')
    for (lab, v), x, y in zip(pts, xs, ys):
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.9" fill="{BLUE}" stroke="#fff" stroke-width=".6"/>')
        out.append(f'<text x="{x:.1f}" y="{y-4:.1f}" text-anchor="middle" font-size="4.2" font-weight="700" fill="{NAVY}">{v*100:.1f}%</text>')
        out.append(f'<text x="{x:.1f}" y="{base+7}" text-anchor="middle" font-size="3.8" fill="#253650">{lab}</text>')
    out.append("</svg>")
    return "".join(out)


def donut(pct, label, size=60):
    import math
    r, c = 22, 30
    circ = 2 * math.pi * r
    return (f'<svg viewBox="0 0 60 60" width="{size}mm" xmlns="http://www.w3.org/2000/svg" font-family="Inter">'
            f'<circle cx="{c}" cy="{c}" r="{r}" fill="none" stroke="#DCE8FB" stroke-width="9"/>'
            f'<circle cx="{c}" cy="{c}" r="{r}" fill="none" stroke="{BLUE}" stroke-width="9" stroke-dasharray="{circ*pct:.1f} {circ:.1f}" transform="rotate(-90 30 30)"/>'
            f'<text x="30" y="33" text-anchor="middle" font-size="10" font-weight="700" fill="{NAVY}">{label}</text></svg>')


def people_row(total, hi, size=7):
    out = []
    for k in range(total):
        col = BLUE if k < hi else "#C4D8F6"
        out.append(f'<svg viewBox="0 0 10 14" width="{size}mm" style="margin-right:1.2mm"><circle cx="5" cy="3.3" r="3" fill="{col}"/><path d="M0 14 V10 a5 5 0 0 1 10 0 V14 Z" fill="{col}"/></svg>')
    return "".join(out)


def skyline_svg(h=60, w=170, seed=5):
    import random
    rnd = random.Random(seed)
    out = [f'<svg viewBox="0 0 {w} {h}" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMax slice" style="display:block">']
    x = 2
    spire = w * 0.58
    while x < w - 4:
        if abs(x - spire) < 6:
            sw = 9
            yy = h
            for frac, hh in [(1, .28), (.72, .22), (.48, .16), (.28, .12)]:
                bh = hh * h
                bw = sw * frac
                out.append(f'<rect x="{x+(sw-bw)/2:.1f}" y="{yy-bh:.1f}" width="{bw:.1f}" height="{bh:.1f}" fill="{BLUE}"/>')
                yy -= bh
            out.append(f'<rect x="{x+sw/2-.4:.1f}" y="{yy-0.1*h:.1f}" width=".8" height="{0.1*h:.1f}" fill="{BLUE}"/>')
            x += sw + 1.5
            continue
        bw = rnd.uniform(6, 13)
        bh = rnd.uniform(.18, .55) * h
        col = rnd.choice(["#1A3358", "#1C3D6B", "#1F4A85"])
        out.append(f'<rect x="{x:.1f}" y="{h-bh:.1f}" width="{bw:.1f}" height="{bh:.1f}" fill="{col}"/>')
        x += bw + rnd.uniform(.6, 1.6)
    out.append("</svg>")
    return "".join(out)


def scene_svg():
    """Abstract founders-around-a-table illustration (used where a photo would go)."""
    cols = [NAVY, BLUE, "#1F4A85", MID, "#17407F"]
    out = ['<svg viewBox="0 0 170 70" width="100%" xmlns="http://www.w3.org/2000/svg"><rect width="170" height="70" fill="#DCE8FB"/>',
           '<rect x="18" y="47" width="134" height="6" rx="3" fill="#B8CFEE"/>']
    for i in range(5):
        cx = 30 + i * 27.5
        out.append(f'<circle cx="{cx}" cy="22" r="6.5" fill="{cols[i]}"/><path d="M{cx-11} 47 V40 a11 10 0 0 1 22 0 V47 Z" fill="{cols[i]}"/>')
    for x in (52, 107):
        out.append(f'<rect x="{x}" y="41" width="14" height="6" fill="#fff" stroke="#B8CFEE" stroke-width=".4"/>')
    out.append("</svg>")
    return "".join(out)


def photo_block(key, fallback_html, height_mm):
    return f'<!--PHOTO:{key}:{height_mm}-->{fallback_html}<!--/PHOTO-->'


# ---------------------------------------------------------------- pages
def p_glance():
    return page(f'''
  <div class="eyebrow">At a glance</div>
  <h1>A practical ecosystem around the founder — on one page.</h1>
  <div class="panel-dark" style="margin-top:2mm">
    <h2 style="font-size:15pt;line-height:1.35">Startup Roof brings practical guidance, useful tools and meaningful connections together to help founders take their next step.</h2>
    <p class="small" style="margin:3mm 0 0"><b style="color:#fff">Startup Roof</b> is the ecosystem. <b style="color:{MID}">Founder OS</b> is the digital workspace inside it.</p>
  </div>
  <div class="grid3" style="margin-top:6mm;gap:4mm">
    <div class="panel"><div class="eyebrow">What</div><h3 style="margin-top:1.5mm">A year-round founder ecosystem</h3><p class="small" style="margin:0">Community, programmes, services and a guided digital workspace.</p></div>
    <div class="panel"><div class="eyebrow">For whom</div><h3 style="margin-top:1.5mm">Founders first</h3><p class="small" style="margin:0">Aspiring, early-stage and growing founders — tech and non-tech.</p></div>
    <div class="panel"><div class="eyebrow">How</div><h3 style="margin-top:1.5mm">Build · Learn · Connect · Grow</h3><p class="small" style="margin:0">Next steps, practical learning, relevant people and opportunities.</p></div>
    <div class="panel"><div class="eyebrow">Where</div><h3 style="margin-top:1.5mm">UAE first, global ambition</h3><p class="small" style="margin:0">Starting in the UAE and widening coverage over time.</p></div>
    <div class="panel"><div class="eyebrow">Stage</div><h3 style="margin-top:1.5mm">Shaping and pilot phase</h3><p class="small" style="margin:0">Testing the founder experience with an initial group of contributors.</p></div>
    <div class="panel"><div class="eyebrow">Next</div><h3 style="margin-top:1.5mm">A small, measured pilot</h3><p class="small" style="margin:0">Useful sessions, onboarding and follow-up — then expand what works.</p></div>
  </div>
  <div class="eyebrow" style="margin:8mm 0 2mm">Contents</div>
  <div class="grid2" style="gap:0 8mm">
    <ul class="clean small">
      <li><span class="num">01</span><b style="color:{NAVY}">Why founders need a roof</b> — context and evidence</li>
      <li><span class="num">02</span><b style="color:{NAVY}">The concept</b> — ecosystem, pillars, audiences, sectors</li>
      <li><span class="num">03</span><b style="color:{NAVY}">The founder journey</b> — stages, checklists, metrics, funding</li>
      <li><span class="num">04</span><b style="color:{NAVY}">Founder OS</b> — the planned digital workspace</li>
    </ul>
    <ul class="clean small">
      <li><span class="num">05</span><b style="color:{NAVY}">Ecosystem services</b> — community, mentoring, Academy, experts</li>
      <li><span class="num">06</span><b style="color:{NAVY}">Value for the ecosystem</b> — investors and partners</li>
      <li><span class="num">07</span><b style="color:{NAVY}">Model, pilot and roadmap</b> — economics, measures, risks</li>
      <li><span class="num">08</span><b style="color:{NAVY}">People and participation</b> — contribute, FAQ, glossary</li>
    </ul>
  </div>''')


def p_struggle():
    fail = hbars([("Ran out of cash / failed to raise", .38), ("No market need", .35), ("Got outcompeted", .20)], w=235)
    return page(f'''
  <div class="eyebrow">Why startups struggle</div>
  <h1>Most failures come back to the market, cash and competition.</h1>
  <p class="lead" style="font-size:12pt">International evidence is consistent: many new businesses close within a few years, and the reasons are often avoidable with earlier validation, financial discipline and good advice.</p>
  <div class="rule" style="margin-top:5mm">
    <h2>Top reasons startups fail</h2>
    <p class="small muted" style="margin-bottom:3mm">% of 111 startup post-mortems citing each reason (multiple reasons allowed).</p>
    {fail}
    <p class="small muted" style="margin-top:1mm;font-size:8.5pt">Source: CB Insights, “The Top 12 Reasons Startups Fail”, 2021.</p>
  </div>
  <div class="rule" style="margin-top:5mm">
    <h2>How many businesses survive</h2>
    <p class="small muted" style="margin-bottom:3mm">Share of US private-sector establishments opened in March 1994 still operating.</p>
    {survival_line(w=215, h=66)}
    <div class="grid3" style="margin-top:4mm;gap:4mm">
      <div class="panel" style="padding:4mm"><div style="font-size:18pt;font-weight:700;color:{BLUE}">34.7%</div><p class="small" style="margin:0">of US establishments born in 2013 were still operating in 2023.</p></div>
      <div class="panel" style="padding:4mm"><div style="font-size:18pt;font-weight:700;color:{BLUE}">≈ 50%</div><p class="small" style="margin:0">of start-ups survive five years across OECD countries studied.</p></div>
      <div class="panel-dark" style="padding:4mm"><div style="font-size:18pt;font-weight:700">1 in 2</div><p class="small" style="margin:0">Support in the early years matters.</p></div>
    </div>
    <p class="small muted" style="margin-top:2mm;font-size:8.5pt">Sources: US Bureau of Labor Statistics, Business Employment Dynamics; BLS “The Economics Daily” (2024); Calvino, Criscuolo &amp; Menon, OECD (2015).</p>
  </div>''')


def p_evidence():
    return page(f'''
  <div class="eyebrow">Evidence that support helps</div>
  <h1>Mentors, networks and structure are linked to better outcomes.</h1>
  <div class="grid3" style="margin-top:3mm;gap:4mm">
    <div class="panel-dark"><div style="font-size:26pt;font-weight:700">33%</div><p class="small">of New York tech founders mentored by successful entrepreneurs became top performers — over three times the rate of other firms.</p><p class="small" style="color:#8EA0B8;font-size:8.5pt;margin:0">Endeavor Insight, 2015</p></div>
    <div class="panel"><div style="font-size:26pt;font-weight:700;color:{BLUE}">2×</div><p class="small">Companies connected to a top-performing company were twice as likely to become top performers.</p><p class="small muted" style="font-size:8.5pt;margin:0">Endeavor Insight</p></div>
    <div class="panel"><div style="font-size:26pt;font-weight:700;color:{BLUE}">47–171%</div><p class="small">more funding raised by accelerator companies than near-miss peers in three of four cohorts studied.</p><p class="small muted" style="font-size:8.5pt;margin:0">Hallen, Cohen &amp; Bingham, 2020</p></div>
  </div>
  <p class="small muted" style="margin-top:3mm">These studies show associations, not guarantees. They support Startup Roof’s design choice: combine mentoring, peer networks and structured programmes — then measure outcomes.</p>
  <div class="rule" style="margin-top:7mm">
    <h2>AI is arriving in small businesses</h2>
    <div style="display:grid;grid-template-columns:52mm 1fr;gap:8mm;align-items:center;margin-top:3mm">
      <div style="text-align:center">{donut(0.31, "31%", 50)}<p class="small" style="margin-top:2mm">of SMEs surveyed in seven OECD countries use generative AI (late 2024).</p></div>
      <div>
        {columns(["Early 2024", "Sept 2025"], [4.6, 10.0], w=120, h=62, max_v=12, fmt=lambda v: f"{v:.1f}%", color="#1F4A85")}
        <p class="small" style="margin-top:1mm">US firms using AI to produce goods or services — roughly doubling in under two years.</p>
      </div>
    </div>
    <div class="panel" style="margin-top:4mm"><h3>What this means for Startup Roof</h3><p class="small" style="margin:0">Practical AI and automation is a Founder Academy theme, and Founder OS plans AI-assisted guidance — always with human support for important decisions.</p></div>
    <p class="small muted" style="margin-top:2mm;font-size:8.5pt">Sources: OECD, “Generative AI and the SME Workforce” (2025); US Census Bureau, Business Trends and Outlook Survey.</p>
  </div>''')


def p_uae():
    chart = columns(["2020", "2021", "2022", "2023", "2024", "2025"], [0.654, 2.8, 3.94, 4.0, 2.3, 7.5], w=210, h=72, hl=5)
    return page(f'''
  <div class="eyebrow">The UAE and regional context</div>
  <h1>A national ambition to become a home for entrepreneurs.</h1>
  <div class="rule">
    <h2>MENA startup funding reached a record in 2025</h2>
    <p class="small muted" style="margin-bottom:2mm">Total startup funding raised in MENA, US$ billions (includes debt financing).</p>
    {chart}
    <p class="small muted" style="font-size:8.5pt;margin-top:1mm">Source: Wamda annual MENA investment reviews, 2020–2025. 2023 includes $1.77bn of debt.</p>
  </div>
  <div class="grid3" style="margin-top:4mm;gap:3mm 5mm">
    <div class="rule"><div style="font-size:17pt;font-weight:700;color:{BLUE}">#1</div><p class="small" style="margin:0">globally in the GEM National Entrepreneurship Context Index, five years running.</p><span class="small muted" style="font-size:8pt">GEM 2025/2026</span></div>
    <div class="rule"><div style="font-size:17pt;font-weight:700;color:{BLUE}">63.5%</div><p class="small" style="margin:0">of non-oil GDP from SMEs, which are 94.4% of UAE companies.</p><span class="small muted" style="font-size:8pt">UAE Ministry of Economy / Central Bank</span></div>
    <div class="rule"><div style="font-size:17pt;font-weight:700;color:{BLUE}">557k → 1m</div><p class="small" style="margin:0">SMEs at end-2022, with a target of one million by 2030.</p><span class="small muted" style="font-size:8pt">UAE Minister of Economy</span></div>
    <div class="rule"><div style="font-size:17pt;font-weight:700;color:{BLUE}">30</div><p class="small" style="margin:0">companies to grow into global unicorns under Dubai’s D33 agenda.</p><span class="small muted" style="font-size:8pt">Dubai Economic Agenda D33</span></div>
    <div class="rule"><div style="font-size:17pt;font-weight:700;color:{BLUE}">$1.1bn</div><p class="small" style="margin:0">raised by UAE startups across 207 deals in 2024, first in MENA.</p><span class="small muted" style="font-size:8pt">Wamda 2024 review</span></div>
    <div class="rule"><div style="font-size:17pt;font-weight:700;color:{BLUE}">#19</div><p class="small" style="margin:0">Dubai’s rank among global emerging startup ecosystems.</p><span class="small muted" style="font-size:8pt">Startup Genome GSER 2025</span></div>
  </div>
  <div style="background:{NAVY};margin-top:4mm;height:24mm;overflow:hidden">{photo_block("dubai", skyline_svg(h=40, w=290), 24)}</div>''')


def p_uae_founders():
    return page(f'''
  <div class="eyebrow">UAE founders today</div>
  <h1>High ambition, real opportunity — and a fear of failure to address.</h1>
  <p class="lead" style="font-size:12pt">The Global Entrepreneurship Monitor’s survey of UAE adults shows strong entrepreneurial intent. It also shows why practical support and small first steps matter.</p>
  <div style="margin-top:6mm">
    <div class="rule" style="display:grid;grid-template-columns:60mm 1fr;gap:6mm;align-items:center;padding:4mm 0">
      <div>{people_row(5, 1, 9)}</div>
      <div><div style="font-size:22pt;font-weight:700;color:{NAVY}">1 in 5</div><p style="margin:0">adults in the UAE were starting or running a new business in 2025 — up from about one in seven in 2024.</p></div>
    </div>
    <div class="rule" style="display:grid;grid-template-columns:60mm 1fr;gap:6mm;align-items:center;padding:4mm 0">
      <div>{people_row(10, 9, 4.6)}</div>
      <div><div style="font-size:22pt;font-weight:700;color:{NAVY}">9 in 10</div><p style="margin:0">adults see good opportunities to start a business — among the highest of all economies surveyed.</p></div>
    </div>
    <div class="rule" style="display:grid;grid-template-columns:60mm 1fr;gap:6mm;align-items:center;padding:4mm 0">
      <div>{people_row(2, 1, 9)}</div>
      <div><div style="font-size:22pt;font-weight:700;color:{NAVY}">Over half</div><p style="margin:0">of those who see opportunities say fear of failure would stop them starting.</p></div>
    </div>
  </div>
  <div class="panel-dark" style="margin-top:5mm"><h2>Our response</h2><p style="margin:0">Structured validation, peer groups, mentors and small, low-risk first steps make starting less daunting — and help more good ideas get tested properly.</p></div>
  <div class="panel" style="margin-top:4mm"><h3>Closing a gap</h3><p class="small" style="margin:0">Female-founded startups received 1.2% of MENA startup funding in 2024 (Wamda). Inclusive community, mentoring and readiness support are part of the design.</p></div>
  <p class="small muted" style="margin-top:3mm;font-size:8.5pt">Sources: Global Entrepreneurship Monitor, UAE country profile (2025); Wamda 2024 MENA review.</p>''')


def p_pillars_sectors():
    pill = lambda t, c, a, b, d: f'<div><div style="background:{c};color:#fff;font-weight:700;letter-spacing:.12em;text-align:center;padding:2.5mm 0;font-size:9.5pt">{t}</div><div class="panel" style="padding:3.5mm;min-height:52mm"><h3>{a}</h3><p class="small">{b}</p><div class="eyebrow" style="font-size:7pt">In Founder OS</div><div class="small" style="font-weight:700;color:{NAVY}">{d}</div></div></div>'
    return page(f'''
  <div class="eyebrow">Build · Learn · Connect · Grow</div>
  <h1>Four things founders need, under one roof.</h1>
  <svg viewBox="0 0 170 14" width="100%"><polyline points="4,13 85,1.5 166,13" fill="none" stroke="{NAVY}" stroke-width="1.3"/></svg>
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:2mm">
    {pill("BUILD", "#1A3358", "Turn an idea into a working business.", "Next-step plans, templates, product and setup guidance.", "Tasks and templates")}
    {pill("LEARN", "#1C3D6B", "Gain practical skills, quickly.", "Founder Academy sessions that end in an action.", "Learning progress")}
    {pill("CONNECT", "#1F4A85", "Reach the right people.", "Consent-based introductions, mentors, peers and specialists.", "Discovery and requests")}
    {pill("GROW", BLUE, "Find customers, capability and capital.", "Go-to-market, expert services, readiness and opportunities.", "Opportunities and progress")}
  </div>
  <div class="rule" style="margin-top:7mm">
    <h2>Sectors we serve — not only tech</h2>
    <table style="margin-top:2mm">
      <tr><th style="width:24%">Sector</th><th style="width:34%">Examples</th><th>Typical challenges</th></tr>
      <tr><td>Technology</td><td>Software, platforms, AI-enabled products</td><td>Product–market fit, technical cost, recurring revenue, investor readiness</td></tr>
      <tr><td>Consumer products</td><td>Food, beauty, home and lifestyle brands</td><td>Margin, sourcing and manufacturing, retail and e-commerce channels, brand</td></tr>
      <tr><td>Wellness</td><td>Fitness, nutrition, wellbeing, care</td><td>Trust, licensing and compliance, repeat customers, community</td></tr>
      <tr><td>Retail</td><td>Physical and online stores, marketplaces</td><td>Inventory and cash flow, channel mix, acquisition cost, operations</td></tr>
      <tr><td>Services</td><td>Agencies, consultancies, B2B and local services</td><td>Pricing and packaging, productising expertise, pipeline, hiring</td></tr>
    </table>
    <p class="small muted" style="margin-top:2mm">Venture funding is one route, not the goal. Many strong businesses grow from revenue — Startup Roof is designed for them too.</p>
  </div>''')


def p_personas():
    def persona(col, t, st, sit, need, help_):
        return f'''<div class="panel" style="padding:3.5mm;font-size:9.5pt">
      <div style="display:flex;gap:3mm;align-items:center">{people_row(1, 1, 9).replace(BLUE, col)}<div><h3 style="margin:0">{t}</h3><span class="tag" style="background:#fff">{st}</span></div></div>
      <div class="eyebrow" style="margin-top:3mm;font-size:7pt">Situation</div><p class="small" style="margin:0 0 1.5mm">{sit}</p>
      <div class="eyebrow" style="font-size:7pt">What they need</div><p class="small" style="margin:0 0 1.5mm">{need}</p>
      <div class="eyebrow" style="font-size:7pt">How Startup Roof helps</div><p class="small" style="margin:0">{help_}</p></div>'''
    return page(f'''
  <div style="display:flex;justify-content:space-between;align-items:center"><div class="eyebrow">Founders we design for</div><span class="tag">Illustrative personas</span></div>
  <h1>Four example founders, four different next steps.</h1>
  <div class="grid2" style="gap:4mm">
    {persona(NAVY, "The aspiring founder", "Explore", "Has an idea and a full-time job; unsure where to start.", "Clarity on whether the idea is worth testing.", "Validation guide, peer group, first clinic.")}
    {persona(BLUE, "The first-time brand owner", "Validate → Build", "Launching a consumer product with savings.", "Evidence that customers will buy at a viable margin.", "Pricing session, sourcing specialist, retail mentor.")}
    {persona("#1F4A85", "The tech founder", "Launch", "Has a product and early users; needs traction.", "A repeatable way to acquire paying customers.", "GTM sprint, customer-acquisition mentor, tool credits.")}
    {persona("#17407F", "The growing service business", "Grow", "Profitable agency, stuck at founder capacity.", "Systems, hiring and productised offers.", "Operations specialist, automation, peer group.")}
  </div>
  <p class="small muted" style="margin-top:2mm">Personas are illustrative composites used for design — not real people.</p>
  <div class="rule" style="margin-top:5mm">
    <h2>How value flows</h2>
    <table class="compact" style="margin-top:1.5mm">
      <tr><th style="width:30%">Participant</th><th>Gives</th><th>Gets</th></tr>
      <tr><td>Mentors and specialists</td><td>Experience and judgement</td><td>Purposeful impact, visibility, good-fit founders</td></tr>
      <tr><td>Investors and angels</td><td>Readiness feedback, sessions</td><td>Better-prepared founders</td></tr>
      <tr><td>Universities and incubators</td><td>Talent, programmes, research</td><td>Continuity for student founders</td></tr>
      <tr><td>Corporates</td><td>Challenges, pilots, expertise</td><td>Early innovation and partners</td></tr>
      <tr><td>Service and tool providers</td><td>Services, tools, offers</td><td>Relevant founder customers</td></tr>
      <tr><td>Founder community</td><td>Peer advice and accountability</td><td>Support, network, momentum</td></tr>
    </table>
  </div>''')


STAGES = [
    ("1", "Explore", "Decide whether an idea is worth testing.", ["Whose problem is this, and how painful is it?", "How do people solve it today?", "Why am I the right person to solve it?"],
     ["Write a one-line problem statement", "Describe the target customer", "List current alternatives", "Note your unfair advantages", "Pick three assumptions to test"], "A clear, testable problem statement", "Peer groups, idea clinics, Explore templates"),
    ("2", "Validate", "Prove that people want it — and will pay.", ["Will people pay, and how much?", "Who is the first, most eager customer?", "What is the smallest test I can run?"],
     ["Run 10–20 customer conversations", "Test a price with a pre-order or deposit", "Build a landing page or sample", "Record what you learned", "Decide: continue, change or stop"], "Customers committing time or money", "Validation clinic, interview guide, mentor feedback"),
    ("3", "Build", "Create the simplest version people will pay for.", ["What is the minimum viable product?", "Which company structure and licence do I need?", "What will it cost to deliver?"],
     ["Define the first offer and scope", "Choose setup route and licence", "Estimate unit costs and margin", "Set up basic finance and contracts", "Line up first customers"], "A first offer delivered to real customers", "Setup, legal and product specialists; templates"),
    ("4", "Launch", "Reach first customers in a repeatable way.", ["Which channel brings customers most efficiently?", "Is my pricing right?", "What do customers say after buying?"],
     ["Pick one acquisition channel to test", "Track cost per customer", "Collect reviews and feedback", "Refine pricing and packaging", "Build a simple sales process"], "Repeat sales from a known channel", "GTM sessions, marketing and sales specialists"),
    ("5", "Grow", "Scale what works without breaking the business.", ["Where is the biggest bottleneck?", "Which roles or systems come next?", "How do I protect cash while growing?"],
     ["Map the operating bottleneck", "Automate repeat tasks", "Plan first key hires", "Review margins by product or client", "Set a 12-month cash plan"], "Growth with healthy margins and cash", "Operations, automation, finance and hiring support"),
    ("6", "Prepare for capital", "Decide if external funding fits — and get ready.", ["Do I need outside money, and why?", "Which type of capital suits my business?", "What will investors ask to see?"],
     ["Define what the money is for", "Compare funding options", "Prepare core metrics and a data room", "Sharpen the pitch and story", "Practise with experienced investors"], "A funding decision made on evidence", "Readiness review, pitch feedback, relevant introductions"),
]


def _stage_block(st):
    n, name, goal, qs, checks, sig, sup = st
    col = NAVY if n == "6" else BLUE
    chk = "".join(f'<div style="display:flex;gap:2mm;margin-bottom:1.2mm"><span style="flex:none;width:3mm;height:3mm;border:1.3px solid {BLUE};margin-top:1.2mm"></span><span class="small">{c}</span></div>' for c in checks)
    qq = "".join(f'<p class="small" style="margin:0 0 1.5mm">{q}</p>' for q in qs)
    return f'''<div style="margin-bottom:4.5mm">
    <div style="background:{col};color:#fff;padding:2.2mm 4mm;font-weight:700"><span style="font-size:8pt;letter-spacing:.12em;color:#C9D6E8">STAGE {n}</span>&nbsp;&nbsp; {name}</div>
    <div style="display:grid;grid-template-columns:1fr 1.15fr;gap:5mm;padding:3mm 0 0">
      <div><h3>{goal}</h3><div class="eyebrow" style="font-size:7pt;margin:1.5mm 0 1mm">Key questions</div>{qq}</div>
      <div><div class="eyebrow" style="font-size:7pt;margin-bottom:1.5mm">Practical checklist</div>{chk}</div>
    </div>
    <div class="panel small" style="padding:2.5mm 4mm"><b style="color:{NAVY}">Sign of progress:</b> {sig} &nbsp;·&nbsp; <b style="color:{BLUE}">Startup Roof support:</b> {sup}</div>
  </div>'''


def p_stages(a, b, title):
    blocks = "".join(_stage_block(s) for s in STAGES[a:b])
    return page(f'''
  <div class="eyebrow">The founder journey in practice</div>
  <h1>{title}</h1>
  {blocks}''')


def p_metrics_funding():
    tiles = [("MVP", "Minimum viable product", "The simplest version customers will use or pay for."), ("PMF", "Product–market fit", "Customers keep buying and recommending."),
             ("CAC", "Customer acquisition cost", "Sales + marketing spend ÷ new customers."), ("LTV", "Customer lifetime value", "Gross profit per customer over time."),
             ("GM", "Gross margin", "(Revenue − direct costs) ÷ revenue."), ("Burn", "Monthly net burn", "Cash out − cash in, per month."),
             ("Runway", "Months of cash left", "Cash ÷ monthly net burn."), ("Churn", "Customer churn", "Customers lost ÷ customers at start.")]
    t = "".join(f'<div class="{"panel-dark" if i in (2,3) else "panel"}" style="padding:3.5mm"><div style="font-size:15pt;font-weight:700;color:{"#fff" if i in (2,3) else BLUE}">{a}</div><h3 style="font-size:9.5pt;{"color:#fff" if i in (2,3) else ""}">{b}</h3><p class="small" style="margin:0;font-size:8.8pt">{c}</p></div>' for i, (a, b, c) in enumerate(tiles))
    return page(f'''
  <div class="eyebrow">Startup metrics and funding options</div>
  <h1>The numbers every founder should understand.</h1>
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:2.5mm">{t}</div>
  <p class="small muted" style="margin-top:2mm">Rule of thumb many investors use: LTV should comfortably exceed CAC — often cited as about 3×. It varies by sector and model.</p>
  <div class="rule" style="margin-top:4mm">
    <h2>There is more than one way to fund a business</h2>
    <table class="compact" style="margin-top:2mm">
      <tr><th>Source</th><th>Best suited to</th><th>You give up</th><th>Watch out for</th></tr>
      <tr><td>Revenue and savings</td><td>Businesses that can sell early</td><td>Nothing — full control</td><td>Slower growth; personal risk</td></tr>
      <tr><td>Friends and family</td><td>Very early tests</td><td>Sometimes equity</td><td>Relationships if it goes wrong</td></tr>
      <tr><td>Grants and programmes</td><td>Innovation, sector or social goals</td><td>Time and reporting</td><td>Eligibility and timelines</td></tr>
      <tr><td>Bank and SME finance</td><td>Proven revenue and assets</td><td>Repayments, collateral</td><td>Cash-flow pressure</td></tr>
      <tr><td>Angel investors</td><td>Early teams with potential to scale</td><td>Equity</td><td>Fit, terms, expectations</td></tr>
      <tr><td>Venture capital</td><td>Fast-growing, large-market ventures</td><td>Equity and some control</td><td>Pressure for rapid scale</td></tr>
      <tr><td>Venture debt</td><td>VC-backed companies with revenue</td><td>Repayments, covenants</td><td>Usually needs equity first</td></tr>
      <tr><td>Crowdfunding</td><td>Consumer products with a community</td><td>Rewards or equity</td><td>Campaign effort; scrutiny</td></tr>
    </table>
    <p class="small muted" style="margin-top:2mm">General guidance only — not financial advice.</p>
  </div>''')


def p_ladder_readiness():
    steps = [("Bootstrapped", "Own money and revenue", "A real problem and early demand", "#EDF4FE", NAVY, 14),
             ("Pre-seed", "Test and build the first version", "Team, insight and first signals", "#DCE8FB", NAVY, 20),
             ("Seed", "Find product–market fit", "Early traction and repeat usage", "#B8CFEE", NAVY, 26),
             ("Series A", "Build a repeatable growth engine", "Proven model and strong metrics", BLUE, "#fff", 32),
             ("Growth", "Scale into new markets", "Efficient, predictable growth", NAVY, "#fff", 38)]
    cols = "".join(f'<div style="display:flex;flex-direction:column;justify-content:flex-end"><p class="small" style="margin:0 0 1mm"><b style="color:{BLUE};font-size:7pt;letter-spacing:.1em">USED TO</b><br>{p}</p><p class="small" style="margin:0 0 2mm"><b style="color:{BLUE};font-size:7pt;letter-spacing:.1em">INVESTORS LOOK FOR</b><br>{e}</p><div style="background:{f};color:{c};height:{h}mm;padding:2.5mm;font-weight:700">{n}</div></div>' for n, p, e, f, c, h in steps)
    groups = [("Business", ["A clear problem and target customer", "Evidence of demand or traction"]), ("Model", ["Unit economics you understand", "A credible plan for the funds"]),
              ("Team", ["The right founding team, gaps known", "Advisers or mentors where useful"]), ("Finance", ["Up-to-date accounts and runway", "A simple financial model"]),
              ("Legal", ["Clean company and share structure", "IP and key contracts in order"])]
    g = "".join(f'<div><div style="background:{c};color:#fff;font-weight:700;font-size:8pt;letter-spacing:.12em;text-align:center;padding:1.8mm 0">{t.upper()}</div>' + "".join(f'<div class="panel" style="padding:2.5mm;margin-top:1.5mm;display:flex;gap:2mm"><span style="flex:none;width:3mm;height:3mm;border:1.3px solid {BLUE};background:#fff;margin-top:.8mm"></span><span class="small" style="font-weight:600;color:{NAVY};font-size:8.8pt">{i}</span></div>' for i in its) + '</div>'
                for (t, its), c in zip(groups, [BLUE, "#1A55AC", "#17407F", "#1A3358", NAVY]))
    return page(f'''
  <div class="eyebrow">Capital, where it fits</div>
  <h1>How equity funding stages usually work.</h1>
  <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:1.5mm;border-bottom:1.2mm solid {NAVY}">{cols}</div>
  <p class="small muted" style="margin-top:2mm">Stage names and expectations vary by market and sector. Many businesses never raise equity — and that can be the right choice.</p>
  <div class="rule" style="margin-top:5mm">
    <h2>Investor readiness checklist</h2>
    <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:2mm;margin-top:2mm">{g}</div>
    <div class="panel-dark" style="margin-top:4mm;padding:4.5mm"><p class="small" style="margin:0"><b style="color:#fff">How Startup Roof helps:</b> readiness reviews, pitch feedback, data-room templates and — where relevant and with consent — introductions to investors who match the founder’s sector and stage.</p></div>
  </div>''')


def _win(title, body, h="auto"):
    return f'''<div style="border:1px solid #C9D6E8;font-size:8pt"><div style="background:{PALE};padding:1.4mm 2.5mm;color:#61738A;font-weight:700">● ● ●&nbsp;&nbsp; {title}</div><div style="padding:3mm">{body}</div></div>
  <div class="small muted" style="font-style:italic;font-size:7.5pt;margin-top:1mm">Illustrative product concept — not a live screen.</div>'''


def p_os_screens():
    onboarding = _win("Founder OS · Create your profile", "".join(
        f'<div style="border:1px solid {BLUE if i==1 else "#D5E2F3"};background:{PALE if i==1 else "#fff"};padding:1.6mm 2.5mm;margin-bottom:1.2mm;font-weight:{700 if i==1 else 400};color:{NAVY if i==1 else "#253650"}">{"●" if i==1 else "○"}&nbsp; {o}</div>'
        for i, o in enumerate(["Exploring an idea", "Validating demand", "Building a first offer", "Launched, finding customers", "Growing an established business"])).join(
        ['<b style="color:#10213B;font-size:9pt">Which stage best describes your business today?</b><div style="height:2mm"></div>', '']))
    matching = _win("Founder OS · People", "".join(
        f'<div style="border:1px solid #D5E2F3;padding:2mm;margin-bottom:1.5mm;display:flex;gap:2.5mm;align-items:center"><span style="flex:none;width:7mm;height:7mm;border-radius:50%;background:{c}"></span><div style="flex:1"><b style="color:{BLUE};font-size:6.5pt;letter-spacing:.1em">{r}</b><br><b style="color:{NAVY}">{f}</b></div><span style="background:{BLUE};color:#fff;font-weight:700;padding:1mm 2mm;border-radius:2mm;font-size:7pt">{cta}</span></div>'
        for r, f, cta, c in [("MENTOR", "Consumer brands · retail", "Request intro", NAVY), ("SPECIALIST", "Pricing and unit economics", "Book session", BLUE), ("PEER GROUP", "Food and beverage founders", "Join group", "#1F4A85")]))
    radar = _win("Founder OS · Radar", "".join(
        f'<div style="border-top:1px solid #D5E2F3;padding:1.8mm 0"><b style="color:{BLUE};font-size:6.5pt;letter-spacing:.1em">{c}</b><br><b style="color:{NAVY}">{t}</b><br><span style="color:#61738A">{w}</span></div>'
        for c, t, w in [("PROGRAMME", "Accelerator applications open (sample)", "Why it matters: fits your stage and sector"), ("FUNDING", "Grant call for early-stage innovation (sample)", "Why it matters: non-dilutive; check eligibility"), ("INSIGHT", "Founder interview: a first retail launch (sample)", "Why it matters: you are entering retail next")]))
    plan = _win("Founder OS · My plan", "".join(
        f'<div style="display:flex;justify-content:space-between;padding:1.6mm 0;border-bottom:1px solid #EEF3FB"><span style="color:{NAVY};font-weight:{700 if s=="In progress" else 400}">{"●" if s=="Done" else "◉" if s=="In progress" else "○"}&nbsp; {m}</span><b style="color:{BLUE if s!="Next" else "#61738A"}">{s}</b></div>'
        for m, s in [("Problem statement written", "Done"), ("Interview guide prepared", "Done"), ("Customer conversations", "In progress"), ("Price test with pre-orders", "Next"), ("Decision: continue, change or stop", "Next")]))
    return page(f'''
  <div style="display:flex;justify-content:space-between;align-items:center"><div class="eyebrow">Founder OS · inside the workspace</div><span class="tag">Planned capability</span></div>
  <h1>What founders will see — and why it helps.</h1>
  <div class="grid2" style="gap:5mm">
    <div><h3>Onboarding</h3><p class="small">A five-minute profile — stage, sector, goals, support needs and visibility settings — shapes everything after it.</p>{onboarding}</div>
    <div><h3>People</h3><p class="small">A few well-matched mentors, specialists and peers — by need, stage, sector and availability. Consent on both sides.</p>{matching}</div>
    <div><h3>Opportunities (Radar)</h3><p class="small">Relevant programmes, funding calls, events and insights — each dated, credited and with a next step.</p>{radar}</div>
    <div><h3>My plan</h3><p class="small">Stage templates founders adapt. Completed steps are how we measure whether support is useful.</p>{plan}</div>
  </div>''')


def p_os_engine():
    col = lambda t, items, bg, fg: f'<div style="background:{bg};color:{fg};padding:4mm"><div class="eyebrow" style="color:{"#C9D6E8" if fg=="#fff" else BLUE}">{t}</div>' + "".join(f'<div style="padding:1.3mm 0;font-weight:{600 if i==0 else 400}">{x}</div>' for i, x in enumerate(items)) + '</div>'
    return page(f'''
  <div style="display:flex;justify-content:space-between;align-items:center"><div class="eyebrow">Founder OS · how it works</div><span class="tag">Planned capability</span></div>
  <h1>The next-step engine, the building blocks and the principles.</h1>
  <div style="display:grid;grid-template-columns:1fr 6mm 1fr 6mm 1fr;align-items:stretch">
    {col("Inputs", ["Profile and sector", "Current stage", "90-day goals", "Recent progress", "Time and budget"], PALE, NAVY)}
    <div style="display:flex;align-items:center;justify-content:center;color:{BLUE};font-weight:700">→</div>
    {col("Guidance", ["Stage playbooks", "Rules from mentors", "AI-assisted suggestions", "Human review for complex cases"], BLUE, "#fff")}
    <div style="display:flex;align-items:center;justify-content:center;color:{BLUE};font-weight:700">→</div>
    {col("Outputs", ["One clear next step", "A relevant resource", "A session to join", "A person to meet", "An opportunity"], NAVY, "#fff")}
  </div>
  <p class="small" style="text-align:center;color:{BLUE};font-weight:700;margin-top:2mm">↺ Progress recorded → the next suggestion improves</p>
  <div class="rule" style="margin-top:4mm">
    <h2>Planned building blocks</h2>
    <table class="compact" style="margin-top:2mm">
      <tr><td style="width:30%">Experience</td><td>Web and mobile-friendly workspace · dashboard · notifications · community spaces</td></tr>
      <tr><td>Founder modules</td><td>Profile · next steps · resources · learning · people · opportunities · services · progress</td></tr>
      <tr><td>Guidance layer</td><td>Stage playbooks · mentor rules · AI-assisted drafting and suggestions · human escalation</td></tr>
      <tr><td>Data and trust</td><td>Consent records · visibility settings · secure storage · audit of introductions</td></tr>
      <tr><td>Integrations</td><td>Calendar and video · email and messaging · payments · partner tools, where rights allow</td></tr>
    </table>
  </div>
  <div class="rule" style="margin-top:4mm">
    <h2>Trust, privacy and responsible AI</h2>
    <div class="grid3" style="gap:2.5mm;margin-top:2mm">
      <div class="panel-dark" style="padding:2.6mm"><h3>Consent first</h3><p class="small" style="margin:0">No introduction or data sharing without agreement.</p></div>
      <div class="panel" style="padding:2.6mm"><h3>Founder-controlled visibility</h3><p class="small" style="margin:0">Founders decide what is shown, and to whom.</p></div>
      <div class="panel" style="padding:2.6mm"><h3>Data minimisation</h3><p class="small" style="margin:0">Collect only what improves support.</p></div>
      <div class="panel" style="padding:2.6mm"><h3>Transparent AI</h3><p class="small" style="margin:0">AI content labelled; a person is always available.</p></div>
      <div class="panel-dark" style="padding:2.6mm"><h3>Human escalation</h3><p class="small" style="margin:0">Complex matters go to qualified people.</p></div>
      <div class="panel" style="padding:2.6mm"><h3>Secure by design</h3><p class="small" style="margin:0">Access controls, encryption, audit trails.</p></div>
    </div>
    <p class="small muted" style="margin-top:2mm">Designed with the UAE Personal Data Protection Law (Federal Decree-Law No. 45 of 2021) in mind; formal legal review will precede launch.</p>
  </div>''')


def p_os_priorities():
    col = lambda t, w, items, c: f'<div><div style="background:{c};color:#fff;padding:3mm"><b style="letter-spacing:.1em">{t}</b><br><span class="small" style="color:#DCE6F5">{w}</span></div>' + "".join(f'<div class="panel" style="padding:2.5mm 3mm;margin-top:1.5mm;font-weight:700;color:{NAVY};font-size:9.5pt">{i}</div>' for i in items) + '</div>'
    return page(f'''
  <div class="eyebrow">Founder OS · what to build first</div>
  <h1>Start small, learn fast, then add depth.</h1>
  <p class="lead" style="font-size:12pt">The first version should be small enough to test quickly. The pilot can begin with simple tools behind the scenes — the point is to learn what founders actually use.</p>
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:2.5mm;margin-top:4mm">
    {col("MUST HAVE", "Pilot", ["Founder profile and stage", "Next-step suggestions", "Resource and template library", "Session booking and requests", "Basic progress tracking"], BLUE)}
    {col("SHOULD HAVE", "After pilot", ["Mentor and specialist discovery", "Opportunities feed (Radar)", "Peer groups and discussions", "Service request workflow"], "#1A55AC")}
    {col("COULD HAVE", "Once proven", ["AI-assisted drafting and planning", "Partner tool integrations", "Learning paths with progress", "Mobile app experience"], "#17407F")}
    {col("LATER", "Separate decisions", ["Investor-readiness profiles", "Payments and marketplace", "Multi-market localisation", "Advanced analytics"], NAVY)}
  </div>
  <div class="rule" style="margin-top:7mm">
    <h2>Service requests — from need to reviewed outcome</h2>
    <div style="display:grid;grid-template-columns:repeat(6,1fr);gap:1.2mm;margin-top:2mm;text-align:center;font-weight:700;font-size:9pt">
      <div style="background:{PALE};color:{NAVY};padding:2.5mm 0">Request</div><div style="background:{PALE};color:{NAVY};padding:2.5mm 0">Scope</div>
      <div style="background:{BLUE};color:#fff;padding:2.5mm 0">Match</div><div style="background:{BLUE};color:#fff;padding:2.5mm 0">Agree</div>
      <div style="background:{NAVY};color:#fff;padding:2.5mm 0">Deliver</div><div style="background:{NAVY};color:#fff;padding:2.5mm 0">Review</div>
    </div>
    <div class="grid2" style="margin-top:4mm;gap:3mm 8mm">
      <div class="callout"><h3>Clear scope first</h3><span class="small">No open-ended engagements.</span></div>
      <div class="callout"><h3>Transparent pricing</h3><span class="small">Agreed before any work starts.</span></div>
      <div class="callout"><h3>Vetted providers</h3><span class="small">Selected on track record and fit.</span></div>
      <div class="callout"><h3>Founder reviews</h3><span class="small">Quality visible over time.</span></div>
    </div>
    <p class="small muted" style="margin-top:3mm">Safeguards and prioritisation will be confirmed with pilot founders.</p>
  </div>''')


def p_rhythm_mentoring():
    return page(f'''
  <div style="display:flex;justify-content:space-between;align-items:center"><div class="eyebrow">Community and mentoring</div><span class="tag">Proposed</span></div>
  <h1>Support that does not stop when a programme ends.</h1>
  <div style="background:#DCE8FB;margin-bottom:5mm">{photo_block("community", scene_svg(), 55)}</div>
  <table>
    <tr><th style="width:20%">Rhythm</th><th>What could happen</th></tr>
    <tr><td>Weekly</td><td>Office hours · peer-group check-ins · new resources and opportunities in Founder OS</td></tr>
    <tr><td>Monthly</td><td>Thematic clinics · Academy sessions · mentor rounds · small founder gatherings</td></tr>
    <tr><td>Quarterly</td><td>Progress reviews · showcase sessions · partner workshops · cohort intakes</td></tr>
    <tr><td>Always on</td><td>Founder OS workspace · community discussions · service requests · Radar insights</td></tr>
  </table>
  <div class="rule" style="margin-top:6mm">
    <h2>How mentoring works</h2>
    <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:2mm;margin-top:2mm">
      {"".join(f'<div style="text-align:center"><div class="circle {"navy" if i==4 else ""}" style="margin:0 auto 1.5mm">{i+1}</div><h3 style="font-size:10pt">{a}</h3><p class="small" style="font-size:8.8pt">{b}</p></div>' for i, (a, b) in enumerate([("Prepare", "Founder states the question and context."), ("Match", "A relevant mentor accepts."), ("Meet", "30–60 minutes on one decision."), ("Commit", "One or two concrete actions."), ("Follow up", "Progress check; next session if useful.")]))}
    </div>
    <div class="grid2" style="gap:4mm;margin-top:2mm">
      <div class="panel"><div class="eyebrow">Mentors commit to</div><ul class="dots small" style="margin-top:2mm"><li>Honest, practical feedback</li><li>Declaring conflicts of interest</li><li>Respecting confidentiality</li><li>Agreed availability</li></ul></div>
      <div class="panel-dark"><div class="eyebrow">Founders commit to</div><ul class="dots small" style="margin-top:2mm;color:#fff"><li>Preparing a clear question</li><li>Respecting the mentor’s time</li><li>Acting on what was agreed</li><li>Sharing progress and feedback</li></ul></div>
    </div>
  </div>''')


def p_curriculum_catalogue():
    return page(f'''
  <div style="display:flex;justify-content:space-between;align-items:center"><div class="eyebrow">Founder Academy and expert services</div><span class="tag">Proposed</span></div>
  <h1>Learn it on Monday. Use it on Tuesday.</h1>
  <table class="compact">
    <tr><th style="width:27%">Theme</th><th style="width:37%">Example session</th><th>Founder leaves with</th></tr>
    <tr><td>Idea validation</td><td>Customer interviews that reveal the truth</td><td>An interview guide and 10 people to call</td></tr>
    <tr><td>Business models</td><td>How your business actually makes money</td><td>A one-page business model</td></tr>
    <tr><td>AI and automation</td><td>Practical AI tools for a small team</td><td>Three tasks automated or AI-assisted</td></tr>
    <tr><td>GTM and customer acquisition</td><td>Choosing your first channel</td><td>A 30-day acquisition test plan</td></tr>
    <tr><td>Pricing and unit economics</td><td>Pricing with confidence; knowing your margin</td><td>A pricing sheet and unit-cost model</td></tr>
    <tr><td>Pitch readiness</td><td>The story investors and partners need</td><td>A 10-slide outline and practice feedback</td></tr>
    <tr><td>Legal and operational foundations</td><td>Setup routes, contracts, compliance basics</td><td>A setup checklist and key contract list</td></tr>
    <tr><td>Consumer-brand and retail</td><td>From product to shelf or online store</td><td>A channel plan and retailer pitch</td></tr>
  </table>
  <p class="small muted" style="margin-top:1.5mm">A sample curriculum showing the format; no course catalogue exists yet.</p>
  <div class="rule" style="margin-top:4mm">
    <h2>Expert services — what founders typically need</h2>
    <div class="grid2" style="gap:1.8mm 7mm;margin-top:2mm">
      {"".join(f'<div class="callout" style="border-color:{BLUE if i%3 else NAVY}"><h3>{a}</h3><span class="small">{b}</span></div>' for i, (a, b) in enumerate([("Legal", "Setup documents, shareholder agreements, contracts, IP basics"), ("Accounting and finance", "Bookkeeping, VAT registration, models, cash-flow planning"), ("Branding and design", "Identity, packaging, pitch design, website look and feel"), ("Technology and automation", "No-code builds, app scoping, workflow automation"), ("Marketing and sales", "Positioning, campaigns, sales scripts and CRM"), ("Customer communication", "WhatsApp and email journeys, support, reviews"), ("Business setup", "Licence route, free zone or mainland, banking, visas"), ("Product and retail guidance", "Sourcing, manufacturing, listings, retail entry")]))}
    </div>
    <p class="small muted" style="margin-top:2mm">Providers, packages and prices will be validated in the pilot; no supplier is confirmed.</p>
  </div>''')


def p_partners_detail():
    return page(f'''
  <div class="eyebrow">Universities, corporates and service partners</div>
  <h1>Practical ways to collaborate.</h1>
  <h2>Continuity for student and alumni founders</h2>
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1.2mm;margin:2mm 0 2mm;text-align:center;font-weight:700;font-size:9.5pt">
    <div style="background:{PALE};color:{NAVY};padding:3mm 0">Idea in class</div><div style="background:{PALE};color:{NAVY};padding:3mm 0">University programme</div>
    <div style="background:{BLUE};color:#fff;padding:3mm 0">Startup Roof</div><div style="background:{NAVY};color:#fff;padding:3mm 0">Alumni founder</div>
  </div>
  <div class="grid2" style="gap:6mm">
    <div><div class="eyebrow" style="margin-bottom:1mm">What universities could gain</div><ul class="clean small"><li>Support after programmes end</li><li>Practitioner mentors and specialists</li><li>Visibility for student ventures</li><li>Practical content for courses</li></ul></div>
    <div><div class="eyebrow" style="margin-bottom:1mm">Possible formats</div><ul class="clean small"><li>Guest clinics and workshops</li><li>Joint founder challenges</li><li>Mentor office hours on campus</li><li>Founder OS access for student founders</li></ul></div>
  </div>
  <div class="rule" style="margin-top:5mm">
    <h2>Corporates and service providers</h2>
    <table style="margin-top:2mm;font-size:9.2pt">
      <tr><th>Partner type</th><th>Can offer</th><th>Can gain</th><th>Starting format</th></tr>
      <tr><td>Corporate innovation teams</td><td>Challenges, pilots, expertise</td><td>Early access to solutions and talent</td><td>A themed founder challenge</td></tr>
      <tr><td>Professional firms</td><td>Legal, finance, tax, setup advice</td><td>Relationships with future clients</td><td>Monthly office hours</td></tr>
      <tr><td>Technology providers</td><td>Tools, credits, technical guidance</td><td>Adoption by relevant founders</td><td>A limited tool pilot</td></tr>
      <tr><td>Banks and financial institutions</td><td>SME banking, finance education</td><td>Better-prepared SME customers</td><td>A founder finance clinic</td></tr>
      <tr><td>Venues and co-working</td><td>Space for sessions</td><td>Community activity and visibility</td><td>Hosting a founder evening</td></tr>
      <tr><td>Media and content</td><td>Reach, interviews, editorial skill</td><td>Founder stories and insights</td><td>A co-created guide or series</td></tr>
    </table>
    <p class="small muted" style="margin-top:2mm">Illustrative formats for discussion. No partnerships are signed or implied.</p>
  </div>''')


def p_economics():
    lab = {0: ("—", "#fff", "#61738A"), 1: ("Explore", PALE, NAVY), 2: ("Test", "#8DB4EA", NAVY), 3: ("Scale", NAVY, "#fff")}
    rows = [("Paid memberships or tools", [1, 2, 3]), ("Specialist support packages", [1, 2, 3]), ("Structured programmes", [1, 2, 3]), ("Partner and service revenue", [1, 1, 2]),
            ("Corporate or university programmes", [1, 2, 2]), ("Sponsorship of suitable activities", [0, 1, 2]), ("Selective incubation arrangements", [0, 1, 2])]
    trs = "".join(f'<tr><td>{r}</td>' + "".join(f'<td style="background:{lab[v][1]};color:{lab[v][2]};text-align:center;font-weight:700;border:2px solid #fff">{lab[v][0]}</td>' for v in vals) + '</tr>' for r, vals in rows)
    box = lambda t, s, bg, fg: f'<div style="background:{bg};color:{fg};padding:3mm;flex:1"><b>{t}</b><br><span class="small" style="color:{fg}">{s}</span></div>'
    op = lambda o: f'<div style="color:{BLUE};font-weight:700;font-size:16pt;padding:0 1.5mm;align-self:center">{o}</div>'
    return page(f'''
  <div style="display:flex;justify-content:space-between;align-items:center"><div class="eyebrow">Commercial model</div><span class="tag">Hypotheses</span></div>
  <h1>Revenue to explore, test and scale — in order.</h1>
  <table>
    <tr><th style="width:40%">Revenue hypothesis</th><th style="text-align:center">Now · Shape</th><th style="text-align:center">Next · Pilot</th><th style="text-align:center">Then · Expand</th></tr>
    {trs}
  </table>
  <p class="small muted" style="margin-top:2mm">“Scale” only after unit economics are proven. Sequencing will change with pilot evidence.</p>
  <div class="rule" style="margin-top:5mm">
    <h2>How each paid service must pay its way</h2>
    <div style="display:flex;margin-top:2mm">{box("Price paid", "by founder or partner", PALE, NAVY)}{op("−")}{box("Delivery cost", "expert time, materials, venue", "#DCE8FB", NAVY)}{op("−")}{box("Platform cost", "tools, support, admin", "#B8CFEE", NAVY)}{op("=")}{box("Contribution", "sustains the free layer", NAVY, "#fff")}</div>
    <div class="eyebrow" style="margin:4mm 0 1mm">Questions the pilot must answer</div>
    <ul class="dots small" style="columns:2;column-gap:8mm"><li>What will founders pay for, and how much?</li><li>How much expert time does each outcome take?</li><li>Which services work in groups to lower cost?</li><li>Where do partners fund value for founders?</li><li>What does free access cost per active founder?</li><li>Which offers lead to repeat use?</li></ul>
    <p class="small muted">No financial forecast is presented. Pricing will be tested before anything is published.</p>
  </div>''')


def p_pilot_kpis():
    return page(f'''
  <div style="display:flex;justify-content:space-between;align-items:center"><div class="eyebrow">Pilot design and measurement</div><span class="tag">Proposed</span></div>
  <h1>A small, measured test of the founder experience.</h1>
  <table>
    <tr><td style="width:22%">Who</td><td>A small group of founders across stages and sectors, including non-tech businesses.</td></tr>
    <tr><td>What</td><td>Onboarding, a validation or growth track, clinics, mentor sessions and follow-up.</td></tr>
    <tr><td>How</td><td>Simple tools first; Founder OS features introduced as they are ready.</td></tr>
    <tr><td>Contributors</td><td>Participants deliver sessions and support in roles that suit their time and skills.</td></tr>
    <tr><td>Learning</td><td>Founder interviews, feedback after every session, delivery cost tracked throughout.</td></tr>
  </table>
  <div class="panel-dark" style="margin-top:4mm"><div class="eyebrow" style="margin-bottom:2mm">The pilot succeeds if</div>
    <div class="grid3" style="gap:2mm 5mm" ><span class="small" style="color:#fff">● Founders complete useful next steps</span><span class="small" style="color:#fff">● They return without being chased</span><span class="small" style="color:#fff">● Sessions are rated as practical</span><span class="small" style="color:#fff">● Contributors deliver reliably</span><span class="small" style="color:#fff">● We know the real cost to serve</span></div></div>
  <div class="rule" style="margin-top:5mm">
    <div style="display:grid;grid-template-columns:55mm 1fr;gap:6mm">
      <div class="panel" style="border-left:1.5mm solid {BLUE}"><div class="eyebrow">North-star measure</div><div style="font-size:16pt;font-weight:700;color:{NAVY};line-height:1.15;margin:2mm 0">Completed founder next steps</div><p class="small" style="margin:0">Counts when the founder confirms it is done — usefulness, not activity.</p></div>
      <table style="font-size:9.3pt">
        <tr><td>Activation</td><td>New founders completing a profile and first step</td></tr>
        <tr><td>Follow-through</td><td>Agreed actions completed after sessions</td></tr>
        <tr><td>Return rate</td><td>Founders active again within 30 days</td></tr>
        <tr><td>Useful introductions</td><td>Introductions leading to a real conversation</td></tr>
        <tr><td>Session quality</td><td>Founder rating of practical value</td></tr>
        <tr><td>Cost to serve</td><td>Delivery cost per active founder</td></tr>
        <tr><td>Paid conversion</td><td>Founders choosing an optional paid service</td></tr>
        <tr><td>Contributor reliability</td><td>Sessions delivered as committed</td></tr>
      </table>
    </div>
  </div>''')


def p_path_risks():
    steps = [("Shape", "Today", PALE, NAVY, 16), ("Pilot", "Next", "#DCE8FB", NAVY, 22), ("10,000", "Launch threshold", BLUE, "#fff", 28),
             ("March 2027", "Tentative target", "#1A55AC", "#fff", 34), ("100,000", "Wider ambition", NAVY, "#fff", 40)]
    st = "".join(f'<div style="display:flex;flex-direction:column;justify-content:flex-end"><div style="background:{bg};color:{fg};height:{h}mm;padding:2.5mm"><div style="font-weight:700;font-size:{12 if i<2 else 13}pt">{a}</div><div style="font-size:7pt;letter-spacing:.1em;font-weight:700;opacity:.85">{b.upper()}</div></div></div>' for i, (a, b, bg, fg, h) in enumerate(steps))
    return page(f'''
  <div style="display:flex;justify-content:space-between;align-items:center"><div class="eyebrow">Milestones and risks</div><span class="tag">Targets, not traction</span></div>
  <h1>Each step must be earned by the one before it.</h1>
  <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:1.5mm;border-bottom:1.2mm solid {NAVY}">{st}</div>
  <p class="small muted" style="margin-top:2mm">10,000 free users is the threshold for a public launch event; March 2027 is a tentative target subject to readiness; 100,000 free users is the wider ambition. All will be refined through the pilot. None represents current users or traction.</p>
  <div class="rule" style="margin-top:5mm">
    <h2>Risks and how we address them</h2>
    <table style="margin-top:2mm;font-size:9.3pt">
      <tr><th style="width:26%">Risk</th><th style="width:32%">Why it matters</th><th>How we address it</th></tr>
      <tr><td>Low founder engagement</td><td>Without use, there is no ecosystem</td><td>Small pilot, practical formats, measure return rate</td></tr>
      <tr><td>Inconsistent delivery</td><td>Volunteer time can be unreliable</td><td>Clear commitments; roles based on reliable delivery</td></tr>
      <tr><td>Quality of advice</td><td>Poor advice harms founders and trust</td><td>Vetted contributors, founder ratings, human escalation</td></tr>
      <tr><td>Cost to serve too high</td><td>Free access must be sustainable</td><td>Group formats; unit-economics test per service</td></tr>
      <tr><td>Platform built too early</td><td>Wasted effort on unused features</td><td>Simple tools first; build what the pilot proves</td></tr>
      <tr><td>Data and privacy</td><td>Founder trust is essential</td><td>Consent-first design; data-protection review</td></tr>
      <tr><td>Over-promising</td><td>Credibility with founders and partners</td><td>Clear stage labels; no claims beyond evidence</td></tr>
    </table>
  </div>''')


def p_faq():
    qa = [("Is Startup Roof an accelerator or a fund?", "Neither today. It is a founder ecosystem with a planned digital workspace. Any investment activity would need its own structure and approvals."),
          ("Is Founder OS live?", "Not yet. It is planned and will be introduced step by step, starting in the pilot."),
          ("Do I need a tech startup to join?", "No. Consumer, wellness, retail and service businesses are equally welcome."),
          ("Will it cost money?", "Founder access starts free. Optional paid tools and services will be tested in the pilot."),
          ("Do I have to raise investment?", "No. Many businesses grow from revenue; capital is one option among several."),
          ("Is it only for the UAE?", "It starts in the UAE, with an ambition to extend to other markets."),
          ("How is my data used?", "Consent first: founders control what is shared, and introductions need agreement from both sides."),
          ("How can I contribute?", "As a session lead, mentor, specialist, workstream contributor, connector or content contributor — in a role that suits your time."),
          ("How will longer-term roles be decided?", "Later, based on actual contribution, time commitment, responsibility taken, reliable delivery and value created."),
          ("How can I get involved?", "Visit startuproof.com to express interest as a founder, mentor, partner, investor or contributor.")]
    items = "".join(f'<div class="rule" style="padding:2.5mm 0"><h3>{q}</h3><p class="small" style="margin:0">{a}</p></div>' for q, a in qa)
    return page(f'''
  <div class="eyebrow">Frequently asked questions</div>
  <h1>Short answers to common questions.</h1>
  <div class="grid2" style="gap:0 7mm">{items}</div>''')


def p_glossary_sources():
    g = [("Accelerator", "A time-bound programme supporting startups, often with investment."), ("Angel investor", "An individual investing personal money in early startups."),
         ("Bootstrapping", "Funding a business from savings and revenue."), ("CAC", "Cost of acquiring one new customer."), ("Churn", "The rate at which customers stop buying."),
         ("Dilution", "Owning a smaller share after new shares are issued."), ("Free zone", "A UAE economic zone with its own licensing rules."), ("GTM", "Go-to-market: how a product reaches customers."),
         ("Incubator", "Support for very early ventures, often with space and mentoring."), ("LTV", "Gross profit expected from a customer over time."), ("MVP", "Minimum viable product — the simplest sellable version."),
         ("Pre-seed / Seed", "Early funding rounds to build and find product–market fit."), ("Product–market fit", "Strong, repeat demand from a clear market."), ("Runway", "Months a business can operate on current cash."),
         ("Unit economics", "Revenue and cost per unit, customer or order."), ("Venture capital", "Professional funds investing in high-growth companies.")]
    gl = "".join(f'<div style="display:grid;grid-template-columns:30mm 1fr;gap:2mm;padding:1.3mm 0;border-bottom:1px solid #E6EEF9"><b style="color:{BLUE};font-size:9.5pt">{t}</b><span class="small">{d}</span></div>' for t, d in g)
    src = ["CB Insights, “The Top 12 Reasons Startups Fail” (2021).", "US Bureau of Labor Statistics, Business Employment Dynamics; “The Economics Daily” (2024).",
           "Calvino, Criscuolo &amp; Menon (2015), “Cross-country evidence on start-up dynamics”, OECD.", "Endeavor Insight (2015) NYC founder research; “The Power of Entrepreneur Networks”.",
           "Hallen, Cohen &amp; Bingham (2020), “Do Accelerators Work? If So, How?”, Organization Science.", "Wamda, annual MENA startup investment reviews, 2020–2025.",
           "Global Entrepreneurship Monitor 2025/2026 Global Report and UAE country profile (2025).", "UAE Ministry of Economy; Central Bank of the UAE; Minister of Economy (2023).",
           "Dubai Media Office, Dubai Economic Agenda D33 (2023).", "Startup Genome, Global Startup Ecosystem Report 2025.",
           "OECD (2025), “Generative AI and the SME Workforce”; US Census Bureau, BTOS."]
    sl = "".join(f'<li>{s}</li>' for s in src)
    return page(f'''
  <div class="eyebrow">Glossary and sources</div>
  <h1>Startup terms, explained.</h1>
  <div class="grid2" style="gap:0 7mm">
    <div>{"".join(f'<div style="display:grid;grid-template-columns:30mm 1fr;gap:2mm;padding:1.3mm 0;border-bottom:1px solid #E6EEF9"><b style="color:{BLUE};font-size:9.5pt">{t}</b><span class="small">{d}</span></div>' for t, d in g[:8])}</div>
    <div>{"".join(f'<div style="display:grid;grid-template-columns:30mm 1fr;gap:2mm;padding:1.3mm 0;border-bottom:1px solid #E6EEF9"><b style="color:{BLUE};font-size:9.5pt">{t}</b><span class="small">{d}</span></div>' for t, d in g[8:])}</div>
  </div>
  <div class="rule" style="margin-top:6mm">
    <h2>Sources for external data</h2>
    <ol class="small" style="padding-left:5mm;margin-top:2mm;line-height:1.5">{sl}</ol>
    <p class="small muted" style="margin-top:2mm">Figures are reported as published by each source and year. Startup Roof’s own targets are ambitions, not results.</p>
  </div>''')
