/**
 * Supabase Auth in the browser. Loaded only on pages that need a session (auth pages, member area, gated actions).
 * There is NO local fallback: if the identity provider is not configured or unreachable, sign-in is unavailable.
 */
import type { SupabaseClient, Session } from '@supabase/supabase-js';

const url = import.meta.env.PUBLIC_SUPABASE_URL as string | undefined;
const key = import.meta.env.PUBLIC_SUPABASE_ANON_KEY as string | undefined;
export const authConfigured = Boolean(url && key);

let client: Promise<SupabaseClient> | null = null;
export function getClient(): Promise<SupabaseClient> {
  if (!authConfigured) return Promise.reject(new Error('auth_unavailable'));
  client ??= import('@supabase/supabase-js').then(({ createClient }) =>
    createClient(url!, key!, { auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true, flowType: 'pkce' } }));
  return client;
}
export async function getSession(): Promise<Session | null> {
  if (!authConfigured) return null;
  const sb = await getClient();
  const { data } = await sb.auth.getSession();
  return data.session;
}
export async function accessToken(): Promise<string | null> {
  return (await getSession())?.access_token ?? null;
}

/** Only allow same-site relative paths as post-login destinations. */
export function safeNext(raw: string | null | undefined, fallback = '/app/'): string {
  if (!raw) return fallback;
  try {
    const u = new URL(raw, location.origin);
    if (u.origin !== location.origin) return fallback;
    if (!u.pathname.startsWith('/') || u.pathname.startsWith('//')) return fallback;
    if (['/login/', '/signup/', '/forgot/', '/reset/'].includes(u.pathname)) return fallback;
    return u.pathname + u.search + u.hash;
  } catch { return fallback; }
}
export function loginUrl(next = location.pathname + location.search, intent?: string) {
  const p = new URLSearchParams({ next });
  if (intent) p.set('intent', intent);
  return `/login/?${p}`;
}

export function friendlyAuthError(e: unknown): string {
  const msg = (e as { message?: string; code?: string })?.message ?? String(e);
  const code = (e as { code?: string })?.code ?? '';
  if (/auth_unavailable/.test(msg)) return 'Sign-in is not available right now. Please try again later.';
  if (code === 'invalid_credentials' || /Invalid login credentials/i.test(msg)) return 'That email and password do not match an account.';
  if (code === 'email_not_confirmed' || /Email not confirmed/i.test(msg)) return 'Please verify your email address first. You can resend the verification email below.';
  if (code === 'user_already_exists' || /already registered/i.test(msg)) return 'An account with this email may already exist. Try logging in or resetting your password.';
  if (code === 'weak_password' || /password/i.test(msg) && /weak|short|characters/i.test(msg)) return 'Choose a stronger password: at least 10 characters, not a common password.';
  if (code === 'over_email_send_rate_limit' || /rate limit/i.test(msg)) return 'Too many emails were requested. Please wait a few minutes and try again.';
  if (/fetch|network|Failed to fetch/i.test(msg)) return 'We could not reach the sign-in service. Check your connection and try again.';
  if (/expired|otp_expired|invalid.*link/i.test(msg)) return 'This link has expired or was already used. Request a new one.';
  return 'Something went wrong. Please try again.';
}
