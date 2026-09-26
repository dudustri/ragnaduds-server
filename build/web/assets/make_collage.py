#!/usr/bin/env python3
"""Build the website collage: your photo as the base, the other pictures cut out as die-cut stickers around you.

  python3 make_collage.py

Sources:  collage/main_base_collage.jpeg (base, kept as is) + collage/<other pictures>
Cutouts:  collage/cut/<name>.png   background removed once with rembg (pip install "rembg[cpu]"), then cached,
                                   so later runs don't need rembg. Delete a file there to cut it again.
Painted into the photo: the white potion (replaces the cup) and a drawn glowing halo over your head.
Outputs:  ../site/img/collage/     base.jpg, <name>.png stickers, layout.json (read by the page), collage.jpg (flattened)
Move things around by editing LAYOUT (coordinates are in base-photo pixels, 1200x1600).
"""
import json, os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "collage")
CUT = os.path.join(SRC, "cut")
OUT = os.path.join(HERE, "..", "site", "img", "collage")
BASE_W, BASE_H = 1200, 1600
STORE = 0.75                    # stickers/base are stored at 75% (page shows the collage ~600 px wide)

# name: source file, center x (+ center y, or bottom = where it stands on the floor), width, rotation (deg),
#       ground (casts a floor shadow), pixel (nearest scaling), crop (source box before cutting)
FLOOR = 1565                     # the deck line near the bottom of the photo
LEGS = (490, 770)                # x range of your legs: nothing on the floor goes there
LAYOUT = {
    # sky
    "valk":      dict(src="collage_valk.jpg",       x=160,  y=270,  w=175, rot=-7),
    "serpente":  dict(src="collage_serpentesuprema.png", x=978, y=1222, w=115, rot=4),
    # sides
    "goldenbug": dict(src="collage_goldenbug.png",  x=935, y=1362, w=72, rot=8),
    "aprendiz":  dict(src="collage_aprendiz.png",   x=130,  y=745,  w=160, rot=-8),
    "shura":     dict(src="collage_shura.jpg",      x=115,  y=1030, w=150, rot=-8),
    "poro":      dict(src="collage_poro.png",       x=100, y=1250,  w=88, rot=-6),
    "kafra":     dict(src="collage_kafra.jpeg",     x=1052, y=885, w=250, rot=3),
    "tao":       dict(src="collage_tao.png",        x=1120, y=1290, w=54,  rot=0,  pixel=True, crop=(34, 0, 80, 96)),
    # floor (left and right of the legs)
    "knight":    dict(src="collage_knight.png",     x=150,  bottom=FLOOR, w=175, rot=0,  ground=True),
    "muka":      dict(src="collage_muka.png",       x=310,  bottom=FLOOR - 5, w=100, rot=-5, ground=True),
    "card":      dict(src="card_drop.png",          x=440,  bottom=FLOOR + 15, w=60, rot=-10, ground=True, pixel=True),
    "card2":     dict(src="card_drop.png",          x=812,  bottom=FLOOR + 15, w=38, rot=12, ground=True, pixel=True),
    "poring":    dict(src="collage_poring.png",     x=890,  bottom=FLOOR + 10, w=86,  rot=0,  ground=True, pixel=True),
    "mvp":       dict(src="collage_mvp.jpeg",       x=1050, bottom=FLOOR, w=195, rot=3,  ground=True),
    "homunculus": dict(src="homunculus.png",        x=250,  y=1255, w=95,  rot=-6, pixel=True),
}
TITLE = dict(text="RAGNADUDS", y=222, size=46)   # small logo at the top
FONT = os.path.join(HERE, "fonts", "PressStart2P-Regular.ttf")


def cutout(name, spec):
    """Transparent version of a source picture (cached in collage/cut)."""
    os.makedirs(CUT, exist_ok=True)
    path = os.path.join(CUT, name + ".png")
    if not os.path.exists(path):
        im = Image.open(os.path.join(SRC, spec["src"]))
        if "crop" in spec: im = im.crop(spec["crop"])
        im = im.convert("RGBA")
        if im.getchannel("A").getextrema()[0] == 255 and (spec.get("pixel") or spec.get("flood")):   # sprite/icon on white
            from make_web_assets import cut_white
            im = cut_white(im)
        elif im.getchannel("A").getextrema()[0] == 255:          # no transparency yet → remove the background
            from rembg import remove, new_session             # anime model works best for RO artwork
            im = remove(im.convert("RGB"), session=new_session("isnet-anime"), post_process_mask=True)
        im.crop(im.getbbox()).save(path)
    return Image.open(path).convert("RGBA")


# The white potion replaces the cup in your hand, painted into the photo (no sticker), fingers stay in front.
CUP = (446, 848, 541, 983)       # the cup in main_base_collage.jpeg (left, top, right, bottom)
FINGERS_FROM = (479, 908)        # fingers are right of / below this point
JACKET = (540, 838, 626, 916)    # plain jacket patch used to paint the cup away
POTION = dict(x=500, bottom=1000, w=120)   # bottle center x, bottom (behind the fingers), width

def finger_mask(base):
    """Skin pixels over the cup = your fingers (they go back on top of the potion)."""
    l, t, r, b = CUP[0], CUP[1], CUP[2] + 70, CUP[3] + 40
    m = Image.new("L", base.size, 0); px, mp = base.load(), m.load()
    for y in range(max(t, FINGERS_FROM[1]), b):
        for x in range(max(l, FINGERS_FROM[0]), r):
            R, G, B = px[x, y]
            if R > 120 and G > 75 and R - G > 30 and R - B > 35: mp[x, y] = 255   # skin, not the brown cake
    return m.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(.8))

def potion_image():
    """Cut the potion drawing from its white background: close the outline, fill the silhouette, then open the
    two holes inside the handles again (they are background, not glass)."""
    im = Image.open(os.path.join(SRC, "white_potion.jpg")).convert("RGB")
    im = im.resize((im.width * 3, im.height * 3), Image.LANCZOS)
    ink = im.convert("L").point(lambda v: 255 if v < 215 else 0)                    # outline + colored parts
    closed = ink.filter(ImageFilter.MaxFilter(9))                                   # seal small gaps in the outline
    ImageDraw.floodfill(closed, (0, 0), 128)                                        # 128 = outside
    alpha = closed.point(lambda v: 0 if v == 128 else 255).filter(ImageFilter.MinFilter(9))
    out = im.convert("RGBA"); out.putalpha(alpha); out = out.crop(alpha.getbbox())
    W, H = out.size
    rgb = out.convert("RGB")
    for seed in ((int(W * .22), int(H * .40)), (int(W * .78), int(H * .40))):     # the hole inside each handle
        ImageDraw.floodfill(rgb, seed, (255, 0, 255), thresh=45)
    hole = rgb.point(lambda v: v).convert("RGB")
    a2 = out.getchannel("A").copy(); hp, ap = hole.load(), a2.load()
    for y in range(H):
        for x in range(W):
            if hp[x, y] == (255, 0, 255): ap[x, y] = 0
    out.putalpha(a2)
    out.putalpha(out.getchannel("A").filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(.7)))
    return out

def embed_potion(base):
    fingers = finger_mask(base)
    out = base.copy()
    l, t, r, b = CUP; jacket = base.crop(JACKET).filter(ImageFilter.GaussianBlur(1.5))
    fill = Image.new("RGB", (r - l, b - t))                         # paint the cup away with jacket texture
    for y in range(0, fill.height, jacket.height):
        for x in range(0, fill.width, jacket.width): fill.paste(jacket, (x, y))
    soft = Image.new("L", fill.size, 0); ImageDraw.Draw(soft).rectangle((3, 3, fill.width - 4, fill.height - 4), fill=255)
    out.paste(fill, (l, t), soft.filter(ImageFilter.GaussianBlur(2)))
    pot = potion_image(); w = POTION["w"]; h = round(pot.height * w / pot.width)
    pot = pot.resize((w, h), Image.LANCZOS)
    from PIL import ImageEnhance                                    # match the night photo: dimmer, warmer, softer
    a = pot.getchannel("A")
    pot = ImageEnhance.Brightness(pot.convert("RGB")).enhance(.86)
    pot = Image.blend(pot, Image.new("RGB", pot.size, (255, 196, 150)), .08).filter(ImageFilter.GaussianBlur(.4)).convert("RGBA")
    pot.putalpha(a)
    shade = Image.new("RGBA", pot.size, (0, 0, 0, 0)); shade.putalpha(pot.getchannel("A").point(lambda v: v * .5))
    shade = shade.filter(ImageFilter.GaussianBlur(4))
    o = out.convert("RGBA"); pos = (POTION["x"] - w // 2, POTION["bottom"] - h)
    o.alpha_composite(shade, (pos[0] + 4, pos[1] + 5)); o.alpha_composite(pot, pos)
    o = o.convert("RGB")
    o.paste(base, (0, 0), fingers)                                  # fingers back on top
    return o


# Angel halo over your head: drawn as light (no source picture), painted into the photo.
HALO = dict(x=560, y=380, w=190, rot=-3)   # center x/y, width, tilt

def light_halo(base):
    """Draw a glowing halo: thin gold-to-white ring, back half dimmer (tilted in 3D), soft bloom that tints the
    sky, and a faint warm light on the hair under it. Blended as light (screen), so it glows instead of sitting on top."""
    from PIL import ImageChops
    S = 4                                                           # draw at 4x, then scale down (smooth edges)
    rx, ry = HALO["w"] / 2, HALO["w"] * .135; pad = 70
    W, H = int(2 * (rx + pad)), int(2 * (ry + pad))
    core = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0)); d = ImageDraw.Draw(core)
    box = ((pad) * S, (pad) * S, (W - pad) * S, (H - pad) * S)
    for start, end, alpha in ((180, 360, 150), (0, 180, 255)):      # back (upper) arc dimmer, front arc bright
        d.arc(box, start, end, fill=(236, 150, 30, alpha), width=7 * S)
        d.arc(box, start, end, fill=(255, 196, 64, alpha), width=4 * S)
        d.arc(box, start, end, fill=(255, 238, 170, alpha), width=1 * S)
    core = core.resize((W, H), Image.LANCZOS).rotate(-HALO["rot"], resample=Image.BICUBIC)
    def light(layer, blur, strength, color=None):
        g = layer.filter(ImageFilter.GaussianBlur(blur)) if blur else layer
        rgb = Image.new("RGB", g.size, color) if color else g.convert("RGB")
        a = g.getchannel("A").point(lambda v: min(255, int(v * strength)))
        return Image.composite(rgb, Image.new("RGB", g.size, (0, 0, 0)), a)   # premultiplied light
    x0, y0 = int(HALO["x"] - W / 2), int(HALO["y"] - H / 2)
    o = base.convert("RGBA")
    def glow(blur, alpha, color):                                   # golden haze (tints the sky gold, not white)
        g = core.filter(ImageFilter.GaussianBlur(blur)); lay = Image.new("RGBA", g.size, color)
        lay.putalpha(g.getchannel("A").point(lambda v: min(255, int(v * alpha)))); return lay
    for blur, alpha, color in ((28, 1.7, (255, 160, 40)), (11, 1.8, (255, 185, 60)), (3, 1.3, (255, 205, 100))):
        o.alpha_composite(glow(blur, alpha, color), (x0, y0))
    o.alpha_composite(core, (x0, y0))                               # the ring itself
    region = o.convert("RGB").crop((x0, y0, x0 + W, y0 + H))
    region = ImageChops.screen(region, light(core, 2, .35, (255, 230, 170)))   # a touch of real light on top
    out = o.convert("RGB"); out.paste(region, (x0, y0))
    # warm light spilling onto the top of the hair
    hw, hh = int(rx * 1.7), int(rx * .7)
    spill = Image.new("RGBA", (hw + 120, hh + 120), (0, 0, 0, 0))
    ImageDraw.Draw(spill).ellipse((60, 60, 60 + hw, 60 + hh), fill=(255, 180, 90, 70))
    sx, sy = HALO["x"] - spill.width // 2, HALO["y"] + int(ry) + 18
    r2 = out.crop((sx, sy, sx + spill.width, sy + spill.height))
    r2 = ImageChops.screen(r2, light(spill, 22, 1.0))
    out.paste(r2, (sx, sy))
    return out


def embed_halo(base):
    return light_halo(base)


def sticker(im, width, pixel, border):
    """Scale to width and add a white die-cut border around the shape."""
    h = round(im.height * width / im.width)
    im = im.resize((width, h), Image.NEAREST if pixel else Image.LANCZOS)
    pad = border + 2
    canvas = Image.new("RGBA", (width + 2 * pad, h + 2 * pad), (0, 0, 0, 0)); canvas.alpha_composite(im, (pad, pad))
    a = canvas.getchannel("A").point(lambda v: 255 if v > 90 else 0)
    edge = a.filter(ImageFilter.MaxFilter(2 * border + 1)).filter(ImageFilter.GaussianBlur(1))
    out = Image.new("RGBA", canvas.size, (255, 255, 255, 0)); out.putalpha(edge)
    out.alpha_composite(canvas)
    return out


def title_image(scale):
    font = ImageFont.truetype(FONT, round(TITLE["size"] * scale))
    x0, y0, x1, y1 = font.getbbox(TITLE["text"]); off = max(1, round(5 * scale))
    im = Image.new("RGBA", (x1 + 3 * off, y1 + 3 * off), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.text((2 * off, 2 * off), TITLE["text"], font=font, fill=(0, 0, 0, 255))
    d.text((off, off), TITLE["text"], font=font, fill=(122, 62, 18, 255))
    d.text((0, 0), TITLE["text"], font=font, fill=(255, 209, 102, 255))
    return im


def main():
    os.makedirs(OUT, exist_ok=True)
    base = Image.open(os.path.join(SRC, "main_base_collage.jpeg")).convert("RGB").resize((BASE_W, BASE_H), Image.LANCZOS)
    base = embed_halo(embed_potion(base))
    base.resize((round(BASE_W * STORE), round(BASE_H * STORE)), Image.LANCZOS).save(os.path.join(OUT, "base.jpg"), quality=86)
    flat = base.convert("RGBA")
    import time
    layout = {"v": int(time.time()), "base": "img/collage/base.jpg", "w": BASE_W, "h": BASE_H, "stickers": []}   # v: cache-buster for the page

    order = sorted(LAYOUT, key=lambda n: LAYOUT[n].get("bottom", LAYOUT[n].get("y")))   # lower = in front
    for name in order:
        spec = LAYOUT[name]; pixel = spec.get("pixel", False)
        cut = cutout(name, spec)
        big = sticker(cut, spec["w"], pixel, border=7)
        if "bottom" in spec: spec["y"] = spec["bottom"] - big.height // 2
        # flattened collage: floor shadow + rotated sticker + drop shadow
        rot = big.rotate(-spec["rot"], resample=Image.BICUBIC, expand=True)
        if spec.get("ground"):
            sw, sh = round(spec["w"] * .9), round(spec["w"] * .16)
            sh_im = Image.new("RGBA", (sw + 40, sh + 40), (0, 0, 0, 0))
            ImageDraw.Draw(sh_im).ellipse((20, 20, 20 + sw, 20 + sh), fill=(0, 0, 0, 120))
            sh_im = sh_im.filter(ImageFilter.GaussianBlur(10))
            flat.alpha_composite(sh_im, (spec["x"] - sh_im.width // 2, spec["y"] + rot.height // 2 - sh_im.height // 2 - 10))
        shadow = Image.new("RGBA", rot.size, (0, 0, 0, 0)); shadow.putalpha(rot.getchannel("A").point(lambda v: v * .45))
        shadow = shadow.filter(ImageFilter.GaussianBlur(8))
        pos = (spec["x"] - rot.width // 2, spec["y"] - rot.height // 2)
        flat.alpha_composite(shadow, (pos[0] + 8, pos[1] + 12)); flat.alpha_composite(rot, pos)
        # page sticker (unrotated; the page rotates it)
        small = sticker(cut, round(spec["w"] * STORE), pixel, border=5)
        small.save(os.path.join(OUT, name + ".png"), optimize=True)
        layout["stickers"].append(dict(name=name, img=f"img/collage/{name}.png", x=spec["x"], y=spec["y"],
                                       w=round(spec["w"] * big.width / (spec["w"] + 0)), rot=spec["rot"],
                                       ground=spec.get("ground", False), pixel=pixel))

    t = title_image(1.0)
    flat.alpha_composite(t, ((BASE_W - t.width) // 2, TITLE["y"] - t.height // 2))
    title_image(STORE * 2).save(os.path.join(OUT, "title.png"))
    layout["title"] = dict(img="img/collage/title.png", y=TITLE["y"], w=t.width, h=t.height)
    for name, spec in LAYOUT.items():                               # keep the legs free
        if spec.get("ground") and LEGS[0] < spec["x"] < LEGS[1]: print("WARNING:", name, "stands on the legs")
    flat.convert("RGB").save(os.path.join(OUT, "collage.jpg"), quality=88)
    json.dump(layout, open(os.path.join(OUT, "layout.json"), "w"), indent=1)
    for f in sorted(os.listdir(OUT)):
        print(f"img/collage/{f}", os.path.getsize(os.path.join(OUT, f)), "bytes")


if __name__ == "__main__":
    main()
