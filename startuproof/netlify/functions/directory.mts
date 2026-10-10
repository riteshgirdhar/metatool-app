import type { Config } from '@netlify/functions';
import { handleDirectory } from '../lib/handlers.ts';
import { depsFromEnv } from '../lib/deps.ts';
export default (req: Request) => handleDirectory(req, depsFromEnv());
export const config: Config = { path: '/api/directory', method: ['GET'] };
