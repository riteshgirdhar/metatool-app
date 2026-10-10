// Generates 1200x630 social preview images and the apple-touch-icon from SVG. Run: node scripts/og.mjs
// Output is committed so builds stay reproducible without native image tooling on the build host.
import sharp from 'sharp';
import { mkdirSync } from 'node:fs';

const out = new URL('../public/og/', import.meta.url);
mkdirSync(out, { recursive: true });

const mark = (x, y, s = 1) => `<g transform="translate(${x} ${y}) scale(${s})"><rect width="32" height="32" rx="7" fill="#1b1e22"/><path d="M6.5 15.5 16 7.5l9.5 8" fill="none" stroke="#3fc2a6" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/><path d="M10.5 24.5v-6.2h11v6.2" fill="none" stroke="#fff" stroke-width="2.2" stroke-linejoin="round"/></g>`;
const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
const card = (eyebrow, lines, accent = '#0e6b5a') => `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <rect width="1200" height="630" fill="#fafaf7"/>
  <rect x="0" y="0" width="16" height="630" fill="${accent}"/>
  ${mark(80, 72, 2)}
  <text x="160" y="118" font-family="Inter, DejaVu Sans, Arial, sans-serif" font-size="34" font-weight="700" fill="#1b1e22">Startup Roof</text>
  <text x="80" y="260" font-family="Inter, DejaVu Sans, Arial, sans-serif" font-size="28" font-weight="700" letter-spacing="3" fill="${accent}">${esc(eyebrow.toUpperCase())}</text>
  ${lines.map((l, i) => `<text x="80" y="${340 + i * 78}" font-family="Inter, DejaVu Sans, Arial, sans-serif" font-size="64" font-weight="700" fill="#1b1e22">${esc(l)}</text>`).join('')}
  <text x="80" y="570" font-family="Inter, DejaVu Sans, Arial, sans-serif" font-size="26" fill="#5f656d">startuproof.com</text>
</svg>`;

const cards = {
  default: card('For founders', ['Build, connect, raise and', 'scale — under one roof.']),
  radar: card('Radar', ['Startup funding and', 'ecosystem news, checked.'], '#23518c'),
  academy: card('Academy', ['Practical guides for', 'every stage of a startup.']),
  tv: card('Startup Roof TV', ['Founder programming,', 'in development.'], '#6b3f8f'),
  festival: card('Founder Festival · Dubai', ['Founder Festival 2027:', 'planning status.'], '#8a4b00'),
};
for (const [name, svg] of Object.entries(cards)) {
  await sharp(Buffer.from(svg)).png({ compressionLevel: 9, palette: true }).toFile(new URL(`${name}.png`, out).pathname);
}
const icon = `<svg xmlns="http://www.w3.org/2000/svg" width="180" height="180" viewBox="0 0 32 32"><rect width="32" height="32" fill="#1b1e22"/><path d="M6.5 15.5 16 7.5l9.5 8" fill="none" stroke="#3fc2a6" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/><path d="M10.5 24.5v-6.2h11v6.2" fill="none" stroke="#fff" stroke-width="2.2" stroke-linejoin="round"/></svg>`;
await sharp(Buffer.from(icon)).resize(180, 180).png().toFile(new URL('../public/apple-touch-icon.png', import.meta.url).pathname);
console.log('og images written');
