/**
 * Verifies a Supabase access token by asking Supabase Auth who it belongs to. Authorization decisions use only
 * server-controlled `app_metadata` — never `user_metadata`, which the user can edit.
 */
import { HttpError } from './http.ts';

export interface Principal {
  id: string; email: string; emailVerified: boolean;
  investorVerified: boolean; admin: boolean;
  requestedRole: string | null; // informational only
}
export interface AuthDeps { supabaseUrl?: string; anonKey?: string; fetch?: typeof fetch }

export function authConfigured(d: AuthDeps) { return Boolean(d.supabaseUrl && d.anonKey); }

export function principalFromUser(u: Record<string, any>): Principal {
  const app = (u.app_metadata ?? {}) as Record<string, unknown>;
  const user = (u.user_metadata ?? {}) as Record<string, unknown>;
  return {
    id: String(u.id), email: String(u.email ?? ''), emailVerified: Boolean(u.email_confirmed_at),
    investorVerified: app.investor_verified === true,
    admin: app.sr_admin === true,
    requestedRole: typeof user.requested_role === 'string' ? user.requested_role : null,
  };
}

export async function requirePrincipal(req: Request, d: AuthDeps): Promise<Principal> {
  if (!authConfigured(d)) throw new HttpError(503, 'auth_unavailable', 'Sign-in is not available right now. Please try again later.');
  const h = req.headers.get('authorization') ?? '';
  const token = h.startsWith('Bearer ') ? h.slice(7).trim() : '';
  if (!token || token.length > 4096) throw new HttpError(401, 'unauthenticated', 'Please log in to continue.');
  let res: Response;
  try {
    res = await (d.fetch ?? fetch)(`${d.supabaseUrl!.replace(/\/$/, '')}/auth/v1/user`, {
      headers: { apikey: d.anonKey!, authorization: `Bearer ${token}` },
      signal: AbortSignal.timeout(6000),
    });
  } catch {
    throw new HttpError(503, 'auth_unavailable', 'We could not verify your session. Please try again shortly.');
  }
  if (res.status === 401 || res.status === 403) throw new HttpError(401, 'session_expired', 'Your session has expired. Please log in again.');
  if (!res.ok) throw new HttpError(503, 'auth_unavailable', 'We could not verify your session. Please try again shortly.');
  const p = principalFromUser(await res.json());
  if (!p.emailVerified) throw new HttpError(403, 'email_unverified', 'Please verify your email address first.');
  return p;
}
