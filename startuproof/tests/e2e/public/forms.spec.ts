import { test, expect, type Page } from '@playwright/test';

async function fillContact(page: Page, email = 'founder@example.com') {
  await page.getByLabel('Name').fill('Test Founder');
  await page.getByLabel('Email').fill(email);
  await page.getByLabel('Topic').selectOption('general');
  await page.getByLabel('Message').fill('Testing the contact form end to end.');
  await page.waitForTimeout(2600); // minimum fill time enforced server-side
}

test.describe('forms never show false success', () => {
  test('contact: success only with a server reference', async ({ page }) => {
    await page.goto('/contact/');
    await fillContact(page);
    const [resp] = await Promise.all([page.waitForResponse('**/api/submit'), page.getByRole('button', { name: 'Send message' }).click()]);
    expect(resp.status()).toBe(201);
    const { reference } = await resp.json();
    await expect(page.locator('[data-form-status]')).toContainText(reference);
    await expect(page.locator('[data-form-status]')).toContainText('received');
  });

  test('server error: no success, input kept, retry reuses idempotency key and succeeds once', async ({ page }) => {
    await page.goto('/contact/');
    await fillContact(page);
    const keys: string[] = [];
    let fail = true;
    await page.route('**/api/submit', async (route) => {
      keys.push(JSON.parse(route.request().postData() ?? '{}').idempotencyKey);
      if (fail) { fail = false; return route.fulfill({ status: 500, contentType: 'application/json', body: JSON.stringify({ ok: false, error: 'server_error', message: 'Database unavailable.' }) }); }
      return route.continue();
    });
    await page.getByRole('button', { name: 'Send message' }).click();
    const status = page.locator('[data-form-status]');
    await expect(status).toContainText('Not sent');
    await expect(status).not.toContainText('reference');
    await expect(page.getByLabel('Message')).toHaveValue('Testing the contact form end to end.');
    await status.getByRole('button', { name: 'Try again' }).click();
    await expect(status).toContainText(/SR-CON-/);
    expect(keys).toHaveLength(2);
    expect(keys[0]).toBe(keys[1]);
  });

  test('network failure shows not-sent state', async ({ page }) => {
    await page.goto('/contact/');
    await fillContact(page);
    await page.route('**/api/submit', (r) => r.abort('failed'));
    await page.getByRole('button', { name: 'Send message' }).click();
    await expect(page.locator('[data-form-status]')).toContainText('Not sent');
  });

  test('slow request shows a pending state and disables the button', async ({ page }) => {
    await page.goto('/contact/');
    await fillContact(page);
    await page.route('**/api/submit', async (r) => { await new Promise((res) => setTimeout(res, 1500)); await r.continue(); });
    const btn = page.getByRole('button', { name: 'Send message' });
    await btn.click();
    await expect(page.locator('form#contact')).toHaveAttribute('aria-busy', 'true');
    await expect(page.locator('form#contact button[type="submit"]')).toBeDisabled();
    await expect(page.locator('[data-form-status]')).toContainText(/SR-CON-/, { timeout: 10_000 });
  });

  test('client validation marks invalid fields and sends nothing', async ({ page }) => {
    await page.goto('/contact/');
    let sent = false;
    await page.route('**/api/submit', (r) => { sent = true; return r.continue(); });
    await page.getByRole('button', { name: 'Send message' }).click();
    await expect(page.getByLabel('Name')).toHaveAttribute('aria-invalid', 'true');
    await expect(page.locator('[data-error-for="email"]')).toBeVisible();
    expect(sent).toBe(false);
  });

  test('server validation errors map to fields', async ({ page }) => {
    await page.goto('/pitch/');
    await page.route('**/api/submit', (r) => r.fulfill({ status: 422, contentType: 'application/json', body: JSON.stringify({ ok: false, error: 'validation_failed', message: 'Please correct the highlighted fields.', details: { sector: 'Enter your sector' } }) }));
    const f = page.locator('form#pitch-apply');
    await f.getByLabel('Your name').fill('A Founder'); await f.getByLabel('Email').fill('a@example.com');
    await f.locator('#pitch-apply-company').fill('Example'); await f.getByLabel('Stage').selectOption('seed');
    await f.getByLabel('Sector').fill('Fintech'); await f.getByLabel(/Raising/).selectOption('yes');
    await f.getByLabel('What does the company do?').fill('We make invoices reconcile themselves.');
    await page.getByRole('button', { name: 'Submit application' }).click();
    await expect(page.locator('[data-error-for="sector"]')).toHaveText('Enter your sector');
  });

  test('API rejects honeypot, too-fast and duplicate submissions correctly', async ({ request }) => {
    const run = Math.random().toString(36).slice(2, 12);
    const base = { type: 'contact', fields: { name: 'Bot', email: 'b@example.com', topic: 'general', message: 'Hello there friend' } };
    const hp = await request.post('/api/submit', { data: { ...base, idempotencyKey: `hp-aaaaaaaaaaaaaaaa-${run}`, elapsedMs: 9000, hp: 'http://spam' } });
    expect(hp.status()).toBe(400);
    const fast = await request.post('/api/submit', { data: { ...base, idempotencyKey: `fast-aaaaaaaaaaaaaa-${run}`, elapsedMs: 200 } });
    expect(fast.status()).toBe(429);
    const a = await request.post('/api/submit', { data: { ...base, idempotencyKey: `dupe-aaaaaaaaaaaaaa-${run}`, elapsedMs: 9000 } });
    const b = await request.post('/api/submit', { data: { ...base, idempotencyKey: `dupe-aaaaaaaaaaaaaa-${run}`, elapsedMs: 9000 } });
    expect(a.status()).toBe(201); expect(b.status()).toBe(200);
    expect((await a.json()).reference).toBe((await b.json()).reference);
    const bad = await request.post('/api/submit', { data: { type: 'contact', idempotencyKey: `bad-aaaaaaaaaaaaaaa-${run}`, elapsedMs: 9000, fields: { name: 'X', email: 'nope' } } });
    expect(bad.status()).toBe(422);
    const unknown = await request.post('/api/submit', { data: { ...base, type: 'nope', idempotencyKey: `unk-aaaaaaaaaaaaaaa-${run}`, elapsedMs: 9000 } });
    expect(unknown.status()).toBe(400);
  });
});

test.describe('filters keep state in shareable URLs', () => {
  test('Radar type filter and keyword', async ({ page }) => {
    await page.goto('/radar/?type=equity_round');
    await expect(page.getByLabel('Type')).toHaveValue('equity_round');
    const visible = page.locator('[data-radar-results] li:visible');
    expect(await visible.count()).toBeGreaterThan(0);
    for (const k of await visible.evaluateAll((els) => els.map((e) => (e as HTMLElement).dataset.kind))) expect(k).toBe('equity_round');
    await page.getByLabel('Keyword').fill('zzzz-no-match');
    await expect(page.locator('[data-radar-empty]')).toBeVisible();
    await expect(page).toHaveURL(/q=zzzz-no-match/);
  });

  test('UAE edition contains no unrelated or Egypt-only stories', async ({ page }) => {
    await page.goto('/radar/uae/');
    const text = await page.locator('[data-radar-results]').innerText();
    for (const bad of ['Al Sadr', 'Ronaldo', 'Gaza', 'diesel', 'EBRD', 'Cairo', 'Beltone']) expect(text).not.toContain(bad);
  });

  test('directory filter by sector', async ({ page }) => {
    await page.goto('/startups/?sector=Fintech');
    await expect(page.locator('[data-dir-item]:visible')).toHaveCount(1);
    await expect(page.locator('[data-dir-item]:visible')).toContainText('Nimbus Ledger');
  });
});
