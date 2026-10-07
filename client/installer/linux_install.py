#!/usr/bin/env python3
"""RagnaDuds installer for Linux (started by ./install.sh).

Unpacks game.zip into ~/.local/share/ragnaduds/<edition>/, prepares a Wine prefix (+ CJK fonts),
and creates a "RagnaDuds" launcher in the app menu and on the desktop.
Progress UI: a GTK window with the photo as background if available, else Tk (photo beside it), else zenity, else a terminal bar.
Running it again on the same folder updates it: files replaced, files the new version doesn't have removed,
Wine + settings kept. An "Uninstall …" app menu entry (or ./uninstall.sh in the download) removes everything.
Options: --dest DIR    install somewhere else
         --no-fonts    skip the winetricks font download
         --text        force the terminal progress bar
         --uninstall   remove this edition (game folder, Wine setup, launchers)
         --launch      the launcher (menu / desktop entries): download changed files, then PLAY
         --upgrade     give an existing install the launcher (the small "launcher upgrade" download)
"""
import hashlib, json, os, re, shutil, socket, subprocess, sys, threading, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CFG = json.load(open(os.path.join(HERE, "config.json")))
ARGS = sys.argv[1:]
DEST = os.path.expanduser(ARGS[ARGS.index("--dest") + 1]) if "--dest" in ARGS else \
    os.path.expanduser(f"~/.local/share/ragnaduds/{CFG['folder']}")
if os.path.basename(HERE) == ".installer":        # the copy kept in the game folder (for the uninstaller)
    DEST = os.path.dirname(HERE)
PREFIX = os.path.join(DEST, "wine")
APPS = os.path.expanduser("~/.local/share/applications")
LAUNCHER = f"ragnaduds-{CFG['folder'].lower()}"               # .desktop file names
FONT_DIR = os.path.expanduser("~/.local/share/fonts/ragnaduds")   # shared by both editions
# kept on reinstall: Wine (with its fonts), settings, screenshots, chat logs + our own files in the game folder
KEEP_DIRS = {"wine", "savedata", "screenshot", "chat", "replay", ".installer"}
KEEP_FILES = {"ragnaduds.png", "ragnaduds.sh", "ragnaduds-install.json", "ragnaduds-patch.json"}
PATCH_STATE = "ragnaduds-patch.json"     # auto-update: path -> sha256 of what is installed (see update())


# ---------------- errors: the whole text, so friends can copy it and send it ----------------
def error_report(e):
    import platform, traceback
    distro = ""
    try:
        distro = next((l.split("=", 1)[1].strip().strip('"') for l in open("/etc/os-release")
                       if l.startswith("PRETTY_NAME=")), "")
    except OSError: pass
    return (f"RagnaDuds installer error ({CFG['edition']})\n{e}\n\n"
            + "".join(traceback.format_exception(type(e), e, e.__traceback__))
            + f"\nSystem: {distro or platform.platform()} · Python {platform.python_version()} · "
              f"Wine: {shutil.which('wine') or 'not installed'}\nFolder: {DEST}")


def copy_text(text):
    """Clipboard without a GUI toolkit (zenity / terminal): wl-copy, xclip or xsel. True if one worked."""
    for cmd in (["wl-copy"], ["xclip", "-selection", "clipboard"], ["xsel", "--clipboard", "--input"]):
        if shutil.which(cmd[0]):
            try:
                subprocess.run(cmd, input=text, text=True, timeout=5, check=True); return True
            except Exception: pass
    return False


# ---------------- the actual work (reports progress 0..100 + a message) ----------------
def install(report):
    if not shutil.which("wine"):
        raise RuntimeError("Wine is not installed.\n  Fedora: sudo dnf install wine winetricks\n"
                           "  Ubuntu/Debian (the game is 32-bit):\n    sudo dpkg --add-architecture i386 && sudo apt update && sudo apt install wine wine32:i386 winetricks\n  Arch: sudo pacman -S wine winetricks")
    zpath = os.path.join(ROOT, "game.zip")
    if not os.path.exists(zpath):
        raise RuntimeError("game.zip not found. Unzip the whole download first.")
    if game_running():
        raise RuntimeError("The game is still open: close it, then run the installer again.")
    reinstall = installed()
    if reinstall: report(0, "Already installed: updating it (your settings are kept)…")
    os.makedirs(DEST, exist_ok=True)
    dest_real = os.path.realpath(DEST)
    with zipfile.ZipFile(zpath) as z:
        entries = z.infolist(); total = sum(e.file_size for e in entries) or 1; done = 0
        for e in entries:
            target = os.path.realpath(os.path.join(DEST, e.filename))
            if not target.startswith(dest_real + os.sep):           # unsafe path, skip
                continue
            if e.is_dir():
                os.makedirs(target, exist_ok=True); continue
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with z.open(e) as src, open(target, "wb") as out:
                while chunk := src.read(4 << 20):
                    out.write(chunk); done += len(chunk)
                    report(80 * done / total, f"Unpacking the game… {done/1024**3:.1f} / {total/1024**3:.1f} GB")

    new_files = verify(report)
    if reinstall:
        report(81, "Removing files from the old version…")
        RESULT["notes"].append(f"✔ updated: {remove_old_files(new_files)} old file(s) removed, settings kept")

    env = dict(os.environ, WINEPREFIX=PREFIX, WINEDEBUG="-all")
    report(82, "Preparing Wine (first time takes a minute)…")
    subprocess.run(["wineboot", "-u"], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if "--no-fonts" not in ARGS and shutil.which("winetricks"):
        report(88, "Installing fonts (a few minutes, downloads once)…")
        subprocess.run(["winetricks", "-q", "cjkfonts"], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elif "--no-fonts" not in ARGS:
        RESULT["notes"].append("⚠ winetricks not found: fonts skipped, some text may show as boxes.\n"
                               f"  Install winetricks, then run: WINEPREFIX=\"{PREFIX}\" winetricks -q cjkfonts")
    # the game's own font is Gulim (Microsoft, can't be shipped). With it the text looks like the original game;
    # without it Wine uses a look-alike (blurrier). Taken from next to install.sh or the user's font folders.
    gulim = None if CFG.get("arial") else find_gulim()
    if CFG.get("arial"):
        fonts = os.path.join(PREFIX, "drive_c", "windows", "Fonts"); os.makedirs(fonts, exist_ok=True)
        if install_arial(fonts, env):
            RESULT["notes"].append("✔ game font: Arial (like bRO)")
        else:
            RESULT["notes"].append("⚠ couldn't download Microsoft Arial: using Wine's look-alike (text a bit blurrier).\n"
                                   "  Run the installer again when online to fix it.")
    elif gulim:
        fonts = os.path.join(PREFIX, "drive_c", "windows", "Fonts"); os.makedirs(fonts, exist_ok=True)
        shutil.copy(gulim, os.path.join(fonts, "gulim.ttc"))
        for name in ("Gulim", "GulimChe", "Dotum", "DotumChe"):       # drop cjkfonts' look-alike aliases
            subprocess.run(["wine", "reg", "delete", r"HKCU\Software\Wine\Fonts\Replacements", "/v", name, "/f"],
                           env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        RESULT["notes"].append("✔ game font: Gulim (original look)")
    elif not CFG.get("arial"):
        RESULT["notes"].append("⚠ original game font (Gulim) not found: using a look-alike.\n"
                               "  For the original look: copy gulim.ttc from a Windows PC with Korean fonts\n"
                               "  (C:\\Windows\\Fonts\\gulim.ttc) next to install.sh and run it again.")

    report(97, "Creating the RagnaDuds shortcut…")
    make_shortcuts()
    report(100, f"Done! Start '{CFG['shortcut']}' from your desktop or app menu.")


def make_shortcuts():
    """Start script, menu/desktop entries (they open the launcher), uninstaller and the launcher's files."""
    shutil.copy(os.path.join(HERE, "ragnaduds.png"), os.path.join(DEST, "ragnaduds.png"))
    launcher = os.path.join(DEST, "ragnaduds.sh")
    lp = CFG.get("login_pics")        # random login picture: DATA.INI line 0 = one of our login GRFs
    pick = ("# login picture: DATA.INI line 0 names the login GRF the game loads first; use the next one (they take turns)\n"
            f'cur=$(sed -n "s/^0=\\([^\\r]*\\).*/\\1/p" "{lp["ini"]}"); set -- {" ".join(lp["grfs"])}; p=$1; prev=\n'
            'for g in "$@"; do [ "$prev" = "$cur" ] && p=$g; prev=$g; done\n'
            f'sed -i "s/^0=[^\\r]*/0=$p/" "{lp["ini"]}" 2>/dev/null\n') if lp and len(lp.get("grfs", [])) > 1 else ""
    with open(launcher, "w") as f:
        f.write("#!/bin/sh\n# Start RagnaDuds with its own Wine prefix\n"
                f'cd "{DEST}" || exit 1\n' + pick +
                "# classic TrueType hinting: crisp small text, like on Windows\n"
                f'export FREETYPE_PROPERTIES="truetype:interpreter-version=35" WINEPREFIX="{PREFIX}" WINEDEBUG="${{WINEDEBUG:--all}}"\n'
                f'exec wine {CFG["exe"]} {CFG["args"]}\n')
    os.chmod(launcher, 0o755)
    desktop = (f"[Desktop Entry]\nType=Application\nName={CFG['shortcut']}\nComment={CFG['title']}\n"
               f"Exec=python3 \"{os.path.join(DEST, '.installer', 'linux_install.py')}\" --launch\nPath={DEST}\nIcon={os.path.join(DEST, 'ragnaduds.png')}\n"
               "Terminal=false\nCategories=Game;\n")
    os.makedirs(APPS, exist_ok=True)
    for d in [APPS, desktop_dir()]:
        if not d: continue
        p = os.path.join(d, f"{LAUNCHER}.desktop")
        with open(p, "w") as f: f.write(desktop)
        os.chmod(p, 0o755)
        subprocess.run(["gio", "set", p, "metadata::trusted", "true"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    # uninstaller: this script + config kept in the game folder, and an "Uninstall …" entry in the app menu
    keep = os.path.join(DEST, ".installer"); os.makedirs(keep, exist_ok=True)
    if os.path.realpath(HERE) != os.path.realpath(keep):
        for f in ("linux_install.py", "config.json", "duds_ok_bg.png", "PressStart2P-Regular.ttf", "ragnaduds.png"):
            if os.path.exists(os.path.join(HERE, f)): shutil.copy(os.path.join(HERE, f), keep)
    if RESULT["shas"]:
        json.dump(RESULT["shas"], open(os.path.join(DEST, PATCH_STATE), "w"))
    with open(os.path.join(DEST, "ragnaduds-install.json"), "w") as f: json.dump(dict(CFG, dest=DEST), f, indent=2)
    with open(os.path.join(APPS, f"{LAUNCHER}-uninstall.desktop"), "w") as f:
        f.write(f"[Desktop Entry]\nType=Application\nName=Uninstall {CFG['shortcut']}\nComment=Remove {CFG['title']}\n"
                f"Exec=python3 \"{os.path.join(keep, 'linux_install.py')}\" --uninstall\n"
                f"Icon={os.path.join(DEST, 'ragnaduds.png')}\nTerminal=false\nCategories=Game;\n")
    if "GNOME" in os.environ.get("XDG_CURRENT_DESKTOP", "").upper():   # GNOME shows no desktop icons by default
        RESULT["notes"].append(f"✔ GNOME hides desktop icons: press the Super key and type RagnaDuds")


RESULT = {"notes": [], "shas": {}}          # sanity-check summary, shown at the end; installed file checksums


def verify(report):
    """Sanity check after unpacking: every file present with the right size, the game exe is
    exactly the packaged one, the client points at our server, and the server answers."""
    man = json.load(open(os.path.join(HERE, "manifest.json")))
    files = man["files"]; bad = []
    if not isinstance(files, dict):
        RESULT["shas"] = {x[0]: x[2] for x in files if len(x) >= 3}            # auto-update starting point
    files = list(files.items()) if isinstance(files, dict) else [tuple(x[:2]) for x in files]   # old dict / new list
    for i, (rel, size) in enumerate(files):
        p = os.path.join(DEST, rel)
        if not os.path.isfile(p) or os.path.getsize(p) != size:
            bad.append(rel)
        if i % 50 == 0:
            report(80 + 1.5 * i / len(files), f"Checking files… {i}/{len(files)}")
    if bad:
        raise RuntimeError(f"{len(bad)} file(s) missing or damaged, e.g. {bad[0]}. Download again and retry.")
    h = hashlib.sha256(open(os.path.join(DEST, CFG["exe"]), "rb").read()).hexdigest()
    if h != man["exe_sha256"]:
        raise RuntimeError("The game exe doesn't match the packaged one (damaged download?).")
    for xml in ("data/clientinfo.xml", "data/sclientinfo.xml"):
        p = os.path.join(DEST, xml)
        if os.path.isfile(p):
            m = re.search(r"<address>(.*?)</address>", open(p, encoding="latin-1").read())
            if not m or m.group(1).strip() != CFG["host"]:
                raise RuntimeError(f"{xml} points to '{m.group(1) if m else '?'}' instead of {CFG['host']}.")
    RESULT["notes"].append(f"✔ {len(files)} files OK · client → {CFG['host']}:{CFG['port']}")
    try:
        socket.create_connection((CFG["host"], CFG["port"]), timeout=4).close()
        RESULT["notes"].append("✔ server is online")
    except OSError:
        RESULT["notes"].append("⚠ server didn't answer right now (offline or maintenance?). The game is installed anyway.")
    return {rel for rel, _ in files}


def find_gulim():
    """gulim.ttc next to install.sh / the installer, or in the user's font folders (any letter case)."""
    places = [ROOT, HERE, DEST, os.path.expanduser("~/.local/share/fonts"), os.path.expanduser("~/.fonts")]
    for place in places:
        for root, _, files in os.walk(place) if os.path.isdir(place) else ():
            if os.path.relpath(root, place).count(os.sep) > 2: continue
            for f in files:
                if f.lower() == "gulim.ttc" and "wine" not in root.split(os.sep):
                    return os.path.join(root, f)
    return None


# Real Microsoft Arial for the renewal client (its exe is patched to draw text in Arial, like bRO; Wine's own
# "Arial" is a look-alike that blurs small bold text such as character names). Microsoft's free core fonts package,
# the same file winetricks uses. Unpacked with cabextract when installed, else by the package itself under Wine
# (/Q /T:<folder> /C: extract only, nothing is installed).
ARIAL_URL = "https://downloads.sourceforge.net/corefonts/arial32.exe"
ARIAL_SHA = "85297a4d146e9c87ac6f74822734bdee5f4b2a722d7eaa584b7f2cbf76f478f6"


def install_arial(fonts, env):
    """Put Microsoft's Arial (.ttf) in the game's Wine fonts folder. Returns True when done."""
    import tempfile, urllib.request
    cache = os.path.join(DEST, ".installer", "arial32.exe")
    try:
        if not (os.path.exists(cache) and hashlib.sha256(open(cache, "rb").read()).hexdigest() == ARIAL_SHA):
            os.makedirs(os.path.dirname(cache), exist_ok=True)
            with urllib.request.urlopen(ARIAL_URL, timeout=60) as r: data = r.read()
            if hashlib.sha256(data).hexdigest() != ARIAL_SHA: return False
            open(cache, "wb").write(data)
        with tempfile.TemporaryDirectory() as tmp:
            if shutil.which("cabextract"):
                subprocess.run(["cabextract", "-q", "-d", tmp, cache], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                subprocess.run(["wine", cache, "/Q", f"/T:Z:{tmp}", "/C"], env=env, timeout=120,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            for f in os.listdir(tmp):
                if f.lower().endswith(".ttf"):
                    shutil.copy(os.path.join(tmp, f), os.path.join(fonts, f.lower()))
        return os.path.exists(os.path.join(fonts, "arial.ttf"))
    except Exception:
        return False


def installed():
    return os.path.isfile(os.path.join(DEST, "ragnaduds-install.json")) or os.path.isfile(os.path.join(DEST, CFG["exe"]))


def game_running():
    """Is this edition's exe running (under Wine)? Only the program itself counts (its first argument,
    e.g. C:\\...\\ragexe.exe), not a command line that merely mentions it."""
    exe = CFG["exe"].lower()
    for pid in filter(str.isdigit, os.listdir("/proc")):
        try:
            prog = open(f"/proc/{pid}/cmdline", "rb").read().split(b"\0")[0].decode("utf-8", "replace")
        except OSError: continue
        if re.split(r"[\\/]", prog)[-1].lower() == exe: return True
    return False


def remove_old_files(new_files):
    """After a reinstall: delete files the new version doesn't have (e.g. old translation files)."""
    removed = 0
    for root, dirs, files in os.walk(DEST):
        rel_root = os.path.relpath(root, DEST)
        if rel_root == ".":
            dirs[:] = [d for d in dirs if d.lower() not in KEEP_DIRS]
        for f in files:
            rel = os.path.normpath(os.path.join(rel_root, f)).replace(os.sep, "/")
            if rel in new_files or (rel_root == "." and f.lower() in KEEP_FILES): continue
            os.remove(os.path.join(root, f)); removed += 1
    for root, dirs, files in os.walk(DEST, topdown=False):             # empty folders left behind
        top = os.path.relpath(root, DEST).split(os.sep)[0].lower()
        if root != DEST and top not in KEEP_DIRS and not os.listdir(root): os.rmdir(root)
    return removed


def dialog(text, question=False):
    """OK message or Yes/No question: GTK, zenity, Tk or the terminal, whichever works. True = OK/Yes."""
    title = f"{CFG['title']} - Uninstall"
    if (os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")) and "--text" not in ARGS:
        try:
            import gi
            gi.require_version("Gtk", "3.0"); gi.require_version("Gdk", "3.0")
            from gi.repository import Gtk
            d = Gtk.MessageDialog(message_type=Gtk.MessageType.QUESTION if question else Gtk.MessageType.INFO,
                                  buttons=Gtk.ButtonsType.YES_NO if question else Gtk.ButtonsType.OK, text=title)
            d.format_secondary_text(text); d.set_title(title); r = d.run(); d.destroy()
            while Gtk.events_pending(): Gtk.main_iteration()
            return r == Gtk.ResponseType.YES if question else True
        except (ImportError, ValueError): pass
        if shutil.which("zenity"):
            safe = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            return subprocess.run(["zenity", "--question" if question else "--info", f"--title={title}",
                                   "--width=460", f"--text={safe}"]).returncode == 0
        try:
            from tkinter import Tk, messagebox
            Tk().withdraw()
            return messagebox.askyesno(title, text) if question else bool(messagebox.showinfo(title, text) or True)
        except ImportError: pass
    print(f"\n{text}")
    if not question: return True
    return sys.stdin.isatty() and input("Continue? [y/N] ").strip().lower().startswith("y")


def uninstall():
    """Remove this edition: the game folder (with its Wine setup and settings), the launchers,
    and the pixel font if no other RagnaDuds edition is left."""
    found = installed()
    what = f"the game folder with its Wine setup and your settings:\n   {DEST}\n - " if found else ""
    if not dialog(f"Remove {CFG['title']} from this computer?\n\nThis deletes:\n - {what}the app menu and desktop launchers", True):
        return 0
    if found:
        real = os.path.realpath(DEST)
        ours = os.path.isfile(os.path.join(real, CFG["exe"])) or os.path.isfile(os.path.join(real, "ragnaduds-install.json"))
        if real in ("/", os.path.realpath(os.path.expanduser("~"))) or not ours:
            dialog(f"Refusing to delete {DEST} (not a RagnaDuds game folder)."); return 1
        while game_running():
            if not dialog(f"{CFG['title']} is still open. Close the game, then press Yes to continue.", True): return 0
    try:
        for d in (APPS, desktop_dir()):
            for n in (f"{LAUNCHER}.desktop", f"{LAUNCHER}-uninstall.desktop"):
                if d and os.path.exists(os.path.join(d, n)): os.remove(os.path.join(d, n))
        if found:
            os.chdir(os.path.expanduser("~")); shutil.rmtree(DEST)
        base = os.path.expanduser("~/.local/share/ragnaduds")
        if os.path.isdir(base) and not any(os.path.isfile(os.path.join(base, e, "ragnaduds.sh")) for e in os.listdir(base)):
            shutil.rmtree(base, ignore_errors=True)                      # no edition left: the font goes too
            if os.path.isdir(FONT_DIR):
                shutil.rmtree(FONT_DIR, ignore_errors=True)
                subprocess.run(["fc-cache", "-f"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        text = error_report(e)
        copied = copy_text(text)
        dialog(("Uninstall stopped. The error was copied: paste it to Duds.\n\n" if copied else
                "Uninstall stopped. Copy this and send it to Duds:\n\n") + text)
        return 1
    dialog(f"{CFG['title']} was removed. Bye! The Porings will miss you (they won't).")
    return 0


def start_game():
    subprocess.Popen([os.path.join(DEST, "ragnaduds.sh")], cwd=DEST, start_new_session=True,
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


START_LABEL = "Start and YEAAAAAAAAAAH!"
QUIPS = ["\"Installing. Don't touch anything, you degenerate.\"",
         "\"Checking every file. Yes, every single one. Relax.\"",
         "\"The Poring is watching you install. Stay calm.\"",
         "\"Almost there. Hydrate. Or don't.\"",
         "\"Setting up Wine. The good kind, not the drinking kind.\""]


def desktop_dir():
    try:
        d = subprocess.run(["xdg-user-dir", "DESKTOP"], capture_output=True, text=True).stdout.strip()
    except FileNotFoundError:
        d = os.path.expanduser("~/Desktop")
    return d if d and os.path.isdir(d) else None


# ---------------- progress front-ends ----------------
def run_tk():
    import tkinter as tk
    from tkinter import ttk
    root = tk.Tk(); root.title(f"{CFG['title']} - Setup"); root.resizable(False, False)
    bg, fg, gold = "#221d33", "#f6ecd2", "#ffd166"
    root.configure(bg=bg)
    try: root.iconphoto(True, tk.PhotoImage(file=os.path.join(HERE, "ragnaduds.png")))
    except tk.TclError: pass
    photo = tk.PhotoImage(file=os.path.join(HERE, "duds_ok.png"))
    tk.Label(root, image=photo, bg=bg).grid(row=0, column=0, rowspan=6, padx=10, pady=10)
    tk.Label(root, text="RagnaDuds", font=("Sans", 20, "bold"), fg=gold, bg=bg).grid(row=0, column=1, sticky="w", padx=(0, 16))
    tk.Label(root, text=CFG["edition"], font=("Sans", 11), fg=fg, bg=bg).grid(row=1, column=1, sticky="w")
    msg = tk.StringVar(value="Installing… thumbs up!")
    tk.Label(root, textvariable=msg, font=("Sans", 10), fg=fg, bg=bg, wraplength=280, justify="left").grid(row=2, column=1, sticky="w", pady=8)
    bar = ttk.Progressbar(root, length=280, maximum=100); bar.grid(row=3, column=1, sticky="w")
    notes = tk.StringVar(value="")
    tk.Label(root, textvariable=notes, font=("Sans", 9), fg=fg, bg=bg, wraplength=280, justify="left").grid(row=4, column=1, sticky="w", pady=6)
    err_box = tk.Text(root, width=44, height=7, wrap="word", bg="black", fg="#ff6b6b", font=("Monospace", 8),
                      relief="solid", bd=1, cursor="hand2")
    copy_btn = tk.Button(root, text="COPY ERROR", bg="#ff8fb1", font=("Sans", 10, "bold"))
    btn = tk.Button(root, text=START_LABEL, state="disabled", bg=gold, font=("Sans", 11, "bold"),
                    command=lambda: (start_game(), root.destroy()))
    btn.grid(row=7, column=1, sticky="e", padx=(0, 16), pady=10)
    state = {"p": 0, "m": msg.get(), "done": False, "err": None, "report": ""}

    def copy_error(*_):
        root.clipboard_clear(); root.clipboard_append(state["report"]); root.update()
        copy_btn.configure(text="COPIED! Paste it to Duds")
    copy_btn.configure(command=copy_error); err_box.bind("<Button-1>", copy_error)
    def report(p, m): state.update(p=p, m=m)
    def worker():
        try: install(report)
        except Exception as e: state["err"] = str(e); state["report"] = error_report(e)
        state["done"] = True
    def poll():
        bar["value"] = state["p"]; msg.set(state["err"] or state["m"])
        if state["done"]:
            notes.set("\n".join(RESULT["notes"]))
            if state["err"]:
                err_box.insert("1.0", state["report"]); err_box.configure(state="disabled")
                err_box.grid(row=5, column=1, sticky="w", padx=(0, 16))
                copy_btn.grid(row=6, column=1, sticky="we", padx=(0, 16), pady=(6, 0))
                btn.configure(text="Close", state="normal", command=root.destroy)
            else: btn.configure(state="normal")
            return
        root.after(150, poll)
    threading.Thread(target=worker, daemon=True).start(); poll(); root.mainloop()
    return 1 if state["err"] else 0


GTK_CSS = b"""
      window { background-color: #14121f; }
      .panel { background-color: rgba(34, 29, 51, 0.93); border: 4px solid #6b4f2a; margin: 8px 10px 10px;
               box-shadow: inset 0 0 0 4px #000, inset 0 0 0 7px #c9a25b, 5px 5px 0 #000; padding: 16px 18px; }
      .title { font-family: "Press Start 2P", monospace; font-size: 17px; color: #ffd166;
               text-shadow: 2px 2px #7a3e12, 4px 4px #000; }
      .npc   { font-family: "Press Start 2P", monospace; font-size: 8px; color: #7cc4ff; }
      .text  { font-family: monospace; font-size: 13px; color: #f6ecd2; }
      .quip  { font-family: monospace; font-size: 12px; color: #ff8fb1; font-style: italic; }
      .notes { font-family: monospace; font-size: 11px; color: #7ee081; }
      progressbar trough { min-height: 16px; background-color: #000; border: 2px solid #444; border-radius: 0; }
      progressbar progress { min-height: 16px; border: none; border-radius: 0; background-color: #7ee081;
               background-image: repeating-linear-gradient(90deg, #7ee081 0px, #7ee081 10px, #5cbf5f 10px, #5cbf5f 12px); }
      button.start { font-family: "Press Start 2P", monospace; font-size: 10px; color: #1b1203; background-image: none;
               background-color: #ffd166; border: 4px solid #000; border-radius: 0; padding: 10px 14px;
               box-shadow: inset -4px -4px 0 #c99a2e, 4px 4px 0 #000; }
      button.start:hover { background-color: #ffe08a; }
      button.start:disabled { background-color: #555; color: #999; box-shadow: 4px 4px 0 #000; }
      textview.err, textview.err text { background-color: #000; color: #ff6b6b; font-family: monospace; font-size: 10px; }
      scrolledwindow.err { border: 2px solid #444; }
      button.copy { font-family: "Press Start 2P", monospace; font-size: 8px; color: #000; background-image: none;
               background-color: #ff8fb1; border: 2px solid #000; border-radius: 0; padding: 6px; }
    """


def run_gtk():
    """Window with the whole duds_ok photo on top; progress, notes and the start button in a retro panel below it.
    GTK 3 via PyGObject is installed on most desktops (Fedora Workstation, Ubuntu, GNOME, KDE with GTK apps)."""
    # the website's pixel font: put it in the user's font folder so GTK can use it (free, OFL)
    font = os.path.join(HERE, "PressStart2P-Regular.ttf")
    fdir = os.path.expanduser("~/.local/share/fonts/ragnaduds")
    if os.path.exists(font) and not os.path.exists(os.path.join(fdir, "PressStart2P-Regular.ttf")):
        try:
            os.makedirs(fdir, exist_ok=True); shutil.copy(font, fdir)
            subprocess.run(["fc-cache", "-f", fdir], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception: pass
    import gi
    gi.require_version("Gtk", "3.0"); gi.require_version("Gdk", "3.0")
    from gi.repository import Gdk, GdkPixbuf, GLib, Gtk
    css = Gtk.CssProvider()                  # same look as the website: wooden frame, gold, pixel font
    css.load_from_data(GTK_CSS)
    Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    win = Gtk.Window(title=f"{CFG['title']} - Setup"); win.set_resizable(False)
    try: win.set_icon_from_file(os.path.join(HERE, "ragnaduds.png"))
    except Exception: pass
    bg = os.path.join(HERE, "duds_ok_bg.png")
    if not os.path.exists(bg): bg = os.path.join(HERE, "duds_ok.png")
    column = Gtk.Box(orientation=Gtk.Orientation.VERTICAL); win.add(column)     # photo on top, panel below it
    photo_h = 565                                          # shrink the photo on short screens so the window fits
    try:
        area = Gdk.Display.get_default().get_monitor(0).get_workarea()
        photo_h = max(260, min(565, area.height - 470))
    except Exception: pass
    photo = Gtk.Image.new_from_pixbuf(GdkPixbuf.Pixbuf.new_from_file_at_scale(bg, -1, photo_h, True))
    column.pack_start(photo, False, False, 0)

    panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
    panel.get_style_context().add_class("panel")
    def label(text, cls, wrap=False):
        l = Gtk.Label(label=text, xalign=0); l.get_style_context().add_class(cls)
        if wrap: l.set_line_wrap(True); l.set_max_width_chars(46)
        panel.pack_start(l, False, False, 0); return l
    label("RAGNADUDS", "title"); label(CFG["edition"], "text")
    label("[RagnaDuds, Kafra intern]", "npc")
    quip = label(QUIPS[0], "quip", wrap=True)
    msg = label("Installing… thumbs up!", "text", wrap=True)
    bar = Gtk.ProgressBar(); panel.pack_start(bar, False, False, 4)
    notes = label("", "notes", wrap=True)
    err_view = Gtk.TextView(); err_view.set_editable(False); err_view.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
    err_view.get_style_context().add_class("err")
    err_box = Gtk.ScrolledWindow(); err_box.set_size_request(-1, 120); err_box.get_style_context().add_class("err")
    err_box.add(err_view); err_box.set_no_show_all(True); panel.pack_start(err_box, False, False, 4)
    copy_btn = Gtk.Button(label="COPY ERROR"); copy_btn.get_style_context().add_class("copy")
    copy_btn.set_no_show_all(True); panel.pack_start(copy_btn, False, False, 2)
    btn = Gtk.Button(label=START_LABEL); btn.get_style_context().add_class("start"); btn.set_sensitive(False)
    btn.set_halign(Gtk.Align.END); panel.pack_start(btn, False, False, 4)
    column.pack_start(panel, True, True, 0)

    state = {"p": 0, "m": msg.get_text(), "done": False, "err": None, "report": ""}
    def copy_error(*_):
        clip = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD); clip.set_text(state["report"], -1); clip.store()
        copy_btn.set_label("COPIED! PASTE IT TO DUDS")
    copy_btn.connect("clicked", copy_error); err_view.connect("button-release-event", copy_error)
    def report(p, m): state.update(p=p, m=m)
    def worker():
        try: install(report)
        except Exception as e: state["err"] = str(e); state["report"] = error_report(e)
        state["done"] = True
    def on_start(_):
        if not state["err"]: start_game()
        win.destroy()
    btn.connect("clicked", on_start)
    state["q"] = 0
    def next_quip():
        if state["done"]: return False
        state["q"] = (state["q"] + 1) % len(QUIPS); quip.set_text(QUIPS[state["q"]]); return True
    GLib.timeout_add(4500, next_quip)
    def poll():
        bar.set_fraction(min(1.0, state["p"] / 100)); msg.set_text(state["err"] or state["m"])
        if state["done"]:
            notes.set_text("\n".join(RESULT["notes"]))
            quip.set_text("Something broke. Not my fault. Probably yours." if state["err"] else "Done. Now go lose your social life.")
            if state["err"]:
                err_view.get_buffer().set_text(state["report"]); err_box.set_no_show_all(False); err_box.show_all(); copy_btn.show()
                photo.set_from_pixbuf(GdkPixbuf.Pixbuf.new_from_file_at_scale(bg, -1, max(200, photo_h - 170), True))
                btn.set_label("Close")
            btn.set_sensitive(True)
            return False
        return True
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    threading.Thread(target=worker, daemon=True).start()
    GLib.timeout_add(150, poll)
    Gtk.main()
    return 1 if state["err"] else 0


def run_zenity():
    z = subprocess.Popen(["zenity", "--progress", f"--title={CFG['title']} - Setup", "--text=Starting…",
                          "--percentage=0", "--width=420"], stdin=subprocess.PIPE, text=True)
    last = [-1]
    def report(p, m):
        if int(p) != last[0] or p >= 100:
            last[0] = int(p); z.stdin.write(f"{int(p)}\n# {m}\n"); z.stdin.flush()
    try:
        install(report); z.stdin.close(); z.wait()
        r = subprocess.run(["zenity", "--question", f"--title={CFG['title']}", "--width=420",
                            "--text=" + "\n".join(["Installed!"] + RESULT["notes"]),
                            f"--ok-label={START_LABEL}", "--cancel-label=Later"])
        if r.returncode == 0: start_game()
        return 0
    except Exception as e:
        z.kill(); text = error_report(e)
        head = "(Already copied: just paste it to Duds.)\n\n" if copy_text(text) else "(Select all, copy and send it to Duds.)\n\n"
        subprocess.run(["zenity", "--text-info", f"--title={CFG['title']} - Error", "--width=640", "--height=420"],
                       input=head + text, text=True)
        return 1


def run_text():
    print(f"RagnaDuds · {CFG['edition']} → {DEST}")
    last = [""]
    def report(p, m):
        line = f"\r[{'#' * int(p / 2.5):<40}] {p:5.1f}%  {m[:60]:<60}"
        if line != last[0]: sys.stdout.write(line); sys.stdout.flush(); last[0] = line
    try:
        install(report); print("\n" + "\n".join(RESULT["notes"]))
        if sys.stdin.isatty():
            input(f"\nPress Enter to {START_LABEL} (Ctrl+C to skip) ")
            start_game()
        return 0
    except Exception as e:
        text = error_report(e)
        print("\n\n" + text + ("\n\n(Copied to the clipboard: paste it to Duds.)" if copy_text(text) else
                               "\n\n(Copy everything above and send it to Duds.)"))
        return 1


# ---------------- launcher: auto-update, then PLAY (the menu / desktop entries run "linux_install.py --launch") ----------------
def update(report):
    """Download the files that changed on the website (patch.json: [path, size, sha256(, os)]). Returns a summary."""
    import urllib.request, urllib.parse
    patch = CFG.get("patch") or {}
    if not patch.get("url"):
        return "This install has no auto-update (install once more from the website to get it)."
    if game_running():
        return "The game is already open: updates are checked next time."
    def get(rel):
        req = urllib.request.Request(patch["url"] + "/".join(urllib.parse.quote(x) for x in rel.split("/")),
                                     headers={"Cookie": f"rd_auth={patch['token']}", "User-Agent": "RagnaDuds-Launcher"})
        return urllib.request.urlopen(req, timeout=20)
    report(2, "Checking for updates…")
    with get("patch.json") as r:
        if r.geturl().rstrip("/").endswith("login.html"):
            raise RuntimeError("The website refused the update (login changed?). Install once more from the website.")
        remote = json.load(r)
    state_path = os.path.join(DEST, PATCH_STATE)
    state = json.load(open(state_path)) if os.path.exists(state_path) else {}
    first = not state
    files = [e for e in remote["files"] if len(e) < 4 or e[3] == "linux"]
    todo = []
    for i, e in enumerate(files):
        rel, size, sha = e[0], e[1], e[2]
        local = os.path.join(DEST, rel)
        have = os.path.isfile(local) and os.path.getsize(local) == size
        if have and first:                     # first run: check the disk once (big archives: size is enough)
            if size < 64 << 20:
                h = hashlib.sha256()
                with open(local, "rb") as f:
                    while chunk := f.read(8 << 20): h.update(chunk)
                have = h.hexdigest() == sha
            if have: state[rel] = sha
        if i % 40 == 0: report(2 + 8 * i / max(1, len(files)), f"Checking files… {i} / {len(files)}")
        if not have or state.get(rel) != sha: todo.append((rel, size, sha))
    names = {e[0] for e in remote["files"]}
    removed = 0
    for rel in [k for k in state if k not in names]:      # files the new version doesn't have any more
        p = os.path.join(DEST, rel)
        if os.path.isfile(p): os.remove(p); removed += 1
        state.pop(rel)
    def save():
        json.dump(state, open(state_path + ".part", "w")); os.replace(state_path + ".part", state_path)
    if first or removed: save()
    if not todo:
        report(100, f"Up to date ({remote.get('version', '')}).")
        return ""
    total = sum(t[1] for t in todo) or 1; done = 0
    tmp = os.path.join(DEST, ".patch"); os.makedirs(tmp, exist_ok=True)
    for n, (rel, size, sha) in enumerate(todo, 1):
        part = os.path.join(tmp, os.path.basename(rel) + ".part"); h = hashlib.sha256()
        with get(rel) as r, open(part, "wb") as out:
            while chunk := r.read(1 << 20):
                out.write(chunk); h.update(chunk); done += len(chunk)
                report(10 + 90 * done / total, f"Updating {n} / {len(todo)}: {rel}   {done / 1048576:.1f} / {total / 1048576:.1f} MB")
        if h.hexdigest() != sha:
            os.remove(part); raise RuntimeError(f"Damaged download: {rel} (try again)")
        target = os.path.join(DEST, rel); os.makedirs(os.path.dirname(target), exist_ok=True)
        os.replace(part, target)
        if rel.endswith(".sh") or rel.endswith("linux_install.py"): os.chmod(target, 0o755)
        state[rel] = sha; save()
    shutil.rmtree(tmp, ignore_errors=True)
    report(100, f"Updated! ({remote.get('version', '')})")
    return f"Updated {len(todo)} file(s), {total / 1048576:.1f} MB" + (f", removed {removed} old file(s)" if removed else "")


def launch_gtk():
    import gi
    gi.require_version("Gtk", "3.0"); gi.require_version("Gdk", "3.0")
    from gi.repository import Gdk, GdkPixbuf, GLib, Gtk
    css = Gtk.CssProvider(); css.load_from_data(GTK_CSS + b"""
      button.play { font-family: "Press Start 2P", monospace; font-size: 12px; color: #10131f; background-image: none;
               background-color: #7ee081; border: 4px solid #000; border-radius: 0; padding: 12px 18px;
               box-shadow: inset -4px -4px 0 #5cbf5f, 4px 4px 0 #000; }
      button.play:hover { background-color: #9af09c; }
      button.play:disabled { background-color: #555; color: #999; box-shadow: 4px 4px 0 #000; }
    """)
    Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
    win = Gtk.Window(title=CFG["title"]); win.set_resizable(False)
    for icon in (os.path.join(HERE, "ragnaduds.png"), os.path.join(DEST, "ragnaduds.png")):
        if os.path.exists(icon):
            try: win.set_icon_from_file(icon); break
            except Exception: pass
    column = Gtk.Box(orientation=Gtk.Orientation.VERTICAL); win.add(column)
    bg = next((p for p in (os.path.join(HERE, "duds_ok_bg.png"), os.path.join(HERE, "duds_ok.png")) if os.path.exists(p)), None)
    if bg:
        h = 420
        try: h = max(220, min(420, Gdk.Display.get_default().get_monitor(0).get_workarea().height - 360))
        except Exception: pass
        column.pack_start(Gtk.Image.new_from_pixbuf(GdkPixbuf.Pixbuf.new_from_file_at_scale(bg, -1, h, True)), False, False, 0)
    panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6); panel.get_style_context().add_class("panel")
    def label(text, cls):
        l = Gtk.Label(label=text, xalign=0); l.get_style_context().add_class(cls); l.set_line_wrap(True); l.set_max_width_chars(46)
        panel.pack_start(l, False, False, 0); return l
    label("RAGNADUDS", "title"); label(CFG["edition"], "text")
    msg = label("Checking for updates…", "text")
    bar = Gtk.ProgressBar(); panel.pack_start(bar, False, False, 4)
    notes = label("", "notes")
    row = Gtk.Box(spacing=10)
    play = Gtk.Button(label="PLAY"); play.get_style_context().add_class("play"); play.set_sensitive(False)
    close = Gtk.Button(label="CLOSE"); close.get_style_context().add_class("start")
    row.pack_start(play, True, True, 0); row.pack_start(close, False, False, 0)
    panel.pack_start(row, False, False, 6); column.pack_start(panel, True, True, 0)
    state = {"p": 0, "m": "Checking for updates…", "done": False, "note": "", "err": None}
    def worker():
        try: state["note"] = update(lambda p, m: state.update(p=p, m=m))
        except Exception as e: state["err"] = str(e) or e.__class__.__name__
        state["done"] = True
    def poll():
        bar.set_fraction(min(1.0, state["p"] / 100)); msg.set_text(state["m"])
        if not state["done"]: return True
        if state["err"]:
            msg.set_text("Couldn't update right now. You can still play.")
            notes.set_text(state["err"]); play.set_label("PLAY ANYWAY")
        else:
            notes.set_text(state["note"]); bar.set_fraction(1.0)
        play.set_sensitive(True); play.grab_focus()
        return False
    play.connect("clicked", lambda _: (start_game(), win.destroy()))
    close.connect("clicked", lambda _: win.destroy())
    win.connect("destroy", Gtk.main_quit); win.show_all()
    threading.Thread(target=worker, daemon=True).start(); GLib.timeout_add(150, poll); Gtk.main()
    return 0


def launch():
    if (os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")) and "--text" not in ARGS:
        try: return launch_gtk()
        except (ImportError, ValueError): pass
    try:                                                  # no GTK: update with a terminal bar, then play
        note = update(lambda p, m: sys.stdout.write(f"\r[{'#' * int(p / 2.5):<40}] {m[:60]:<60}"))
        print("\n" + note)
    except Exception as e:
        print(f"\nCouldn't update right now ({e}). Starting the game anyway.")
    start_game(); return 0


# ---------------- upgrade: give an existing install the launcher (no game download) ----------------
def find_install():
    """The game folder of an existing install: --dest, its menu entry, or the usual places."""
    cands = []
    if "--dest" in ARGS: cands.append(DEST)
    entry = os.path.join(APPS, f"{LAUNCHER}.desktop")
    if os.path.exists(entry):
        for line in open(entry, errors="replace"):
            if line.startswith("Path="): cands.append(line[5:].strip())
    cands += [DEST, os.path.expanduser(f"~/ragnaduds/{CFG['folder']}"), os.path.expanduser(f"~/RagnaDuds/{CFG['folder']}")]
    for d in cands:
        if d and os.path.exists(os.path.join(d, CFG["exe"])): return d
    return None


def upgrade():
    global DEST, PREFIX
    d = find_install()
    if not d:
        print(f"No {CFG['title']} install found. Install it from the website, or run: upgrade.sh --dest /path/to/the/game/folder")
        return 1
    DEST, PREFIX = d, os.path.join(d, "wine")
    if game_running():
        print("The game is open: close it, then run the upgrade again."); return 1
    print(f"Upgrading {d} ...")
    for old in ("lang", "ragnaduds_lang.grf", os.path.join("System", "itemInfo_PT.lua")):   # Portuguese-era leftovers
        p = os.path.join(d, old)
        if os.path.isdir(p): shutil.rmtree(p, ignore_errors=True)
        elif os.path.exists(p): os.remove(p)
    make_shortcuts()
    print(f"Done! Open '{CFG['shortcut']}' from your desktop or app menu: the first start checks your files and downloads only what changed.")
    if "--no-launch" not in ARGS:
        subprocess.Popen([sys.executable, os.path.join(d, ".installer", "linux_install.py"), "--launch"], start_new_session=True,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return 0


if __name__ == "__main__":
    if "--uninstall" in ARGS: sys.exit(uninstall())
    if "--launch" in ARGS: sys.exit(launch())
    if "--upgrade" in ARGS: sys.exit(upgrade())
    gui = os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")
    if "--text" in ARGS or not gui: sys.exit(run_text())
    try:                                   # 1st choice: GTK window with the photo as background
        import gi
        gi.require_version("Gtk", "3.0")
        from gi.repository import Gtk  # noqa: F401
        sys.exit(run_gtk())
    except (ImportError, ValueError):
        pass
    try:                                   # 2nd: Tk (photo beside the progress)
        import tkinter  # noqa: F401
        sys.exit(run_tk())
    except ImportError:
        pass
    sys.exit(run_zenity() if shutil.which("zenity") else run_text())
