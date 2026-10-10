import { z } from 'zod';

/**
 * Server-validated submission schemas. The server is authoritative; the browser uses matching HTML constraints
 * for fast feedback only. Keep field names in sync with src/components/forms/*.astro.
 */
const name = z.string().trim().min(2, 'Enter your name').max(120);
const email = z.string().trim().toLowerCase().email('Enter a valid email address').max(200);
const optionalText = (max: number) => z.string().trim().max(max).optional().or(z.literal('').transform(() => undefined));
const optionalUrl = z.string().trim().max(500).url('Enter a full URL starting with https://').optional().or(z.literal('').transform(() => undefined));
const message = (min = 10, max = 4000) => z.string().trim().min(min, `Please write at least ${min} characters`).max(max);
const stage = z.enum(['idea', 'pre-seed', 'seed', 'series-a', 'series-b-plus'], { message: 'Choose a stage' });

export const FORM_SCHEMAS = {
  contact: z.object({ name, email, organisation: optionalText(160),
    topic: z.enum(['general', 'support', 'press', 'partnership', 'account', 'other'], { message: 'Choose a topic' }), message: message() }),
  partnership: z.object({ name, email, organisation: z.string().trim().min(2, 'Enter your organisation').max(160),
    partnerType: z.enum(['university', 'corporate', 'government', 'accelerator', 'community', 'service-provider', 'investor-network', 'other'], { message: 'Choose a partner type' }),
    message: message() }),
  sponsor: z.object({ name, email, organisation: z.string().trim().min(2, 'Enter your organisation').max(160),
    interest: z.enum(['festival', 'programmes', 'radar', 'tv', 'academy', 'other'], { message: 'Choose an area' }), message: message() }),
  exhibitor: z.object({ name, email, company: z.string().trim().min(2, 'Enter your company').max(160), website: optionalUrl, stage, message: message(10, 2000) }),
  pitch: z.object({ name, email, company: z.string().trim().min(2, 'Enter your company').max(160), website: optionalUrl, stage,
    sector: z.string().trim().min(2, 'Enter your sector').max(80), raising: z.enum(['yes', 'no', 'unsure'], { message: 'Choose an option' }),
    oneLiner: message(10, 280), deckUrl: optionalUrl }),
  programme: z.object({ name, email, company: optionalText(160), programme: z.enum(['accelerator', 'incubator'], { message: 'Choose a programme' }),
    stage, message: optionalText(2000) }),
  'festival-interest': z.object({ name, email,
    role: z.enum(['founder', 'investor', 'mentor', 'partner', 'sponsor', 'attendee'], { message: 'Choose how you would take part' }),
    country: optionalText(80) }),
  provider: z.object({ name, email, company: z.string().trim().min(2, 'Enter your company').max(160),
    category: z.enum(['legal', 'accounting', 'banking', 'company-setup', 'hr', 'marketing', 'technology', 'other'], { message: 'Choose a category' }),
    website: optionalUrl, message: message(10, 2000) }),
  'mentor-application': z.object({ name, email, profileUrl: z.string().trim().url('Enter your LinkedIn or website URL').max(500),
    expertise: z.string().trim().min(3, 'List at least one area').max(300), availability: z.enum(['weekly', 'fortnightly', 'monthly', 'ad-hoc'], { message: 'Choose your availability' }),
    message: message(20, 2000) }),
  'radar-submission': z.object({ name, email, url: z.string().trim().url('Enter the full source URL').max(500),
    kind: z.enum(['funding', 'fund', 'programme', 'event', 'correction', 'other'], { message: 'Choose a type' }), note: message(10, 2000) }),
  'opportunity-submission': z.object({ name, email, organiser: z.string().trim().min(2).max(160), title: z.string().trim().min(4).max(200),
    url: z.string().trim().url('Enter the full application URL').max(500),
    deadline: z.string().regex(/^\d{4}-\d{2}-\d{2}$/, 'Use the date picker').optional().or(z.literal('').transform(() => undefined)),
    deadlineTz: optionalText(60), note: optionalText(2000) }),
  // Authenticated-only forms (server verifies the session; name/email come from the account, not the form)
  'intro-request': z.object({ targetType: z.enum(['startup', 'investor', 'mentor']), targetSlug: z.string().regex(/^[a-z0-9-]{2,80}$/), message: message(20, 1500) }),
  'investor-verification': z.object({ firm: z.string().trim().min(2, 'Enter your firm or “Independent angel”').max(160),
    roleTitle: z.string().trim().min(2).max(120), profileUrl: z.string().trim().url('Enter a profile or firm URL').max(500),
    ticket: z.enum(['<25k', '25k-100k', '100k-500k', '500k-2m', '>2m'], { message: 'Choose a typical cheque size' }), evidence: message(20, 2000) }),
} as const;

export type FormType = keyof typeof FORM_SCHEMAS;
export const AUTH_REQUIRED: ReadonlySet<FormType> = new Set(['intro-request', 'investor-verification']);
export const FORM_TYPES = Object.keys(FORM_SCHEMAS) as FormType[];
export const MIN_FILL_MS = 2500;

export function isFormType(t: unknown): t is FormType {
  return typeof t === 'string' && (FORM_TYPES as string[]).includes(t);
}
