#!/usr/bin/env python3
"""Generate the installer icons and picture (the website has its own: build/web/assets/make_web_assets.py).

  python3 make_assets.py

Sources:  ../web/assets/photos/ragnaduds.jpeg   (face → desktop/shortcut icon)
          duds_ok.jpeg                          (thumbs up → installer window picture)
Outputs:  ../../client/installer/  ragnaduds.ico, ragnaduds.png, duds_ok.png, duds_ok_bg.png
Crops are in source-pixel coordinates (left, top, right, bottom); tweak them if you replace a photo.
"""
import os
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
PHOTO = os.path.join(HERE, "..", "web", "assets", "photos", "ragnaduds.jpeg")
INST = os.path.join(HERE, "..", "..", "client", "installer")
FACE_CROP = (360, 400, 940, 980)       # square: eyes to beard, reads well even at 16 px
OK_CROP = (220, 330, 960, 1326)        # you + the whole stack of dessert cups on the table (zoomed out)


def rounded(im, radius):
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, *im.size), radius, fill=255)
    out = im.convert("RGBA"); out.putalpha(mask); return out


def main():
    os.makedirs(INST, exist_ok=True)
    face = Image.open(PHOTO).convert("RGB").crop(FACE_CROP)
    ok = Image.open(os.path.join(HERE, "duds_ok.jpeg")).convert("RGB").crop(OK_CROP)

    icon = rounded(face.resize((256, 256), Image.LANCZOS), 40)                 # desktop icons (rounded corners)
    icon.save(os.path.join(INST, "ragnaduds.png"))
    icon.save(os.path.join(INST, "ragnaduds.ico"), sizes=[(s, s) for s in (16, 24, 32, 48, 64, 128, 256)])
    ok.resize((240, 323), Image.LANCZOS).save(os.path.join(INST, "duds_ok.png"))   # installer window picture
    ok.resize((420, 565), Image.LANCZOS).save(os.path.join(INST, "duds_ok_bg.png"))   # Linux installer background

    for f in ("ragnaduds.png", "ragnaduds.ico", "duds_ok.png", "duds_ok_bg.png"):
        print(os.path.relpath(os.path.join(INST, f), HERE), os.path.getsize(os.path.join(INST, f)), "bytes")


if __name__ == "__main__":
    main()
