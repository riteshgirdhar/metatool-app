// @ts-check
import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://startuproof.com',
  output: 'static',
  trailingSlash: 'always',
  build: { format: 'directory', inlineStylesheets: 'auto' },
  compressHTML: true,
  prefetch: false,
  devToolbar: { enabled: false },
  vite: { build: { cssMinify: true } },
});
