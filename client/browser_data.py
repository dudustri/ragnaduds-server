#!/usr/bin/env python3
"""The browser client's game folder, made from the friends' download, so the browser sees exactly what the exe does:
our GRFs (item pictures, casino art, screens) in the same order, the music, and the same item list.

  browser_data.py <pre|re> <out folder>     (run ./duds.sh package <pre|re> first)

Writes into <out folder>:
  - the game folder from deploy/files/duds-<edition>.zip (game.zip inside it), without the Windows program files
  - DATA_browser.INI: the client's DATA.INI as the browser's file server reads it (paths under /game, same order)
  - System/itemInfo_browser.lua: the item list the exe ends up with, as one plain Lua table. roBrowser runs a
    single Lua file in its own Lua engine, so the client's layered loader (compiled kRO list + English + our
    items + generated fixes) is run here once, with the client's own Lua 5.1, and its result written out.
"""
import os, re, shutil, subprocess, sys, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
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


def data_ini(out):
    name = next(f for f in os.listdir(out) if f.lower() == "data.ini")
    grfs = [l.split("=", 1)[1].strip() for l in open(os.path.join(out, name), encoding="latin-1")
            if re.match(r"\s*\d+\s*=", l)]
    grfs = [g for g in grfs if os.path.exists(os.path.join(out, g))]
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
    print("GRFs, in order:", ", ".join(data_ini(out)))
    print("item list:", item_list(edition, out))
