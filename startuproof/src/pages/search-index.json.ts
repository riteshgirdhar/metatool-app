import type { APIRoute } from 'astro';
import { RADAR, KINDS } from '../data/radar';
import { GUIDES, TRACKS, TOOLS, STORIES, OPPORTUNITIES, SHOWS } from '../data/content';
import { NAV, FOOTER } from '../config/site';

/** Public search index generated from the same content model the pages use. Demo profiles are excluded. */
export const GET: APIRoute = () => {
  const docs = [
    ...NAV.flatMap((g) => g.links.map((l) => ({ t: l.label, u: l.href, s: l.description ?? '', k: g.label }))),
    ...FOOTER.flatMap((c) => c.links).filter((l) => !NAV.some((g) => g.links.some((x) => x.href === l.href))).map((l) => ({ t: l.label, u: l.href, s: '', k: 'Page' })),
    ...RADAR.map((i) => ({ t: i.title, u: `/radar/item/${i.slug}/`, s: i.summary, k: `Radar · ${KINDS[i.kind]}` })),
    ...TRACKS.map((t) => ({ t: `Track ${t.number}: ${t.title}`, u: `/academy/${t.slug}/`, s: `${t.description} ${t.outcome}`, k: 'Academy track' })),
    ...GUIDES.map((g) => ({ t: g.title, u: `/academy/guides/${g.slug}/`, s: `${g.summary} ${g.body.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').slice(0, 600)}`, k: 'Academy guide' })),
    ...TOOLS.map((t) => ({ t: t.title, u: `/toolkit/${t.slug}/`, s: t.summary, k: `Toolkit · ${t.format}` })),
    ...STORIES.map((s) => ({ t: s.title, u: `/media/${s.slug}/`, s: s.summary, k: 'Story' })),
    ...OPPORTUNITIES.map((o) => ({ t: o.name, u: `/opportunities/${o.slug}/`, s: o.summary, k: 'Opportunity' })),
    ...SHOWS.map((s) => ({ t: s.title, u: `/tv/shows/${s.slug}/`, s: s.summary, k: 'TV (planned)' })),
  ];
  const seen = new Set<string>();
  return new Response(JSON.stringify(docs.filter((d) => (seen.has(d.u) ? false : (seen.add(d.u), true)))), { headers: { 'content-type': 'application/json' } });
};
