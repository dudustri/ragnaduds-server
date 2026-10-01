#!/usr/bin/env python3
"""Generate the installer icons and picture (the website has its own: build/web/assets/make_web_assets.py).

  python3 make_assets.py

Sources:  ../web/assets/photos/ragnaduds.jpeg   (face → desktop/shortcut icon)
          duds_ok.jpeg                          (thumbs up → installer window picture)
          ../entrance_imageanime.jpeg           (hand on the lamp, anime → the warning screen before the login)
          ../landinggameiamgeanime.jpeg, ../landinggame2anime.jpeg   (waterfalls, fishing, anime → login screen, one per start)
Outputs:  ../../client/installer/  ragnaduds.ico, ragnaduds.png, duds_ok.png, duds_ok_bg.png
          ../../client/login/  entrance.bmp, 1.jpg/.bmp, 2.jpg/.bmp   (package_client.py puts them in the game)
Crops are in source-pixel coordinates (left, top, right, bottom); tweak them if you replace a photo.
The game screens are never cropped or edited: the original photo, resized, on black sides.
"""
import os
from PIL import Image, ImageDraw, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
PHOTO = os.path.join(HERE, "..", "web", "assets", "photos", "ragnaduds.jpeg")
INST = os.path.join(HERE, "..", "..", "client", "installer")
FACE_CROP = (360, 400, 940, 980)       # square: eyes to beard, reads well even at 16 px
OK_CROP = (220, 330, 960, 1326)        # you + the whole stack of dessert cups on the table (zoomed out)
ENTRANCE_PHOTO = os.path.join(HERE, "..", "entrance_imageanime.jpeg")
LOGIN_PHOTOS = [os.path.join(HERE, "..", f) for f in ("landinggameiamgeanime.jpeg", "landinggame2anime.jpeg")]
SCREENS = os.path.join(HERE, "..", "..", "client", "login")
SCREEN = (1024, 768)                    # the client stretches it to the window


def fit(path):
    """The original photo, only resized to the screen height (no crop, no effects), centred on black:
    the client stretches the picture to the window, so it must be 4:3 or a portrait photo gets squashed."""
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    W, H = SCREEN
    bg = Image.new("RGB", SCREEN, "black")
    scale = min(W / im.width, H / im.height)
    fg = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    bg.paste(fg, ((W - fg.width) // 2, (H - fg.height) // 2))
    return bg


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

    # game screens: warning screen before the login (BMP), and the login pictures the launcher picks from
    # (the 2026 client reads t_login.jpg, older ones bgi_temp.bmp: both formats of each)
    os.makedirs(SCREENS, exist_ok=True)
    fit(ENTRANCE_PHOTO).save(os.path.join(SCREENS, "entrance.bmp"))
    for i, p in enumerate(LOGIN_PHOTOS, 1):
        im = fit(p); im.save(os.path.join(SCREENS, f"{i}.bmp")); im.save(os.path.join(SCREENS, f"{i}.jpg"), quality=92)
    for f in sorted(os.listdir(SCREENS)):
        print(os.path.relpath(os.path.join(SCREENS, f), HERE), os.path.getsize(os.path.join(SCREENS, f)), "bytes")

    for f in ("ragnaduds.png", "ragnaduds.ico", "duds_ok.png", "duds_ok_bg.png"):
        print(os.path.relpath(os.path.join(INST, f), HERE), os.path.getsize(os.path.join(INST, f)), "bytes")


if __name__ == "__main__":
    main()
