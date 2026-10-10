import { test, expect } from '@playwright/test';

/** Production build without identity-provider config: there must be no local fallback. */
test.describe('auth unavailable (no identity provider configured)', () => {
  test('signup is disabled and nothing is stored locally', async ({ page }) => {
    await page.goto('/signup/');
    await expect(page.locator('[data-auth-status]')).toContainText('temporarily unavailable');
    await expect(page.getByRole('button', { name: 'Create account' })).toBeDisabled();
    await expect(page.getByLabel('Password')).toBeDisabled();
    const storage = await page.evaluate(() => JSON.stringify({ ...localStorage }) + JSON.stringify({ ...sessionStorage }));
    expect(storage).not.toMatch(/password/i);
  });

  test('login is disabled; no demo or local accounts', async ({ page }) => {
    await page.goto('/login/');
    await expect(page.getByRole('button', { name: 'Log in' })).toBeDisabled();
    await expect(page.locator('body')).not.toContainText(/demo admin|demo login/i);
  });

  test('member area explains unavailability instead of faking a session', async ({ page }) => {
    await page.goto('/app/');
    await expect(page.locator('[data-app-unavailable]')).toBeVisible();
    await expect(page.locator('[data-app-ready]')).toBeHidden();
  });

  test('protected APIs refuse without a verified session', async ({ request }) => {
    for (const p of ['/api/me', '/api/directory?type=startups', '/api/referrals?action=summary']) {
      const r = await request.get(p);
      expect([401, 503]).toContain(r.status());
      const body = await r.json();
      expect(body.ok).toBe(false);
      expect(JSON.stringify(body)).not.toContain('traction');
    }
    const forged = await request.get('/api/directory?type=startups', { headers: { authorization: 'Bearer forged.token.value' } });
    expect([401, 503]).toContain(forged.status());
  });

  test('gated action keeps the user\'s message and links to login with next', async ({ page }) => {
    await page.goto('/startups/nimbus-ledger/');
    const form = page.locator('form#intro-nimbus-ledger');
    await form.getByLabel(/Why do you want to connect/).fill('We would like to explore a pilot together soon.');
    await page.waitForTimeout(2600);
    await form.getByRole('button', { name: 'Send request' }).click();
    const link = form.locator('[data-form-status] a');
    await expect(link).toHaveAttribute('href', /\/login\/\?next=%2Fstartups%2Fnimbus-ledger%2F&intent=intro-request/);
    await expect(form.getByLabel(/Why do you want to connect/)).toHaveValue('We would like to explore a pilot together soon.');
  });

  test('member-only sections show a login prompt, never private data', async ({ page }) => {
    await page.goto('/startups/nimbus-ledger/');
    const slot = page.locator('[data-member-slot]');
    await expect(slot).toContainText('Log in to view');
    const html = await page.content();
    expect(html).not.toContain('320 paying SMEs');
    expect(html).not.toContain('Wafeq');
  });

  test('TV legacy hash links route to path URLs', async ({ page }) => {
    await page.goto('/tv/#show=the-raise');
    await expect(page).toHaveURL(/\/tv\/shows\/the-raise\/$/);
    await page.goto('/tv/#/watch/office-hours/e2-pricing');
    await expect(page).toHaveURL(/\/tv\/shows\/office-hours\/e2-pricing\/$/);
  });

  test('episode numbering is sequential and pages show an unavailable state', async ({ page }) => {
    await page.goto('/tv/shows/the-raise/');
    const labels = await page.locator('ol.item-list a').allInnerTexts();
    expect(labels.map((l) => l.split(':')[0])).toEqual(['E1', 'E2', 'E3']);
    await page.goto('/tv/shows/the-raise/e3-term-sheet/');
    await expect(page.locator('.player')).toContainText('not available yet');
    expect(await page.locator('video, iframe').count()).toBe(0);
  });

  test('calendar files are not offered for provisional dates', async ({ page, request }) => {
    await page.goto('/opportunities/founder-festival-pitch-studio-2027/');
    await expect(page.getByText('calendar file will be available once the deadline is confirmed')).toBeVisible();
    expect((await request.get('/opportunities/founder-festival-pitch-studio-2027.ics')).status()).toBe(404);
  });
});
