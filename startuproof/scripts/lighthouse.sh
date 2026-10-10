#!/usr/bin/env bash
# Lab Lighthouse runs (mobile + desktop) for representative pages against the local preview server on :4321.
# Usage: node scripts/serve.mjs &  then  bash scripts/lighthouse.sh [base-url]
set -euo pipefail
export CHROME_PATH="${PW_CHROMIUM:-/opt/pw-browsers/chromium-1194/chrome-linux/chrome}"
BASE="${1:-http://localhost:4321}"
CHROME="${PW_CHROMIUM:-/opt/pw-browsers/chromium-1194/chrome-linux/chrome}"
OUT="reports/lighthouse"; mkdir -p "$OUT"
PAGES=("/" "/radar/" "/radar/item/erad-22m-series-a-mevp/" "/academy/guides/unit-economics-basics/" "/startups/" "/festival/" "/contact/")
for p in "${PAGES[@]}"; do
  name=$(echo "$p" | sed 's#^/##; s#/$##; s#/#_#g'); name=${name:-home}
  for form in mobile desktop; do
    flags=(--quiet --chrome-path="$CHROME" --chrome-flags="--headless=new --no-sandbox" --output=json --output-path="$OUT/$name.$form.json" --only-categories=performance,accessibility,best-practices,seo)
    [ "$form" = desktop ] && flags+=(--preset=desktop)
    npx lighthouse "$BASE$p" "${flags[@]}" || echo "lighthouse failed for $p ($form)"
  done
done
node -e '
const fs=require("fs");const dir="reports/lighthouse";const rows=[];
for(const f of fs.readdirSync(dir).filter(f=>f.endsWith(".json")).sort()){const r=JSON.parse(fs.readFileSync(`${dir}/${f}`));const c=r.categories;const a=r.audits;
rows.push({page:f.replace(/\.(mobile|desktop)\.json$/,""),form:f.includes(".mobile.")?"mobile":"desktop",perf:Math.round(c.performance.score*100),a11y:Math.round(c.accessibility.score*100),bp:Math.round(c["best-practices"].score*100),seo:Math.round(c.seo.score*100),lcp:a["largest-contentful-paint"].displayValue,cls:a["cumulative-layout-shift"].displayValue,tbt:a["total-blocking-time"].displayValue,bytes:Math.round(a["total-byte-weight"].numericValue/1024)+" KiB"});}
fs.writeFileSync("reports/lighthouse-summary.json",JSON.stringify(rows,null,2));console.table(rows);'
