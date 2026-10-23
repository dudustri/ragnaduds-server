#!/usr/bin/env python3
"""README banner: "RAGNADUDS" like the website logo (Press Start 2P, gold, brown + black pixel shadows) with the
Knight-on-Peco sprite next to it. Transparent PNG, so it works on GitHub's light and dark themes.
Output: docs/img/ragnaduds-banner.png"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "..", "docs", "img", "ragnaduds-banner.png")
SIZE, SH1, SH2 = 48, 4, 8               # font 48 px (6 × the font's 8 px grid); shadows like the site's 3/6 px at 40 px
GOLD, BROWN, BLACK = (255, 209, 102, 255), (122, 62, 18, 255), (0, 0, 0, 255)

font = ImageFont.truetype(os.path.join(HERE, "fonts", "PressStart2P-Regular.ttf"), SIZE)
text = "RAGNADUDS"
l, t, r, b = font.getbbox(text)
tw, th = r - l + SH2, b - t + SH2
peco = Image.open(os.path.join(HERE, "sprites", "pecopeco_mount.png")).convert("RGBA")
peco = peco.crop(peco.getbbox())
GAP = 24
W, H = tw + GAP + peco.width, max(th, peco.height)
img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
y = (H - th) // 2 - t
for dx, col in ((SH2, BLACK), (SH1, BROWN), (0, GOLD)):   # back to front, like text-shadow
    d.text((dx - l, y + dx), text, font=font, fill=col)
img.alpha_composite(peco, (tw + GAP, (H - peco.height) // 2))
img.save(OUT)
print(OUT, img.size)
