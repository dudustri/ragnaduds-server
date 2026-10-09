#!/usr/bin/env python3
"""Casino sound effects for the Comodo Casino NPCs (deploy/casino.txt), synthesized here (no samples, no licences).

    python3 casino/build_casino_sounds.py

Writes 16-bit mono PCM WAVs to client/grf_casino/data/wav/ (packed into ragnaduds_casino.grf with the art). The NPC
script plays them with soundeffect "<name>.wav",0 (the client wants PCM and names of at most 23 characters).
Their lengths follow the animations in casino.txt: the wheel sound lasts the roulette spin, the reel sound has its
three stops where the reels stop on screen.

Your own clips: put a file named like a sound (any format ffmpeg reads, e.g. duds_cheer.mp3) in
client/casino_media/wav/ (git-ignored) and it replaces the synthesized one, converted to PCM. duds_cheer (played to
everybody in the casino on a 1,000,000+ win) is cut to 3 seconds.
"""
import math, os, random, struct, subprocess, wave

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "client", "grf_casino", "data", "wav")
CUSTOM = os.path.join(os.path.dirname(HERE), "client", "casino_media", "wav")
MAX_SECONDS = {"duds_cheer": 3.0}
RATE = 22050
rnd = random.Random(7)


def buf(seconds):
    return [0.0] * int(seconds * RATE)


def add(dst, src, at=0.0, gain=1.0):
    o = int(at * RATE)
    for i, v in enumerate(src):
        if 0 <= o + i < len(dst):
            dst[o + i] += v * gain


def env_exp(n, tau):
    return [math.exp(-i / (tau * RATE)) for i in range(n)]


def noise(seconds):
    return [rnd.uniform(-1, 1) for _ in range(int(seconds * RATE))]


def highpass(x, a=0.85):
    out, prev_x, prev_y = [], 0.0, 0.0
    for v in x:
        prev_y = a * (prev_y + v - prev_x)
        prev_x = v
        out.append(prev_y)
    return out


def lowpass(x, a=0.2):
    out, y = [], 0.0
    for v in x:
        y += a * (v - y)
        out.append(y)
    return out


def tone(freq, seconds, partials=((1, 1.0),), tau=0.3, attack=0.004):
    n = int(seconds * RATE)
    out = []
    for i in range(n):
        t = i / RATE
        a = min(1.0, t / attack) * math.exp(-t / tau)
        out.append(a * sum(g * math.sin(2 * math.pi * freq * m * t) for m, g in partials))
    return out


BELL = ((1, 1.0), (2.76, 0.45), (5.4, 0.25), (8.93, 0.12))
BRASS = ((1, 1.0), (2, 0.6), (3, 0.45), (4, 0.3), (5, 0.2), (6, 0.12))


def tick(freq=3200, seconds=0.012, gain=1.0):
    """A small hard click: a decaying burst of noise and a ping."""
    n = int(seconds * RATE)
    e = env_exp(n, seconds / 4)
    nz = highpass(noise(seconds), 0.6)
    return [gain * e[i] * (0.6 * nz[i] + 0.5 * math.sin(2 * math.pi * freq * i / RATE)) for i in range(n)]


def thunk(seconds=0.09, freq=110):
    """A reel stopping: low knock plus a click."""
    n = int(seconds * RATE)
    low = [math.exp(-i / (0.025 * RATE)) * math.sin(2 * math.pi * freq * i / RATE * (1 - i / n * 0.3)) for i in range(n)]
    out = [v * 0.9 for v in low]
    add(out, tick(1800, 0.015, 0.7))
    return out


def card_flick():
    x = highpass(noise(0.11), 0.75)
    e = env_exp(len(x), 0.025)
    out = [x[i] * e[i] * 0.8 for i in range(len(x))]
    add(out, tick(2600, 0.01, 0.5), 0.0)
    return out


def shuffle():   # a riffle: ~22 quick flicks speeding up, then the cards squared off
    out = buf(0.62)
    t = 0.0
    for k in range(22):
        add(out, card_flick(), t, 0.35 + 0.25 * rnd.random())
        t += 0.024 - k * 0.0003
    add(out, thunk(0.07, 160), 0.56, 0.6)
    return out


def wheel():
    """Roulette, 2.55 s like the animation: the ball rolls (rumble) and rattles over the frets, slowing down,
    then a few bounces and it drops into the pocket."""
    total = 2.55
    out = buf(total)
    rumble = lowpass(noise(2.1), 0.05)
    for i in range(len(rumble)):
        t = i / RATE
        rumble[i] *= 0.9 * min(1.0, t / 0.15) * max(0.0, 1 - t / 2.1)
    add(out, rumble, 0.0, 1.2)
    t, rate = 0.05, 26.0          # fret ticks per second, slowing down
    while t < 2.05:
        add(out, tick(2800 + rnd.uniform(-300, 300), 0.01, 0.35 + 0.2 * rnd.random()), t)
        t += 1 / rate
        rate = max(4.0, rate * 0.975)
    for at, g in ((2.12, 0.9), (2.26, 0.7), (2.36, 0.5), (2.42, 0.35)):   # bounces into the pocket
        add(out, tick(2100, 0.02, g), at)
        add(out, thunk(0.05, 240), at, g * 0.4)
    return out


def reels():
    """Slots, 1.6 s: the three reels whirring (fast mechanical ticks) and stopping at 0.56, 0.98 and 1.46 s."""
    out = buf(1.62)
    stops = (0.56, 0.98, 1.46)
    for r, stop in enumerate(stops):
        t = 0.0
        while t < stop - 0.02:
            add(out, tick(1500 + 300 * r, 0.008, 0.18), t + r * 0.011)
            t += 1 / 30
        add(out, thunk(), stop, 0.9)
    whir = lowpass(noise(1.46), 0.08)
    for i in range(len(whir)):
        t = i / RATE
        live = sum(1 for s in stops if t < s)
        whir[i] *= 0.12 * live
    add(out, whir)
    return out


def arpeggio(notes, step, tau=0.35, gain=0.5, seconds=0.9):
    out = buf(seconds + step * len(notes))
    for k, f in enumerate(notes):
        add(out, tone(f, seconds, BELL, tau), k * step, gain)
    return out


def coins(seconds, density, gain=0.25):
    out = buf(seconds)
    t = 0.0
    while t < seconds - 0.05:
        add(out, tone(rnd.choice((2637, 3136, 3520, 4186)), 0.12, BELL, 0.03), t, gain * rnd.uniform(0.4, 1.0))
        t += rnd.expovariate(density)
    return out


def win():
    out = arpeggio([1047, 1319, 1568, 2093], 0.07)
    add(out, coins(0.6, 25), 0.05)
    return out


def bigwin():
    out = arpeggio([784, 1047, 1319, 1568, 2093, 2637], 0.07, gain=0.45, seconds=1.0)
    add(out, coins(1.3, 40), 0.1)
    return out


def jackpot():
    """A short brass fanfare over a shower of coins."""
    out = buf(2.8)
    seq = [(523, 0.0, 0.16), (523, 0.18, 0.16), (523, 0.36, 0.16), (659, 0.54, 0.5), (784, 1.05, 0.25), (1047, 1.32, 1.2)]
    for f, at, d in seq:
        for det in (0.997, 1.003):   # two slightly detuned voices: fuller
            add(out, tone(f * det, d + 0.25, BRASS, d * 0.9, 0.02), at, 0.16)
        add(out, tone(f / 2, d + 0.25, BRASS, d * 0.9, 0.02), at, 0.08)
    add(out, coins(2.6, 55, 0.2), 0.3)
    return out


def lose():
    out = buf(0.7)
    for k, f in enumerate((392, 370, 349, 311)):
        add(out, tone(f, 0.3, ((1, 1.0), (2, 0.3)), 0.18), k * 0.12, 0.35)
    return out


def chip():   # chips put on the table
    out = buf(0.25)
    for at in (0.0, 0.05, 0.085):
        add(out, tone(rnd.uniform(2400, 3000), 0.08, BELL, 0.015), at, 0.5)
        add(out, tick(4000, 0.008, 0.4), at)
    return out


def tumble():   # lottery balls rattling in the globe, ~1 s
    out = buf(1.0)
    t = 0.0
    while t < 0.95:
        add(out, tick(rnd.uniform(1200, 2200), 0.02, rnd.uniform(0.15, 0.4)), t)
        t += rnd.expovariate(45)
    hum = lowpass(noise(1.0), 0.03)
    add(out, hum, 0.0, 0.5)
    return out


def ball_out():   # a ball drops out of the chute: knock, roll, ding
    out = buf(0.8)
    add(out, thunk(0.08, 200), 0.0, 0.7)
    add(out, tick(1600, 0.02, 0.4), 0.09)
    add(out, tone(1568, 0.6, BELL, 0.25), 0.16, 0.45)
    return out


def cheer():
    """Everybody in the casino hears this on a 1,000,000+ win: 3 s, bouncy and loud (replace it with your own)."""
    out = buf(3.0)
    melody = [(784, 0.0), (988, 0.15), (1175, 0.3), (1568, 0.45), (1175, 0.75), (1568, 0.9), (1976, 1.2), (2349, 1.5)]
    for f, at in melody:
        add(out, tone(f, 0.5, BELL, 0.22), at, 0.4)
        add(out, tone(f / 2, 0.4, BRASS, 0.2, 0.01), at, 0.12)
    add(out, coins(2.9, 50, 0.22), 0.1)
    for at in (0.0, 0.6, 1.2, 1.8, 2.4):   # claps
        add(out, highpass(noise(0.06), 0.7), at, 0.5)
    return out


SOUNDS = {
    "duds_shuffle": shuffle, "duds_card": card_flick, "duds_chip": chip,
    "duds_wheel": wheel, "duds_reels": reels,
    "duds_win": win, "duds_bigwin": bigwin, "duds_jackpot": jackpot, "duds_lose": lose,
    "duds_tumble": tumble, "duds_ball": ball_out, "duds_cheer": cheer,
}


def write(name, samples):
    peak = max(1e-9, max(abs(v) for v in samples))
    g = 0.85 * 32767 / peak
    data = b"".join(struct.pack("<h", int(max(-32767, min(32767, v * g)))) for v in samples)
    with wave.open(os.path.join(OUT, name + ".wav"), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(data)


def custom(name):
    """Your own clip for this sound, converted to what the client plays (16-bit mono PCM), or None."""
    if not os.path.isdir(CUSTOM):
        return None
    src = next((os.path.join(CUSTOM, f) for f in sorted(os.listdir(CUSTOM)) if os.path.splitext(f)[0].lower() == name), None)
    if not src:
        return None
    dst = os.path.join(OUT, name + ".wav")
    cmd = ["ffmpeg", "-loglevel", "error", "-y", "-i", src, "-ac", "1", "-ar", str(RATE), "-acodec", "pcm_s16le"]
    if name in MAX_SECONDS:
        cmd += ["-t", str(MAX_SECONDS[name]), "-af", f"afade=t=out:st={MAX_SECONDS[name] - 0.3}:d=0.3"]
    subprocess.run(cmd + [dst], check=True)
    return src


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, make in SOUNDS.items():
        assert len(name) + 4 <= 23, name   # the client's limit
        src = custom(name)
        if src:
            print(f"  {name}: your clip {os.path.relpath(src, os.path.dirname(HERE))}")
        else:
            write(name, make())
    total = sum(os.path.getsize(os.path.join(OUT, n + ".wav")) for n in SOUNDS)
    print(f"{len(SOUNDS)} sounds, {total / 1e6:.1f} MB -> {OUT}")


if __name__ == "__main__":
    main()
