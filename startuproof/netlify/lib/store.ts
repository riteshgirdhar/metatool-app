/**
 * Durable key-value storage for submissions, idempotency records, rate limits and referrals.
 * Production uses Netlify Blobs (strong consistency). An in-memory store exists ONLY for local tests and is refused
 * whenever the code runs on Netlify, so a deploy can never silently fall back to non-durable storage.
 */
import { getStore } from '@netlify/blobs';

export interface KV {
  get(key: string): Promise<unknown | null>;
  set(key: string, value: unknown): Promise<void>;
  /** Write only if absent. Returns false when the key already existed. */
  create(key: string, value: unknown): Promise<boolean>;
  list(prefix: string): Promise<string[]>;
}

const memory = new Map<string, Map<string, string>>();
export function memoryKV(name: string): KV {
  if (!memory.has(name)) memory.set(name, new Map());
  const m = memory.get(name)!;
  return {
    async get(k) { const v = m.get(k); return v === undefined ? null : JSON.parse(v); },
    async set(k, v) { m.set(k, JSON.stringify(v)); },
    async create(k, v) { if (m.has(k)) return false; m.set(k, JSON.stringify(v)); return true; },
    async list(p) { return [...m.keys()].filter((k) => k.startsWith(p)); },
  };
}
export function resetMemory() { memory.clear(); }

function blobsKV(name: string): KV {
  const store = getStore({ name, consistency: 'strong' });
  return {
    async get(k) { return (await store.get(k, { type: 'json' })) ?? null; },
    async set(k, v) { await store.setJSON(k, v); },
    async create(k, v) {
      const res = await store.setJSON(k, v, { onlyIfNew: true });
      return res.modified;
    },
    async list(p) { const { blobs } = await store.list({ prefix: p }); return blobs.map((b) => b.key); },
  };
}

export function openKV(name: string, env: Record<string, string | undefined> = process.env): KV {
  const onNetlify = Boolean(env.NETLIFY || env.NETLIFY_BLOBS_CONTEXT || env.CONTEXT || env.SITE_ID);
  if (env.SR_LOCAL_MEMORY_STORE === '1' && !onNetlify) return memoryKV(name);
  return blobsKV(name);
}
