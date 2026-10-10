import { openKV } from './store.ts';
import type { Deps } from './handlers.ts';

export function depsFromEnv(env: Record<string, string | undefined> = process.env): Deps {
  return {
    supabaseUrl: env.PUBLIC_SUPABASE_URL,
    anonKey: env.PUBLIC_SUPABASE_ANON_KEY,
    submissions: openKV('submissions', env),
    meta: openKV('submission-meta', env),
    referrals: openKV('referrals', env),
    salt: env.SR_HASH_SALT ?? 'startuproof',
    allowedOrigins: (env.SR_ALLOWED_ORIGINS ?? '').split(',').map((s) => s.trim()).filter(Boolean),
  };
}
