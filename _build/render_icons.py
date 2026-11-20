#!/usr/bin/env python3
"""Maakt favicon.ico van de door render_icons.js gemaakte favicon-PNG's en ruimt ze op. Vereist Pillow."""
import os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
srcs = [os.path.join(ROOT, "images", "favicon-%d.png" % s) for s in (48, 32, 16)]
ims = [Image.open(p).convert("RGBA") for p in srcs]
ims[0].save(os.path.join(ROOT, "favicon.ico"), format="ICO", sizes=[(48, 48), (32, 32), (16, 16)], append_images=ims[1:])
for p in srcs:
    os.remove(p)
# social-afbeelding compact opslaan
og = os.path.join(ROOT, "images", "opengraph-image.png")
Image.open(og).convert("RGB").save(og, optimize=True)
for n in ("icon-512.png", "icon-192.png", "apple-touch-icon.png"):
    p = os.path.join(ROOT, "images", n)
    Image.open(p).save(p, optimize=True)
print("favicon.ico gemaakt")
