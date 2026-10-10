import type { Config } from '@netlify/functions';
import { handleHealth } from '../lib/handlers.ts';
import { depsFromEnv } from '../lib/deps.ts';
export default () => handleHealth(depsFromEnv());
export const config: Config = { path: '/api/health', method: ['GET'] };
