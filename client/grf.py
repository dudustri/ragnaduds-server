#!/usr/bin/env python3
"""Minimal GRF reader (versions 0x200 and 0x300), enough to list and extract files.
Usage: grf.py <file.grf> list [substring]
       grf.py <file.grf> get <exact path inside grf> <output file>
       grf.py <file.grf> pack <folder>     every file under <folder>/data/... → data\\... in a new GRF
       grf.py - mirror <folder> <dest>      <folder>/data as roBrowser spells paths (cp949 bytes read as Latin-1)"""
import os, re, struct, sys, zlib

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
        out[tbl[i:j]] = (max(csize, casize), size, flags, pos)   # some 0x300 entries: casize < csize
        i = j + (22 if ver >= 0x300 else 18)
    return f, out

def read(f, e):
    casize, size, flags, pos = e
    if flags != 1:  # 1 = plain file; others are folders or encrypted
        return None
    f.seek(46 + pos)
    return zlib.decompressobj().decompress(f.read(casize))[:size]   # ignores alignment padding

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

def pack(path, folder):
    files = {}
    for root, _, names in os.walk(os.path.join(folder, "data")):
        for n in names:
            full = os.path.join(root, n)
            files[os.path.relpath(full, folder).replace(os.sep, "\\")] = open(full, "rb").read()
    write(path, files)
    return len(files)

def mirror(folder, dest):
    """Hard links under dest/data with the names roBrowser asks for: it sends cp949 paths as Latin-1 text, and its
    file server only translates names inside GRFs, not in a loose folder."""
    n = 0
    for root, _, names in os.walk(os.path.join(folder, "data")):
        for name in names:
            src = os.path.join(root, name)
            rel = os.path.relpath(src, folder).encode("cp949").decode("latin1")
            dst = os.path.join(dest, rel); os.makedirs(os.path.dirname(dst), exist_ok=True)
            os.link(src, dst); n += 1
    return n

if __name__ == "__main__":
    if sys.argv[2] == "mirror":
        print(mirror(sys.argv[3], sys.argv[4]), "files mirrored for the browser"); sys.exit()
    if sys.argv[2] == "pack":
        print(pack(sys.argv[1], sys.argv[3]), "files packed into", sys.argv[1]); sys.exit()
    f, ents = entries(sys.argv[1])
    if sys.argv[2] == "list":
        sub = (sys.argv[3] if len(sys.argv) > 3 else "").lower().encode("cp949")   # names are stored as cp949
        for n in ents:
            if sub in n.lower():
                print(n.decode("cp949", "replace"))
    elif sys.argv[2] == "get":
        want = sys.argv[3].lower().encode("cp949")
        name = next(n for n in ents if n.lower() == want)
        open(sys.argv[4], "wb").write(read(f, ents[name]))
