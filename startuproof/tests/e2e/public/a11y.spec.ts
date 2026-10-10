import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import { writeFileSync, mkdirSync } from 'node:fs';
import { TEMPLATES } from '../pages';

const results: Record<string, { violations: { id: string; impact: string | null; nodes: number }[] }> = {};

test.describe('axe WCAG 2.2 AA (automated subset)', () => {
  for (const [name, url] of Object.entries(TEMPLATES)) {
    test(name, async ({ page }) => {
      await page.goto(url);
      await page.waitForLoadState('networkidle');
      const r = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa', 'best-practice']).analyze();
      results[name] = { violations: r.violations.map((v) => ({ id: v.id, impact: v.impact ?? null, nodes: v.nodes.length })) };
      mkdirSync('reports/axe', { recursive: true });
      writeFileSync(`reports/axe/${name}.json`, JSON.stringify(results[name], null, 2));
      const serious = r.violations.filter((v) => v.impact === 'serious' || v.impact === 'critical' || v.impact === 'moderate');
      expect(serious.map((v) => `${v.id}: ${v.nodes.map((n) => n.target.join(' ')).slice(0, 3).join(', ')}`)).toEqual([]);
    });
  }
});

test('reduced motion disables animation', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto('/app/');
  const dur = await page.evaluate(() => getComputedStyle(document.querySelector('.skeleton') ?? document.body).animationDuration);
  expect(['0.01ms', '1e-05s', '0s']).toContain(dur);
});

test('200% zoom (640px CSS viewport) keeps content readable without horizontal scroll', async ({ page }) => {
  for (const url of ['/', '/radar/', '/investors/', '/festival/', '/contact/']) {
    await page.setViewportSize({ width: 640, height: 400 });
    await page.goto(url);
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    expect(overflow, url).toBeLessThanOrEqual(0);
  }
});

test('320px reflow stress test', async ({ page }) => {
  for (const url of Object.values(TEMPLATES)) {
    await page.setViewportSize({ width: 320, height: 640 });
    await page.goto(url);
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    expect(overflow, url).toBeLessThanOrEqual(0);
  }
});

test('focus is visible on keyboard navigation', async ({ page }) => {
  await page.goto('/');
  await page.keyboard.press('Tab'); // skip link
  await expect(page.locator('.skip-link')).toBeFocused();
  const outline = await page.evaluate(() => getComputedStyle(document.activeElement!).outlineStyle);
  expect(outline).not.toBe('none');
  await page.keyboard.press('Enter');
  await expect(page.locator('#main')).toBeFocused();
});
