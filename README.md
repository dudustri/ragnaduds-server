<h1 align="center"><img src="docs/img/ragnaduds-banner.png" alt="RagnaDuds" width="536"></h1>

A private Ragnarok Online server for a group of friends in Denmark and Brazil.
It runs on [rAthena](https://github.com/rathena/rathena), the open-source server, with two worlds:
**Renewal** and **Pre-Renewal** (the classic game). Not affiliated with Gravity.

## How it works

```mermaid
flowchart TB
    FRIENDS(["Friends in Denmark and Brazil"])

    subgraph VM["Cloud VM · Docker"]
        direction TB
        WEB["Website + account portal<br/>login · downloads · status"]
        subgraph WORLDS[" "]
            direction LR
            RE["Renewal world<br/>login → characters → maps"]
            PRE["Pre-Renewal world<br/>login → characters → maps"]
        end
        DB[("Databases<br/>one per world, never public")]
        OPS["Status checker<br/>backups every 6 hours"]
        WEB --> DB
        RE --> DB
        PRE --> DB
        OPS -.-> DB
    end

    subgraph PC["Your PC"]
        direction LR
        CODE["This repo<br/>official rAthena + our patches<br/>+ our NPCs, maps, settings"] --> CMD["duds.sh"]
    end
    REG[("GitHub registry<br/>server images")]

    FRIENDS -- "play" --> RE & PRE
    FRIENDS -- "browse" --> WEB
    CMD -- "release" --> REG
    REG -- "up: pull" --> VM
    CMD -- "up: settings + scripts" --> VM
```

- **Images** are the programs; **settings and scripts** stay outside them, so most changes need no rebuild.
- **Databases** are never open to the internet: only the servers, the portal and the status checker reach them.
- **Passwords and accounts** live in `deploy/hosts/` and never go into git.

## Quick start
```bash
git clone --recurse-submodules https://github.com/dudustri/ragnaduds-server.git
./duds.sh help                 # every command
./duds.sh start local re       # a server on your PC
./duds.sh release              # build the images
./duds.sh up vm                # put everything on the VM
```

Update rAthena: `git -C rathena fetch && git -C rathena checkout <commit>`, then `./duds.sh release`.
The build stops if one of our patches no longer fits. Check `rathena/sql-files/upgrades/` for database changes first.

## Docs
| Doc | For |
|---|---|
| [DEPLOY](docs/DEPLOY.md) | putting it on the VM, day-to-day tasks |
| [OPERATIONS](docs/OPERATIONS.md) | diagrams and every `duds.sh` command |
| [CONFIG](docs/CONFIG.md) | rates and settings, and how to change them |
| [SPECIAL-MAPS](docs/SPECIAL-MAPS.md) | Mapas Especiais, Cheffenia, casino, 4th job quests |
| [BROWSER](docs/BROWSER.md) | playing in the browser (/play, /play-renewal), and the local GRF viewers |
| [grf](grf/README.md) | making your own maps, sprites and effects |
| [CASHSHOP](docs/CASHSHOP.md) | the Cash Shop and cash points |
| [GM-COMMANDS](docs/GM-COMMANDS.md) | GM commands, MVPs, jobs, cards |
| [PORTAL](docs/PORTAL.md) | account requests, website login, password reset |
| [WEBSITE](docs/WEBSITE.md) | the website |
| [SETUP](docs/SETUP.md) | running the servers on your PC |
| [builds](docs/builds/README.md) | class builds used for the shop |

## Folders
```
duds.sh       the command center
rathena/      official rAthena (git submodule)
robrowser/    roBrowserLegacy, the browser client (git submodule)
patches/      our engine changes, applied when the images are built
build/        server images, website, account portal
deploy/       what runs on the VM: compose file, our scripts, settings (hosts/ is private)
cashshop/     Cash Shop builder
casino/       casino art and sounds
client/       tools for the friends' download
docs/         documentation
grf/          your GRF work (maps, sprites, effects), see grf/README.md
vm_provisioning/  setup for a new VM
```
