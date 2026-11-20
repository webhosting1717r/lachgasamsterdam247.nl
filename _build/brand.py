#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genereert de merkbestanden (logo, grachtenpanden-silhouet) als SVG.

Gebruik (vanuit de root van de repository):
    python3 _build/brand.py

Stijl "Amsterdam After Dark": grafiet/zwart, Apple-blauw als actiekleur en amber als licht.
De PNG-iconen, favicon.ico en de social-afbeelding worden van deze SVG's gerenderd
(zie _build/render_icons.js).

De skyline bestaat in twee vormen die uit dezelfde tekening komen:
  * horizon_html()   inline SVG-lagen voor de hero (huizen + drie groepen verlichte ramen +
                     spiegeling); de ramen gaan per groep aan via scroll-gestuurde animatie.
  * grachtenpanden.svg  statisch bestand (twee van de drie lichtgroepen, warm) voor de horizon boven de footer.
"""
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

INK = "#000000"
GRAPHITE = "#1c1c1e"
AMBER = "#ffd60a"
AMBER2 = "#ff9f0a"

# kleuren van het silhouet (ook gebruikt in site.css via klassen)
HOUSE_TONES = ("#08080a", "#0c0c0f", "#101014")
PANE = "#17171c"
LIGHTS = {"a": "#ffd98a", "b": "#ffae45", "c": "#a8d3ff"}

SKY_W = 1900   # breedte van de tekening (viewBox-eenheden)
SKY_H = 220    # hoogte; de kade ligt op y = 220


def mark(color=AMBER, cut=INK):
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
        '<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#2a2a2d"/><stop offset="1" stop-color="%s"/></linearGradient>'
        '<linearGradient id="m" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient></defs>'
        '<rect width="512" height="512" rx="116" fill="url(#g)"/>'
        '<rect x="1.5" y="1.5" width="509" height="509" rx="114.5" fill="none" stroke="#fff" stroke-opacity=".14" stroke-width="3"/>'
        '<g transform="translate(256 262) scale(.8) translate(-250 -256)">%s</g></svg>'
    ) % (INK, AMBER, AMBER2, mark("url(#m)", "#111113"))


def mark_inline():
    """Los beeldmerk zonder achtergrond, inline in header en footer. Kleur via CSS (currentColor)."""
    return '<svg viewBox="30 40 460 440" aria-hidden="true" focusable="false">%s</svg>' % mark("currentColor", INK)


def bottle_inline():
    """Glazen lachgasfles (zelfde vorm als in het beeldmerk) voor de tank-kaarten. Decoratief, geen tekst."""
    return ('<svg viewBox="0 0 64 130" focusable="false">'
            '<path class="bt-b" d="M25 8V4a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v4zM28 8h8v10h-8zM9 42c0-15 11-24 23-24s23 9 23 24v78a8 8 0 0 1-8 8H17a8 8 0 0 1-8-8z"/>'
            '<path class="bt-h" d="M14 45c0-10 5-17 10-20v98h-6a4 4 0 0 1-4-4z"/>'
            '<path class="bt-s" d="M50 45c0-10-4-16-8-19v97h4a4 4 0 0 0 4-4z"/>'
            '<path class="bt-x" d="M27 57l10 10m0-10l-10 10M27 77l10 10m0-10l-10 10M27 97l10 10m0-10l-10 10"/></svg>')


# ---------------------------------------------------------------------------
# Skyline
# ---------------------------------------------------------------------------
def _n(v):
    """Compact getal voor een SVG-pad."""
    s = ("%.1f" % v).rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def skyline_data(width=SKY_W, base=SKY_H, seed=247):
    """Rij grachtenpanden met trap-, hals-, klok-, tuit- en lijstgevels.

    Geeft (huizen, breedte). Elk huis: dict(d=pad, tone=0..2, panes=[(x, y, w, h)],
    lights=[(x, y, w, h, groep 1..3, kleur a/b/c)]).
    """
    rnd = random.Random(seed)
    houses, x = [], 0
    kinds = ["trap", "hals", "klok", "tuit", "lijst", "tuit", "klok", "hals"]
    last = None
    i = 0
    while x < width:
        w = rnd.choice([44, 48, 52, 56, 60, 66])
        h = rnd.randint(92, 148)
        kind = rnd.choice([k for k in kinds if k != last])
        last = kind
        top = base - h
        m = x + w / 2.0
        if kind == "trap":
            s, d = round(w / 8.0), 12
            mid = w - 6 * s
            dd = "M%s %dV%s" % (_n(x), base, _n(top)) + ("h%dv-%d" % (s, d)) * 3 + "h%d" % mid + ("v%dh%d" % (d, s)) * 3 + "V%dz" % base
            peak = top - d * 3
        elif kind == "hals":
            n = w * 0.21
            dd = "M%s %dV%sh3Q%s %s %s %sV%sL%s %sL%s %sV%sQ%s %s %s %sh3V%dz" % (
                _n(x), base, _n(top), _n(m - n), _n(top), _n(m - n), _n(top - 15), _n(top - 40), _n(m), _n(top - 53),
                _n(m + n), _n(top - 40), _n(top - 15), _n(m + n), _n(top), _n(x + w - 3), _n(top), base)
            peak = top - 53
        elif kind == "klok":
            dd = "M%s %dV%sC%s %s %s %s %s %sC%s %s %s %s %s %sC%s %s %s %s %s %sC%s %s %s %s %s %sV%dz" % (
                _n(x), base, _n(top),
                _n(x + w * .22), _n(top), _n(x + w * .16), _n(top - 28), _n(x + w * .30), _n(top - 32),
                _n(x + w * .34), _n(top - 48), _n(x + w * .42), _n(top - 50), _n(m), _n(top - 50),
                _n(x + w * .58), _n(top - 50), _n(x + w * .66), _n(top - 48), _n(x + w * .70), _n(top - 32),
                _n(x + w * .84), _n(top - 28), _n(x + w * .78), _n(top), _n(x + w), _n(top), base)
            peak = top - 50
        elif kind == "tuit":
            dd = "M%s %dV%sL%s %sh12L%s %sV%dz" % (_n(x), base, _n(top), _n(m - 6), _n(top - 40), _n(x + w), _n(top), base)
            peak = top - 40
        else:  # lijstgevel: rechte kroonlijst
            dd = "M%s %dV%sh-2v-5h%dv5h-2V%dz" % (_n(x), base, _n(top), w + 4, base)
            peak = None
        if peak is not None:  # hijsbalk
            dd += "M%s %sh3v8h-3z" % (_n(m - 1.5), _n(peak - 7))
        panes, lights = [], []

        def window(wx, wy, ww, wh, p=0.27):
            if rnd.random() < p:
                grp = rnd.choice([1, 1, 1, 1, 2, 2, 2, 3, 3, 3])
                col = rnd.choice("aaaaaaabbbc")
                lights.append((wx, wy, ww, wh, grp, col))
            else:
                panes.append((wx, wy, ww, wh))

        cols = 3 if w >= 56 else 2
        gap = w / (cols + 1.0)
        row = 0
        wy = top + 11
        while wy + 17 < base - 36:
            for c in range(cols):
                window(round(x + gap * (c + 1) - 4.5), round(wy), 9, 17)
            wy += 28
            row += 1
        # begane grond: deur en hoge ramen
        door = rnd.randrange(cols)
        for c in range(cols):
            gx = round(x + gap * (c + 1) - 4.5)
            if c == door:
                panes.append((gx - 1, base - 25, 11, 25))
            else:
                window(gx, base - 29, 9, 21, 0.2)
        if peak is not None and kind != "tuit":  # zolderraam
            window(round(m - 3.5), round(top - 21), 7, 11, 0.16)
        houses.append(dict(d=dd, tone=i % 3 if rnd.random() < .7 else rnd.randrange(3), panes=panes, lights=lights,
                           lamp=(x + w + 1) if i % 2 == 0 else None))
        x += w + 2
        i += 1
    return houses, x


LAMP_H = 27  # hoogte van de lantaarns langs de kade


def _lamps(houses, w):
    """x-posities van de lantaarns (op de naad tussen twee panden), binnen de tekening."""
    return [hs["lamp"] for hs in houses if hs["lamp"] is not None and hs["lamp"] < w - 4]


def _lamp_posts(xs, base=SKY_H):
    return "".join("M%s %dv-%dh1.6v%dz" % (_n(x - .8), base, LAMP_H - 3, LAMP_H - 3) for x in xs)


def _lamp_heads(xs, base=SKY_H, r=2.8):
    return "".join("M%s %sa%s %s 0 1 0 %s 0a%s %s 0 1 0-%s 0z" % (_n(x - r), _n(base - LAMP_H), r, r, _n(2 * r), r, r, _n(2 * r)) for x in xs)


def _lamp_streaks(xs, base=SKY_H):
    """Langgerekte weerspiegeling van elke lantaarn (alleen in de spiegeling gebruikt)."""
    return "".join("M%s %dv-%dh2.4v%dz" % (_n(x - 1.2), base - 4, LAMP_H + 30, LAMP_H + 30) for x in xs)


def _rects(rs):
    """Lijst rechthoeken als één compact pad (relatieve verplaatsingen)."""
    out, px, py = [], 0, 0
    for k, (x, y, w, h) in enumerate(sorted(rs)):
        out.append(("M%d %d" % (x, y) if k == 0 else "m%d %d" % (x - px, y - py)) + "h%dv%dh-%dz" % (w, h, w))
        px, py = x, y
    return "".join(out)


def _layers(houses):
    tones = ["", "", ""]
    panes = []
    lights = {}
    for hs in houses:
        tones[hs["tone"]] += hs["d"]
        panes += hs["panes"]
        for (x, y, w, h, g, c) in hs["lights"]:
            lights.setdefault((g, c), []).append((x, y, w, h))
    return tones, panes, lights


def horizon_html():
    """Inline horizon voor de hero: stad (huizen, donkere ruiten, drie lichtgroepen) plus spiegeling.

    Bevat geen tekst, geen id's en geen <title>; puur decoratief (aria-hidden).
    """
    houses, w = skyline_data()
    tones, panes, lights = _layers(houses)
    vb = 'viewBox="0 0 %d %d"' % (w, SKY_H)
    hs = "".join('<path class="t%d" d="%s"/>' % (i, d) for i, d in enumerate(tones))
    xs = _lamps(houses, w)

    def light_svg(g, extra=""):
        return '<svg class="hz-l l%d" %s>%s%s</svg>' % (g, vb, "".join(
            '<path class="w%s" d="%s"/>' % (c, _rects(lights[(g, c)])) for c in "abc" if (g, c) in lights), extra)

    def lights_html(extra):
        return light_svg(1, extra) + light_svg(2) + light_svg(3)

    city = '<svg class="hz-h" %s>%s<path class="pn" d="%s"/><path class="lp" d="%s"/></svg>%s' % (
        vb, hs, _rects(panes), _lamp_posts(xs), lights_html('<path class="wa" d="%s"/>' % _lamp_heads(xs)))
    refl = '<svg class="hz-h" %s>%s</svg>%s' % (vb, hs, lights_html('<path class="lr" d="%s"/>' % _lamp_streaks(xs)))
    return ('<div class="horizon" aria-hidden="true"><div class="hz-city">%s</div>'
            '<div class="hz-refl">%s</div></div>' % (city, refl))


def skyline_svg():
    """Statisch bestand voor de footer-horizon: zelfde tekening met zachte gloed. Alleen lichtgroep 1 en 2
    branden en alles is warm van toon: even ingetogen als de hero in rust, geen lichtslinger."""
    houses, w = skyline_data()
    tones, panes, lights = _layers(houses)
    body = "".join('<path d="%s" fill="%s"/>' % (d, HOUSE_TONES[i]) for i, d in enumerate(tones))
    body = '<g stroke="#fff" stroke-opacity=".13" stroke-width="1">%s</g>' % body
    body += '<path d="%s" fill="%s"/>' % (_rects(panes), PANE)
    xs = _lamps(houses, w)
    body += '<path d="%s" fill="#1d1d22"/>' % _lamp_posts(xs)
    lit = '<path d="%s" fill="%s"/>' % (_lamp_heads(xs), LIGHTS["a"])
    for c in "abc":
        rs = [r for (g, cc), v in lights.items() if cc == c and g != 3 for r in v]
        if rs:
            lit += '<path d="%s" fill="%s"/>' % (_rects(rs), LIGHTS["a" if c == "c" else c])
    body += '<g filter="url(#f)" opacity=".9">%s</g>%s' % (lit, lit)
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">'
            '<defs><filter id="f" x="-5%%" y="-20%%" width="110%%" height="140%%"><feGaussianBlur stdDeviation="3.2"/></filter></defs>'
            '%s</svg>') % (w, SKY_H, w, SKY_H, body)


def main():
    for name, data in (("logo.svg", logo_svg()), ("grachtenpanden.svg", skyline_svg())):
        with open(os.path.join(ROOT, "images", name), "w", encoding="utf-8") as f:
            f.write(data)
    print("merkbestanden gegenereerd")


if __name__ == "__main__":
    main()
