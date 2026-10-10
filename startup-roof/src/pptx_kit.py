"""Small drawing kit on top of python-pptx so every visual stays an editable shape."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from lxml import etree

NAVY = "10213B"
BLUE = "1765D1"
PALE = "EDF4FE"
WHITE = "FFFFFF"
TEXT = "253650"
MUTED = "61738A"
LINE = "D5E2F3"
MID = "4F8BE0"      # lighter blue for tints on navy
DEEP = "1A3358"     # navy tint for panels on navy
FONT = "Inter"

W, H = 13.333, 7.5
ML = 0.65  # left margin


def rgb(h):
    return RGBColor.from_string(h)


def new_prs():
    prs = Presentation()
    prs.slide_width = Inches(W)
    prs.slide_height = Inches(H)
    return prs


def blank(prs, bg=WHITE):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bgfill = s.background.fill
    bgfill.solid()
    bgfill.fore_color.rgb = rgb(bg)
    return s


def strip_style(sh):
    st = sh._element.find(qn("p:style"))
    if st is not None:
        sh._element.remove(st)


def rect(s, x, y, w, h, fill=None, line=None, lw=0.75, shape=MSO_SHAPE.RECTANGLE, radius=None, name=None):
    sh = s.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill:
        sh.fill.solid()
        sh.fill.fore_color.rgb = rgb(fill)
    else:
        sh.fill.background()
    if line:
        sh.line.color.rgb = rgb(line)
        sh.line.width = Pt(lw)
    else:
        sh.line.fill.background()
    if radius is not None and len(sh.adjustments) > 0:
        sh.adjustments[0] = radius
    sh.shadow.inherit = False
    strip_style(sh)
    if name:
        sh.name = name
    tf = sh.text_frame
    tf.margin_left = tf.margin_right = Inches(0.08)
    tf.margin_top = tf.margin_bottom = Inches(0.04)
    return sh


def _apply_run(run, size, color, bold, italic=False, font=FONT, spacing=None):
    f = run.font
    f.name = font
    f.size = Pt(size)
    f.bold = bold
    f.italic = italic
    f.color.rgb = rgb(color)
    if spacing is not None:
        rPr = run._r.get_or_add_rPr()
        rPr.set("spc", str(int(spacing * 100)))


def fill_tf(tf, paras, size=14, color=TEXT, bold=False, align=PP_ALIGN.LEFT,
            anchor=MSO_ANCHOR.TOP, spacing=None, line=1.15, after=0, font=FONT, italic=False):
    """paras: list of paragraphs. Each paragraph is a str or a list of runs.
    A run is a str or (str, dict(size,color,bold,italic,spacing))."""
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    if isinstance(paras, str):
        paras = [paras]
    first = True
    for p in paras:
        para = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        popts = {}
        if isinstance(p, dict):
            popts = p
            p = p["runs"]
        para.alignment = popts.get("align", align)
        para.line_spacing = popts.get("line", line)
        para.space_after = Pt(popts.get("after", after))
        if "before" in popts:
            para.space_before = Pt(popts["before"])
        runs = [p] if isinstance(p, (str, tuple)) else p
        for r in runs:
            if isinstance(r, str):
                r = (r, {})
            t, o = r
            run = para.add_run()
            run.text = t
            _apply_run(run, o.get("size", popts.get("size", size)), o.get("color", popts.get("color", color)),
                       o.get("bold", popts.get("bold", bold)), o.get("italic", italic), font,
                       o.get("spacing", popts.get("spacing", spacing)))
    return tf


def text(s, x, y, w, h, paras, size=14, color=TEXT, bold=False, align=PP_ALIGN.LEFT,
         anchor=MSO_ANCHOR.TOP, spacing=None, line=1.15, after=0, margin=0.0, name=None, italic=False):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.margin_left = tf.margin_right = Inches(margin)
    tf.margin_top = tf.margin_bottom = Inches(0)
    tf.auto_size = None
    fill_tf(tf, paras, size, color, bold, align, anchor, spacing, line, after, italic=italic)
    if name:
        tb.name = name
    return tb


def shape_text(sh, paras, size=14, color=TEXT, bold=False, align=PP_ALIGN.CENTER,
               anchor=MSO_ANCHOR.MIDDLE, line=1.1, after=0, margin=0.08, spacing=None):
    tf = sh.text_frame
    tf.margin_left = tf.margin_right = Inches(margin)
    tf.margin_top = tf.margin_bottom = Inches(0.03)
    fill_tf(tf, paras, size, color, bold, align, anchor, spacing, line, after)
    return sh


def line(s, x1, y1, x2, y2, color=LINE, w=1.0, arrow=False, dash=False):
    c = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = rgb(color)
    c.line.width = Pt(w)
    strip_style(c)
    ln = c.line._get_or_add_ln()
    if dash:
        d = etree.SubElement(ln, qn("a:prstDash"))
        d.set("val", "dash")
    if arrow:
        tail = etree.SubElement(ln, qn("a:tailEnd"))
        tail.set("type", "triangle")
        tail.set("w", "med")
        tail.set("len", "med")
    return c


def polyline(s, pts, color=WHITE, w=3.0, closed=False, fill=None):
    fb = s.shapes.build_freeform(Inches(pts[0][0]), Inches(pts[0][1]), scale=1.0)
    fb.add_line_segments([(Inches(a), Inches(b)) for a, b in pts[1:]], close=closed)
    sh = fb.convert_to_shape()
    if fill:
        sh.fill.solid()
        sh.fill.fore_color.rgb = rgb(fill)
    else:
        sh.fill.background()
    if w:
        sh.line.color.rgb = rgb(color)
        sh.line.width = Pt(w)
    else:
        sh.line.fill.background()
    sh.shadow.inherit = False
    strip_style(sh)
    return sh


def wordmark(s, x, y, size=12, dark=False, align=PP_ALIGN.LEFT, w=3.0):
    c1 = WHITE if dark else NAVY
    c2 = MID if dark else BLUE
    return text(s, x, y, w, size / 72 * 1.4,
                [[("STARTUP", {"color": c1, "bold": True, "spacing": size * 0.12}),
                  (" ROOF", {"color": c2, "bold": True, "spacing": size * 0.12})]],
                size=size, align=align)


def pill(s, x, y, label, fill=PALE, color=BLUE, size=9, w=None, line_color=None):
    w = w or (0.3 + len(label) * size * 0.0098)
    sh = rect(s, x, y, w, 0.28, fill=fill, line=line_color, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
    shape_text(sh, [[(label, {"bold": True, "spacing": 0.8})]], size=size, color=color, margin=0.06)
    sh.text_frame.word_wrap = False
    return sh


def header(s, num, section, title, dark=False, title_size=28, tag=None, title_w=11.6):
    ec = MID if dark else BLUE
    tc = WHITE if dark else NAVY
    text(s, ML, 0.48, 8, 0.3, [[(f"{num:02d}", {"bold": True}), ("   " + section.upper(), {"bold": True})]],
         size=10, color=ec, spacing=1.5)
    text(s, ML, 0.82, title_w, 1.1, title, size=title_size, color=tc, bold=True, line=1.02)
    if tag:
        tag_w = 0.3 + len(tag) * 9 * 0.0098
        pill(s, W - ML - tag_w, 0.44, tag, fill=(DEEP if dark else PALE), color=(WHITE if dark else BLUE))


def footer(s, n, dark=False):
    c = "8EA0B8" if dark else MUTED
    wordmark(s, ML, 7.02, size=8.5, dark=dark)
    text(s, W - ML - 3, 7.02, 3, 0.2, [[("startuproof.com", {}), (f"     {n:02d}", {"bold": True})]],
         size=8.5, color=c, align=PP_ALIGN.RIGHT)


def notes(s, body):
    s.notes_slide.notes_text_frame.text = body


def table(s, x, y, w, h, data, col_w, header_fill=NAVY, header_color=WHITE, size=11.5, header_size=11,
          row_fills=(WHITE, PALE), first_col_bold=True, first_col_color=NAVY, row_h=None):
    rows, cols = len(data), len(data[0])
    gt = s.shapes.add_table(rows, cols, Inches(x), Inches(y), Inches(w), Inches(h))
    tbl = gt.table
    # strip default style banding
    tblPr = tbl._tbl.tblPr
    tblPr.set("firstRow", "0")
    tblPr.set("bandRow", "0")
    for i, cw in enumerate(col_w):
        tbl.columns[i].width = Inches(cw)
    for r in range(rows):
        if row_h:
            tbl.rows[r].height = Inches(row_h[r] if isinstance(row_h, (list, tuple)) else row_h)
        for c in range(cols):
            cell = tbl.cell(r, c)
            cell.fill.solid()
            if r == 0:
                cell.fill.fore_color.rgb = rgb(header_fill)
            else:
                cell.fill.fore_color.rgb = rgb(row_fills[(r - 1) % len(row_fills)])
            cell.margin_left = cell.margin_right = Inches(0.12)
            cell.margin_top = Inches(0.06)
            cell.margin_bottom = Inches(0.06)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            val = data[r][c]
            if r == 0:
                fill_tf(cell.text_frame, [[(val, {"bold": True, "spacing": 0.6})]], size=header_size, color=header_color)
            elif c == 0 and first_col_bold:
                fill_tf(cell.text_frame, val, size=size, color=first_col_color, bold=True)
            else:
                fill_tf(cell.text_frame, val, size=size, color=TEXT)
    return gt


# ---------------------------------------------------------------- extended kit (full edition)
import os
import random
import tempfile
from pathlib import Path as _Path
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION, XL_TICK_LABEL_POSITION

MODE = {"auto": False}
PHOTO_DIR = _Path(__file__).resolve().parent.parent / "photos"
PHOTOS_USED = []


def eyebrow_num(n):
    return "" if MODE["auto"] else f"{n:02d}   "


_orig_header = header
_orig_footer = footer


def header(s, num, section, title, dark=False, title_size=28, tag=None, title_w=11.6):  # noqa: F811
    if not MODE["auto"]:
        return _orig_header(s, num, section, title, dark, title_size, tag, title_w)
    ec = MID if dark else BLUE
    tc = WHITE if dark else NAVY
    text(s, ML, 0.48, 9, 0.3, [[(section.upper(), {"bold": True})]], size=10, color=ec, spacing=1.5)
    text(s, ML, 0.82, title_w, 1.1, title, size=title_size, color=tc, bold=True, line=1.02)
    if tag:
        tag_w = 0.3 + len(tag) * 9 * 0.0098
        pill(s, W - ML - tag_w, 0.44, tag, fill=(DEEP if dark else PALE), color=(WHITE if dark else BLUE))


def _slidenum_run(paragraph, size, color, bold=True):
    fld = etree.SubElement(paragraph._p, qn("a:fld"))
    fld.set("id", "{B6F15528-21DE-4FAA-801E-634DDDAF4B2B}")
    fld.set("type", "slidenum")
    rPr = etree.SubElement(fld, qn("a:rPr"))
    rPr.set("lang", "en-GB")
    rPr.set("sz", str(int(size * 100)))
    rPr.set("b", "1" if bold else "0")
    sf = etree.SubElement(rPr, qn("a:solidFill"))
    c = etree.SubElement(sf, qn("a:srgbClr"))
    c.set("val", color)
    lat = etree.SubElement(rPr, qn("a:latin"))
    lat.set("typeface", FONT)
    t = etree.SubElement(fld, qn("a:t"))
    t.text = "‹#›"


def footer(s, n=None, dark=False):  # noqa: F811
    if not MODE["auto"]:
        return _orig_footer(s, n, dark)
    c = "8EA0B8" if dark else MUTED
    wordmark(s, ML, 7.02, size=8.5, dark=dark)
    tb = text(s, W - ML - 3, 7.02, 3, 0.2, [[("startuproof.com     ", {})]], size=8.5, color=c, align=PP_ALIGN.RIGHT)
    _slidenum_run(tb.text_frame.paragraphs[0], 8.5, c)


def photo(s, key, x, y, w, h, fallback=None, **fb_kwargs):
    """Places photos/<key>.jpg|png cropped to fill the box; otherwise draws the fallback graphic."""
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        p = PHOTO_DIR / f"{key}{ext}"
        if p.exists():
            from PIL import Image
            im = Image.open(p).convert("RGB")
            tr = w / h
            iw, ih = im.size
            if iw / ih > tr:
                nw = int(ih * tr)
                im = im.crop(((iw - nw) // 2, 0, (iw - nw) // 2 + nw, ih))
            else:
                nh = int(iw / tr)
                im = im.crop((0, (ih - nh) // 2, iw, (ih - nh) // 2 + nh))
            im.thumbnail((2400, 2400))
            tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
            im.save(tmp.name, quality=86)
            PHOTOS_USED.append(key)
            return s.shapes.add_picture(tmp.name, Inches(x), Inches(y), Inches(w), Inches(h))
    if fallback:
        return fallback(s, x, y, w, h, **fb_kwargs)


def skyline(s, x, y, w, h, bg=NAVY, fg=("1A3358", "1C3D6B", "1F4A85"), accent=BLUE, seed=7, sun=True):
    """Abstract skyline with a tall spire — a restrained nod to Dubai, drawn as editable shapes."""
    rect(s, x, y, w, h, fill=bg)
    rnd = random.Random(seed)
    base = y + h
    if sun:
        r = h * 0.22
        rect(s, x + w * 0.70, y + h * 0.16, r, r, fill="1C3D6B", shape=MSO_SHAPE.OVAL)
    cx = x + 0.04 * w
    spire_at = x + w * 0.56
    while cx < x + w - 0.1:
        bw = rnd.uniform(0.045, 0.09) * w
        if cx + bw > x + w:
            bw = x + w - cx
        if abs(cx - spire_at) < 0.05 * w:
            # spire: stacked tapered blocks + needle
            sw = 0.06 * w
            levels = [(1.0, 0.30), (0.72, 0.22), (0.48, 0.16), (0.28, 0.12)]
            yy = base
            for frac, hh in levels:
                bh = hh * h
                bww = sw * frac
                rect(s, cx + (sw - bww) / 2, yy - bh, bww, bh, fill=accent)
                yy -= bh
            rect(s, cx + sw / 2 - 0.01, yy - 0.10 * h, 0.02, 0.10 * h, fill=accent)
            cx += sw + 0.01 * w
            continue
        bh = rnd.uniform(0.18, 0.55) * h
        rect(s, cx, base - bh, bw, bh, fill=rnd.choice(fg))
        cx += bw + rnd.uniform(0.004, 0.012) * w
    return None


def person(s, cx, top, size, fill=BLUE):
    head = size * 0.42
    rect(s, cx - head / 2, top, head, head, fill=fill, shape=MSO_SHAPE.OVAL)
    body_w, body_h = size * 0.8, size * 0.5
    b = rect(s, cx - body_w / 2, top + head + size * 0.06, body_w, body_h, fill=fill, shape=MSO_SHAPE.ROUND_2_SAME_RECTANGLE)
    if len(b.adjustments) > 0:
        b.adjustments[0] = 0.5


def people_scene(s, x, y, w, h, bg=PALE, n=5, seed=3, cols=(NAVY, BLUE, "1F4A85", MID, "17407F")):
    """Group of abstract people around a table — used where a team photo would go."""
    rect(s, x, y, w, h, fill=bg)
    rnd = random.Random(seed)
    table_y = y + h * 0.66
    rect(s, x + w * 0.12, table_y, w * 0.76, h * 0.07, fill="C4D8F6", shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
    size = min(h * 0.42, w / (n + 1.5))
    for i in range(n):
        cx = x + w * (0.18 + 0.64 * i / max(1, n - 1))
        top = table_y - size * 0.98 + rnd.uniform(-0.04, 0.04) * h
        person(s, cx, top, size, fill=cols[i % len(cols)])
    # laptops on table
    for i in range(max(1, n // 2)):
        lx = x + w * (0.28 + 0.44 * i / max(1, n // 2 - 1 if n // 2 > 1 else 1))
        rect(s, lx - 0.18, table_y - 0.16, 0.36, 0.16, fill=WHITE, line="B8CFEE")


def _style_chart(ch, size=10):
    ch.has_title = False
    ch.font.name = FONT
    ch.font.size = Pt(size)
    ch.font.color.rgb = rgb(TEXT)


def bar_chart(s, x, y, w, h, cats, series, kind="column", stacked=False, fmt='0', labels=True, legend=False,
              gap=60, size=10, label_color=None, value_axis=False, max_v=None, overlap=None):
    cd = CategoryChartData()
    cd.categories = cats
    for name, vals, _c in series:
        cd.add_series(name, vals)
    ct = {("column", False): XL_CHART_TYPE.COLUMN_CLUSTERED, ("column", True): XL_CHART_TYPE.COLUMN_STACKED,
          ("bar", False): XL_CHART_TYPE.BAR_CLUSTERED, ("bar", True): XL_CHART_TYPE.BAR_STACKED}[(kind, stacked)]
    gf = s.shapes.add_chart(ct, Inches(x), Inches(y), Inches(w), Inches(h), cd)
    ch = gf.chart
    _style_chart(ch, size)
    ch.has_legend = legend
    if legend:
        ch.legend.position = XL_LEGEND_POSITION.TOP
        ch.legend.include_in_layout = False
        ch.legend.font.size = Pt(size)
    plot = ch.plots[0]
    plot.gap_width = gap
    if overlap is not None:
        plot.overlap = overlap
    for i, (name, vals, col) in enumerate(series):
        ser = plot.series[i]
        ser.format.fill.solid()
        ser.format.fill.fore_color.rgb = rgb(col)
        ser.invert_if_negative = False
    if labels:
        plot.has_data_labels = True
        dl = plot.data_labels
        dl.number_format = fmt
        dl.number_format_is_linked = False
        dl.font.size = Pt(size)
        dl.font.bold = True
        dl.font.color.rgb = rgb(label_color or NAVY)
        if not stacked:
            dl.position = XL_LABEL_POSITION.OUTSIDE_END
        else:
            dl.position = XL_LABEL_POSITION.CENTER
    va = ch.value_axis
    va.has_major_gridlines = value_axis
    if value_axis:
        va.major_gridlines.format.line.color.rgb = rgb(LINE)
    va.visible = value_axis
    va.format.line.fill.background()
    if max_v is not None:
        va.maximum_scale = max_v
    va.minimum_scale = 0
    va.tick_labels.font.size = Pt(size - 1)
    va.tick_labels.font.color.rgb = rgb(MUTED)
    ca = ch.category_axis
    ca.format.line.color.rgb = rgb(LINE)
    ca.tick_labels.font.size = Pt(size)
    ca.tick_labels.font.color.rgb = rgb(TEXT)
    ca.has_major_gridlines = False
    if kind == "bar":
        ca.reverse_order = True
        va.tick_label_position = XL_TICK_LABEL_POSITION.NONE if not value_axis else XL_TICK_LABEL_POSITION.LOW
    return gf


def line_chart(s, x, y, w, h, cats, series, fmt='0', labels=True, size=10, max_v=None, legend=False, markers=True):
    cd = CategoryChartData()
    cd.categories = cats
    for name, vals, _c in series:
        cd.add_series(name, vals)
    gf = s.shapes.add_chart(XL_CHART_TYPE.LINE_MARKERS if markers else XL_CHART_TYPE.LINE,
                            Inches(x), Inches(y), Inches(w), Inches(h), cd)
    ch = gf.chart
    _style_chart(ch, size)
    ch.has_legend = legend
    if legend:
        ch.legend.position = XL_LEGEND_POSITION.TOP
        ch.legend.include_in_layout = False
    plot = ch.plots[0]
    for i, (name, vals, col) in enumerate(series):
        ser = plot.series[i]
        ser.format.line.color.rgb = rgb(col)
        ser.format.line.width = Pt(2.75)
        ser.smooth = False
        if markers:
            ser.marker.size = 8
            ser.marker.format.fill.solid()
            ser.marker.format.fill.fore_color.rgb = rgb(col)
            ser.marker.format.line.color.rgb = rgb(WHITE)
    if labels:
        plot.has_data_labels = True
        dl = plot.data_labels
        dl.number_format = fmt
        dl.number_format_is_linked = False
        dl.font.size = Pt(size)
        dl.font.bold = True
        dl.font.color.rgb = rgb(NAVY)
        dl.position = XL_LABEL_POSITION.ABOVE
    va = ch.value_axis
    va.visible = False
    va.has_major_gridlines = True
    va.major_gridlines.format.line.color.rgb = rgb("E6EEF9")
    va.minimum_scale = 0
    if max_v is not None:
        va.maximum_scale = max_v
    ca = ch.category_axis
    ca.format.line.color.rgb = rgb(LINE)
    ca.tick_labels.font.size = Pt(size)
    return gf


def donut(s, x, y, w, h, cats, vals, colors, fmt='0%', size=10, hole=62, labels=False):
    cd = CategoryChartData()
    cd.categories = cats
    cd.add_series("s", vals)
    gf = s.shapes.add_chart(XL_CHART_TYPE.DOUGHNUT, Inches(x), Inches(y), Inches(w), Inches(h), cd)
    ch = gf.chart
    _style_chart(ch, size)
    ch.has_legend = False
    plot = ch.plots[0]
    for i, c in enumerate(colors):
        pt = plot.series[0].points[i]
        pt.format.fill.solid()
        pt.format.fill.fore_color.rgb = rgb(c)
        pt.format.line.color.rgb = rgb(WHITE)
    hs = plot._element.find(qn("c:holeSize"))
    if hs is None:
        hs = etree.SubElement(plot._element, qn("c:holeSize"))
    hs.set("val", str(hole))
    if labels:
        plot.has_data_labels = True
        plot.data_labels.number_format = fmt
        plot.data_labels.number_format_is_linked = False
    return gf


def source(s, txt, y=6.72, dark=False, w=None):
    text(s, ML, y, w or (W - 2 * ML), 0.25, txt, size=8.5, color=("8EA0B8" if dark else MUTED), italic=False)


def divider(prs, num, title, sub, items=None, bg=NAVY):
    s = blank(prs, bg)
    rect(s, 0, 0, 0.18, H, fill=BLUE)
    text(s, ML + 0.1, 1.2, 4, 1.4, f"{num:02d}", size=72, color=BLUE, bold=True)
    text(s, ML + 0.1, 2.75, 7.6, 1.6, title, size=40, color=WHITE, bold=True, line=1.0)
    text(s, ML + 0.1, 4.45, 7.0, 1.4, sub, size=16, color="C9D6E8", line=1.3)
    if items:
        text(s, 8.85, 2.0, 3.8, 0.3, "IN THIS CHAPTER", size=9.5, color=MID, bold=True, spacing=1.3)
        for i, it in enumerate(items):
            yy = 2.45 + i * 0.52
            line(s, 8.85, yy, 12.68, yy, color="2E4A72")
            text(s, 8.85, yy + 0.1, 3.8, 0.4, it, size=12.5, color=WHITE)
    wordmark(s, ML + 0.1, 6.85, size=9.5, dark=True)
    return s
