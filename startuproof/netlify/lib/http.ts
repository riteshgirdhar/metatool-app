export const SECURITY_HEADERS = {
  'content-type': 'application/json; charset=utf-8',
  'cache-control': 'no-store',
  'x-content-type-options': 'nosniff',
};
export function json(status: number, body: unknown, extra: Record<string, string> = {}) {
  return new Response(JSON.stringify(body), { status, headers: { ...SECURITY_HEADERS, ...extra } });
}
export async function readJson(req: Request, maxBytes = 32_000): Promise<unknown> {
  const len = Number(req.headers.get('content-length') ?? 0);
  if (len > maxBytes) throw new HttpError(413, 'payload_too_large', 'The submission is too large.');
  const text = await req.text();
  if (text.length > maxBytes) throw new HttpError(413, 'payload_too_large', 'The submission is too large.');
  try { return JSON.parse(text); } catch { throw new HttpError(400, 'invalid_json', 'The request could not be read.'); }
}
export class HttpError extends Error {
  status: number; code: string; details?: unknown;
  constructor(status: number, code: string, message: string, details?: unknown) {
    super(message); this.status = status; this.code = code; this.details = details;
  }
}
export function sameOrigin(req: Request, allowed: string[]): boolean {
  const origin = req.headers.get('origin');
  if (!origin) return true; // non-browser clients; other controls (honeypot, timing, rate limit) still apply
  try { const o = new URL(origin); return allowed.some((a) => a === o.origin) || o.hostname === new URL(req.url).hostname; } catch { return false; }
}
export async function sha256(input: string) {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(input));
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, '0')).join('');
}
export function clientIp(req: Request) {
  return req.headers.get('x-nf-client-connection-ip') ?? req.headers.get('x-forwarded-for')?.split(',')[0]?.trim() ?? 'unknown';
}
