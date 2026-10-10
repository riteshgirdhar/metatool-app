import type { Config } from '@netlify/functions';
import { handleReferrals } from '../lib/handlers.ts';
import { depsFromEnv } from '../lib/deps.ts';
export default (req: Request) => handleReferrals(req, depsFromEnv());
export const config: Config = { path: '/api/referrals', method: ['GET', 'POST'] };
