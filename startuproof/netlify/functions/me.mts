import type { Config } from '@netlify/functions';
import { handleMe } from '../lib/handlers.ts';
import { depsFromEnv } from '../lib/deps.ts';
export default (req: Request) => handleMe(req, depsFromEnv());
export const config: Config = { path: '/api/me', method: ['GET'] };
