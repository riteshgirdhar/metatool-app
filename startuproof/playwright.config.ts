import { defineConfig, devices } from '@playwright/test';

const executablePath = process.env.PW_CHROMIUM ?? '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const launchOptions = { executablePath };

export default defineConfig({
  testDir: 'tests/e2e',
  outputDir: 'test-results',
  timeout: 45_000,
  fullyParallel: true,
  workers: 4,
  reporter: [['list'], ['json', { outputFile: 'reports/e2e-results.json' }]],
  use: { trace: 'retain-on-failure', launchOptions },
  webServer: [
    { command: 'node scripts/serve.mjs', env: { PORT: '4321', DIST: 'dist' }, url: 'http://localhost:4321/api/health', reuseExistingServer: true },
    { command: 'node scripts/serve.mjs', env: { PORT: '4322', DIST: 'dist-e2e', SR_MOCK_SUPABASE: '1' }, url: 'http://localhost:4322/api/health', reuseExistingServer: true },
  ],
  projects: [
    { name: 'public-desktop', testMatch: /public\/.*\.spec\.ts/, use: { ...devices['Desktop Chrome'], baseURL: 'http://localhost:4321' } },
    { name: 'public-mobile', testMatch: /public\/(nav|forms)\.spec\.ts/, use: { ...devices['Pixel 7'], baseURL: 'http://localhost:4321' } },
    { name: 'journeys', fullyParallel: false, testMatch: /journeys\/.*\.spec\.ts/, use: { ...devices['Desktop Chrome'], baseURL: 'http://localhost:4322' } },
  ],
});
