#!/usr/bin/env python3
"""Minimal GRF reader (versions 0x200 and 0x300), enough to list and extract files.
Usage: grf.py <file.grf> list [substring]
       grf.py <file.grf> get <exact path inside grf> <output file>"""
import re, struct, sys, zlib

def entries(path):
    f = open(path, "rb")
    h = f.read(46)
    ver = struct.unpack_from("<I", h, 42)[0]
    off = struct.unpack_from("<Q" if ver >= 0x300 else "<I", h, 30)[0]
    f.seek(46 + off)
    raw = f.read(16)
    for skip in (0, 4, 8):  # 0x300 tables may have a small prefix
        clen, _ = struct.unpack_from("<II", raw, skip)
        f.seek(46 + off + skip + 8)
        try:
            tbl = zlib.decompress(f.read(clen)); break
        except zlib.error:
            continue
    i, out = 0, {}
    while i < len(tbl):
        j = tbl.index(b"\0", i)
        csize, casize, size, flags = struct.unpack_from("<IIIB", tbl, j + 1)
        pos = struct.unpack_from("<Q" if ver >= 0x300 else "<I", tbl, j + 14)[0]
        out[tbl[i:j]] = (casize, size, flags, pos)
        i = j + (22 if ver >= 0x300 else 18)
    return f, out

def read(f, e):
    casize, size, flags, pos = e
    if flags != 1:  # 1 = plain file; others are folders or encrypted
        return None
    f.seek(46 + pos)
    return zlib.decompress(f.read(casize))[:size]

def write(path, files):
    """Write a GRF 0x200 (zlib, no encryption) with {name inside the grf: data}. Names are client paths
    with backslashes, e.g. 'data\\texture\\유저인터페이스\\t_login.jpg'; stored as cp949 like the client asks."""
    body, table = bytearray(), bytearray()
    for name, data in files.items():
        comp = zlib.compress(data, 9)
        table += name.encode("cp949") + b"\0" + struct.pack("<IIIBI", len(comp), len(comp), len(data), 1, len(body))
        body += comp
    ctable = zlib.compress(bytes(table), 9)
    header = b"Master of Magic\0" + bytes(range(14)) + struct.pack("<IIII", len(body), 0, len(files) + 7, 0x200)
    with open(path, "wb") as out:
        out.write(header + bytes(body) + struct.pack("<II", len(ctable), len(table)) + ctable)

if __name__ == "__main__":
    f, ents = entries(sys.argv[1])
    if sys.argv[2] == "list":
        sub = (sys.argv[3] if len(sys.argv) > 3 else "").lower().encode()
        for n in ents:
            if sub in n.lower():
                print(n.decode("cp949", "replace"))
    elif sys.argv[2] == "get":
        want = sys.argv[3].lower().encode("cp949")
        name = next(n for n in ents if n.lower() == want)
        open(sys.argv[4], "wb").write(read(f, ents[name]))
