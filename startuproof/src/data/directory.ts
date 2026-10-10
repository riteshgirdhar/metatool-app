/**
 * PUBLIC directory fields only. Member-only fields (traction, tickets, portfolio, availability) live in
 * netlify/functions/_data/directory-private.ts and are served only to signed-in members by /api/directory.
 * Every record below is a DEMO profile from the Startup Roof database (`is_demo = true`).
 * Demo profiles are labelled on every surface, never carry verification badges, and are excluded from sitemaps.
 */

export interface StartupPublic {
  slug: string; name: string; tagline: string; oneLiner: string; description: string; sector: string; stage: string;
  hq: string; country: string; markets: string[]; yearFounded: number; teamSize: number; businessModel: string; isDemo: true;
}
export interface InvestorPublic {
  slug: string; name: string; type: 'vc' | 'angel' | 'family_office' | 'cvc'; location: string; geographies: string[];
  sectors: string[]; stages: string[]; thesis: string; isDemo: true;
}
export interface MentorPublic {
  slug: string; name: string; title: string; company: string; location: string; expertise: string[]; sectors: string[]; bio: string; isDemo: true;
}

const strip = (s: string) => s.replace(/^DEMO (company|fund|family office|angel|CVC|mentor)\.\s*/i, '');

export const STARTUPS: StartupPublic[] = [
  { slug: 'nimbus-ledger', name: 'Nimbus Ledger', tagline: 'Real-time cash intelligence for GCC SMEs', oneLiner: 'AI bookkeeping that closes the month in a day, not a fortnight.', description: strip('DEMO company. Nimbus Ledger connects to UAE bank feeds and VAT systems to automate reconciliation for 10–200 person companies.'), sector: 'Fintech', stage: 'Seed', hq: 'Dubai, UAE', country: 'UAE', markets: ['UAE', 'KSA', 'Qatar'], yearFounded: 2024, teamSize: 9, businessModel: 'B2B SaaS', isDemo: true },
  { slug: 'saffron-health', name: 'Saffron Health', tagline: 'Clinic operations, reimagined', oneLiner: 'Workflow automation for outpatient clinics across the Gulf.', description: strip('DEMO company. Saffron Health replaces whiteboards and WhatsApp with a single queue, scheduling and insurance pre-approval layer.'), sector: 'HealthTech', stage: 'Series A', hq: 'Abu Dhabi, UAE', country: 'UAE', markets: ['UAE', 'KSA'], yearFounded: 2022, teamSize: 34, businessModel: 'B2B SaaS', isDemo: true },
  { slug: 'dune-robotics', name: 'Dune Robotics', tagline: 'Autonomous inspection for desert infrastructure', oneLiner: 'Drones and edge AI that inspect solar farms and pipelines in extreme heat.', description: strip('DEMO company. Dune Robotics builds heat-hardened autonomous drones for utility-scale solar and oil & gas inspection.'), sector: 'Hardware & Robotics', stage: 'Pre-seed', hq: 'Dubai, UAE', country: 'UAE', markets: ['UAE', 'KSA'], yearFounded: 2025, teamSize: 5, businessModel: 'Hardware + SaaS', isDemo: true },
  { slug: 'majlis-learn', name: 'Majlis Learn', tagline: 'Arabic-first upskilling', oneLiner: 'Bite-sized career courses in Arabic with AI tutors.', description: strip('DEMO company. Majlis Learn offers Arabic-language micro-courses in data, sales and product with an AI tutor that speaks Gulf, Levantine and Egyptian dialects.'), sector: 'EdTech', stage: 'Seed', hq: 'Riyadh, KSA', country: 'Saudi Arabia', markets: ['KSA', 'UAE', 'Egypt'], yearFounded: 2023, teamSize: 14, businessModel: 'B2C + B2B2C', isDemo: true },
  { slug: 'portside', name: 'Portside', tagline: 'Freight booking that actually confirms', oneLiner: 'Instant-quote LCL freight marketplace for Jebel Ali exporters.', description: strip('DEMO company. Portside gives SME exporters instant, bookable LCL quotes with live container tracking and customs paperwork.'), sector: 'Logistics & Mobility', stage: 'Seed', hq: 'Dubai, UAE', country: 'UAE', markets: ['UAE', 'India', 'KSA'], yearFounded: 2023, teamSize: 19, businessModel: 'Marketplace', isDemo: true },
  { slug: 'verdant-grid', name: 'Verdant Grid', tagline: 'Rooftop solar for every warehouse', oneLiner: 'Financing and software that make industrial rooftop solar straightforward.', description: strip('DEMO company. Verdant Grid originates, finances and monitors rooftop solar for logistics parks across the GCC.'), sector: 'Climate & Energy', stage: 'Series A', hq: 'Dubai, UAE', country: 'UAE', markets: ['UAE', 'KSA', 'Oman'], yearFounded: 2021, teamSize: 41, businessModel: 'Project finance + SaaS', isDemo: true },
  { slug: 'kahwa-club', name: 'Kahwa Club', tagline: 'Specialty coffee subscriptions, roasted in Dubai', oneLiner: 'D2C coffee with roast-to-door in 48 hours.', description: strip('DEMO company. Kahwa Club roasts weekly and ships across the GCC with a loyalty app and an office-supply tier.'), sector: 'E-commerce & Retail', stage: 'Pre-seed', hq: 'Dubai, UAE', country: 'UAE', markets: ['UAE'], yearFounded: 2025, teamSize: 4, businessModel: 'D2C subscription', isDemo: true },
  { slug: 'falcon-stack', name: 'Falcon Stack', tagline: 'Compliance automation for DIFC & ADGM fintechs', oneLiner: 'Policy-as-code that keeps licensed fintechs audit-ready.', description: strip('DEMO company. Falcon Stack maps DFSA and FSRA rulebooks into automated controls, evidence collection and board reporting.'), sector: 'Cybersecurity', stage: 'Seed', hq: 'Dubai, UAE', country: 'UAE', markets: ['UAE', 'UK', 'Singapore'], yearFounded: 2024, teamSize: 11, businessModel: 'B2B SaaS', isDemo: true },
];

/** Only investors whose stored visibility is `public`. Members-only investors are served by the API after sign-in. */
export const INVESTORS: InvestorPublic[] = [
  { slug: 'gulf-horizon-ventures', name: 'Gulf Horizon Ventures', type: 'vc', location: 'Dubai, UAE', geographies: ['UAE', 'KSA', 'Egypt'], sectors: ['Fintech', 'SaaS & Enterprise', 'Logistics & Mobility'], stages: ['Seed', 'Series A'], thesis: strip('DEMO fund. Backs B2B software founders solving Gulf-specific operational problems with regional-to-global ambition.'), isDemo: true },
  { slug: 'riyadh-seed-partners', name: 'Riyadh Seed Partners', type: 'vc', location: 'Riyadh, KSA', geographies: ['KSA', 'UAE', 'Bahrain'], sectors: ['EdTech', 'SaaS & Enterprise', 'AI & Machine Learning'], stages: ['Pre-seed', 'Seed'], thesis: strip('DEMO fund. Pre-seed and seed in Saudi-first products with Vision 2030 tailwinds.'), isDemo: true },
  { slug: 'meridian-growth-capital', name: 'Meridian Growth Capital', type: 'vc', location: 'London, UK', geographies: ['UK', 'UAE', 'Singapore', 'India'], sectors: ['Fintech', 'Cybersecurity', 'SaaS & Enterprise'], stages: ['Series A', 'Series B'], thesis: strip('DEMO fund. Series A/B in regulated-industry software with global expansion potential; active in DIFC.'), isDemo: true },
  { slug: 'palm-street-capital', name: 'Palm Street Capital', type: 'vc', location: 'Dubai, UAE', geographies: ['UAE', 'KSA', 'Global'], sectors: ['PropTech', 'Fintech', 'Travel & Hospitality'], stages: ['Seed', 'Series A'], thesis: strip('DEMO fund. Thesis-driven investments in real estate, hospitality and payments software born in the GCC.'), isDemo: true },
];
export const MEMBERS_ONLY_INVESTOR_COUNT = 4;

export const MENTORS: MentorPublic[] = [
  { slug: 'layla-haddad', name: 'Layla Haddad', title: 'Former VP Sales', company: 'Example SaaS company', location: 'Dubai, UAE', expertise: ['Enterprise sales', 'GCC go-to-market', 'Pricing'], sectors: ['SaaS & Enterprise', 'Fintech'], bio: 'Built a sales organisation from zero across the GCC.', isDemo: true },
  { slug: 'omar-farouk', name: 'Omar Farouk', title: 'CFO-in-residence', company: 'Example accelerator', location: 'Abu Dhabi, UAE', expertise: ['Financial modelling', 'Fundraising', 'Unit economics'], sectors: ['Fintech', 'Climate & Energy'], bio: 'Investment banker turned startup CFO.', isDemo: true },
  { slug: 'priya-nair', name: 'Priya Nair', title: 'Head of Product', company: 'Example marketplace', location: 'Dubai, UAE', expertise: ['Product-market fit', 'Growth loops', 'Marketplaces'], sectors: ['Marketplaces', 'Consumer Apps', 'E-commerce & Retail'], bio: 'Led product for a two-sided marketplace through rapid growth.', isDemo: true },
  { slug: 'daniel-osei', name: 'Daniel Osei', title: 'Founder & angel', company: 'Example security company', location: 'London, UK', expertise: ['Hiring', 'Leadership', 'International expansion'], sectors: ['SaaS & Enterprise', 'Cybersecurity'], bio: 'Founded a B2B security company; advises on scaling teams.', isDemo: true },
  { slug: 'noura-al-mansoori', name: 'Noura Al Mansoori', title: 'Ecosystem lead', company: 'Example government programme', location: 'Dubai, UAE', expertise: ['Government programmes', 'Grants', 'Market entry'], sectors: ['Climate & Energy', 'HealthTech', 'EdTech'], bio: 'Guides founders through licensing, grants and public-sector pilots.', isDemo: true },
  { slug: 'arjun-mehta', name: 'Arjun Mehta', title: 'Growth adviser', company: 'Example D2C brand', location: 'Dubai, UAE', expertise: ['Performance marketing', 'Brand', 'Retention'], sectors: ['E-commerce & Retail', 'Consumer Apps', 'FoodTech & AgriTech'], bio: 'Scaled a D2C brand with disciplined acquisition spend.', isDemo: true },
];

export const INVESTOR_TYPE: Record<InvestorPublic['type'], string> = { vc: 'Venture capital', angel: 'Angel', family_office: 'Family office', cvc: 'Corporate VC' };
export const initials = (n: string) => n.split(/\s+/).map((p) => p[0]).slice(0, 2).join('').toUpperCase();
