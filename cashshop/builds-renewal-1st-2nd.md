# RagnaDuds Cash Shop: 1st and 2nd / transcendent class gear (RENEWAL, base level 99 or lower)

Server: rAthena renewal, kRO 2026 client. 3rd classes are covered in `builds-renewal-3rd-part1/2.md`; this file does not repeat them.

## How the picks were made
- Route: bROWiki's renewal equipment route puts **Eden/Paradise gear** at levels 1-100 (class Paradise weapons unlock skill bonuses at base 60/75/90).
  iRO Wiki and ROGGH class pages give the usual 1-99 builds used here: Bowling Bash Knight, Grand Cross Crusader, Storm Gust/Meteor Wizard,
  Heaven's Drive Sage, Falconer Hunter, Musical Strike/Throw Arrow, Magnus Priest, Combo Monk, Sonic Blow Assassin, Back Stab Rogue,
  Cart Revolution Merchant/Blacksmith, Acid Terror/Acid Demonstration Alchemist, Esma Soul Linker, magic Ninja, Desperado Gunslinger, bolt Super Novice.
- Every item was then searched in this server's DB (`db/re/item_db_equip.yml`, `item_combos.yml`) with a script: skill bonuses (`bSkillAtk`, `bVariableCastrate`, ...)
  for each class's skills, and a generic damage score per slot for the shared slots. Each item was checked against `Jobs` / `Classes`
  (for example `Classes: Upper` = transcendent only) and `EquipLevelMin` (60 or lower for 1st classes, 99 or lower for the rest).
- Every Id was run through `icons/check.py`. `ok` = the client has name, icon and drop sprite. `NEEDS-FIX` = best in slot but the
  client is missing its data (`NOINFO`) or its pictures (`iNsN`). The look-alike Id to copy the pictures from is in the NEEDS-FIX table at the end.
- GM/test items (Ahura Mazdah, Naqsi, Angra Manyu, Balmung) scored highest but were left out on purpose.
- Refine notes: several picks get their skill bonus at +7/+9 (Flaward Hat, Hat of Desert). Sell them together with the refine certificates.

## Shared cores (reused in the class tables)
| Core | Upper | Mid | Lower | Armor | Garment | Shoes | Acc | Acc |
|---|---|---|---|---|---|---|---|---|

| Physical 1st (lv<=60) | RWC Champ Crown Second Place (18780) | Small Devil Horns (18503) | Arbitrator Shawl (420246) | Half Brynhild (15023) | Paradise Manteau (480103) | Pollux Shoes (2400) | Half Megingjard (2856) | Bakunawa Agimat Tattoo (2910) |
| Physical 2nd | RWC Champ Crown Second Place (18780) | Small Devil Horns (18503) | Arbitrator Shawl (420246) | Brynhild (2383) | Temporal Transcendence Manteau (20939) | Pollux Shoes (2400) | Megingjard (2629) | Badge Of Order Grace (5825) |
| Ranged 1st | RWC Champ Crown Second Place (18780) | Small Devil Horns (18503) | Arbitrator Shawl (420246) | Half Brynhild (15023) | Fallen Angel Wing (2589) | Paradise Boots (470067) | Bakunawa Agimat Tattoo (2910) | Badge Of Order Grace (5825) |
| Ranged 2nd | RWC Champ Crown Second Place (18780) | Small Devil Horns (18503) | Arbitrator Shawl (420246) | Brynhild (2383) | Fallen Angel Wing (2589) | Paradise Boots (470067) | Bakunawa Agimat Tattoo (2910) | Badge Of Order Grace (5825) |
| Magic 1st (lv<=60) | F Pecopeco Hairband (5628) | Small Devil Horns (18503) | Survivor's Orb (19139) | Half Brynhild (15023) | Short-term Hunting Manteau (20903) | Paradise Shoes (470068) | Bawaya Agimat Tattoo (2907) | RJC2012 Spell Necklace (2939) |
| Magic 2nd | F Pecopeco Hairband (5628) | Small Devil Horns (18503) | Survivor's Orb (19139) | Brynhild (2383) | Temporal Transcendence Manteau (20939) | Moaning of Evil Spirits (470112) | Bawaya Agimat Tattoo (2907) | RJC2012 Spell Necklace (2939) |

## Swordman
Build: **Bash / Magnum Break melee**. Gear level cap used: 60.

| Slot | Item (Id) | EquipLevelMin | checker status | why |
|---|---|---|---|---|
| Weapon | Cutlus (13402) | 0 | ok | Cutlus: ATK 185 lv4 weapon, Bash Lv5 skill, STR +2, usable at lv1 |
| Shield | Cursed Mad Bunny (28901) | 1 | ok | Cursed Mad Bunny: ASPD +3, ATK/MATK +5% |
| Upper | RWC Champ Crown Second Place (18780) | 1 | ok | +12 all stats, curse/stun immune; best generic top at any level |
| Mid | Small Devil Horns (18503) | 1 | ok | +5% dmg vs all classes, +5% MATK, +10% HP/SP |
| Lower | Arbitrator Shawl (420246) | 1 | ok | ATK +10%, after-cast delay -5% |
| Armor | Half Brynhild (15023) | 47 | ok | Half Brynhild: +5% vs all classes, +5% MATK, HP +20/lv, no knockback (lv47) |
| Garment | Paradise Manteau (480103) | 10 | ok | Paradise Manteau: -20% neutral dmg, HIT, ASPD +10% at lv45 |
| Shoes | Pollux Shoes (2400) | 0 | ok | Pollux Shoes: ATK +50, ASPD +10%, HP/SP +10% |
| Accessory | Half Megingjard (2856) | 47 | ok | Half Megingjard: STR +24 at lv40 (lv47) |
| Accessory | Bakunawa Agimat Tattoo (2910) | 1 | ok | Bakunawa Agimat Tattoo: +7% vs all classes, ASPD +10% |
| Alt weapon | Cutlus (1135) | 40 | ok | Cutlus [lv40 slotted] |

## Knight / Lord Knight
Build: **Bowling Bash, two-handed sword**. Gear level cap used: 99.

| Slot | Item (Id) | EquipLevelMin | checker status | why |
|---|---|---|---|---|
| Weapon | Veteran Sword (1188) | 80 | ok | Veteran Sword: ATK 180, Bowling Bash +50% and Bash +50% with the skills at 10 (lv80) |
| Upper | Hat of Desert (400512) | 50 | NEEDS-FIX | Hat of Desert: ATK +2%, ASPD +1, Bowling Bash +30% at +7; set with Kenshi Gauntlet |
| Mid | Small Devil Horns (18503) | 1 | ok | +5% vs all classes, +10% HP/SP |
| Lower | Arbitrator Shawl (420246) | 1 | ok | ATK +10%, ACD -5% |
| Armor | Brynhild (2383) | 94 | ok | Brynhild: +10% vs all classes, +10% MATK, HP +20/lv, unbreakable (lv94) |
| Garment | Temporal Transcendence Manteau (20939) | 99 | ok | Temporal Transcendence Manteau: ASPD +10%, VCT -10%, -10% fire/water/earth/wind dmg (lv99) |
| Shoes | Pollux Shoes (2400) | 0 | ok | Pollux Shoes: ATK +50, ASPD +10%, HP/SP +10% |
| Accessory | Kenshi Gauntlet (490282) | 50 | NEEDS-FIX | Kenshi Gauntlet: STR/VIT +3, ATK +3%, Brandish Spear +100%, BB +25% (2H Quicken 10); set with Hat of Desert gives BB +50% |
| Accessory | Badge Of Order Grace (5825) | 0 | ok | Badge of Order Grace: +10% vs all classes, +10% MATK |
| Alt weapon | Paradise Knight Two-Handed Sword (600020) | 45 | ok | Paradise Knight Two-Handed Sword (lv45, BB +25%) |

## Crusader / Paladin
Build: **Grand Cross (hybrid ATK+MATK)**. Gear level cap used: 99.

| Slot | Item (Id) | EquipLevelMin | checker status | why |
|---|---|---|---|---|
| Weapon | Paradise Crusader Sword (500033) | 45 | ok | Paradise Crusader Sword: ATK/MATK 160, Grand Cross +25% at lv90, VCT -10% |
| Shield | Purified Knight's Shield (28946) | 1 | ok | Purified Knight's Shield: ATK/MATK +5%, ASPD +10%, -10% all-element dmg |
| Upper | RWC Champ Crown Second Place (18780) | 1 | ok | +12 all stats |
| Mid | Imperial Feather (18823) | 70 | NEEDS-FIX | Imperial Feather: set with Imperial Ring gives Grand Cross +BaseLevel% and -2s cast |
| Lower | Arbitrator Shawl (420246) | 1 | ok | ATK +10%, ACD -5% |
| Armor | Brynhild (2383) | 94 | ok | Brynhild: +10% vs all classes, +10% MATK, HP +20/lv, unbreakable (lv94) |
| Garment | Temporal Transcendence Manteau (20939) | 99 | ok | Temporal Transcendence Manteau: ASPD +10%, VCT -10%, -10% fire/water/earth/wind dmg (lv99) |
| Shoes | Pollux Shoes (2400) | 0 | ok | Pollux Shoes: ATK +50, ASPD +10%, HP/SP +10% |
| Accessory | Imperial Ring (28372) | 50 | NEEDS-FIX | Imperial Ring: STR/INT +1, HP/SP +3%; set with Imperial Feather |
| Accessory | Badge Of Order Grace (5825) | 0 | ok | Badge of Order Grace: +10% vs all classes, +10% MATK |
| Alt weapon | Paradise Crusader Spear (530017) | 45 | ok | Paradise Crusader Spear (Holy Cross +25%) |

## Mage
Build: **Bolts / Fire Ball**. Gear level cap used: 60.

| Slot | Item (Id) | EquipLevelMin | checker status | why |
|---|---|---|---|---|
| Weapon | Paradise Staff (550032) | 10 | ok | Paradise Staff: MATK 100 + 60, unbreakable |
| Shield | Purified Knight's Shield (28946) | 1 | ok | Purified Knight's Shield: ATK/MATK +5%, ASPD +10%, -10% all-element dmg |
| Upper | F Pecopeco Hairband (5628) | 0 | ok | F Pecopeco Hairband: VCT -25%, ASPD +10%, move speed |
| Mid | Small Devil Horns (18503) | 1 | ok | +5% MATK, +10% HP/SP |
| Lower | Survivor's Orb (19139) | 50 | ok | Survivor's Orb: +2% MATK/dmg, VCT -3% (lv50) |
| Armor | Half Brynhild (15023) | 47 | ok | Half Brynhild: +5% MATK, HP (lv47) |
| Garment | Short-term Hunting Manteau (20903) | 50 | ok | Short-term Hunting Manteau: VCT -15%, FLEE +15 (lv50) |
| Shoes | Paradise Shoes (470068) | 10 | ok | Paradise Shoes: +10% elemental magic dmg at lv45, MATK |
| Accessory | Bawaya Agimat Tattoo (2907) | 1 | ok | Bawaya Agimat Tattoo: MATK +7%, fixed cast -7% |
| Accessory | RJC2012 Spell Necklace (2939) | 1 | ok | RJC2012 Spell Necklace: VCT -20%, no cast interruption |

## Wizard / High Wizard
Build: **Storm Gust / Meteor Storm / Lord of Vermilion**. Gear level cap used: 99.

| Slot | Item (Id) | EquipLevelMin | checker status | why |
|---|---|---|---|---|
| Weapon | Paradise Wizard Staff (550034) | 45 | ok | Paradise Wizard Staff: MATK 160, VCT -10%, SG/Meteor +20%, LoV/Heaven's Drive +20% at lv90 |
| Shield | Purified Knight's Shield (28946) | 1 | ok | Purified Knight's Shield: ATK/MATK +5%, ASPD +10%, -10% all-element dmg |
| Upper | F Pecopeco Hairband (5628) | 0 | ok | F Pecopeco Hairband: VCT -25%, ASPD +10%, move speed |
| Mid | Small Devil Horns (18503) | 1 | ok | +5% MATK, +10% HP/SP |
| Lower | Survivor's Orb (19139) | 50 | ok | Survivor's Orb: MATK +2%, VCT -3% |
| Armor | Brynhild (2383) | 94 | ok | Brynhild: MATK +10%, HP +20/lv (lv94) |
| Garment | Temporal Transcendence Manteau (20939) | 99 | ok | Temporal Transcendence Manteau: VCT -10%, ASPD, elemental resist (lv99) |
| Shoes | Moaning of Evil Spirits (470112) | 99 | ok | Moaning of Evil Spirits: MATK +15% (lv99) |
| Accessory | Bawaya Agimat Tattoo (2907) | 1 | ok | Bawaya Agimat Tattoo: MATK +7%, fixed cast -7% |
| Accessory | RJC2012 Spell Necklace (2939) | 1 | ok | RJC2012 Spell Necklace: VCT -20%, no cast interruption |
| Alt weapon | Staff of Destruction (2000) | 80 | ok | Staff of Destruction (High Wizard only, lv80, MATK 280, two-handed) |

## Sage / Professor
Build: **Earth Spike / Heaven's Drive**. Gear level cap used: 99.

| Slot | Item (Id) | EquipLevelMin | checker status | why |
|---|---|---|---|---|
| Weapon | Paradise Sage Magic Book (540027) | 45 | ok | Paradise Sage Magic Book: MATK 160, VCT -10%, Heaven's Drive +25% at lv90 |
| Shield | Purified Knight's Shield (28946) | 1 | ok | Purified Knight's Shield: ATK/MATK +5%, ASPD +10%, -10% all-element dmg |
| Upper | RJC Katusa Flower (5547) | 0 | ok | RJC Katusa Flower: Heaven's Drive/Earth Spike +15% (+weapon refine), their cast -25% |
| Mid | Small Devil Horns (18503) | 1 | ok | +5% MATK, +10% HP/SP |
| Lower | Survivor's Orb (19139) | 50 | ok | Survivor's Orb: MATK +2%, VCT -3% |
| Armor | Brynhild (2383) | 94 | ok | Brynhild: MATK +10%, HP +20/lv (lv94) |
| Garment | Temporal Transcendence Manteau (20939) | 99 | ok | Temporal Transcendence Manteau: VCT -10%, ASPD, elemental resist (lv99) |
| Shoes | Moaning of Evil Spirits (470112) | 99 | ok | Moaning of Evil Spirits: MATK +15% (lv99) |
| Accessory | Bawaya Agimat Tattoo (2907) | 1 | ok | Bawaya Agimat Tattoo: MATK +7%, fixed cast -7% |
| Accessory | RJC2012 Spell Necklace (2939) | 1 | ok | RJC2012 Spell Necklace: VCT -20%, no cast interruption |
| Alt weapon | Paradise Sage Spellbook (540028) | 45 | ok | Paradise Sage Spellbook (bolts +20/+40%) |

## Archer
Build: **Double Strafe / Arrow Shower**. Gear level cap used: 60.

| Slot | Item (Id) | EquipLevelMin | checker status | why |
|---|---|---|---|---|
| Weapon | Bow Of Evil (1744) | 1 | ok | Bow of Evil: ATK 170 lv4 bow, Double Strafe +25%, DEX +2, lv1 |
| Upper | RWC Champ Crown Second Place (18780) | 1 | ok | +12 all stats (DEX/AGI) |
| Mid | Small Devil Horns (18503) | 1 | ok | +5% vs all classes |
| Lower | Arbitrator Shawl (420246) | 1 | ok | ATK +10%, ACD -5% |
| Armor | Half Brynhild (15023) | 47 | ok | Half Brynhild: +5% vs all classes (lv47) |
| Garment | Fallen Angel Wing (2589) | 0 | ok | Fallen Angel Wing: all stats +1, ranged dmg +1% per 20 DEX, ASPD per AGI |
| Shoes | Paradise Boots (470067) | 10 | ok | Paradise Boots: melee/ranged dmg +10%, crit, fixed cast -0.3s at lv85 |
| Accessory | Double Badge (490236) | 20 | NEEDS-FIX | Double Badge: Double Strafe/Arrow Shower +BaseLevel/2 %, AGI/DEX +2 |
| Accessory | Badge Of Order Grace (5825) | 0 | ok | Badge of Order Grace: +10% vs all classes |
| Alt weapon | Paradise Bow (700036) | 10 | ok | Paradise Bow |

## Hunter / Sniper
Build: **Falconer (auto Blitz Beat, LUK/DEX/INT)**. Gear level cap used: 99.

| Slot | Item (Id) | EquipLevelMin | checker status | why |
|---|---|---|---|---|
| Weapon | Paradise Hunter Crossbow (700039) | 45 | ok | Paradise Hunter Crossbow: ATK 180, ASPD +10%, Blitz Beat/Falcon Assault +25% at lv90 |
| Upper | RWC Champ Crown Second Place (18780) | 1 | ok | +12 all stats (DEX/AGI) |
| Mid | Small Devil Horns (18503) | 1 | ok | +5% vs all classes |
| Lower | Falconer Flute (18985) | 75 | ok | Falconer Flute: auto-casts Blitz Beat on attack (chance from LUK); set piece |
| Armor | Brynhild (2383) | 94 | ok | Brynhild: +10% vs all classes (lv94) |
| Garment | Fallen Angel Wing (2589) | 0 | ok | Fallen Angel Wing: all stats +1, ranged dmg +1% per 20 DEX, ASPD per AGI |
| Shoes | Paradise Boots (470067) | 10 | ok | Paradise Boots: melee/ranged dmg +10%, crit, fixed cast -0.3s at lv85 |
| Accessory | Falconer Claw (28321) | 80 | NEEDS-FIX | Falconer Claw: Blitz Beat +10% per Steel Crow level (+100%); Flute+Claw+Glove set = Blitz +200% |
| Accessory | Falconer Glove (28322) | 80 | NEEDS-FIX | Falconer Glove: SP cost -5%, DEX +1; completes the Falconer set |
| Alt weapon | Falken Blitz (1745) | 50 | ok | Falken Blitz (Sniper only, Sharp Shooting/DS/Charge Arrow +10%) |

## Bard / Clown
Build: **Musical Strike / Arrow Vulcan**. Gear level cap used: 99.

| Slot | Item (Id) | EquipLevelMin | checker status | why |
|---|---|---|---|---|
| Weapon | Paradise Bard Violin (570021) | 45 | ok | Paradise Bard Violin: ATK 180, ranged +10%, Musical Strike +25% at lv90 |
| Upper | RWC Champ Crown Second Place (18780) | 1 | ok | +12 all stats (DEX/AGI) |
| Mid | Small Devil Horns (18503) | 1 | ok | +5% vs all classes |
| Lower | Arbitrator Shawl (420246) | 1 | ok | ATK +10%, ACD -5% |
| Armor | Brynhild (2383) | 94 | ok | Brynhild: +10% vs all classes (lv94) |
| Garment | Fallen Angel Wing (2589) | 0 | ok | Fallen Angel Wing: all stats +1, ranged dmg +1% per 20 DEX, ASPD per AGI |
| Shoes | Paradise Boots (470067) | 10 | ok | Paradise Boots: melee/ranged dmg +10%, crit, fixed cast -0.3s at lv85 |
| Accessory | Emerald Earrings (28411) | 50 | NEEDS-FIX | Emerald Earrings: Arrow Vulcan/Musical Strike/Throw Arrow +BaseLevel% (+99%), DEX/AGI/INT +5; wear two |
| Accessory | Emerald Earrings (28411) | 50 | NEEDS-FIX | second Emerald Earrings: another +BaseLevel% |
| Alt weapon | Crimson Violin (1939) | 70 | ok | Crimson Violin (lv70, ATK grows with refine) |

## Dancer / Gypsy
Build: **Throw Arrow (Slinging Arrow) / Arrow Vulcan**. Gear level cap used: 99.

| Slot | Item (Id) | EquipLevelMin | checker status | why |
|---|---|---|---|---|
| Weapon | Paradise Dancer Rope (580021) | 45 | ok | Paradise Dancer Rope: ATK 180, ranged +10%, Throw Arrow +25% at lv90 |
| Upper | RWC Champ Crown Second Place (18780) | 1 | ok | +12 all stats (DEX/AGI) |
| Mid | Small Devil Horns (18503) | 1 | ok | +5% vs all classes |
| Lower | Arbitrator Shawl (420246) | 1 | ok | ATK +10%, ACD -5% |
| Armor | Brynhild (2383) | 94 | ok | Brynhild: +10% vs all classes (lv94) |
| Garment | Fallen Angel Wing (2589) | 0 | ok | Fallen Angel Wing: all stats +1, ranged dmg +1% per 20 DEX, ASPD per AGI |
| Shoes | Paradise Boots (470067) | 10 | ok | Paradise Boots: melee/ranged dmg +10%, crit, fixed cast -0.3s at lv85 |
| Accessory | Emerald Earrings (28411) | 50 | NEEDS-FIX | Emerald Earrings: Throw Arrow/Arrow Vulcan +BaseLevel% (+99%); wear two |
| Accessory | Emerald Earrings (28411) | 50 | NEEDS-FIX | second Emerald Earrings |
| Alt weapon | Crimson Whip (1995) | 70 | ok | Crimson Whip (lv70) |

## Acolyte
Build: **Holy Light / Heal**. Gear level cap used: 60.

| Slot | Item (Id) | EquipLevelMin | checker status | why |
|---|---|---|---|---|
| Weapon | Paradise Staff (550032) | 10 | ok | Paradise Staff: MATK 100 + 60 |
| Shield | Purified Knight's Shield (28946) | 1 | ok | Purified Knight's Shield: ATK/MATK +5%, ASPD +10%, -10% all-element dmg |
| Upper | Magical Feather (19211) | 10 | ok | Magical Feather: +5% (+10% at +7) magic/physical dmg vs undead/dark/ghost/poison/holy |
| Mid | Small Devil Horns (18503) | 1 | ok | +5% MATK, +10% HP/SP |
| Lower | Survivor's Orb (19139) | 50 | ok | Survivor's Orb: +2% MATK/dmg, VCT -3% (lv50) |
| Armor | Half Brynhild (15023) | 47 | ok | Half Brynhild: +5% MATK, HP (lv47) |
| Garment | Short-term Hunting Manteau (20903) | 50 | ok | Short-term Hunting Manteau: VCT -15%, FLEE +15 (lv50) |
| Shoes | Paradise Shoes (470068) | 10 | ok | Paradise Shoes: +10% elemental magic dmg at lv45, MATK |
| Accessory | Clip (2607) | 0 | ok | Clip: set with Spiritual Ring gives Heal +50%, Magnus +30% |
| Accessory | Spiritual Ring (28432) | 0 | ok | Spiritual Ring: INT +2, DEX +1; set with Clip |

## Priest / High Priest
Build: **Magnus Exorcismus (battle priest)**. Gear level cap used: 99.

| Slot | Item (Id) | EquipLevelMin | checker status | why |
|---|---|---|---|---|
| Weapon | Holy Stick (1631) | 70 | ok | Holy Stick: MATK 140 lv4, holy element, Magnus/Holy Light/Turn Undead cast -25% (lv70) |
| Shield | Exorcism Bible (2129) | 50 | ok | Exorcism Bible: set with Holy Stick gives Magnus +20%, auto Turn Undead |
| Upper | F Pecopeco Hairband (5628) | 0 | ok | F Pecopeco Hairband: VCT -25%, ASPD +10%, move speed |
| Mid | Small Devil Horns (18503) | 1 | ok | +5% MATK, +10% HP/SP |
| Lower | Survivor's Orb (19139) | 50 | ok | Survivor's Orb: MATK +2%, VCT -3% |
| Armor | Brynhild (2383) | 94 | ok | Brynhild: MATK +10%, HP +20/lv (lv94) |
| Garment | Temporal Transcendence Manteau (20939) | 99 | ok | Temporal Transcendence Manteau: VCT -10%, ASPD, elemental resist (lv99) |
| Shoes | Moaning of Evil Spirits (470112) | 99 | ok | Moaning of Evil Spirits: MATK +15% (lv99) |
| Accessory | Rosary (2626) | 90 | ok | Rosary: set with Spiritual Ring gives Heal +50%, Magnus +30% (lv90; use Clip 2607 below 90) |
| Accessory | Spiritual Ring (28432) | 0 | ok | Spiritual Ring: INT +2, DEX +1; set with Rosary/Clip |
| Alt weapon | Paradise Priest Staff (550036) | 45 | ok | Paradise Priest Staff (Magnus +25%, VCT -10%) |

## Monk / Champion
Build: **Combo (Triple Attack > Chain Combo > Combo Finish > Tiger Fist / Chain Crush)**. Gear level cap used: 99.

| Slot | Item (Id) | EquipLevelMin | checker status | why |
|---|---|---|---|---|
| Weapon | Paradise Monk Knuckles (560022) | 45 | ok | Paradise Monk Knuckles: ATK 160, ASPD +10%, Chain Combo +20%, Combo Finish +20% at lv90 |
| Upper | RWC Champ Crown Second Place (18780) | 1 | ok | +12 all stats |
| Mid | Small Devil Horns (18503) | 1 | ok | +5% vs all classes, +10% HP/SP |
| Lower | Arbitrator Shawl (420246) | 1 | ok | ATK +10%, ACD -5% |
| Armor | Brynhild (2383) | 94 | ok | Brynhild: +10% vs all classes, +10% MATK, HP +20/lv, unbreakable (lv94) |
| Garment | Temporal Transcendence Manteau (20939) | 99 | ok | Temporal Transcendence Manteau: ASPD +10%, VCT -10%, -10% fire/water/earth/wind dmg (lv99) |
| Shoes | Pollux Shoes (2400) | 0 | ok | Pollux Shoes: ATK +50, ASPD +10%, HP/SP +10% |
| Accessory | Boxer Glove (490399) | 55 | NEEDS-FIX | Boxer Glove: Monk only: Chain Combo/Combo Finish/Tiger Fist/Chain Crush +BaseLevel%, STR/AGI +3, auto Summon Spirit Sphere |
| Accessory | Badge Of Order Grace (5825) | 0 | ok | Badge of Order Grace: +10% vs all classes, +10% MATK |
| Alt weapon | Combo Battle Glove (1822) | 60 | ok | Combo Battle Glove (4 slots, TA +15, Chain +15, Finish +20) |

## Thief
Build: **Double Attack melee**. Gear level cap used: 60.

| Slot | Item (Id) | EquipLevelMin | checker status | why |
|---|---|---|---|---|
| Weapon | Cutlus (13402) | 0 | ok | Cutlus: ATK 185 lv4 sword, STR +2, lv1 |
| Shield | Cursed Mad Bunny (28901) | 1 | ok | Cursed Mad Bunny: ASPD +3, ATK/MATK +5% |
| Upper | RWC Champ Crown Second Place (18780) | 1 | ok | +12 all stats, curse/stun immune; best generic top at any level |
| Mid | Small Devil Horns (18503) | 1 | ok | +5% dmg vs all classes, +5% MATK, +10% HP/SP |
| Lower | Arbitrator Shawl (420246) | 1 | ok | ATK +10%, after-cast delay -5% |
| Armor | Half Brynhild (15023) | 47 | ok | Half Brynhild: +5% vs all classes, +5% MATK, HP +20/lv, no knockback (lv47) |
| Garment | Paradise Manteau (480103) | 10 | ok | Paradise Manteau: -20% neutral dmg, HIT, ASPD +10% at lv45 |
| Shoes | Pollux Shoes (2400) | 0 | ok | Pollux Shoes: ATK +50, ASPD +10%, HP/SP +10% |
| Accessory | Half Megingjard (2856) | 47 | ok | Half Megingjard: STR +24 at lv40 (lv47) |
| Accessory | Bakunawa Agimat Tattoo (2910) | 1 | ok | Bakunawa Agimat Tattoo: +7% vs all classes, ASPD +10% |
| Alt weapon | Paradise Dagger (510035) | 10 | ok | Paradise Dagger |

## Assassin / Assassin Cross
Build: **Sonic Blow katar**. Gear level cap used: 99.

| Slot | Item (Id) | EquipLevelMin | checker status | why |
|---|---|---|---|---|
| Weapon | Paradise Assassin Katar (610025) | 45 | ok | Paradise Assassin Katar: ATK 180, HIT +15, Sonic Blow +25% at lv90 |
| Upper | RWC Champ Crown Second Place (18780) | 1 | ok | +12 all stats |
| Mid | Small Devil Horns (18503) | 1 | ok | +5% vs all classes, +10% HP/SP |
| Lower | Arbitrator Shawl (420246) | 1 | ok | ATK +10%, ACD -5% |
| Armor | Brynhild (2383) | 94 | ok | Brynhild: +10% vs all classes, +10% MATK, HP +20/lv, unbreakable (lv94) |
| Garment | Temporal Transcendence Manteau (20939) | 99 | ok | Temporal Transcendence Manteau: ASPD +10%, VCT -10%, -10% fire/water/earth/wind dmg (lv99) |
| Shoes | Pollux Shoes (2400) | 0 | ok | Pollux Shoes: ATK +50, ASPD +10%, HP/SP +10% |
| Accessory | Megingjard (2629) | 94 | ok | Megingjard: STR +59 at lv99 (lv94) |
| Accessory | Badge Of Order Grace (5825) | 0 | ok | Badge of Order Grace: +10% vs all classes, +10% MATK |
| Alt weapon | Crimson Katar (28007) | 70 | ok | Crimson Katar (lv70, ATK grows with refine) |

## Rogue / Stalker
Build: **Back Stab spam**. Gear level cap used: 99.

| Slot | Item (Id) | EquipLevelMin | checker status | why |
|---|---|---|---|---|
| Weapon | Paradise Rogue Dagger (510036) | 45 | ok | Paradise Rogue Dagger: ATK 160, ASPD +10%, Back Stab +20%, Raid +25% |
| Shield | Cursed Mad Bunny (28901) | 1 | ok | Cursed Mad Bunny: ASPD +3, ATK/MATK +5% |
| Upper | RWC Champ Crown Second Place (18780) | 1 | ok | +12 all stats |
| Mid | Small Devil Horns (18503) | 1 | ok | +5% vs all classes, +10% HP/SP |
| Lower | Arbitrator Shawl (420246) | 1 | ok | ATK +10%, ACD -5% |
| Armor | Brynhild (2383) | 94 | ok | Brynhild: +10% vs all classes, +10% MATK, HP +20/lv, unbreakable (lv94) |
| Garment | Temporal Transcendence Manteau (20939) | 99 | ok | Temporal Transcendence Manteau: ASPD +10%, VCT -10%, -10% fire/water/earth/wind dmg (lv99) |
| Shoes | Pollux Shoes (2400) | 0 | ok | Pollux Shoes: ATK +50, ASPD +10%, HP/SP +10% |
| Accessory | Shadow Ring (28379) | 20 | NEEDS-FIX | Shadow Ring: Back Stab +2x BaseLevel % (+198% at 99), Raid stun; wear two |
| Accessory | Shadow Ring (28379) | 20 | NEEDS-FIX | second Shadow Ring: another +198% Back Stab |
| Alt weapon | Dagger of Hunter (13038) | 70 | ok | Dagger of Hunter (Stalker only, lv70, Back Stab +20%, auto Bash) |

## Merchant
Build: **Cart Revolution spam**. Gear level cap used: 60.

| Slot | Item (Id) | EquipLevelMin | checker status | why |
|---|---|---|---|---|
| Weapon | Mace Of Madness (1547) | 0 | ok | Mace of Madness: ATK 150 lv3, Cart Revolution +25%, STR +2, lv0 |
| Shield | Cursed Mad Bunny (28901) | 1 | ok | Cursed Mad Bunny: ASPD +3, ATK/MATK +5% |
| Shadow | Merchant Shadow Pendant (24251) | 1 | ok | Merchant Shadow Pendant (shadow accessory): Cart Revolution +20% +5% per refine |
| Upper | RWC Champ Crown Second Place (18780) | 1 | ok | +12 all stats, curse/stun immune; best generic top at any level |
| Mid | Small Devil Horns (18503) | 1 | ok | +5% dmg vs all classes, +5% MATK, +10% HP/SP |
| Lower | Arbitrator Shawl (420246) | 1 | ok | ATK +10%, after-cast delay -5% |
| Armor | Half Brynhild (15023) | 47 | ok | Half Brynhild: +5% vs all classes, +5% MATK, HP +20/lv, no knockback (lv47) |
| Garment | Paradise Manteau (480103) | 10 | ok | Paradise Manteau: -20% neutral dmg, HIT, ASPD +10% at lv45 |
| Shoes | Pollux Shoes (2400) | 0 | ok | Pollux Shoes: ATK +50, ASPD +10%, HP/SP +10% |
| Accessory | Arquien's Necklace (28429) | 20 | ok | Arquien's Necklace: Cart Revolution +BaseLevel% (lv20) |
| Accessory | Arquien's Necklace (28429) | 20 | ok | second Arquien's Necklace: another +BaseLevel% |
| Alt weapon | Paradise Axe (520010) | 10 | ok | Paradise Axe (lv10) |
| Card | Heavy Metaling Card (4467) | - | ok | Heavy Metaling Card (shoes): Merchant class Cart Revolution +50%, SP -12 |

## Blacksmith
Build: **Cart Revolution spam (non-trans)**. Gear level cap used: 99.

| Slot | Item (Id) | EquipLevelMin | checker status | why |
|---|---|---|---|---|
| Weapon | Paradise Blacksmith Axe (520011) | 45 | ok | Paradise Blacksmith Axe: ATK 160, melee +10%, Cart Revolution +25% at lv90 |
| Shield | Cursed Mad Bunny (28901) | 1 | ok | Cursed Mad Bunny: ASPD +3, ATK/MATK +5% |
| Shadow | Merchant Shadow Pendant (24251) | 1 | ok | Merchant Shadow Pendant: Cart Revolution +20%+ |
| Upper | RWC Champ Crown Second Place (18780) | 1 | ok | +12 all stats |
| Mid | Small Devil Horns (18503) | 1 | ok | +5% vs all classes, +10% HP/SP |
| Lower | Arbitrator Shawl (420246) | 1 | ok | ATK +10%, ACD -5% |
| Armor | Brynhild (2383) | 94 | ok | Brynhild: +10% vs all classes, +10% MATK, HP +20/lv, unbreakable (lv94) |
| Garment | Temporal Transcendence Manteau (20939) | 99 | ok | Temporal Transcendence Manteau: ASPD +10%, VCT -10%, -10% fire/water/earth/wind dmg (lv99) |
| Shoes | Pollux Shoes (2400) | 0 | ok | Pollux Shoes: ATK +50, ASPD +10%, HP/SP +10% |
| Accessory | Arquien's Necklace (28429) | 20 | ok | Arquien's Necklace: Cart Revolution +BaseLevel% (+99%) |
| Accessory | Arquien's Necklace (28429) | 20 | ok | second Arquien's Necklace: another +99% |
| Alt weapon | Mace Of Madness (1547) | 0 | ok | Mace of Madness (CR +25%) |
| Card | Heavy Metaling Card (4467) | - | ok | Heavy Metaling Card (shoes): Cart Revolution +50% |

## Whitesmith
Build: **Cart Revolution spam (trans)**. Gear level cap used: 99.

| Slot | Item (Id) | EquipLevelMin | checker status | why |
|---|---|---|---|---|
| Weapon | Paradise Blacksmith Axe (520011) | 45 | ok | Paradise Blacksmith Axe: Cart Revolution +25% at lv90 |
| Shield | Cursed Mad Bunny (28901) | 1 | ok | Cursed Mad Bunny: ASPD +3, ATK/MATK +5% |
| Shadow | Merchant Shadow Pendant (24251) | 1 | ok | Merchant Shadow Pendant: Cart Revolution +20%+ |
| Upper | Gigant Helm (400500) | 50 | NEEDS-FIX | Gigant Helm (trans only): HP +500, Tomahawk skill; set with Armaia Belt = Cart Revolution +200% |
| Mid | Small Devil Horns (18503) | 1 | ok | +5% vs all classes, +10% HP/SP |
| Lower | Arbitrator Shawl (420246) | 1 | ok | ATK +10%, ACD -5% |
| Armor | Brynhild (2383) | 94 | ok | Brynhild: +10% vs all classes, +10% MATK, HP +20/lv, unbreakable (lv94) |
| Garment | Temporal Transcendence Manteau (20939) | 99 | ok | Temporal Transcendence Manteau: ASPD +10%, VCT -10%, -10% fire/water/earth/wind dmg (lv99) |
| Shoes | Pollux Shoes (2400) | 0 | ok | Pollux Shoes: ATK +50, ASPD +10%, HP/SP +10% |
| Accessory | Armaia Belt (490295) | 1 | NEEDS-FIX | Armaia Belt: Cart Revolution +25% with Maximize Power 5; set with Gigant Helm (+200%) |
| Accessory | Arquien's Necklace (28429) | 20 | ok | Arquien's Necklace: Cart Revolution +BaseLevel% (+99%) |
| Alt weapon | Mace Of Madness (1547) | 0 | ok | Mace of Madness (CR +25%) |
| Card | Heavy Metaling Card (4467) | - | ok | Heavy Metaling Card (shoes): Cart Revolution +50% |
| Card | Senior Papila Card (300092) | - | ok | Senior Papila Card (shoes, alternative): CR +50%, HP/SP +10% |

## Alchemist
Build: **Acid Terror**. Gear level cap used: 99.

| Slot | Item (Id) | EquipLevelMin | checker status | why |
|---|---|---|---|---|
| Weapon | Paradise Alchemist Mace (590026) | 45 | ok | Paradise Alchemist Mace: ATK 160, VCT -10%, Acid Terror +25% at lv90 |
| Shield | Cursed Mad Bunny (28901) | 1 | ok | Cursed Mad Bunny: ASPD +3, ATK/MATK +5% |
| Upper | Flaward Hat (400676) | 50 | NEEDS-FIX | Flaward Hat: STR/INT +3, fixed cast -0.2s at +5, Acid Terror/Demonstration +20% at +7, ranged +10% at +11 |
| Mid | Small Devil Horns (18503) | 1 | ok | +5% vs all classes, +10% HP/SP |
| Lower | Arbitrator Shawl (420246) | 1 | ok | ATK +10%, ACD -5% |
| Armor | Brynhild (2383) | 94 | ok | Brynhild: +10% vs all classes, +10% MATK, HP +20/lv, unbreakable (lv94) |
| Garment | Temporal Transcendence Manteau (20939) | 99 | ok | Temporal Transcendence Manteau: ASPD +10%, VCT -10%, -10% fire/water/earth/wind dmg (lv99) |
| Shoes | Paradise Boots (470067) | 10 | ok | Paradise Boots: ranged/melee +10% (Acid Terror counts as ranged), fixed cast -0.3s at lv85 |
| Accessory | Armaia Belt (490295) | 1 | NEEDS-FIX | Armaia Belt: Acid Terror +BaseLevel% (+99%), DEX/INT +3; wear two |
| Accessory | Armaia Belt (490295) | 1 | NEEDS-FIX | second Armaia Belt: another +99% Acid Terror |
| Alt weapon | Crimson Mace (16040) | 70 | ok | Crimson Mace (lv70, ATK grows with refine) |

## Creator
Build: **Acid Demonstration (Acid Bomb) + Acid Terror**. Gear level cap used: 99.

| Slot | Item (Id) | EquipLevelMin | checker status | why |
|---|---|---|---|---|
| Weapon | Paradise Alchemist Mace (590026) | 45 | ok | Paradise Alchemist Mace: VCT -10%, Acid Terror +25% |
| Shield | Cursed Mad Bunny (28901) | 1 | ok | Cursed Mad Bunny: ASPD +3, ATK/MATK +5% |
| Upper | Flaward Hat (400676) | 50 | NEEDS-FIX | Flaward Hat: AD/AT +20% at +7, AD cooldown -0.1s at +9, ranged +10% at +11; set with Chemical Glove = AD +100%, AT +50% |
| Mid | Small Devil Horns (18503) | 1 | ok | +5% vs all classes, +10% HP/SP |
| Lower | Arbitrator Shawl (420246) | 1 | ok | ATK +10%, ACD -5% |
| Armor | Brynhild (2383) | 94 | ok | Brynhild: +10% vs all classes, +10% MATK, HP +20/lv, unbreakable (lv94) |
| Garment | Temporal Transcendence Manteau (20939) | 99 | ok | Temporal Transcendence Manteau: ASPD +10%, VCT -10%, -10% fire/water/earth/wind dmg (lv99) |
| Shoes | Paradise Boots (470067) | 10 | ok | Paradise Boots: ranged +10% (Acid Demonstration is ranged), fixed cast -0.3s |
| Accessory | Chemical Glove (490475) | 70 | NEEDS-FIX | Chemical Glove (trans only): AD +20% per 20 lv (+80%), AT +30% per 20 lv (+120%), ASPD, HIT +20 |
| Accessory | Armaia Belt (490295) | 1 | NEEDS-FIX | Armaia Belt: Acid Terror +99%, DEX/INT +3 |
| Alt weapon | Erde (16000) | 50 | ok | Erde (trans only, lv50, Acid Terror +20%) |

## Taekwon
Build: **Kicks (unarmed)**. Gear level cap used: 60.

| Slot | Item (Id) | EquipLevelMin | checker status | why |
|---|---|---|---|---|
| Shield | Cursed Mad Bunny (28901) | 1 | ok | Cursed Mad Bunny: ASPD +3, ATK/MATK +5% |
| Upper | RWC Champ Crown Second Place (18780) | 1 | ok | +12 all stats, curse/stun immune; best generic top at any level |
| Mid | Small Devil Horns (18503) | 1 | ok | +5% dmg vs all classes, +5% MATK, +10% HP/SP |
| Lower | Arbitrator Shawl (420246) | 1 | ok | ATK +10%, after-cast delay -5% |
| Armor | Half Brynhild (15023) | 47 | ok | Half Brynhild: +5% vs all classes, +5% MATK, HP +20/lv, no knockback (lv47) |
| Garment | Paradise Manteau (480103) | 10 | ok | Paradise Manteau: -20% neutral dmg, HIT, ASPD +10% at lv45 |
| Shoes | Pollux Shoes (2400) | 0 | ok | Pollux Shoes: ATK +50, ASPD +10%, HP/SP +10% |
| Accessory | Half Megingjard (2856) | 47 | ok | Half Megingjard: STR +24 at lv40 (lv47) |
| Accessory | Bakunawa Agimat Tattoo (2910) | 1 | ok | Bakunawa Agimat Tattoo: +7% vs all classes, ASPD +10% |

## Star Gladiator
Build: **Kicks (book)**. Gear level cap used: 99.

| Slot | Item (Id) | EquipLevelMin | checker status | why |
|---|---|---|---|---|
| Weapon | Paradise Taekwon Martial Arts Book (540029) | 45 | ok | Paradise Taekwon Martial Arts Book: ATK 160, melee +10%, Tornado/Turn Kick +25% at lv90 |
| Shield | Cursed Mad Bunny (28901) | 1 | ok | Cursed Mad Bunny: ASPD +3, ATK/MATK +5% |
| Upper | RWC Champ Crown Second Place (18780) | 1 | ok | +12 all stats |
| Mid | Small Devil Horns (18503) | 1 | ok | +5% vs all classes, +10% HP/SP |
| Lower | Arbitrator Shawl (420246) | 1 | ok | ATK +10%, ACD -5% |
| Armor | Brynhild (2383) | 94 | ok | Brynhild: +10% vs all classes, +10% MATK, HP +20/lv, unbreakable (lv94) |
| Garment | Temporal Transcendence Manteau (20939) | 99 | ok | Temporal Transcendence Manteau: ASPD +10%, VCT -10%, -10% fire/water/earth/wind dmg (lv99) |
| Shoes | Pollux Shoes (2400) | 0 | ok | Pollux Shoes: ATK +50, ASPD +10%, HP/SP +10% |
| Accessory | Megingjard (2629) | 94 | ok | Megingjard: STR +59 at lv99 (lv94) |
| Accessory | Badge Of Order Grace (5825) | 0 | ok | Badge of Order Grace: +10% vs all classes, +10% MATK |
| Alt weapon | Paradise Taekwon Power Book (540030) | 45 | ok | Paradise Taekwon Power Book (Heel Drop/Counter Kick) |

## Soul Linker
Build: **Esma (Estin/Estun)**. Gear level cap used: 99.

| Slot | Item (Id) | EquipLevelMin | checker status | why |
|---|---|---|---|---|
| Weapon | Paradise Soul Linker Staff (550037) | 45 | ok | Paradise Soul Linker Staff: MATK 160, VCT -10%, Esma +25% at lv90 |
| Shield | Purified Knight's Shield (28946) | 1 | ok | Purified Knight's Shield: ATK/MATK +5%, ASPD +10%, -10% all-element dmg |
| Upper | F Pecopeco Hairband (5628) | 0 | ok | F Pecopeco Hairband: VCT -25%, ASPD +10%, move speed |
| Mid | Small Devil Horns (18503) | 1 | ok | +5% MATK, +10% HP/SP |
| Lower | Survivor's Orb (19139) | 50 | ok | Survivor's Orb: MATK +2%, VCT -3% |
| Armor | Brynhild (2383) | 94 | ok | Brynhild: MATK +10%, HP +20/lv (lv94) |
| Garment | Temporal Transcendence Manteau (20939) | 99 | ok | Temporal Transcendence Manteau: VCT -10%, ASPD, elemental resist (lv99) |
| Shoes | Moaning of Evil Spirits (470112) | 99 | ok | Moaning of Evil Spirits: MATK +15% (lv99) |
| Accessory | Bawaya Agimat Tattoo (2907) | 1 | ok | Bawaya Agimat Tattoo: MATK +7%, fixed cast -7% |
| Accessory | RJC2012 Spell Necklace (2939) | 1 | ok | RJC2012 Spell Necklace: VCT -20%, no cast interruption |

## Ninja
Build: **Magic ninja (Flaming Petals / Freezing Spear / Wind Blade)**. Gear level cap used: 99.

| Slot | Item (Id) | EquipLevelMin | checker status | why |
|---|---|---|---|---|
| Weapon | Paradise Ninja Punishment Shuriken (650010) | 45 | ok | Paradise Ninja Punishment Shuriken: MATK 180, VCT -10%, ninja spells +20% (+20% more for the big ones at lv90) |
| Upper | F Pecopeco Hairband (5628) | 0 | ok | F Pecopeco Hairband: VCT -25%, ASPD +10%, move speed |
| Mid | Small Devil Horns (18503) | 1 | ok | +5% MATK, +10% HP/SP |
| Lower | Orochimaru's Mask (18948) | 70 | ok | Orochimaru's Mask: Freezing Spear SP -5, Ice Meteor (Hyousyouraku) +20% |
| Armor | Brynhild (2383) | 94 | ok | Brynhild: MATK +10%, HP +20/lv (lv94) |
| Garment | Temporal Transcendence Manteau (20939) | 99 | ok | Temporal Transcendence Manteau: VCT -10%, ASPD, elemental resist (lv99) |
| Shoes | Moaning of Evil Spirits (470112) | 99 | ok | Moaning of Evil Spirits: MATK +15% (lv99) |
| Accessory | Bawaya Agimat Tattoo (2907) | 1 | ok | Bawaya Agimat Tattoo: MATK +7%, fixed cast -7% |
| Accessory | Mercenary Ring Type B (28426) | 99 | ok | Mercenary Ring Type B: INT +3, VCT -30% for Ninja/Gunslinger/Taekwon/SN |
| Alt weapon | Paradise Ninja Crucifixion Shuriken (650011) | 45 | ok | Paradise Ninja Crucifixion Shuriken (physical: Kunai/Huuma) |

## Gunslinger
Build: **Desperado / Rapid Shower (revolver)**. Gear level cap used: 99.

| Slot | Item (Id) | EquipLevelMin | checker status | why |
|---|---|---|---|---|
| Weapon | Paradise Gunslinger Revolver (800005) | 45 | ok | Paradise Gunslinger Revolver: ATK 180, ASPD +10%, Rapid Shower +20%, Desperado +20% at lv90 |
| Upper | RWC Champ Crown Second Place (18780) | 1 | ok | +12 all stats (DEX/AGI) |
| Mid | Small Devil Horns (18503) | 1 | ok | +5% vs all classes |
| Lower | Arbitrator Shawl (420246) | 1 | ok | ATK +10%, ACD -5% |
| Armor | Brynhild (2383) | 94 | ok | Brynhild: +10% vs all classes (lv94) |
| Garment | Fallen Angel Wing (2589) | 0 | ok | Fallen Angel Wing: all stats +1, ranged dmg +1% per 20 DEX, ASPD per AGI |
| Shoes | Paradise Boots (470067) | 10 | ok | Paradise Boots: melee/ranged dmg +10%, crit, fixed cast -0.3s at lv85 |
| Accessory | Mercenary Ring Type A (28425) | 99 | ok | Mercenary Ring Type A: VIT +3, HP +1000, SP +200 for Gunslinger |
| Accessory | Badge Of Order Grace (5825) | 0 | ok | Badge of Order Grace: +10% vs all classes |
| Alt weapon | Heaven's Feather & Hell's Fire (13120) | 99 | ok | Heaven's Feather & Hell's Fire (lv99, Desperado +20%) |

## Super Novice
Build: **Magic (bolts)**. Gear level cap used: 99.

| Slot | Item (Id) | EquipLevelMin | checker status | why |
|---|---|---|---|---|
| Weapon | Paradise Super Novice Staff (550040) | 45 | ok | Paradise Super Novice Staff: MATK 160, VCT -10%, Fire/Cold/Lightning Bolt +40% at lv90 |
| Shield | Purified Knight's Shield (28946) | 1 | ok | Purified Knight's Shield: ATK/MATK +5%, ASPD +10%, -10% all-element dmg |
| Upper | F Pecopeco Hairband (5628) | 0 | ok | F Pecopeco Hairband: VCT -25%, ASPD +10%, move speed |
| Mid | Small Devil Horns (18503) | 1 | ok | +5% MATK, +10% HP/SP |
| Lower | Survivor's Orb (19139) | 50 | ok | Survivor's Orb: MATK +2%, VCT -3% |
| Armor | Brynhild (2383) | 94 | ok | Brynhild: MATK +10%, HP +20/lv (lv94) |
| Garment | Temporal Transcendence Manteau (20939) | 99 | ok | Temporal Transcendence Manteau: VCT -10%, ASPD, elemental resist (lv99) |
| Shoes | Moaning of Evil Spirits (470112) | 99 | ok | Moaning of Evil Spirits: MATK +15% (lv99) |
| Accessory | Bawaya Agimat Tattoo (2907) | 1 | ok | Bawaya Agimat Tattoo: MATK +7%, fixed cast -7% |
| Accessory | Mercenary Ring Type B (28426) | 99 | ok | Mercenary Ring Type B: INT +3, VCT -30% for Super Novice |
| Alt weapon | Paradise Super Novice Sword (500035) | 45 | ok | Paradise Super Novice Sword (melee, Bash +40%) |

## Acid Demonstration / Acid Terror consumable packs
Acid Terror uses 1 Acid Bottle (7136, ok). Acid Demonstration uses 1 Acid Bottle + 1 Bottle Grenade (7135, ok).

| Item (Id) | Aegis | checker status | contents (from Script / item_group_db) |
|---|---|---|---|
| Acidbomb Box500 (17070) | Acidbomb_Box500 | ok | 500 Acid Bottle + 500 Bottle Grenade |
| Acidbomb Box100 (17069) | Acidbomb_Box100 | ok | 100 Acid Bottle + 100 Bottle Grenade |
| Acidbomb Box50 (17068) | Acidbomb_Box50 | ok | group ACIDBOMB_BOX50: 50 Bottle Grenade + 50 Acid Bottle |
| Acid Bomb 10 Box (13989) | Acidbomb_10_Box | ok | group ACIDBOMB_10_BOX: 10 Bottle Grenade + 10 Acid Bottle |
| Acid Bomb 500 Box (200056) | C_Acid_B_500_Box | ok | group C_ACID_B_500_BOX: 500 Acid Bottle + 11 K_Secret_Key (no Bottle Grenade: Acid Terror only) |
| Acid Bomb 50 Box (200055) | C_Acid_B_50Box | ok | group C_ACID_B_50BOX: 50 Acid Bottle + K_Secret_Key (Acid Terror only) |

Best for the shop: **17070** (500+500) and **17069** (100+100). 200055/200056 give Acid Bottles only (plus K_Secret_Key), so they only feed Acid Terror.

## NEEDS-FIX (client pictures missing)
| Item (Id) | problem | look-alike Id (ok) | look-alike name |
|---|---|---|---|
| Hat of Desert (400512) | NOINFO | 2222 | Turban |
| Kenshi Gauntlet (490282) | NOINFO | 2780 | Dark Knight Glove |
| Imperial Feather (18823) | iNsN | 5074 | Angel Wing Ears |
| Imperial Ring (28372) | iNsN | 2601 | Ring |
| Double Badge (490236) | NOINFO | 2733 | Sheriff Badge |
| Falconer Claw (28321) | iNsN | 2667 | Renown Archer's Gloves |
| Falconer Glove (28322) | iNsN | 2604 | Glove |
| Emerald Earrings (28411) | iNsN | 2602 | Earring |
| Boxer Glove (490399) | NOINFO | 28434 | Boxing Gloves |
| Shadow Ring (28379) | iNsN | 2601 | Ring |
| Gigant Helm (400500) | NOINFO | 5017 | Bone Helm |
| Armaia Belt (490295) | NOINFO | 2627 | Belt |
| Flaward Hat (400676) | NOINFO | 5679 | Engineer Cap |
| Chemical Glove (490475) | NOINFO | 2854 | Alchemy Glove |

`NOINFO` = no entry in the client item info (no name, no picture). `iNsN` = entry exists but icon and drop sprite are missing.

## Machine-readable
```yaml
sets:
  - class: Swordman
    items: [13402, 28901, 18780, 18503, 420246, 15023, 480103, 2400, 2856, 2910]
    alt_weapons: [1135]
  - class: Knight / Lord Knight
    items: [1188, 400512, 18503, 420246, 2383, 20939, 2400, 490282, 5825]
    alt_weapons: [600020]
  - class: Crusader / Paladin
    items: [500033, 28946, 18780, 18823, 420246, 2383, 20939, 2400, 28372, 5825]
    alt_weapons: [530017]
  - class: Mage
    items: [550032, 28946, 5628, 18503, 19139, 15023, 20903, 470068, 2907, 2939]
  - class: Wizard / High Wizard
    items: [550034, 28946, 5628, 18503, 19139, 2383, 20939, 470112, 2907, 2939]
    alt_weapons: [2000]
  - class: Sage / Professor
    items: [540027, 28946, 5547, 18503, 19139, 2383, 20939, 470112, 2907, 2939]
    alt_weapons: [540028]
  - class: Archer
    items: [1744, 18780, 18503, 420246, 15023, 2589, 470067, 490236, 5825]
    alt_weapons: [700036]
  - class: Hunter / Sniper
    items: [700039, 18780, 18503, 18985, 2383, 2589, 470067, 28321, 28322]
    alt_weapons: [1745]
  - class: Bard / Clown
    items: [570021, 18780, 18503, 420246, 2383, 2589, 470067, 28411, 28411]
    alt_weapons: [1939]
  - class: Dancer / Gypsy
    items: [580021, 18780, 18503, 420246, 2383, 2589, 470067, 28411, 28411]
    alt_weapons: [1995]
  - class: Acolyte
    items: [550032, 28946, 19211, 18503, 19139, 15023, 20903, 470068, 2607, 28432]
  - class: Priest / High Priest
    items: [1631, 2129, 5628, 18503, 19139, 2383, 20939, 470112, 2626, 28432]
    alt_weapons: [550036]
  - class: Monk / Champion
    items: [560022, 18780, 18503, 420246, 2383, 20939, 2400, 490399, 5825]
    alt_weapons: [1822]
  - class: Thief
    items: [13402, 28901, 18780, 18503, 420246, 15023, 480103, 2400, 2856, 2910]
    alt_weapons: [510035]
  - class: Assassin / Assassin Cross
    items: [610025, 18780, 18503, 420246, 2383, 20939, 2400, 2629, 5825]
    alt_weapons: [28007]
  - class: Rogue / Stalker
    items: [510036, 28901, 18780, 18503, 420246, 2383, 20939, 2400, 28379, 28379]
    alt_weapons: [13038]
  - class: Merchant
    items: [1547, 28901, 24251, 18780, 18503, 420246, 15023, 480103, 2400, 28429, 28429]
    alt_weapons: [520010]
    cards: [4467]
  - class: Blacksmith
    items: [520011, 28901, 24251, 18780, 18503, 420246, 2383, 20939, 2400, 28429, 28429]
    alt_weapons: [1547]
    cards: [4467]
  - class: Whitesmith
    items: [520011, 28901, 24251, 400500, 18503, 420246, 2383, 20939, 2400, 490295, 28429]
    alt_weapons: [1547]
    cards: [4467, 300092]
  - class: Alchemist
    items: [590026, 28901, 400676, 18503, 420246, 2383, 20939, 470067, 490295, 490295]
    alt_weapons: [16040]
  - class: Creator
    items: [590026, 28901, 400676, 18503, 420246, 2383, 20939, 470067, 490475, 490295]
    alt_weapons: [16000]
  - class: Taekwon
    items: [28901, 18780, 18503, 420246, 15023, 480103, 2400, 2856, 2910]
  - class: Star Gladiator
    items: [540029, 28901, 18780, 18503, 420246, 2383, 20939, 2400, 2629, 5825]
    alt_weapons: [540030]
  - class: Soul Linker
    items: [550037, 28946, 5628, 18503, 19139, 2383, 20939, 470112, 2907, 2939]
  - class: Ninja
    items: [650010, 5628, 18503, 18948, 2383, 20939, 470112, 2907, 28426]
    alt_weapons: [650011]
  - class: Gunslinger
    items: [800005, 18780, 18503, 420246, 2383, 2589, 470067, 28425, 5825]
    alt_weapons: [13120]
  - class: Super Novice
    items: [550040, 28946, 5628, 18503, 19139, 2383, 20939, 470112, 2907, 28426]
    alt_weapons: [500035]
acid_packs: [17070, 17069, 17068, 13989, 200056, 200055]
needs_fix: {400512: 2222, 490282: 2780, 18823: 5074, 28372: 2601, 490236: 2733, 28321: 2667, 28322: 2604, 28411: 2602, 490399: 28434, 28379: 2601, 400500: 5017, 490295: 2627, 400676: 5679, 490475: 2854}
```
