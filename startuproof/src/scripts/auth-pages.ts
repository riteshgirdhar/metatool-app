import { authConfigured, getClient, safeNext, friendlyAuthError, loginUrl } from './auth-client';

const page = document.querySelector<HTMLElement>('[data-auth-page]')?.dataset.authPage;
const params = new URLSearchParams(location.search);
const hash = new URLSearchParams(location.hash.slice(1));
const status = document.querySelector<HTMLElement>('[data-auth-status]');

function say(kind: 'error' | 'ok' | 'info', html: string) {
  if (!status) return;
  status.className = `notice ${kind === 'error' ? 'danger' : kind}`;
  status.innerHTML = html;
  status.hidden = false;
  status.focus();
}
function esc(s: string) { return s.replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]!)); }
function busy(form: HTMLFormElement, on: boolean, label?: string) {
  const b = form.querySelector<HTMLButtonElement>('button[type="submit"]');
  if (!b) return;
  if (on) { b.dataset.label = b.innerHTML; b.disabled = true; b.innerHTML = `<span class="spinner" aria-hidden="true"></span> ${label ?? 'Please wait…'}`; }
  else { b.disabled = false; b.innerHTML = b.dataset.label ?? b.innerHTML; }
}
function fieldError(form: HTMLFormElement, name: string, msg: string) {
  const input = form.querySelector<HTMLInputElement>(`[name="${name}"]`);
  const err = form.querySelector<HTMLElement>(`[data-error-for="${name}"]`);
  input?.setAttribute('aria-invalid', 'true');
  if (err) { err.textContent = msg; err.hidden = false; }
  input?.focus();
}
function clearErrors(form: HTMLFormElement) {
  form.querySelectorAll<HTMLElement>('[data-error-for]').forEach((e) => { e.hidden = true; e.textContent = ''; });
  form.querySelectorAll('[aria-invalid]').forEach((e) => e.removeAttribute('aria-invalid'));
}
const linkError = () => params.get('error_code') ?? hash.get('error_code') ?? params.get('error') ?? hash.get('error');
const linkErrorText = () => params.get('error_description') ?? hash.get('error_description') ?? '';

async function resend(email: string) {
  try {
    const sb = await getClient();
    const { error } = await sb.auth.resend({ type: 'signup', email, options: { emailRedirectTo: `${location.origin}/auth/callback/?next=${encodeURIComponent(safeNext(params.get('next')))}` } });
    if (error) throw error;
    say('ok', `<strong>Verification email sent.</strong> If an unverified account exists for ${esc(email)}, a new link is on its way. Links expire, so use the newest one.`);
  } catch (e) { say('error', esc(friendlyAuthError(e))); }
}
function wireResend(getEmail: () => string) {
  document.querySelectorAll<HTMLButtonElement>('[data-resend]').forEach((b) => b.addEventListener('click', () => {
    const email = getEmail();
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) { say('error', 'Enter your email address first, then choose resend.'); return; }
    void resend(email);
  }));
}

function disableAll(reason: string) {
  document.querySelectorAll<HTMLFormElement>('form[data-auth-form]').forEach((f) => f.querySelectorAll<HTMLElement>('input, button, select').forEach((el) => el.setAttribute('disabled', '')));
  say('info', reason);
}

async function init() {
  const intent = params.get('intent');
  const intentBox = document.querySelector<HTMLElement>('[data-intent]');
  if (intent && intentBox) {
    const map: Record<string, string> = { 'intro-request': 'Log in to send your introduction request — your message has been kept.', 'investor-verification': 'Log in to submit your investor verification.', 'view-startup': 'Log in to see member details for this startup.', 'view-investor': 'Log in to see investor details.', 'view-investors': 'Log in to see members-only investors.', 'view-mentor': 'Log in to see mentor availability.' };
    if (map[intent]) { intentBox.textContent = map[intent]; intentBox.hidden = false; }
  }
  // Keep the destination when switching between log in and sign up.
  document.querySelectorAll<HTMLAnchorElement>('[data-keep-next]').forEach((a) => { const u = new URL(a.href); params.forEach((v, k) => { if (['next', 'intent', 'ref', 'role'].includes(k)) u.searchParams.set(k, v); }); a.href = u.pathname + u.search; });

  if (!authConfigured) { disableAll('<strong>Sign-in is temporarily unavailable.</strong> Accounts are not being created or accessed on this preview right now. Nothing you type here is stored. Please try again later or <a href="/contact/">contact us</a>.'); return; }

  if (page === 'signup') {
    const form = document.querySelector<HTMLFormElement>('form[data-auth-form]')!;
    const role = params.get('role');
    if (role) { const r = form.querySelector<HTMLInputElement>(`input[name="role"][value="${CSS.escape(role)}"]`); if (r) r.checked = true; }
    wireResend(() => (form.elements.namedItem('email') as HTMLInputElement).value.trim());
    form.addEventListener('submit', async (e) => {
      e.preventDefault(); clearErrors(form);
      const fd = new FormData(form);
      const name = String(fd.get('full_name') ?? '').trim(); const email = String(fd.get('email') ?? '').trim();
      const password = String(fd.get('password') ?? ''); const reqRole = String(fd.get('role') ?? 'founder');
      if (name.length < 2) return fieldError(form, 'full_name', 'Enter your name');
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return fieldError(form, 'email', 'Enter a valid email address');
      if (password.length < 10) return fieldError(form, 'password', 'Use at least 10 characters');
      if (!fd.get('agree')) return fieldError(form, 'agree', 'Please confirm you have read the terms and privacy notice');
      busy(form, true, 'Creating account…');
      try {
        const sb = await getClient();
        const ref = params.get('ref');
        const { data, error } = await sb.auth.signUp({ email, password, options: {
          emailRedirectTo: `${location.origin}/auth/callback/?next=${encodeURIComponent(safeNext(params.get('next'), '/app/onboarding/'))}`,
          // requested_role is informational. Authorization uses server-controlled app_metadata only.
          data: { full_name: name, requested_role: reqRole, ...(ref && /^[A-F0-9]{8}$/.test(ref) ? { ref_code: ref } : {}) },
        } });
        if (error) throw error;
        if (data.session) { location.assign(safeNext(params.get('next'), '/app/onboarding/')); return; }
        form.hidden = true;
        say('ok', `<strong>Check your email.</strong> We sent a verification link to ${esc(email)}. Open it on this device to finish creating your account. <br /><button type="button" class="btn btn-secondary" data-resend-after>Resend email</button>`);
        status?.querySelector('[data-resend-after]')?.addEventListener('click', () => void resend(email));
      } catch (err) { say('error', esc(friendlyAuthError(err))); }
      finally { busy(form, false); }
    });
  }

  if (page === 'login') {
    const form = document.querySelector<HTMLFormElement>('form[data-auth-form]')!;
    const sb = await getClient();
    if (params.get('reason') === 'expired') {
      // The server rejected the stored session; discard it locally so we don't bounce straight back.
      await sb.auth.signOut({ scope: 'local' }).catch(() => null);
      say('info', 'Your session expired. Please log in again.');
    } else {
      const { data } = await sb.auth.getSession();
      if (data.session) { location.replace(safeNext(params.get('next'))); return; }
    }
    if (params.get('reason') === 'logged-out') say('ok', 'You have been logged out.');
    wireResend(() => (form.elements.namedItem('email') as HTMLInputElement).value.trim());
    form.addEventListener('submit', async (e) => {
      e.preventDefault(); clearErrors(form);
      const fd = new FormData(form);
      const email = String(fd.get('email') ?? '').trim(); const password = String(fd.get('password') ?? '');
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return fieldError(form, 'email', 'Enter a valid email address');
      if (!password) return fieldError(form, 'password', 'Enter your password');
      busy(form, true, 'Logging in…');
      try {
        const { error } = await sb.auth.signInWithPassword({ email, password });
        if (error) throw error;
        location.assign(safeNext(params.get('next')));
      } catch (err) {
        const msg = friendlyAuthError(err);
        say('error', `${esc(msg)}${/verify/.test(msg) ? ' <button type="button" class="btn btn-secondary" data-resend>Resend verification email</button>' : ''}`);
        wireResend(() => email);
      } finally { busy(form, false); }
    });
  }

  if (page === 'forgot') {
    const form = document.querySelector<HTMLFormElement>('form[data-auth-form]')!;
    form.addEventListener('submit', async (e) => {
      e.preventDefault(); clearErrors(form);
      const email = String(new FormData(form).get('email') ?? '').trim();
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return fieldError(form, 'email', 'Enter a valid email address');
      busy(form, true, 'Sending…');
      try {
        const sb = await getClient();
        const { error } = await sb.auth.resetPasswordForEmail(email, { redirectTo: `${location.origin}/reset/` });
        if (error && !/not found|user/i.test(error.message)) throw error;
        form.hidden = true;
        say('ok', `<strong>Check your email.</strong> If an account exists for ${esc(email)}, we've sent a link to reset the password. It can be used once and expires soon.`);
      } catch (err) { say('error', esc(friendlyAuthError(err))); }
      finally { busy(form, false); }
    });
  }

  if (page === 'reset') {
    const form = document.querySelector<HTMLFormElement>('form[data-auth-form]')!;
    if (linkError()) { form.hidden = true; say('error', `<strong>This reset link has expired or was already used.</strong> ${esc(linkErrorText())} <a href="/forgot/">Request a new link</a>.`); return; }
    const sb = await getClient();
    let ready = false;
    sb.auth.onAuthStateChange((evt) => { if (evt === 'PASSWORD_RECOVERY' || evt === 'SIGNED_IN') ready = true; });
    const { data } = await sb.auth.getSession(); if (data.session) ready = true;
    if (!ready) { form.hidden = true; say('error', '<strong>Open this page from the link in your reset email.</strong> If the link has expired, <a href="/forgot/">request a new one</a>.'); return; }
    form.addEventListener('submit', async (e) => {
      e.preventDefault(); clearErrors(form);
      const fd = new FormData(form); const p1 = String(fd.get('password') ?? ''); const p2 = String(fd.get('confirm') ?? '');
      if (p1.length < 10) return fieldError(form, 'password', 'Use at least 10 characters');
      if (p1 !== p2) return fieldError(form, 'confirm', 'Passwords do not match');
      busy(form, true, 'Saving…');
      try {
        const { error } = await sb.auth.updateUser({ password: p1 });
        if (error) throw error;
        form.hidden = true; say('ok', '<strong>Password updated.</strong> <a href="/app/">Continue to your account</a>.');
      } catch (err) { say('error', esc(friendlyAuthError(err))); }
      finally { busy(form, false); }
    });
  }

  if (page === 'callback') {
    if (linkError()) {
      say('error', `<strong>This link has expired or is invalid.</strong> ${esc(linkErrorText())} Log in to request a new verification email. <a class="btn btn-secondary" href="${loginUrl(safeNext(params.get('next')))}">Go to log in</a>`);
      return;
    }
    const sb = await getClient();
    // detectSessionInUrl exchanges the code; wait briefly for the session.
    let session = (await sb.auth.getSession()).data.session;
    for (let i = 0; !session && i < 10; i++) { await new Promise((r) => setTimeout(r, 300)); session = (await sb.auth.getSession()).data.session; }
    if (!session) { say('error', `<strong>We couldn't confirm this link.</strong> It may have been opened in a different browser. <a href="${loginUrl()}">Log in</a> instead.`); return; }
    say('ok', 'Email verified. Taking you to your account…');
    location.replace(safeNext(params.get('next'), '/app/onboarding/'));
  }
}
void init().catch((e) => say('error', esc(friendlyAuthError(e))));
