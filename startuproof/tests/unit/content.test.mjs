import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { RADAR, EXCLUDED, FINANCING_KINDS } from '../../src/data/radar.ts';
import { buildIcs } from '../../src/lib/ics.ts';
import { OPPORTUNITIES, SHOWS } from '../../src/data/content.ts';
import { PRICING, FESTIVAL } from '../../src/config/site.ts';

test('Radar: slugs unique, editions justified, no unrelated topics', () => {
  const slugs = new Set();
  for (const i of RADAR) {
    assert.ok(!slugs.has(i.slug), `duplicate slug ${i.slug}`); slugs.add(i.slug);
    const geo = i.storyGeography.join(' ').toLowerCase();
    for (const e of i.editions) {
      const direct = { uae: /uae|gcc|mena/, saudi: /saudi|mena/, qatar: /qatar/, egypt: /egypt/, india: /india/, global: /./ }[e].test(geo) || e === 'global';
      assert.ok(direct || i.connectionNote, `${i.slug} in ${e} edition without geography or documented connection`);
    }
    assert.doesNotMatch(i.title, /Ronaldo|cricket|militia|Gaza|diesel|Yemen|keyboard/i);
    assert.equal(i.publishedAtStatus === 'verified', Boolean(i.publishedAt), 'publishedAt only when verified');
  }
  assert.ok(EXCLUDED.length >= 15);
});

test('Radar: amounts are never inferred, and financing kinds are specific', () => {
  for (const i of RADAR) {
    if (i.amount) assert.ok(i.amount.basis.length > 5, `${i.slug} amount needs a basis`);
    if (i.kind === 'undisclosed_investment') assert.equal(i.amount, null, `${i.slug}: undisclosed must not carry an amount`);
  }
  assert.ok(RADAR.some((i) => i.kind === 'debt'));
  assert.ok(RADAR.some((i) => i.kind === 'investment_plan' || i.kind === 'acquisition'));
  assert.ok(RADAR.some((i) => i.kind === 'fund_close'));
  assert.ok(FINANCING_KINDS.length >= 8);
});

test('ICS: valid all-day event with UID, DTSTAMP, DTSTART/DTEND and CRLF line endings', () => {
  const ics = buildIcs({ uid: 'x@startuproof.com', date: '2027-02-15', summary: 'Deadline: Test, with comma; and semicolon', description: 'Line one\nLine two', url: 'https://startuproof.com/x/', dtstamp: new Date('2026-10-10T12:00:00Z') });
  assert.match(ics, /^BEGIN:VCALENDAR\r\nVERSION:2.0\r\n/);
  assert.match(ics, /UID:x@startuproof.com\r\n/);
  assert.match(ics, /DTSTAMP:20261010T120000Z\r\n/);
  assert.match(ics, /DTSTART;VALUE=DATE:20270215\r\n/);
  assert.match(ics, /DTEND;VALUE=DATE:20270216\r\n/);
  assert.match(ics, /SUMMARY:Deadline: Test\\, with comma\\; and semicolon/);
  assert.match(ics, /DESCRIPTION:Line one\\nLine two/);
  for (const line of ics.split('\r\n')) assert.ok(Buffer.byteLength(line) <= 75, `line too long: ${line}`);
  assert.throws(() => buildIcs({ uid: 'a', date: '15/02/2027', summary: '', description: '', url: '' }));
});

test('Opportunities: calendar only for confirmed dates; provisional dates carry no time or timezone', () => {
  for (const o of OPPORTUNITIES) if (o.dateStatus === 'provisional') { assert.equal(o.deadlineTime, null); assert.equal(o.deadlineTz, null); }
});

test('TV: episode numbers are sequential from 1 for each show', () => {
  for (const s of SHOWS) assert.deepEqual(s.episodes.map((e) => e.n), s.episodes.map((_, i) => i + 1), s.slug);
});

test('Commercial facts stay pending until approved', () => {
  assert.equal(PRICING.paymentsActive, false);
  for (const p of PRICING.plans) if (p.status !== 'live') assert.equal(p.price, null, `${p.id} has an unapproved price`);
  assert.equal(FESTIVAL.venue, null); assert.equal(FESTIVAL.zones, null); assert.equal(FESTIVAL.dates.status, 'provisional');
});

test('no member-only or investor-only values leak into the static build', () => {
  const dist = new URL('../../dist/', import.meta.url).pathname;
  const files = [];
  const walk = (d) => { for (const f of readdirSync(d)) { const p = join(d, f); statSync(p).isDirectory() ? walk(p) : /\.(html|js|json|xml|txt)$/.test(f) && files.push(p); } };
  walk(dist);
  const all = files.map((f) => readFileSync(f, 'utf8')).join('\n');
  for (const secret of ['320 paying SMEs', 'Wafeq', '62 MW installed', 'Al Noor Family Office', 'Sana Qureshi', 'USD 500k', 'No financials uploaded']) {
    assert.ok(!all.includes(secret), `private value leaked into dist: ${secret}`);
  }
  assert.ok(!/service_role|SUPABASE_SERVICE/i.test(all), 'privileged key name present in client output');
});
