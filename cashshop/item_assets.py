"""Real item pictures and descriptions from divine-pride.net (kRO data), for items our client can't show.

  icon_bmp(id)        24x24 inventory / shop icon  (data\\texture\\유저인터페이스\\item\\<name>.bmp)
  collection_bmp(id)  75x100 picture in the item window (…\\collection\\<name>.bmp)
  description(id)     official English description lines
Downloads are cached in cashshop/.cache/dp/ (one request per file, ever) and paced to be polite.
The client draws magenta (255,0,255) as transparent: images are flattened onto it and saved as 8-bit BMPs
like the original kRO ones.
"""
import html, io, os, re, threading, time, urllib.error, urllib.request
from concurrent.futures import ThreadPoolExecutor
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DP = os.path.join(HERE, ".cache", "dp")
AGENT = "Mozilla/5.0 (RagnaDuds private server; item icons)"
GAP = {"static.divine-pride.net": 0.1, "www.divine-pride.net": 0.4}   # seconds between requests per host
_lock, _next = threading.Lock(), {}


def _get(url, path):
    if os.path.exists(path):
        return open(path, "rb").read() or None
    os.makedirs(DP, exist_ok=True)
    host = url.split("/")[2]
    for attempt in range(3):
        with _lock:                       # polite: one request per GAP seconds per host
            now = time.time(); at = max(now, _next.get(host, 0)); _next[host] = at + GAP.get(host, 0.5)
        if at > now: time.sleep(at - now)
        try:
            data = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": AGENT}), timeout=30).read()
            if "/database/item/" in url:          # keep only the description line, not the whole page
                m = re.search(rb'<meta name="description" content="[^"]*"', data)
                data = m.group(0) if m else b""
            break
        except urllib.error.HTTPError as e:
            data = b""
            if e.code not in (429, 500, 502, 503, 504): break
            time.sleep(5 * (attempt + 1))
        except Exception:
            data = b""; time.sleep(3)
    else:
        return None                        # network trouble: not cached, tried again next run
    open(path, "wb").write(data)          # empty file = "not available", not asked again
    return data or None


def prefetch(icon_ids, page_ids, workers=16):
    """Download many items at once (cached; safe to interrupt and rerun). Pages and pictures are interleaved
    so both hosts are busy; each host keeps its own polite pace (GAP)."""
    imgs = [(f"https://static.divine-pride.net/images/items/item/{i}.png", os.path.join(DP, f"{i}_icon.png")) for i in icon_ids]
    imgs += [(f"https://static.divine-pride.net/images/items/collection/{i}.png", os.path.join(DP, f"{i}_col.png")) for i in icon_ids]
    pages = [(f"https://www.divine-pride.net/database/item/{i}", os.path.join(DP, f"{i}.html")) for i in page_ids]
    imgs = [j for j in imgs if not os.path.exists(j[1])]
    pages = [j for j in pages if not os.path.exists(j[1])]
    jobs, step = [], max(1, len(imgs) // max(1, len(pages)))
    while imgs or pages:
        jobs += imgs[:step]; del imgs[:step]
        if pages: jobs.append(pages.pop(0))
    done = [0]
    def one(job):
        _get(*job); done[0] += 1
        if done[0] % 500 == 0: print(f"  downloaded {done[0]}/{len(jobs)}", flush=True)
    with ThreadPoolExecutor(workers) as pool:
        list(pool.map(one, jobs))
    return len(jobs)


def _bmp(png, size):
    im = Image.open(io.BytesIO(png)).convert("RGBA")
    if im.size != size:
        im.thumbnail(size, Image.LANCZOS)
    canvas = Image.new("RGBA", size, (255, 0, 255, 255))
    canvas.paste(im, ((size[0] - im.width) // 2, (size[1] - im.height) // 2), im)
    rgb = canvas.convert("RGB")
    # hard edge: half-transparent pixels become magenta or solid (the client has no alpha)
    alpha = Image.new("L", size, 0); alpha.paste(im.getchannel("A"), ((size[0] - im.width) // 2, (size[1] - im.height) // 2))
    px, a = rgb.load(), alpha.load()
    for y in range(size[1]):
        for x in range(size[0]):
            if a[x, y] < 128: px[x, y] = (255, 0, 255)
    pal = rgb.quantize(colors=255, method=Image.Quantize.MEDIANCUT)
    out = io.BytesIO(); pal.save(out, "BMP"); return out.getvalue()


def icon_bmp(item_id):
    png = _get(f"https://static.divine-pride.net/images/items/item/{item_id}.png", os.path.join(DP, f"{item_id}_icon.png"))
    return _bmp(png, (24, 24)) if png else None


def collection_bmp(item_id):
    png = _get(f"https://static.divine-pride.net/images/items/collection/{item_id}.png", os.path.join(DP, f"{item_id}_col.png"))
    return _bmp(png, (75, 100)) if png else None


def description(item_id):
    page = _get(f"https://www.divine-pride.net/database/item/{item_id}", os.path.join(DP, f"{item_id}.html"))
    if not page:
        return None
    m = re.search(r'<meta name="description" content="([^"]*)"', page.decode("utf-8", "replace"))
    if not m:
        return None
    text = html.unescape(m.group(1)).strip()
    text = re.sub(r"\s*(SET BONUS)\s*", r" ---------- \1\n", text)
    parts = [p.strip() for p in re.split(r"-{8,}", text) if p.strip()]
    keys = r"(Class|Type|Weight|Defense|Required [Ll]evel|Jobs|Attack|Weapon Level|Armor Level|Location|Property|MATK|Slot)\s*:"
    lines = []
    for i, p in enumerate(parts):
        if i: lines.append("________________________")
        p = re.sub(r"\s+(?=" + keys + ")", "\n", p)             # one requirement per line
        p = re.sub(r"(?<=[a-z0-9%.)])\.\s+(?=[A-Z])", ".\n", p)  # one effect per line
        lines += [l.strip() for l in p.split("\n") if l.strip()]
    return lines
