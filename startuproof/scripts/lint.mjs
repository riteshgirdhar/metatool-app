// Project-specific lint: guards the security and honesty rules this rebuild depends on.
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

const root = new URL('..', import.meta.url).pathname;
const files = [];
const walk = (d) => { for (const f of readdirSync(d)) { const p = join(d, f); if (statSync(p).isDirectory()) walk(p); else if (/\.(ts|mts|astro|mjs)$/.test(f)) files.push(p); } };
['src', 'netlify'].forEach((d) => walk(join(root, d)));

const rules = [
  { re: /localStorage\.setItem\([^)]*password/i, msg: 'Never store passwords in browser storage' },
  { re: /SERVICE_ROLE|service_role/, msg: 'Privileged Supabase keys must not appear in source', skip: /netlify\/lib\// },
  { re: /demo[ _-]?admin|admin123|password123/i, msg: 'No demo or default credentials' },
  { re: /console\.log\(/, msg: 'Remove debug logging', skip: /scripts\// },
  { re: /user_metadata[^\n]*(investor_verified|sr_admin)/, msg: 'Authorization must not read user_metadata', skip: /tests\// },
  { re: /\bVERIFIED\b/, msg: 'Uppercase VERIFIED badges are not allowed without a verification process' },
];
const problems = [];
for (const f of files) {
  const text = readFileSync(f, 'utf8');
  for (const r of rules) {
    if (r.skip?.test(f)) continue;
    text.split('\n').forEach((line, i) => { if (r.re.test(line)) problems.push(`${f.replace(root, '')}:${i + 1} ${r.msg}`); });
  }
}
const pkg = JSON.parse(readFileSync(join(root, 'package.json'), 'utf8'));
for (const [name, v] of Object.entries({ ...pkg.dependencies, ...pkg.devDependencies })) if (!/^\d+\.\d+\.\d+$/.test(v)) problems.push(`package.json: ${name}@${v} is not pinned to an exact version`);
if (problems.length) { console.error(problems.join('\n')); process.exit(1); }
console.log(`lint: ${files.length} files clean`);
