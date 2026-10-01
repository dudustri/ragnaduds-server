# RagnaDuds

Private Ragnarok Online servers for friends (Denmark + Brazil), built on this rAthena repo.
Everything of ours is in `duds_server/`; rAthena itself is untouched.

| | Pre-renewal | Renewal |
|---|---|---|
| Client | kRO 2021-11-03, English | kRO 2026-01-07, English |
| Port | 6900 | 6901 |
| Extras | GM commands, buffer, welcome lines, PvP/MVP counters | same + bRO special maps |

- Website + downloads: https://ragnaduds.duckdns.org (EN / PT / DA)
- Everything is run with `./duds.sh` (see `./duds.sh help`)

## Docs
| Doc | Read it for |
|---|---|
| [DEPLOY.md](DEPLOY.md) | putting it on the VM, and day-to-day tasks |
| [OPERATIONS.md](OPERATIONS.md) | diagrams, every command, what friends download |
| [CONFIG.md](CONFIG.md) | what's set and how to change settings |
| [SPECIAL-MAPS.md](SPECIAL-MAPS.md) | Mapas Especiais, Cheffenia, Turn In |
| [GM-COMMANDS.md](GM-COMMANDS.md) | GM commands, MVPs, builds, cards |
| [CASHSHOP-AND-CLIENT.md](CASHSHOP-AND-CLIENT.md) | Cash Shop, item fixes, GRF/Lua client files, how to add items |
| [SETUP.md](SETUP.md) | local servers and how the game clients were built |
| [build/web/README.md](build/web/README.md) | the website |

## Folders
```
duds.sh           command center
build/            images: pre_renewal, renewal, db, web (+ installer art)
deploy/           compose.yml, our scripts (*.txt), status.sh, backup.sh
deploy/hosts/     local/ and vm/: passwords, accounts, game configs   (private, not in git)
client/           client tools, installers, homunculus AI, package_client.py
vm_provisioning/  cloud-init for a new VM
```
