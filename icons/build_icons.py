#!/usr/bin/env python3
"""Generate the Ram-Gear App Hub icon set (SVG + PNG + preview sheet).

Run:  python3 build_icons.py      (needs: pip install cairosvg pillow)
Gear outlines are computed (straight-flank, 20 deg pressure angle approximation
of an involute tooth with module-based addendum/dedendum), so every gear has
evenly spaced, correctly proportioned teeth and meshing gears really mesh.
"""
import math, os
import cairosvg
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.dirname(os.path.abspath(__file__))

# ---- Brand palette (sampled from /workspace/ramgear-app/app.css + logo) ----
BG_TOP = "#2E7386"     # --navy / primary UI teal (buttons, existing app icon)
BG_BOT = "#245E6E"     # same teal, ~20% darker, for a subtle vertical gradient
GLYPH = "#FFFFFF"      # white glyph
ACCENT = "#9FD3E1"     # --link-on-dark light teal (also the underline in the app's RG icon)
SHEET_BG = "#F3F5F6"   # --light, preview sheet background
SHEET_TEXT = "#2C2C2E" # --header / charcoal, preview sheet labels

CUT = "url(#bg)"       # "cut-out" paint: same userSpaceOnUse gradient as the tile
RADIUS = 112           # tile corner radius on the 512 canvas (~22%)


def f(v):
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s


def pol(cx, cy, r, a):
    return cx + r * math.cos(a), cy + r * math.sin(a)


def circle_sub(cx, cy, r):
    """Circle as a path sub-path (for even-odd holes)."""
    return (f"M{f(cx + r)} {f(cy)}A{f(r)} {f(r)} 0 1 1 {f(cx - r)} {f(cy)}"
            f"A{f(r)} {f(r)} 0 1 1 {f(cx + r)} {f(cy)}Z")


def gear_d(cx, cy, n, m, rot_deg=0.0, hole=0.0, alpha=10.0, add=0.85, ded=1.0):
    """Gear outline path data. n teeth, module m (pitch radius = m*n/2).
    addendum = add*m, dedendum = ded*m (stub-tooth proportions), tooth
    thickness = half the pitch at the pitch circle, straight flanks at the
    pressure angle `alpha`. Stub teeth with a low flank angle keep the tips
    broad so they read as solid teeth (not a sunburst) at 64 px."""
    R = m * n / 2.0
    rt, rr = R + add * m, R - ded * m
    ta = math.tan(math.radians(alpha))
    s_p = math.pi * m / 2.0
    s_t = s_p - 2 * add * m * ta
    s_r = s_p + 2 * ded * m * ta
    ht, hr = (s_t / 2) / rt, (s_r / 2) / rr
    p = 2 * math.pi / n
    hr = min(hr, p * 0.5 * 0.92)  # keep a bit of root land on small gears
    rot = math.radians(rot_deg)
    d = []
    for i in range(n):
        th = rot + i * p
        x0, y0 = pol(cx, cy, rr, th - hr)
        x1, y1 = pol(cx, cy, rt, th - ht)
        x2, y2 = pol(cx, cy, rt, th + ht)
        x3, y3 = pol(cx, cy, rr, th + hr)
        x4, y4 = pol(cx, cy, rr, th + p - hr)
        if i == 0:
            d.append(f"M{f(x0)} {f(y0)}")
        d.append(f"L{f(x1)} {f(y1)}A{f(rt)} {f(rt)} 0 0 1 {f(x2)} {f(y2)}"
                 f"L{f(x3)} {f(y3)}A{f(rr)} {f(rr)} 0 0 1 {f(x4)} {f(y4)}")
    d.append("Z")
    if hole:
        d.append(circle_sub(cx, cy, hole))
    return "".join(d)


def mesh_rot(c1, n1, rot1, c2, n2):
    """Rotation (deg) for gear 2 so its teeth fall in gear 1's gaps."""
    phi = math.atan2(c2[1] - c1[1], c2[0] - c1[0])
    p1, p2 = 2 * math.pi / n1, 2 * math.pi / n2
    r1 = math.radians(rot1)
    k = round((phi - r1) / p1)
    delta = (r1 + k * p1) - phi             # gear-1 tooth nearest the contact line
    t2 = phi + math.pi - delta * n1 / n2 + p2 / 2
    return math.degrees(t2)


def svg_doc(title, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <title>{title}</title>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="512" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{BG_TOP}"/>
      <stop offset="1" stop-color="{BG_BOT}"/>
    </linearGradient>
  </defs>
  <!-- tile: identical on every icon -->
  <rect width="512" height="512" rx="{RADIUS}" fill="url(#bg)"/>
{body}
</svg>
'''

# ---------------------------------------------------------------- icons ----

def icon_qc_form():
    # clipboard board + clip, two checked rows, one open row, accent gear badge
    gx, gy, gn, gm = 362, 370, 10, 15
    b = []
    b.append('  <!-- clipboard -->')
    b.append(f'  <rect x="124" y="122" width="236" height="306" rx="30" fill="{GLYPH}"/>')
    b.append(f'  <rect x="184" y="94" width="116" height="62" rx="20" fill="{ACCENT}" stroke="{CUT}" stroke-width="14" paint-order="stroke"/>')
    b.append(f'  <circle cx="242" cy="112" r="11" fill="{CUT}"/>')
    b.append('  <!-- check rows -->')
    for y in (206, 284):
        b.append(f'  <path d="M158 {y}l22 22 40-44" fill="none" stroke="{CUT}" stroke-width="22" stroke-linecap="round" stroke-linejoin="round"/>')
        b.append(f'  <rect x="240" y="{y - 11}" width="88" height="22" rx="11" fill="{CUT}"/>')
    b.append(f'  <rect x="158" y="351" width="60" height="22" rx="11" fill="{CUT}"/>')
    b.append('  <!-- gear badge -->')
    b.append(f'  <path d="{gear_d(gx, gy, gn, gm, -90, hole=24)}" fill="{ACCENT}" fill-rule="evenodd" stroke="{CUT}" stroke-width="16" paint-order="stroke" stroke-linejoin="round"/>')
    return svg_doc("QC Form", "\n".join(b))


def icon_web_gear_calc():
    cx, cy, n, m = 256, 214, 16, 13
    rt = m * n / 2 + 0.85 * m
    b = []
    b.append('  <!-- gear -->')
    b.append(f'  <path d="{gear_d(cx, cy, n, m, -90, hole=34)}" fill="{GLYPH}" fill-rule="evenodd"/>')
    xl, xr, yd = cx - rt, cx + rt, 392
    b.append('  <!-- tip-diameter dimension -->')
    b.append(f'  <path d="M{f(xl)} {f(cy + 56)}V{yd + 32}M{f(xr)} {f(cy + 56)}V{yd + 32}" stroke="{ACCENT}" stroke-width="20" stroke-linecap="round"/>')
    b.append(f'  <path d="M{f(xl + 40)} {yd}H{f(xr - 40)}" stroke="{ACCENT}" stroke-width="22"/>')
    b.append(f'  <path d="M{f(xl + 8)} {yd}l46-26v52zM{f(xr - 8)} {yd}l-46-26v52z" fill="{ACCENT}" stroke="{ACCENT}" stroke-width="8" stroke-linejoin="round"/>')
    return svg_doc("Web Gear Calc", "\n".join(b))


def icon_worm_mow():
    """Axial section of a single-start worm (trapezoidal thread, 20 deg flank
    half-angle, cut square at both ends) with the 3-wire setup: two wires in
    adjacent grooves on top, one on the bottom between them, micrometer anvils
    on the wires and an M (measurement over wires) dimension arrow."""
    P, alpha, h2 = 84.0, math.radians(20), 22.0     # pitch, flank half-angle, half depth
    ytp, ybp = 208.0, 304.0                          # top / bottom pitch lines
    g1 = 164.0                                       # first top wire groove centre
    ht = P / 4 - h2 * math.tan(alpha)                # half width of crest / root land
    fl = 2 * h2 * math.tan(alpha)                    # flank run
    xs, xe = g1 - P, g1 + 2 * P                      # 3 pitches, section cut square at both ends
    def prof(x0, pitch_y, out):
        """breakpoints of a thread edge, groove centres at x0 + kP; out=+1 top."""
        crest, root = pitch_y - out * h2, pitch_y + out * h2
        pts = []
        k = math.floor((xs - x0) / P) - 1
        while x0 + k * P < xe + P:
            g = x0 + k * P
            pts += [(g - ht, root), (g + ht, root), (g + ht + fl, crest), (g + P - ht - fl, crest)]
            k += 1
        def yat(x):
            for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
                if xa <= x <= xb:
                    return ya if xb == xa else ya + (yb - ya) * (x - xa) / (xb - xa)
        inner = [(x, y) for x, y in pts if xs + 0.5 < x < xe - 0.5]
        return [(xs, yat(xs))] + inner + [(xe, yat(xe))]

    top = prof(g1, ytp, +1)
    bot = prof(g1 + P / 2, ybp, -1)
    d = [f"M{f(xs)} {f(top[0][1])}"]
    d += [f"L{f(x)} {f(y)}" for x, y in top[1:]]
    d += [f"L{f(x)} {f(y)}" for x, y in reversed(bot)]
    d.append("Z")
    rw = 26.0                                        # wire radius (sits tangent to both flanks)
    lift = (rw / math.cos(alpha) - P / 4) / math.tan(alpha)
    wires = [(g1, ytp - lift), (g1 + P, ytp - lift), (g1 + P / 2, ybp + lift)]
    b = ['  <!-- worm axial section -->',
         f'  <path d="{"".join(d)}" fill="{GLYPH}" stroke="{GLYPH}" stroke-width="4" stroke-linejoin="round"/>',
         '  <!-- three measuring wires, tangent to the thread flanks -->']
    for wx, wy in wires:
        b.append(f'  <circle cx="{f(wx)}" cy="{f(wy)}" r="{f(rw)}" fill="{ACCENT}" stroke="{CUT}" stroke-width="6" paint-order="stroke"/>')
    ytop, ybot = ytp - lift - rw, ybp + lift + rw
    b.append('  <!-- micrometer anvils + M dimension -->')
    b.append(f'  <rect x="{f(g1 - 44)}" y="{f(ytop - 22)}" width="{f(P + 88)}" height="22" rx="8" fill="{GLYPH}"/>')
    b.append(f'  <rect x="{f(g1 + P / 2 - 52)}" y="{f(ybot)}" width="104" height="22" rx="8" fill="{GLYPH}"/>')
    ax = 410
    b.append(f'  <path d="M{ax} {f(ytop + 14)}V{f(ybot - 14)}" stroke="{ACCENT}" stroke-width="22"/>')
    b.append(f'  <path d="M{ax} {f(ytop - 22)}l-26 44h52zM{ax} {f(ybot + 22)}l-26 -44h52z" fill="{ACCENT}" stroke="{ACCENT}" stroke-width="8" stroke-linejoin="round"/>')
    return svg_doc("RG Worm MOW", "\n".join(b))


def icon_cardfile():
    """Stack of three landscape index cards, front card ruled like an index card."""
    W, H, rx = 252, 164, 22
    cards = [(160, 124, ACCENT), (128, 174, GLYPH), (96, 224, GLYPH)]   # back -> front
    b = ['  <!-- stacked index cards -->']
    for i, (x, y, fill) in enumerate(cards):
        st = "" if i == 0 else f' stroke="{CUT}" stroke-width="16" paint-order="stroke"'
        b.append(f'  <rect x="{x}" y="{y}" width="{W}" height="{H}" rx="{rx}" fill="{fill}"{st}/>')
    x, y, _ = cards[-1]
    b.append('  <!-- header rule + text lines -->')
    b.append(f'  <rect x="{x + 28}" y="{y + 30}" width="{W - 56}" height="26" rx="13" fill="{CUT}"/>')
    b.append(f'  <rect x="{x + 28}" y="{y + 78}" width="150" height="20" rx="10" fill="{CUT}"/>')
    b.append(f'  <rect x="{x + 28}" y="{y + 116}" width="110" height="20" rx="10" fill="{CUT}"/>')
    return svg_doc("Cardfile", "\n".join(b))


def icon_change_gear():
    """Three-gear change-gear train, all one module, phased so teeth mesh.
    The train is scaled to fit a 372 px box and centred on the tile."""
    gears = [(18, GLYPH, 0.30), (12, ACCENT, 0.28), (9, GLYPH, 0.26)]  # n, colour, hole/pitch-radius
    a1, a2 = math.radians(-28), math.radians(-128)
    def layout(m):
        R = [m * n / 2 for n, _, _ in gears]
        c0 = (0.0, 0.0)
        c1 = (c0[0] + (R[0] + R[1]) * math.cos(a1), c0[1] + (R[0] + R[1]) * math.sin(a1))
        c2 = (c1[0] + (R[1] + R[2]) * math.cos(a2), c1[1] + (R[1] + R[2]) * math.sin(a2))
        cs = [c0, c1, c2]
        xs = [c[0] + s * (r + 0.85 * m) for c, r in zip(cs, R) for s in (-1, 1)]
        ys = [c[1] + s * (r + 0.85 * m) for c, r in zip(cs, R) for s in (-1, 1)]
        return R, cs, (min(xs), max(xs), min(ys), max(ys))
    _, _, (x0, x1, y0, y1) = layout(1.0)
    m = 372 / max(x1 - x0, y1 - y0)
    R, cs, (x0, x1, y0, y1) = layout(m)
    dx, dy = 256 - (x0 + x1) / 2, 256 - (y0 + y1) / 2
    cs = [(x + dx, y + dy) for x, y in cs]
    rots = [0.0]
    rots.append(mesh_rot(cs[0], gears[0][0], rots[0], cs[1], gears[1][0]))
    rots.append(mesh_rot(cs[1], gears[1][0], rots[1], cs[2], gears[2][0]))
    b = [f'  <!-- meshing change-gear train: {gears[0][0]}/{gears[1][0]}/{gears[2][0]} teeth, module {m:.2f} px -->']
    for (n, col, hf), (x, y), rot, r in zip(gears, cs, rots, R):
        b.append(f'  <path d="{gear_d(x, y, n, m, rot, hole=hf * r)}" fill="{col}" fill-rule="evenodd"/>')
    return svg_doc("Change Gear", "\n".join(b))


def icon_app_hub():
    s, g = 124, 36
    x0 = 256 - s - g / 2
    b = ['  <!-- 2x2 launcher grid, one tile is a gear -->']
    for r in range(2):
        for c in range(2):
            x, y = x0 + c * (s + g), x0 + r * (s + g)
            if (r, c) == (1, 1):
                cx, cy = x + s / 2, y + s / 2
                b.append(f'  <path d="{gear_d(cx, cy, 10, 13.8, -90, hole=20)}" fill="{ACCENT}" fill-rule="evenodd"/>')
            else:
                b.append(f'  <rect x="{f(x)}" y="{f(y)}" width="{s}" height="{s}" rx="30" fill="{GLYPH}"/>')
    return svg_doc("App Hub", "\n".join(b))


ICONS = [
    ("qc-form", "QC Form", icon_qc_form),
    ("web-gear-calc", "Web Gear Calc", icon_web_gear_calc),
    ("rg-worm-mow", "RG Worm MOW", icon_worm_mow),
    ("cardfile", "Cardfile", icon_cardfile),
    ("change-gear", "Change Gear", icon_change_gear),
    ("app-hub", "App Hub", icon_app_hub),
]
SIZES = (512, 192, 64)


def font(size, bold=False):
    base = "/usr/share/fonts/truetype/sand-box/google/Inter/"
    for name in os.listdir(base) if os.path.isdir(base) else []:
        if name.startswith("Inter-VariableFont") or name.startswith("Inter[") :
            ft = ImageFont.truetype(base + name, size)
            try:
                ft.set_variation_by_name("Bold" if bold else "Medium")
            except Exception:
                pass
            return ft
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)


def main():
    for slug, name, fn in ICONS:
        svg = fn()
        p = os.path.join(OUT, f"{slug}.svg")
        with open(p, "w") as fh:
            fh.write(svg)
        for sz in SIZES:
            cairosvg.svg2png(bytestring=svg.encode(), write_to=os.path.join(OUT, f"{slug}-{sz}.png"),
                             output_width=sz, output_height=sz)
    # preview sheet
    col, pad = 260, 40
    Wd = pad * 2 + col * len(ICONS)
    Ht = 540
    sheet = Image.new("RGB", (Wd, Ht), SHEET_BG)
    dr = ImageDraw.Draw(sheet)
    dr.text((pad, 24), "Ram-Gear App Hub icons", font=font(30, True), fill=SHEET_TEXT)
    dr.text((pad, 66), "192 px", font=font(18), fill="#6E767E")
    fl = font(22, True)
    for i, (slug, name, _) in enumerate(ICONS):
        cx = pad + col * i + col // 2
        im = Image.open(os.path.join(OUT, f"{slug}-192.png")).convert("RGBA")
        sheet.paste(im, (cx - 96, 100), im)
        tw = dr.textlength(name, font=fl)
        dr.text((cx - tw / 2, 306), name, font=fl, fill=SHEET_TEXT)
    dr.line((pad, 360, Wd - pad, 360), fill="#D5D8DB", width=2)
    dr.text((pad, 376), "64 px (actual size)", font=font(18), fill="#6E767E")
    fs = font(16)
    for i, (slug, name, _) in enumerate(ICONS):
        cx = pad + col * i + col // 2
        im = Image.open(os.path.join(OUT, f"{slug}-64.png")).convert("RGBA")
        sheet.paste(im, (cx - 32, 412), im)
        tw = dr.textlength(name, font=fs)
        dr.text((cx - tw / 2, 486), name, font=fs, fill=SHEET_TEXT)
    # 64px row on a dark strip too, launcher-like
    sheet.save(os.path.join(OUT, "preview-sheet.png"))


if __name__ == "__main__":
    main()
