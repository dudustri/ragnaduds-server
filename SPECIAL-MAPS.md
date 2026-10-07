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

## Homunculus Room (alchemists)
NPC **Homunculus Trainer**, Prontera (190,177). Alchemist line only (Alchemist, Creator, Genetic, Biolo, babies).
Each player gets a private copy of the round arena `1@dime` (instance "Homunculus Room", Id 915; closes 15 minutes
after you leave). You start in the middle; 30 monsters of the chosen set stand still within 12 cells of you (our
homunculus AI chases up to 14 cells from its owner), and come back within 3 seconds when killed. The Guide inside
changes the set or takes you back to Prontera.

| Set (homunculus level) | Monsters |
|---|---|
| 1-15 | Poring, Lunatic, Fabre, Pupa, Chonchon |
| 15-30 | Spore, Rocker, Thief Bug, Picky, Condor |
| 30-45 | Poison Spore, Smokie, Muka, Hornet, Wolf |
| 45-60 | Deniro, Piere, Andre, Vitata, Horn |
| 60-75 | Orc Zombie, Jakk, Horong, Dustiness, Hunter Fly |
| 75-90 | Baby Leopard, Wild Rose, Brilight, Banaspaty |
| 90-105 | Marionette, Novus, Anopheles, Roween |
| 105-120 | Explosion, Gig, Beholder |
| 120+ | Beholder, Imp, Creepy Demon |

Script: `deploy/homunculus_room.txt` (sets are in its OnInit). Homunculi everywhere (both servers): kept fed by
`deploy/gm_commands.txt` (never starve or run away) and not sent to rest when their owner dies
(`homunculus_auto_vapor: 0` in the hosts' battle_conf).

## Item Disposal (renewal)
NPC **Item Disposal**, Prontera (193,177), right of the Homunculus Trainer. Destroys items players can't drop or
sell: the Paradise starter shadow set, Mace of Madness and other bound items. Scripts can't read an item's trade
flags, so it lists every **unequipped** item (asks how many for stacks) and asks again before destroying. Each
destroyed item is written to the map server's script log (`logmes`). Script: end of `deploy/cash_points.txt`.

## Job Master and 4th classes (renewal)
NPC **Job Master**, Prontera (153,193): every job change, including **4th classes**. rAthena has no official
4th job quests, so this NPC is the way. Our copy (`deploy/jobmaster.txt`, loaded instead of rAthena's) lets
**any** 3rd class become 4th, not only transcendent ones, because the NPC lets players skip rebirth. Still
needed: base level 200, job level 70, no unused skill points, no cart/falcon/mount. Pre-renewal keeps the
stock Job Master (no 4th classes there).

### 4th job change quests (like the official ones)
Scripts: `deploy/fourth_quests.txt` (shared helpers + Cardinal, Biolo, Dragon Knight) and `fourth_quests_a/b/c/d.txt`.
Official steps, places and trials (iRO Wiki job change guides), our own dialogue. Every quest needs **base 200 /
job 70** and ends with the job change + Hourglass Necklace. Private per-character instances (no party needed):
`re_db_import/instance_db.yml` 916-933, mostly on the official 4th job maps the 2026 client has. Official quest
monsters (Golden/Bone Acidus, Letizia, the Imperial knights, Verkhasel, Doomk, Heinous Monster, Yeongwi, Seo...)
are defined with their client Ids in `re_db_import/mob_db.yml`. Spirit Handler uses rAthena's built-in quest.

| Class (from) | Start NPC | Where | Script |
|---|---|---|---|
| Dragon Knight (Rune Knight) | Oscar | gef_fild08 54,101 | fourth_quests.txt |
| Imperial Guard (Royal Guard) | King's Knight | prt_cas 181,10 | _a |
| Arch Mage (Warlock) | Fairy / Strange Plant | ba_maison 201,269 | _b |
| Elemental Master (Sorcerer) | Elma | gef_tower 108,166 | _b |
| Windhawk (Ranger) | Drunk Old Man | payon 100,177 (then Luluka Forest um_fild01 47,345) | _d |
| Troubadour / Trouvere (Minstrel / Wanderer) | Flyer Part-timer | lighthalzen 186,124 | _b |
| Cardinal (Arch Bishop) | Priest Jergus | prt_church 114,122 | fourth_quests.txt |
| Inquisitor (Sura) | Inn Employee | prt_in 253,133 (Prontera hotel) | _a |
| Meister (Mechanic) | Roday / Mist | yuno 112,208 | _a |
| Biolo (Genetic) | Aldina | verus04 157,165 | fourth_quests.txt |
| Shadow Cross (Guillotine Cross) | Rumin | job3_guil01 74,92 (Finn's Secret Tavern, veins) | _c |
| Abyss Chaser (Shadow Chaser) | Vicente | s_atelier 123,59 (Rachel) | _c |
| Sky Emperor (Star Emperor) | Sign | payon 215,202 | _d |
| Soul Ascetic (Soul Reaper) | Clerk | payon 195,119 | _d |
| Night Watch (Rebellion) | Anya | einbroch 312,323 | _c |
| Shinkiro / Shiranui (Kagerou / Oboro) | Seoyeon | amatsu 82,118 | _c |
| Hyper Novice (Expanded Super Novice) | Grape | aldebaran 110,69 | _a |
| Spirit Handler (Summoner) | rAthena's official quest | | npc/re/jobs/doram |

## Other NPCs (renewal, rAthena's ready-made scripts, enabled in hosts/<host>/renewal/import/map_conf.txt)
| NPC | Where | What |
|---|---|---|
| Reset Girl | prontera 150,193 | resets stats and/or skills (zeny) |
| Platinum Skill NPC | prontera 128,200 | quest skills of your class (the Job Master also gives them on job change) |
| Stylist | prontera 170,180 | hair style / hair colour / clothes colour. Our copy (`deploy/stylist.txt`) offers only the clothes colours the class has: `getclothmax()` / `pc_cloth_color_max` (src/map/pc.cpp) cap every class to the body palettes in the 2026 client (Novice 8, 1st/2nd 4, trans 2nd + Crusader/Monk/Sage/Rogue/Assassin/Bard/Dancer 3, 3rd/4th 7, Royal Guard on a gryphon 3); `max_cloth_color: 8` is only the overall ceiling |
| Private MVP Room | prontera 148,174 | rent a room (100k zeny, 60 min, party/guild/account) and summon MVPs (100k) or bosses (50k). MVPs killed there give **no** cash points (deploy/cash_points.txt) |
| Marriage (Vomars, Happy Marry, Sister Lisa) | prt_church (Prontera church) | weddings |
