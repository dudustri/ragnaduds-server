#!/usr/bin/env python3
"""Build a friend-ready RagnaDuds download (zip with an installer) from your installed game folder.

  package_client.py pre  <server-address> [out-dir]
  package_client.py re   <server-address> [out-dir]

  e.g. package_client.py pre <VM_IP>   → duds_server/deploy/files/duds-pre-renewal.zip

The download unzips to:
  RagnaDuds-PreRenewal/
    Install RagnaDuds.bat     Windows: installer window (photo + progress) → "RagnaDuds" shortcuts
    install.sh                Linux:   same, with Wine prefix + app-menu/desktop launcher
    README.txt
    installer/                install.ps1, linux_install.py, config.json, icons, picture
    game.zip                  the game folder (unpacked by the installer)

game.zip = your game folder minus personal/backup files (savedata/, *.bak*, *.disabled,
_backup_before_english/) and Gravity's official exe/launcher, with our homunculus AI (client/homunculus_ai/,
Mir AI Mod preset to hunt by itself, /hoai in game) in every AI*/USER_AI, with data/clientinfo.xml +
sclientinfo.xml pointing at <server-address>. Your installed folder is not modified.
Icons/pictures come from client/installer/ (generate them with build/installer/make_assets.py).
"""
import hashlib, json, os, re, sys, tempfile, time, zipfile

import grf

HOME = os.path.expanduser("~")
HERE = os.path.dirname(os.path.abspath(__file__))
INSTALLER = os.path.join(HERE, "installer")
CLIENTS = {
    "pre": dict(src=f"{HOME}/games/kro2021/wine/drive_c/Gravity/RagnarokKRO", exe="ragexe_2021_patched.exe",
                args="", port=6900, web_port=8889, zipname="duds-pre-renewal.zip", folder="PreRenewal",
                edition="Pre-Renewal · classic 2021 client", shortcut="RagnaDuds Pre-Renewal"),
    "re":  dict(src=f"{HOME}/games/kro2026/wine/drive_c/Gravity/kRO2026", exe="ragexe_2026_patched.exe",
                args="1rag1", port=6901, web_port=8888, zipname="duds-renewal.zip", folder="Renewal",
                edition="Renewal · 2026 client", shortcut="RagnaDuds Renewal",
                arial=True),    # exe patched to Arial + Western charset (WARP2026/rAthena_Font.yml): Linux installs real Arial
}
SKIP_DIRS = {"savedata", "_backup_before_english", "USER_AI_before_mirai"}
HOMUN_AI = os.path.join(HERE, "homunculus_ai")
# client asks rAthena's web server (account settings, guild emblems) at AssistAddr: point it at our server
EXT_DIR = "data/luafiles514/lua files/service_korea"
EXT_FILES = ("ExternalSettings_kr.lub", "ExternalSettings_kr_sak.lub")
EXT_TEMPLATE = os.path.join(HERE, "external_settings_template.lub")   # English 2026 version, text Lua    # Mir AI Mod + RagnaDuds preset, put in every AI*/USER_AI
SKIP_FILES = {"Ragexe.exe", "Ragnarok.exe"}           # official, unpatched: not for our server
SKIP_RE = re.compile(r"\.(bak|bak-[\w-]+|disabled)$", re.I)
STORED = {".grf", ".zip", ".mp3", ".bmp", ".jpg", ".png", ".avi", ".bik"}   # already compressed / big
# Our screens and item pictures go in GRF archives listed FIRST in DATA.INI. Names inside a GRF are the client's
# own cp949 bytes, so they work whatever the Windows language settings. (Loose files in Korean-named folders
# don't: the client asks Windows for the folder name in the system code page, which differs between PCs.)
#  - ragnaduds.grf: warning screen before the login (the 3 kRO age-warning pictures) + renewal item pictures
#    fixed by cashshop/build_shop.py (client/grf_items/)
#  - ragnaduds_login<N>.grf: login screen N (t_login.jpg for the 2026 client, bgi_temp.bmp for older ones).
#    The launcher (launch.ps1 / ragnaduds.sh) points DATA.INI line 0 at a random one at every start.
SCREENS = os.path.join(HERE, "login")                  # build/installer/make_assets.py
GRF_ITEMS = os.path.join(HERE, "grf_items")            # cashshop/build_shop.py
ITEMINFO = {"System/itemInfo_true.lub": os.path.join(HERE, "itemInfo_true.lub"),   # renewal item info loader
            "System/itemInfo_RD.lua": os.path.join(HERE, "itemInfo_RD.lua")}       # + our fixes (build_shop.py)
UI = "data\\texture\\유저인터페이스"
MAIN_GRF, LOGIN_GRF = "ragnaduds.grf", "ragnaduds_login{}.grf"
# screens copied loose into the dev clients by earlier versions: never ship them (they'd win over the GRFs)
LOOSE_SCREENS = re.compile(r"(?i)^data/texture/[^/]+/(t_login\.jpg|bgi_temp\.bmp|login_interface/warning\d?\.bmp)$")


def game_grfs(edition, tmpdir):
    """Build our GRFs in tmpdir. Returns ({name in the game folder: path}, [login grf names])."""
    main = {}
    entrance = os.path.join(SCREENS, "entrance.bmp")
    if os.path.exists(entrance):
        for w in ("warning.bmp", "warning2.bmp", "warning3.bmp"):
            main[f"{UI}\\login_interface\\{w}"] = open(entrance, "rb").read()
    if edition == "re" and os.path.isdir(GRF_ITEMS):
        for root, _, files in os.walk(GRF_ITEMS):
            for f in files:
                rel = os.path.relpath(os.path.join(root, f), GRF_ITEMS).replace(os.sep, "\\")
                main[rel] = open(os.path.join(root, f), "rb").read()
    out, logins = {}, []
    if main:
        grf.write(os.path.join(tmpdir, MAIN_GRF), main); out[MAIN_GRF] = os.path.join(tmpdir, MAIN_GRF)
    n = 1
    while os.path.exists(os.path.join(SCREENS, f"{n}.jpg")):
        files = {f"{UI}\\t_login.jpg": open(os.path.join(SCREENS, f"{n}.jpg"), "rb").read()}
        if os.path.exists(os.path.join(SCREENS, f"{n}.bmp")):
            files[f"{UI}\\bgi_temp.bmp"] = open(os.path.join(SCREENS, f"{n}.bmp"), "rb").read()
        name = LOGIN_GRF.format(n); grf.write(os.path.join(tmpdir, name), files)
        out[name] = os.path.join(tmpdir, name); logins.append(name); n += 1
    return out, logins


# No web pages: the official exes open Gravity's sites on exit and payment/"charge" pages from the cash shop,
# and the translated msgstringtable.txt adds donation links. Every web address is blanked in what we ship
# (same length, zero-filled in the exe; empty line in the table), so nothing opens. Your game folder is untouched.
URL = re.compile(rb"https?://[\x21-\x7e]+")


def no_web_exe(data):
    def blank(m):
        u = m.group(0)
        return u if b"schemas" in u or b"w3.org" in u else b"\0" * len(u)   # keep the manifest's XML namespaces
    return URL.sub(blank, data)


def no_web_msgstrings(data):
    return b"\n".join(b"#\r" if URL.match(l.lstrip()) and l.rstrip().endswith((b"#", b"#\r")) else l
                       for l in data.split(b"\n"))


# Cash shop tab labels (renewal): the client shows the 9 tabs (server order New, Hot, Limited, Rental, Permanent,
# Scrolls, Consumables, Other, Sale) with consecutive msgstringtable lines "New#", "Popular#", "Limited Sale#", ...
# Our labels come from cashshop/shop.yml (tab_labels), so the tabs read Beginner, 2nd Class, ... in game.
SHOP_YML = os.path.join(HERE, "..", "cashshop", "shop.yml")
TAB_ORDER = ["New", "Hot", "Limited", "Rental", "Permanent", "Scrolls", "Consumables", "Other", "Sale"]
TAB_DEFAULT = [b"New", b"Popular", b"Limited Sale", b"Rental Equipment", b"Permanent Equipment", b"Scrolls",
               b"Consumables", b"Other", b"Special"]


def cash_tab_labels(data):
    import yaml
    labels = (yaml.safe_load(open(SHOP_YML)) or {}).get("tab_labels") or {}
    lines = data.split(b"\n")
    strip = [l.rstrip(b"\r").rstrip(b"#") for l in lines]
    for i in range(len(lines) - len(TAB_DEFAULT)):
        if strip[i:i + len(TAB_DEFAULT)] == TAB_DEFAULT:
            for k, tab in enumerate(TAB_ORDER):
                if labels.get(tab):
                    lines[i + k] = str(labels[tab]).encode("latin-1") + b"#" + (b"\r" if lines[i + k].endswith(b"\r") else b"")
            return b"\n".join(lines)
    sys.exit("cash shop tab labels not found in msgstringtable.txt")


def data_ini(src, ours):
    """(name, bytes) of the client's DATA.INI with our GRFs listed first."""
    name = next(f for f in os.listdir(src) if f.lower() == "data.ini")
    old = [l.split("=", 1)[1].strip() for l in open(os.path.join(src, name), encoding="latin-1")
           if re.match(r"\s*\d+\s*=", l)]
    grfs = ours + [g for g in old if g not in ours]
    return name, ("[Data]\r\n" + "".join(f"{i}={g}\r\n" for i, g in enumerate(grfs))).encode("latin-1")


INSTALLER_FILES = ["install.ps1", "uninstall.ps1", "launch.ps1", "linux_install.py", "ragnaduds.ico", "ragnaduds.png", "duds_ok.png", "duds_ok_bg.png", "PressStart2P-Regular.ttf"]


def build_game_zip(c, edition, addr, path):
    def clientinfo(p):
        x = open(p, encoding="latin-1").read()
        x = re.sub(r"<address>.*?</address>", f"<address>{addr}</address>", x)
        x = re.sub(r"<display>.*?</display>", f"<display>RagnaDuds {c['folder']}</display>", x)
        return x.encode("latin-1")
    n = size = 0; files_meta = {}
    tmpdir = tempfile.mkdtemp(prefix="ragnaduds-grf-")
    grfs, logins = game_grfs(edition, tmpdir)
    ini_name, ini = data_ini(c["src"], logins[:1] + [g for g in grfs if g not in logins])
    ours = {g.lower() for g in grfs} | {ini_name.lower()}
    if edition == "re": ours |= {k.lower() for k in ITEMINFO}
    # Windows (and PowerShell's JSON reader) ignore upper/lower case: 2 paths that differ only in case would
    # overwrite each other. Keep the newest (e.g. the English tipoftheday.txt over Korean tipOfTheDay.txt).
    newest = {}
    for root, dirs, files in os.walk(c["src"]):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            full = os.path.join(root, f); key = os.path.relpath(full, c["src"]).replace(os.sep, "/").lower()
            if key not in newest or os.path.getmtime(full) > os.path.getmtime(newest[key]): newest[key] = full
    with zipfile.ZipFile(path, "w", allowZip64=True) as z:
        for root, dirs, files in os.walk(c["src"]):
            rel_root = os.path.relpath(root, c["src"])
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            if re.fullmatch(r"AI[^/]*/USER_AI(/.*)?", rel_root.replace(os.sep, "/")):
                continue                                        # replaced by our homunculus AI below
            for f in files:
                if f in SKIP_FILES or SKIP_RE.search(f):
                    continue
                rel = os.path.normpath(os.path.join(rel_root, f)).replace(os.sep, "/")
                full = os.path.join(root, f)
                if newest.get(rel.lower()) != full:
                    print(f"  skipping {rel}: same name as {os.path.relpath(newest[rel.lower()], c['src'])} on Windows (older)")
                    continue
                if rel.lower() in ours or LOOSE_SCREENS.match(rel):
                    continue                                    # ours, written below
                if rel.lower() in {f"{EXT_DIR}/{x}".lower() for x in EXT_FILES}:
                    continue                                    # written below, pointed at our web server
                if f == c["exe"] or rel.lower() == "data/msgstringtable.txt":
                    raw = open(full, "rb").read()
                    data = no_web_exe(raw) if f == c["exe"] else no_web_msgstrings(raw)
                    if edition == "re" and f != c["exe"]: data = cash_tab_labels(data)
                    z.writestr(rel, data, zipfile.ZIP_DEFLATED)
                    files_meta[rel] = len(data); n += 1; size += len(data)
                    if f == c["exe"]: exe_sha = hashlib.sha256(data).hexdigest()
                    continue
                if rel.lower() in ("data/clientinfo.xml", "data/sclientinfo.xml"):
                    data = clientinfo(full); z.writestr(rel, data, zipfile.ZIP_DEFLATED)
                    files_meta[rel] = len(data); n += 1; size += len(data); continue
                method = zipfile.ZIP_STORED if os.path.splitext(f)[1].lower() in STORED else zipfile.ZIP_DEFLATED
                z.write(full, rel, method)
                files_meta[rel] = os.path.getsize(full); n += 1; size += files_meta[rel]
        # web server address for account settings / guild emblems
        for x in EXT_FILES:
            local = os.path.join(c["src"], EXT_DIR, x)
            src = local if os.path.exists(local) and open(local, "rb").read(4) != b"\x1bLua" else EXT_TEMPLATE
            txt = open(src, encoding="latin-1").read()
            txt, hits = re.subn(r'AssistAddr\s*=\s*"[^"]*"', f'AssistAddr = "{addr}:{c["web_port"]}"', txt)
            if hits != 1: sys.exit(f"AssistAddr not found in {src}")
            rel = f"{EXT_DIR}/{x}"; data = txt.encode("latin-1")
            z.writestr(rel, data, zipfile.ZIP_DEFLATED); files_meta[rel] = len(data); n += 1; size += len(data)
        # our GRFs (screens, item pictures) + DATA.INI listing them first, + renewal item info fixes
        for rel, src in grfs.items():
            z.write(src, rel, zipfile.ZIP_STORED)
            files_meta[rel] = os.path.getsize(src); n += 1; size += files_meta[rel]
        z.writestr(ini_name, ini, zipfile.ZIP_DEFLATED); files_meta[ini_name] = len(ini); n += 1
        if edition == "re":
            for rel, src in ITEMINFO.items():
                if not os.path.exists(src): sys.exit(f"missing {src} (run: python3 cashshop/build_shop.py)")
                z.write(src, rel, zipfile.ZIP_DEFLATED)
                files_meta[rel] = os.path.getsize(src); n += 1; size += files_meta[rel]
        # homunculus AI: same files in every AI folder the exe may read (AI/, AI_sakray/)
        for ai_dir in sorted(d for d in os.listdir(c["src"]) if re.fullmatch(r"AI(_\w+)?", d) and os.path.isdir(os.path.join(c["src"], d))):
            for f in sorted(os.listdir(HOMUN_AI)):
                rel = f"{ai_dir}/USER_AI/{f}"
                z.write(os.path.join(HOMUN_AI, f), rel, zipfile.ZIP_DEFLATED)
                files_meta[rel] = os.path.getsize(os.path.join(HOMUN_AI, f)); n += 1; size += files_meta[rel]
    for f in grfs.values(): os.remove(f)
    os.rmdir(tmpdir)
    # exe_sha: of the exe as shipped (web addresses blanked), set while packing
    # list of [path, size] (not a dict): PowerShell's ConvertFrom-Json rejects keys that differ only in case
    return n, size, {"files": [[k, v] for k, v in files_meta.items()], "exe_sha256": exe_sha}, \
        {"ini": ini_name, "grfs": logins}


# Auto-update (the launcher, see installer/launch.ps1 and linux_install.py --launch): every game file, unpacked,
# in <out_dir>/patch/<edition>/ + patch.json with [path, size, sha256] for each. Only changed files are rewritten,
# so "./duds.sh files" (rsync) uploads only those. Players' launchers download just the files whose checksum changed.
# Also the launcher scripts themselves (self-update), marked "win" / "linux".
PATCH_EXTRA = {"launch.ps1": "win", "uninstall.ps1": "win", "duds_ok_bg.png": "win", "PressStart2P-Regular.ttf": "win",
               ".installer/linux_install.py": "linux", ".installer/duds_ok_bg.png": "linux",
               ".installer/PressStart2P-Regular.ttf": "linux"}


def build_patch(game_zip, edition, out_dir):
    """Returns {path: (size, sha256)} of the game files."""
    root = os.path.join(out_dir, "patch", edition)
    index_path = os.path.join(root, "patch.json")
    old = {}
    if os.path.exists(index_path):
        for p, size, sha, *_ in json.load(open(index_path))["files"]:
            old[p] = (size, sha)
    files, written = {}, 0
    with zipfile.ZipFile(game_zip) as z:
        for e in z.infolist():
            if e.is_dir(): continue
            h = hashlib.sha256()
            with z.open(e) as f:
                while chunk := f.read(8 << 20): h.update(chunk)
            sha = h.hexdigest(); files[e.filename] = (e.file_size, sha)
            target = os.path.join(root, *e.filename.split("/"))
            if old.get(e.filename) == (e.file_size, sha) and os.path.exists(target) and os.path.getsize(target) == e.file_size:
                continue
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with z.open(e) as src, open(target + ".part", "wb") as out:
                while chunk := src.read(8 << 20): out.write(chunk)
            os.replace(target + ".part", target); written += 1
    extra = []
    for rel, osname in PATCH_EXTRA.items():
        src = os.path.join(INSTALLER, os.path.basename(rel))
        data = open(src, "rb").read()
        target = os.path.join(root, *rel.split("/")); os.makedirs(os.path.dirname(target), exist_ok=True)
        if not os.path.exists(target) or open(target, "rb").read() != data:
            open(target, "wb").write(data); written += 1
        extra.append([rel, len(data), hashlib.sha256(data).hexdigest(), osname])
    for p in set(old) - set(files) - set(PATCH_EXTRA):              # files the new version doesn't have
        t = os.path.join(root, *p.split("/"))
        if os.path.exists(t): os.remove(t)
    index = {"version": time.strftime("%Y-%m-%d %H:%M:%S"), "edition": edition,
             "files": [[p, s, h] for p, (s, h) in sorted(files.items())] + extra}
    json.dump(index, open(index_path + ".part", "w")); os.replace(index_path + ".part", index_path)
    print(f"Patch files: {written} changed, {len(files)} game files in {root}")
    return files


def web_settings():
    """(site url, login token) for the launcher's downloads, from deploy/hosts/vm/.env."""
    env = {}
    p = os.path.join(HERE, "..", "deploy", "hosts", "vm", ".env")
    if os.path.exists(p):
        for line in open(p):
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1); env[k.strip()] = v.split("#")[0].strip().strip('"')
    site = env.get("SITE_ADDRESS", "")
    url = f"https://{site}" if site and not site.startswith(":") else ""
    return url, env.get("DL_TOKEN", "")


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in CLIENTS:
        sys.exit(__doc__)
    c = CLIENTS[sys.argv[1]]; addr = sys.argv[2]
    out_dir = sys.argv[3] if len(sys.argv) > 3 else os.path.join(HERE, "..", "deploy", "files")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.abspath(os.path.join(out_dir, c["zipname"]))
    if not os.path.isfile(os.path.join(c["src"], c["exe"])):
        sys.exit(f"patched exe not found in {c['src']}")
    missing = [f for f in INSTALLER_FILES if not os.path.isfile(os.path.join(INSTALLER, f))]
    if missing:
        sys.exit(f"missing in client/installer/: {missing} (icons: python3 build/installer/make_assets.py)")

    top = f"RagnaDuds-{c['folder']}"
    cfg = {"title": f"RagnaDuds {c['folder']}", "edition": c["edition"], "folder": c["folder"],
           "shortcut": c["shortcut"], "exe": c["exe"], "args": c["args"], "server": f"{addr}:{c['port']}",
           "host": addr, "port": c["port"], "arial": c.get("arial", False)}
    readme = (f"RagnaDuds · {c['edition']}\r\nServer: {addr}:{c['port']}\r\n\r\n"
              "WINDOWS: double-click 'Install RagnaDuds.bat'. A 'RagnaDuds' icon appears on your desktop.\r\n"
              "  If Windows warns ('Windows protected your PC'): More info -> Run anyway.\r\n"
              "  Windows Defender may also warn about the patched game exe: allow it.\r\n\r\n"
              "LINUX: install Wine first, then run ./install.sh\r\n"
              "  Fedora: sudo dnf install wine winetricks\r\n"
              "  Ubuntu/Debian: sudo dpkg --add-architecture i386 && sudo apt update && sudo apt install wine wine32:i386 winetricks\r\n"
              "  A 'RagnaDuds' launcher appears in your app menu and on the desktop.\r\n\r\n"
              "UPDATE / REPAIR: run the installer again on the same folder (REINSTALL). Your settings are kept.\r\n"
              "UNINSTALL: Windows: Start menu -> RagnaDuds -> Uninstall, Settings -> Apps, or 'Uninstall RagnaDuds.bat'.\r\n"
              "  Linux: 'Uninstall RagnaDuds ...' in the app menu, or ./uninstall.sh\r\n\r\n"
              "Keep the game windowed and smaller than your screen (e.g. 1280x720).\r\n"
              "Homunculus: type /hoai in the chat once and it hunts by itself (AI/USER_AI/README_RagnaDuds.txt).\r\n"
              "Account: ask Duds.\r\n")

    game_tmp = out + ".game.part"; tmp = out + ".part"
    print(f"Packing game files from {c['src']} …")
    n, size, manifest, login_pics = build_game_zip(c, sys.argv[1], addr, game_tmp)
    patch = build_patch(game_tmp, sys.argv[1], out_dir)
    manifest["files"] = [[p, sz, patch[p][1]] for p, sz in manifest["files"]]     # + sha256: the launcher's starting point
    site, token = web_settings()
    if site and token:
        cfg["patch"] = {"url": f"{site}/files/patch/{sys.argv[1]}/", "token": token}
    print("Adding installer …")
    with zipfile.ZipFile(tmp, "w", allowZip64=True) as z:
        z.writestr(f"{top}/Install RagnaDuds.bat",
                   '@echo off\r\ntitle RagnaDuds Setup\r\n'
                   'powershell -NoProfile -ExecutionPolicy Bypass -STA -WindowStyle Hidden '
                   '-File "%~dp0installer\\install.ps1"\r\n', zipfile.ZIP_DEFLATED)
        z.writestr(f"{top}/Uninstall RagnaDuds.bat",
                   '@echo off\r\ntitle RagnaDuds Uninstall\r\n'
                   'powershell -NoProfile -ExecutionPolicy Bypass -STA -WindowStyle Hidden '
                   '-File "%~dp0installer\\uninstall.ps1"\r\n', zipfile.ZIP_DEFLATED)
        for name, what, extra in (("install.sh", "installer", ""), ("uninstall.sh", "uninstaller", " --uninstall")):
            sh = zipfile.ZipInfo(f"{top}/{name}"); sh.external_attr = 0o100755 << 16; sh.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(sh, f'#!/bin/sh\n# RagnaDuds {what} for Linux\ncd "$(dirname "$0")" || exit 1\n'
                           f'exec python3 installer/linux_install.py{extra} "$@"\n')
        z.writestr(f"{top}/README.txt", readme, zipfile.ZIP_DEFLATED)
        cfg["login_pics"] = login_pics     # launcher: DATA.INI line 0 = one of these at random
        z.writestr(f"{top}/installer/config.json", json.dumps(cfg, indent=2), zipfile.ZIP_DEFLATED)
        z.writestr(f"{top}/installer/manifest.json", json.dumps(manifest), zipfile.ZIP_DEFLATED)   # for the file check
        for f in INSTALLER_FILES:
            z.write(os.path.join(INSTALLER, f), f"{top}/installer/{f}", zipfile.ZIP_DEFLATED)
        z.write(game_tmp, f"{top}/game.zip", zipfile.ZIP_STORED)
    os.remove(game_tmp); os.replace(tmp, out)
    print(f"{out}\n  {n} game files, {size/1024**3:.2f} GB in → {os.path.getsize(out)/1024**3:.2f} GB download, "
          f"server {addr}:{c['port']}")

    # small "launcher upgrade" download: gives an existing install the auto-updating launcher, no game files
    up = out[:-4] + "-launcher-upgrade.zip"; utop = f"{top}-Upgrade"
    with zipfile.ZipFile(up + ".part", "w") as z:
        z.writestr(f"{utop}/Upgrade RagnaDuds.bat",
                   '@echo off\r\ntitle RagnaDuds launcher upgrade\r\n'
                   'powershell -NoProfile -ExecutionPolicy Bypass -STA -WindowStyle Hidden '
                   '-File "%~dp0installer\\upgrade.ps1"\r\n', zipfile.ZIP_DEFLATED)
        sh = zipfile.ZipInfo(f"{utop}/upgrade.sh"); sh.external_attr = 0o100755 << 16; sh.compress_type = zipfile.ZIP_DEFLATED
        z.writestr(sh, '#!/bin/sh\n# RagnaDuds launcher upgrade for Linux\ncd "$(dirname "$0")" || exit 1\n'
                       'exec python3 installer/linux_install.py --upgrade "$@"\n')
        z.writestr(f"{utop}/README.txt",
                   f"RagnaDuds · {c['edition']} · launcher upgrade\r\n\r\n"
                   "For players who ALREADY have the game installed: adds the launcher that updates the game by itself\r\n"
                   "(only changed files are downloaded). No need to download the whole game again.\r\n\r\n"
                   "WINDOWS: close the game, double-click 'Upgrade RagnaDuds.bat'.\r\n"
                   "LINUX: close the game, run ./upgrade.sh (or ./upgrade.sh --dest /path/to/the/game/folder).\r\n\r\n"
                   "Then open 'RagnaDuds' from your desktop. The first start checks every file, so it takes a bit longer.\r\n",
                   zipfile.ZIP_DEFLATED)
        z.writestr(f"{utop}/installer/config.json", json.dumps(cfg, indent=2), zipfile.ZIP_DEFLATED)
        for f in INSTALLER_FILES + ["upgrade.ps1"]:
            if f in ("install.ps1",): continue
            z.write(os.path.join(INSTALLER, f), f"{utop}/installer/{f}", zipfile.ZIP_DEFLATED)
    os.replace(up + ".part", up)
    print(f"{up}\n  launcher upgrade, {os.path.getsize(up)/1024:.0f} KB")


if __name__ == "__main__":
    main()
