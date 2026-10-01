# In-game GM commands

Type them in the chat box. Your account must be a GM (**group 99 = Admin**, e.g. `dudsgm`). Make one (or promote someone):
```bash
./duds.sh add-user vm <username> <M|F> 99      # then relog
```
- `@command` acts on **you**. `!command <character> <values>` does the same to **another player**: name first, then values (e.g. `!lvup Padrinho 10`, `!job Padrinho 4008`). On our servers it's `!` instead of rAthena's usual `#`, because the 2026 client swallows lines starting with `#`.
- `@help <command>` shows the syntax in game. `@commands` lists everything you're allowed to use.
- Full list (~300 commands): `doc/atcommands.txt` and `conf/atcommands.yml`.
- `[ ]` = optional, `< >` = required. Names with spaces: use the ID or quotes.

---

## Spawn / kill monsters
| Command | What it does |
|---|---|
| `@monster <name/ID> [amount]` | spawn monsters (alias `@spawn`). e.g. `@monster poring 10`, `@monster 1002 5` |
| `@monsterbig <name/ID>` / `@monstersmall <name/ID>` | giant / tiny version |
| `@summon <name/ID> [minutes]` | spawn a monster that fights **for** you |
| `@clone <player>` | spawn a clone of a player that helps you |
| `@killmonster2` | kill all monsters on your map (no drops) |
| `@killmonster <map>` | kill all monsters on a map (they drop items) |
| `@cleanmap` | delete all items lying on the floor |
| `@mobinfo <name/ID>` | monster stats, exp, drops |
| `@whodrops <item>` | which monsters drop an item |
| `@showmobs <name/ID>` | mark where a monster is on the minimap |

## Levels, stats, skills
| Command | What it does |
|---|---|
| `@blvl <n>` | +n base levels (`@baselevelup`). `@blvl 98` → level 99. Negative lowers |
| `@jlvl <n>` | +n job levels (`@joblevelup`) |
| `@job <name/ID>` | change job, e.g. `@job 4008` (Lord Knight), `@job Knight` |
| `@allskill` | learn every skill of your job |
| `@allstats [value]` | add to all stats (max if no value) |
| `@str <n>` (also `@agi @vit @int @dex @luk`) | raise one stat |
| `@stpoint <n>` / `@skpoint <n>` | give stat / skill points |
| `@reset` / `@streset` / `@skreset` | reset stats+skills / only stats / only skills |

## Survive ("god mode")
| Command | What it does |
|---|---|
| `@god` | **custom** (our `gm_commands.txt`): toggle Invincible status, every hit does 1 damage. `!god <player>` for someone else |
| `@nocooldown` | **custom**: toggle zero cooldown + zero after-cast delay for the skills you know. Run it again after learning new skills (`@allskill`). Removed on logout. Turning it off also clears other timed script buffs (food etc.) |
| `@resetcooltime` | built-in: reset all your cooldowns once |
| `@monsterignore` | monsters and players can't attack you (toggle; alias `@battleignore`) |
| `@heal [hp sp]` | full heal (no numbers = full) |
| `@alive` | revive yourself |
| `@raisemap` | revive everyone on the map |
| `@hide` | invisible (toggle) |

## Appear / disappear / look
| Command | What it does |
|---|---|
| `@hide` | GM invisibility on/off |
| `@disguise <monster>` / `@undisguise` | look like a monster to others |
| `@size <0-2>` | 0 normal, 1 small, 2 big |
| `@hairstyle <n>` / `@dye <n>` / `@model <hair> <color> <clothes>` | change looks |
| `@effect <id>` | play a visual effect on yourself |

## Move around
| Command | What it does |
|---|---|
| `@go <city>` | warp to a town: `@go prontera`, `@go geffen`, `@go 0` (`@go` alone lists numbers) |
| `@warp <map> [x y]` | warp anywhere (`@mapmove`), e.g. `@warp prt_fild08 150 150` |
| `@jump [x y]` | random spot on the map (like a Fly Wing) |
| `@jumpto <player>` | go to a player (`@goto`) |
| `@recall <player>` / `@recallall` | bring a player / everyone to you |
| `@speed <1-1000>` | walk speed, 1 = fastest, 150 = normal |
| `@save` / `@load` | set / go to your respawn point |
| `@where <player>` / `@who` | find a player / who's online |

## Items and money
| Command | What it does |
|---|---|
| `@item <name/ID> <amount>` | get items, e.g. `@item 501 100` (Red Potion), `@item Jellopy 10` |
| `@item2 <id> <qty> <identified> <refine> <broken> <c1> <c2> <c3> <c4>` | item with refine + cards, e.g. `@item2 1201 1 1 10 0 4001 0 0 0` |
| `@zeny <amount>` | get zeny (negative removes) |
| `@cash <amount>` · `!cash "<name>" <amount>` | Cash Shop points for you / for a player (renewal; negative removes) |
| `@points` | (everyone) your Cash Shop points and how to earn more: +10 daily login, +5/hour played, +20/MVP, +2/PvP kill |
| `@refine <position> <+/- n>` | refine equipped gear (`@refine` alone lists positions) |
| `@refine 0 10` | **refine everything you're wearing to the max** (+10 pre-renewal; use `@refine 0 20` on renewal) |
| `@identify` / `@repairall` | identify / repair everything |
| `@storage` / `@gstorage` | open storage / guild storage anywhere |
| `@autoloot [on/off/%]` | loot goes to inventory |
| `@iteminfo <name/ID>` | item details |
| `@itemreset` | **delete** your whole inventory |

## Server / players
| Command | What it does |
|---|---|
| `@broadcast <msg>` / `@kami <msg>` | yellow message to everyone (with / without your name) |
| `@kick <player>` / `@kickall` | disconnect player / everyone |
| `@ban <time> <player>` / `@unban <player>` | ban, e.g. `@ban +1d Padrinho` |
| `@jail <player>` / `@unjail <player>` | send to / release from jail |
| `@mute <player>` | stop someone from talking |
| `@day` / `@night` | change lighting for everyone |
| `@rates` | show current exp/drop rates |
| `@reloadbattleconf` | apply `battle_conf.txt` changes (rates etc.) without restart |
| `@reloadscript` | reload all NPC scripts |
| `@reloaditemdb` / `@reloadmobdb` | reload item / monster databases |
| `@showexp` | show exp gained per kill |

---

## Quick "test character" recipe
```
@job 4008
@blvl 98
@jlvl 49
@allskill
@allstats
@zeny 10000000
@item 501 100
@speed 50
@go prontera
```
(4008 = Lord Knight. Other IDs: `@help job` in game, or `src/common/mmo.hpp` (the `JOB_…` list).)

---

## MVP list (`@monster <ID>`)

Generated from `db/pre-re/mob_db.yml` and `db/re/mob_db.yml` (monsters with MVP rewards). Stats differ per server; the pre-renewal table shows pre-renewal stats.
`@monster 1039` spawns Baphomet. `@killmonster2` removes everything. `@mobinfo <ID>` shows drops.
Sorted by level. A name listed twice (e.g. Baphomet 1039 and 1399) = the regular MVP and a special/event/quest version with other stats: use the lower, classic ID for the normal one.

### Both servers (53 MVPs, pre-renewal stats)

| ID | Name | Lv | HP |
|---|---|---|---|
| 1086 | Golden Thief Bug | 64 | 126,000 |
| 1115 | Eddga | 65 | 152,000 |
| 1150 | Moonlight Flower | 67 | 120,000 |
| 1399 | Baphomet | 68 | 1,264,000 |
| 1159 | Phreeoni | 69 | 188,000 |
| 1112 | Drake | 70 | 326,666 |
| 1583 | Tao Gunka | 70 | 193,000 |
| 1492 | Samurai Specter | 71 | 218,652 |
| 1046 | Doppelganger | 72 | 249,000 |
| 1252 | Hatii | 73 | 197,000 |
| 1418 | Evil Snake Lord | 73 | 254,993 |
| 1059 | Mistress | 74 | 212,000 |
| 1190 | Orc Lord | 74 | 783,000 |
| 1087 | Orc Hero | 77 | 585,700 |
| 1251 | Stormy Knight | 77 | 240,000 |
| 1038 | Osiris | 78 | 415,400 |
| 1658 | Egnigem Cenia | 79 | 214,200 |
| 1272 | Dark Lord | 80 | 720,000 |
| 1871 | Fallen Bishop Hibram | 80 | 3,333,333 |
| 1039 | Baphomet | 81 | 668,000 |
| 1147 | Maya | 81 | 169,000 |
| 1785 | Atroce | 82 | 1,008,420 |
| 1389 | Dracula | 85 | 320,096 |
| 1630 | White Lady | 85 | 253,221 |
| 1885 | Gopinich | 85 | 299,321 |
| 1980 | Kublin | 85 | 1,176,000 |
| 1623 | RSX-0806 | 86 | 560,733 |
| 1511 | Amon Ra | 88 | 1,214,138 |
| 1688 | Lady Tanee | 89 | 493,000 |
| 1768 | Gloom Under Night | 89 | 2,298,000 |
| 1719 | Detardeurus | 90 | 960,000 |
| 1734 | Kiel D-01 | 90 | 1,523,000 |
| 1157 | Pharaoh | 93 | 445,997 |
| 2068 | Boitata | 93 | 1,283,990 |
| 1373 | Lord of the Dead | 94 | 603,383 |
| 1312 | Turtle General | 97 | 320,700 |
| 1685 | Vesper | 97 | 640,700 |
| 1779 | Ktullanux | 98 | 4,417,000 |
| 1874 | Beelzebub | 98 | 6,666,666 |
| 1502 | Bring it on! | 99 | 95,000,000 |
| 1646 | Lord Knight Seyren | 99 | 1,647,590 |
| 1647 | Assassin Cross Eremes | 99 | 1,411,230 |
| 1648 | Whitesmith Howard | 99 | 1,460,000 |
| 1649 | High Priest Margaretha | 99 | 1,092,910 |
| 1650 | Sniper Cecil | 99 | 1,349,000 |
| 1651 | High Wizard Kathryne | 99 | 1,069,920 |
| 1708 | Memory of Thanatos | 99 | 445,660 |
| 1751 | Valkyrie Randgris | 99 | 3,567,200 |
| 1766 | Angeling | 99 | 128,430 |
| 1767 | Deviling | 99 | 128,430 |
| 1832 | Ifrit | 99 | 7,700,000 |
| 1917 | Wounded Morocc | 99 | 8,388,607 |
| 2022 | Nidhoggr's Shadow | 117 | 3,450,000 |

### Renewal server only (140 more)

Many are episode or instance (memorial dungeon) versions; they may behave oddly outside their map.

| ID | Name | Lv | HP |
|---|---|---|---|
| 2075 | Ragunta | 1 | 300 |
| 2066 | Anopheles | 5 | 50 |
| 1816 | Gourd | 12 | 1,000 |
| 3505 | Big Eggring | 25 | 142,480 |
| 3810 | King Poring | 35 | 140,000 |
| 2094 | Orc Hero | 50 | 362,000 |
| 2095 | Eddga | 65 | 947,500 |
| 2306 | Golden Thief Bug | 65 | 100,000,000 |
| 2096 | Osiris | 68 | 475,840 |
| 2097 | Dracula | 75 | 350,000 |
| 2098 | Doppelganger | 77 | 380,000 |
| 2099 | Mistress | 78 | 378,000 |
| 2100 | Baphomet | 81 | 668,000 |
| 1957 | Entweihen Crothen | 90 | 2,400,500 |
| 2212 | Stormy Knight | 92 | 100,000,000 |
| 2101 | Lord of the Dead | 94 | 603,883 |
| 2156 | Leak | 94 | 1,266,000 |
| 2194 | Giant Octopus | 95 | 500,000 |
| 2052 | Dark Lord | 96 | 100,000,000 |
| 2102 | Dark Lord | 96 | 1,190,900 |
| 1518 | White Lady | 97 | 720,500 |
| 2103 | Ktullanux | 98 | 2,626,000 |
| 1813 | Hydrolancer | 99 | 1,880,000 |
| 1817 | Detardeurus | 99 | 8,880,000 |
| 1876 | Lord of the Dead | 99 | 99,000,000 |
| 1956 | Naght Sieger | 99 | 5,000,000 |
| 2441 | The Last One | 99 | 265,203 |
| 2442 | King of the Alley | 99 | 268,800 |
| 2187 | Gloomy Coelacanth | 100 | 2,200,000 |
| 2188 | Weird Coelacanth | 100 | 2,200,000 |
| 2352 | RSX 0805 | 100 | 10,000,000 |
| 3658 | Lich Lord | 100 | 2,516,502 |
| 3000 | Morocc Necromancer | 101 | 80,000,000 |
| 3426 | Infinite Eddga | 101 | 1,850,000 |
| 3427 | Infinite Osiris | 103 | 2,850,000 |
| 2104 | Evil Snake Lord | 105 | 1,101,000 |
| 3428 | Infinite Phreeoni | 105 | 4,750,000 |
| 3429 | Infinite Orc Hero | 107 | 6,650,000 |
| 3430 | Infinite Tao Gunka | 109 | 8,550,000 |
| 2105 | Turtle General | 110 | 1,442,000 |
| 3628 | Heart Hunter Ebel | 110 | 2,800,000 |
| 3633 | Venomous Chimera | 110 | 2,800,000 |
| 2327 | Bangungot | 115 | 250 |
| 3450 | Bijou | 115 | 10,000,000 |
| 20346 | Miguel | 115 | 8,600,000 |
| 3758 | Angry Moonlight Flower | 118 | 4,287,803 |
| 20340 | EL1-A17T | 118 | 16,412,000 |
| 3621 | Pet Child | 120 | 3,500,000 |
| 2202 | Kraken | 124 | 5,602,800 |
| 2106 | Vesper | 128 | 3,802,000 |
| 3181 | Captain Ferlock | 130 | 3,000,000 |
| 2131 | Lost Dragon | 135 | 608,920 |
| 3796 | Awakened Ktullanux | 135 | 13,521,442 |
| 20620 | Red Pepper | 135 | 9,514,800 |
| 2107 | Fallen Bishop Hibram | 138 | 5,655,000 |
| 20659 | Pitaya Boss | 138 | 7,221,377 |
| 2108 | Gloom Under Night | 139 | 3,005,000 |
| 3757 | Dracula of Rage | 139 | 6,909,690 |
| 20642 | Sweety | 139 | 5,011,304 |
| 2087 | Scaraba Queen | 140 | 2,441,600 |
| 2165 | Gold Queen Scaraba | 140 | 6,441,600 |
| 3073 | Awakened Ferre | 140 | 19,471,800 |
| 2109 | Valkyrie Randgris | 141 | 3,205,000 |
| 2249 | Angry Student Pyuriel | 141 | 2,205,000 |
| 2341 | 2011 RWC Boss | 141 | 3,205,000 |
| 2253 | General Daehyun | 142 | 2,500,148 |
| 2255 | Dark Guardian Kades | 143 | 2,505,000 |
| 2362 | Amon Ra (Nightmare) | 145 | 2,515,784 |
| 3124 | Charleston 3 | 145 | 23,671,401 |
| 20667 | Silva Papilia | 145 | 7,375,012 |
| 2110 | Ifrit | 146 | 6,935,000 |
| 2251 | Gioia | 146 | 2,507,989 |
| 2475 | Corrupted Soul | 150 | 1,820,000 |
| 2476 | Amdarais | 150 | 4,290,000 |
| 2319 | Buwaya | 151 | 4,090,365 |
| 2942 | Evil Fanatics | 151 | 8,256,000 |
| 2483 | Nightmare Baphomet | 154 | 4,008,000 |
| 2189 | Mutant Coelacanth | 155 | 5,200,000 |
| 2190 | Violent Coelacanth | 155 | 5,200,000 |
| 2529 | Faceworm Queen | 155 | 50,000,000 |
| 2532 | Red Faceworm Queen | 155 | 50,000,000 |
| 2533 | Green Faceworm Queen | 155 | 50,000,000 |
| 2534 | Blue Faceworm Queen | 155 | 50,000,000 |
| 2535 | Yellow Faceworm Queen | 155 | 50,000,000 |
| 2322 | Bakonawa | 156 | 3,351,884 |
| 3741 | Spider Chariot | 158 | 9,799,123 |
| 3029 | Reaper Yanku | 159 | 50,000,000 |
| 2111 | Whitesmith Howard | 160 | 6,750,000 |
| 2112 | Lord Knight Seyren | 160 | 4,680,000 |
| 2113 | Assassin Cross Eremes | 160 | 4,230,000 |
| 2235 | Paladin Randel | 160 | 6,870,000 |
| 2236 | Creator Flamel | 160 | 4,230,000 |
| 2237 | Professor Celia | 160 | 3,847,804 |
| 2238 | Champion Chen | 160 | 4,249,350 |
| 2239 | Stalker Gertie | 160 | 4,057,279 |
| 2240 | Clown Alphoccio | 160 | 3,894,278 |
| 2241 | Gypsy Trentini | 160 | 3,894,278 |
| 2564 | Fenrir | 160 | 20,000,000 |
| 2996 | Celine Kimi | 160 | 66,666,666 |
| 3190 | Sarah Irene | 160 | 100,000,000 |
| 3473 | Stefan.J.E.Wolf | 160 | 20,000,000 |
| 3659 | Lich Lord | 160 | 23,485,539 |
| 3254 | T_W_O | 165 | 48,000,000 |
| 3804 | Ominous Turtle General | 165 | 11,628,549 |
| 20648 | Boss Meow | 168 | 19,298,694 |
| 20273 | Ancient Tao Gunka | 169 | 19,280,000 |
| 20277 | Ancient Wootan Defender | 169 | 20,154,000 |
| 3074 | Time Holder | 170 | 25,000,000 |
| 20381 | R48-85-Bestia | 174 | 4,885,000 |
| 3097 | Despair God Morroc | 175 | 120,000,000 |
| 21395 | Silent Maya | 175 | 24,512,365 |
| 20621 | Senior Red Pepper | 185 | 1,008,398,847 |
| 21316 | Schulang | 185 | 2,000,000,000 |
| 21317 | Twisted God Freyja | 185 | 2,000,000,000 |
| 3241 | Genetic Flamel | 186 | 14,400,000 |
| 3245 | Minstrel Alphoccio | 186 | 10,800,000 |
| 3246 | Wanderer Trentini | 186 | 10,800,000 |
| 3221 | Arch Bishop Margaretha | 187 | 14,400,000 |
| 3223 | Mechanic Howard | 187 | 18,000,000 |
| 3224 | Warlock Kathryne | 187 | 10,800,000 |
| 3240 | Royal Guard Randel | 188 | 18,000,000 |
| 3242 | Sorcerer Celia | 188 | 16,200,000 |
| 3243 | Sura Chen | 188 | 12,600,000 |
| 3244 | Shadow Chaser Gertie | 188 | 14,400,000 |
| 20419 | Rigid Muspellskoll | 188 | 48,530,254 |
| 3220 | Guillotine Cross Eremes | 189 | 12,600,000 |
| 3222 | Ranger Cecil | 189 | 12,600,000 |
| 3225 | Rune Knight Seyren | 189 | 14,400,000 |
| 20422 | Corrupted Dark Lord | 194 | 74,476,822 |
| 20421 | Corrupted Spider Queen | 195 | 74,623,473 |
| 20668 | Gran Papilia | 195 | 74,730,723 |
| 20601 | Jewel Ungoliant | 197 | 37,847,096 |
| 20811 | Deep Sea Kraken | 204 | 81,289,587 |
| 20843 | Deep Sea Witch | 205 | 78,368,745 |
| 21301 | Burning Fang | 212 | 98,158,095 |
| 20934 | R001-Bestia | 215 | 134,179,630 |
| 21360 | Schulang | 224 | 2,000,000,000 |
| 21361 | Twisted God Freyja | 224 | 2,000,000,000 |
| 20928 | The One | 245 | 275,042,400 |
| 20943 | Death Witch | 255 | 398,856,250 |

---

## Job classes (`@job <ID>`)

The best gear for each class is in **Best set per class** below.

Generated from the job list in `src/common/mmo.hpp`. `@job 4008` → Lord Knight. Then `@allskill` and `@jlvl` to fill skills.
- **Pre-renewal server:** only groups marked *both*. 3rd/4th jobs have no skills there.
- Gender-locked: Bard/Clown/Minstrel/Troubadour/Kagerou/Shinkiro = male; Dancer/Gypsy/Wanderer/Trouvere/Oboro/Shiranui = female.
- Summoner and Spirit Handler are the Doram race (cat people); switching a human to them may look odd.
- Other babies (3rd-job babies, baby ninja, etc.) exist too: `@help job` in game.

### Novice & 1st jobs (both servers)

| ID | Job |
|---|---|
| 0 | Novice |
| 1 | Swordman |
| 2 | Mage |
| 3 | Archer |
| 4 | Acolyte |
| 5 | Merchant |
| 6 | Thief |

### 2nd jobs (both servers)

| ID | Job |
|---|---|
| 7 | Knight |
| 14 | Crusader |
| 9 | Wizard |
| 16 | Sage |
| 11 | Hunter |
| 19 | Bard |
| 20 | Dancer |
| 8 | Priest |
| 15 | Monk |
| 10 | Blacksmith |
| 18 | Alchemist |
| 12 | Assassin |
| 17 | Rogue |

### Transcendent (rebirth) (both servers)

| ID | Job |
|---|---|
| 4001 | Novice High |
| 4002 | Swordman High |
| 4003 | Mage High |
| 4004 | Archer High |
| 4005 | Acolyte High |
| 4006 | Merchant High |
| 4007 | Thief High |
| 4008 | Lord Knight |
| 4015 | Paladin |
| 4010 | High Wizard |
| 4017 | Professor |
| 4012 | Sniper |
| 4020 | Clown |
| 4021 | Gypsy |
| 4009 | High Priest |
| 4016 | Champion |
| 4011 | Whitesmith |
| 4019 | Creator |
| 4013 | Assassin Cross |
| 4018 | Stalker |

### Expanded jobs (both servers)

| ID | Job |
|---|---|
| 23 | Super Novice |
| 4046 | Taekwon |
| 4047 | Star Gladiator |
| 4049 | Soul Linker |
| 24 | Gunslinger |
| 25 | Ninja |

### Baby jobs (both servers)

| ID | Job |
|---|---|
| 4023 | Baby |
| 4024 | Baby Swordman |
| 4025 | Baby Mage |
| 4026 | Baby Archer |
| 4027 | Baby Acolyte |
| 4028 | Baby Merchant |
| 4029 | Babyhief |
| 4030 | Baby Knight |
| 4037 | Baby Crusader |
| 4032 | Baby Wizard |
| 4039 | Baby Sage |
| 4034 | Baby Hunter |
| 4042 | Baby Bard |
| 4043 | Baby Dancer |
| 4031 | Baby Priest |
| 4038 | Baby Monk |
| 4033 | Baby Blacksmith |
| 4041 | Baby Alchemist |
| 4035 | Baby Assassin |
| 4040 | Baby Rogue |
| 4045 | Super Baby |

### 3rd jobs (renewal only)

| ID | Job |
|---|---|
| 4054 | Rune Knight |
| 4066 | Royal Guard |
| 4055 | Warlock |
| 4067 | Sorcerer |
| 4056 | Ranger |
| 4068 | Minstrel |
| 4069 | Wanderer |
| 4057 | Arch Bishop |
| 4070 | Sura |
| 4058 | Mechanic |
| 4071 | Genetic |
| 4059 | Guillotine Cross |
| 4072 | Shadow Chaser |

### 3rd jobs from transcendent (renewal only)

| ID | Job |
|---|---|
| 4060 | Rune Knight (trans) |
| 4073 | Royal Guard (trans) |
| 4061 | Warlock (trans) |
| 4074 | Sorcerer (trans) |
| 4062 | Ranger (trans) |
| 4075 | Minstrel (trans) |
| 4076 | Wanderer (trans) |
| 4063 | Arch Bishop (trans) |
| 4077 | Sura (trans) |
| 4064 | Mechanic (trans) |
| 4078 | Genetic (trans) |
| 4065 | Guillotine Cross (trans) |
| 4079 | Shadow Chaser (trans) |

### Expanded 3rd jobs (renewal only)

| ID | Job |
|---|---|
| 4190 | Super Novice (expanded) |
| 4239 | Starmperor |
| 4240 | Soul Reaper |
| 4215 | Rebellion |
| 4211 | Kagerou |
| 4212 | Oboro |
| 4218 | Summoner |

### 4th jobs (renewal only)

| ID | Job |
|---|---|
| 4252 | Dragon Knight |
| 4258 | Imperial Guard |
| 4255 | Arch Mage |
| 4261 | Elemental Master |
| 4257 | Windhawk |
| 4263 | Troubadour |
| 4264 | Trouvere |
| 4256 | Cardinal |
| 4262 | Inquisitor |
| 4253 | Meister |
| 4259 | Biolo |
| 4254 | Shadow Cross |
| 4260 | Abyss Chaser |

### Expanded 4th jobs (renewal only)

| ID | Job |
|---|---|
| 4307 | Hyper Novice |
| 4302 | Skymperor |
| 4303 | Soul Ascetic |
| 4306 | Night Watch |
| 4304 | Shinkiro |
| 4305 | Shiranui |
| 4308 | Spirit Handler |


---

## Best set per class

One full set per class line. The job IDs it's for are listed under each class name.
- **How it was built:** every item comes from the server's own item database (`db/pre-re/…` for pre-renewal classes, `db/re/…` for 3rd/4th jobs) and was checked: the ID exists, the class can equip it, the tier allows it (trans-only / 3rd-only / 4th-only) and it fits that slot. Slotted versions are used when they exist.
- **"(upper only)"** = transcendent only (Lord Knight, High Wizard…). The line below it (**others:**) is the pick for normal and baby classes.
- **"Best"** here means strong, widely used gear, not one absolute truth: it depends on build and, on renewal, on the game episode.
- **Pre-renewal sets** have two card columns: **Card** (normal cards, easy to farm) and **MVP card** (strongest). Each has a ready **command block** that creates the whole set **+10 with MVP cards inserted**. God items (Sleipnir, Megingjard, Brisingamen) have **no card slot**, so an optional block swaps them for a slotted item carrying the MVP card: pick one or the other.
- **Renewal sets** list gear only (no card suggestions). **A-type / Booster** = physical (ATK), **B-type / Battle Chip** = magic (MATK).
- **Min lv** = required base level (empty = none).

## Refining (`@refine`)
`@refine <position> <amount>` refines what you're **wearing** (+ or -). Max: **+10 pre-renewal**, **+20 renewal**. GM refine never fails and ignores the "refinable" flag.

| Position | Slot | | Position | Slot |
|---|---|---|---|---|
| `0` | **everything equipped** | | `16` | armor |
| `2` | weapon (right hand) | | `4` | garment |
| `32` | shield (left hand) | | `64` | shoes |
| `256` | head top | | `8` | accessory right |
| `512` | head mid | | `128` | accessory left |
| `1` | head low | | | |

**Refine everything to the max:** `@refine 0 10` (pre-renewal) / `@refine 0 20` (renewal). Asking for more is capped, and `@refine 0 -20` resets everything to +0.
Only **equipped** items are refined; items in your inventory are skipped (equip them first, or create them refined with `@item2`).

Examples: `@refine 2 5` = weapon +5 · `@refine 16 -3` = armor -3.
Or create items already refined: `@item2 <ID> 1 1 <refine> 0 <card1> <card2> <card3> <card4>`, e.g. `@item2 1172 1 1 10 0 4305 4142 0 0` = +10 Claymore with Turtle General + Doppelganger. (Order: item, amount, identified, refine, attribute, 4 cards; 0 = empty slot.)

### Pre-renewal MVP cards (by slot)

Taken from the MVP drops in `db/pre-re/mob_db.yml`; slot and effect read from each card's entry and bonus script in the item database (some have downsides: check before using).

**Weapon**

| ID | Card | Effect | Dropped by |
|---|---|---|---|
| 4121 | Phreeoni | +100 HIT | Phreeoni |
| 4134 | Dracula | SP drain on hit | Dracula |
| 4137 | Drake | no size penalty (full damage vs all sizes) | Drake |
| 4142 | Doppelganger | +10% attack speed | Doppelganger |
| 4147 | Baphomet | splash damage around target, -10 HIT | Baphomet |
| 4263 | Samurai Spector | ignores DEF of normal monsters, but no HP regen and you lose HP | Samurai Specter |
| 4276 | Lord of The Dead | chance of stun/curse/silence/poison…, coma on normal monsters | Lord of the Dead |
| 4305 | Turtle General | +20% damage vs all monsters, Magnum Break autocast | Turtle General |
| 4318 | Stormy Knight | freeze chance + Storm Gust autocast | Stormy Knight |
| 4361 | MasterSmith | breaks enemy weapons/armor | Whitesmith Howard |
| 4367 | Sniper | HP drain on hit, -10% HP regen | Sniper Cecil |
| 4399 | Memory of Thanatos | more damage vs high-DEF targets, -30 DEF/FLEE, costs SP per hit | Memory of Thanatos |
| 4407 | Randgris | +10% damage, unbreakable weapon, Dispel autocast | Valkyrie Randgris |
| 4425 | Atroce | +25 ATK, chance of +100% attack speed for 10s | Atroce |

**Headgear**

| ID | Card | Effect | Dropped by |
|---|---|---|---|
| 4132 | Mistress | no gemstones needed, +25% SP cost | Mistress |
| 4143 | Orc Hero | stun immunity, +3 VIT | Orc Hero |
| 4148 | Pharaoh | -30% SP cost | Pharaoh |
| 4330 | Evil Snake Lord | +3 INT, blind/curse immunity | Evil Snake Lord |
| 4357 | Lord Knight | gives Berserk skill, -50% max HP | Lord Knight Seyren |
| 4365 | High Wizard | ignores normal monsters' MDEF, but +100% cast time and no SP regen | High Wizard Kathryne |
| 4372 | White Lady | +30% heal power, +15% SP cost | White Lady |
| 4374 | Vesper | +2 DEX, ignores 30% of bosses' MDEF | Vesper |
| 4403 | Kiel-D-01 | -30% after-cast delay | Kiel D-01 |

**Armor**

| ID | Card | Effect | Dropped by |
|---|---|---|---|
| 4135 | Orc Lord | reflects 30% melee damage | Orc Lord |
| 4302 | Tao Gunka | +100% max HP, -50 DEF and MDEF | Tao Gunka |
| 4324 | Hatii | freezes attackers | Hatii |
| 4342 | RSX-0806 | no knockback, unbreakable armor, +3 VIT | RSX-0806 |
| 4363 | High Priest | Assumptio autocast when hit | High Priest Margaretha |
| 4386 | Detardeurus | freeze immune, Land Protector autocast, -20 MDEF | Detardeurus |
| 4408 | Gloom Under Night | +40% vs holy/dark element and angel/demon monsters | Gloom Under Night |
| 4419 | Ktullanux | +50% vs fire element, Frost Nova autocast when hit | Ktullanux |

**Shield**

| ID | Card | Effect | Dropped by |
|---|---|---|---|
| 4128 | Golden Thief Bug | immune to magic (also blocks heals/buffs), +100% SP cost | Golden Thief Bug |
| 4146 | Maya | reflects 50% of single-target magic | Maya |

**Garment**

| ID | Card | Effect | Dropped by |
|---|---|---|---|
| 4359 | Assassin Cross | gives the Cloaking skill (Lv 3) | Assassin Cross Eremes |

**Shoes**

| ID | Card | Effect | Dropped by |
|---|---|---|---|
| 4123 | Eddga | no flinch when hit (endure), -25% max HP | Eddga |
| 4131 | Moonlight Flower | +25% movement speed | Moonlight Flower |
| 4168 | Dark Lord | Meteor Storm autocast when hit | Dark Lord |
| 4236 | Amon Ra | +1 all stats, Kyrie Eleison autocast when hit | Amon Ra |
| 4352 | General Egnigem Cenia | +10% HP/SP, better regen | Egnigem Cenia |
| 4376 | Lady Tanee | -40% HP, +50% SP, better Banana Juice (joke card) | Lady Tanee |
| 4441 | Fallen Bishop Hibram | +10% MATK, +50% magic vs demi-humans/angels, -50% max SP | Fallen Bishop Hibram |

**Accessory**

| ID | Card | Effect | Dropped by |
|---|---|---|---|
| 4144 | Osiris | full HP/SP when revived | Osiris |
| 4145 | Berzebub | -30% cast time | Beelzebub |
| 4430 | Ifrit | +ATK/crit/HIT (job level ÷ 10), Earthquake autocast when hit | Ifrit |

### Everyone: consumables & materials

| ID | Item |
|---|---|
| 504 | White Potion |
| 505 | Blue Potion |
| 607 | Yggdrasil Berry |
| 601 | Fly Wing |
| 602 | Butterfly Wing |
| 12103 | Bloody Branch |
| 616 | Old Card Album |
| 603 | Old Blue Box |
| 7620 | Enriched Oridecon |
| 7619 | Enriched Elunium |
| 7621 | Token Of Siegfried |

### Consumables per class (pre-renewal)

Every item checked in `db/pre-re/item_db_*.yml`: exists, usable by the class (Berserk/Awakening potions are class-locked) and level. Same IDs exist on the renewal server.
- **Speed potion** = attack speed. Strongest allowed: Berserk `657` (lv 85) > Awakening `656` (lv 40) > Concentration `645` (anyone). If your level is lower, use the next one.
- **Stat dishes** = +10 to one stat for 20 minutes (they stack with each other: one of each stat).
- **For everyone:** White Potion `504`, Condensed White Potion `547`, Blue Potion `505`, Yggdrasil Berry `607`, Yggdrasil Seed `608`, Yggdrasil Leaf `610`, Fly Wing `601`, Butterfly Wing `602`, Speed Potion `12016` (movement speed for 5 s, not attack speed).

| Class line | Job IDs | Speed potion | Stat dishes (+10) | Class items |
|---|---|---|---|---|
| Novice | `0`, `4001`, `4023` | Awakening `656` (lv40) / Concentration `645` | STR `12075`, AGI `12090`, VIT `12085` | — |
| Swordman | `1`, `4002`, `4024` | Berserk `657` (lv85) / Awakening `656` (lv40) / Concentration `645` | STR `12075`, AGI `12090`, VIT `12085` | — |
| Mage | `2`, `4003`, `4025` | Berserk `657` (lv85) / Awakening `656` (lv40) / Concentration `645` | INT `12080`, DEX `12095`, VIT `12085` | Blue Gemstone `717`, Yellow Gemstone `715` |
| Archer | `3`, `4004`, `4026` | Awakening `656` (lv40) / Concentration `645` | DEX `12095`, AGI `12090`, LUK `12100` | Silver Arrow `1751`, Crystal Arrow `1754`, Fire Arrow `1752`, Immaterial Arrow `1757` |
| Acolyte | `4`, `4005`, `4027` | Concentration `645` | INT `12080`, DEX `12095`, VIT `12085` | Blue Gemstone `717`, Holy Water `523` |
| Merchant | `5`, `4006`, `4028` | Berserk `657` (lv85) / Awakening `656` (lv40) / Concentration `645` | STR `12075`, DEX `12095`, VIT `12085` | — |
| Thief | `6`, `4007`, `4029` | Awakening `656` (lv40) / Concentration `645` | AGI `12090`, STR `12075`, LUK `12100` | Silver Arrow `1751` |
| Knight line | `7`, `4008`, `4030` | Berserk `657` (lv85) / Awakening `656` (lv40) / Concentration `645` | STR `12075`, AGI `12090`, VIT `12085` | — |
| Crusader line | `14`, `4015`, `4037` | Berserk `657` (lv85) / Awakening `656` (lv40) / Concentration `645` | STR `12075`, VIT `12085`, DEX `12095` | Holy Water `523` |
| Wizard line | `9`, `4010`, `4032` | Berserk `657` (lv85) / Awakening `656` (lv40) / Concentration `645` | INT `12080`, DEX `12095`, VIT `12085` | Blue Gemstone `717`, Yellow Gemstone `715` |
| Sage line | `16`, `4017`, `4039` | Awakening `656` (lv40) / Concentration `645` | INT `12080`, DEX `12095`, VIT `12085` | Yellow Gemstone `715`, Blue Gemstone `717`, Red Gemstone `716` |
| Hunter line | `11`, `4012`, `4034` | Awakening `656` (lv40) / Concentration `645` | DEX `12095`, AGI `12090`, LUK `12100` | Silver Arrow `1751`, Crystal Arrow `1754`, Fire Arrow `1752`, Arrow of Wind `1755`, Stone Arrow `1756`, Immaterial Arrow `1757` |
| Bard line | `19`, `4020`, `4042` | Concentration `645` | DEX `12095`, AGI `12090`, INT `12080` | Silver Arrow `1751`, Crystal Arrow `1754` |
| Dancer line | `20`, `4021`, `4043` | Concentration `645` | DEX `12095`, AGI `12090`, INT `12080` | Silver Arrow `1751`, Crystal Arrow `1754` |
| Priest line | `8`, `4009`, `4031` | Concentration `645` | INT `12080`, DEX `12095`, VIT `12085` | Blue Gemstone `717`, Holy Water `523` |
| Monk line | `15`, `4016`, `4038` | Awakening `656` (lv40) / Concentration `645` | STR `12075`, AGI `12090`, DEX `12095` | — |
| Blacksmith line | `10`, `4011`, `4033` | Berserk `657` (lv85) / Awakening `656` (lv40) / Concentration `645` | STR `12075`, DEX `12095`, LUK `12100` | — |
| Alchemist line | `18`, `4019`, `4041` | Berserk `657` (lv85) / Awakening `656` (lv40) / Concentration `645` | STR `12075`, DEX `12095`, INT `12080` | Acid Bottle `7136`, Bottle Grenade `7135`, Marine Sphere Bottle `7138`, Glistening Coat `7139` |
| Assassin line | `12`, `4013`, `4035` | Awakening `656` (lv40) / Concentration `645` | AGI `12090`, STR `12075`, LUK `12100` | Poison Bottle `678` |
| Rogue line | `17`, `4018`, `4040` | Berserk `657` (lv85) / Awakening `656` (lv40) / Concentration `645` | DEX `12095`, AGI `12090`, STR `12075` | Silver Arrow `1751`, Crystal Arrow `1754` |
| Super Novice | `23`, `4045` | Awakening `656` (lv40) / Concentration `645` | STR `12075`, AGI `12090`, VIT `12085` | — |
| Gunslinger | `24` | Berserk `657` (lv85) / Awakening `656` (lv40) / Concentration `645` | DEX `12095`, AGI `12090`, LUK `12100` | Silver Bullet `13201`, Bullet `13200`, Flare Sphere `13203`, Freezing Sphere `13207` |
| Ninja | `25` | Awakening `656` (lv40) / Concentration `645` | DEX `12095`, INT `12080`, AGI `12090` | Thorn Needle Shuriken `13254`, Icicle Kunai `13255`, Heat Wave Kunai `13258`, High Wind Kunai `13257` |
| Taekwon | `4046` | Berserk `657` (lv85) / Awakening `656` (lv40) / Concentration `645` | AGI `12090`, STR `12075`, DEX `12095` | — |
| Star Gladiator | `4047` | Berserk `657` (lv85) / Awakening `656` (lv40) / Concentration `645` | STR `12075`, AGI `12090`, LUK `12100` | — |
| Soul Linker | `4049` | Berserk `657` (lv85) / Awakening `656` (lv40) / Concentration `645` | INT `12080`, DEX `12095`, VIT `12085` | Blue Gemstone `717` |

Ready commands per class (includes the everyone-items):

**Novice**
```
@item 656 20
@item 12075 10
@item 12090 10
@item 12085 10
@item 504 100
@item 547 100
@item 505 50
@item 607 20
@item 608 20
@item 610 10
@item 601 100
@item 602 10
@item 12016 10
```
**Swordman**
```
@item 657 20
@item 12075 10
@item 12090 10
@item 12085 10
@item 504 100
@item 547 100
@item 505 50
@item 607 20
@item 608 20
@item 610 10
@item 601 100
@item 602 10
@item 12016 10
```
**Mage**
```
@item 657 20
@item 12080 10
@item 12095 10
@item 12085 10
@item 717 20
@item 715 20
@item 504 100
@item 547 100
@item 505 50
@item 607 20
@item 608 20
@item 610 10
@item 601 100
@item 602 10
@item 12016 10
```
**Archer**
```
@item 656 20
@item 12095 10
@item 12090 10
@item 12100 10
@item 1751 1000
@item 1754 1000
@item 1752 1000
@item 1757 1000
@item 504 100
@item 547 100
@item 505 50
@item 607 20
@item 608 20
@item 610 10
@item 601 100
@item 602 10
@item 12016 10
```
**Acolyte**
```
@item 645 20
@item 12080 10
@item 12095 10
@item 12085 10
@item 717 20
@item 523 20
@item 504 100
@item 547 100
@item 505 50
@item 607 20
@item 608 20
@item 610 10
@item 601 100
@item 602 10
@item 12016 10
```
**Merchant**
```
@item 657 20
@item 12075 10
@item 12095 10
@item 12085 10
@item 504 100
@item 547 100
@item 505 50
@item 607 20
@item 608 20
@item 610 10
@item 601 100
@item 602 10
@item 12016 10
```
**Thief**
```
@item 656 20
@item 12090 10
@item 12075 10
@item 12100 10
@item 1751 1000
@item 504 100
@item 547 100
@item 505 50
@item 607 20
@item 608 20
@item 610 10
@item 601 100
@item 602 10
@item 12016 10
```
**Knight line**
```
@item 657 20
@item 12075 10
@item 12090 10
@item 12085 10
@item 504 100
@item 547 100
@item 505 50
@item 607 20
@item 608 20
@item 610 10
@item 601 100
@item 602 10
@item 12016 10
```
**Crusader line**
```
@item 657 20
@item 12075 10
@item 12085 10
@item 12095 10
@item 523 20
@item 504 100
@item 547 100
@item 505 50
@item 607 20
@item 608 20
@item 610 10
@item 601 100
@item 602 10
@item 12016 10
```
**Wizard line**
```
@item 657 20
@item 12080 10
@item 12095 10
@item 12085 10
@item 717 30
@item 715 30
@item 504 100
@item 547 100
@item 505 50
@item 607 20
@item 608 20
@item 610 10
@item 601 100
@item 602 10
@item 12016 10
```
**Sage line**
```
@item 656 20
@item 12080 10
@item 12095 10
@item 12085 10
@item 715 30
@item 717 30
@item 716 30
@item 504 100
@item 547 100
@item 505 50
@item 607 20
@item 608 20
@item 610 10
@item 601 100
@item 602 10
@item 12016 10
```
**Hunter line**
```
@item 656 20
@item 12095 10
@item 12090 10
@item 12100 10
@item 1751 1000
@item 1754 1000
@item 1752 1000
@item 1755 1000
@item 1756 1000
@item 1757 1000
@item 504 100
@item 547 100
@item 505 50
@item 607 20
@item 608 20
@item 610 10
@item 601 100
@item 602 10
@item 12016 10
```
**Bard line**
```
@item 645 20
@item 12095 10
@item 12090 10
@item 12080 10
@item 1751 1000
@item 1754 1000
@item 504 100
@item 547 100
@item 505 50
@item 607 20
@item 608 20
@item 610 10
@item 601 100
@item 602 10
@item 12016 10
```
**Dancer line**
```
@item 645 20
@item 12095 10
@item 12090 10
@item 12080 10
@item 1751 1000
@item 1754 1000
@item 504 100
@item 547 100
@item 505 50
@item 607 20
@item 608 20
@item 610 10
@item 601 100
@item 602 10
@item 12016 10
```
**Priest line**
```
@item 645 20
@item 12080 10
@item 12095 10
@item 12085 10
@item 717 30
@item 523 30
@item 504 100
@item 547 100
@item 505 50
@item 607 20
@item 608 20
@item 610 10
@item 601 100
@item 602 10
@item 12016 10
```
**Monk line**
```
@item 656 20
@item 12075 10
@item 12090 10
@item 12095 10
@item 504 100
@item 547 100
@item 505 50
@item 607 20
@item 608 20
@item 610 10
@item 601 100
@item 602 10
@item 12016 10
```
**Blacksmith line**
```
@item 657 20
@item 12075 10
@item 12095 10
@item 12100 10
@item 504 100
@item 547 100
@item 505 50
@item 607 20
@item 608 20
@item 610 10
@item 601 100
@item 602 10
@item 12016 10
```
**Alchemist line**
```
@item 657 20
@item 12075 10
@item 12095 10
@item 12080 10
@item 7136 50
@item 7135 50
@item 7138 20
@item 7139 20
@item 504 100
@item 547 100
@item 505 50
@item 607 20
@item 608 20
@item 610 10
@item 601 100
@item 602 10
@item 12016 10
```
**Assassin line**
```
@item 656 20
@item 12090 10
@item 12075 10
@item 12100 10
@item 678 20
@item 504 100
@item 547 100
@item 505 50
@item 607 20
@item 608 20
@item 610 10
@item 601 100
@item 602 10
@item 12016 10
```
**Rogue line**
```
@item 657 20
@item 12095 10
@item 12090 10
@item 12075 10
@item 1751 1000
@item 1754 1000
@item 504 100
@item 547 100
@item 505 50
@item 607 20
@item 608 20
@item 610 10
@item 601 100
@item 602 10
@item 12016 10
```
**Super Novice**
```
@item 656 20
@item 12075 10
@item 12090 10
@item 12085 10
@item 504 100
@item 547 100
@item 505 50
@item 607 20
@item 608 20
@item 610 10
@item 601 100
@item 602 10
@item 12016 10
```
**Gunslinger**
```
@item 657 20
@item 12095 10
@item 12090 10
@item 12100 10
@item 13201 1000
@item 13200 1000
@item 13203 100
@item 13207 100
@item 504 100
@item 547 100
@item 505 50
@item 607 20
@item 608 20
@item 610 10
@item 601 100
@item 602 10
@item 12016 10
```
**Ninja**
```
@item 656 20
@item 12095 10
@item 12080 10
@item 12090 10
@item 13254 1000
@item 13255 100
@item 13258 100
@item 13257 100
@item 504 100
@item 547 100
@item 505 50
@item 607 20
@item 608 20
@item 610 10
@item 601 100
@item 602 10
@item 12016 10
```
**Taekwon**
```
@item 657 20
@item 12090 10
@item 12075 10
@item 12095 10
@item 504 100
@item 547 100
@item 505 50
@item 607 20
@item 608 20
@item 610 10
@item 601 100
@item 602 10
@item 12016 10
```
**Star Gladiator**
```
@item 657 20
@item 12075 10
@item 12090 10
@item 12100 10
@item 504 100
@item 547 100
@item 505 50
@item 607 20
@item 608 20
@item 610 10
@item 601 100
@item 602 10
@item 12016 10
```
**Soul Linker**
```
@item 657 20
@item 12080 10
@item 12095 10
@item 12085 10
@item 717 20
@item 504 100
@item 547 100
@item 505 50
@item 607 20
@item 608 20
@item 610 10
@item 601 100
@item 602 10
@item 12016 10
```

### Pre-renewal classes (use on the pre-renewal server)

#### Novice

Job IDs: `0` Novice · `4001` High Novice · `4023` Baby

| Slot | ID | Item | Min lv | Card | MVP card |
|---|---|---|---|---|---|
| Weapon | `1505` | Mace | 2 | Hydra `4035` ×4 | Turtle General `4305`, Doppelganger `4142`, Drake `4137`, Baphomet `4147` |
| Shield | `2113` | Novice Shield | 40 | Thara Frog `4058` | Golden Thief Bug `4128` |
| Head top | `5125` | Angel's Kiss | 50 | Orc Hero `4143` | Orc Hero `4143` |
| Head mid | `2202` | Sunglasses |  |  | Pharaoh `4148` |
| Head low | `2265` | Gangster Mask |  |  |  |
| Armor | `2355` | Angelic Protection | 40 | Marc `4105` | Tao Gunka `4302` |
| Garment | `2512` | Novice Manteau | 40 | Raydric `4133` | Assassin Cross `4359` |
| Shoes | `2410` | Sleipnir | 94 |  |  |
| Accessory 1 | `2629` | Megingjard | 94 |  | no slot → Ifrit `4430` on Clip `2607` |
| Accessory 2 | `2630` | Brisingamen | 94 |  |  |

Other weapons: Blade `1108`

Whole set (same order as the table), +10 where refinable, MVP cards inserted:
```
@item2 1505 1 1 10 0 4305 4142 4137 4147
@item2 2113 1 1 10 0 4128 0 0 0
@item2 5125 1 1 10 0 4143 0 0 0
@item2 2202 1 1 0 0 4148 0 0 0
@item2 2265 1 1 0 0 0 0 0 0
@item2 2355 1 1 10 0 4302 0 0 0
@item2 2512 1 1 10 0 4359 0 0 0
@item2 2410 1 1 0 0 0 0 0 0
@item2 2629 1 1 0 0 0 0 0 0
@item2 2630 1 1 0 0 0 0 0 0
```

Optional card swaps (slotted item + MVP card instead of the no-slot item):
```
@item2 2607 1 1 0 0 4430 0 0 0
```

#### Swordman

Job IDs: `1` Swordman · `4002` High Swordman · `4024` Baby Swordman

| Slot | ID | Item | Min lv | Card | MVP card |
|---|---|---|---|---|---|
| Weapon | `1131` | Ice Falchion | 40 |  |  |
| Shield | `2115` | Valkyrja's Shield | 65 | Thara Frog `4058` | Golden Thief Bug `4128` |
| Head top | `5171` | Valkyrie Helm (upper only)<br>others: Helm `2229` |  | Orc Hero `4143` | Orc Hero `4143` |
| Head mid | `2202` | Sunglasses |  |  | Pharaoh `4148` |
| Head low | `2265` | Gangster Mask |  |  |  |
| Armor | `2357` | Valkyrian Armor (upper only)<br>others: Formal Suit `2320` | 1 | Marc `4105` | Tao Gunka `4302` |
| Garment | `2524` | Valkyrian Manteau (upper only)<br>others: Muffler `2504` | 1 | Raydric `4133` | Assassin Cross `4359` |
| Shoes | `2410` | Sleipnir | 94 |  | no slot → Eddga `4123` on Valkyrian Shoes `2421` |
| Accessory 1 | `2629` | Megingjard | 94 |  | no slot → Ifrit `4430` on Clip `2607` |
| Accessory 2 | `2630` | Brisingamen | 94 |  | no slot → Osiris `4144` on Rosary `2626` |

Other weapons: Blade `1108`, Sword `1102`

Whole set (same order as the table), +10 where refinable, MVP cards inserted:
```
@item2 1131 1 1 10 0 0 0 0 0
@item2 2115 1 1 10 0 4128 0 0 0
@item2 5171 1 1 10 0 4143 0 0 0
@item2 2202 1 1 0 0 4148 0 0 0
@item2 2265 1 1 0 0 0 0 0 0
@item2 2357 1 1 10 0 4302 0 0 0
@item2 2524 1 1 10 0 4359 0 0 0
@item2 2410 1 1 0 0 0 0 0 0
@item2 2629 1 1 0 0 0 0 0 0
@item2 2630 1 1 0 0 0 0 0 0
```

Optional card swaps (slotted item + MVP card instead of the no-slot item):
```
@item2 2421 1 1 10 0 4123 0 0 0
@item2 2607 1 1 0 0 4430 0 0 0
@item2 2626 1 1 0 0 4144 0 0 0
```

#### Mage

Job IDs: `2` Mage · `4003` High Mage · `4025` Baby Mage

| Slot | ID | Item | Min lv | Card | MVP card |
|---|---|---|---|---|---|
| Weapon | `1644` | Staff of Piercing (upper only)<br>others: Survivor's Rod `1618` | 70 |  |  |
| Shield | `2115` | Valkyrja's Shield | 65 | Thara Frog `4058` | Maya `4146` |
| Head top | `5045` | Magician Hat | 50 |  | no slot → Kiel-D-01 `4403` on Crown `5165` |
| Head mid | `2202` | Sunglasses |  |  | Vesper `4374` |
| Head low | `2265` | Gangster Mask |  |  |  |
| Armor | `2357` | Valkyrian Armor (upper only)<br>others: Formal Suit `2320` | 1 | Marc `4105` | Tao Gunka `4302` |
| Garment | `2524` | Valkyrian Manteau (upper only)<br>others: Muffler `2504` | 1 | Raydric `4133` | Assassin Cross `4359` |
| Shoes | `2410` | Sleipnir | 94 |  | no slot → Fallen Bishop Hibram `4441` on Valkyrian Shoes `2421` |
| Accessory 1 | `2630` | Brisingamen | 94 |  | no slot → Berzebub `4145` on Clip `2607` |
| Accessory 2 | `2626` | Rosary | 90 | Phen `4077` | Osiris `4144` |

Other weapons: Survivor's Rod `1618`, Rod `1602`

Whole set (same order as the table), +10 where refinable, MVP cards inserted:
```
@item2 1644 1 1 10 0 0 0 0 0
@item2 2115 1 1 10 0 4146 0 0 0
@item2 5045 1 1 10 0 0 0 0 0
@item2 2202 1 1 0 0 4374 0 0 0
@item2 2265 1 1 0 0 0 0 0 0
@item2 2357 1 1 10 0 4302 0 0 0
@item2 2524 1 1 10 0 4359 0 0 0
@item2 2410 1 1 0 0 0 0 0 0
@item2 2630 1 1 0 0 0 0 0 0
@item2 2626 1 1 0 0 4144 0 0 0
```

Optional card swaps (slotted item + MVP card instead of the no-slot item):
```
@item2 5165 1 1 10 0 4403 0 0 0
@item2 2421 1 1 10 0 4441 0 0 0
@item2 2607 1 1 0 0 4145 0 0 0
```

#### Archer

Job IDs: `3` Archer · `4004` High Archer · `4026` Baby Archer

| Slot | ID | Item | Min lv | Card | MVP card |
|---|---|---|---|---|---|
| Weapon | `1705` | Composite Bow | 4 | Hydra `4035` ×4 | Turtle General `4305`, Doppelganger `4142`, Drake `4137`, Baphomet `4147` |
| Head top | `5171` | Valkyrie Helm (upper only)<br>others: Crown `5165` |  | Orc Hero `4143` | Orc Hero `4143` |
| Head mid | `2202` | Sunglasses |  |  | Pharaoh `4148` |
| Head low | `2265` | Gangster Mask |  |  |  |
| Armor | `2357` | Valkyrian Armor (upper only)<br>others: Formal Suit `2320` | 1 | Marc `4105` | Tao Gunka `4302` |
| Garment | `2524` | Valkyrian Manteau (upper only)<br>others: Muffler `2504` | 1 | Raydric `4133` | Assassin Cross `4359` |
| Shoes | `2410` | Sleipnir | 94 |  | no slot → Eddga `4123` on Valkyrian Shoes `2421` |
| Accessory 1 | `2629` | Megingjard | 94 |  | no slot → Ifrit `4430` on Clip `2607` |
| Accessory 2 | `2630` | Brisingamen | 94 |  | no slot → Osiris `4144` on Rosary `2626` |

Other weapons: Bow `1702`

Whole set (same order as the table), +10 where refinable, MVP cards inserted:
```
@item2 1705 1 1 10 0 4305 4142 4137 4147
@item2 5171 1 1 10 0 4143 0 0 0
@item2 2202 1 1 0 0 4148 0 0 0
@item2 2265 1 1 0 0 0 0 0 0
@item2 2357 1 1 10 0 4302 0 0 0
@item2 2524 1 1 10 0 4359 0 0 0
@item2 2410 1 1 0 0 0 0 0 0
@item2 2629 1 1 0 0 0 0 0 0
@item2 2630 1 1 0 0 0 0 0 0
```

Optional card swaps (slotted item + MVP card instead of the no-slot item):
```
@item2 2421 1 1 10 0 4123 0 0 0
@item2 2607 1 1 0 0 4430 0 0 0
@item2 2626 1 1 0 0 4144 0 0 0
```

#### Acolyte

Job IDs: `4` Acolyte · `4005` High Acolyte · `4027` Baby Acolyte

| Slot | ID | Item | Min lv | Card | MVP card |
|---|---|---|---|---|---|
| Weapon | `1505` | Mace | 2 |  | Dracula `4134` |
| Shield | `2115` | Valkyrja's Shield | 65 | Thara Frog `4058` | Maya `4146` |
| Head top | `5171` | Valkyrie Helm (upper only)<br>others: Crown `5165` |  | Kiel-D-01 `4403` | Kiel-D-01 `4403` |
| Head mid | `2202` | Sunglasses |  |  | Vesper `4374` |
| Head low | `2265` | Gangster Mask |  |  |  |
| Armor | `2357` | Valkyrian Armor (upper only)<br>others: Formal Suit `2320` | 1 | Marc `4105` | Tao Gunka `4302` |
| Garment | `2524` | Valkyrian Manteau (upper only)<br>others: Muffler `2504` | 1 | Raydric `4133` | Assassin Cross `4359` |
| Shoes | `2410` | Sleipnir | 94 |  | no slot → Fallen Bishop Hibram `4441` on Valkyrian Shoes `2421` |
| Accessory 1 | `2630` | Brisingamen | 94 |  | no slot → Berzebub `4145` on Clip `2607` |
| Accessory 2 | `2626` | Rosary | 90 | Phen `4077` | Osiris `4144` |

Other weapons: Rod `1602`

Whole set (same order as the table), +10 where refinable, MVP cards inserted:
```
@item2 1505 1 1 10 0 4134 0 0 0
@item2 2115 1 1 10 0 4146 0 0 0
@item2 5171 1 1 10 0 4403 0 0 0
@item2 2202 1 1 0 0 4374 0 0 0
@item2 2265 1 1 0 0 0 0 0 0
@item2 2357 1 1 10 0 4302 0 0 0
@item2 2524 1 1 10 0 4359 0 0 0
@item2 2410 1 1 0 0 0 0 0 0
@item2 2630 1 1 0 0 0 0 0 0
@item2 2626 1 1 0 0 4144 0 0 0
```

Optional card swaps (slotted item + MVP card instead of the no-slot item):
```
@item2 2421 1 1 10 0 4441 0 0 0
@item2 2607 1 1 0 0 4145 0 0 0
```

#### Merchant

Job IDs: `5` Merchant · `4006` High Merchant · `4028` Baby Merchant

| Slot | ID | Item | Min lv | Card | MVP card |
|---|---|---|---|---|---|
| Weapon | `1314` | Tomahawk |  |  |  |
| Head top | `5171` | Valkyrie Helm (upper only)<br>others: Crown `5165` |  | Orc Hero `4143` | Orc Hero `4143` |
| Head mid | `2202` | Sunglasses |  |  | Pharaoh `4148` |
| Head low | `2265` | Gangster Mask |  |  |  |
| Armor | `2357` | Valkyrian Armor (upper only)<br>others: Formal Suit `2320` | 1 | Marc `4105` | Tao Gunka `4302` |
| Garment | `2524` | Valkyrian Manteau (upper only)<br>others: Muffler `2504` | 1 | Raydric `4133` | Assassin Cross `4359` |
| Shoes | `2410` | Sleipnir | 94 |  | no slot → Eddga `4123` on Valkyrian Shoes `2421` |
| Accessory 1 | `2629` | Megingjard | 94 |  | no slot → Ifrit `4430` on Clip `2607` |
| Accessory 2 | `2630` | Brisingamen | 94 |  | no slot → Osiris `4144` on Rosary `2626` |

Other weapons: Axe `1302`

Whole set (same order as the table), +10 where refinable, MVP cards inserted:
```
@item2 1314 1 1 0 0 0 0 0 0
@item2 5171 1 1 10 0 4143 0 0 0
@item2 2202 1 1 0 0 4148 0 0 0
@item2 2265 1 1 0 0 0 0 0 0
@item2 2357 1 1 10 0 4302 0 0 0
@item2 2524 1 1 10 0 4359 0 0 0
@item2 2410 1 1 0 0 0 0 0 0
@item2 2629 1 1 0 0 0 0 0 0
@item2 2630 1 1 0 0 0 0 0 0
```

Optional card swaps (slotted item + MVP card instead of the no-slot item):
```
@item2 2421 1 1 10 0 4123 0 0 0
@item2 2607 1 1 0 0 4430 0 0 0
@item2 2626 1 1 0 0 4144 0 0 0
```

#### Thief

Job IDs: `6` Thief · `4007` High Thief · `4029` Baby Thief

| Slot | ID | Item | Min lv | Card | MVP card |
|---|---|---|---|---|---|
| Weapon | `1220` | Gladius | 24 | Hydra `4035` ×3 | Turtle General `4305`, Doppelganger `4142`, Drake `4137` |
| Shield | `2115` | Valkyrja's Shield | 65 | Thara Frog `4058` | Golden Thief Bug `4128` |
| Head top | `5171` | Valkyrie Helm (upper only)<br>others: Crown `5165` |  | Orc Hero `4143` | Orc Hero `4143` |
| Head mid | `2202` | Sunglasses |  |  | Pharaoh `4148` |
| Head low | `2265` | Gangster Mask |  |  |  |
| Armor | `2357` | Valkyrian Armor (upper only)<br>others: Formal Suit `2320` | 1 | Marc `4105` | Tao Gunka `4302` |
| Garment | `2524` | Valkyrian Manteau (upper only)<br>others: Muffler `2504` | 1 | Raydric `4133` | Assassin Cross `4359` |
| Shoes | `2410` | Sleipnir | 94 |  | no slot → Eddga `4123` on Valkyrian Shoes `2421` |
| Accessory 1 | `2629` | Megingjard | 94 |  | no slot → Ifrit `4430` on Clip `2607` |
| Accessory 2 | `2630` | Brisingamen | 94 |  | no slot → Osiris `4144` on Rosary `2626` |

Other weapons: Main Gauche `1208`, Knife `1202`

Whole set (same order as the table), +10 where refinable, MVP cards inserted:
```
@item2 1220 1 1 10 0 4305 4142 4137 0
@item2 2115 1 1 10 0 4128 0 0 0
@item2 5171 1 1 10 0 4143 0 0 0
@item2 2202 1 1 0 0 4148 0 0 0
@item2 2265 1 1 0 0 0 0 0 0
@item2 2357 1 1 10 0 4302 0 0 0
@item2 2524 1 1 10 0 4359 0 0 0
@item2 2410 1 1 0 0 0 0 0 0
@item2 2629 1 1 0 0 0 0 0 0
@item2 2630 1 1 0 0 0 0 0 0
```

Optional card swaps (slotted item + MVP card instead of the no-slot item):
```
@item2 2421 1 1 10 0 4123 0 0 0
@item2 2607 1 1 0 0 4430 0 0 0
@item2 2626 1 1 0 0 4144 0 0 0
```

#### Knight line

Job IDs: `7` Knight · `4008` Lord Knight · `4030` Baby Knight

| Slot | ID | Item | Min lv | Card | MVP card |
|---|---|---|---|---|---|
| Weapon | `1172` | Claymore | 33 | Hydra `4035` ×2 | Turtle General `4305`, Doppelganger `4142` |
| Head top | `5171` | Valkyrie Helm (upper only)<br>others: Helm `2229` |  | Orc Hero `4143` | Orc Hero `4143` |
| Head mid | `2202` | Sunglasses |  |  | Pharaoh `4148` |
| Head low | `2265` | Gangster Mask |  |  |  |
| Armor | `2357` | Valkyrian Armor (upper only)<br>others: Formal Suit `2320` | 1 | Marc `4105` | Tao Gunka `4302` |
| Garment | `2524` | Valkyrian Manteau (upper only)<br>others: Muffler `2504` | 1 | Raydric `4133` | Assassin Cross `4359` |
| Shoes | `2410` | Sleipnir | 94 |  | no slot → Eddga `4123` on Valkyrian Shoes `2421` |
| Accessory 1 | `2629` | Megingjard | 94 |  | no slot → Ifrit `4430` on Clip `2607` |
| Accessory 2 | `2630` | Brisingamen | 94 |  | no slot → Osiris `4144` on Rosary `2626` |

Other weapons: Longinus's Spear `1469`, Gungnir `1418`, Muramasa `1164`

Whole set (same order as the table), +10 where refinable, MVP cards inserted:
```
@item2 1172 1 1 10 0 4305 4142 0 0
@item2 5171 1 1 10 0 4143 0 0 0
@item2 2202 1 1 0 0 4148 0 0 0
@item2 2265 1 1 0 0 0 0 0 0
@item2 2357 1 1 10 0 4302 0 0 0
@item2 2524 1 1 10 0 4359 0 0 0
@item2 2410 1 1 0 0 0 0 0 0
@item2 2629 1 1 0 0 0 0 0 0
@item2 2630 1 1 0 0 0 0 0 0
```

Optional card swaps (slotted item + MVP card instead of the no-slot item):
```
@item2 2421 1 1 10 0 4123 0 0 0
@item2 2607 1 1 0 0 4430 0 0 0
@item2 2626 1 1 0 0 4144 0 0 0
```

#### Crusader line

Job IDs: `14` Crusader · `4015` Paladin · `4037` Baby Crusader

| Slot | ID | Item | Min lv | Card | MVP card |
|---|---|---|---|---|---|
| Weapon | `1145` | Holy Avenger | 75 |  |  |
| Shield | `2115` | Valkyrja's Shield | 65 | Thara Frog `4058` | Golden Thief Bug `4128` |
| Head top | `5171` | Valkyrie Helm (upper only)<br>others: Helm `2229` |  | Orc Hero `4143` | Orc Hero `4143` |
| Head mid | `2202` | Sunglasses |  |  | Pharaoh `4148` |
| Head low | `2265` | Gangster Mask |  |  |  |
| Armor | `2357` | Valkyrian Armor (upper only)<br>others: Formal Suit `2320` | 1 | Marc `4105` | Tao Gunka `4302` |
| Garment | `2524` | Valkyrian Manteau (upper only)<br>others: Muffler `2504` | 1 | Raydric `4133` | Assassin Cross `4359` |
| Shoes | `2410` | Sleipnir | 94 |  | no slot → Eddga `4123` on Valkyrian Shoes `2421` |
| Accessory 1 | `2629` | Megingjard | 94 |  | no slot → Ifrit `4430` on Clip `2607` |
| Accessory 2 | `2630` | Brisingamen | 94 |  | no slot → Osiris `4144` on Rosary `2626` |

Other weapons: Gungnir `1418`, Lance `1410`

Whole set (same order as the table), +10 where refinable, MVP cards inserted:
```
@item2 1145 1 1 10 0 0 0 0 0
@item2 2115 1 1 10 0 4128 0 0 0
@item2 5171 1 1 10 0 4143 0 0 0
@item2 2202 1 1 0 0 4148 0 0 0
@item2 2265 1 1 0 0 0 0 0 0
@item2 2357 1 1 10 0 4302 0 0 0
@item2 2524 1 1 10 0 4359 0 0 0
@item2 2410 1 1 0 0 0 0 0 0
@item2 2629 1 1 0 0 0 0 0 0
@item2 2630 1 1 0 0 0 0 0 0
```

Optional card swaps (slotted item + MVP card instead of the no-slot item):
```
@item2 2421 1 1 10 0 4123 0 0 0
@item2 2607 1 1 0 0 4430 0 0 0
@item2 2626 1 1 0 0 4144 0 0 0
```

#### Wizard line

Job IDs: `9` Wizard · `4010` High Wizard · `4032` Baby Wizard

| Slot | ID | Item | Min lv | Card | MVP card |
|---|---|---|---|---|---|
| Weapon | `2000` | Staff of Destruction (upper only)<br>others: Wizardry Staff `1473` | 80 |  | Dracula `4134` |
| Head top | `5045` | Magician Hat | 50 |  | no slot → Kiel-D-01 `4403` on Crown `5165` |
| Head mid | `2202` | Sunglasses |  |  | Vesper `4374` |
| Head low | `2265` | Gangster Mask |  |  |  |
| Armor | `2357` | Valkyrian Armor (upper only)<br>others: Formal Suit `2320` | 1 | Marc `4105` | Tao Gunka `4302` |
| Garment | `2524` | Valkyrian Manteau (upper only)<br>others: Muffler `2504` | 1 | Raydric `4133` | Assassin Cross `4359` |
| Shoes | `2410` | Sleipnir | 94 |  | no slot → Fallen Bishop Hibram `4441` on Valkyrian Shoes `2421` |
| Accessory 1 | `2630` | Brisingamen | 94 |  | no slot → Berzebub `4145` on Clip `2607` |
| Accessory 2 | `2626` | Rosary | 90 | Phen `4077` | Osiris `4144` |

Other weapons: Wizardry Staff `1473`, Staff of Piercing `1644`

Whole set (same order as the table), +10 where refinable, MVP cards inserted:
```
@item2 2000 1 1 10 0 4134 0 0 0
@item2 5045 1 1 10 0 0 0 0 0
@item2 2202 1 1 0 0 4374 0 0 0
@item2 2265 1 1 0 0 0 0 0 0
@item2 2357 1 1 10 0 4302 0 0 0
@item2 2524 1 1 10 0 4359 0 0 0
@item2 2410 1 1 0 0 0 0 0 0
@item2 2630 1 1 0 0 0 0 0 0
@item2 2626 1 1 0 0 4144 0 0 0
```

Optional card swaps (slotted item + MVP card instead of the no-slot item):
```
@item2 5165 1 1 10 0 4403 0 0 0
@item2 2421 1 1 10 0 4441 0 0 0
@item2 2607 1 1 0 0 4145 0 0 0
```

#### Sage line

Job IDs: `16` Sage · `4017` Professor · `4039` Baby Sage

| Slot | ID | Item | Min lv | Card | MVP card |
|---|---|---|---|---|---|
| Weapon | `1557` | Book of the Apocalypse | 40 |  |  |
| Shield | `2115` | Valkyrja's Shield | 65 | Thara Frog `4058` | Maya `4146` |
| Head top | `5045` | Magician Hat | 50 |  | no slot → Kiel-D-01 `4403` on Crown `5165` |
| Head mid | `2202` | Sunglasses |  |  | Vesper `4374` |
| Head low | `2265` | Gangster Mask |  |  |  |
| Armor | `2357` | Valkyrian Armor (upper only)<br>others: Formal Suit `2320` | 1 | Marc `4105` | Tao Gunka `4302` |
| Garment | `2524` | Valkyrian Manteau (upper only)<br>others: Muffler `2504` | 1 | Raydric `4133` | Assassin Cross `4359` |
| Shoes | `2410` | Sleipnir | 94 |  | no slot → Fallen Bishop Hibram `4441` on Valkyrian Shoes `2421` |
| Accessory 1 | `2630` | Brisingamen | 94 |  | no slot → Berzebub `4145` on Clip `2607` |
| Accessory 2 | `2626` | Rosary | 90 | Phen `4077` | Osiris `4144` |

Other weapons: Staff of Piercing `1644`

Whole set (same order as the table), +10 where refinable, MVP cards inserted:
```
@item2 1557 1 1 10 0 0 0 0 0
@item2 2115 1 1 10 0 4146 0 0 0
@item2 5045 1 1 10 0 0 0 0 0
@item2 2202 1 1 0 0 4374 0 0 0
@item2 2265 1 1 0 0 0 0 0 0
@item2 2357 1 1 10 0 4302 0 0 0
@item2 2524 1 1 10 0 4359 0 0 0
@item2 2410 1 1 0 0 0 0 0 0
@item2 2630 1 1 0 0 0 0 0 0
@item2 2626 1 1 0 0 4144 0 0 0
```

Optional card swaps (slotted item + MVP card instead of the no-slot item):
```
@item2 5165 1 1 10 0 4403 0 0 0
@item2 2421 1 1 10 0 4441 0 0 0
@item2 2607 1 1 0 0 4145 0 0 0
```

#### Hunter line

Job IDs: `11` Hunter · `4012` Sniper · `4034` Baby Hunter

| Slot | ID | Item | Min lv | Card | MVP card |
|---|---|---|---|---|---|
| Weapon | `1720` | Rudra Bow | 48 |  |  |
| Head top | `2285` | Apple of Archer | 30 |  | no slot → Orc Hero `4143` on Crown `5165` |
| Head mid | `2202` | Sunglasses |  |  | Pharaoh `4148` |
| Head low | `2265` | Gangster Mask |  |  |  |
| Armor | `2357` | Valkyrian Armor (upper only)<br>others: Formal Suit `2320` | 1 | Marc `4105` | Tao Gunka `4302` |
| Garment | `2524` | Valkyrian Manteau (upper only)<br>others: Muffler `2504` | 1 | Raydric `4133` | Assassin Cross `4359` |
| Shoes | `2410` | Sleipnir | 94 |  | no slot → Eddga `4123` on Valkyrian Shoes `2421` |
| Accessory 1 | `2629` | Megingjard | 94 |  | no slot → Ifrit `4430` on Clip `2607` |
| Accessory 2 | `2630` | Brisingamen | 94 |  | no slot → Osiris `4144` on Rosary `2626` |

Other weapons: Ballista `1727`, Hunter Bow `1726`, Composite Bow `1705`

Whole set (same order as the table), +10 where refinable, MVP cards inserted:
```
@item2 1720 1 1 10 0 0 0 0 0
@item2 2285 1 1 10 0 0 0 0 0
@item2 2202 1 1 0 0 4148 0 0 0
@item2 2265 1 1 0 0 0 0 0 0
@item2 2357 1 1 10 0 4302 0 0 0
@item2 2524 1 1 10 0 4359 0 0 0
@item2 2410 1 1 0 0 0 0 0 0
@item2 2629 1 1 0 0 0 0 0 0
@item2 2630 1 1 0 0 0 0 0 0
```

Optional card swaps (slotted item + MVP card instead of the no-slot item):
```
@item2 5165 1 1 10 0 4143 0 0 0
@item2 2421 1 1 10 0 4123 0 0 0
@item2 2607 1 1 0 0 4430 0 0 0
@item2 2626 1 1 0 0 4144 0 0 0
```

#### Bard line (male)

Job IDs: `19` Bard · `4020` Clown · `4042` Baby Bard

| Slot | ID | Item | Min lv | Card | MVP card |
|---|---|---|---|---|---|
| Weapon | `1922` | Oriental Lute | 65 | Hydra `4035` ×2 | Turtle General `4305`, Doppelganger `4142` |
| Shield | `2115` | Valkyrja's Shield | 65 | Thara Frog `4058` | Golden Thief Bug `4128` |
| Head top | `5171` | Valkyrie Helm (upper only)<br>others: Crown `5165` |  | Orc Hero `4143` | Orc Hero `4143` |
| Head mid | `2202` | Sunglasses |  |  | Pharaoh `4148` |
| Head low | `2265` | Gangster Mask |  |  |  |
| Armor | `2357` | Valkyrian Armor (upper only)<br>others: Formal Suit `2320` | 1 | Marc `4105` | Tao Gunka `4302` |
| Garment | `2524` | Valkyrian Manteau (upper only)<br>others: Muffler `2504` | 1 | Raydric `4133` | Assassin Cross `4359` |
| Shoes | `2410` | Sleipnir | 94 |  | no slot → Eddga `4123` on Valkyrian Shoes `2421` |
| Accessory 1 | `2629` | Megingjard | 94 |  | no slot → Ifrit `4430` on Clip `2607` |
| Accessory 2 | `2630` | Brisingamen | 94 |  | no slot → Osiris `4144` on Rosary `2626` |

Other weapons: Electric Guitar `1913`, Composite Bow `1705`

Whole set (same order as the table), +10 where refinable, MVP cards inserted:
```
@item2 1922 1 1 10 0 4305 4142 0 0
@item2 2115 1 1 10 0 4128 0 0 0
@item2 5171 1 1 10 0 4143 0 0 0
@item2 2202 1 1 0 0 4148 0 0 0
@item2 2265 1 1 0 0 0 0 0 0
@item2 2357 1 1 10 0 4302 0 0 0
@item2 2524 1 1 10 0 4359 0 0 0
@item2 2410 1 1 0 0 0 0 0 0
@item2 2629 1 1 0 0 0 0 0 0
@item2 2630 1 1 0 0 0 0 0 0
```

Optional card swaps (slotted item + MVP card instead of the no-slot item):
```
@item2 2421 1 1 10 0 4123 0 0 0
@item2 2607 1 1 0 0 4430 0 0 0
@item2 2626 1 1 0 0 4144 0 0 0
```

#### Dancer line (female)

Job IDs: `20` Dancer · `4021` Gypsy · `4043` Baby Dancer

| Slot | ID | Item | Min lv | Card | MVP card |
|---|---|---|---|---|---|
| Weapon | `1976` | Queen's Whip | 65 | Hydra `4035` ×2 | Turtle General `4305`, Doppelganger `4142` |
| Shield | `2115` | Valkyrja's Shield | 65 | Thara Frog `4058` | Golden Thief Bug `4128` |
| Head top | `5171` | Valkyrie Helm (upper only)<br>others: Crown `5165` |  | Orc Hero `4143` | Orc Hero `4143` |
| Head mid | `2202` | Sunglasses |  |  | Pharaoh `4148` |
| Head low | `2265` | Gangster Mask |  |  |  |
| Armor | `2357` | Valkyrian Armor (upper only)<br>others: Formal Suit `2320` | 1 | Marc `4105` | Tao Gunka `4302` |
| Garment | `2524` | Valkyrian Manteau (upper only)<br>others: Muffler `2504` | 1 | Raydric `4133` | Assassin Cross `4359` |
| Shoes | `2410` | Sleipnir | 94 |  | no slot → Eddga `4123` on Valkyrian Shoes `2421` |
| Accessory 1 | `2629` | Megingjard | 94 |  | no slot → Ifrit `4430` on Clip `2607` |
| Accessory 2 | `2630` | Brisingamen | 94 |  | no slot → Osiris `4144` on Rosary `2626` |

Other weapons: Rante Whip `1957`, Chemeti Whip `1964`, Composite Bow `1705`

Whole set (same order as the table), +10 where refinable, MVP cards inserted:
```
@item2 1976 1 1 10 0 4305 4142 0 0
@item2 2115 1 1 10 0 4128 0 0 0
@item2 5171 1 1 10 0 4143 0 0 0
@item2 2202 1 1 0 0 4148 0 0 0
@item2 2265 1 1 0 0 0 0 0 0
@item2 2357 1 1 10 0 4302 0 0 0
@item2 2524 1 1 10 0 4359 0 0 0
@item2 2410 1 1 0 0 0 0 0 0
@item2 2629 1 1 0 0 0 0 0 0
@item2 2630 1 1 0 0 0 0 0 0
```

Optional card swaps (slotted item + MVP card instead of the no-slot item):
```
@item2 2421 1 1 10 0 4123 0 0 0
@item2 2607 1 1 0 0 4430 0 0 0
@item2 2626 1 1 0 0 4144 0 0 0
```

#### Priest line

Job IDs: `8` Priest · `4009` High Priest · `4031` Baby Priest

| Slot | ID | Item | Min lv | Card | MVP card |
|---|---|---|---|---|---|
| Weapon | `1505` | Mace | 2 |  | Dracula `4134` |
| Shield | `2115` | Valkyrja's Shield | 65 | Thara Frog `4058` | Maya `4146` |
| Head top | `5171` | Valkyrie Helm (upper only)<br>others: Crown `5165` |  | Kiel-D-01 `4403` | Kiel-D-01 `4403` |
| Head mid | `2202` | Sunglasses |  |  | Vesper `4374` |
| Head low | `2265` | Gangster Mask |  |  |  |
| Armor | `2357` | Valkyrian Armor (upper only)<br>others: Formal Suit `2320` | 1 | Marc `4105` | Tao Gunka `4302` |
| Garment | `2524` | Valkyrian Manteau (upper only)<br>others: Muffler `2504` | 1 | Raydric `4133` | Assassin Cross `4359` |
| Shoes | `2410` | Sleipnir | 94 |  | no slot → Fallen Bishop Hibram `4441` on Valkyrian Shoes `2421` |
| Accessory 1 | `2630` | Brisingamen | 94 |  | no slot → Berzebub `4145` on Clip `2607` |
| Accessory 2 | `2626` | Rosary | 90 | Phen `4077` | Osiris `4144` |

Other weapons: Bible `1551`

Whole set (same order as the table), +10 where refinable, MVP cards inserted:
```
@item2 1505 1 1 10 0 4134 0 0 0
@item2 2115 1 1 10 0 4146 0 0 0
@item2 5171 1 1 10 0 4403 0 0 0
@item2 2202 1 1 0 0 4374 0 0 0
@item2 2265 1 1 0 0 0 0 0 0
@item2 2357 1 1 10 0 4302 0 0 0
@item2 2524 1 1 10 0 4359 0 0 0
@item2 2410 1 1 0 0 0 0 0 0
@item2 2630 1 1 0 0 0 0 0 0
@item2 2626 1 1 0 0 4144 0 0 0
```

Optional card swaps (slotted item + MVP card instead of the no-slot item):
```
@item2 2421 1 1 10 0 4441 0 0 0
@item2 2607 1 1 0 0 4145 0 0 0
```

#### Monk line

Job IDs: `15` Monk · `4016` Champion · `4038` Baby Monk

| Slot | ID | Item | Min lv | Card | MVP card |
|---|---|---|---|---|---|
| Weapon | `1816` | Berserk | 36 | Hydra `4035` | Turtle General `4305` |
| Shield | `2115` | Valkyrja's Shield | 65 | Thara Frog `4058` | Golden Thief Bug `4128` |
| Head top | `5171` | Valkyrie Helm (upper only)<br>others: Crown `5165` |  | Orc Hero `4143` | Orc Hero `4143` |
| Head mid | `2202` | Sunglasses |  |  | Pharaoh `4148` |
| Head low | `2265` | Gangster Mask |  |  |  |
| Armor | `2357` | Valkyrian Armor (upper only)<br>others: Formal Suit `2320` | 1 | Marc `4105` | Tao Gunka `4302` |
| Garment | `2524` | Valkyrian Manteau (upper only)<br>others: Muffler `2504` | 1 | Raydric `4133` | Assassin Cross `4359` |
| Shoes | `2410` | Sleipnir | 94 |  | no slot → Eddga `4123` on Valkyrian Shoes `2421` |
| Accessory 1 | `2629` | Megingjard | 94 |  | no slot → Ifrit `4430` on Clip `2607` |
| Accessory 2 | `2630` | Brisingamen | 94 |  | no slot → Osiris `4144` on Rosary `2626` |

Other weapons: Waghnak `1802`, Hatii Claw `1815`

Whole set (same order as the table), +10 where refinable, MVP cards inserted:
```
@item2 1816 1 1 10 0 4305 0 0 0
@item2 2115 1 1 10 0 4128 0 0 0
@item2 5171 1 1 10 0 4143 0 0 0
@item2 2202 1 1 0 0 4148 0 0 0
@item2 2265 1 1 0 0 0 0 0 0
@item2 2357 1 1 10 0 4302 0 0 0
@item2 2524 1 1 10 0 4359 0 0 0
@item2 2410 1 1 0 0 0 0 0 0
@item2 2629 1 1 0 0 0 0 0 0
@item2 2630 1 1 0 0 0 0 0 0
```

Optional card swaps (slotted item + MVP card instead of the no-slot item):
```
@item2 2421 1 1 10 0 4123 0 0 0
@item2 2607 1 1 0 0 4430 0 0 0
@item2 2626 1 1 0 0 4144 0 0 0
```

#### Blacksmith line

Job IDs: `10` Blacksmith · `4011` Whitesmith · `4033` Baby Blacksmith

| Slot | ID | Item | Min lv | Card | MVP card |
|---|---|---|---|---|---|
| Weapon | `1530` | Mjolnir | 95 |  |  |
| Shield | `2115` | Valkyrja's Shield | 65 | Thara Frog `4058` | Golden Thief Bug `4128` |
| Head top | `5171` | Valkyrie Helm (upper only)<br>others: Crown `5165` |  | Orc Hero `4143` | Orc Hero `4143` |
| Head mid | `2202` | Sunglasses |  |  | Pharaoh `4148` |
| Head low | `2265` | Gangster Mask |  |  |  |
| Armor | `2357` | Valkyrian Armor (upper only)<br>others: Formal Suit `2320` | 1 | Marc `4105` | Tao Gunka `4302` |
| Garment | `2524` | Valkyrian Manteau (upper only)<br>others: Muffler `2504` | 1 | Raydric `4133` | Assassin Cross `4359` |
| Shoes | `2410` | Sleipnir | 94 |  | no slot → Eddga `4123` on Valkyrian Shoes `2421` |
| Accessory 1 | `2629` | Megingjard | 94 |  | no slot → Ifrit `4430` on Clip `2607` |
| Accessory 2 | `2630` | Brisingamen | 94 |  | no slot → Osiris `4144` on Rosary `2626` |

Other weapons: Bloody Axe `1363`, Guillotine `1369`, Tomahawk `1314`

Whole set (same order as the table), +10 where refinable, MVP cards inserted:
```
@item2 1530 1 1 0 0 0 0 0 0
@item2 2115 1 1 10 0 4128 0 0 0
@item2 5171 1 1 10 0 4143 0 0 0
@item2 2202 1 1 0 0 4148 0 0 0
@item2 2265 1 1 0 0 0 0 0 0
@item2 2357 1 1 10 0 4302 0 0 0
@item2 2524 1 1 10 0 4359 0 0 0
@item2 2410 1 1 0 0 0 0 0 0
@item2 2629 1 1 0 0 0 0 0 0
@item2 2630 1 1 0 0 0 0 0 0
```

Optional card swaps (slotted item + MVP card instead of the no-slot item):
```
@item2 2421 1 1 10 0 4123 0 0 0
@item2 2607 1 1 0 0 4430 0 0 0
@item2 2626 1 1 0 0 4144 0 0 0
```

#### Alchemist line

Job IDs: `18` Alchemist · `4019` Creator · `4041` Baby Alchemist

| Slot | ID | Item | Min lv | Card | MVP card |
|---|---|---|---|---|---|
| Weapon | `1517` | Sword Mace | 27 | Hydra `4035` | Turtle General `4305` |
| Shield | `2115` | Valkyrja's Shield | 65 | Thara Frog `4058` | Golden Thief Bug `4128` |
| Head top | `5171` | Valkyrie Helm (upper only)<br>others: Crown `5165` |  | Orc Hero `4143` | Orc Hero `4143` |
| Head mid | `2202` | Sunglasses |  |  | Pharaoh `4148` |
| Head low | `2265` | Gangster Mask |  |  |  |
| Armor | `2357` | Valkyrian Armor (upper only)<br>others: Formal Suit `2320` | 1 | Marc `4105` | Tao Gunka `4302` |
| Garment | `2524` | Valkyrian Manteau (upper only)<br>others: Muffler `2504` | 1 | Raydric `4133` | Assassin Cross `4359` |
| Shoes | `2410` | Sleipnir | 94 |  | no slot → Eddga `4123` on Valkyrian Shoes `2421` |
| Accessory 1 | `2629` | Megingjard | 94 |  | no slot → Ifrit `4430` on Clip `2607` |
| Accessory 2 | `2630` | Brisingamen | 94 |  | no slot → Osiris `4144` on Rosary `2626` |

Other weapons: Mace `1505`, Tomahawk `1314`

Whole set (same order as the table), +10 where refinable, MVP cards inserted:
```
@item2 1517 1 1 10 0 4305 0 0 0
@item2 2115 1 1 10 0 4128 0 0 0
@item2 5171 1 1 10 0 4143 0 0 0
@item2 2202 1 1 0 0 4148 0 0 0
@item2 2265 1 1 0 0 0 0 0 0
@item2 2357 1 1 10 0 4302 0 0 0
@item2 2524 1 1 10 0 4359 0 0 0
@item2 2410 1 1 0 0 0 0 0 0
@item2 2629 1 1 0 0 0 0 0 0
@item2 2630 1 1 0 0 0 0 0 0
```

Optional card swaps (slotted item + MVP card instead of the no-slot item):
```
@item2 2421 1 1 10 0 4123 0 0 0
@item2 2607 1 1 0 0 4430 0 0 0
@item2 2626 1 1 0 0 4144 0 0 0
```

#### Assassin line

Job IDs: `12` Assassin · `4013` Assassin Cross · `4035` Baby Assassin

| Slot | ID | Item | Min lv | Card | MVP card |
|---|---|---|---|---|---|
| Weapon | `1266` | Infiltrator | 75 | Hydra `4035` | Turtle General `4305` |
| Head top | `5171` | Valkyrie Helm (upper only)<br>others: Crown `5165` |  | Orc Hero `4143` | Orc Hero `4143` |
| Head mid | `2202` | Sunglasses |  |  | Pharaoh `4148` |
| Head low | `2265` | Gangster Mask |  |  |  |
| Armor | `2357` | Valkyrian Armor (upper only)<br>others: Formal Suit `2320` | 1 | Marc `4105` | Tao Gunka `4302` |
| Garment | `2524` | Valkyrian Manteau (upper only)<br>others: Muffler `2504` | 1 | Raydric `4133` | Assassin Cross `4359` |
| Shoes | `2410` | Sleipnir | 94 |  | no slot → Eddga `4123` on Valkyrian Shoes `2421` |
| Accessory 1 | `2629` | Megingjard | 94 |  | no slot → Ifrit `4430` on Clip `2607` |
| Accessory 2 | `2630` | Brisingamen | 94 |  | no slot → Osiris `4144` on Rosary `2626` |

Other weapons: Jur `1251`, Katar of Frozen Icicle `1275`, Bloody Roar `1265`

Whole set (same order as the table), +10 where refinable, MVP cards inserted:
```
@item2 1266 1 1 10 0 4305 0 0 0
@item2 5171 1 1 10 0 4143 0 0 0
@item2 2202 1 1 0 0 4148 0 0 0
@item2 2265 1 1 0 0 0 0 0 0
@item2 2357 1 1 10 0 4302 0 0 0
@item2 2524 1 1 10 0 4359 0 0 0
@item2 2410 1 1 0 0 0 0 0 0
@item2 2629 1 1 0 0 0 0 0 0
@item2 2630 1 1 0 0 0 0 0 0
```

Optional card swaps (slotted item + MVP card instead of the no-slot item):
```
@item2 2421 1 1 10 0 4123 0 0 0
@item2 2607 1 1 0 0 4430 0 0 0
@item2 2626 1 1 0 0 4144 0 0 0
```

#### Rogue line

Job IDs: `17` Rogue · `4018` Stalker · `4040` Baby Rogue

| Slot | ID | Item | Min lv | Card | MVP card |
|---|---|---|---|---|---|
| Weapon | `1220` | Gladius | 24 | Hydra `4035` ×3 | Turtle General `4305`, Doppelganger `4142`, Drake `4137` |
| Shield | `2115` | Valkyrja's Shield | 65 | Thara Frog `4058` | Golden Thief Bug `4128` |
| Head top | `5171` | Valkyrie Helm (upper only)<br>others: Crown `5165` |  | Orc Hero `4143` | Orc Hero `4143` |
| Head mid | `2202` | Sunglasses |  |  | Pharaoh `4148` |
| Head low | `2265` | Gangster Mask |  |  |  |
| Armor | `2357` | Valkyrian Armor (upper only)<br>others: Formal Suit `2320` | 1 | Marc `4105` | Tao Gunka `4302` |
| Garment | `2524` | Valkyrian Manteau (upper only)<br>others: Muffler `2504` | 1 | Raydric `4133` | Assassin Cross `4359` |
| Shoes | `2410` | Sleipnir | 94 |  | no slot → Eddga `4123` on Valkyrian Shoes `2421` |
| Accessory 1 | `2629` | Megingjard | 94 |  | no slot → Ifrit `4430` on Clip `2607` |
| Accessory 2 | `2630` | Brisingamen | 94 |  | no slot → Osiris `4144` on Rosary `2626` |

Other weapons: Combat Knife `1228`, Composite Bow `1705`

Whole set (same order as the table), +10 where refinable, MVP cards inserted:
```
@item2 1220 1 1 10 0 4305 4142 4137 0
@item2 2115 1 1 10 0 4128 0 0 0
@item2 5171 1 1 10 0 4143 0 0 0
@item2 2202 1 1 0 0 4148 0 0 0
@item2 2265 1 1 0 0 0 0 0 0
@item2 2357 1 1 10 0 4302 0 0 0
@item2 2524 1 1 10 0 4359 0 0 0
@item2 2410 1 1 0 0 0 0 0 0
@item2 2629 1 1 0 0 0 0 0 0
@item2 2630 1 1 0 0 0 0 0 0
```

Optional card swaps (slotted item + MVP card instead of the no-slot item):
```
@item2 2421 1 1 10 0 4123 0 0 0
@item2 2607 1 1 0 0 4430 0 0 0
@item2 2626 1 1 0 0 4144 0 0 0
```

#### Super Novice

Job IDs: `23` Super Novice · `4045` Super Baby

| Slot | ID | Item | Min lv | Card | MVP card |
|---|---|---|---|---|---|
| Weapon | `1505` | Mace | 2 | Hydra `4035` ×4 | Turtle General `4305`, Doppelganger `4142`, Drake `4137`, Baphomet `4147` |
| Shield | `2113` | Novice Shield | 40 | Thara Frog `4058` | Golden Thief Bug `4128` |
| Head top | `5125` | Angel's Kiss | 50 | Orc Hero `4143` | Orc Hero `4143` |
| Head mid | `2202` | Sunglasses |  |  | Pharaoh `4148` |
| Head low | `2265` | Gangster Mask |  |  |  |
| Armor | `2355` | Angelic Protection | 40 | Marc `4105` | Tao Gunka `4302` |
| Garment | `2512` | Novice Manteau | 40 | Raydric `4133` | Assassin Cross `4359` |
| Shoes | `2410` | Sleipnir | 94 |  |  |
| Accessory 1 | `2629` | Megingjard | 94 |  | no slot → Ifrit `4430` on Clip `2607` |
| Accessory 2 | `2630` | Brisingamen | 94 |  |  |

Other weapons: Blade `1108`

Whole set (same order as the table), +10 where refinable, MVP cards inserted:
```
@item2 1505 1 1 10 0 4305 4142 4137 4147
@item2 2113 1 1 10 0 4128 0 0 0
@item2 5125 1 1 10 0 4143 0 0 0
@item2 2202 1 1 0 0 4148 0 0 0
@item2 2265 1 1 0 0 0 0 0 0
@item2 2355 1 1 10 0 4302 0 0 0
@item2 2512 1 1 10 0 4359 0 0 0
@item2 2410 1 1 0 0 0 0 0 0
@item2 2629 1 1 0 0 0 0 0 0
@item2 2630 1 1 0 0 0 0 0 0
```

Optional card swaps (slotted item + MVP card instead of the no-slot item):
```
@item2 2607 1 1 0 0 4430 0 0 0
```

#### Gunslinger

Job IDs: `24` Gunslinger

| Slot | ID | Item | Min lv | Card | MVP card |
|---|---|---|---|---|---|
| Weapon | `13152` | Cyclone | 24 | Hydra `4035` ×2 | Turtle General `4305`, Doppelganger `4142` |
| Head top | `2280` | Sakkat |  |  | no slot → Orc Hero `4143` on Crown `5165` |
| Head mid | `2202` | Sunglasses |  |  | Pharaoh `4148` |
| Head low | `2265` | Gangster Mask |  |  |  |
| Armor | `2382` | Elite Shooter Suit | 80 | Marc `4105` | Tao Gunka `4302` |
| Garment | `2540` | Sheriff's Manteau | 80 | Raydric `4133` | Assassin Cross `4359` |
| Shoes | `2410` | Sleipnir | 94 |  | no slot → Eddga `4123` on Boots `2406` |
| Accessory 1 | `2629` | Megingjard | 94 |  | no slot → Ifrit `4430` on Clip `2607` |
| Accessory 2 | `2630` | Brisingamen | 94 |  | no slot → Osiris `4144` on Rosary `2626` |

Other weapons: Lever Action Rifle `13170`, Garrison `13105`

Whole set (same order as the table), +10 where refinable, MVP cards inserted:
```
@item2 13152 1 1 10 0 4305 4142 0 0
@item2 2280 1 1 10 0 0 0 0 0
@item2 2202 1 1 0 0 4148 0 0 0
@item2 2265 1 1 0 0 0 0 0 0
@item2 2382 1 1 10 0 4302 0 0 0
@item2 2540 1 1 10 0 4359 0 0 0
@item2 2410 1 1 0 0 0 0 0 0
@item2 2629 1 1 0 0 0 0 0 0
@item2 2630 1 1 0 0 0 0 0 0
```

Optional card swaps (slotted item + MVP card instead of the no-slot item):
```
@item2 5165 1 1 10 0 4143 0 0 0
@item2 2406 1 1 10 0 4123 0 0 0
@item2 2607 1 1 0 0 4430 0 0 0
@item2 2626 1 1 0 0 4144 0 0 0
```

#### Ninja

Job IDs: `25` Ninja

| Slot | ID | Item | Min lv | Card | MVP card |
|---|---|---|---|---|---|
| Weapon | `13303` | Huuma Blaze Shuriken | 55 |  |  |
| Head top | `2280` | Sakkat |  |  | no slot → Orc Hero `4143` on Crown `5165` |
| Head mid | `2202` | Sunglasses |  |  | Pharaoh `4148` |
| Head low | `2265` | Gangster Mask |  |  |  |
| Armor | `2378` | Assassin Robe | 80 | Marc `4105` | Tao Gunka `4302` |
| Garment | `2538` | Captain's Manteau | 80 | Raydric `4133` | Assassin Cross `4359` |
| Shoes | `2410` | Sleipnir | 94 |  |  |
| Accessory 1 | `2629` | Megingjard | 94 |  | no slot → Ifrit `4430` on Clip `2607` |
| Accessory 2 | `2630` | Brisingamen | 94 |  | no slot → Osiris `4144` on Rosary `2626` |

Other weapons: Asura `13011`, Murasame `13013`

Whole set (same order as the table), +10 where refinable, MVP cards inserted:
```
@item2 13303 1 1 10 0 0 0 0 0
@item2 2280 1 1 10 0 0 0 0 0
@item2 2202 1 1 0 0 4148 0 0 0
@item2 2265 1 1 0 0 0 0 0 0
@item2 2378 1 1 10 0 4302 0 0 0
@item2 2538 1 1 10 0 4359 0 0 0
@item2 2410 1 1 0 0 0 0 0 0
@item2 2629 1 1 0 0 0 0 0 0
@item2 2630 1 1 0 0 0 0 0 0
```

Optional card swaps (slotted item + MVP card instead of the no-slot item):
```
@item2 5165 1 1 10 0 4143 0 0 0
@item2 2607 1 1 0 0 4430 0 0 0
@item2 2626 1 1 0 0 4144 0 0 0
```

#### Taekwon

Job IDs: `4046` Taekwon

| Slot | ID | Item | Min lv | Card | MVP card |
|---|---|---|---|---|---|
| Weapon | — | (fists / no weapon) | | |
| Shield | `2115` | Valkyrja's Shield | 65 | Thara Frog `4058` | Golden Thief Bug `4128` |
| Head top | `5161` | Spiky Band | 50 | Orc Hero `4143` | Orc Hero `4143` |
| Head mid | `2202` | Sunglasses |  |  | Pharaoh `4148` |
| Head low | `2265` | Gangster Mask |  |  |  |
| Armor | `2376` | Assaulter Plate | 80 | Marc `4105` | Tao Gunka `4302` |
| Garment | `2538` | Captain's Manteau | 80 | Raydric `4133` | Assassin Cross `4359` |
| Shoes | `2410` | Sleipnir | 94 |  | no slot → Eddga `4123` on Boots `2406` |
| Accessory 1 | `2629` | Megingjard | 94 |  | no slot → Ifrit `4430` on Clip `2607` |
| Accessory 2 | `2630` | Brisingamen | 94 |  | no slot → Osiris `4144` on Rosary `2626` |

Whole set (same order as the table), +10 where refinable, MVP cards inserted:
```
@item2 2115 1 1 10 0 4128 0 0 0
@item2 5161 1 1 10 0 4143 0 0 0
@item2 2202 1 1 0 0 4148 0 0 0
@item2 2265 1 1 0 0 0 0 0 0
@item2 2376 1 1 10 0 4302 0 0 0
@item2 2538 1 1 10 0 4359 0 0 0
@item2 2410 1 1 0 0 0 0 0 0
@item2 2629 1 1 0 0 0 0 0 0
@item2 2630 1 1 0 0 0 0 0 0
```

Optional card swaps (slotted item + MVP card instead of the no-slot item):
```
@item2 2406 1 1 10 0 4123 0 0 0
@item2 2607 1 1 0 0 4430 0 0 0
@item2 2626 1 1 0 0 4144 0 0 0
```

#### Star Gladiator

Job IDs: `4047` Star Gladiator

| Slot | ID | Item | Min lv | Card | MVP card |
|---|---|---|---|---|---|
| Weapon | — | (fists / no weapon) | | |
| Shield | `2115` | Valkyrja's Shield | 65 | Thara Frog `4058` | Golden Thief Bug `4128` |
| Head top | `5161` | Spiky Band | 50 | Orc Hero `4143` | Orc Hero `4143` |
| Head mid | `2202` | Sunglasses |  |  | Pharaoh `4148` |
| Head low | `2265` | Gangster Mask |  |  |  |
| Armor | `2376` | Assaulter Plate | 80 | Marc `4105` | Tao Gunka `4302` |
| Garment | `2538` | Captain's Manteau | 80 | Raydric `4133` | Assassin Cross `4359` |
| Shoes | `2410` | Sleipnir | 94 |  | no slot → Eddga `4123` on Boots `2406` |
| Accessory 1 | `2629` | Megingjard | 94 |  | no slot → Ifrit `4430` on Clip `2607` |
| Accessory 2 | `2630` | Brisingamen | 94 |  | no slot → Osiris `4144` on Rosary `2626` |

Whole set (same order as the table), +10 where refinable, MVP cards inserted:
```
@item2 2115 1 1 10 0 4128 0 0 0
@item2 5161 1 1 10 0 4143 0 0 0
@item2 2202 1 1 0 0 4148 0 0 0
@item2 2265 1 1 0 0 0 0 0 0
@item2 2376 1 1 10 0 4302 0 0 0
@item2 2538 1 1 10 0 4359 0 0 0
@item2 2410 1 1 0 0 0 0 0 0
@item2 2629 1 1 0 0 0 0 0 0
@item2 2630 1 1 0 0 0 0 0 0
```

Optional card swaps (slotted item + MVP card instead of the no-slot item):
```
@item2 2406 1 1 10 0 4123 0 0 0
@item2 2607 1 1 0 0 4430 0 0 0
@item2 2626 1 1 0 0 4144 0 0 0
```

#### Soul Linker

Job IDs: `4049` Soul Linker

| Slot | ID | Item | Min lv | Card | MVP card |
|---|---|---|---|---|---|
| Weapon | `1618` | Survivor's Rod | 24 |  | Dracula `4134` |
| Shield | `2115` | Valkyrja's Shield | 65 | Thara Frog `4058` | Maya `4146` |
| Head top | `5353` | Hat of the Sun God |  | Kiel-D-01 `4403` | Kiel-D-01 `4403` |
| Head mid | `2202` | Sunglasses |  |  | Vesper `4374` |
| Head low | `2265` | Gangster Mask |  |  |  |
| Armor | `2379` | Warlock's Battle Robe | 80 | Marc `4105` | Tao Gunka `4302` |
| Garment | `2515` | Eagle Wing | 85 | Raydric `4133` | Assassin Cross `4359` |
| Shoes | `2410` | Sleipnir | 94 |  |  |
| Accessory 1 | `2630` | Brisingamen | 94 |  | no slot → Berzebub `4145` on Clip `2607` |
| Accessory 2 | `2626` | Rosary | 90 | Phen `4077` | Osiris `4144` |

Other weapons: Rod `1602`

Whole set (same order as the table), +10 where refinable, MVP cards inserted:
```
@item2 1618 1 1 10 0 4134 0 0 0
@item2 2115 1 1 10 0 4146 0 0 0
@item2 5353 1 1 10 0 4403 0 0 0
@item2 2202 1 1 0 0 4374 0 0 0
@item2 2265 1 1 0 0 0 0 0 0
@item2 2379 1 1 10 0 4302 0 0 0
@item2 2515 1 1 10 0 4359 0 0 0
@item2 2410 1 1 0 0 0 0 0 0
@item2 2630 1 1 0 0 0 0 0 0
@item2 2626 1 1 0 0 4144 0 0 0
```

Optional card swaps (slotted item + MVP card instead of the no-slot item):
```
@item2 2607 1 1 0 0 4145 0 0 0
```

### Renewal: 3rd jobs (renewal server, level 130–200)

The same set works for the normal, transcendent and baby versions. The Temporal Circlet is class-specific.

#### Rune Knight

Job IDs: `4054` Rune Knight · `4060` Rune Knight (trans) · `4096` Baby Rune Knight

| Slot | ID | Item | Min lv | Card |
|---|---|---|---|---|
| Weapon | `21016` | Vicious Mind Two-Handed Sword | 160 |  |
| Head top | `19474` | Temporal Circlet (Rune Knight) | 170 |  |
| Head mid | `410010` | Eyes of Illusion | 100 |  |
| Head low | `19439` | Vicious Mind Aura | 170 |  |
| Armor | `15376` | Illusion Armor A-type | 130 |  |
| Garment | `20933` | Illusion Engine wing A-type | 130 |  |
| Shoes | `22196` | Illusion Leg A-type | 130 |  |
| Accessory 1 | `32207` | Illusion Booster R | 130 |  |
| Accessory 2 | `32208` | Illusion Booster L | 130 |  |

Other weapons: Dim Glacier Two-handed Sword `600030`

#### Royal Guard

Job IDs: `4066` Royal Guard · `4073` Royal Guard (trans) · `4102` Baby Royal Guard

| Slot | ID | Item | Min lv | Card |
|---|---|---|---|---|
| Weapon | `1400` | Vicious Mind Spear | 160 |  |
| Shield | `460004` | Illusion Shield I | 100 |  |
| Head top | `19475` | Temporal Circlet (Royal Guard) | 170 |  |
| Head mid | `410010` | Eyes of Illusion | 100 |  |
| Head low | `19439` | Vicious Mind Aura | 170 |  |
| Armor | `15376` | Illusion Armor A-type | 130 |  |
| Garment | `20933` | Illusion Engine wing A-type | 130 |  |
| Shoes | `22196` | Illusion Leg A-type | 130 |  |
| Accessory 1 | `32207` | Illusion Booster R | 130 |  |
| Accessory 2 | `32208` | Illusion Booster L | 130 |  |

Other weapons: Dim Glacier Spear `530034`

#### Warlock

Job IDs: `4055` Warlock · `4061` Warlock (trans) · `4097` Baby Warlock

| Slot | ID | Item | Min lv | Card |
|---|---|---|---|---|
| Weapon | `2026` | Vicious Mind Staff | 160 |  |
| Head top | `19482` | Temporal Circlet (Warlock) | 170 |  |
| Head mid | `410010` | Eyes of Illusion | 100 |  |
| Head low | `19439` | Vicious Mind Aura | 170 |  |
| Armor | `15377` | Illusion Armor B-type | 130 |  |
| Garment | `20934` | Illusion Engine wing B-type | 130 |  |
| Shoes | `22197` | Illusion Leg B-type | 130 |  |
| Accessory 1 | `32209` | Illusion Battle chip R | 130 |  |
| Accessory 2 | `32210` | Illusion Battle chip L | 130 |  |

Other weapons: Dim Glacier Staff `640034`

#### Sorcerer

Job IDs: `4067` Sorcerer · `4074` Sorcerer (trans) · `4103` Baby Sorcerer

| Slot | ID | Item | Min lv | Card |
|---|---|---|---|---|
| Weapon | `28605` | Vicious Mind Book | 160 |  |
| Shield | `460004` | Illusion Shield I | 100 |  |
| Head top | `19483` | Temporal Circlet (Sorcerer) | 170 |  |
| Head mid | `410010` | Eyes of Illusion | 100 |  |
| Head low | `19439` | Vicious Mind Aura | 170 |  |
| Armor | `15377` | Illusion Armor B-type | 130 |  |
| Garment | `20934` | Illusion Engine wing B-type | 130 |  |
| Shoes | `22197` | Illusion Leg B-type | 130 |  |
| Accessory 1 | `32209` | Illusion Battle chip R | 130 |  |
| Accessory 2 | `32210` | Illusion Battle chip L | 130 |  |

Other weapons: Dim Glacier Book `540056`

#### Ranger

Job IDs: `4056` Ranger · `4062` Ranger (trans) · `4098` Baby Ranger

| Slot | ID | Item | Min lv | Card |
|---|---|---|---|---|
| Weapon | `18121` | Vicious Mind Bow | 160 |  |
| Head top | `19484` | Temporal Circlet (Ranger) | 170 |  |
| Head mid | `410010` | Eyes of Illusion | 100 |  |
| Head low | `19439` | Vicious Mind Aura | 170 |  |
| Armor | `15376` | Illusion Armor A-type | 130 |  |
| Garment | `20933` | Illusion Engine wing A-type | 130 |  |
| Shoes | `22196` | Illusion Leg A-type | 130 |  |
| Accessory 1 | `32207` | Illusion Booster R | 130 |  |
| Accessory 2 | `32208` | Illusion Booster L | 130 |  |

Other weapons: Dim Glacier Bow `700059`

#### Minstrel (male)

Job IDs: `4068` Minstrel · `4075` Minstrel (trans) · `4104` Baby Minstrel

| Slot | ID | Item | Min lv | Card |
|---|---|---|---|---|
| Weapon | `1900` | Vicious Mind Violin | 160 |  |
| Shield | `460004` | Illusion Shield I | 100 |  |
| Head top | `19485` | Temporal Circlet (Wanderer & Minstrel) | 170 |  |
| Head mid | `410010` | Eyes of Illusion | 100 |  |
| Head low | `19439` | Vicious Mind Aura | 170 |  |
| Armor | `15376` | Illusion Armor A-type | 130 |  |
| Garment | `20933` | Illusion Engine wing A-type | 130 |  |
| Shoes | `22196` | Illusion Leg A-type | 130 |  |
| Accessory 1 | `32207` | Illusion Booster R | 130 |  |
| Accessory 2 | `32208` | Illusion Booster L | 130 |  |

Other weapons: Dim Glacier Violin `570032`

#### Wanderer (female)

Job IDs: `4069` Wanderer · `4076` Wanderer (trans) · `4105` Baby Wanderer

| Slot | ID | Item | Min lv | Card |
|---|---|---|---|---|
| Weapon | `1996` | Vicious Mind Wire | 160 |  |
| Shield | `460004` | Illusion Shield I | 100 |  |
| Head top | `19485` | Temporal Circlet (Wanderer & Minstrel) | 170 |  |
| Head mid | `410010` | Eyes of Illusion | 100 |  |
| Head low | `19439` | Vicious Mind Aura | 170 |  |
| Armor | `15376` | Illusion Armor A-type | 130 |  |
| Garment | `20933` | Illusion Engine wing A-type | 130 |  |
| Shoes | `22196` | Illusion Leg A-type | 130 |  |
| Accessory 1 | `32207` | Illusion Booster R | 130 |  |
| Accessory 2 | `32208` | Illusion Booster L | 130 |  |

Other weapons: Dim Glacier Whip `580033`

#### Arch Bishop

Job IDs: `4057` Arch Bishop · `4063` Arch Bishop (trans) · `4099` Baby Arch Bishop

| Slot | ID | Item | Min lv | Card |
|---|---|---|---|---|
| Weapon | `1600` | Vicious Mind Rod | 160 |  |
| Shield | `460004` | Illusion Shield I | 100 |  |
| Head top | `19480` | Temporal Circlet (Archbishop) | 170 |  |
| Head mid | `410010` | Eyes of Illusion | 100 |  |
| Head low | `19439` | Vicious Mind Aura | 170 |  |
| Armor | `15377` | Illusion Armor B-type | 130 |  |
| Garment | `20934` | Illusion Engine wing B-type | 130 |  |
| Shoes | `22197` | Illusion Leg B-type | 130 |  |
| Accessory 1 | `32209` | Illusion Battle chip R | 130 |  |
| Accessory 2 | `32210` | Illusion Battle chip L | 130 |  |

Other weapons: Dim Glacier Staff `640034`

#### Sura

Job IDs: `4070` Sura · `4077` Sura (trans) · `4106` Baby Sura

| Slot | ID | Item | Min lv | Card |
|---|---|---|---|---|
| Weapon | `1800` | Vicious Mind Knuckle | 160 |  |
| Shield | `460004` | Illusion Shield I | 100 |  |
| Head top | `19481` | Temporal Circlet (Sura) | 170 |  |
| Head mid | `410010` | Eyes of Illusion | 100 |  |
| Head low | `19439` | Vicious Mind Aura | 170 |  |
| Armor | `15376` | Illusion Armor A-type | 130 |  |
| Garment | `20933` | Illusion Engine wing A-type | 130 |  |
| Shoes | `22196` | Illusion Leg A-type | 130 |  |
| Accessory 1 | `32207` | Illusion Booster R | 130 |  |
| Accessory 2 | `32208` | Illusion Booster L | 130 |  |

Other weapons: Dim Glacier Knuckle `560037`

#### Mechanic

Job IDs: `4058` Mechanic · `4064` Mechanic (trans) · `4100` Baby Mechanic

| Slot | ID | Item | Min lv | Card |
|---|---|---|---|---|
| Weapon | `28107` | Vicious Mind Two-Handed Axe | 160 |  |
| Head top | `19476` | Temporal Circlet (Mechanic) | 170 |  |
| Head mid | `410010` | Eyes of Illusion | 100 |  |
| Head low | `19439` | Vicious Mind Aura | 170 |  |
| Armor | `15376` | Illusion Armor A-type | 130 |  |
| Garment | `20933` | Illusion Engine wing A-type | 130 |  |
| Shoes | `22196` | Illusion Leg A-type | 130 |  |
| Accessory 1 | `32207` | Illusion Booster R | 130 |  |
| Accessory 2 | `32208` | Illusion Booster L | 130 |  |

Other weapons: Dim Glacier Mechanic Axe `620019`

#### Genetic

Job IDs: `4071` Genetic · `4078` Genetic (trans) · `4107` Baby Genetic

| Slot | ID | Item | Min lv | Card |
|---|---|---|---|---|
| Weapon | `16041` | Vicious Mind Mace | 160 |  |
| Shield | `460004` | Illusion Shield I | 100 |  |
| Head top | `19477` | Temporal Circlet (Genetic) | 170 |  |
| Head mid | `410010` | Eyes of Illusion | 100 |  |
| Head low | `19439` | Vicious Mind Aura | 170 |  |
| Armor | `15376` | Illusion Armor A-type | 130 |  |
| Garment | `20933` | Illusion Engine wing A-type | 130 |  |
| Shoes | `22196` | Illusion Leg A-type | 130 |  |
| Accessory 1 | `32207` | Illusion Booster R | 130 |  |
| Accessory 2 | `32208` | Illusion Booster L | 130 |  |

Other weapons: Dim Glacier Mace `590047`

#### Guillotine Cross

Job IDs: `4059` Guillotine Cross · `4065` Guillotine Cross (trans) · `4101` Baby Guillotine Cross

| Slot | ID | Item | Min lv | Card |
|---|---|---|---|---|
| Weapon | `28008` | Vicious Mind Katar | 160 |  |
| Head top | `19478` | Temporal Circlet (Guillotine Cross) | 170 |  |
| Head mid | `410010` | Eyes of Illusion | 100 |  |
| Head low | `19439` | Vicious Mind Aura | 170 |  |
| Armor | `15376` | Illusion Armor A-type | 130 |  |
| Garment | `20933` | Illusion Engine wing A-type | 130 |  |
| Shoes | `22196` | Illusion Leg A-type | 130 |  |
| Accessory 1 | `32207` | Illusion Booster R | 130 |  |
| Accessory 2 | `32208` | Illusion Booster L | 130 |  |

Other weapons: Dim Glacier Katar `610041`

#### Shadow Chaser

Job IDs: `4072` Shadow Chaser · `4079` Shadow Chaser (trans) · `4108` Baby Shadow Chaser

| Slot | ID | Item | Min lv | Card |
|---|---|---|---|---|
| Weapon | `18121` | Vicious Mind Bow | 160 |  |
| Head top | `19479` | Temporal Circlet (Shadow Chaser) | 170 |  |
| Head mid | `410010` | Eyes of Illusion | 100 |  |
| Head low | `19439` | Vicious Mind Aura | 170 |  |
| Armor | `15376` | Illusion Armor A-type | 130 |  |
| Garment | `20933` | Illusion Engine wing A-type | 130 |  |
| Shoes | `22196` | Illusion Leg A-type | 130 |  |
| Accessory 1 | `32207` | Illusion Booster R | 130 |  |
| Accessory 2 | `32208` | Illusion Booster L | 130 |  |

Other weapons: Dim Glacier Rogue Knife `510075`

#### Super Novice (expanded)

Job IDs: `4190` Super Novice (expanded) · `4191` Super Baby (expanded)

| Slot | ID | Item | Min lv | Card |
|---|---|---|---|---|
| Weapon | `16041` | Vicious Mind Mace | 160 |  |
| Shield | `460004` | Illusion Shield I | 100 |  |
| Head top | `19491` | Temporal Circlet (Super Novice) | 170 |  |
| Head mid | `410010` | Eyes of Illusion | 100 |  |
| Head low | `19439` | Vicious Mind Aura | 170 |  |
| Armor | `15376` | Illusion Armor A-type | 130 |  |
| Garment | `20933` | Illusion Engine wing A-type | 130 |  |
| Shoes | `22196` | Illusion Leg A-type | 130 |  |
| Accessory 1 | `32207` | Illusion Booster R | 130 |  |
| Accessory 2 | `32208` | Illusion Booster L | 130 |  |

Other weapons: Dim Glacier Basic Sword `500055`

#### Star Emperor

Job IDs: `4239` Star Emperor · `4241` Baby Star Emperor

| Slot | ID | Item | Min lv | Card |
|---|---|---|---|---|
| Weapon | `28605` | Vicious Mind Book | 160 |  |
| Shield | `460004` | Illusion Shield I | 100 |  |
| Head top | `19486` | Temporal Circlet (Star Emperor) | 170 |  |
| Head mid | `410010` | Eyes of Illusion | 100 |  |
| Head low | `19439` | Vicious Mind Aura | 170 |  |
| Armor | `15376` | Illusion Armor A-type | 130 |  |
| Garment | `20933` | Illusion Engine wing A-type | 130 |  |
| Shoes | `22196` | Illusion Leg A-type | 130 |  |
| Accessory 1 | `32207` | Illusion Booster R | 130 |  |
| Accessory 2 | `32208` | Illusion Booster L | 130 |  |

Other weapons: Dim Glacier Book `540056`

#### Soul Reaper

Job IDs: `4240` Soul Reaper · `4242` Baby Soul Reaper

| Slot | ID | Item | Min lv | Card |
|---|---|---|---|---|
| Weapon | `2026` | Vicious Mind Staff | 160 |  |
| Head top | `19487` | Temporal Circlet (Soul Reaper) | 170 |  |
| Head mid | `410010` | Eyes of Illusion | 100 |  |
| Head low | `19439` | Vicious Mind Aura | 170 |  |
| Armor | `15377` | Illusion Armor B-type | 130 |  |
| Garment | `20934` | Illusion Engine wing B-type | 130 |  |
| Shoes | `22197` | Illusion Leg B-type | 130 |  |
| Accessory 1 | `32209` | Illusion Battle chip R | 130 |  |
| Accessory 2 | `32210` | Illusion Battle chip L | 130 |  |

Other weapons: Dim Glacier Staff `640034`

#### Rebellion

Job IDs: `4215` Rebellion · `4229` Baby Rebellion

| Slot | ID | Item | Min lv | Card |
|---|---|---|---|---|
| Weapon | `13128` | Vicious Mind Revolver | 160 |  |
| Head top | `19488` | Temporal Circlet (Rebellion) | 170 |  |
| Head mid | `410010` | Eyes of Illusion | 100 |  |
| Head low | `19439` | Vicious Mind Aura | 170 |  |
| Armor | `15376` | Illusion Armor A-type | 130 |  |
| Garment | `20933` | Illusion Engine wing A-type | 130 |  |
| Shoes | `22196` | Illusion Leg A-type | 130 |  |
| Accessory 1 | `32207` | Illusion Booster R | 130 |  |
| Accessory 2 | `32208` | Illusion Booster L | 130 |  |

Other weapons: Dim Glacier Rifle `810015`

#### Kagerou (male)

Job IDs: `4211` Kagerou · `4223` Baby Kagerou

| Slot | ID | Item | Min lv | Card |
|---|---|---|---|---|
| Weapon | `13328` | Vicious Mind Huuma Shuriken | 160 |  |
| Head top | `19490` | Temporal Circlet (Kagerou) | 170 |  |
| Head mid | `410010` | Eyes of Illusion | 100 |  |
| Head low | `19439` | Vicious Mind Aura | 170 |  |
| Armor | `15376` | Illusion Armor A-type | 130 |  |
| Garment | `20933` | Illusion Engine wing A-type | 130 |  |
| Shoes | `22196` | Illusion Leg A-type | 130 |  |
| Accessory 1 | `32207` | Illusion Booster R | 130 |  |
| Accessory 2 | `32208` | Illusion Booster L | 130 |  |

Other weapons: Dim Glacier Huuma Shuriken `650028`

#### Oboro (female)

Job IDs: `4212` Oboro · `4224` Baby Oboro

| Slot | ID | Item | Min lv | Card |
|---|---|---|---|---|
| Weapon | `13328` | Vicious Mind Huuma Shuriken | 160 |  |
| Head top | `19489` | Temporal Circlet (Oboro) | 170 |  |
| Head mid | `410010` | Eyes of Illusion | 100 |  |
| Head low | `19439` | Vicious Mind Aura | 170 |  |
| Armor | `15376` | Illusion Armor A-type | 130 |  |
| Garment | `20933` | Illusion Engine wing A-type | 130 |  |
| Shoes | `22196` | Illusion Leg A-type | 130 |  |
| Accessory 1 | `32207` | Illusion Booster R | 130 |  |
| Accessory 2 | `32208` | Illusion Booster L | 130 |  |

Other weapons: Dim Glacier Huuma Shuriken `650028`

#### Summoner (Doram)

Job IDs: `4218` Summoner · `4220` Baby Summoner

| Slot | ID | Item | Min lv | Card |
|---|---|---|---|---|
| Weapon | `550027` | Adulter Fides Foxtail Wand | 180 |  |
| Shield | `460004` | Illusion Shield I | 100 |  |
| Head top | `19492` | Temporal Circlet (Summoner) | 170 |  |
| Head mid | `410010` | Eyes of Illusion | 100 |  |
| Head low | `19439` | Vicious Mind Aura | 170 |  |
| Armor | `15377` | Illusion Armor B-type | 130 |  |
| Garment | `20934` | Illusion Engine wing B-type | 130 |  |
| Shoes | `22197` | Illusion Leg B-type | 130 |  |
| Accessory 1 | `32209` | Illusion Battle chip R | 130 |  |
| Accessory 2 | `32210` | Illusion Battle chip L | 130 |  |

### Renewal: 4th jobs (renewal server, level 200–275)

#### Dragon Knight

Job IDs: `4252` Dragon Knight

| Slot | ID | Item | Min lv | Card |
|---|---|---|---|---|
| Weapon | `600030` | Dim Glacier Two-handed Sword | 230 |  |
| Head top | `19474` | Temporal Circlet (Rune Knight) | 170 |  |
| Head mid | `410010` | Eyes of Illusion | 100 |  |
| Head low | `19439` | Vicious Mind Aura | 170 |  |
| Armor | `450127` | Automatic Armor Type A | 160 |  |
| Garment | `480020` | Automatic Engine Wing Type A | 160 |  |
| Shoes | `470022` | Automatic Leg Type A | 160 |  |
| Accessory 1 | `490024` | Automatic Booster R | 160 |  |
| Accessory 2 | `490025` | Automatic Booster L | 160 |  |

Other weapons: Vicious Mind Two-Handed Sword `21016`

#### Imperial Guard

Job IDs: `4258` Imperial Guard

| Slot | ID | Item | Min lv | Card |
|---|---|---|---|---|
| Weapon | `530034` | Dim Glacier Spear | 230 |  |
| Shield | `460015` | Automatic Shield I | 120 |  |
| Head top | `19475` | Temporal Circlet (Royal Guard) | 170 |  |
| Head mid | `410010` | Eyes of Illusion | 100 |  |
| Head low | `19439` | Vicious Mind Aura | 170 |  |
| Armor | `450127` | Automatic Armor Type A | 160 |  |
| Garment | `480020` | Automatic Engine Wing Type A | 160 |  |
| Shoes | `470022` | Automatic Leg Type A | 160 |  |
| Accessory 1 | `490024` | Automatic Booster R | 160 |  |
| Accessory 2 | `490025` | Automatic Booster L | 160 |  |

Other weapons: Vicious Mind Spear `1400`

#### Arch Mage

Job IDs: `4255` Arch Mage

| Slot | ID | Item | Min lv | Card |
|---|---|---|---|---|
| Weapon | `640034` | Dim Glacier Staff | 230 |  |
| Head top | `19482` | Temporal Circlet (Warlock) | 170 |  |
| Head mid | `410010` | Eyes of Illusion | 100 |  |
| Head low | `19439` | Vicious Mind Aura | 170 |  |
| Armor | `450128` | Automatic Armor Type B | 160 |  |
| Garment | `480021` | Automatic Engine Wing Type B | 160 |  |
| Shoes | `470023` | Automatic Leg Type B | 160 |  |
| Accessory 1 | `490026` | Automatic Battle Chip R | 160 |  |
| Accessory 2 | `490027` | Automatic Battle Chip L | 160 |  |

Other weapons: Vicious Mind Staff `2026`

#### Elemental Master

Job IDs: `4261` Elemental Master

| Slot | ID | Item | Min lv | Card |
|---|---|---|---|---|
| Weapon | `540056` | Dim Glacier Book | 230 |  |
| Shield | `460015` | Automatic Shield I | 120 |  |
| Head top | `19483` | Temporal Circlet (Sorcerer) | 170 |  |
| Head mid | `410010` | Eyes of Illusion | 100 |  |
| Head low | `19439` | Vicious Mind Aura | 170 |  |
| Armor | `450128` | Automatic Armor Type B | 160 |  |
| Garment | `480021` | Automatic Engine Wing Type B | 160 |  |
| Shoes | `470023` | Automatic Leg Type B | 160 |  |
| Accessory 1 | `490026` | Automatic Battle Chip R | 160 |  |
| Accessory 2 | `490027` | Automatic Battle Chip L | 160 |  |

Other weapons: Vicious Mind Book `28605`

#### Windhawk

Job IDs: `4257` Windhawk

| Slot | ID | Item | Min lv | Card |
|---|---|---|---|---|
| Weapon | `700059` | Dim Glacier Bow | 230 |  |
| Head top | `19484` | Temporal Circlet (Ranger) | 170 |  |
| Head mid | `410010` | Eyes of Illusion | 100 |  |
| Head low | `19439` | Vicious Mind Aura | 170 |  |
| Armor | `450127` | Automatic Armor Type A | 160 |  |
| Garment | `480020` | Automatic Engine Wing Type A | 160 |  |
| Shoes | `470022` | Automatic Leg Type A | 160 |  |
| Accessory 1 | `490024` | Automatic Booster R | 160 |  |
| Accessory 2 | `490025` | Automatic Booster L | 160 |  |

Other weapons: Vicious Mind Bow `18121`

#### Troubadour (male)

Job IDs: `4263` Troubadour

| Slot | ID | Item | Min lv | Card |
|---|---|---|---|---|
| Weapon | `570032` | Dim Glacier Violin | 230 |  |
| Shield | `460015` | Automatic Shield I | 120 |  |
| Head top | `19485` | Temporal Circlet (Wanderer & Minstrel) | 170 |  |
| Head mid | `410010` | Eyes of Illusion | 100 |  |
| Head low | `19439` | Vicious Mind Aura | 170 |  |
| Armor | `450127` | Automatic Armor Type A | 160 |  |
| Garment | `480020` | Automatic Engine Wing Type A | 160 |  |
| Shoes | `470022` | Automatic Leg Type A | 160 |  |
| Accessory 1 | `490024` | Automatic Booster R | 160 |  |
| Accessory 2 | `490025` | Automatic Booster L | 160 |  |

Other weapons: Vicious Mind Violin `1900`

#### Trouvere (female)

Job IDs: `4264` Trouvere

| Slot | ID | Item | Min lv | Card |
|---|---|---|---|---|
| Weapon | `580033` | Dim Glacier Whip | 230 |  |
| Shield | `460015` | Automatic Shield I | 120 |  |
| Head top | `19485` | Temporal Circlet (Wanderer & Minstrel) | 170 |  |
| Head mid | `410010` | Eyes of Illusion | 100 |  |
| Head low | `19439` | Vicious Mind Aura | 170 |  |
| Armor | `450127` | Automatic Armor Type A | 160 |  |
| Garment | `480020` | Automatic Engine Wing Type A | 160 |  |
| Shoes | `470022` | Automatic Leg Type A | 160 |  |
| Accessory 1 | `490024` | Automatic Booster R | 160 |  |
| Accessory 2 | `490025` | Automatic Booster L | 160 |  |

Other weapons: Vicious Mind Wire `1996`

#### Cardinal

Job IDs: `4256` Cardinal

| Slot | ID | Item | Min lv | Card |
|---|---|---|---|---|
| Weapon | `640034` | Dim Glacier Staff | 230 |  |
| Head top | `19480` | Temporal Circlet (Archbishop) | 170 |  |
| Head mid | `410010` | Eyes of Illusion | 100 |  |
| Head low | `19439` | Vicious Mind Aura | 170 |  |
| Armor | `450128` | Automatic Armor Type B | 160 |  |
| Garment | `480021` | Automatic Engine Wing Type B | 160 |  |
| Shoes | `470023` | Automatic Leg Type B | 160 |  |
| Accessory 1 | `490026` | Automatic Battle Chip R | 160 |  |
| Accessory 2 | `490027` | Automatic Battle Chip L | 160 |  |

Other weapons: Vicious Mind Rod `1600`

#### Inquisitor

Job IDs: `4262` Inquisitor

| Slot | ID | Item | Min lv | Card |
|---|---|---|---|---|
| Weapon | `560037` | Dim Glacier Knuckle | 230 |  |
| Shield | `460015` | Automatic Shield I | 120 |  |
| Head top | `19481` | Temporal Circlet (Sura) | 170 |  |
| Head mid | `410010` | Eyes of Illusion | 100 |  |
| Head low | `19439` | Vicious Mind Aura | 170 |  |
| Armor | `450127` | Automatic Armor Type A | 160 |  |
| Garment | `480020` | Automatic Engine Wing Type A | 160 |  |
| Shoes | `470022` | Automatic Leg Type A | 160 |  |
| Accessory 1 | `490024` | Automatic Booster R | 160 |  |
| Accessory 2 | `490025` | Automatic Booster L | 160 |  |

Other weapons: Vicious Mind Knuckle `1800`

#### Meister

Job IDs: `4253` Meister

| Slot | ID | Item | Min lv | Card |
|---|---|---|---|---|
| Weapon | `620019` | Dim Glacier Mechanic Axe | 230 |  |
| Head top | `19476` | Temporal Circlet (Mechanic) | 170 |  |
| Head mid | `410010` | Eyes of Illusion | 100 |  |
| Head low | `19439` | Vicious Mind Aura | 170 |  |
| Armor | `450127` | Automatic Armor Type A | 160 |  |
| Garment | `480020` | Automatic Engine Wing Type A | 160 |  |
| Shoes | `470022` | Automatic Leg Type A | 160 |  |
| Accessory 1 | `490024` | Automatic Booster R | 160 |  |
| Accessory 2 | `490025` | Automatic Booster L | 160 |  |

Other weapons: Vicious Mind Two-Handed Axe `28107`

#### Biolo

Job IDs: `4259` Biolo

| Slot | ID | Item | Min lv | Card |
|---|---|---|---|---|
| Weapon | `590047` | Dim Glacier Mace | 230 |  |
| Shield | `460015` | Automatic Shield I | 120 |  |
| Head top | `19477` | Temporal Circlet (Genetic) | 170 |  |
| Head mid | `410010` | Eyes of Illusion | 100 |  |
| Head low | `19439` | Vicious Mind Aura | 170 |  |
| Armor | `450127` | Automatic Armor Type A | 160 |  |
| Garment | `480020` | Automatic Engine Wing Type A | 160 |  |
| Shoes | `470022` | Automatic Leg Type A | 160 |  |
| Accessory 1 | `490024` | Automatic Booster R | 160 |  |
| Accessory 2 | `490025` | Automatic Booster L | 160 |  |

Other weapons: Vicious Mind Mace `16041`

#### Shadow Cross

Job IDs: `4254` Shadow Cross

| Slot | ID | Item | Min lv | Card |
|---|---|---|---|---|
| Weapon | `610041` | Dim Glacier Katar | 230 |  |
| Head top | `19478` | Temporal Circlet (Guillotine Cross) | 170 |  |
| Head mid | `410010` | Eyes of Illusion | 100 |  |
| Head low | `19439` | Vicious Mind Aura | 170 |  |
| Armor | `450127` | Automatic Armor Type A | 160 |  |
| Garment | `480020` | Automatic Engine Wing Type A | 160 |  |
| Shoes | `470022` | Automatic Leg Type A | 160 |  |
| Accessory 1 | `490024` | Automatic Booster R | 160 |  |
| Accessory 2 | `490025` | Automatic Booster L | 160 |  |

Other weapons: Vicious Mind Katar `28008`

#### Abyss Chaser

Job IDs: `4260` Abyss Chaser

| Slot | ID | Item | Min lv | Card |
|---|---|---|---|---|
| Weapon | `510075` | Dim Glacier Rogue Knife | 230 |  |
| Shield | `460015` | Automatic Shield I | 120 |  |
| Head top | `19479` | Temporal Circlet (Shadow Chaser) | 170 |  |
| Head mid | `410010` | Eyes of Illusion | 100 |  |
| Head low | `19439` | Vicious Mind Aura | 170 |  |
| Armor | `450127` | Automatic Armor Type A | 160 |  |
| Garment | `480020` | Automatic Engine Wing Type A | 160 |  |
| Shoes | `470022` | Automatic Leg Type A | 160 |  |
| Accessory 1 | `490024` | Automatic Booster R | 160 |  |
| Accessory 2 | `490025` | Automatic Booster L | 160 |  |

Other weapons: Vicious Mind Bow `18121`

#### Hyper Novice

Job IDs: `4307` Hyper Novice

| Slot | ID | Item | Min lv | Card |
|---|---|---|---|---|
| Weapon | `500055` | Dim Glacier Basic Sword | 230 |  |
| Shield | `460015` | Automatic Shield I | 120 |  |
| Head top | `19491` | Temporal Circlet (Super Novice) | 170 |  |
| Head mid | `410010` | Eyes of Illusion | 100 |  |
| Head low | `19439` | Vicious Mind Aura | 170 |  |
| Armor | `450127` | Automatic Armor Type A | 160 |  |
| Garment | `480020` | Automatic Engine Wing Type A | 160 |  |
| Shoes | `470022` | Automatic Leg Type A | 160 |  |
| Accessory 1 | `490024` | Automatic Booster R | 160 |  |
| Accessory 2 | `490025` | Automatic Booster L | 160 |  |

Other weapons: Vicious Mind Mace `16041`

#### Sky Emperor

Job IDs: `4302` Sky Emperor

| Slot | ID | Item | Min lv | Card |
|---|---|---|---|---|
| Weapon | `540056` | Dim Glacier Book | 230 |  |
| Shield | `460015` | Automatic Shield I | 120 |  |
| Head top | `19486` | Temporal Circlet (Star Emperor) | 170 |  |
| Head mid | `410010` | Eyes of Illusion | 100 |  |
| Head low | `19439` | Vicious Mind Aura | 170 |  |
| Armor | `450127` | Automatic Armor Type A | 160 |  |
| Garment | `480020` | Automatic Engine Wing Type A | 160 |  |
| Shoes | `470022` | Automatic Leg Type A | 160 |  |
| Accessory 1 | `490024` | Automatic Booster R | 160 |  |
| Accessory 2 | `490025` | Automatic Booster L | 160 |  |

Other weapons: Vicious Mind Book `28605`

#### Soul Ascetic

Job IDs: `4303` Soul Ascetic

| Slot | ID | Item | Min lv | Card |
|---|---|---|---|---|
| Weapon | `640034` | Dim Glacier Staff | 230 |  |
| Head top | `19487` | Temporal Circlet (Soul Reaper) | 170 |  |
| Head mid | `410010` | Eyes of Illusion | 100 |  |
| Head low | `19439` | Vicious Mind Aura | 170 |  |
| Armor | `450128` | Automatic Armor Type B | 160 |  |
| Garment | `480021` | Automatic Engine Wing Type B | 160 |  |
| Shoes | `470023` | Automatic Leg Type B | 160 |  |
| Accessory 1 | `490026` | Automatic Battle Chip R | 160 |  |
| Accessory 2 | `490027` | Automatic Battle Chip L | 160 |  |

Other weapons: Vicious Mind Staff `2026`

#### Night Watch

Job IDs: `4306` Night Watch

| Slot | ID | Item | Min lv | Card |
|---|---|---|---|---|
| Weapon | `13128` | Vicious Mind Revolver | 160 |  |
| Head top | `19488` | Temporal Circlet (Rebellion) | 170 |  |
| Head mid | `410010` | Eyes of Illusion | 100 |  |
| Head low | `19439` | Vicious Mind Aura | 170 |  |
| Armor | `450127` | Automatic Armor Type A | 160 |  |
| Garment | `480020` | Automatic Engine Wing Type A | 160 |  |
| Shoes | `470022` | Automatic Leg Type A | 160 |  |
| Accessory 1 | `490024` | Automatic Booster R | 160 |  |
| Accessory 2 | `490025` | Automatic Booster L | 160 |  |

#### Shinkiro (male)

Job IDs: `4304` Shinkiro

| Slot | ID | Item | Min lv | Card |
|---|---|---|---|---|
| Weapon | `13328` | Vicious Mind Huuma Shuriken | 160 |  |
| Head top | `19490` | Temporal Circlet (Kagerou) | 170 |  |
| Head mid | `410010` | Eyes of Illusion | 100 |  |
| Head low | `19439` | Vicious Mind Aura | 170 |  |
| Armor | `450127` | Automatic Armor Type A | 160 |  |
| Garment | `480020` | Automatic Engine Wing Type A | 160 |  |
| Shoes | `470022` | Automatic Leg Type A | 160 |  |
| Accessory 1 | `490024` | Automatic Booster R | 160 |  |
| Accessory 2 | `490025` | Automatic Booster L | 160 |  |

#### Shiranui (female)

Job IDs: `4305` Shiranui

| Slot | ID | Item | Min lv | Card |
|---|---|---|---|---|
| Weapon | `13328` | Vicious Mind Huuma Shuriken | 160 |  |
| Head top | `19489` | Temporal Circlet (Oboro) | 170 |  |
| Head mid | `410010` | Eyes of Illusion | 100 |  |
| Head low | `19439` | Vicious Mind Aura | 170 |  |
| Armor | `450127` | Automatic Armor Type A | 160 |  |
| Garment | `480020` | Automatic Engine Wing Type A | 160 |  |
| Shoes | `470022` | Automatic Leg Type A | 160 |  |
| Accessory 1 | `490024` | Automatic Booster R | 160 |  |
| Accessory 2 | `490025` | Automatic Booster L | 160 |  |

#### Spirit Handler (Doram)

Job IDs: `4308` Spirit Handler

| Slot | ID | Item | Min lv | Card |
|---|---|---|---|---|
| Weapon | `550090` | Dim Glacier Foxtail | 230 |  |
| Shield | `460015` | Automatic Shield I | 120 |  |
| Head top | `19492` | Temporal Circlet (Summoner) | 170 |  |
| Head mid | `410010` | Eyes of Illusion | 100 |  |
| Head low | `19439` | Vicious Mind Aura | 170 |  |
| Armor | `450128` | Automatic Armor Type B | 160 |  |
| Garment | `480021` | Automatic Engine Wing Type B | 160 |  |
| Shoes | `470023` | Automatic Leg Type B | 160 |  |
| Accessory 1 | `490026` | Automatic Battle Chip R | 160 |  |
| Accessory 2 | `490027` | Automatic Battle Chip L | 160 |  |

Other weapons: Adulter Fides Foxtail Wand `550027`

---

## Mounts & pets
| Command | What it does |
|---|---|
| `@mount` | ride / get off your job's mount. **Knight / Lord Knight → Peco Peco**, Crusader / Paladin → Grand Peco. The class is required, the skill isn't |
| `@mount <1-5>` | Rune Knight (renewal): dragon color (needs Dragon Training skill: `@allskill`) |
| `@mount` | Ranger (renewal): warg (needs Warg Rider skill); Mechanic: Mado Gear |
| `@mount2` | cash-shop mount (any class) |
| `@makeegg <pet id>` → `@hatch` | get a pet egg and hatch it; `@petfriendly 1000` = max intimacy |
| `@makehomun <id>` | Alchemist homunculus (6001 Lif, 6002 Amistr, 6003 Filir, 6004 Vanilmirth) |

For normal players (no GM): learn **Peco Peco Ride** (Knight/Crusader skill), then talk to the **Peco Peco Breeder** in Prontera: Knights at `prontera 55 350`, Crusaders at `prontera 232 318` (GM shortcut: `@warp prontera 55 350`).
Quick test: `@job 4008` → `@allskill` → `@mount`.

## Fun commands
| Command | What it does |
|---|---|
| `@snow` / `@sakura` / `@fireworks` / `@leaves` / `@fog` / `@clouds` / `@clouds2` | weather effect on all maps (run again to turn off) |
| `@night` / `@day` | darken / brighten the whole server |
| `@disguise <monster>` / `@undisguise` | turn into a monster (`@disguise baphomet`) |
| `@size 2` / `@size 1` / `@size 0` | giant / tiny / normal |
| `@monsterbig <monster>` / `@monstersmall <monster>` | giant / tiny monsters |
| `@evilclone <player>` | spawn an aggressive clone of a player |
| `@slaveclone <player>` | clone that follows and fights for you |
| `@summon <monster> [minutes]` | a monster pet that fights for you (`@summon 1039 10` = Baphomet for 10 min) |
| `@fakename <name>` | temporary fake name (no name = back to normal) |
| `@me <text>` | action text: `*YourName text*` |
| `@npctalk <npc> <text>` | make an NPC say something |
| `@kamic <hex color> <text>` | colored server-wide message, e.g. `@kamic FF0000 Hello` |
| `@effect <id>` / `@misceffect <id>` | play visual effects (try ids 0–1000) |
| `@nuke <player>` | blow up a player and everyone around them |
| `@doom` / `@doommap` | kill everyone on the server / on your map (not GMs) |
| `@raisemap` | revive everyone on your map |
| `@pvpon` / `@pvpoff` | PvP on your current map |
| `@duel` | challenge someone to a duel |
| `@killer` / `@killable` | you can attack / be attacked outside PvP |
| `@marry <player>` / `@divorce` | instant wedding |
| `@changecharsex` | change your character's gender (relog) |
| `@font <0-9>` | change the client font |
