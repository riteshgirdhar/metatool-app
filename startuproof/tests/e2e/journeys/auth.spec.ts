import { test, expect, type Page, type APIRequestContext } from '@playwright/test';

const PW = 'correct-horse-battery';
const uid = () => Math.random().toString(36).slice(2, 10);
const lastLink = async (request: APIRequestContext, email: string) =>
  (await (await request.get(`/mock-supabase/_test/last-link?email=${encodeURIComponent(email)}`)).json()).link as string;

async function signUp(page: Page, email: string, role = 'founder', query = '') {
  await page.goto(`/signup/${query}`);
  await page.getByLabel('Full name').fill('Journey Tester');
  await page.getByLabel('Email').fill(email);
  await page.getByLabel('Password').fill(PW);
  await page.locator(`input[name="role"][value="${role}"]`).check();
  await page.getByLabel(/I've read the/).check();
  await page.getByRole('button', { name: 'Create account' }).click();
  await expect(page.locator('[data-auth-status]')).toContainText('Check your email');
}
async function verify(page: Page, request: APIRequestContext, email: string) {
  const link = await lastLink(request, email);
  expect(link).toContain('/auth/callback/');
  await page.goto(link.replace(/^https?:\/\/[^/]+/, ''));
}
async function login(page: Page, email: string, next = '') {
  await page.goto(`/login/${next}`);
  await page.getByLabel('Email').fill(email);
  await page.getByLabel('Password').fill(PW);
  await page.getByRole('button', { name: 'Log in' }).click();
}
async function token(page: Page) {
  return page.evaluate(() => { const k = Object.keys(localStorage).find((x) => /^sb-.*-auth-token$/.test(x)); return k ? JSON.parse(localStorage.getItem(k)!).access_token as string : null; });
}

test.describe('founder journey', () => {
  test('signup → verify email → onboarding → member area → logout → login', async ({ page, request }) => {
    const email = `founder-${uid()}@example.com`;
    await signUp(page, email);
    // No password ever lands in browser storage
    expect(await page.evaluate(() => JSON.stringify({ ...localStorage }))).not.toContain(PW);
    await verify(page, request, email);
    await expect(page).toHaveURL(/\/app\/onboarding\/$/, { timeout: 15_000 });
    await expect(page.locator('[data-role-section="founder"]')).toBeVisible();
    await page.getByLabel('Company name').fill('Journey Co');
    await page.getByLabel('Stage', { exact: true }).selectOption('seed');
    await page.getByRole('button', { name: 'Save and continue' }).click();
    await expect(page).toHaveURL(/\/app\/\?onboarded=1$/);
    await expect(page.locator('[data-name]')).toHaveText('Journey Tester');
    await expect(page.locator('[data-onboarding-todo]')).toBeHidden();
    await expect(page.locator('[data-investor-status]')).toHaveText('Not applicable');
    await page.getByRole('button', { name: 'Log out' }).click();
    await expect(page).toHaveURL(/\/login\/\?reason=logged-out/);
    await expect(page.locator('[data-auth-status]')).toContainText('logged out');
    await login(page, email);
    await expect(page).toHaveURL(/\/app\/$/);
  });

  test('login preserves the intended destination and action', async ({ page, request }) => {
    const email = `next-${uid()}@example.com`;
    await signUp(page, email); await verify(page, request, email);
    await page.waitForURL(/\/app\/onboarding\//);
    await page.evaluate(() => localStorage.clear());
    await page.goto('/startups/saffron-health/');
    const form = page.locator('form#intro-saffron-health');
    await form.getByLabel(/Why do you want to connect/).fill('Exploring a distribution partnership in KSA.');
    await page.waitForTimeout(2600);
    await form.getByRole('button', { name: 'Send request' }).click();
    await form.locator('[data-form-status] a').click();
    await expect(page.locator('[data-intent]')).toContainText('introduction request');
    await page.getByLabel('Email').fill(email); await page.getByLabel('Password').fill(PW);
    await page.getByRole('button', { name: 'Log in' }).click();
    await expect(page).toHaveURL(/\/startups\/saffron-health\/$/);
    // Draft restored, then submitted with the verified session
    await expect(form.getByLabel(/Why do you want to connect/)).toHaveValue('Exploring a distribution partnership in KSA.');
    await page.waitForTimeout(2600);
    await form.getByRole('button', { name: 'Send request' }).click();
    await expect(form.locator('[data-form-status]')).toContainText(/SR-INT-/);
    // Member-only section now shows member data
    await expect(page.locator('[data-member-slot]')).toContainText('140 clinics');
    await expect(page.locator('[data-member-slot]')).toContainText('limited to verified investors');
  });

  test('unverified email cannot log in; resend issues a fresh link', async ({ page, request }) => {
    const email = `unverified-${uid()}@example.com`;
    await signUp(page, email);
    const first = await lastLink(request, email);
    await login(page, email);
    await expect(page.locator('[data-auth-status]')).toContainText('verify your email');
    await page.locator('[data-auth-status]').getByRole('button', { name: 'Resend verification email' }).click();
    await expect(page.locator('[data-auth-status]')).toContainText('Verification email sent');
    expect(await lastLink(request, email)).not.toBe(first);
  });

  test('wrong password shows a clear error and no session', async ({ page, request }) => {
    const email = `wrongpw-${uid()}@example.com`;
    await signUp(page, email); await verify(page, request, email); await page.waitForURL(/\/app\//);
    await page.evaluate(() => localStorage.clear());
    await page.goto('/login/');
    await page.getByLabel('Email').fill(email); await page.getByLabel('Password').fill('not-the-password');
    await page.getByRole('button', { name: 'Log in' }).click();
    await expect(page.locator('[data-auth-status]')).toContainText('do not match');
    expect(await token(page)).toBeNull();
  });

  test('expired or reused verification link is handled', async ({ page, request }) => {
    const email = `expired-${uid()}@example.com`;
    await signUp(page, email);
    const link = (await lastLink(request, email)).replace(/^https?:\/\/[^/]+/, '');
    await page.goto(link); await page.waitForURL(/\/app\//);
    await page.evaluate(() => localStorage.clear());
    await page.goto(link); // code already used
    await expect(page.locator('[data-auth-status]')).toContainText(/couldn't confirm|expired|invalid/i);
    await page.goto('/auth/callback/?error=access_denied&error_code=otp_expired&error_description=Email+link+is+invalid+or+has+expired');
    await expect(page.locator('[data-auth-status]')).toContainText('expired');
  });

  test('password reset: request → link → new password → login with it', async ({ page, request }) => {
    const email = `reset-${uid()}@example.com`;
    await signUp(page, email); await verify(page, request, email); await page.waitForURL(/\/app\//);
    await page.evaluate(() => localStorage.clear());
    await page.goto('/forgot/');
    await page.getByLabel('Email').fill(email);
    await page.getByRole('button', { name: 'Send reset link' }).click();
    await expect(page.locator('[data-auth-status]')).toContainText('If an account exists');
    const link = (await lastLink(request, email)).replace(/^https?:\/\/[^/]+/, '');
    expect(link).toContain('/reset/');
    await page.goto(link);
    await page.locator('#rs-password').fill('a-brand-new-password');
    await page.getByLabel('Confirm new password').fill('a-brand-new-password');
    await page.getByRole('button', { name: 'Save new password' }).click();
    await expect(page.locator('[data-auth-status]')).toContainText('Password updated');
    await page.evaluate(() => localStorage.clear());
    await page.goto('/login/');
    await page.getByLabel('Email').fill(email); await page.getByLabel('Password').fill('a-brand-new-password');
    await page.getByRole('button', { name: 'Log in' }).click();
    await expect(page).toHaveURL(/\/app\/$/);
  });

  test('forgot password does not reveal whether an account exists', async ({ page }) => {
    await page.goto('/forgot/');
    await page.getByLabel('Email').fill(`nobody-${uid()}@example.com`);
    await page.getByRole('button', { name: 'Send reset link' }).click();
    await expect(page.locator('[data-auth-status]')).toContainText('If an account exists');
  });

  test('expired reset link shows recovery path', async ({ page }) => {
    await page.goto('/reset/?error=access_denied&error_code=otp_expired&error_description=Email+link+is+invalid+or+has+expired');
    await expect(page.locator('[data-auth-status]')).toContainText('expired');
    await expect(page.locator('[data-auth-status] a[href="/forgot/"]')).toBeVisible();
  });

  test('session expiry is detected by the server and sends the user to log in', async ({ page, request }) => {
    const email = `expiry-${uid()}@example.com`;
    await signUp(page, email); await verify(page, request, email); await page.waitForURL(/\/app\//);
    await request.post('/mock-supabase/_test/expire-all');
    await page.goto('/app/');
    await expect(page).toHaveURL(/\/login\/.*reason=expired/, { timeout: 15_000 });
  });
});

test.describe('investor access is earned, not self-selected', () => {
  test('choosing Investor at signup does not unlock investor-only data until verified', async ({ page, request }) => {
    const email = `investor-${uid()}@example.com`;
    await signUp(page, email, 'investor'); await verify(page, request, email);
    await expect(page.locator('[data-role-section="investor"]')).toBeVisible({ timeout: 15_000 });
    await expect(page.locator('[data-role-section="investor"]')).toContainText('needs verification');
    const t = await token(page);
    // Try to self-promote through user-editable metadata: must have no effect on authorization.
    await page.evaluate(async () => {
      const k = Object.keys(localStorage).find((x) => /^sb-.*-auth-token$/.test(x))!; const s = JSON.parse(localStorage.getItem(k)!);
      await fetch('/mock-supabase/auth/v1/user', { method: 'PUT', headers: { apikey: 'test-anon-key', authorization: `Bearer ${s.access_token}`, 'content-type': 'application/json' }, body: JSON.stringify({ data: { investor_verified: true, role: 'investor_verified', sr_admin: true } }) });
    });
    const before = await (await request.get('/api/directory?type=startups&slug=verdant-grid', { headers: { authorization: `Bearer ${t}` } })).json();
    expect(before.viewer.investorVerified).toBe(false);
    expect(before.items[0].investorOnly).toBeNull();
    expect(before.items[0].traction).toContain('62 MW');
    const me = await (await request.get('/api/me', { headers: { authorization: `Bearer ${t}` } })).json();
    expect(me.user.investorVerified).toBe(false);
    // Verification submission is stored and acknowledged
    await page.goto('/investors/#for-investors');
    await page.locator('#inv-verify-firm').fill('Example Angels'); await page.getByLabel('Your role').fill('Partner');
    await page.getByLabel('Firm website or professional profile').fill('https://example.com/angel');
    await page.getByLabel(/Typical cheque size/).selectOption('25k-100k');
    await page.getByLabel('Evidence of investing').fill('Invested in two seed rounds in 2025, references available.');
    await page.waitForTimeout(2600);
    await page.getByRole('button', { name: 'Submit for review' }).click();
    await expect(page.locator('form#inv-verify [data-form-status]')).toContainText(/SR-INV-/);
    // Only an admin-side change (server-controlled app_metadata) grants access
    await request.post('/mock-supabase/_test/verify-investor', { data: { email } });
    const after = await (await request.get('/api/directory?type=startups&slug=verdant-grid', { headers: { authorization: `Bearer ${t}` } })).json();
    expect(after.viewer.investorVerified).toBe(true);
    expect(after.items[0].investorOnly).not.toBeNull();
  });

  test('members see members-only investors; visitors do not', async ({ page, request }) => {
    const email = `member-${uid()}@example.com`;
    await signUp(page, email); await verify(page, request, email); await page.waitForURL(/\/app\//);
    await page.goto('/investors/');
    await expect(page.locator('[data-mode="extra-investors"]')).toContainText('Al Noor Family Office');
    const anon = await request.get('/api/directory?type=investors');
    expect(anon.status()).toBe(401);
  });
});

test.describe('referrals are server-side and cross-user safe', () => {
  test('referral link attributes once, blocks self-referral, qualifies after onboarding', async ({ browser, request }) => {
    const a = await browser.newContext(); const pa = await a.newPage();
    const refEmail = `referrer-${uid()}@example.com`;
    await signUp(pa, refEmail); await verify(pa, request, refEmail); await pa.waitForURL(/\/app\//);
    await pa.goto('/app/');
    const link = await pa.locator('[data-ref-link]').inputValue();
    expect(link).toMatch(/\/signup\/\?ref=[A-F0-9]{8}$/);
    const code = link.split('ref=')[1];
    const ta = await token(pa);
    const self = await request.post('/api/referrals?action=attribute', { headers: { authorization: `Bearer ${ta}` }, data: { code } });
    expect(self.status()).toBe(422);

    const b = await browser.newContext(); const pb = await b.newPage();
    const newEmail = `referred-${uid()}@example.com`;
    await signUp(pb, newEmail, 'founder', `?ref=${code}`); await verify(pb, request, newEmail);
    await pb.waitForURL(/\/app\/onboarding\//);
    await pb.getByRole('button', { name: 'Save and continue' }).click();
    await pb.waitForURL(/\/app\/\?onboarded=1/);
    await expect(pb.locator('[data-ref-counts]')).toContainText('0 referred'); // B's own link
    const tb = await token(pb);
    const again = await request.post('/api/referrals?action=attribute', { headers: { authorization: `Bearer ${tb}` }, data: { code } });
    expect((await again.json()).status).toBe('already_attributed');

    await pa.reload();
    await expect(pa.locator('[data-ref-counts]')).toContainText('1 referred · 1 qualified');
    // B cannot read A's referral data by any parameter: summary is always the caller's own
    const bSummary = await (await request.get('/api/referrals?action=summary', { headers: { authorization: `Bearer ${tb}` } })).json();
    expect(bSummary.code).not.toBe(code);
    await a.close(); await b.close();
  });
});

test.describe('identity provider outage', () => {
  test('login shows an outage message and creates no local session', async ({ page, request }) => {
    await request.post('/mock-supabase/_test/down', { data: { down: true } });
    try {
      await page.goto('/login/');
      await page.getByLabel('Email').fill('someone@example.com'); await page.getByLabel('Password').fill(PW);
      await page.getByRole('button', { name: 'Log in' }).click();
      await expect(page.locator('[data-auth-status]')).toBeVisible();
      await expect(page.locator('[data-auth-status]')).not.toContainText('Welcome');
      expect(await token(page)).toBeNull();
      expect(page.url()).toContain('/login/');
    } finally {
      await request.post('/mock-supabase/_test/down', { data: { down: false } });
    }
  });
});
