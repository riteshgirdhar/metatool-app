/**
 * Member-only and verified-investor-only directory fields. Server-side only: imported by Netlify Functions,
 * never by Astro pages, so these values are not present in the static build output (checked by tests/unit/leak.test.mjs).
 * All rows are DEMO records from the Startup Roof database.
 */
export const PRIVATE_STARTUPS = [
  { slug: 'nimbus-ledger', traction: '320 paying SMEs (demo figure)', growth: '18% MoM (demo)', customers: '320 customers', competitors: 'Zoho Books, Xero, Wafeq', usp: 'Native integration with UAE VAT and WPS payroll rails.', expansion: ['KSA', 'Egypt'], currentRound: 'Seed', readiness: { product: 68, traction: 64, team: 70, fundraising: 58 }, investorOnly: { financials: 'No financials uploaded (demo profile).' } },
  { slug: 'saffron-health', traction: '140 clinics (demo figure)', growth: '9% MoM (demo)', customers: '140 clinics', competitors: 'Okadoc, Vezeeta', usp: 'Insurance pre-approval engine.', expansion: ['KSA', 'Oman', 'Bahrain'], currentRound: 'Series A', readiness: { product: 82, traction: 78, team: 76, fundraising: 70 }, investorOnly: { financials: 'No financials uploaded (demo profile).' } },
  { slug: 'dune-robotics', traction: '2 paid pilots (demo figure)', growth: '—', customers: '2 pilot customers', competitors: 'Percepto, Skydio', usp: 'Heat-hardened inspection platform.', expansion: ['KSA', 'Australia'], currentRound: 'Pre-seed', readiness: { product: 55, traction: 30, team: 62, fundraising: 40 }, investorOnly: { financials: 'No financials uploaded (demo profile).' } },
  { slug: 'majlis-learn', traction: '48k monthly learners (demo figure)', growth: '12% MoM (demo)', customers: '48,000 MAU', competitors: 'Coursera, Rwaq, Edraak', usp: 'Dialect-aware AI tutor.', expansion: ['Egypt', 'Morocco'], currentRound: 'Seed', readiness: { product: 70, traction: 62, team: 68, fundraising: 55 }, investorOnly: { financials: 'No financials uploaded (demo profile).' } },
  { slug: 'portside', traction: '$14M annualised GMV (demo figure)', growth: '15% MoM (demo)', customers: '900 shippers', competitors: 'Freightos, Flexport', usp: 'Confirmed bookings in under 60 seconds.', expansion: ['India', 'Kenya'], currentRound: 'Seed+', readiness: { product: 65, traction: 68, team: 66, fundraising: 60 }, investorOnly: { financials: 'No financials uploaded (demo profile).' } },
  { slug: 'verdant-grid', traction: '62 MW installed (demo figure)', growth: '6% MoM (demo)', customers: '85 sites', competitors: 'Yellow Door Energy, Emerge', usp: 'Vertically integrated origination, finance and monitoring.', expansion: ['KSA', 'Egypt', 'India'], currentRound: 'Series B', readiness: { product: 76, traction: 82, team: 80, fundraising: 72 }, investorOnly: { financials: 'No financials uploaded (demo profile).' } },
  { slug: 'kahwa-club', traction: '1,800 subscribers (demo figure)', growth: '22% MoM (demo)', customers: '1,800 subscribers', competitors: 'Nightjar, Boon Coffee', usp: '48-hour roast-to-door.', expansion: ['KSA', 'Kuwait'], currentRound: 'Pre-seed', readiness: { product: 60, traction: 55, team: 45, fundraising: 42 }, investorOnly: { financials: 'No financials uploaded (demo profile).' } },
  { slug: 'falcon-stack', traction: '21 licensed fintech customers (demo figure)', growth: '11% MoM (demo)', customers: '21 customers', competitors: 'Vanta, Drata', usp: 'DFSA and FSRA rulebook coverage.', expansion: ['UK', 'Singapore'], currentRound: 'Seed', readiness: { product: 66, traction: 58, team: 72, fundraising: 60 }, investorOnly: { financials: 'No financials uploaded (demo profile).' } },
];

export const PRIVATE_INVESTORS = [
  { slug: 'gulf-horizon-ventures', ticket: 'USD 500k – 3M (demo)', followOn: true, portfolio: ['Demo portfolio company A', 'Demo portfolio company B'], acceptingIntros: true },
  { slug: 'riyadh-seed-partners', ticket: 'USD 250k – 1.5M (demo)', followOn: true, portfolio: ['Demo portfolio company D'], acceptingIntros: true },
  { slug: 'meridian-growth-capital', ticket: 'USD 3M – 20M (demo)', followOn: true, portfolio: ['Demo portfolio company F', 'Demo portfolio company G'], acceptingIntros: true },
  { slug: 'palm-street-capital', ticket: 'USD 750k – 4M (demo)', followOn: true, portfolio: ['Demo portfolio company H'], acceptingIntros: true },
];

/** Investors whose visibility is `members`: not in the public build at all. */
export const MEMBERS_ONLY_INVESTORS = [
  { slug: 'al-noor-family-office', name: 'Al Noor Family Office', type: 'family_office', location: 'Abu Dhabi, UAE', sectors: ['Climate & Energy', 'HealthTech', 'PropTech'], stages: ['Series A', 'Series B', 'Growth'], ticket: 'USD 2M – 15M (demo)', thesis: 'Long-horizon capital for infrastructure-adjacent technology.', isDemo: true },
  { slug: 'sana-qureshi', name: 'Sana Qureshi', type: 'angel', location: 'Dubai, UAE', sectors: ['Fintech', 'E-commerce & Retail', 'Consumer Apps'], stages: ['Pre-seed', 'Seed'], ticket: 'USD 25k – 150k (demo)', thesis: 'Former payments operator; first cheques for founders with proprietary distribution.', isDemo: true },
  { slug: 'oryx-corporate-ventures', name: 'Oryx Corporate Ventures', type: 'cvc', location: 'Doha, Qatar', sectors: ['Logistics & Mobility', 'Climate & Energy', 'Hardware & Robotics'], stages: ['Seed', 'Series A'], ticket: 'USD 1M – 5M (demo)', thesis: 'Strategic investments where a pilot with the parent group accelerates traction.', isDemo: true },
  { slug: 'karim-el-sayed', name: 'Karim El-Sayed', type: 'angel', location: 'Cairo, Egypt', sectors: ['EdTech', 'Media & Creator Economy', 'Consumer Apps'], stages: ['Pre-seed', 'Seed'], ticket: 'USD 15k – 100k (demo)', thesis: 'Backs Arabic-first consumer products with strong retention.', isDemo: true },
];

export const PRIVATE_MENTORS = [
  { slug: 'layla-haddad', availability: '2 office hours / month (demo)' },
  { slug: 'omar-farouk', availability: 'Fortnightly (demo)' },
  { slug: 'priya-nair', availability: 'Monthly (demo)' },
  { slug: 'daniel-osei', availability: 'Ad hoc (demo)' },
  { slug: 'noura-al-mansoori', availability: 'Weekly (demo)' },
  { slug: 'arjun-mehta', availability: 'Monthly (demo)' },
];
