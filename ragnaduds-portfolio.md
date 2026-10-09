---
title: "RagnaDuds: running a private Ragnarok Online server for friends across two continents"
description: "rAthena on an ARM cloud VM, multi-arch Docker images, a custom client toolchain, installers for Windows and Linux, and a retro website with live server stats."
tags: [docker, devops, reverse-engineering, game-servers, python, bash, caddy, lua]
---

# RagnaDuds: a private Ragnarok Online server, end to end

Ragnarok Online was *the* game of my childhood. My friends are now split between **Denmark and Brazil**, so I built us our own server: two game servers (the classic *pre-renewal* era and the modern *renewal* era), a website, installers for Windows and Linux, and a small command-line tool to run it all.

It's a friends-only, non-commercial hobby project. The interesting part for me was everything *around* the game: infrastructure, packaging, and a lot of reverse-engineering of an old game client.

> **TL;DR** · [rAthena](https://github.com/rathena/rathena) (open-source C++ emulator) in multi-arch Docker images on an **ARM** Oracle Cloud VM · one `compose.yml` for 12 services · a Bash "command center" for build, release, deploy, accounts and backups · a patched and translated game client packaged with custom installers · a retro website with login, live status and a Hall of Fame fed straight from the game databases.

---

## Architecture

```
 friends (DK + BR)
      │  game ports (login/char/map ×2) · HTTPS · web-server ports
      ▼
 Oracle Cloud VM (ARM, Ubuntu) ── Security List + iptables
 └─ Docker Compose (12 services)
    ├─ pre-renewal: login · char · map · web · MariaDB
    ├─ renewal:     login · char · map · web · MariaDB
    ├─ web:    Caddy (auto-HTTPS, cookie login, client downloads)
    └─ status: sidecar polling ports + DBs every 15 s → status.json
```

- **Images are built once, on my PC**, for `amd64` and `arm64` with `docker buildx` + QEMU, and pushed to a private GitHub Container Registry. The VM never sees source code: it only pulls images.
- **Configs never go into images or git.** Each host (local / VM) has its own folder with `.env` secrets, game configs and accounts, mounted at runtime. Changing a rate or a script needs no rebuild.
- **The databases have no public port.** Only the game containers and the status sidecar can reach them, on internal Docker networks.

## The command center: `duds.sh`

One Bash script wraps everything, with green step headers and a progress bar:

| Command | What it does |
|---|---|
| `release [image…]` | multi-arch build and push, tagged `:latest` + `:<git sha>` (rollback = change the tag) |
| `up vm` | rsync configs, pull images, recreate only what changed; warns first if players are online |
| `start` / `stop pre\|re` | run only the server we're playing |
| `accounts` / `add-user` | game accounts from a local file, applied over SSH as idempotent SQL |
| `package` / `files` | build client zips, resumable upload with rsync |
| `backup` / `autobackup` | DB dumps to my PC, plus a 6-hourly cron job on the VM keeping 7 days |

## Reverse-engineering the game client

The server is the easy part. The **client** is a 2000s-era 32-bit Windows program, running on Linux via Wine for me and natively for friends on Windows.

- **Version matching.** The client exe's build date must match the server's packet version exactly. I picked a 2021 Korean exe for the classic server and a 2026 one for renewal, and compiled each server for its date.
- **Binary patching.** I patched both exes with the open-source **WARP** patcher: prefer local files over the game archives, drop the anti-cheat, change the server address. The patch sessions are version-controlled.
- **Game archives.** I wrote a small Python reader for the GRF archive format (versions 0x200 and 0x300) to inspect what the client actually loads.
- **Translation.** I built an English client from a community translation project, then fixed crashes where the translation referenced items newer than the 2021 data (Lua `table index is nil` popups).
- **The "Korean items" bug.** The 2026 exe only ever loads one compiled Lua file with Korean names; the English translation sat unused in the folder. The fix: that file became a tiny loader that runs the original bytecode, overlays the English table, then adds our custom items. I tested it in a **32-bit** Lua container, because the bytecode is 32-bit: 27,000+ items load in 0.5 s.
- **A packet mismatch in the cash shop.** The first item showed the right price and the second showed `544194803`. The exe had been patched to expect item-preview data in each shop entry; the server didn't send it, so every entry after the first was read out of alignment. The fix was one compile flag, set in the Dockerfile, so rAthena's source stays untouched.

## Recreating Brazilian-server events

Brazil's official server (bRO) shut down in 2026, and my Brazilian friends missed its events. Using the **Wayback Machine**, I rebuilt three of them from archived announcements, matching Portuguese monster names to IDs via community databases:
- **Mapas Especiais:** 8 rooms with instant respawn and no EXP loss.
- **Cheffenia:** an MVP arena with +100% boss HP, bosses trickling back one every 2 minutes.
- **Turn In:** a hunting quest.

The special maps are **shared instances**: private copies of existing maps, reachable only through event NPCs, so the normal maps stay untouched and no client changes are needed. A **buff NPC** stands at the same 36 town coordinates bRO used.

## The website

A single static page, no framework, deliberately retro (pixel font, CRT scanlines):
- **Custom login page.** The browser hashes ID + password into a token cookie, and Caddy only serves the site when the cookie matches. The password is never stored on the server.
- **Live server status** and a **Hall of Fame**:
  - a status sidecar checks the game ports and runs one read-only query per game database every 15 s
  - the page shows online/offline and players online, plus the top 10 characters with MVP kills and PvP kills (PvP kills come from a small server script I added)
- **Mini game.** My face on a knight sprite fighting an orc and Porings, with ragdoll physics via **matter.js**.
- **Collage.** My photo with game-art stickers on physics springs. Backgrounds removed with **rembg**, layout built with **Pillow**, and a potion and a halo drawn into the photo.
- **Three languages** (EN / PT / DA), picked from the browser and remembered.

## Installers

Each download ships a Windows and a Linux installer that unpack the game, **check every file against a manifest** (sizes plus the exe's SHA-256), confirm the client points at our server, test that the server answers, and create shortcuts.
- **Windows:** PowerShell WinForms, restyled to match the site. It must stay **ASCII-only**, because Windows PowerShell 5.1 reads scripts in the ANSI code page.
- **Linux:** Python with a GTK window (falling back to Tk, zenity, then plain terminal). Each install gets its own Wine prefix, and the installer knows that Debian/Ubuntu need 32-bit Wine.
- **Homunculus AI.** The zips include a self-hunting pet AI (the GPL-licensed Mir AI Mod), so friends don't need the external tools we used as kids.

## Bugs worth telling

- **The server DDoS-banned itself.** Before accounts existed, the char server kept dropping the map server, which reconnected many times per second. rAthena's anti-flood guard banned our own container. Fix: trust Docker's internal network.
- **A 5 GB installer crash.** PowerShell picked the *integer* overload of `[Math]::Max(1, $total)`, and 5,140,330,802 bytes doesn't fit in an `int`. I reproduced the error message exactly in a PowerShell container, then fixed it with doubles.
- **`#` commands did nothing.** rAthena's commands on other players start with `#`, but the 2026 client never sends chat lines starting with `#`. Fix: change the command symbol to `!`.
- **The "error loading data account settings" message.** Newer clients store per-account settings on a separate web service. The translation pointed it at `127.0.0.1`. I added rAthena's web server as two more containers and pointed the clients at it.

## Security and hygiene

- **Secrets stay out of images and out of git:** per-host `.env` files, and accounts sent as SQL over SSH.
- **Minimal open ports:** only the game, web and HTTPS ports. No database port is exposed, and SSH is key-only.
- **Private image registry;** the VM pulls with a read-only token.
- **Personal photos are git-ignored,** since the repo is public.

## Stack

`C++ (rAthena)` · `Docker / buildx / QEMU` · `Docker Compose` · `Oracle Cloud (ARM)` · `MariaDB` · `Caddy` · `Bash` · `Python (Pillow, rembg)` · `Lua 5.1` · `PowerShell / WinForms` · `GTK` · `Wine` · `JavaScript + matter.js` · `Mermaid` for the docs

## What I learned

- **Legacy software is an archaeology project:** version-matching, byte patterns, and reading old archives are half the job.
- **Separating images from config** makes a tiny deployment feel professional: releases, rollbacks and config changes are all boring, one-command operations.
- **Test on the real target:** a 32-bit Lua runtime, Windows PowerShell 5.1, a clean Debian container. Most bugs only show up there.
- **The best feature was the Hall of Fame,** because my friends now compete over it.

<!-- Optional, if you want to be transparent about tooling:
Built with an AI pair programmer (Claude Code) for research, scripting and debugging. I made the design decisions, ran every deploy, and tested everything in game with my friends. -->

*Ragnarok Online is a trademark of Gravity Co., Ltd. This is a non-commercial, friends-only fan project, not affiliated with Gravity. No game files are distributed publicly.*
