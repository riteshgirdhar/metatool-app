/**
 * Single source of truth for commercial facts, feature status and navigation.
 * Edit this file (not individual pages) to change prices, dates, zone counts or Live/Beta/Planned/Demo labels.
 * Anything not yet approved by Startup Roof stays `null` and renders as "pending".
 */

export type Status = 'live' | 'beta' | 'planned' | 'demo' | 'pending';

export const SITE = {
  name: 'Startup Roof',
  tagline: 'Everything a founder needs to build, connect, raise and scale — under one roof.',
  description:
    'Startup Roof is a year-round ecosystem for founders, investors, mentors and partners: Founder OS, directories, Radar startup news, Academy, Toolkit and Founder Festival.',
  /** The replacement stays noindex until the domain migration is approved. Flip via env SITE_INDEXABLE=true. */
  indexable: import.meta.env.SITE_INDEXABLE === 'true',
  /** Canonical origin used for canonical/OG URLs. Keep startuproof.com so canonicals survive migration. */
  canonicalOrigin: 'https://startuproof.com',
  locale: 'en_GB',
  supportEmail: null as string | null, // inbox not confirmed — forms are the contact channel
} as const;

export const FEATURES: Record<string, { label: string; status: Status; note: string }> = {
  founderOs: { label: 'Founder OS', status: 'beta', note: 'Early access for registered founders.' },
  directories: { label: 'Startup, investor & mentor directories', status: 'beta', note: 'Profiles shown today are clearly labelled demo profiles while verified members are onboarded.' },
  radar: { label: 'Radar', status: 'beta', note: 'Editor-reviewed summaries with source links. Coverage is selective, not exhaustive.' },
  tv: { label: 'Startup Roof TV', status: 'planned', note: 'No licensed episodes are published yet.' },
  academy: { label: 'Academy', status: 'beta', note: 'Nine tracks; guides are being published progressively.' },
  toolkit: { label: 'Toolkit', status: 'live', note: 'Free downloadable templates.' },
  community: { label: 'Community', status: 'planned', note: 'Member community launches after directory verification.' },
  marketplace: { label: 'Marketplace', status: 'planned', note: 'Provider applications open; no providers are listed yet.' },
  referrals: { label: 'Referrals', status: 'beta', note: 'Referral links are tracked; reward terms are not yet approved.' },
  festival: { label: 'Founder Festival', status: 'planned', note: 'Dates provisional, venue not announced.' },
  accelerator: { label: 'Accelerator', status: 'planned', note: 'Programme design in progress; register interest.' },
  incubator: { label: 'Incubator', status: 'planned', note: 'Programme design in progress; register interest.' },
  pricing: { label: 'Paid plans', status: 'pending', note: 'Prices and payment are not active. Membership is free.' },
};

/** Prices are deliberately null until approved. Never render a number that is not set here. */
export const PRICING = {
  currency: 'AED',
  paymentsActive: false,
  plans: [
    { id: 'member', name: 'Member', price: 0 as number | null, period: null as string | null, status: 'live' as Status,
      summary: 'Free account: Radar alerts, Academy, Toolkit downloads, directory browsing and applications.' },
    { id: 'founder-pro', name: 'Founder Pro', price: null, period: 'month', status: 'pending' as Status,
      summary: 'Founder OS workspace, investor-readiness reviews and priority introductions.' },
    { id: 'investor', name: 'Investor Access', price: null, period: 'year', status: 'pending' as Status,
      summary: 'Verified-investor deal flow, startup data rooms and Capital Night invitations.' },
    { id: 'partner', name: 'Partner & Sponsor', price: null, period: null, status: 'pending' as Status,
      summary: 'Programme partnerships, sponsorship and Festival packages — quoted individually.' },
  ],
};

/** Founder Festival facts. Dates come from the Startup Roof events table and are marked provisional. */
export const FESTIVAL = {
  name: 'Founder Festival Dubai 2027',
  city: 'Dubai',
  dates: { start: '2027-03-26', end: '2027-03-28', status: 'provisional' as 'provisional' | 'confirmed' },
  venue: null as string | null,
  zones: null as number | null, // conflicting counts on the old site — pending confirmation
  ticketPrices: null as null | Record<string, number>,
  structure: ['Discover + Connect', 'Build + Raise', 'Scale + Celebrate'],
  capitalNight: { date: '2027-03-25', status: 'provisional' as const, note: 'Invitation-only evening for investors and selected founders.' },
};

export interface NavLink { label: string; href: string; description?: string }
export interface NavGroup { id: string; label: string; links: NavLink[] }

export const NAV: NavGroup[] = [
  {
    id: 'platform', label: 'Platform', links: [
      { label: 'Founder OS', href: '/founder-os/', description: 'Your startup workspace and readiness plan' },
      { label: 'Startups', href: '/startups/', description: 'Directory of member startups' },
      { label: 'Investors', href: '/investors/', description: 'Angels, VCs and family offices' },
      { label: 'Mentors', href: '/mentors/', description: 'Operators who give office hours' },
      { label: 'Opportunities', href: '/opportunities/', description: 'Calls, grants and programmes' },
      { label: 'Marketplace', href: '/marketplace/', description: 'Vetted service providers' },
      { label: 'Pricing', href: '/pricing/', description: 'Membership and plans' },
    ],
  },
  {
    id: 'programmes', label: 'Programmes', links: [
      { label: 'Accelerator', href: '/accelerator/', description: 'Structured programme for funded teams' },
      { label: 'Incubator', href: '/incubator/', description: 'From idea to first customers' },
      { label: 'Partners', href: '/partners/', description: 'Universities, corporates and government' },
      { label: 'Referrals', href: '/referrals/', description: 'Invite founders and track referrals' },
    ],
  },
  {
    id: 'festival', label: 'Festival', links: [
      { label: 'Founder Festival', href: '/festival/', description: 'Planning status and how to take part' },
      { label: 'Pitch', href: '/pitch/', description: 'Apply to pitch' },
      { label: 'Exhibitors', href: '/exhibitors/', description: 'Startup Market stands' },
      { label: 'Sponsors', href: '/sponsors/', description: 'Sponsorship enquiries' },
    ],
  },
  {
    id: 'resources', label: 'Resources', links: [
      { label: 'Academy', href: '/academy/', description: 'Nine founder learning tracks' },
      { label: 'Toolkit', href: '/toolkit/', description: 'Free templates and downloads' },
      { label: 'Stories', href: '/media/', description: 'Editorial from Startup Roof' },
      { label: 'Community', href: '/community/', description: 'Member groups and meetups' },
      { label: 'Help centre', href: '/support/', description: 'Answers and support requests' },
    ],
  },
];

/** Top-level single links shown between groups. */
export const NAV_DIRECT: NavLink[] = [
  { label: 'Radar', href: '/radar/' },
  { label: 'TV', href: '/tv/' },
];

export const FOOTER: { heading: string; links: NavLink[] }[] = [
  { heading: 'Platform', links: NAV[0].links },
  { heading: 'Discover', links: [
    { label: 'Radar', href: '/radar/' }, { label: 'Startup Roof TV', href: '/tv/' },
    { label: 'Academy', href: '/academy/' }, { label: 'Toolkit', href: '/toolkit/' }, { label: 'Stories', href: '/media/' },
  ] },
  { heading: 'Take part', links: [
    { label: 'Founder Festival', href: '/festival/' }, { label: 'Accelerator', href: '/accelerator/' },
    { label: 'Incubator', href: '/incubator/' }, { label: 'Partners', href: '/partners/' }, { label: 'Sponsors', href: '/sponsors/' },
  ] },
  { heading: 'Company', links: [
    { label: 'About', href: '/about/' }, { label: 'Contact', href: '/contact/' }, { label: 'Help centre', href: '/support/' },
    { label: 'FAQ', href: '/faq/' }, { label: 'Search', href: '/search/' },
  ] },
  { heading: 'Legal', links: [
    { label: 'Privacy', href: '/privacy/' }, { label: 'Terms', href: '/terms/' }, { label: 'Cookies', href: '/cookie/' },
    { label: 'Code of conduct', href: '/conduct/' }, { label: 'Acceptable use', href: '/acceptable-use/' },
    { label: 'Investment disclaimer', href: '/investment-disclaimer/' },
  ] },
];

export const STATUS_LABEL: Record<Status, string> = {
  live: 'Live', beta: 'Beta', planned: 'Planned', demo: 'Demo', pending: 'Pending',
};
