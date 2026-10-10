/**
 * Progressive form controller. Success is shown ONLY when the server confirms a durable write and returns a
 * reference. On any failure the user's input stays in place and the same idempotency key is reused, so retrying
 * can never create a duplicate.
 */
const AUTH_FORMS = new Set(['intro-request', 'investor-verification']);

function uuid() {
  return (crypto.randomUUID?.() ?? [...crypto.getRandomValues(new Uint8Array(16))].map((b) => b.toString(16).padStart(2, '0')).join(''));
}

function setStatus(form: HTMLFormElement, kind: 'error' | 'ok' | 'info' | '', html: string) {
  const box = form.querySelector<HTMLElement>('[data-form-status]');
  if (!box) return;
  box.className = `form-status${kind ? ` notice ${kind === 'error' ? 'danger' : kind}` : ''}`;
  box.innerHTML = html;
  if (kind) box.focus();
}
function clearFieldErrors(form: HTMLFormElement) {
  form.querySelectorAll<HTMLElement>('[data-error-for]').forEach((el) => { el.textContent = ''; el.hidden = true; });
  form.querySelectorAll('[aria-invalid="true"]').forEach((el) => el.removeAttribute('aria-invalid'));
}
function showFieldErrors(form: HTMLFormElement, details: Record<string, string>) {
  let first: HTMLElement | null = null;
  for (const [field, msg] of Object.entries(details)) {
    const input = form.querySelector<HTMLElement>(`[name="${CSS.escape(field)}"]`);
    const err = form.querySelector<HTMLElement>(`[data-error-for="${CSS.escape(field)}"]`);
    if (input) { input.setAttribute('aria-invalid', 'true'); first ??= input; }
    if (err) { err.textContent = msg; err.hidden = false; }
  }
  first?.focus();
}
function esc(s: string) { return s.replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]!)); }

function collect(form: HTMLFormElement) {
  const fd = new FormData(form);
  const fields: Record<string, string> = {};
  fd.forEach((v, k) => { if (!k.startsWith('_') && typeof v === 'string') fields[k] = v; });
  return { fields, hp: String(fd.get('_company_website') ?? '') };
}

function clientValidate(form: HTMLFormElement): boolean {
  const details: Record<string, string> = {};
  form.querySelectorAll<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>('input, select, textarea').forEach((el) => {
    if (!el.name || el.name.startsWith('_') || el.checkValidity()) return;
    const label = form.querySelector(`label[for="${el.id}"]`)?.textContent?.replace('*', '').trim() ?? 'This field';
    details[el.name] = el.validity.valueMissing ? `${label} is required` : el.validity.typeMismatch ? (el.type === 'email' ? 'Enter a valid email address' : 'Enter a full URL starting with https://') : el.validity.tooShort ? `Please write at least ${(el as HTMLInputElement).minLength} characters` : el.validationMessage;
  });
  if (Object.keys(details).length) { showFieldErrors(form, details); setStatus(form, 'error', '<strong>Please check the form.</strong> Some fields need attention.'); return false; }
  return true;
}

async function send(form: HTMLFormElement, started: number) {
  const type = form.dataset.form!;
  const btn = form.querySelector<HTMLButtonElement>('button[type="submit"]');
  const label = btn?.innerHTML ?? '';
  clearFieldErrors(form);
  if (!clientValidate(form)) return;
  const keyName = `sr-idem-${type}-${form.id}`;
  let idem = sessionStorage.getItem(keyName);
  if (!idem) { idem = uuid(); try { sessionStorage.setItem(keyName, idem); } catch { /* private mode */ } }
  const { fields, hp } = collect(form);
  const headers: Record<string, string> = { 'content-type': 'application/json' };
  if (AUTH_FORMS.has(type)) {
    const { accessToken, authConfigured, loginUrl } = await import('./auth-client');
    const token = authConfigured ? await accessToken().catch(() => null) : null;
    if (!token) {
      setStatus(form, 'info', `<strong>Log in to continue.</strong> <a href="${loginUrl(location.pathname, type)}">Log in or create a free account</a>. Your message will still be here when you come back.`);
      try { sessionStorage.setItem(`sr-draft-${form.id}`, JSON.stringify(fields)); } catch { /* ignore */ }
      return;
    }
    headers.authorization = `Bearer ${token}`;
  }
  form.setAttribute('aria-busy', 'true');
  if (btn) { btn.disabled = true; btn.innerHTML = '<span class="spinner" aria-hidden="true"></span> Sending…'; }
  setStatus(form, '', '');
  let res: Response | null = null; let body: any = null;
  try {
    res = await fetch(form.action || '/api/submit', {
      method: 'POST', headers, signal: AbortSignal.timeout(20000),
      body: JSON.stringify({ type, idempotencyKey: idem, elapsedMs: Math.round(performance.now() - started), hp, fields }),
    });
    body = await res.json().catch(() => null);
  } catch { res = null; }
  form.removeAttribute('aria-busy');
  if (btn) { btn.disabled = false; btn.innerHTML = label; }

  if (res && (res.status === 201 || res.status === 200) && body?.ok && body.reference) {
    try { sessionStorage.removeItem(keyName); sessionStorage.removeItem(`sr-draft-${form.id}`); } catch { /* ignore */ }
    const success = form.dataset.success ?? 'Thank you — we have received your submission.';
    form.reset();
    form.querySelectorAll<HTMLElement>('[data-form-fields]').forEach((el) => (el.hidden = true));
    setStatus(form, 'ok', `<strong>${esc(success)}</strong> Your reference is <code>${esc(body.reference)}</code>. Keep it if you need to follow up. <button type="button" class="btn btn-ghost" data-form-again>Send another</button>`);
    form.querySelector('[data-form-again]')?.addEventListener('click', () => {
      form.querySelectorAll<HTMLElement>('[data-form-fields]').forEach((el) => (el.hidden = false));
      setStatus(form, '', '');
      form.querySelector<HTMLElement>('input, select, textarea')?.focus();
    });
    return;
  }
  if (res?.status === 422 && body?.details) { showFieldErrors(form, body.details); setStatus(form, 'error', `<strong>Please check the form.</strong> ${esc(body.message ?? '')}`); return; }
  if (res && (res.status === 401 || res.status === 403)) {
    const { loginUrl } = await import('./auth-client');
    setStatus(form, 'error', `<strong>${esc(body?.message ?? 'Please log in again.')}</strong> <a href="${loginUrl(location.pathname, type)}">Log in</a>. Your input has been kept.`);
    return;
  }
  const msg = body?.message ?? 'We could not reach our server, so nothing was sent.';
  setStatus(form, 'error', `<strong>Not sent.</strong> ${esc(msg)} Your answers are still in the form. <button type="submit" class="btn btn-secondary">Try again</button>`);
}

document.querySelectorAll<HTMLFormElement>('form[data-form]').forEach((form) => {
  const started = performance.now();
  form.noValidate = true;
  // Restore a draft saved before a login redirect.
  try {
    const draft = sessionStorage.getItem(`sr-draft-${form.id}`);
    if (draft) for (const [k, v] of Object.entries(JSON.parse(draft) as Record<string, string>)) {
      const el = form.elements.namedItem(k) as HTMLInputElement | null; if (el && 'value' in el) el.value = v;
    }
  } catch { /* ignore */ }
  form.addEventListener('submit', (e) => { e.preventDefault(); void send(form, started); });
});
