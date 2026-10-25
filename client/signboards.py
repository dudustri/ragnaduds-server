#!/usr/bin/env python3
"""Pre-renewal: drop the client's floating signs (data/luafiles514/lua files/SignBoardList.lub) that stand where our
server has no NPC. The 2021 kRO client marks NPCs that rAthena's pre-renewal scripts don't have (Eden Group,
clans, kRO promotions...), so players see a sign over an empty spot. package_client.py puts the filtered list in
ragnaduds.grf, which both the exe and the browser read before data.grf.

  python3 signboards.py <client data.grf>     (prints what it keeps and drops)
"""
import os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import grf  # noqa: E402
ROOT = os.path.join(HERE, "..")
RATHENA, DEPLOY = os.path.join(ROOT, "rathena"), os.path.join(ROOT, "deploy")
LIST = b"data\\luafiles514\\lua files\\signboardlist.lub"
NEAR = 3   # cells: a sign this close to one of our NPCs (or warps) stays

DUMP = r"""
dofile(arg[1])
local out = assert(io.open(arg[2], "wb"))
for _, e in ipairs(SignBoardList) do
  local parts = {}
  for i, x in ipairs(e) do parts[i] = type(x) == "string" and string.format("%q", x) or tostring(x) end
  out:write(e[1], "\t", e[2], "\t", e[3], "\t{", table.concat(parts, ", "), "}\0")
end
out:close()
"""
HEADER = re.compile(r"^([\w@.-]+),(\d+),(\d+)(?:,\d+)?\t(?:script|warp2?|shop|cashshop|itemshop|pointshop|marketshop"
                    r"|trader|duplicate\([^)]*\))\t", re.M)


def server_files():
    """Container path → file on this PC for what the pre-renewal map server mounts over rAthena (deploy/compose.yml)."""
    block = open(os.path.join(DEPLOY, "compose.yml")).read().split("prere-map:")[1].split("\n\n")[0]
    files = {dst: os.path.join(DEPLOY, src) for src, dst in re.findall(r'"\./([^:"]+):/rathena/([^:"]+)', block)}
    files["npc/scripts_custom.conf"] = os.path.join(DEPLOY, "hosts", "vm", "pre_renewal", "import", "scripts_custom.conf")
    return files


def npc_spots():
    """{map: [(x, y)]} of every NPC and warp the pre-renewal server loads."""
    mounted, spots, seen = server_files(), {}, set()

    def load(path):
        real = mounted.get(path, os.path.join(RATHENA, path))
        if path in seen or not os.path.isfile(real):
            return
        seen.add(path)
        text = open(real, encoding="latin-1").read()
        if path.endswith(".conf"):
            for _, p in re.findall(r"^\s*(npc|import):\s*(\S+)", text, re.M):
                load(p)
        else:
            for m, x, y in HEADER.findall(text):
                spots.setdefault(m, []).append((int(x), int(y)))
    load("npc/pre-re/scripts_main.conf")
    load("npc/scripts_custom.conf")
    assert spots.get("prontera"), "found no NPCs: rAthena submodule missing?"
    return spots


def signboards(data_grf):
    """[(map, x, y, Lua literal bytes)] from the client's compiled list, read with the client's own Lua 5.1."""
    f, ents = grf.entries(data_grf)
    with tempfile.TemporaryDirectory(dir=os.path.expanduser("~/.cache")) as d:
        open(os.path.join(d, "list.lub"), "wb").write(grf.read(f, ents[LIST]))
        open(os.path.join(d, "dump.lua"), "w").write(DUMP)
        subprocess.run(["docker", "run", "--rm", "--platform", "linux/386", "-v", f"{d}:/w:z", "-w", "/w", "i386/alpine",
                        "sh", "-c", "apk add -q lua5.1 && lua5.1 dump.lua list.lub out.bin"], check=True, capture_output=True)
        raw = open(os.path.join(d, "out.bin"), "rb").read()
    rows = [r.split(b"\t", 3) for r in raw.split(b"\0") if r]
    return [(m.decode("latin-1"), int(float(x)), int(float(y)), lit) for m, x, y, lit in rows]


def filtered(data_grf):
    """(SignBoardList.lub as Lua source, kept, dropped)."""
    spots, keep, drop = npc_spots(), [], []
    for m, x, y, lit in signboards(data_grf):
        near = any(abs(x - a) <= NEAR and abs(y - b) <= NEAR for a, b in spots.get(m, ()))
        (keep if near or m == "Default" else drop).append((m, x, y, lit))
    lua = b"SignBoardList = {\n" + b"".join(b"\t" + lit + b",\n" for *_, lit in keep) + b"}\n"
    return lua, keep, drop


if __name__ == "__main__":
    lua, keep, drop = filtered(sys.argv[1])
    for m, x, y, lit in drop:
        print("drop", m, x, y, lit.decode("cp949", "replace")[:90])
    print(f"{len(keep)} kept, {len(drop)} dropped")
