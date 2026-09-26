#!/usr/bin/env python3
"""RagnaDuds installer for Linux (started by ./install.sh).

Unpacks game.zip into ~/.local/share/ragnaduds/<edition>/, prepares a Wine prefix (+ CJK fonts),
and creates a "RagnaDuds" launcher in the app menu and on the desktop.
Progress UI: a GTK window with the photo as background if available, else Tk (photo beside it), else zenity, else a terminal bar.
Options: --dest DIR   install somewhere else
         --no-fonts   skip the winetricks font download
         --text       force the terminal progress bar
"""
import hashlib, json, os, re, shutil, socket, subprocess, sys, threading, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CFG = json.load(open(os.path.join(HERE, "config.json")))
ARGS = sys.argv[1:]
DEST = os.path.expanduser(ARGS[ARGS.index("--dest") + 1]) if "--dest" in ARGS else \
    os.path.expanduser(f"~/.local/share/ragnaduds/{CFG['folder']}")
PREFIX = os.path.join(DEST, "wine")


# ---------------- the actual work (reports progress 0..100 + a message) ----------------
def install(report):
    if not shutil.which("wine"):
        raise RuntimeError("Wine is not installed.\n  Fedora: sudo dnf install wine winetricks\n"
                           "  Ubuntu/Debian (the game is 32-bit):\n    sudo dpkg --add-architecture i386 && sudo apt update && sudo apt install wine wine32:i386 winetricks\n  Arch: sudo pacman -S wine winetricks")
    zpath = os.path.join(ROOT, "game.zip")
    if not os.path.exists(zpath):
        raise RuntimeError("game.zip not found. Unzip the whole download first.")
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

    verify(report)

    env = dict(os.environ, WINEPREFIX=PREFIX, WINEDEBUG="-all")
    report(82, "Preparing Wine (first time takes a minute)…")
    subprocess.run(["wineboot", "-u"], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if "--no-fonts" not in ARGS and shutil.which("winetricks"):
        report(88, "Installing fonts (a few minutes, downloads once)…")
        subprocess.run(["winetricks", "-q", "cjkfonts"], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elif "--no-fonts" not in ARGS:
        RESULT["notes"].append("⚠ winetricks not found: fonts skipped, some text may show as boxes.\n"
                               f"  Install winetricks, then run: WINEPREFIX=\"{PREFIX}\" winetricks -q cjkfonts")

    report(97, "Creating the RagnaDuds shortcut…")
    shutil.copy(os.path.join(HERE, "ragnaduds.png"), os.path.join(DEST, "ragnaduds.png"))
    launcher = os.path.join(DEST, "ragnaduds.sh")
    with open(launcher, "w") as f:
        f.write("#!/bin/sh\n# Start RagnaDuds with its own Wine prefix\n"
                f'cd "{DEST}" || exit 1\n'
                f'export WINEPREFIX="{PREFIX}" WINEDEBUG="${{WINEDEBUG:--all}}"\n'
                f'exec wine {CFG["exe"]} {CFG["args"]}\n')
    os.chmod(launcher, 0o755)
    desktop = (f"[Desktop Entry]\nType=Application\nName={CFG['shortcut']}\nComment={CFG['title']}\n"
               f"Exec=\"{launcher}\"\nPath={DEST}\nIcon={os.path.join(DEST, 'ragnaduds.png')}\n"
               "Terminal=false\nCategories=Game;\n")
    apps = os.path.expanduser("~/.local/share/applications"); os.makedirs(apps, exist_ok=True)
    name = f"ragnaduds-{CFG['folder'].lower()}.desktop"
    for d in [apps, desktop_dir()]:
        if not d: continue
        p = os.path.join(d, name)
        with open(p, "w") as f: f.write(desktop)
        os.chmod(p, 0o755)
        subprocess.run(["gio", "set", p, "metadata::trusted", "true"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    if "GNOME" in os.environ.get("XDG_CURRENT_DESKTOP", "").upper():   # GNOME shows no desktop icons by default
        RESULT["notes"].append(f"✔ GNOME hides desktop icons: press the Super key and type RagnaDuds")
    report(100, f"Done! Start '{CFG['shortcut']}' from your desktop or app menu.")


RESULT = {"notes": []}          # sanity-check summary, shown at the end


def verify(report):
    """Sanity check after unpacking: every file present with the right size, the game exe is
    exactly the packaged one, the client points at our server, and the server answers."""
    man = json.load(open(os.path.join(HERE, "manifest.json")))
    files = man["files"]; bad = []
    for i, (rel, size) in enumerate(files.items()):
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
    btn = tk.Button(root, text=START_LABEL, state="disabled", bg=gold, font=("Sans", 11, "bold"),
                    command=lambda: (start_game(), root.destroy()))
    btn.grid(row=5, column=1, sticky="e", padx=(0, 16), pady=10)
    state = {"p": 0, "m": msg.get(), "done": False, "err": None}

    def report(p, m): state.update(p=p, m=m)
    def worker():
        try: install(report)
        except Exception as e: state["err"] = str(e)
        state["done"] = True
    def poll():
        bar["value"] = state["p"]; msg.set(state["err"] or state["m"])
        if state["done"]:
            notes.set("\n".join(RESULT["notes"]))
            if state["err"]: btn.configure(text="Close", state="normal", command=root.destroy)
            else: btn.configure(state="normal")
            return
        root.after(150, poll)
    threading.Thread(target=worker, daemon=True).start(); poll(); root.mainloop()
    return 1 if state["err"] else 0


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
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gdk, GdkPixbuf, GLib, Gtk
    css = Gtk.CssProvider()                  # same look as the website: wooden frame, gold, pixel font
    css.load_from_data(b"""
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
    """)
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
    column.pack_start(Gtk.Image.new_from_pixbuf(GdkPixbuf.Pixbuf.new_from_file_at_scale(bg, -1, photo_h, True)), False, False, 0)

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
    btn = Gtk.Button(label=START_LABEL); btn.get_style_context().add_class("start"); btn.set_sensitive(False)
    btn.set_halign(Gtk.Align.END); panel.pack_start(btn, False, False, 4)
    column.pack_start(panel, True, True, 0)

    state = {"p": 0, "m": msg.get_text(), "done": False, "err": None}
    def report(p, m): state.update(p=p, m=m)
    def worker():
        try: install(report)
        except Exception as e: state["err"] = str(e)
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
            if state["err"]: btn.set_label("Close")
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
        z.kill(); subprocess.run(["zenity", "--error", f"--text={e}"]); return 1


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
    except Exception as e: print(f"\n\nError: {e}"); return 1


if __name__ == "__main__":
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
