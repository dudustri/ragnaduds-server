#!/usr/bin/env python3
"""What the renewal game client can show, for the cash shop builder (build_shop.py).

Reads the client in ~/games/kro2026 (the one package_client.py ships) and caches in cashshop/.cache/:
  items.json   item id -> client item info (name, description, resource name, slots, look)
  looks.json   headgear / garment / weapon look ids -> sprite names
  files.json   every file the client can load (GRF archives + loose data folder), lower case, Korean names
The kRO tables are 32-bit Lua 5.1 bytecode: they are dumped by dump_client.lua in an i386 Alpine container.

  python3 client_data.py          # (re)build the cache
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "client"))
import grf  # noqa: E402

CLIENT = os.path.expanduser("~/games/kro2026/wine/drive_c/Gravity/kRO2026")
CACHE = os.path.join(HERE, ".cache")
GRFS = ("2026.grf", "data.grf")
DATAINFO = ("accessoryid.lub", "accname.lub", "spriterobeid.lub", "spriterobename.lub", "weapontable.lub")
UI, ITEM_SPR, ACC_SPR, ROBE_SPR = "유저인터페이스", "아이템", "악세사리", "로브"


def kr(s):
    """Strings from the Lua dump are cp949 bytes carried as latin-1 characters."""
    try:
        return s.encode("latin-1").decode("cp949")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return s


def fix(v):
    if isinstance(v, str): return kr(v)
    if isinstance(v, list): return [fix(x) for x in v]
    if isinstance(v, dict): return {kr(k): fix(x) for k, x in v.items()}
    return v


def build():
    os.makedirs(os.path.join(CACHE, "datainfo"), exist_ok=True)
    files = set()
    for g in GRFS:
        f, entries = grf.entries(os.path.join(CLIENT, g))
        for name, e in entries.items():
            low = name.decode("cp949", "replace").lower()
            files.add(low)
            base = low.rsplit("\\", 1)[-1]
            if g == "data.grf" and "\\datainfo\\" in low and base in DATAINFO:
                data = grf.read(f, e)
                if data: open(os.path.join(CACHE, "datainfo", "data.grf_" + base), "wb").write(data)
    for root, _, names in os.walk(os.path.join(CLIENT, "data")):
        for n in names:
            rel = os.path.relpath(os.path.join(root, n), CLIENT).replace("/", "\\")
            try: rel = rel.encode("cp1252").decode("cp949")      # loose files: Korean names read as cp1252
            except (UnicodeEncodeError, UnicodeDecodeError): pass
            files.add(rel.lower())
    json.dump(sorted(files), open(os.path.join(CACHE, "files.json"), "w"), ensure_ascii=False)

    subprocess.run(["docker", "run", "--rm", "--platform", "linux/386",
                    "-v", f"{os.path.join(CLIENT, 'System')}:/c:ro,z", "-v", f"{os.path.join(CACHE, 'datainfo')}:/d:ro,z",
                    "-v", f"{CACHE}:/out:z", "-v", f"{os.path.join(HERE, 'dump_client.lua')}:/dump.lua:ro,z",
                    "i386/alpine", "sh", "-c", f"apk add -q lua5.1 >/dev/null && lua5.1 /dump.lua && chown -R {os.getuid()}:{os.getgid()} /out"], check=True)
    items = {}
    for line in open(os.path.join(CACHE, "items.jsonl"), encoding="latin-1"):
        row = json.loads(line)
        items[str(row["id"])] = fix(row["v"])
    json.dump(items, open(os.path.join(CACHE, "items.json"), "w"), ensure_ascii=False)
    os.remove(os.path.join(CACHE, "items.jsonl"))
    looks = fix(json.load(open(os.path.join(CACHE, "looks.json"), encoding="latin-1")))
    json.dump(looks, open(os.path.join(CACHE, "looks.json"), "w"), ensure_ascii=False)
    print(f"client cache: {len(items)} items, {len(files)} files, looks: "
          + ", ".join(f"{k} {len(v)}" for k, v in looks.items()))


class Client:
    """Loaded cache + the checks the builder needs."""
    def __init__(self):
        if not os.path.exists(os.path.join(CACHE, "items.json")):
            build()
        self.items = json.load(open(os.path.join(CACHE, "items.json")))
        self.files = set(json.load(open(os.path.join(CACHE, "files.json"))))
        self.looks = json.load(open(os.path.join(CACHE, "looks.json")))
        robe = f"data\\sprite\\{ROBE_SPR}\\"
        self.robe_dirs = {f[len(robe):].split("\\")[0] for f in self.files if f.startswith(robe)}

    def info(self, item_id):
        return self.items.get(str(item_id))

    def has_pictures(self, resname):
        """Inventory icon + dropped-on-the-floor sprite."""
        rn = (resname or "").lower()
        return bool(rn) and f"data\\texture\\{UI}\\item\\{rn}.bmp" in self.files \
            and f"data\\sprite\\{ITEM_SPR}\\{rn}.spr" in self.files

    def look_ok(self, kind, view):
        """Can the client draw this look on a character? kind: acc (headgear) / robe (garment) / weapon."""
        if not view:
            return True
        name = self.looks.get(kind, {}).get(str(view))
        if name is None:
            return False
        if kind == "acc":
            return all(f"data\\sprite\\{ACC_SPR}\\{g}\\{g}{name}.spr".lower() in self.files for g in ("남", "여"))
        if kind == "robe":
            return bool(name) and name.lower() in self.robe_dirs
        return str(view) in self.looks.get("weapon", {})     # weapons: the view must be in the weapon table


if __name__ == "__main__":
    build()
