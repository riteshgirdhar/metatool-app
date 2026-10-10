import { readdirSync, statSync } from 'node:fs';
import { join, relative } from 'node:path';

/** Every HTML route in the production build (dist/), derived from the files actually built. */
export function builtRoutes(dist = join(process.cwd(), 'dist')): string[] {
  const out: string[] = [];
  const walk = (d: string) => {
    for (const f of readdirSync(d)) {
      const p = join(d, f);
      if (statSync(p).isDirectory()) walk(p);
      else if (f === 'index.html') out.push(`/${relative(dist, p).replace(/index\.html$/, '')}`);
    }
  };
  walk(dist);
  return out.sort();
}

/** One representative URL per template, used for screenshots, axe and viewport checks. */
export const TEMPLATES: Record<string, string> = {
  home: '/', 'founder-os': '/founder-os/', 'radar-index': '/radar/', 'radar-edition': '/radar/uae/', 'radar-item': '/radar/item/maven-robotics-100m-series-a-shorooq-presight/',
  'radar-submit': '/radar/submit/', startups: '/startups/', 'startup-detail': '/startups/nimbus-ledger/', investors: '/investors/', 'investor-detail': '/investors/gulf-horizon-ventures/',
  mentors: '/mentors/', 'mentor-detail': '/mentors/omar-farouk/', opportunities: '/opportunities/', 'opportunity-detail': '/opportunities/founder-festival-pitch-studio-2027/',
  academy: '/academy/', 'academy-track': '/academy/fundraising-readiness/', 'academy-guide': '/academy/guides/unit-economics-basics/', toolkit: '/toolkit/', 'toolkit-item': '/toolkit/investor-pipeline-tracker/',
  stories: '/media/', story: '/media/radar-editorial-standards/', tv: '/tv/', 'tv-show': '/tv/shows/the-raise/', 'tv-episode': '/tv/shows/the-raise/e2-first-meetings/', 'tv-category': '/tv/category/raise/',
  'tv-learning': '/tv/learning/', 'tv-live': '/tv/live/', festival: '/festival/', pitch: '/pitch/', exhibitors: '/exhibitors/', sponsors: '/sponsors/', partners: '/partners/',
  accelerator: '/accelerator/', incubator: '/incubator/', community: '/community/', marketplace: '/marketplace/', referrals: '/referrals/', pricing: '/pricing/',
  about: '/about/', contact: '/contact/', support: '/support/', faq: '/faq/', search: '/search/?q=series', privacy: '/privacy/', terms: '/terms/', cookie: '/cookie/',
  conduct: '/conduct/', 'acceptable-use': '/acceptable-use/', 'investment-disclaimer': '/investment-disclaimer/',
  signup: '/signup/', login: '/login/', forgot: '/forgot/', reset: '/reset/', app: '/app/', onboarding: '/app/onboarding/', 'not-found': '/this-page-does-not-exist/',
};
