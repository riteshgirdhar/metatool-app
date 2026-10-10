"""Renders src/brochure.html to an A4 PDF with Playwright/Chromium, embedding a QR code."""
import base64, io, subprocess, sys, tempfile, pathlib, qrcode
src = pathlib.Path(__file__).with_name("brochure.html")
out = pathlib.Path(sys.argv[1]).resolve()
q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=20, border=2)
q.add_data("https://startuproof.com"); q.make(fit=True)
buf = io.BytesIO(); q.make_image(fill_color="#10213B", back_color="white").save(buf, format="PNG")
html = src.read_text().replace("{{QR}}", "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode())
tmp = pathlib.Path(tempfile.mkdtemp()) / "brochure.html"; tmp.write_text(html)
js = f"""const {{chromium}} = require('playwright');
(async () => {{ const b = await chromium.launch(); const p = await b.newPage();
await p.goto('file://{tmp}'); await p.evaluate(() => document.fonts.ready);
await p.pdf({{path: '{out}', format: 'A4', printBackground: true, preferCSSPageSize: true}}); await b.close(); }})();"""
subprocess.run(["node", "-e", js], check=True, env={**__import__("os").environ, "NODE_PATH": "/opt/node22/lib/node_modules"})
print("saved", out)
