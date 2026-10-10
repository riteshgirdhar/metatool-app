"""Renders the full A4 brochure: core pages from brochure.html plus extra pages from brochure_extra.py."""
import base64, io, os, re, subprocess, sys, tempfile, pathlib, qrcode
import brochure_extra as X

HERE = pathlib.Path(__file__).resolve().parent
PHOTOS = HERE.parent / "photos"
out = pathlib.Path(sys.argv[1]).resolve()

html = (HERE / "brochure.html").read_text()
head, body = html.split("<body>", 1)
body = body.split("</body>")[0]
core = re.findall(r"<section class=\"page.*?</section>", body, flags=re.S)
assert len(core) == 12, len(core)
core = [re.sub(r'(<div class="eyebrow"[^>]*>)\d\d · ', r"\1", c) for c in core]
core = [re.sub(r"startuproof\.com · \d\d", 'startuproof.com · <span class="pn"></span>', c) for c in core]

pages = [core[0], X.p_glance(), core[1], X.p_struggle(), X.p_evidence(), X.p_uae(), X.p_uae_founders(),
         core[2], X.p_pillars_sectors(), X.p_personas(), core[3], X.p_stages(0, 3, "From idea to a first offer."),
         X.p_stages(3, 6, "From first customers to scale — and capital where it fits."),
         X.p_metrics_funding(), X.p_ladder_readiness(), X.p_os_screens(), X.p_os_engine(), X.p_os_priorities(),
         core[4], X.p_rhythm_mentoring(), core[5], X.p_curriculum_catalogue(), core[6], core[7], X.p_partners_detail(),
         core[8], X.p_economics(), X.p_pilot_kpis(), core[9], X.p_path_risks(), core[10], X.p_faq(), X.p_glossary_sources(), core[11]]

doc = "\n".join(pages)


def photo_sub(m):
    key, hmm, fallback = m.group(1), m.group(2), m.group(3)
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        p = PHOTOS / f"{key}{ext}"
        if p.exists():
            mime = "image/png" if ext == ".png" else "image/webp" if ext == ".webp" else "image/jpeg"
            data = base64.b64encode(p.read_bytes()).decode()
            return f'<img src="data:{mime};base64,{data}" style="width:100%;height:{hmm}mm;object-fit:cover;display:block" alt="">'
    return fallback


doc = re.sub(r"<!--PHOTO:(\w+):(\d+)-->(.*?)<!--/PHOTO-->", photo_sub, doc, flags=re.S)
q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=20, border=2)
q.add_data("https://startuproof.com"); q.make(fit=True)
buf = io.BytesIO(); q.make_image(fill_color="#10213B", back_color="white").save(buf, format="PNG")
doc = doc.replace("{{QR}}", "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode())
head = head.replace("</style>", "  body { counter-reset: pg; } .page { counter-increment: pg; } .pn::before { content: counter(pg, decimal-leading-zero); } table.compact { font-size: 9.1pt; } table.compact td, table.compact th { padding: 1.5mm 2.6mm; }\n</style>")
head = head.replace("<title>Startup Roof — Project Brochure</title>", "<title>Startup Roof — Full Brochure</title>")
full = head + "<body>\n" + doc + "\n</body>\n</html>\n"
tmpdir = pathlib.Path(tempfile.mkdtemp())
tmp = tmpdir / "brochure_full.html"
tmp.write_text(full)
if os.environ.get("KEEP_HTML"):
    (HERE / "_brochure_full_preview.html").write_text(full)
js = f"""const {{chromium}} = require('playwright');
(async () => {{ const b = await chromium.launch(); const p = await b.newPage();
await p.goto('file://{tmp}'); await p.evaluate(() => document.fonts.ready);
await p.pdf({{path: '{out}', format: 'A4', printBackground: true, preferCSSPageSize: true}}); await b.close(); }})();"""
subprocess.run(["node", "-e", js], check=True, env={**os.environ, "NODE_PATH": "/opt/node22/lib/node_modules"})
print("saved", out, "pages:", len(pages), "->", tmp)
