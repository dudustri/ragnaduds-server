#!/usr/bin/env python3
"""The browser client's game folder, made from the friends' download, so the browser sees exactly what the exe does:
our GRFs (item pictures, casino art, screens) in the same order, the music, and the same item list.

  uv run --no-project --with pillow python3 browser_data.py <pre|re> <out folder>   (run ./duds.sh package first)

Writes into <out folder>:
  - the game folder from deploy/files/duds-<edition>.zip (game.zip inside it), without the Windows program files
  - DATA_browser.INI: the client's DATA.INI as the browser's file server reads it (paths under /game, same order)
  - SystemEN/: roBrowser reads the English sign, town and quest tables there; renewal keeps them in System/
  - ragnaduds_browser.grf: what roBrowser asks for under other names than the exe (pre-renewal login picture)
  - System/itemInfo_browser.lua: the item list the exe ends up with, as one plain Lua table. roBrowser runs a
    single Lua file in its own Lua engine, so the client's layered loader (compiled kRO list + English + our
    items + generated fixes) is run here once, with the client's own Lua 5.1, and its result written out.
"""
import os, re, shutil, subprocess, sys, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import grf  # noqa: E402
FILES = os.path.join(HERE, "..", "deploy", "files")
ZIPS = {"pre": "duds-pre-renewal.zip", "re": "duds-renewal.zip"}
ENTRY = {"pre": "SystemEN/itemInfo.lua", "re": "System/itemInfo_true.lub"}   # the item list each exe loads
SKIP = re.compile(r"(^|/)[^/]+\.(exe|dll|asi|m3d|manifest|epi)$|^savedata/", re.I)   # the browser never reads these
OUT_LUA = "System/itemInfo_browser.lua"

DUMP = r"""
-- the exe's item functions, as no-ops: we only want the table the item list builds
for _, f in ipairs({"AddItem", "AddItemUnidentifiedDesc", "AddItemIdentifiedDesc", "AddItemIsCostume",
                    "AddItemEffectInfo", "AddItemPackageID"}) do _G[f] = function() return true end end
dofile(arg[1])
assert(type(tbl) == "table", "the item list made no tbl")
local out, n = assert(io.open(arg[2], "wb")), 0
local function v(x)
  if type(x) == "string" then return string.format("%q", x) end
  if type(x) == "table" then
    local parts = {}
    for i, y in ipairs(x) do parts[i] = v(y) end
    for k, y in pairs(x) do
      if type(k) ~= "number" or k < 1 or k > #x or k % 1 ~= 0 then
        parts[#parts + 1] = "[" .. v(k) .. "]=" .. v(y)
      end
    end
    return "{" .. table.concat(parts, ",") .. "}"
  end
  return tostring(x)
end
out:write("tbl = {\n")
for id, info in pairs(tbl) do
  if type(id) == "number" and type(info) == "table" then out:write("[", id, "]=", v(info), ",\n"); n = n + 1 end
end
out:write("}\n"); out:close()
print(n .. " items")
"""


def unpack(edition, out):
    outer = zipfile.ZipFile(os.path.join(FILES, ZIPS[edition]))
    inner = zipfile.ZipFile(outer.open(next(n for n in outer.namelist() if n.endswith("/game.zip"))))
    n = 0
    for info in inner.infolist():
        if info.is_dir() or SKIP.search(info.filename):
            continue
        dest = os.path.join(out, info.filename)
        if os.path.exists(dest) and os.path.getsize(dest) == info.file_size:
            continue                                   # unchanged (re-runs only rewrite what changed)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with inner.open(info) as src, open(dest, "wb") as dst:
            shutil.copyfileobj(src, dst, 1 << 20)
        n += 1
    return n


def system_en(edition, out):
    """roBrowser reads SystemEN/Sign_Data.lub, Towninfo.lub, OngoingQuests.lub...; the 2026 client keeps them in
    System/, so renewal gets a copy (pre-renewal ships its own SystemEN/)."""
    if edition != "re":
        # the 2021 exe is patched (WARP Custom*Lub) to read SystemEN/<file> instead of System/<file>:
        # roBrowser reads System/, so put the English files there too
        n = 0
        for name in os.listdir(os.path.join(out, "SystemEN")):
            src = os.path.join(out, "SystemEN", name)
            if os.path.isfile(src) and name.lower().endswith((".lub", ".lua")):
                for dst in (name, re.sub(r"(?i)\.lub$|\.lua$", "", name) + "_true" + os.path.splitext(name)[1]):
                    target = os.path.join(out, "System", dst)
                    if dst == name or os.path.exists(target):   # also over the Korean *_true file roBrowser tries
                        shutil.copyfile(src, target); n += 1
        return f"own; {n} English files copied over System/ (as the exe reads them)"
    dest = os.path.join(out, "SystemEN"); shutil.rmtree(dest, ignore_errors=True)
    shutil.copytree(os.path.join(out, "System"), dest, ignore=shutil.ignore_patterns("itemInfo_browser.lua"))
    return "copied from System/"


UI = "data\\texture\\유저인터페이스"
def browser_grf(edition, out):
    """Our pictures under the names roBrowser asks for when they differ from the exe's. Pre-renewal (2021): the exe
    shows bgi_temp.bmp at the login, roBrowser the twelve kRO "t_배경" pictures for 2018-2022 clients. Both: the
    loading pictures roBrowser picks from that the clients don't have."""
    files = {}
    if edition == "pre":
        import io
        from PIL import Image
        f, ents = grf.entries(os.path.join(out, "ragnaduds_login1.grf"))
        pic = Image.open(io.BytesIO(grf.read(f, ents[next(k for k in ents if k.lower().endswith(b"t_login.jpg"))]))).convert("RGB")
        pic = pic.resize((1024, 768), Image.LANCZOS)     # roBrowser draws them as 4 x 3 tiles of 256 x 256
        for row in range(1, 4):
            for col in range(1, 5):
                tile = pic.crop(((col - 1) * 256, (row - 1) * 256, col * 256, row * 256))
                buf = io.BytesIO(); tile.save(buf, "BMP"); files[f"{UI}\\t_배경{row}-{col}.bmp"] = buf.getvalue()
    # roBrowser picks a random loading01-10.jpg between maps; the clients ship loading00-07: without 08-10 it shows
    # a blank screen 3 times in 10. Fill the gaps with the clients' own pictures.
    have = {}
    for g in sorted(f for f in os.listdir(out) if f.lower().endswith(".grf") and f != "ragnaduds_browser.grf"):
        f, ents = grf.entries(os.path.join(out, g))
        for k, e in ents.items():
            m = re.search(rb"\\loading(\d+)\.jpg$", k.lower())
            if m and int(m.group(1)) not in have:
                have[int(m.group(1))] = (f, e)
    pics = [have[n] for n in sorted(have)]
    for i, n in enumerate(n for n in range(1, 11) if n not in have):
        f, e = pics[i % len(pics)]
        files[f"{UI}\\loading{n:02d}.jpg"] = grf.read(f, e)
    path = os.path.join(out, "ragnaduds_browser.grf")
    if files:
        grf.write(path, files)
    elif os.path.exists(path):
        os.remove(path)
    return len(files)


def data_ini(out):
    name = next(f for f in os.listdir(out) if f.lower() == "data.ini")
    grfs = [l.split("=", 1)[1].strip() for l in open(os.path.join(out, name), encoding="latin-1")
            if re.match(r"\s*\d+\s*=", l)]
    grfs = [g for g in grfs if os.path.exists(os.path.join(out, g))]
    if os.path.exists(os.path.join(out, "ragnaduds_browser.grf")):
        grfs.insert(0, "ragnaduds_browser.grf")   # first: it only holds the browser-only names
    with open(os.path.join(out, "DATA_browser.INI"), "w") as f:
        f.write("[Data]\n" + "".join(f"{i}=/game/{g}\n" for i, g in enumerate(grfs)))
    return grfs


def item_list(edition, out):
    with open(os.path.join(out, ".dump_items.lua"), "w") as f:
        f.write(DUMP)
    try:   # the client's compiled Lua is 32-bit Lua 5.1 bytecode: run it in a 32-bit Lua 5.1
        r = subprocess.run(["docker", "run", "--rm", "--platform", "linux/386", "-v", f"{out}:/w:z", "-w", "/w",
                            "i386/alpine", "sh", "-c",
                            f"apk add -q lua5.1 && lua5.1 .dump_items.lua '{ENTRY[edition]}' '{OUT_LUA}'"],
                           capture_output=True, text=True)
    finally:
        os.remove(os.path.join(out, ".dump_items.lua"))
    if r.returncode != 0:
        sys.exit("item list failed:\n" + r.stdout + r.stderr)
    return r.stdout.strip().splitlines()[-1]


if __name__ == "__main__":
    edition, out = sys.argv[1], os.path.abspath(sys.argv[2])
    os.makedirs(out, exist_ok=True)
    print(f"{unpack(edition, out)} files written to {out}")
    print("SystemEN:", system_en(edition, out))
    print("browser-only pictures:", browser_grf(edition, out))
    print("GRFs, in order:", ", ".join(data_ini(out)))
    print("item list:", item_list(edition, out))
