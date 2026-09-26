#!/usr/bin/env python3
"""Remove translation lines that reference monsters (jobtbl/JOBID) or item
options (EnumVAR) which don't exist in an older data.grf. Those lines cause
'table index is nil' / 'attempt to index a nil value' popups at startup.
Originals are kept as <file>.bak. Run from the game folder.
Usage: fix_translation_ids.py [data.grf]"""
import os, re, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grf

f, ents = grf.entries(sys.argv[1] if len(sys.argv) > 1 else "data.grf")
lua = [n for n in ents if n.lower().startswith(b"data\\luafiles514\\") and n.lower().endswith((b".lub", b".lua"))]
known = {b"jobtbl": set(), b"EnumVAR": set(), b"JOBID": set()}
for n in lua:
    d = grf.read(f, ents[n]) or b""
    for t in known:
        if t in d:
            known[t] |= set(re.findall(rb"\b[A-Z][A-Z0-9_]{2,}\b", d))
removed = 0
for root, _, files in os.walk("data/luafiles514"):
    for fn in files:
        p = os.path.join(root, fn)
        if not fn.endswith((".lub", ".lua")):
            continue
        b = open(p, "rb").read()
        if b.startswith(b"\x1bLua"):  # compiled, not editable
            continue
        keep, bad = [], 0
        for line in b.split(b"\n"):
            miss = [k for t in known for k in re.findall(rb"\b" + t + rb"\.(\w+)", line) if k not in known[t]]
            if miss: bad += 1
            else: keep.append(line)
        if bad:
            if not os.path.exists(p + ".bak"):
                shutil.copy(p, p + ".bak")
            open(p, "wb").write(b"\n".join(keep))
            removed += bad
            print(f"{p}: removed {bad} line(s)")
print("total lines removed:", removed)
