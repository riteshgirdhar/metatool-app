import type { Config } from '@netlify/functions';
import { handleSubmit } from '../lib/handlers.ts';
import { depsFromEnv } from '../lib/deps.ts';
export default (req: Request) => handleSubmit(req, depsFromEnv());
export const config: Config = { path: '/api/submit', method: ['POST'] };
