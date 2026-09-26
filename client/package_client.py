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
import hashlib, json, os, re, sys, zipfile

HOME = os.path.expanduser("~")
HERE = os.path.dirname(os.path.abspath(__file__))
INSTALLER = os.path.join(HERE, "installer")
CLIENTS = {
    "pre": dict(src=f"{HOME}/games/kro2021/wine/drive_c/Gravity/RagnarokKRO", exe="ragexe_2021_patched.exe",
                args="", port=6900, web_port=8889, zipname="duds-pre-renewal.zip", folder="PreRenewal",
                edition="Pre-Renewal · classic 2021 client", shortcut="RagnaDuds Pre-Renewal"),
    "re":  dict(src=f"{HOME}/games/kro2026/wine/drive_c/Gravity/kRO2026", exe="ragexe_2026_patched.exe",
                args="1rag1", port=6901, web_port=8888, zipname="duds-renewal.zip", folder="Renewal",
                edition="Renewal · 2026 client", shortcut="RagnaDuds Renewal"),
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
INSTALLER_FILES = ["install.ps1", "linux_install.py", "ragnaduds.ico", "ragnaduds.png", "duds_ok.png", "duds_ok_bg.png", "PressStart2P-Regular.ttf"]


def build_game_zip(c, addr, path):
    def clientinfo(p):
        x = open(p, encoding="latin-1").read()
        x = re.sub(r"<address>.*?</address>", f"<address>{addr}</address>", x)
        x = re.sub(r"<display>.*?</display>", f"<display>RagnaDuds {c['folder']}</display>", x)
        return x.encode("latin-1")
    n = size = 0; files_meta = {}
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
                if rel.lower() in {f"{EXT_DIR}/{x}".lower() for x in EXT_FILES}:
                    continue                                    # written below, pointed at our web server
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
        # homunculus AI: same files in every AI folder the exe may read (AI/, AI_sakray/)
        for ai_dir in sorted(d for d in os.listdir(c["src"]) if re.fullmatch(r"AI(_\w+)?", d) and os.path.isdir(os.path.join(c["src"], d))):
            for f in sorted(os.listdir(HOMUN_AI)):
                rel = f"{ai_dir}/USER_AI/{f}"
                z.write(os.path.join(HOMUN_AI, f), rel, zipfile.ZIP_DEFLATED)
                files_meta[rel] = os.path.getsize(os.path.join(HOMUN_AI, f)); n += 1; size += files_meta[rel]
    exe_sha = hashlib.sha256(open(os.path.join(c["src"], c["exe"]), "rb").read()).hexdigest()
    return n, size, {"files": files_meta, "exe_sha256": exe_sha}


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
           "host": addr, "port": c["port"]}
    readme = (f"RagnaDuds · {c['edition']}\r\nServer: {addr}:{c['port']}\r\n\r\n"
              "WINDOWS: double-click 'Install RagnaDuds.bat'. A 'RagnaDuds' icon appears on your desktop.\r\n"
              "  If Windows warns ('Windows protected your PC'): More info -> Run anyway.\r\n"
              "  Windows Defender may also warn about the patched game exe: allow it.\r\n\r\n"
              "LINUX: install Wine first, then run ./install.sh\r\n"
              "  Fedora: sudo dnf install wine winetricks\r\n"
              "  Ubuntu/Debian: sudo dpkg --add-architecture i386 && sudo apt update && sudo apt install wine wine32:i386 winetricks\r\n"
              "  A 'RagnaDuds' launcher appears in your app menu and on the desktop.\r\n\r\n"
              "Keep the game windowed and smaller than your screen (e.g. 1280x720).\r\n"
              "Homunculus: type /hoai in the chat once and it hunts by itself (AI/USER_AI/README_RagnaDuds.txt).\r\n"
              "Account: ask Duds.\r\n")

    game_tmp = out + ".game.part"; tmp = out + ".part"
    print(f"Packing game files from {c['src']} …")
    n, size, manifest = build_game_zip(c, addr, game_tmp)
    print("Adding installer …")
    with zipfile.ZipFile(tmp, "w", allowZip64=True) as z:
        z.writestr(f"{top}/Install RagnaDuds.bat",
                   '@echo off\r\ntitle RagnaDuds Setup\r\n'
                   'powershell -NoProfile -ExecutionPolicy Bypass -STA -WindowStyle Hidden '
                   '-File "%~dp0installer\\install.ps1"\r\n', zipfile.ZIP_DEFLATED)
        sh = zipfile.ZipInfo(f"{top}/install.sh"); sh.external_attr = 0o100755 << 16; sh.compress_type = zipfile.ZIP_DEFLATED
        z.writestr(sh, '#!/bin/sh\n# RagnaDuds installer for Linux\ncd "$(dirname "$0")" || exit 1\n'
                       'exec python3 installer/linux_install.py "$@"\n')
        z.writestr(f"{top}/README.txt", readme, zipfile.ZIP_DEFLATED)
        z.writestr(f"{top}/installer/config.json", json.dumps(cfg, indent=2), zipfile.ZIP_DEFLATED)
        z.writestr(f"{top}/installer/manifest.json", json.dumps(manifest), zipfile.ZIP_DEFLATED)   # for the file check
        for f in INSTALLER_FILES:
            z.write(os.path.join(INSTALLER, f), f"{top}/installer/{f}", zipfile.ZIP_DEFLATED)
        z.write(game_tmp, f"{top}/game.zip", zipfile.ZIP_STORED)
    os.remove(game_tmp); os.replace(tmp, out)
    print(f"{out}\n  {n} game files, {size/1024**3:.2f} GB in → {os.path.getsize(out)/1024**3:.2f} GB download, "
          f"server {addr}:{c['port']}")


if __name__ == "__main__":
    main()
