#!/usr/bin/env python3
"""Generate the website images (everything in ../site/img except the collage).

  python3 make_web_assets.py

Sources (this folder):  photos/ragnaduds.jpeg     your photo → favicon, link preview, NPC face
                        photos/face_cap.png       your head + cap cut out of it → head on the Peco knight
                        sprites/pecopeco_mount.png, sprites/orc.png, sprites/orc_map_background.jpeg
Outputs:                ../site/img/  favicon.ico, favicon-32.png, ragnaduds-256.png, ragnaduds-npc.png,
                                      peco-duds.png, orc.png, orc-map.jpg     and ../site/favicon.ico
Crops/boxes are in source-pixel coordinates (left, top, right, bottom); tweak them if you replace a picture.
"""
import os
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, "..", "site")
IMG = os.path.join(SITE, "img")
PHOTO = os.path.join(HERE, "photos", "ragnaduds.jpeg")
SPRITES = os.path.join(HERE, "sprites")
FACE_CROP = (360, 400, 940, 980)        # square: eyes to beard (pixelated NPC face)
ICON_CROP = (215, 150, 1085, 1020)      # wider square: whole head with the cap (round icon)


def pixelated(im, grid, size):
    return im.resize((grid, grid), Image.LANCZOS).resize((size, size), Image.NEAREST)


def round_icon(head, size):
    big = head.resize((size * 4, size * 4), Image.LANCZOS)
    mask = Image.new("L", big.size, 0); ImageDraw.Draw(mask).ellipse((0, 0, *big.size), fill=255)
    out = big.convert("RGBA"); out.putalpha(mask); return out.resize((size, size), Image.LANCZOS)


# Knight-on-Peco game sprite (pecopeco_mount.png, 150x150): sword added, head swapped for your head + cap.
# photos/face_cap.png = head with cap cut out of ragnaduds.jpeg (rembg "isnet-general-use", crop (290,150,1010,1090)).
PECO_HEAD = (49, 12, 85, 53)            # box for the new head in sprite pixels
def head_cutout():
    im = Image.open(os.path.join(HERE, "photos", "face_cap.png")).convert("RGBA"); W, H = im.size; px = im.load()
    for y in range(H):
        for x in range(W):
            r, g, b, a = px[x, y]
            if not a: continue
            light = y < H * .3 and min(r, g, b) > 200                        # ceiling light left by the cutout
            shirt = y > H * .8 and b >= r                                     # navy t-shirt under the beard
            if light or shirt: px[x, y] = (0, 0, 0, 0)
            elif y < H * .4 and b > r + 2 and b >= g:                          # the cap: brighter blue so it reads at sprite size
                px[x, y] = (min(255, int(r * 1.3) + 25), min(255, int(g * 1.4) + 35), min(255, int(b * 1.7) + 60), a)
    return im.crop(im.getbbox())


def make_peco():
    sprite = Image.open(os.path.join(SPRITES, "pecopeco_mount.png")).convert("RGBA")
    px = sprite.load()
    for y in range(0, 46):                                         # erase the original head + hair
        for x in range(50, 87): px[x, y] = (0, 0, 0, 0)
    out = sprite.copy(); d = ImageDraw.Draw(out)
    # sword in the knight's hand: blade pointing up-right, gold crossguard, brown grip
    K, S, SL, G, B = (40, 30, 40, 255), (196, 204, 218, 255), (244, 247, 252, 255), (236, 190, 70, 255), (110, 66, 34, 255)
    d.line((88, 66, 112, 30), fill=K, width=5); d.line((88, 66, 112, 30), fill=S, width=3); d.line((89, 64, 112, 31), fill=SL, width=1)
    d.polygon([(110, 29), (116, 24), (114, 33)], fill=K); d.polygon([(111, 30), (115, 26), (113, 32)], fill=SL)   # tip
    d.line((82, 62, 94, 70), fill=K, width=4); d.line((83, 62, 93, 69), fill=G, width=2)                           # crossguard
    d.line((86, 68, 82, 75), fill=K, width=4); d.line((86, 68, 82, 74), fill=B, width=2)                           # grip
    d.point((81, 76), fill=G)                                                                                      # pommel
    # head: pixelated cutout with a dark outline
    l, t, r, b = PECO_HEAD; head = head_cutout()
    w = r - l; h = round(head.height * w / head.width)
    small = head.resize((w, h), Image.LANCZOS)
    a = small.getchannel("A").point(lambda v: 255 if v > 110 else 0); small.putalpha(a)
    small = small.convert("RGB").quantize(40).convert("RGBA"); small.putalpha(a)
    ring = Image.new("RGBA", (w + 2, h + 2), (0, 0, 0, 0)); edge = Image.new("L", (w + 2, h + 2), 0); edge.paste(a, (1, 1))
    ring.putalpha(edge.filter(ImageFilter.MaxFilter(3))); ring = Image.composite(Image.new("RGBA", ring.size, (40, 22, 16, 255)), ring, ring.getchannel("A"))
    top = b - h
    out.alpha_composite(ring, (l - 1, top - 1)); out.alpha_composite(small, (l, top))
    return out.crop(out.getbbox())


BG_ORC = (386, 151, 423, 205)           # the orc standing in orc_map_background.jpeg
def remove_bg_orc(im):
    """Paint the background orc out: blend the ground right next to it (left + right copies), soft edges."""
    l, t, r, b = BG_ORC; w = r - l; pad = 6
    box = (l - pad, t - pad, r + pad, b + pad)
    left = im.crop((box[0] - w, box[1], box[2] - w, box[3]))
    right = im.crop((box[0] + w, box[1], box[2] + w, box[3]))
    fill = Image.blend(left, right, .5)
    mask = Image.new("L", fill.size, 0); ImageDraw.Draw(mask).rectangle((pad // 2, pad // 2, fill.width - pad // 2, fill.height - pad // 2), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(pad / 2))
    out = im.copy(); out.paste(fill, box[:2], mask); return out


def cut_white(im, tol=40):
    """Flood-fill the white background from the borders to transparency (crisp game sprites)."""
    im = im.convert("RGBA"); W, H = im.size; px = im.load(); seen = set()
    stack = [(x, y) for x in range(W) for y in (0, H - 1)] + [(x, y) for y in range(H) for x in (0, W - 1)]
    while stack:
        x, y = stack.pop()
        if (x, y) in seen or not (0 <= x < W and 0 <= y < H): continue
        seen.add((x, y)); r, g, b, a = px[x, y]
        if a and min(r, g, b) < 255 - tol: continue
        px[x, y] = (0, 0, 0, 0); stack += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    return im.crop(im.getbbox())


def main():
    os.makedirs(IMG, exist_ok=True)
    photo = Image.open(PHOTO).convert("RGB")
    pixelated(photo.crop(FACE_CROP), 48, 192).save(os.path.join(IMG, "ragnaduds-npc.png"))   # NPC dialog face
    head = photo.crop(ICON_CROP)                                                               # round icon with the cap
    round_icon(head, 32).save(os.path.join(IMG, "favicon-32.png"))
    for path in (os.path.join(IMG, "favicon.ico"), os.path.join(SITE, "favicon.ico")):
        round_icon(head, 256).save(path, sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    round_icon(head, 256).save(os.path.join(IMG, "ragnaduds-256.png"))                       # link previews
    make_peco().save(os.path.join(IMG, "peco-duds.png"))                                     # mini game: you
    cut_white(Image.open(os.path.join(SPRITES, "orc.png"))).save(os.path.join(IMG, "orc.png"))  # mini game: the orc
    remove_bg_orc(Image.open(os.path.join(SPRITES, "orc_map_background.jpeg")).convert("RGB")).save(
        os.path.join(IMG, "orc-map.jpg"), quality=90)                                        # mini game: the map
    for f in sorted(os.listdir(IMG)):
        p = os.path.join(IMG, f)
        if os.path.isfile(p): print("site/img/" + f, os.path.getsize(p), "bytes")


if __name__ == "__main__":
    main()
