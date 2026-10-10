/**
 * Member area. The session comes from Supabase Auth; anything that grants access (investor verification,
 * referral records) is fetched from server functions that re-verify the token. Nothing here is trusted for authorization.
 */
import { authConfigured, getClient, loginUrl } from './auth-client';

const root = document.querySelector<HTMLElement>('[data-app]');
const view = root?.dataset.app;
const $ = <T extends HTMLElement>(s: string) => document.querySelector<T>(s);
function text(sel: string, v: string) { const e = $(sel); if (e) e.textContent = v; }
function show(sel: string, on = true) { const e = $(sel); if (e) e.hidden = !on; }

async function api(path: string, token: string, init: RequestInit = {}) {
  const res = await fetch(path, { ...init, headers: { ...(init.headers ?? {}), authorization: `Bearer ${token}`, 'content-type': 'application/json' } });
  const body = await res.json().catch(() => ({}));
  if (res.status === 401) { location.assign(`${loginUrl(location.pathname)}&reason=expired`); throw new Error('expired'); }
  return { ok: res.ok, status: res.status, body };
}

async function main() {
  if (!authConfigured) { show('[data-app-loading]', false); show('[data-app-unavailable]'); return; }
  const sb = await getClient();
  const { data } = await sb.auth.getSession();
  const session = data.session;
  if (!session) { location.replace(loginUrl(location.pathname + location.hash)); return; }
  const user = session.user;
  const meta = (user.user_metadata ?? {}) as Record<string, any>;
  show('[data-app-loading]', false); show('[data-app-ready]');

  $('[data-logout]')?.addEventListener('click', async () => {
    await sb.auth.signOut().catch(() => null);
    location.assign('/login/?reason=logged-out');
  });

  if (view === 'home') {
    text('[data-name]', meta.full_name ?? user.email ?? 'there');
    text('[data-email]', user.email ?? '');
    text('[data-requested-role]', meta.requested_role ?? 'founder');
    show('[data-onboarding-todo]', !meta.onboarding_complete);
    // Server truth for investor status.
    const me = await api('/api/me', session.access_token).catch(() => null);
    if (me?.ok) text('[data-investor-status]', me.body.user.investorVerified ? 'Verified investor' : meta.requested_role === 'investor' ? 'Not yet verified — apply below' : 'Not applicable');
    else text('[data-investor-status]', me?.body?.message ?? 'Unavailable right now');
    // Referral attribution (once) and summary.
    if (meta.ref_code) await api('/api/referrals?action=attribute', session.access_token, { method: 'POST', body: JSON.stringify({ code: meta.ref_code }) }).catch(() => null);
    const ref = await api('/api/referrals?action=summary', session.access_token).catch(() => null);
    if (ref?.ok) {
      const link = `${location.origin}/signup/?ref=${ref.body.code}`;
      const input = $<HTMLInputElement>('[data-ref-link]'); if (input) input.value = link;
      text('[data-ref-counts]', `${ref.body.referred} referred · ${ref.body.qualified} qualified. Reward terms are not yet approved.`);
    } else text('[data-ref-counts]', ref?.body?.message ?? 'Referral details are unavailable right now.');
    $('[data-copy-ref]')?.addEventListener('click', async () => {
      const v = $<HTMLInputElement>('[data-ref-link]')?.value ?? '';
      try { await navigator.clipboard.writeText(v); text('[data-copy-status]', 'Copied.'); } catch { text('[data-copy-status]', 'Select the link and copy it.'); }
    });
    // Saved Radar items (device-only).
    let saved: string[] = []; try { saved = JSON.parse(localStorage.getItem('sr-radar-saved') ?? '[]'); } catch { /* ignore */ }
    const ul = $('[data-saved]');
    if (ul && saved.length) {
      const idx = await fetch('/search-index.json').then((r) => r.json() as Promise<{ t: string; u: string }[]>).catch(() => []);
      const titles = new Map(idx.map((d) => [d.u, d.t]));
      const items = saved.map((s) => [`/radar/item/${s}/`, titles.get(`/radar/item/${s}/`)] as const).filter(([, t]) => t);
      ul.replaceChildren(...items.map(([u, t]) => { const li = document.createElement('li'); const a = document.createElement('a'); a.href = u; a.textContent = t!; li.append(a); return li; }));
      show('[data-saved-empty]', items.length === 0);
    }
  }

  if (view === 'onboarding') {
    const form = $<HTMLFormElement>('[data-onboarding-form]');
    const role = (meta.requested_role ?? 'founder') as string;
    document.querySelectorAll<HTMLElement>('[data-role-section]').forEach((s) => (s.hidden = s.dataset.roleSection !== role && !(s.dataset.roleSection === 'other' && !['founder', 'investor', 'mentor', 'partner'].includes(role))));
    if (form) {
      for (const [k, v] of Object.entries(meta.profile ?? {})) { const el = form.elements.namedItem(k) as HTMLInputElement | null; if (el && typeof v === 'string') el.value = v; }
      form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const st = $('[data-onb-status]');
        const fd = new FormData(form); const profile: Record<string, string> = {};
        fd.forEach((v, k) => { const el = form.elements.namedItem(k) as HTMLElement | null; if (el && !el.closest('[hidden]')) profile[k] = String(v).slice(0, 300); });
        const btn = form.querySelector<HTMLButtonElement>('button[type="submit"]'); if (btn) btn.disabled = true;
        const { error } = await sb.auth.updateUser({ data: { profile, onboarding_complete: true } });
        if (btn) btn.disabled = false;
        if (error) { if (st) { st.className = 'notice danger'; st.textContent = 'We could not save your profile. Your answers are still here — please try again.'; st.hidden = false; st.focus(); } return; }
        await api('/api/referrals?action=qualify', session.access_token, { method: 'POST', body: '{}' }).catch(() => null);
        location.assign('/app/?onboarded=1');
      });
    }
  }
}
void main().catch(() => { show('[data-app-loading]', false); show('[data-app-error]'); });
