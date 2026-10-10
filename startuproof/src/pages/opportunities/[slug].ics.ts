import type { APIRoute } from 'astro';
import { OPPORTUNITIES, type Opportunity } from '../../data/content';
import { buildIcs } from '../../lib/ics';
export function getStaticPaths() {
  return OPPORTUNITIES.filter((o) => o.dateStatus === 'confirmed' && o.deadline).map((o) => ({ params: { slug: o.slug }, props: { o } }));
}
export const GET: APIRoute = ({ props }) => {
  const o = (props as { o: Opportunity }).o;
  const body = buildIcs({ uid: `${o.slug}-deadline@startuproof.com`, date: o.deadline!, summary: `Deadline: ${o.name}`, description: `${o.summary} Apply: https://startuproof.com${o.applyHref}`, url: `https://startuproof.com/opportunities/${o.slug}/` });
  return new Response(body, { headers: { 'content-type': 'text/calendar; charset=utf-8' } });
};
