/** RFC 5545 calendar generation for all-day deadlines. Callers must only pass confirmed dates. */
export interface IcsEvent { uid: string; date: string; summary: string; description: string; url: string; dtstamp?: Date }
const fold = (line: string) => {
  const out: string[] = []; let s = line;
  while (Buffer.byteLength(s, 'utf8') > 75) { let i = 74; while (Buffer.byteLength(s.slice(0, i), 'utf8') > 74) i--; out.push(s.slice(0, i)); s = ` ${s.slice(i)}`; }
  out.push(s); return out.join('\r\n');
};
const esc = (s: string) => s.replace(/\\/g, '\\\\').replace(/;/g, '\\;').replace(/,/g, '\\,').replace(/\r?\n/g, '\\n');
const ymd = (iso: string) => iso.replace(/-/g, '');
function addDay(iso: string) { const d = new Date(`${iso}T00:00:00Z`); d.setUTCDate(d.getUTCDate() + 1); return d.toISOString().slice(0, 10); }
const stamp = (d: Date) => d.toISOString().replace(/[-:]/g, '').replace(/\.\d{3}/, '');
export function buildIcs(e: IcsEvent): string {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(e.date)) throw new Error('ICS requires a YYYY-MM-DD date');
  return [
    'BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Startup Roof//Opportunities//EN', 'CALSCALE:GREGORIAN', 'METHOD:PUBLISH',
    'BEGIN:VEVENT', `UID:${e.uid}`, `DTSTAMP:${stamp(e.dtstamp ?? new Date())}`,
    `DTSTART;VALUE=DATE:${ymd(e.date)}`, `DTEND;VALUE=DATE:${ymd(addDay(e.date))}`,
    `SUMMARY:${esc(e.summary)}`, `DESCRIPTION:${esc(e.description)}`, `URL:${e.url}`, 'TRANSP:TRANSPARENT',
    'END:VEVENT', 'END:VCALENDAR', '',
  ].map(fold).join('\r\n');
}
