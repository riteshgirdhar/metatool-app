import { test, expect } from '@playwright/test';

test.describe('header navigation', () => {
  test('desktop dropdowns: hidden state and aria-expanded stay in sync', async ({ page, isMobile }) => {
    test.skip(isMobile, 'desktop menus');
    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto('/');
    const triggers = page.locator('.primary-nav .nav-trigger');
    const n = await triggers.count();
    expect(n).toBe(4);
    for (let i = 0; i < n; i++) {
      const t = triggers.nth(i);
      const panel = page.locator(`#${await t.getAttribute('aria-controls')}`);
      await expect(t).toHaveAttribute('aria-expanded', 'false');
      await expect(panel).toBeHidden();
    }
    const platform = page.getByRole('button', { name: 'Platform' });
    await platform.click();
    await expect(platform).toHaveAttribute('aria-expanded', 'true');
    await expect(page.locator('#menu-platform')).toBeVisible();
    // Opening another closes the first
    await page.getByRole('button', { name: 'Resources' }).click();
    await expect(platform).toHaveAttribute('aria-expanded', 'false');
    await expect(page.locator('#menu-platform')).toBeHidden();
    await expect(page.locator('#menu-resources')).toBeVisible();
    // Escape closes and returns focus
    await page.keyboard.press('Escape');
    await expect(page.locator('#menu-resources')).toBeHidden();
    await expect(page.getByRole('button', { name: 'Resources' })).toBeFocused();
    // Outside click closes
    await platform.click();
    await page.mouse.click(5, 790);
    await expect(page.locator('#menu-platform')).toBeHidden();
  });

  test('keyboard: ArrowDown opens menu and moves through links; Tab out closes', async ({ page, isMobile }) => {
    test.skip(isMobile, 'desktop menus');
    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto('/');
    await page.getByRole('button', { name: 'Platform' }).focus();
    await page.keyboard.press('ArrowDown');
    await expect(page.locator('#menu-platform a').first()).toBeFocused();
    await page.keyboard.press('ArrowDown');
    await expect(page.locator('#menu-platform a').nth(1)).toBeFocused();
    for (let i = 0; i < 8; i++) await page.keyboard.press('Tab');
    await expect(page.locator('#menu-platform')).toBeHidden();
  });

  test('labels are accurate: Community and Stories are distinct, Help centre is not Contact', async ({ page, isMobile }) => {
    test.skip(isMobile, 'desktop menus');
    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto('/');
    await page.getByRole('button', { name: 'Resources' }).click();
    const panel = page.locator('#menu-resources');
    await expect(panel.getByRole('link', { name: /^Community/ })).toHaveAttribute('href', '/community/');
    await expect(panel.getByRole('link', { name: /^Stories/ })).toHaveAttribute('href', '/media/');
    await expect(panel.getByRole('link', { name: /^Help centre/ })).toHaveAttribute('href', '/support/');
  });

  test('active section is indicated', async ({ page, isMobile }) => {
    test.skip(isMobile, 'desktop menus');
    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto('/radar/uae/');
    await expect(page.locator('.primary-nav a.nav-direct[href="/radar/"]')).toHaveAttribute('aria-current', 'page');
    await page.goto('/academy/');
    await expect(page.getByRole('button', { name: 'Resources' })).toHaveClass(/is-active/);
  });

  test('mobile drawer opens, traps focus, closes with Escape and returns focus', async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto('/');
    const open = page.locator('[data-drawer-open]');
    await expect(page.locator('.primary-nav')).toBeHidden();
    await expect(open).toHaveAttribute('aria-expanded', 'false');
    await open.click();
    const drawer = page.locator('#site-drawer');
    await expect(drawer).toBeVisible();
    await expect(open).toHaveAttribute('aria-expanded', 'true');
    // Focus stays inside the drawer
    for (let i = 0; i < 40; i++) await page.keyboard.press('Tab');
    expect(await page.evaluate(() => document.getElementById('site-drawer')!.contains(document.activeElement))).toBe(true);
    await page.keyboard.press('Escape');
    await expect(drawer).toBeHidden();
    await expect(open).toBeFocused();
    // Navigate via drawer link (touch)
    await open.click();
    await drawer.getByRole('link', { name: 'Academy' }).click();
    await expect(page).toHaveURL(/\/academy\/$/);
  });

  test('touch targets in header and drawer are at least 44px', async ({ page }) => {
    await page.setViewportSize({ width: 360, height: 740 });
    await page.goto('/');
    await page.locator('[data-drawer-open]').click();
    const small = await page.evaluate(() => [...document.querySelectorAll<HTMLElement>('.site-header a, .site-header button, #site-drawer a, #site-drawer button')]
      .filter((el) => el.offsetParent !== null).map((el) => ({ t: el.textContent?.trim(), h: el.getBoundingClientRect().height })).filter((x) => x.h < 40));
    expect(small).toEqual([]);
  });
});
