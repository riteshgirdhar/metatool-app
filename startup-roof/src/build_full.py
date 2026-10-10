"""Builds the full edition: Startup_Roof_Full_Presentation.pptx (all chapters, charts, infographics, notes)."""
import sys
from pathlib import Path

import pptx_kit as kit
import build_deck as bd
import full_a as A
import full_b as Bm
import full_data as D

kit.MODE["auto"] = True
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "Startup_Roof_Full_Presentation.pptx")
bd.prs = kit.new_prs()


def chapter(n, items):
    t, sub = A.CHAPTERS[n - 1]
    def _f():
        s = kit.divider(bd.prs, n, t, sub, items)
        kit.notes(s, f"Chapter {n}: {t}. {sub}.")
    return _f


ORDER = [
    bd.s_cover, A.s_glance, A.s_contents,
    chapter(1, ["The founder experience today", "Why startups struggle", "The survival challenge", "Evidence that support helps", "Regional momentum and the UAE", "AI in small businesses"]),
    bd.s_problem, D.s_why_fail, D.s_survival, D.s_support_evidence, D.s_mena_funding, D.s_uae_context, D.s_uae_founders, D.s_ai_adoption, A.s_gap,
    chapter(2, ["What Startup Roof is", "Build · Learn · Connect · Grow", "Audiences and sectors", "Founder personas", "How value flows", "The four-layer model"]),
    bd.s_what, A.s_pillars, bd.s_who, A.s_sectors, A.s_personas, A.s_value_exchange, bd.s_layers, Bm.s_photo_dubai,
    chapter(3, ["Six stages at a glance", "Stage-by-stage checklists", "Startup metrics explained", "Funding options compared", "How funding stages work"]),
    bd.s_journey, A.s_stage_1, A.s_stage_2, A.s_stage_3, A.s_metrics, A.s_funding_options, A.s_funding_ladder,
    chapter(4, ["The digital workspace", "Onboarding and the next-step engine", "An illustrative scenario", "People, opportunities and services", "Architecture and trust", "What to build first"]),
    bd.s_founder_os, A.s_os_onboarding, A.s_os_engine, bd.s_scenario, A.s_os_matching, A.s_os_opps, A.s_os_services, A.s_os_progress,
    A.s_os_architecture, A.s_trust, A.s_os_mvp,
    chapter(5, ["AI with human support", "Community and a year-round rhythm", "Mentoring", "Founder Academy", "Expert services", "Insights, incubation and readiness"]),
    Bm.s_photo_community, bd.s_ai_human, bd.s_community, Bm.s_rhythm, Bm.s_mentor_model, Bm.s_photo_learning, bd.s_academy, Bm.s_curriculum,
    bd.s_services, Bm.s_catalogue, bd.s_insights, bd.s_incubation, Bm.s_readiness,
    chapter(6, ["Investors", "Ecosystem partners", "Universities and incubators", "Corporates and service providers"]),
    bd.s_investors, bd.s_partners, Bm.s_universities, Bm.s_corporates,
    chapter(7, ["Commercial model", "Revenue hypotheses by phase", "Service economics", "Pilot design and measurement", "Roadmap and milestones", "Risks"]),
    bd.s_commercial, Bm.s_revenue_matrix, Bm.s_unit_econ, Bm.s_pilot, Bm.s_kpis, bd.s_roadmap, Bm.s_growth_path, Bm.s_risks,
    chapter(8, ["Capabilities", "Ways to contribute", "FAQ and glossary", "Sources", "Invitation to participate"]),
    bd.s_people, Bm.s_contribution, Bm.s_faq, Bm.s_glossary, D.s_sources, bd.s_invitation,
]

for fn in ORDER:
    fn()
bd.prs.save(OUT)
print("saved", OUT, len(bd.prs.slides._sldIdLst), "slides; photos used:", kit.PHOTOS_USED or "none")
