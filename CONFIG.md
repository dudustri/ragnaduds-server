# Configuration

## Where to change things
Never edit rAthena's `conf/` files. Put changes in the import files of each host and server:
`deploy/hosts/<local|vm>/<pre_renewal|renewal>/import/` (private, not in git).

| File | For | Apply |
|---|---|---|
| `battle_conf.txt` | rates, drops, gameplay | `@reloadbattleconf` in game |
| `map_conf.txt` | NPC scripts (`npc:` lines), extra maps | restart map |
| `char_conf.txt` | start items, zeny, PIN, delete delay | restart char |
| `login_conf.txt` | registration | restart login |
| `groups.yml` | GM / player permissions | restart map |
| `inter_conf.txt` | database, party share | restart all |

Our scripts (`deploy/*.txt`): `@reloadscript` in game, or restart map.
On the VM: `./duds.sh up vm`, then `./duds.sh restart vm prere-map re-map` (or `-char`, `-login`).
Format: `setting: value`, `//` = comment. Each setting is explained in the rAthena file it comes from, e.g. `grep -n -B5 "^base_exp_rate" conf/battle/exp.conf`.

## What's set now
| Setting | Local | VM |
|---|---|---|
| Rates | 1x | 10x EXP, 3x all drops |
| Starter kit (Knife, Cotton Shirt, Hat, potions, wings, 10k zeny) | – | ✔ |
| Warper, healer, job master NPCs | – | ✔ |
| Agente VIP buffer (Blessing + Agi, free) at bRO's 36 town spots | ✔ | ✔ |
| Free-for-all (no KS protection); parties share EXP + items, always | ✔ | ✔ |
| `@god`, `@nocooldown` for GMs ([GM-COMMANDS.md](GM-COMMANDS.md)) | ✔ | ✔ |
| Special maps: Mapas Especiais, Cheffenia, Turn In ([SPECIAL-MAPS.md](SPECIAL-MAPS.md)) | renewal | renewal |
| Random "Bem vindo do Supla:" line at login | ✔ | ✔ |
| No PIN; characters deleted after 10 min; no self-registration | ✔ | ✔ |
| Denmark time (daily resets at Danish midnight) | ✔ | ✔ |
| MVP kills logged + PvP kills counted (website Hall of Fame) | ✔ | ✔ |
| Autoloot only for your homunculus' kills (players use `@autoloot`) | ✔ | ✔ |
| Docker's network trusted (no anti-DDoS ban between our servers) | ✔ | ✔ |

Where each lives:
- rates, homunculus autoloot, idle trick: `battle_conf.txt`
- NPC lines and extra maps: `map_conf.txt`
- PIN, delete delay, starter kit: `char_conf.txt`
- MVP log: `log_conf.txt`
- trusted network: `packet_conf.txt`
- `@autoloot` for players: `groups.yml`
- timezone: `deploy/compose.yml`
- scripts: `deploy/*.txt`

Accounts: `hosts/vm/accounts.txt` → `./duds.sh accounts vm`, or `./duds.sh add-user vm <username> <M|F>`.

## Common changes (`battle_conf.txt`, `100` = 1x)
```
base_exp_rate: 1000     job_exp_rate: 1000      // 10x EXP
item_rate_common: 1000  item_rate_card: 1000    // 10x drops (renewal; also _heal _use _equip _boss _mvp)
death_penalty_base: 100                         // % EXP lost on death (100 = 1%)
item_auto_get: yes                              // all loot straight to inventory
show_mob_info: 6                                // monster HP % + level
mob_count_rate: 200                             // 2x monsters
boss_spawn_delay: 50                            // MVPs respawn 2x faster
pk_mode: 1                                      // PvP outside towns
```
`char_conf.txt`: `start_zeny: 100000`. More NPCs: `npc: npc/custom/<file>.txt` in `map_conf.txt` (see `ls npc/custom`).
