#!/usr/bin/env python3
"""Casino animations for the Comodo Casino NPCs (deploy/casino.txt).

Every frame is drawn here and saved as a PNG "cutin" (the client shows one illustration at a time; the NPC script
plays an animation by swapping frames about 10 times a second). Output goes to client/grf_casino/, which
package_client.py packs into ragnaduds_casino.grf for the renewal client (players get it from the launcher update).
The sounds are made by build_casino_sounds.py into the same folder.

    python3 casino/build_casino_art.py [--client ~/ragnaduds/Renewal] [--preview out.png]

Everything is drawn in a base layout and scaled by SCALE per game (twice the first size, but never taller than
MAX_H, so it fits a 1080p game window). The slot machine symbols are the client's own pictures (card
illustrations, item pictures), read from its GRFs.
Frame names (the NPC script builds them the same way):
  roulette   duds_rl_idle, duds_rl_spin00..15, duds_rl_<n>_0..5   (n = 0..36, frame 5 = final with the result)
  slots      duds_sl_idle, duds_sl_spin0..2, duds_sl_a<r1>, duds_sl_b<r1><r2>, duds_sl_c<r1><r2><r3>, duds_sl_jp0..3
  blackjack  duds_bj_table, duds_bj_shuf0..3, duds_bj_back, duds_bj_backh, duds_bj_edge, duds_bj_c<card>h, duds_bj_c<card>
             (card = rank*4 + suit, rank 0 = A .. 12 = K, suit 0 hearts, 1 diamonds, 2 spades, 3 clubs)
  lottery    duds_lt_idle, duds_lt_tumble0..5, duds_lt_ball1..25
  bicho      duds_jb_table, duds_jb_spin0..5, duds_jb_<group 1..25>_<prize 1..5>
"""
import argparse, io, math, os, random, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "client"))
import grf  # noqa: E402

OUT = os.path.join(ROOT, "client", "grf_casino", "data", "texture", "유저인터페이스", "illust")
UI = "data\\texture\\유저인터페이스"
SANS = "/usr/share/fonts/liberation-sans-fonts/LiberationSans-Bold.ttf"
SERIF = "/usr/share/fonts/liberation-serif-fonts/LiberationSerif-Bold.ttf"
GOLD, GOLD_D, CREAM = (255, 209, 102), (160, 110, 30), (246, 236, 210)
FELT, FELT_D = (22, 110, 60), (12, 70, 38)
RED, BLACK, GREEN = (200, 30, 40), (28, 28, 34), (20, 140, 70)
K = 1.6   # size of everything on screen; set per game by main() (SCALE)
MAX_H = 900   # px: the tallest picture still fits a 1080p game window
SCALE = {"blackjack": 3.2, "slots": 3.2, "lottery": 3.0, "roulette": 2.45, "bicho": 2.5}   # 2x the first size, capped by MAX_H


def z(v):
    """A base-layout length or coordinate, scaled."""
    return int(round(v * K))


def Z(*vs):
    return tuple(z(v) for v in vs)


# the same order and payout table as the NPC script
WHEEL = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22,
         18, 29, 7, 28, 12, 35, 3, 26]
REDS = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
# slot symbols: (client picture, name); index = the script's symbol number
SYMBOLS = [("collection\\빨간포션.bmp", "Red Potion"), ("collection\\사과.bmp", "Apple"),
           ("cardbmp\\포링카드.bmp", "Poring"), ("cardbmp\\포포링카드.bmp", "Poporing"),
           ("cardbmp\\엔젤링카드.bmp", "Angeling"), ("cardbmp\\데빌링카드.bmp", "Deviling"),
           ("cardbmp\\금도둑벌레카드.bmp", "Golden Thief Bug")]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
SUITS = ["♥", "♦", "♠", "♣"]

saved = {}


def font(path, size):
    return ImageFont.truetype(path, z(size))


def save(img, name):
    """Palette PNG with transparency: small files, the client reads them like the official PNG cutins."""
    q = img.convert("RGBA").quantize(colors=128, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE)
    buf = io.BytesIO()
    q.save(buf, "PNG", optimize=True)
    saved[name] = buf.getvalue()


def frame_box(w, h, fill=(34, 29, 51), border=(107, 79, 42)):
    """The RagnaDuds look: dark panel, brown/gold border, rounded corners (transparent outside). w, h: base units."""
    W, H = z(w), z(h)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, W - 1, H - 1), z(14), fill=border)
    d.rounded_rectangle((z(4), z(4), W - 1 - z(4), H - 1 - z(4)), z(11), fill=GOLD_D)
    d.rounded_rectangle((z(7), z(7), W - 1 - z(7), H - 1 - z(7)), z(9), fill=fill)
    return img


def text_c(d, xy, s, f, fill, stroke=0, stroke_fill=(0, 0, 0)):
    d.text(Z(*xy), s, font=f, fill=fill, anchor="mm", stroke_width=z(stroke) if stroke else 0, stroke_fill=stroke_fill)


def felt(w, h):
    img = frame_box(w, h, fill=FELT)
    W, H = img.size
    v = Image.new("L", (W, H), 0)   # soft vignette on the felt
    ImageDraw.Draw(v).ellipse((-W * 0.2, -H * 0.2, W * 1.2, H * 1.2), fill=255)
    v = v.filter(ImageFilter.GaussianBlur(z(40)))
    dark = Image.new("RGBA", (W, H), FELT_D + (255,))
    inner = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    inner.paste(dark, (0, 0), Image.eval(v, lambda p: 255 - p))
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).rounded_rectangle((z(7), z(7), W - 1 - z(7), H - 1 - z(7)), z(9), fill=255)
    img.paste(Image.alpha_composite(img, inner), (0, 0), mask)
    return img


# ------------------------------------------------------------------ roulette
RW, RH, RC = 320, 368, (160, 160)   # base units
WHEEL_D = 246


def roulette_wheel():
    """The turning part (2x supersampled), pocket i centred at i*360/37 degrees clockwise from the top."""
    S = 2 * K
    size = int(WHEEL_D * S)
    c = size / 2
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    step = 360 / 37
    r_out, r_num, r_pock, r_cone = 122 * S, 103 * S, 86 * S, 44 * S
    w = max(1, int(S))
    for i, n in enumerate(WHEEL):
        a0 = -90 + i * step - step / 2
        col = GREEN if n == 0 else (RED if n in REDS else BLACK)
        d.pieslice((c - r_out, c - r_out, c + r_out, c + r_out), a0, a0 + step, fill=col, outline=GOLD_D, width=w)
    d.ellipse((c - r_num, c - r_num, c + r_num, c + r_num), fill=(70, 40, 20))
    for i, n in enumerate(WHEEL):   # pockets: darker, with gold frets
        a0 = -90 + i * step - step / 2
        col = (10, 90, 50) if n == 0 else ((130, 20, 28) if n in REDS else (16, 16, 20))
        r = r_num - 3 * S
        d.pieslice((c - r, c - r, c + r, c + r), a0, a0 + step, fill=col, outline=GOLD, width=w)
    for k in range(20):   # inner cone (wood) + turret
        r = r_pock - (r_pock - r_cone) * k / 20
        t = k / 20
        d.ellipse((c - r, c - r, c + r, c + r), fill=(int(120 + 60 * t), int(70 + 40 * t), int(30 + 20 * t)))
    d.ellipse((c - r_cone, c - r_cone, c + r_cone, c + r_cone), fill=(150, 100, 40))
    for k in range(4):
        a = math.radians(45 + k * 90)
        d.line((c, c, c + math.cos(a) * 40 * S, c + math.sin(a) * 40 * S), fill=GOLD, width=int(5 * S))
    d.ellipse((c - 13 * S, c - 13 * S, c + 13 * S, c + 13 * S), fill=GOLD, outline=GOLD_D, width=int(2 * S))
    d.ellipse((c - 6 * S, c - 6 * S, c + 6 * S, c + 6 * S), fill=(255, 240, 190))
    f = ImageFont.truetype(SANS, int(11 * S))   # numbers, written outward on the number ring
    for i, n in enumerate(WHEEL):
        ang = i * step
        t = Image.new("RGBA", (int(30 * S), int(18 * S)), (0, 0, 0, 0))
        ImageDraw.Draw(t).text((15 * S, 9 * S), str(n), font=f, fill=(255, 255, 255), anchor="mm")
        t = t.rotate(-ang, resample=Image.BICUBIC, expand=True)
        rr = (r_out + r_num) / 2
        x = c + rr * math.sin(math.radians(ang)) - t.width / 2
        y = c - rr * math.cos(math.radians(ang)) - t.height / 2
        img.alpha_composite(t, (int(x), int(y)))
    return img


def roulette_base():
    img = felt(RW, RH)
    d = ImageDraw.Draw(img)
    cx, cy = RC
    d.ellipse(Z(cx - 155, cy - 155, cx + 155, cy + 155), fill=(92, 52, 22), outline=GOLD_D, width=z(3))   # bowl rim
    d.ellipse(Z(cx - 140, cy - 140, cx + 140, cy + 140), fill=(58, 32, 14))                              # ball track
    d.ellipse(Z(cx - 124, cy - 124, cx + 124, cy + 124), fill=(40, 22, 10))
    return img


def roulette_frame(base, wheel, w_ang, ball=None, label=None):
    img = base.copy()
    wh = wheel.rotate(-w_ang, resample=Image.BICUBIC).resize((z(WHEEL_D), z(WHEEL_D)), Image.LANCZOS)
    img.alpha_composite(wh, (z(RC[0]) - z(WHEEL_D) // 2, z(RC[1]) - z(WHEEL_D) // 2))
    d = ImageDraw.Draw(img)
    if ball:
        b_ang, r = ball
        x = RC[0] + r * math.sin(math.radians(b_ang))
        y = RC[1] - r * math.cos(math.radians(b_ang))
        d.ellipse(Z(x - 6, y - 4, x + 8, y + 9), fill=(0, 0, 0, 90))                 # shadow
        d.ellipse(Z(x - 6, y - 6, x + 6, y + 6), fill=(245, 245, 245), outline=(150, 150, 150))
        d.ellipse(Z(x - 3, y - 4, x, y - 1), fill=(255, 255, 255))
    if label is not None:
        n = label
        col = GREEN if n == 0 else (RED if n in REDS else BLACK)
        name = "GREEN" if n == 0 else ("RED" if n in REDS else "BLACK")
        d.rounded_rectangle(Z(60, 322, RW - 60, 356), z(8), fill=col, outline=GOLD, width=z(3))
        text_c(d, (RW / 2, 339), f"{n}  {name}", font(SANS, 22), (255, 255, 255), 2)
    else:
        text_c(d, (RW / 2, 339), "RAGNADUDS ROULETTE", font(SANS, 16), GOLD, 2)
    return img


def build_roulette():
    wheel, base = roulette_wheel(), roulette_base()
    save(roulette_frame(base, wheel, 0), "duds_rl_idle")
    for f in range(16):   # seamless loop: the wheel turns once, the ball goes 3 times around the other way
        save(roulette_frame(base, wheel, f * 22.5, (-f * 67.5, 131)), f"duds_rl_spin{f:02d}")
    step, L, w_end = 360 / 37, 6, 150.0
    ease = lambda t: 1 - (1 - t) ** 2   # noqa: E731
    for n in range(37):
        target = (w_end + WHEEL.index(n) * step) % 360           # where the pocket is when the wheel stops
        dist = ((0 - target) % 360) + 360                        # ball: one more lap, counter-clockwise
        for k in range(1, L + 1):
            t = k / L
            drop = min(1.0, max(0.0, (t - 0.35) / 0.65))
            r = 131 - 36 * (drop * drop * (3 - 2 * drop))
            save(roulette_frame(base, wheel, w_end * ease(t), (-dist * ease(t), r), n if k == L else None),
                 f"duds_rl_{n}_{k - 1}")


# ------------------------------------------------------------------ slots
SW, SH = 330, 250
WIN_X, WIN_Y, WIN_W, WIN_H = (34, 125, 216), 70, 80, 112
SYM = 70   # symbol tile, base units


def client_index(client):
    idx = {}
    for g in ("ragnaduds.grf", "2026.grf", "data.grf"):
        p = os.path.join(client, g)
        if not os.path.exists(p):
            continue
        f, es = grf.entries(p)
        for n, e in es.items():
            idx.setdefault(n.decode("cp949", "replace").lower(), (f, e))
    return idx


def symbol_images(client):
    idx = client_index(client)
    out = []
    for path, _ in SYMBOLS:
        key = f"{UI}\\{path}".lower()
        if key not in idx:
            sys.exit(f"missing in the client GRFs: {key}")
        im = Image.open(io.BytesIO(grf.read(*idx[key]))).convert("RGBA")
        px = im.load()   # magenta = transparent (RO bitmaps)
        for y in range(im.height):
            for x in range(im.width):
                r, g, b, _ = px[x, y]
                if r > 240 and g < 15 and b > 240:
                    px[x, y] = (0, 0, 0, 0)
        if "cardbmp" in path:   # card art: the monster sits in the middle of the upper part
            w, h = im.size
            s = int(min(w, h * 0.72))
            im = im.crop(((w - s) // 2, int(h * 0.06), (w - s) // 2 + s, int(h * 0.06) + s))
        else:
            im = im.crop(im.getbbox())
        im.thumbnail((z(SYM - 4), z(SYM - 4)), Image.LANCZOS)
        sq = Image.new("RGBA", (z(SYM), z(SYM)), (0, 0, 0, 0))
        sq.alpha_composite(im, ((z(SYM) - im.width) // 2, (z(SYM) - im.height) // 2))
        out.append(sq)
    return out


def slot_body(jackpot=None):
    img = frame_box(SW, SH, fill=(120, 18, 30))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle(Z(18, 12, SW - 19, 52), z(10), fill=(40, 10, 20), outline=GOLD, width=z(3))
    for k in range(13):   # marquee bulbs
        x = 30 + k * 22.5
        on = (k + jackpot) % 2 == 0 if jackpot is not None else True
        d.ellipse(Z(x - 3, 15, x + 3, 21), fill=GOLD if on else (90, 60, 20))
    text_c(d, (SW / 2, 36), "RAGNADUDS  SLOTS", font(SANS, 18), GOLD, 2)
    for x in WIN_X:
        d.rounded_rectangle(Z(x - 6, WIN_Y - 6, x + WIN_W + 5, WIN_Y + WIN_H + 5), z(8), fill=GOLD_D, outline=GOLD, width=z(2))
    d.rounded_rectangle(Z(18, 196, SW - 19, 236), z(8), fill=(40, 10, 20), outline=GOLD_D, width=z(2))
    return img


def reel_window(syms, center, above, below):
    W, H, T = z(WIN_W), z(WIN_H), z(SYM)
    win = Image.new("RGBA", (W, H), CREAM + (255,))
    for s, dy in ((above, -SYM), (center, 0), (below, SYM)):
        win.alpha_composite(syms[s], ((W - T) // 2, (H - T) // 2 + z(dy)))
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))   # curved-reel shading at top and bottom
    sd = ImageDraw.Draw(shade)
    for y in range(H):
        sd.line((0, y, W, y), fill=(0, 0, 0, int(110 * (abs(y - H / 2) / (H / 2)) ** 2)))
    return Image.alpha_composite(win, shade)


def spinning_window(syms, seed):
    rnd = random.Random(seed)
    W, H, T = z(WIN_W), z(WIN_H), z(SYM)
    strip = Image.new("RGBA", (W, T * 6), CREAM + (255,))
    for k in range(6):
        strip.alpha_composite(syms[rnd.randrange(len(syms))], ((W - T) // 2, k * T))
    off = rnd.randrange(0, T * 4)
    win = strip.crop((0, off, W, off + H))
    return win.resize((W, H // 10), Image.BILINEAR).resize((W, H), Image.BILINEAR)   # vertical blur


def slot_frame(syms, reels, highlight=False, caption="", jackpot=None):
    """reels: 3 items, each a symbol index (stopped) or ('spin', seed)."""
    img = slot_body(jackpot)
    n = len(syms)
    for x, r in zip(WIN_X, reels):
        win = spinning_window(syms, r[1]) if isinstance(r, tuple) else reel_window(syms, r, (r - 1) % n, (r + 1) % n)
        img.alpha_composite(win, (z(x), z(WIN_Y)))
    d = ImageDraw.Draw(img)
    d.line(Z(22, WIN_Y + WIN_H / 2, SW - 23, WIN_Y + WIN_H / 2), fill=GOLD if highlight else (230, 40, 40),
           width=z(3) if highlight else z(2))
    text_c(d, (SW / 2, 216), caption, font(SANS, 15), GOLD if highlight else CREAM, 2)
    return img


def slot_caption(a, b, c):
    if a == b == c:
        return "JACKPOT!" if a == 6 else f"3x {SYMBOLS[a][1].upper()}!"
    if [a, b, c].count(0) == 2:
        return "2x RED POTION: BET BACK"
    return "NO WIN"


def build_slots(client):
    syms = symbol_images(client)
    save(slot_frame(syms, [2, 2, 2], caption="PULL THE LEVER!"), "duds_sl_idle")
    for v in range(3):
        save(slot_frame(syms, [("spin", v * 3 + k) for k in range(3)], caption="SPINNING..."), f"duds_sl_spin{v}")
    for a in range(7):
        save(slot_frame(syms, [a, ("spin", 100 + a), ("spin", 200 + a)], caption="SPINNING..."), f"duds_sl_a{a}")
        for b in range(7):
            save(slot_frame(syms, [a, b, ("spin", 300 + a * 7 + b)], caption="SPINNING..."), f"duds_sl_b{a}{b}")
            for c in range(7):
                win = (a == b == c) or [a, b, c].count(0) == 2
                save(slot_frame(syms, [a, b, c], win, slot_caption(a, b, c)), f"duds_sl_c{a}{b}{c}")
    for k in range(4):
        save(slot_frame(syms, [6, 6, 6], True, "* * *  J A C K P O T  * * *" if k % 2 == 0 else "JACKPOT!", jackpot=k),
             f"duds_sl_jp{k}")


# ------------------------------------------------------------------ blackjack
BW, BH = 280, 260
CW, CH = 112, 160


def card_face(code):
    rank, suit = RANKS[code // 4], SUITS[code % 4]
    col = RED if code % 4 < 2 else BLACK
    W, H = z(CW), z(CH)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, W - 1, H - 1), z(9), fill=(252, 250, 244), outline=(120, 110, 90), width=z(2))
    fr, fs = font(SERIF, 22 if rank != "10" else 18), font(SANS, 16)
    corner = Image.new("RGBA", (W, H), (0, 0, 0, 0))   # the index, top-left; the same, turned, bottom-right
    cd = ImageDraw.Draw(corner)
    cd.text(Z(16, 17), rank, font=fr, fill=col, anchor="mm")
    cd.text(Z(16, 38), suit, font=fs, fill=col, anchor="mm")
    img.alpha_composite(corner)
    img.alpha_composite(corner.rotate(180))
    if rank in ("J", "Q", "K"):
        d.rounded_rectangle(Z(30, 30, CW - 31, CH - 31), z(6), outline=GOLD_D, width=z(3), fill=(255, 244, 214))
        text_c(d, (CW / 2, CH / 2 - 12), rank, font(SERIF, 48), col)
        text_c(d, (CW / 2, CH / 2 + 28), suit, font(SANS, 24), col)
    else:
        text_c(d, (CW / 2, CH / 2), suit, font(SANS, 70 if rank == "A" else 54), col)
    return img


def card_back():
    W, H = z(CW), z(CH)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, W - 1, H - 1), z(9), fill=(252, 250, 244), outline=(120, 110, 90), width=z(2))
    d.rounded_rectangle(Z(7, 7, CW - 8, CH - 8), z(6), fill=(120, 18, 30))
    for y in range(12, CH - 10, 14):
        for x in range(12 + (y // 14 % 2) * 7, CW - 10, 14):
            d.polygon([Z(x, y - 5), Z(x + 5, y), Z(x, y + 5), Z(x - 5, y)], fill=(160, 40, 50))
    d.ellipse(Z(CW / 2 - 26, CH / 2 - 26, CW / 2 + 26, CH / 2 + 26), fill=(40, 10, 20), outline=GOLD, width=z(3))
    text_c(d, (CW / 2, CH / 2), "RD", font(SERIF, 26), GOLD)
    return img


def squash(card, frac):
    return card.resize((max(4, int(card.width * frac)), card.height), Image.LANCZOS)


def table():
    img = felt(BW, BH)
    d = ImageDraw.Draw(img)
    d.arc(Z(-60, -170, BW + 60, 150), 25, 155, fill=GOLD_D, width=z(3))
    text_c(d, (BW / 2, 22), "BLACKJACK PAYS 3 TO 2", font(SANS, 14), GOLD, 1)
    text_c(d, (BW / 2, BH - 20), "DEALER STANDS ON 17", font(SANS, 12), CREAM, 1)
    return img


def on_table(card):
    img = table()
    x, y = (img.width - card.width) // 2, (img.height - card.height) // 2 + z(4)
    shadow = Image.new("RGBA", card.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle((0, 0, card.width - 1, card.height - 1), z(9), fill=(0, 0, 0, 90))
    img.alpha_composite(shadow, (x + z(4), y + z(5)))
    img.alpha_composite(card, (x, y))
    return img


def build_blackjack():
    back = card_back()
    t = table()
    for k in range(5):   # the shoe: a little stack of backs
        t.alpha_composite(back.resize(Z(56, 80)), (z(BW / 2 - 28 + k * 2), z(BH / 2 - 44 - k * 2)))
    text_c(ImageDraw.Draw(t), (BW / 2, BH / 2 + 60), "PLACE YOUR BET", font(SANS, 16), GOLD, 2)
    save(t, "duds_bj_table")
    small = back.resize(Z(70, 100))
    for k in range(4):   # shuffle: two halves riffling together
        img = table()
        gap = [60, 38, 16, 0][k]
        for j in range(4):
            img.alpha_composite(small, (z(BW / 2 - 35 - gap + j), z(BH / 2 - 54 - j)))
            img.alpha_composite(small, (z(BW / 2 - 35 + gap + j), z(BH / 2 - 54 - j)))
        text_c(ImageDraw.Draw(img), (BW / 2, BH / 2 + 66), "SHUFFLING...", font(SANS, 16), GOLD, 2)
        save(img, f"duds_bj_shuf{k}")
    save(on_table(back), "duds_bj_back")
    save(on_table(squash(back, 0.45)), "duds_bj_backh")
    save(on_table(squash(back, 0.06)), "duds_bj_edge")
    for code in range(52):
        face = card_face(code)
        save(on_table(squash(face, 0.45)), f"duds_bj_c{code}h")
        save(on_table(face), f"duds_bj_c{code}")


# ------------------------------------------------------------------ lottery
LW, LH, LC, LR = 280, 300, (140, 128), 92


def lotto_ball(n, r):
    """A ball of radius r (base units)."""
    R = z(r)
    img = Image.new("RGBA", (R * 2 + 2, R * 2 + 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    hue = [(230, 60, 60), (240, 170, 30), (70, 160, 230), (90, 190, 90), (180, 90, 210)][(n - 1) // 5]
    d.ellipse((0, 0, R * 2, R * 2), fill=hue, outline=(60, 40, 20), width=max(1, R // 10))
    d.ellipse((R * 0.45, R * 0.45, R * 1.55, R * 1.55), fill=(255, 255, 255))
    d.text((R, R + 1), str(n), font=ImageFont.truetype(SANS, int(R * 0.85)), fill=(30, 30, 30), anchor="mm")
    d.ellipse((R * 0.35, R * 0.2, R * 0.75, R * 0.5), fill=(255, 255, 255, 140))
    return img


def lotto_machine(seed, out_ball=None, caption="DAILY DRAW 21:00 UTC"):
    img = frame_box(LW, LH, fill=(48, 26, 70))
    d = ImageDraw.Draw(img)
    cx, cy = LC
    d.polygon([Z(cx - 40, cy + LR - 6), Z(cx + 40, cy + LR - 6), Z(cx + 64, LH - 44), Z(cx - 64, LH - 44)], fill=GOLD_D)
    d.rectangle(Z(cx - 80, LH - 46, cx + 80, LH - 36), fill=GOLD)
    d.ellipse(Z(cx - LR, cy - LR, cx + LR, cy + LR), fill=(180, 210, 240, 70), outline=(220, 235, 255), width=z(3))
    rnd = random.Random(seed)
    for n in rnd.sample(range(1, 26), 18):   # tumbling balls
        a, rr = rnd.uniform(0, math.tau), LR * 0.78 * math.sqrt(rnd.random())
        img.alpha_composite(lotto_ball(n, 11), (z(cx + rr * math.cos(a) - 11), z(cy + rr * math.sin(a) - 11)))
    d = ImageDraw.Draw(img)
    d.ellipse(Z(cx - LR + 18, cy - LR + 14, cx - LR + 50, cy - LR + 34), fill=(255, 255, 255, 110))   # glass shine
    if out_ball:
        img.alpha_composite(lotto_ball(out_ball, 34), Z(cx + 60, LH - 120))
    text_c(d, (LW / 2, LH - 20), caption, font(SANS, 14), GOLD, 2)
    return img


def build_lottery():
    save(lotto_machine(1), "duds_lt_idle")
    for k in range(6):
        save(lotto_machine(100 + k, caption="DRAWING..."), f"duds_lt_tumble{k}")
    for n in range(1, 26):
        save(lotto_machine(200 + n, n, caption=f"BALL  {n}"), f"duds_lt_ball{n}")


# ------------------------------------------------------------------ jogo do bicho
EMOJI = "/usr/share/fonts/google-noto-emoji-fonts/NotoEmoji-Regular.ttf"
# the 25 groups in order (group g has the dezenas 4g-3 .. 4g, the 25th 97 98 99 00); the ostrich has no emoji: a feather
BICHOS = [("Avestruz", "🪶"), ("Águia", "🦅"), ("Burro", "🫏"), ("Borboleta", "🦋"), ("Cachorro", "🐕"), ("Cabra", "🐐"),
          ("Carneiro", "🐏"), ("Camelo", "🐫"), ("Cobra", "🐍"), ("Coelho", "🐇"), ("Cavalo", "🐎"), ("Elefante", "🐘"),
          ("Galo", "🐓"), ("Gato", "🐈"), ("Jacaré", "🐊"), ("Leão", "🦁"), ("Macaco", "🐒"), ("Porco", "🐖"),
          ("Pavão", "🦚"), ("Peru", "🦃"), ("Touro", "🐂"), ("Tigre", "🐅"), ("Urso", "🐻"), ("Veado", "🦌"), ("Vaca", "🐄")]
JW, JH = 330, 360
PAPER, INK = (244, 232, 196), (60, 40, 20)


def dezenas(g):
    return " ".join(f"{(4 * g - 3 + k) % 100:02d}" for k in range(4))


def bicho_icon(g, size, col):
    f = ImageFont.truetype(EMOJI, z(size))
    _, e = BICHOS[g - 1]
    box = f.getbbox(e)
    im = Image.new("RGBA", (box[2] + 4, box[3] + 4), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((2, 2), e, font=f, fill=col)
    return im.crop(im.getbbox())


def bicho_table():
    """The board every banca has: 25 animals, their group number and dezenas."""
    img = frame_box(JW, JH, fill=PAPER, border=(90, 60, 30))
    d = ImageDraw.Draw(img)
    text_c(d, (JW / 2, 24), "TABELA DO JOGO DO BICHO", font(SANS, 17), (140, 30, 30))
    cw, ch, x0, y0 = 62, 64, 10, 40
    for g in range(1, 26):
        c, r = (g - 1) % 5, (g - 1) // 5
        x, y = x0 + c * cw, y0 + r * ch
        d.rounded_rectangle(Z(x + 1, y + 1, x + cw - 2, y + ch - 2), z(5), fill=(255, 248, 225), outline=(170, 130, 70), width=z(1))
        ic = bicho_icon(g, 22, (40, 90, 50))
        img.alpha_composite(ic, (z(x + cw / 2) - ic.width // 2, z(y + 22) - ic.height // 2))
        text_c(d, (x + 9, y + 9), f"{g:02d}", font(SANS, 9), (140, 30, 30))
        text_c(d, (x + cw / 2, y + 42), BICHOS[g - 1][0], font(SANS, 9), INK)
        text_c(d, (x + cw / 2, y + 54), dezenas(g), font(SANS, 7), (110, 90, 60))
    return img


def drums(seed, caption):
    """The extraction: four number drums spinning (blurred digits)."""
    img = frame_box(JW, JH, fill=(30, 60, 40))
    d = ImageDraw.Draw(img)
    text_c(d, (JW / 2, 30), "EXTRAÇÃO DO BICHO", font(SANS, 20), GOLD, 2)
    rnd = random.Random(seed)
    for k in range(4):
        x = 30 + k * 70
        col = Image.new("RGBA", Z(60, 170), CREAM + (255,))
        cd = ImageDraw.Draw(col)
        off = rnd.randrange(0, 50)
        for j in range(-1, 5):
            text_c(cd, (30, j * 50 + off - 10), str(rnd.randrange(10)), font(SANS, 40), INK)
        col = col.resize((z(60), z(170) // 12), Image.BILINEAR).resize(Z(60, 170), Image.BILINEAR)
        img.alpha_composite(col, Z(x, 90))
        d.rounded_rectangle(Z(x - 3, 87, x + 63, 263), z(6), outline=GOLD, width=z(3))
    d.line(Z(22, 175, JW - 23, 175), fill=(230, 40, 40), width=z(2))
    text_c(d, (JW / 2, 300), caption, font(SANS, 16), CREAM, 2)
    return img


def bicho_card(g, prize):
    img = frame_box(JW, JH, fill=(30, 60, 40))
    d = ImageDraw.Draw(img)
    text_c(d, (JW / 2, 30), f"{prize}º PRÊMIO", font(SANS, 22), GOLD, 2)
    d.rounded_rectangle(Z(55, 55, JW - 55, 300), z(14), fill=PAPER, outline=GOLD, width=z(4))
    ic = bicho_icon(g, 92, (40, 90, 50))
    img.alpha_composite(ic, (z(JW / 2) - ic.width // 2, z(140) - ic.height // 2))
    text_c(d, (JW / 2, 225), BICHOS[g - 1][0].upper(), font(SERIF, 30), (140, 30, 30))
    text_c(d, (JW / 2, 258), f"GRUPO {g:02d}", font(SANS, 15), INK)
    text_c(d, (JW / 2, 282), dezenas(g), font(SANS, 13), (110, 90, 60))
    text_c(d, (JW / 2, 330), "RAGNADUDS · DEU NO POSTE!", font(SANS, 13), CREAM, 1)
    return img


def build_bicho():
    save(bicho_table(), "duds_jb_table")
    for k in range(6):
        save(drums(500 + k, "RODANDO..."), f"duds_jb_spin{k}")
    for g in range(1, 26):
        for p in range(1, 6):
            save(bicho_card(g, p), f"duds_jb_{g}_{p}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--client", default=os.path.expanduser("~/ragnaduds/Renewal"), help="renewal client folder (GRFs)")
    ap.add_argument("--preview", help="also write a contact sheet of a few frames to this PNG")
    a = ap.parse_args()
    global K
    for game, build in (("roulette", build_roulette), ("slots", lambda: build_slots(a.client)),
                        ("blackjack", build_blackjack), ("lottery", build_lottery), ("bicho", build_bicho)):
        K = SCALE[game]
        build()
    if os.path.isdir(OUT):
        for f in os.listdir(OUT):
            if f.startswith("duds_") and f.endswith(".png"):
                os.remove(os.path.join(OUT, f))
    os.makedirs(OUT, exist_ok=True)
    for name, data in saved.items():
        with open(os.path.join(OUT, name + ".png"), "wb") as f:
            f.write(data)
    total = sum(len(v) for v in saved.values())
    print(f"{len(saved)} frames, {total / 1e6:.1f} MB -> {OUT}")
    if a.preview:
        pick = ["duds_jb_table", "duds_jb_spin2", "duds_jb_11_1", "duds_jb_16_3", "duds_rl_17_5", "duds_bj_c40"]
        ims = [Image.open(io.BytesIO(saved[p])).convert("RGBA") for p in pick]
        cols = 3
        cw, ch = max(i.width for i in ims), max(i.height for i in ims)
        sheet = Image.new("RGBA", (cols * (cw + 10), ((len(ims) + cols - 1) // cols) * (ch + 10)), (60, 60, 70, 255))
        for k, im in enumerate(ims):
            sheet.alpha_composite(im, ((k % cols) * (cw + 10), (k // cols) * (ch + 10)))
        sheet.save(a.preview)


if __name__ == "__main__":
    main()
