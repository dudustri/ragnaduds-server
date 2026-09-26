# Special maps (renewal only)

Three events rebuilt from bRO (Ragnarok Online Brasil) announcements. Each room is its **own copy** of a map (a shared rAthena instance), so the normal maps stay untouched and the rooms are only reachable through the event NPCs.

| Event | NPC | Where | Level | Ticket |
|---|---|---|---|---|
| **Mapas Especiais** | Nanaru | Morroc (152, 272) | 70+ | Ingresso dos Mapas Especiais |
| **Cheffenia** | Portal Fantasma | Comodo (208, 187) | 90+ | Passe para Cheffenia |
| **Turn In** (Evento de Caça) | Mateus Alem | Geffen (128, 117) | 70–174 | none |

- **Tickets:** in the **Cash Shop** for 1 cash point each. Everyone is topped up to 10 points at login, so they're free. A ticket isn't used up when you enter.
- **Always open:** rooms are created when the map server starts.

## Mapas Especiais (bRO, April 2020, monster amounts ×2)

8 rooms. Every monster **respawns instantly**, and there's **no EXP loss** on death.

| Room | Map | Monsters |
|---|---|---|
| 1 | ra_fild09 | 900 Zenorc, 900 Grove, 200 Orc Skeleton |
| 2 | moc_fild14 | 800 Deviruchi, 800 Injustice, 120 Evil Nymph, 400 Dark Priest, 400 Disguise |
| 3 | moc_fild15 | 20 Bloody Knight, 300 Banshee Master, 1,200 Nightmare Mummy, 500 Zombie Master |
| 4 | moc_fild05 | 1,300 Evil Druid, 300 Frus, 300 Shadow of Vanity, 300 Shadow of Gluttony |
| 5 | moc_fild04 | 10 Am Mut, 1,900 Abyssal Dark Priest, 300 Abandoned Teddy Bear |
| 6 | moc_fild06 | 100 Immortal Commander, 300 Immortal Fortress Legio, 1,400 Corrupt Orc Zombie, 200 Immortal Zombie Soldier, 200 Decorated Evil Tree |
| 7 | moc_fild08 | 2,500 Owl Marquis, 100 Arc Elder, 20 Warrior Laura |
| 8 | moc_fild10 | same as room 7 |

## Cheffenia (bRO, July 2023)

4 rooms on the Boss Nia maps.
- **Monsters:** the official Boss Nia spawns (169 bosses per room, respawn 30 min–2 h), plus one "exclusive" MVP per room. bRO's own versions don't exist in rAthena, so each room gets the closest original: Moonlight Flower, Turtle General, Dracula, Ktullanux.
- **Bosses there:** +100% HP and +50% damage.
- **Fatigue:** after **1,000 kills in a day**, your drops in Cheffenia are 0 until the next day.
- **Services:** a Kafra (storage) and a healer in every room.

## Turn In (bRO, September 2020)

3 hunting maps, 2 monster types each, 600 of each, with instant respawn:

| Area | Map | Monsters |
|---|---|---|
| Payon Cave [70–100] | pay_dun01 | Anopheles, Harpy |
| Geffen Cave [101–125] | gef_dun01 | Remover, Zombie Slaughter |
| Abyss Lake [126–174] | abyss_01 | Pom Spider, Shadow of Vanity |

**Quest:**
1. Pick a monster from your level range.
2. Kill **400** of it (they count anywhere).
3. Get **400× its base and job EXP**.

You can repeat it once every 24 h, with one hunt at a time, and cancel it anytime. The NPC also teleports you to the maps.

## Files

| File | What |
|---|---|
| `deploy/special_maps.txt` | the NPC script (all three events). Amounts: `.mult` in each event |
| `deploy/re_db_import/instance_db.yml` | the 15 rooms (instance Ids 900–914) |
| `deploy/re_db_import/item_db.yml`, `item_cash.yml` | the two tickets (990001, 990002) and the cash shop |
| `deploy/hosts/<host>/renewal/import/map_conf.txt` | loads the script + the Sograt fields the rooms copy |
| client `System/itemInfo_C.lua` | ticket names/descriptions in the renewal client |

All mounted into `re-map` by `deploy/compose.yml`. Changing the script or monster amounts only needs `./duds.sh up <host> re-map`, with no image rebuild. After a start, the map server log shows one `RagnaDuds: ... ready, N monsters` line per room.
