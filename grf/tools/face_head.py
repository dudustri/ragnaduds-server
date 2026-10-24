#!/usr/bin/env python3
"""Turn a cut-out head photo into a hairstyle head sprite (.spr), keeping the hairstyle's own .act.
The .act decides which of the sprite's frames is shown for each direction and animation, so only the frames are
redrawn: the face where the original frame shows the face, the back of the head where it shows the back.
Indexed frames (palette), like every head: use hair colour 0 in game, a hair dye recolours the palette.

  face_head.py <original head .spr> <output .spr> [cut-out head .png]
  default head: build/web/assets/photos/face_cap.png, cleaned like the website's Peco knight (make_web_assets.py)
"""
import os, struct, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
BACK = {3, 4, 6, 7, 8, 11, 12}   # frames that show the back of the head (male hairstyles: 0-2 front→side, 3-4 back)
SCALE = 1.15                      # a little bigger than the hair, so the face reads at sprite size


def read_frames(path):
    """[(w, h)] of the indexed frames of a SPR 2.1 (RLE)."""
    d = open(path, "rb").read()
    assert d[:2] == b"SP" and (d[3], d[2]) >= (2, 1), "need a SPR 2.1 file"
    n, o, sizes = struct.unpack_from("<H", d, 4)[0], 8, []
    for _ in range(n):
        w, h, size = struct.unpack_from("<HHH", d, o); o += 6 + size; sizes.append((w, h))
    return sizes


def default_head():
    sys.path.insert(0, os.path.join(HERE, "..", "..", "build", "web", "assets"))
    import make_web_assets   # its head_cutout(): your photo without the ceiling light and the t-shirt
    return make_web_assets.head_cutout()


def pixel(img, w, h):
    """Fit img into w×h, hard alpha (sprites have no half transparency)."""
    img = img.copy(); img.thumbnail((w, h), Image.LANCZOS)
    out = Image.new("RGBA", (w, h)); out.alpha_composite(img, ((w - img.width) // 2, h - img.height))
    a = out.getchannel("A").point(lambda v: 255 if v > 110 else 0); out.putalpha(a)
    return out


def back_of(head):
    """The back of the head: the cap colour on top, dark hair below, same outline."""
    out = head.copy(); px = out.load(); H = out.height
    for y in range(H):
        for x in range(out.width):
            if px[x, y][3]:
                px[x, y] = (52, 86, 160, 255) if y < H * .45 else (58, 38, 28, 255)
    return out


def rle(indexes):
    out, i = bytearray(), 0
    while i < len(indexes):
        if indexes[i] == 0:
            j = i
            while j < len(indexes) and indexes[j] == 0 and j - i < 255: j += 1
            out += bytes((0, j - i)); i = j
        else:
            out.append(indexes[i]); i += 1
    return bytes(out)


def build(orig_spr, out_spr, head):
    head = head.crop(head.getbbox())
    images = []
    for i, (w, h) in enumerate(read_frames(orig_spr)):
        W, H = round(w * SCALE), round(h * SCALE)
        images.append(pixel(back_of(head) if i in BACK else head, W, H))
    # one palette for all frames; index 0 = transparent
    sheet = Image.new("RGB", (sum(im.width for im in images), max(im.height for im in images)))
    x = 0
    for im in images: sheet.paste(im.convert("RGB"), (x, 0)); x += im.width
    q = sheet.quantize(254)
    pal = q.getpalette()[:254 * 3]
    body = bytearray()
    for im in images:
        qi = im.convert("RGB").quantize(palette=q)
        alpha = list(im.getchannel("A").get_flattened_data())
        idx = [0 if a == 0 else p + 1 for p, a in zip(qi.get_flattened_data(), alpha)]
        data = rle(idx)
        body += struct.pack("<HHH", im.width, im.height, len(data)) + data
    palette = bytearray((255, 0, 255, 0))   # index 0: transparent magenta
    for i in range(255):
        r, g, b = pal[i * 3:i * 3 + 3] if i < 254 else (0, 0, 0)
        palette += bytes((r, g, b, 0))
    with open(out_spr, "wb") as f:
        f.write(b"SP" + bytes((1, 2)) + struct.pack("<HH", len(images), 0) + bytes(body) + bytes(palette))
    return len(images)


if __name__ == "__main__":
    head = Image.open(sys.argv[3]).convert("RGBA") if len(sys.argv) > 3 else default_head()
    n = build(sys.argv[1], sys.argv[2], head)
    assert [s for s in read_frames(sys.argv[2])] and len(read_frames(sys.argv[2])) == n   # self-check: it reads back
    print(f"{sys.argv[2]}: {n} frames")
