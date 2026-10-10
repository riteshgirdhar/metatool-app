/**
 * Fills member-only sections from /api/directory after verifying the session server-side.
 * Visitors see an explanation and a login link that returns them to this page.
 */
import { authConfigured, accessToken, loginUrl } from './auth-client';

type Row = Record<string, unknown>;
function el(tag: string, text?: string, cls?: string) { const e = document.createElement(tag); if (text) e.textContent = text; if (cls) e.className = cls; return e; }

function renderFacts(target: HTMLElement, pairs: [string, unknown][]) {
  const dl = el('dl', undefined, 'facts');
  for (const [k, v] of pairs) {
    if (v === undefined || v === null || v === '') continue;
    const d = el('div'); d.append(el('dt', k), el('dd', Array.isArray(v) ? v.join(', ') : typeof v === 'object' ? Object.entries(v as Row).map(([a, b]) => `${a}: ${b}`).join(' · ') : String(v)));
    dl.append(d);
  }
  target.replaceChildren(dl);
}

async function run() {
  const slots = Array.from(document.querySelectorAll<HTMLElement>('[data-member-slot]'));
  if (!slots.length) return;
  for (const s of slots) s.querySelectorAll<HTMLAnchorElement>('[data-login-link]').forEach((a) => (a.href = loginUrl(location.pathname, s.dataset.intent)));
  if (!authConfigured) return;
  const token = await accessToken().catch(() => null);
  if (!token) return;
  for (const slot of slots) {
    const { type, slug, mode } = slot.dataset;
    const body = slot.querySelector<HTMLElement>('[data-member-body]');
    if (!body) continue;
    body.replaceChildren(el('p', 'Loading member details…', 'small muted'));
    try {
      const res = await fetch(`/api/directory?type=${type}${slug ? `&slug=${slug}` : ''}`, { headers: { authorization: `Bearer ${token}` } });
      const data = await res.json();
      if (!res.ok) { body.replaceChildren(el('p', data?.message ?? 'Member details are unavailable right now.', 'small')); continue; }
      const items = data.items as Row[];
      if (mode === 'extra-investors') {
        const ul = el('ul', undefined, 'item-list');
        for (const i of items.filter((x) => x.name)) {
          const li = el('li'); li.append(el('h3', `${i.name}`), el('p', `${i.location} · ${(i.stages as string[]).join(', ')} · ${i.ticket}`), el('p', String(i.thesis)));
          const b = el('span', 'Demo profile', 'badge demo'); li.prepend(b); ul.append(li);
        }
        body.replaceChildren(ul);
        continue;
      }
      const row = items[0];
      if (!row) { body.replaceChildren(el('p', 'No member details for this profile.', 'small')); continue; }
      if (type === 'startups') {
        renderFacts(body, [['Traction', row.traction], ['Growth', row.growth], ['Customers', row.customers], ['Current round', row.currentRound], ['Competitors', row.competitors], ['Differentiator', row.usp], ['Expansion markets', row.expansion], ['Readiness (self-assessed)', row.readiness]]);
        const inv = row.investorOnly as Row | null;
        const p = el('p', inv ? `Investor-only: ${inv.financials}` : 'Financial information is limited to verified investors.', 'small notice');
        body.append(p);
      } else if (type === 'investors') {
        renderFacts(body, [['Typical cheque', row.ticket], ['Follow-on', row.followOn ? 'Yes' : 'No'], ['Portfolio', row.portfolio], ['Accepting introductions', row.acceptingIntros ? 'Yes' : 'No']]);
      } else {
        renderFacts(body, [['Availability', row.availability]]);
      }
    } catch {
      body.replaceChildren(el('p', 'We could not load member details. Check your connection and refresh.', 'small'));
    }
  }
}
void run();
