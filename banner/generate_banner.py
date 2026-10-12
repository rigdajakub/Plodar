#!/usr/bin/env python3
"""Generuje SVG banner k 20. výročiu PloDar (1920 x 1080, 16:9).

Spustenie:  python3 banner/generate_banner.py
Výstup:     banner/plodar-20-banner.svg
"""
import math
import random
from pathlib import Path

W, H = 1920, 1080

# Paleta prevzatá z existujúceho bannera PloDar
BLUSH = "#F4E6EC"
BLUSH_DEEP = "#E9D0DC"
MAUVE = "#CB9FB3"
MAUVE_DARK = "#B57593"
WINE = "#8F2C5B"
WINE_DARK = "#662841"
CHARCOAL = "#5A5457"
GOLD = "#C9A25E"

# Stred kompozície čísla „20"
CX, CY = 1395, 545


def f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


# ---------------------------------------------------------------- fázy mesiaca
def moon(x, y, r, phase, lit, dark_stroke):
    """phase 0..1 (0 = nov, 0.5 = spln). Vráti SVG skupinu."""
    out = [f'<g transform="translate({f(x)} {f(y)})">']
    out.append(f'<circle r="{f(r)}" fill="{MAUVE}" fill-opacity=".28" stroke="{dark_stroke}" stroke-width="1.1" opacity=".9"/>')
    if 0.02 < phase < 0.98:
        waxing = phase < 0.5
        # podiel osvetlenia 0..1..0
        p = phase * 2 if waxing else (1 - phase) * 2
        k = abs(1 - 2 * p)  # polos terminátora
        side = 1 if waxing else 0  # pravá alebo ľavá polovica
        outer_sweep = 1 if waxing else 0
        # pri p < .5 kosák (terminátor sa vydúva k osvetlenej strane), inak dorastajúci/ubúdajúci mesiac
        inner_sweep = (0 if p < 0.5 else 1) if waxing else (1 if p < 0.5 else 0)
        d = (f"M0 {f(-r)} A{f(r)} {f(r)} 0 0 {outer_sweep} 0 {f(r)} "
             f"A{f(k * r)} {f(r)} 0 0 {inner_sweep} 0 {f(-r)}Z")
        out.append(f'<path d="{d}" fill="{lit}"/>')
    out.append("</g>")
    return "".join(out)


# ---------------------------------------------------------------- číslica „2" a „0"
# „2" – didonská kresba: tenké vlásočnice hore, plný oblúk a pätka
TWO = (
    "M1046 404"
    "C1046 318 1128 262 1214 262"
    "C1318 262 1392 330 1392 424"
    "C1392 528 1312 596 1214 682"
    "L1126 760"
    "L1352 760"
    "C1378 760 1396 744 1408 714"
    "L1422 714"
    "L1396 812"
    "L1040 812"
    "L1040 798"
    "L1222 632"
    "C1298 562 1324 496 1324 424"
    "C1324 340 1282 284 1212 284"
    "C1158 284 1116 312 1102 352"
    "Z"
)
TWO_BALL = (1083, 384, 41)

# „0" – ovál s premenlivou hrúbkou (silné boky, tenké temeno a pätka)
ZERO_C = (1640, 537)
ZERO_OUT = (178, 276)
ZERO_IN = (112, 252)


def zero_path():
    cx, cy = ZERO_C
    (orx, ory), (irx, iry) = ZERO_OUT, ZERO_IN
    return (f"M{cx - orx} {cy}A{orx} {ory} 0 1 0 {cx + orx} {cy}A{orx} {ory} 0 1 0 {cx - orx} {cy}Z"
            f"M{cx - irx} {cy}A{irx} {iry} 0 1 1 {cx + irx} {cy}A{irx} {iry} 0 1 1 {cx - irx} {cy}Z")


# ---------------------------------------------------------------- plynulá krivka cyklu
def wave(y0, amp, phase, periods=2.35, x0=-40, x1=W + 40, damp=True, steps=220):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        x = x0 + (x1 - x0) * t
        a = amp * (0.35 + 0.65 * math.sin(math.pi * t) ** 0.8) if damp else amp
        # krivka mierne stúpa doprava ku číslu
        y = y0 - 70 * t + a * math.sin(2 * math.pi * periods * t + phase)
        pts.append((x, y))
    # Catmull-Rom → Bézier
    d = [f"M{f(pts[0][0])} {f(pts[0][1])}"]
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i else pts[i]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[i + 2] if i + 2 < len(pts) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d.append(f"C{f(c1[0])} {f(c1[1])} {f(c2[0])} {f(c2[1])} {f(p2[0])} {f(p2[1])}")
    return "".join(d)


# ---------------------------------------------------------------- konfety
def confetti(rng):
    items = []
    colors = [(GOLD, 0.9), ("url(#gold)", 1), (WINE, 0.55), (MAUVE_DARK, 0.6), ("#FFFFFF", 0.9), (MAUVE, 0.8)]
    placed = []
    tries = 0
    while len(placed) < 95 and tries < 5000:
        tries += 1
        x = rng.uniform(40, W - 40)
        y = rng.uniform(40, H - 40)
        # ľavá časť ostáva čistá pre text – konfety tam len zriedka
        if x < 820 and rng.random() > 0.12:
            continue
        # nezahlcovať vnútro číslic
        if 1030 < x < 1830 and 250 < y < 830 and rng.random() > 0.25:
            continue
        if any((x - px) ** 2 + (y - py) ** 2 < 46 ** 2 for px, py in placed):
            continue
        placed.append((x, y))
        col, op = rng.choice(colors)
        fade = 0.45 if x < 820 else 1.0
        kind = rng.random()
        rot = rng.uniform(0, 180)
        if kind < 0.5:
            r = rng.choice([1.6, 2.2, 3, 3.8, 5])
            items.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{r}" fill="{col}" opacity="{f(op * fade)}"/>')
        elif kind < 0.72:
            L = rng.uniform(10, 22)
            items.append(
                f'<line x1="{f(x - L / 2)}" y1="{f(y)}" x2="{f(x + L / 2)}" y2="{f(y)}" stroke="{col}" '
                f'stroke-width="1.6" stroke-linecap="round" opacity="{f(op * fade)}" '
                f'transform="rotate({f(rot)} {f(x)} {f(y)})"/>')
        elif kind < 0.88:
            s = rng.uniform(4, 7)
            items.append(
                f'<rect x="{f(x - s / 2)}" y="{f(y - s * 0.9)}" width="{f(s)}" height="{f(s * 1.8)}" rx="1" '
                f'fill="{col}" opacity="{f(op * fade)}" transform="rotate({f(rot)} {f(x)} {f(y)})"/>')
        else:
            s = rng.uniform(4, 6.5)
            items.append(
                f'<path d="M{f(x)} {f(y - s)}L{f(x + s * .55)} {f(y)}L{f(x)} {f(y + s)}L{f(x - s * .55)} {f(y)}Z" '
                f'fill="url(#gold)" opacity="{f(fade)}"/>')
    return "\n    ".join(items)


def sparkle(x, y, s, op=1):
    d = (f"M{f(x)} {f(y - s)}C{f(x + s * .12)} {f(y - s * .12)} {f(x + s * .12)} {f(y - s * .12)} {f(x + s)} {f(y)}"
         f"C{f(x + s * .12)} {f(y + s * .12)} {f(x + s * .12)} {f(y + s * .12)} {f(x)} {f(y + s)}"
         f"C{f(x - s * .12)} {f(y + s * .12)} {f(x - s * .12)} {f(y + s * .12)} {f(x - s)} {f(y)}"
         f"C{f(x - s * .12)} {f(y - s * .12)} {f(x - s * .12)} {f(y - s * .12)} {f(x)} {f(y - s)}Z")
    return f'<path d="{d}" fill="url(#gold)" opacity="{op}"/>'


def build():
    rng = random.Random(2026)

    # --- eliptický oblúk s fázami mesiaca nad číslom (nov → spln → nov)
    ECX, ECY, ERX, ERY = CX - 5, 565, 470, 425
    a0, a1 = 168, 12

    def on_arc(deg, dr=0):
        a = math.radians(deg)
        return ECX + (ERX + dr) * math.cos(a), ECY - (ERY + dr) * math.sin(a)

    def arc_path(d0, d1, dr=0):
        (x0, y0), (x1, y1) = on_arc(d0, dr), on_arc(d1, dr)
        return f"M{f(x0)} {f(y0)}A{ERX + dr} {ERY + dr} 0 0 1 {f(x1)} {f(y1)}"

    arc = arc_path(a0 + 8, a1 - 8)
    inner_arc = arc_path(a0 - 4, a1 + 4, dr=-30)
    moons, ticks = [], []
    n = 9
    for i in range(n):
        t = i / (n - 1)
        x, y = on_arc(a0 + (a1 - a0) * t)
        r = 17 if i == n // 2 else 14
        moons.append(moon(x, y, r, min(t, 0.999), "url(#gold)", GOLD))
        if i < n - 1:
            tx, ty = on_arc(a0 + (a1 - a0) * (i + 0.5) / (n - 1))
            ticks.append(f'<circle cx="{f(tx)}" cy="{f(ty)}" r="2.2" fill="{GOLD}" opacity=".85"/>')

    zp = zero_path()
    bx, by, br = TWO_BALL
    two_full = f'<path d="{TWO}"/><circle cx="{bx}" cy="{by}" r="{br}"/>'

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <title>PloDar – 20 rokov</title>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2=".35">
      <stop offset="0" stop-color="#F8EEF2"/>
      <stop offset=".45" stop-color="{BLUSH}"/>
      <stop offset="1" stop-color="{BLUSH_DEEP}"/>
    </linearGradient>
    <radialGradient id="glow" cx="{CX}" cy="{CY}" r="620" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity=".75"/>
      <stop offset=".55" stop-color="#FFFFFF" stop-opacity=".22"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="vignette" cx=".42" cy=".5" r=".78">
      <stop offset=".62" stop-color="{MAUVE}" stop-opacity="0"/>
      <stop offset="1" stop-color="{MAUVE_DARK}" stop-opacity=".38"/>
    </radialGradient>
    <radialGradient id="blobA" cx="1760" cy="160" r="420" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{MAUVE}" stop-opacity=".35"/>
      <stop offset="1" stop-color="{MAUVE}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="blobB" cx="1120" cy="1010" r="460" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#F2C9D9" stop-opacity=".45"/>
      <stop offset="1" stop-color="#F2C9D9" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="numeral" x1="1040" y1="262" x2="1820" y2="812" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#A2416F"/>
      <stop offset=".5" stop-color="{WINE}"/>
      <stop offset="1" stop-color="{WINE_DARK}"/>
    </linearGradient>
    <linearGradient id="sheen" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity=".22"/>
      <stop offset=".45" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="gold" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#B98A43"/>
      <stop offset=".45" stop-color="#E9D3A1"/>
      <stop offset=".7" stop-color="#CDA866"/>
      <stop offset="1" stop-color="#A97B37"/>
    </linearGradient>
    <linearGradient id="goldLine" x1="0" y1="0" x2="{W}" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{GOLD}" stop-opacity="0"/>
      <stop offset=".25" stop-color="{GOLD}" stop-opacity=".55"/>
      <stop offset=".7" stop-color="#E2C68E" stop-opacity=".95"/>
      <stop offset="1" stop-color="{GOLD}" stop-opacity=".2"/>
    </linearGradient>
    <linearGradient id="wineLine" x1="0" y1="0" x2="{W}" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{WINE}" stop-opacity="0"/>
      <stop offset=".2" stop-color="{WINE}" stop-opacity=".35"/>
      <stop offset=".65" stop-color="{WINE}" stop-opacity=".75"/>
      <stop offset="1" stop-color="{WINE}" stop-opacity=".25"/>
    </linearGradient>
    <linearGradient id="mauveLine" x1="0" y1="0" x2="{W}" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{MAUVE_DARK}" stop-opacity="0"/>
      <stop offset=".4" stop-color="{MAUVE_DARK}" stop-opacity=".35"/>
      <stop offset="1" stop-color="{MAUVE_DARK}" stop-opacity=".15"/>
    </linearGradient>
    <filter id="grain" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="3" seed="7" stitchTiles="stitch"/>
      <feColorMatrix type="matrix" values="0 0 0 0 .45  0 0 0 0 .25  0 0 0 0 .35  0 0 0 .55 0"/>
    </filter>
    <filter id="paper" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency=".006 .012" numOctaves="2" seed="3"/>
      <feColorMatrix type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .9 -.35"/>
    </filter>
    <filter id="soft" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="18" stdDeviation="22" flood-color="{WINE_DARK}" flood-opacity=".22"/>
      <feDropShadow dx="0" dy="3" stdDeviation="3" flood-color="{WINE_DARK}" flood-opacity=".18"/>
    </filter>
    <filter id="faint" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="1.5" stdDeviation="1.5" flood-color="{WINE_DARK}" flood-opacity=".2"/>
    </filter>
    <clipPath id="numClip">{two_full}<path d="{zp}" clip-rule="evenodd" fill-rule="evenodd"/></clipPath>
  </defs>

  <!-- pozadie -->
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <rect width="{W}" height="{H}" fill="url(#blobA)"/>
  <rect width="{W}" height="{H}" fill="url(#blobB)"/>
  <rect width="{W}" height="{H}" fill="url(#glow)"/>
  <rect width="{W}" height="{H}" filter="url(#paper)" opacity=".35"/>
  <rect width="{W}" height="{H}" fill="url(#vignette)"/>

  <!-- veľké jemné organické tvary za číslom -->
  <g opacity=".55">
    <ellipse cx="{CX + 40}" cy="{CY + 10}" rx="520" ry="455" fill="none" stroke="#FFFFFF" stroke-width="1.2" opacity=".9"/>
    <ellipse cx="{CX + 70}" cy="{CY - 10}" rx="560" ry="470" fill="none" stroke="{MAUVE}" stroke-width="1" opacity=".55" transform="rotate(-8 {CX} {CY})"/>
  </g>

  <!-- rytmus: krivky naprieč celým bannerom -->
  <g fill="none" stroke-linecap="round">
    <path d="{wave(820, 70, 0.6)}" stroke="url(#mauveLine)" stroke-width="1"/>
    <path d="{wave(800, 92, 0.15)}" stroke="url(#wineLine)" stroke-width="2.2"/>
    <path d="{wave(812, 82, 0.35)}" stroke="url(#goldLine)" stroke-width="1.2"/>
  </g>

  <!-- oblúk cyklu s fázami mesiaca -->
  <g fill="none" stroke-linecap="round">
    <path d="{arc}" stroke="{GOLD}" stroke-width="1.4" opacity=".75"/>
    <path d="{inner_arc}" stroke="{MAUVE_DARK}" stroke-width="1" stroke-dasharray="1 7" opacity=".6"/>
  </g>
  {"".join(ticks)}
  <g filter="url(#faint)">{"".join(moons)}</g>

  <g transform="translate(-30 0)">
  <!-- číslo 20: vrstvené kontúry (ozvena tvaru) -->
  <g fill="none" stroke-linejoin="round">
    <g transform="translate(20 16)" stroke="{MAUVE}" stroke-width="1.2" opacity=".75">{two_full}<path d="{zp}"/></g>
    <g transform="translate(10 8)" stroke="url(#gold)" stroke-width="1.3" opacity=".9">{two_full}<path d="{zp}"/></g>
  </g>

  <!-- číslo 20: hlavný tvar -->
  <g filter="url(#soft)">
    <g fill="url(#numeral)">
      {two_full}
      <path d="{zp}" fill-rule="evenodd"/>
    </g>
  </g>
  <!-- jemný lesk a vnútorné línie v číslici -->
  <g clip-path="url(#numClip)">
    <rect x="1000" y="240" width="860" height="600" fill="url(#sheen)"/>
    <g fill="none" stroke="#FFFFFF" stroke-width="1" opacity=".22">
      <path d="{wave(560, 40, 1.2, periods=3.2, x0=1000, x1=1860, damp=False)}"/>
      <path d="{wave(600, 46, 1.6, periods=3.2, x0=1000, x1=1860, damp=False)}"/>
      <path d="{wave(640, 52, 2.0, periods=3.2, x0=1000, x1=1860, damp=False)}"/>
    </g>
  </g>
  <!-- tenká zlatá vlásočnica vo vnútri nuly a dvojky -->
  <g fill="none" stroke="url(#gold)" stroke-width="1.1" opacity=".85">
    <ellipse cx="{ZERO_C[0]}" cy="{ZERO_C[1]}" rx="{ZERO_IN[0] - 16}" ry="{ZERO_IN[1] - 16}"/>
  </g>

  </g>

  <!-- konfety a čiastočky -->
  <g>
    {confetti(rng)}
  </g>
  {sparkle(1012, 238, 15)}
  {sparkle(1858, 300, 11, .9)}
  {sparkle(1790, 880, 13)}
  {sparkle(1160, 905, 8, .8)}
  {sparkle(905, 520, 7, .6)}

  <!-- zrno / textúra -->
  <rect width="{W}" height="{H}" filter="url(#grain)" opacity=".07"/>

  <!-- tenký rám ako v identite PloDar -->
  <g fill="none" stroke="{MAUVE_DARK}" stroke-width="1" opacity=".55">
    <rect x="34" y="34" width="{W - 68}" height="{H - 68}"/>
  </g>
  <g fill="none" stroke="url(#gold)" stroke-width="1.6">
    <path d="M34 82V34H82"/><path d="M{W - 82} 34H{W - 34}V82"/>
    <path d="M34 {H - 82}V{H - 34}H82"/><path d="M{W - 82} {H - 34}H{W - 34}V{H - 82}"/>
  </g>
</svg>
'''
    return svg


if __name__ == "__main__":
    out = Path(__file__).with_name("plodar-20-banner.svg")
    out.write_text(build(), encoding="utf-8")
    print(f"zapísané: {out}")
