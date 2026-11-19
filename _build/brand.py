#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genereert de merkbestanden (logo, grachtenpanden-silhouet) als SVG.

Gebruik (vanuit de root van de repository):
    python3 _build/brand.py

De PNG-iconen, favicon.ico en de social-afbeelding worden van deze SVG's gerenderd.
"""
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

NAVY = "#070c17"
NAVY2 = "#0e1b30"
ACCENT = "#f2e23f"


def mark(color=ACCENT, cut=NAVY):
    """Beeldmerk: gasfles met de drie Amsterdamse kruisen in een 24-uurs ring. viewBox 0 0 512 512."""
    crosses = "".join(
        '<path d="M%d %dl36 36m0-36l-36 36"/>' % (238, y) for y in (232, 290, 348)
    )
    return (
        # ring met opening rechtsboven en pijlpunt: de klok rond
        '<path d="M330 74A196 196 0 1 0 438 184" fill="none" stroke="%(c)s" stroke-width="30" stroke-linecap="round"/>'
        '<path d="M472 150l-30 78-52-62z" fill="%(c)s"/>'
        # gasfles
        '<rect x="226" y="120" width="60" height="26" rx="8" fill="%(c)s"/>'
        '<rect x="240" y="140" width="32" height="44" fill="%(c)s"/>'
        '<path d="M190 232c0-34 28-58 66-58s66 24 66 58v150c0 18-14 32-32 32h-68c-18 0-32-14-32-32z" fill="%(c)s"/>'
        '<g fill="none" stroke="%(k)s" stroke-width="13" stroke-linecap="round">%(x)s</g>'
    ) % {"c": color, "k": cut, "x": crosses}


def logo_svg():
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" role="img" aria-label="Lachgasamsterdam-247">'
        '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient></defs>'
        '<rect width="512" height="512" rx="112" fill="url(#g)"/>'
        '<g transform="translate(256 262) scale(.86) translate(-250 -256)">%s</g></svg>'
    ) % (NAVY, NAVY2, mark())


def mark_inline():
    """Los beeldmerk zonder achtergrond, inline in header en footer."""
    return '<svg viewBox="30 40 460 440" aria-hidden="true" focusable="false">%s</svg>' % mark()


def skyline(width=1200, base=220, seed=247, fill="#12213a", lit=ACCENT, dark="#0a1424"):
    """Rij grachtenpanden met trap-, hals-, klok- en tuitgevels. Geeft (svg-inhoud, breedte)."""
    rnd = random.Random(seed)
    out, x = [], 0
    kinds = ["trap", "hals", "klok", "tuit"]
    last = None
    while x < width:
        w = rnd.choice([58, 64, 70, 76, 84])
        h = rnd.randint(95, 150)
        kind = rnd.choice([k for k in kinds if k != last])
        last = kind
        top = base - h
        m = x + w / 2.0
        if kind == "trap":
            s, d = w / 8.0, 13
            pts = [(x, base), (x, top)]
            for i in range(1, 4):
                pts += [(x + s * i, top - d * (i - 1)), (x + s * i, top - d * i)]
            pts += [(x + w - s * 3, top - d * 3)]
            for i in range(3, 0, -1):
                pts += [(x + w - s * i, top - d * (i - 1))] if i < 3 else []
                pts += [(x + w - s * i, top - d * (i - 1))]
                pts += [(x + w - s * (i - 1), top - d * (i - 1))] if i > 1 else [(x + w, top)]
            pts += [(x + w, base)]
            d_ = "M" + "L".join("%.1f %.1f" % p for p in pts) + "Z"
            peak = top - d * 3
        elif kind == "hals":
            n = w * 0.22
            d_ = ("M%.1f %d V%.1f H%.1f Q%.1f %.1f %.1f %.1f V%.1f L%.1f %.1f L%.1f %.1f V%.1f Q%.1f %.1f %.1f %.1f H%.1f V%dZ" % (
                x, base, top, x + 4, m - n, top, m - n, top - 16, top - 44, m, top - 58,
                m + n, top - 44, top - 16, m + n, top, x + w - 4, top, x + w, base))
            peak = top - 58
        elif kind == "klok":
            d_ = ("M%.1f %d V%.1f C%.1f %.1f %.1f %.1f %.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f V%dZ" % (
                x, base, top,
                x + w * .22, top, x + w * .16, top - 30, x + w * .30, top - 34,
                x + w * .34, top - 52, x + w * .42, top - 54, m, top - 54,
                x + w * .58, top - 54, x + w * .66, top - 52, x + w * .70, top - 34,
                x + w * .84, top - 30, x + w * .78, top, x + w, top, base))
            peak = top - 54
        else:
            d_ = "M%.1f %d V%.1f L%.1f %.1f H%.1f L%.1f %.1f V%dZ" % (
                x, base, top, m - 7, top - 42, m + 7, x + w, top, base)
            peak = top - 42
        out.append('<path d="%s" fill="%s"/>' % (d_, fill))
        # hijsbalk
        out.append('<rect x="%.1f" y="%.1f" width="3" height="9" fill="%s"/>' % (m - 1.5, peak - 8, fill))
        # ramen
        cols = 3 if w >= 70 else 2
        gap = w / (cols + 1.0)
        rows = int((h - 34) // 30)
        for r in range(rows):
            for c in range(cols):
                wx = x + gap * (c + 1) - 5
                wy = top + 10 + r * 30
                on = rnd.random() < 0.22
                out.append('<rect x="%.1f" y="%.1f" width="10" height="17" fill="%s"%s/>' % (
                    wx, wy, lit if on else dark, "" if on else ""))
        # zolderraam
        out.append('<rect x="%.1f" y="%.1f" width="8" height="12" fill="%s"/>' % (m - 4, top - 22, dark))
        # deur
        out.append('<rect x="%.1f" y="%d" width="13" height="24" fill="%s"/>' % (x + gap - 6.5, base - 24, dark))
        x += w + 2
    return "".join(out), x


def skyline_svg():
    body, w = skyline()
    return '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="220" viewBox="0 0 %d 220">%s</svg>' % (w, w, body)


def main():
    for name, data in (("logo.svg", logo_svg()), ("grachtenpanden.svg", skyline_svg())):
        with open(os.path.join(ROOT, "images", name), "w", encoding="utf-8") as f:
            f.write(data)
    print("merkbestanden gegenereerd")


if __name__ == "__main__":
    main()
