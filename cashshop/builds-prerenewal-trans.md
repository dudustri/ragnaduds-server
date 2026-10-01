# Pre-Renewal Cash Shop Gear - Transcendent & Extended Classes

Server: rAthena **pre-renewal**, max lv 99/70, 10x/10x/3x. Every item and card below was checked against `db/pre-re/item_db_equip.yml` / `item_db_etc.yml` (existence, slot count vs. cards, equip location, `Jobs`, `Classes` (trans-only), `Gender`, `EquipLevelMin`, and `item_noequip.txt`). Item format: `Name [slots] (Id)`.

## Sources

- iRO Wiki Classic class pages (main source for builds & gear lists): https://irowiki.org/classic/Lord_Knight , https://irowiki.org/classic/Paladin , https://irowiki.org/classic/High_Wizard , https://irowiki.org/classic/Sniper , https://irowiki.org/classic/Assassin_Cross , https://irowiki.org/classic/Champion , https://irowiki.org/classic/High_Priest , https://irowiki.org/classic/Creator , https://irowiki.org/classic/Whitesmith , https://irowiki.org/classic/Stalker , https://irowiki.org/classic/Gunslinger , https://irowiki.org/classic/Ninja
- RateMyServer write-ups (found via search, used for build archetypes only, not read in full): https://write.ratemyserver.net/ragnoark-online-character-guides/lord-knight-a-comprehensive-guide-for-pvmwoepvp/ , https://write.ratemyserver.net/ragnoark-online-character-guides/the-lord-knight-pure-bowling-bash-build/ , https://write.ratemyserver.net/ragnoark-online-character-guides/pvpwoe-sonic-blow-assassin-cross-build/ , https://write.ratemyserver.net/ragnoark-online-character-guides/high-wizard-study-memorize-dominate/
- bRO (Brazilian) references: bROWiki Arquivo https://arquivo.browiki.org/wiki/Cavaleiros (build archetypes Esgrimistas/Lanceiros), https://arquivo.browiki.org/wiki/Mercen%C3%A1rios , https://arquivo.browiki.org/wiki/Arquimagos ; BR pre-re private-server guides: https://ragnamelody.directorioforuns.com/t7-guia-de-magos-bruxos-e-arquimagos (Arquimago), https://www2.worldrag.com/forum/topic/76400-guia-sumo-sacerdote/ (Sumo Sacerdote, pre-re Fenix server)
- Steam guide "Guia Geral de Lorde (Pré-Renovação)": https://steamcommunity.com/sharedfiles/filedetails/?id=382666810 (rate-limited, could not be read)

### How to read this / caveats

- **mid** tier = base lv ~70-90, common/affordable gear (nothing above lv 90 to equip). **end** tier = lv 99 best-in-slot for PvM on a friends server; WoE-only variants are noted.
- Current bROWiki pages are Renewal-era and most BR pre-re private-server guides rely on **custom donate gear** (Hades/Deuses sets, 4-slot headgears) that does not exist in rAthena. From bRO I only took the build archetypes and the item/card picks that exist in this DB (e.g. Robo Eye, Imp/Siroma bolt cards, Evil Snake Lord card, Kiel-D-01, Diabolus set).
- Weapon cards: swap race/size cards per target (Hydra = Demi-Human, Minorous = Large, Skeleton Worker = Medium, Abysmal Knight = Boss). The table shows one sensible default.
- "trans-only" items (Classes: Upper) cannot be worn by Star Gladiator, Soul Linker, Ninja, Gunslinger or Super Novice. Most "all jobs" gear excludes Novice/Super Novice in this DB, so Super Novice gets its own Angel set.
- Refine targets: weapons +7~+10, armor pieces +7 (safe +4) unless the note says otherwise.

## Contents

- **Lord Knight**: Spear Pierce / Brandish (STR/VIT/DEX, Peco) | Two-Hand Quicken / Bowling Bash (STR/AGI)
- **Paladin**: Grand Cross (INT/VIT/DEX) | Shield Chain / Devotion tank (STR/VIT/DEX)
- **High Wizard**: Storm Gust / Jupitel Thunder (INT/DEX full caster) | WoE / Glass Cannon (INT/DEX, Meteor/SG, anti-player)
- **Scholar (Professor)**: Double Bolt caster (INT/DEX, Double Casting / Soul Burn) | WoE / Party support (Dispel, Land Protector, Spider Web, Magic Rod) VIT/DEX/INT
- **Sniper**: AGI/DEX Double Strafe (with auto-Blitz) | Falconer / Sharp Shooting (DEX/LUK/INT)
- **Clown (Minstrel)**: Arrow Vulcan (DEX/AGI/STR) | Support / Ensemble (VIT/DEX/INT)
- **Gypsy**: Arrow Vulcan (DEX/AGI/STR) | Support / Ensemble (VIT/DEX/INT)
- **High Priest**: Full Support (INT/VIT/DEX) | Battle Priest (STR/AGI/DEX, mace)
- **Champion**: Asura Strike / Guillotine Fist (STR/INT/DEX) | Combo (Triple Attack > Chain > Combo Finish) STR/AGI/DEX
- **Assassin Cross**: Sonic Blow katar (STR/AGI/DEX, EDP) | Soul Destroyer (STR/INT/DEX)
- **Stalker**: Melee dagger (STR/AGI/DEX, Sidewinder double attack) | Bow / Divest (DEX, Full Strip + Double Strafe)
- **Whitesmith (Mastersmith)**: Cart Termination (STR/DEX, Cart Boost + Maximize Power) | Battle Axe / Hammerfall (STR/AGI, Adrenaline + Weapon Perfection)
- **Creator (Biochemist)**: Acid Demonstration "Bomber" (INT/DEX/AGI 25) | Potion Pitcher / FCP support (VIT/DEX)
- **Star Gladiator**: Melee Union / Warm Wind (STR/AGI/DEX) with book
- **Soul Linker**: Esma / Kaahi support caster (INT/DEX)
- **Ninja**: Magic Ninja (INT/DEX, ninjutsu) | Throwing Huuma (STR/DEX)
- **Gunslinger**: Desperado revolver (DEX/VIT/INT) | Lever Action crit rifle (AGI/DEX/LUK)
- **Super Novice**: Battle Super Novice (STR/AGI/DEX, Angel set)

## Lord Knight

_Equip-check identity: base job `Knight`, class type `Upper`._

### Lord Knight - Spear Pierce / Brandish (STR/VIT/DEX, Peco)

Source/basis: irowiki classic LK (SVD build), bRO "Lanceiros"

**Mid tier (lv ~70-90)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Pike [4] (1408) | 4x Minorous (4126) | Pike [4]: 4x Minorous (+15% vs Large, Pierce hits Large hardest); 4x Hydra for PvP |
| Shield / Left hand | Buckler [1] (2104) | Thara Frog (4058) | Buckler [1], Thara Frog |
| Upper head | Bone Helm [1] (5162) | Nightmare (4127) | Bone Helm [1] (lv70), Nightmare (sleep immunity, AGI+1) |
| Mid head | Angel Wing Ears [0] (5074) | - | Angel Wing Ears: STR+1 (lv70) |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil: DEX+2, HIT+3 |
| Armor | Full Plate [1] (2317) | Peco Peco (4031) | Full Plate [1], Peco Peco |
| Garment | Manteau [1] (2506) | Raydric (4133) | Manteau [1], Raydric |
| Shoes | Boots [1] (2406) | Verit (4107) | Boots [1], Verit |
| Accessory 1 | Clip [1] (2607) | Mantis (4079) | Clip [1], Mantis (STR+3) |
| Accessory 2 | Clip [1] (2607) | Mantis (4079) | Clip [1], Mantis |

**Endgame (lv 99)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Hunting Spear [1] (1422) | Hydra (4035) | Hunting Spear [1] +10 (trans-only, ignores Brute DEF); Hydra (or Abysmal Knight for MVP) |
| Shield / Left hand | Valkyrja's Shield [1] (2115) | Thara Frog (4058) | Valkyrja's Shield [1], Thara Frog |
| Upper head | Orc Hero Headdress [1] (5375) | Vanberk (4411) | Orc Hero Headdress [1] (top+mid, STR+2, autocasts Weapon Perfection); Vanberk |
| Mid head | (covered by upper headgear) | - | - |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Valkyrian Armor [1] (2357) | Peco Peco (4031) | Valkyrian Armor [1] +7~9, Peco Peco (+10% MaxHP); Marc for freeze immunity |
| Garment | Valkyrian Manteau [1] (2524) | Raydric (4133) | Valkyrian Manteau [1], Raydric (-20% Neutral) |
| Shoes | Sleipnir [0] (2410) | - | Sleipnir: +20% HP/SP, +25% move speed (lv94) |
| Accessory 1 | Megingjard [0] (2629) | - | Megingjard: STR+40 (lv94) |
| Accessory 2 | Brisingamen [0] (2630) | - | Brisingamen: STR/AGI/VIT/INT+6, LUK+10 (lv94) |

### Lord Knight - Two-Hand Quicken / Bowling Bash (STR/AGI)

Source/basis: irowiki classic LK (ASPD/Hybrid), bRO "Esgrimistas"

**Mid tier (lv ~70-90)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Claymore [2] (1172) | Skeleton Worker (4092) + Minorous (4126) | Claymore [2]: Skeleton Worker + Minorous (Medium/Large coverage) |
| Shield / Left hand | (two-handed weapon) | - | - |
| Upper head | Bone Helm [1] (5162) | Nightmare (4127) | Bone Helm [1], Nightmare |
| Mid head | Angel Wing Ears [0] (5074) | - | Angel Wing Ears |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Full Plate [1] (2317) | Peco Peco (4031) | Full Plate [1], Peco Peco |
| Garment | Manteau [1] (2506) | Raydric (4133) | Manteau [1], Raydric |
| Shoes | Boots [1] (2406) | Matyr (4097) | Boots [1], Matyr (AGI+1, HP+10%) |
| Accessory 1 | Clip [1] (2607) | Mantis (4079) | Clip [1], Mantis |
| Accessory 2 | Clip [1] (2607) | Kukre (4027) | Clip [1], Kukre (AGI+2) |

**Endgame (lv 99)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Violet Fear [2] (1185) | Minorous (4126) + Skeleton Worker (4092) | Violet Fear [2] (trans-only, 275 ATK, autocast Meteor/Frost Nova); Minorous + Skeleton Worker. Alt: Muramasa (crit/ASPD) |
| Shield / Left hand | (two-handed weapon) | - | - |
| Upper head | Orc Hero Headdress [1] (5375) | Vanberk (4411) | Orc Hero Headdress [1], Vanberk |
| Mid head | (covered by upper headgear) | - | - |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Valkyrian Armor [1] (2357) | Peco Peco (4031) | Valkyrian Armor [1] +7~9, Peco Peco (+10% MaxHP); Marc for freeze immunity |
| Garment | Valkyrian Manteau [1] (2524) | Raydric (4133) | Valkyrian Manteau [1], Raydric (-20% Neutral) |
| Shoes | Sleipnir [0] (2410) | - | Sleipnir: +20% HP/SP, +25% move speed (lv94) |
| Accessory 1 | Megingjard [0] (2629) | - | Megingjard: STR+40 (lv94) |
| Accessory 2 | Brisingamen [0] (2630) | - | Brisingamen: STR/AGI/VIT/INT+6, LUK+10 (lv94) |

## Paladin

_Equip-check identity: base job `Crusader`, class type `Upper`._

### Paladin - Grand Cross (INT/VIT/DEX)

Source/basis: irowiki classic Paladin (GC Mobber / GC FS)

**Mid tier (lv ~70-90)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Holy Avenger [0] (1145) | - | Holy Avenger (Crusader-only, Holy, VIT+2) +7~10 |
| Shield / Left hand | Sacred Mission [1] (2128) | Khalitzburg (4136) | Sacred Mission [1] (VIT+3 INT+2), Khalitzburg (-30% Demon; swap Thara for PvP) |
| Upper head | Crown of Mistress [0] (5081) | - | Crown of Mistress: INT+2, SP+100 (lv75) |
| Mid head | Sunglasses [1] (2202) | Elder Willow (4052) | Sunglasses [1], Elder Willow (INT+2) |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Legion Plate Armor [1] (2342) | Angeling (4054) | Legion Plate Armor [1], Angeling (Holy armor = no GC self-damage) |
| Garment | Manteau [1] (2506) | Raydric (4133) | Manteau [1], Raydric |
| Shoes | Boots [1] (2406) | Verit (4107) | Boots [1], Verit (HP/SP +8%) |
| Accessory 1 | Earring [0] (2602) | - | Earring: INT+2 |
| Accessory 2 | Earring [0] (2602) | - | Earring: INT+2 |

**Endgame (lv 99)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Holy Avenger [0] (1145) | - | Holy Avenger +10 |
| Shield / Left hand | Sacred Mission [1] (2128) | Thara Frog (4058) | Sacred Mission [1], Thara Frog (Khalitzburg for Demon-heavy maps) |
| Upper head | Diadem [1] (5313) | Evil Snake Lord (4330) | Diadem [1] (top+mid; INT+1, MATK+3%, cast -3%), Evil Snake Lord (INT+3) |
| Mid head | (covered by upper headgear) | - | - |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Valkyrian Armor [1] (2357) | Angeling (4054) | Valkyrian Armor [1], Angeling (keep Holy armor for GC) |
| Garment | Valkyrian Manteau [1] (2524) | Raydric (4133) | Valkyrian Manteau [1], Raydric |
| Shoes | Sleipnir [0] (2410) | - | Sleipnir |
| Accessory 1 | Earring [1] (2622) | Phen (4077) | Earring [1] (lv90), Phen (no cast interruption) |
| Accessory 2 | Brisingamen [0] (2630) | - | Brisingamen (INT+6) |

### Paladin - Shield Chain / Devotion tank (STR/VIT/DEX)

Source/basis: irowiki classic Paladin (Battle / tank equipment set)

**Mid tier (lv ~70-90)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Pike [4] (1408) | 4x Hydra (4035) | Pike [4], 4x Hydra (cards on weapon also boost Shield Chain) |
| Shield / Left hand | Cross Shield [1] (2130) | Thara Frog (4058) | Cross Shield [1] (+30% Shield Chain, STR+1; refine it - Shield Chain scales with shield refine/weight), Thara Frog |
| Upper head | Helm [1] (2229) | Nightmare (4127) | Helm [1], Nightmare |
| Mid head | Angel Wing Ears [0] (5074) | - | Angel Wing Ears |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Legion Plate Armor [1] (2342) | Peco Peco (4031) | Legion Plate Armor [1], Peco Peco |
| Garment | Pauldron [1] (2514) | Raydric (4133) | Pauldron [1] (lv80), Raydric |
| Shoes | Boots [1] (2406) | Green Ferus (4381) | Boots [1], Green Ferus (VIT+1, HP+10%) |
| Accessory 1 | Clip [1] (2607) | Mantis (4079) | Clip [1], Mantis |
| Accessory 2 | Clip [1] (2607) | Mantis (4079) | Clip [1], Mantis |

**Endgame (lv 99)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Hunting Spear [1] (1422) | Hydra (4035) | Hunting Spear [1], Hydra |
| Shield / Left hand | Cross Shield [1] (2130) | Thara Frog (4058) | Cross Shield [1] +10, Thara Frog |
| Upper head | Orc Hero Headdress [1] (5375) | Vanberk (4411) | Orc Hero Headdress [1], Vanberk |
| Mid head | (covered by upper headgear) | - | - |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Valkyrian Armor [1] (2357) | Peco Peco (4031) | Valkyrian Armor [1] +7~9, Peco Peco (+10% MaxHP); Marc for freeze immunity |
| Garment | Valkyrian Manteau [1] (2524) | Raydric (4133) | Valkyrian Manteau [1], Raydric (-20% Neutral) |
| Shoes | Sleipnir [0] (2410) | - | Sleipnir: +20% HP/SP, +25% move speed (lv94) |
| Accessory 1 | Megingjard [0] (2629) | - | Megingjard: STR+40 (lv94) |
| Accessory 2 | Brisingamen [0] (2630) | - | Brisingamen: STR/AGI/VIT/INT+6, LUK+10 (lv94) |

## High Wizard

_Equip-check identity: base job `Wizard`, class type `Upper`._

### High Wizard - Storm Gust / Jupitel Thunder (INT/DEX full caster)

Source/basis: irowiki classic HW (Pure PvM), ragnamelody BR Arquimago guide

**Mid tier (lv ~70-90)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Wing Staff [0] (1616) | - | Wing Staff: MATK+15%, cast -5% |
| Shield / Left hand | Magic Bible Vol1 [1] (2131) | Thara Frog (4058) | Magic Bible Vol1 [1] (INT+2, lv70), Thara Frog |
| Upper head | Mage Hat [0] (5027) | - | Mage Hat: INT+2, SP+150 |
| Mid head | Robo Eye [0] (5325) | - | Robo Eye: DEX+1, MATK+2% |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil: DEX+2 |
| Armor | Robe of Cast [1] (2360) | Evil Druid (4141) | Robe of Cast [1] (cast -3%, lv75), Evil Druid (INT+1) |
| Garment | Muffler [1] (2504) | Raydric (4133) | Muffler [1], Raydric |
| Shoes | Shoes [1] (2404) | Verit (4107) | Shoes [1], Verit |
| Accessory 1 | Glove [0] (2604) | - | Glove: DEX+2 |
| Accessory 2 | Earring [0] (2602) | - | Earring: INT+2 |

**Endgame (lv 99)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | La'cryma Stick [2] (1646) | - | La'cryma Stick [2] +10 (trans-only; INT+4, MATK+15%, Storm Gust dmg +refine%, faster SG at +10). Slots left open (no generic MATK weapon card in pre-re) |
| Shield / Left hand | Valkyrja's Shield [1] (2115) | Thara Frog (4058) | Valkyrja's Shield [1], Thara Frog |
| Upper head | Diadem [1] (5313) | Kathryne Keyron (4366) | Diadem [1] (top+mid), Kathryne Keyron (cast -1%/refine, MATK+2% at +9) |
| Mid head | (covered by upper headgear) | - | - |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Valkyrian Armor [1] (2357) | Marc (4105) | Valkyrian Armor [1]; Marc (freeze immunity) or Evil Druid (INT+1, undead armor) |
| Garment | Valkyrian Manteau [1] (2524) | Raydric (4133) | Valkyrian Manteau [1], Raydric |
| Shoes | Sleipnir [0] (2410) | - | Sleipnir |
| Accessory 1 | Orleans's Glove [1] (2701) | Phen (4077) | Orleans's Glove [1] (DEX+2, MATK+3%), Phen (uninterruptible cast) |
| Accessory 2 | Brisingamen [0] (2630) | - | Brisingamen (INT+6) |

### High Wizard - WoE / Glass Cannon (INT/DEX, Meteor/SG, anti-player)

Source/basis: irowiki classic HW (WoE Glass Cannon) - gear list taken verbatim

**Mid tier (lv ~70-90)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Survivor's Rod [1] (1618) | - | Survivor's Rod [1] (DEX+3, MATK+15%, HP+400) |
| Shield / Left hand | Guard [1] (2102) | Thara Frog (4058) | Guard [1], Thara Frog |
| Upper head | Feather Beret [0] (5170) | - | Feather Beret (-10% Demi-Human) |
| Mid head | Sunglasses [1] (2202) | Nightmare (4127) | Sunglasses [1], Nightmare |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Robe of Cast [1] (2360) | Marc (4105) | Robe of Cast [1], Marc |
| Garment | Muffler [1] (2504) | Raydric (4133) | Muffler [1], Raydric |
| Shoes | Shoes [1] (2404) | Verit (4107) | Shoes [1], Verit |
| Accessory 1 | Glove [0] (2604) | - | Glove |
| Accessory 2 | Earring [0] (2602) | - | Earring |

**Endgame (lv 99)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Warlock's Battle Wand [0] (1633) | - | Warlock's Battle Wand (WoE reward wand) |
| Shield / Left hand | Valkyrja's Shield [1] (2115) | Flame Skull (4439) | Valkyrja's Shield [1], Flame Skull (status resist) |
| Upper head | Parade Hat [1] (5225) | Stalactic Golem (4223) | Parade Hat [1] (STR+2, MDEF+2, autocast Angelus/Assumptio when hit), Stalactic Golem |
| Mid head | Sunglasses [1] (2202) | Stalactic Golem (4223) | Sunglasses [1], Stalactic Golem (stun resist) |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Warlock's Battle Robe [1] (2379) | Marc (4105) | Warlock's Battle Robe [1], Marc (or Evil Druid) |
| Garment | Commander's Manteau [1] (2539) | Salamander (4429) | Commander's Manteau [1], Salamander (+40% Meteor/Fire Pillar) or Raydric/Noxious |
| Shoes | Combat Boots [1] (2436) | Zombie Slaughter (4435) | Combat Boots [1], Zombie Slaughter |
| Accessory 1 | Orleans's Glove [1] (2701) | Zerom (4064) | Orleans's Glove [1], Zerom |
| Accessory 2 | Glove [1] (2624) | Smokie (4044) | Glove [1], Smokie (Hiding) |

## Scholar (Professor)

_Equip-check identity: base job `Sage`, class type `Upper`._

### Scholar (Professor) - Double Bolt caster (INT/DEX, Double Casting / Soul Burn)

Source/basis: irowiki classic Professor + bRO Sábios pages; Imp/Siroma bolt cards are a bRO-favourite trick

**Mid tier (lv ~70-90)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Sage's Diary [2] (1560) | - | Sage's Diary [2]: MATK+15% (+5% more at INT>=70) |
| Shield / Left hand | Magic Bible Vol1 [1] (2131) | Thara Frog (4058) | Magic Bible Vol1 [1], Thara Frog |
| Upper head | Mage Hat [0] (5027) | - | Mage Hat: INT+2, SP+150 |
| Mid head | Robo Eye [0] (5325) | - | Robo Eye |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Robe of Cast [1] (2360) | Evil Druid (4141) | Robe of Cast [1], Evil Druid |
| Garment | Muffler [1] (2504) | Raydric (4133) | Muffler [1], Raydric |
| Shoes | Shoes [1] (2404) | Verit (4107) | Shoes [1], Verit |
| Accessory 1 | Clip [1] (2607) | Imp (4433) | Clip [1], Imp (Fire Bolt +25% dmg, -25% cast) |
| Accessory 2 | Clip [1] (2607) | Siroma (4416) | Clip [1], Siroma (Cold Bolt +25% dmg, -25% cast) |

**Endgame (lv 99)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Staff of Piercing [0] (1644) | - | Staff of Piercing +10 (trans-only; INT+4, MATK+15%, ignores 10%+refine MDEF) |
| Shield / Left hand | Valkyrja's Shield [1] (2115) | Thara Frog (4058) | Valkyrja's Shield [1], Thara Frog |
| Upper head | Diadem [1] (5313) | Evil Snake Lord (4330) | Diadem [1] (top+mid), Evil Snake Lord (INT+3) |
| Mid head | (covered by upper headgear) | - | - |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Valkyrian Armor [1] (2357) | Marc (4105) | Valkyrian Armor [1]; Marc (freeze immunity) or Evil Druid (INT+1, undead armor) |
| Garment | Valkyrian Manteau [1] (2524) | Raydric (4133) | Valkyrian Manteau [1], Raydric |
| Shoes | Sleipnir [0] (2410) | - | Sleipnir |
| Accessory 1 | Orleans's Glove [1] (2701) | Imp (4433) | Orleans's Glove [1], Imp (or Siroma for Cold Bolt element) |
| Accessory 2 | Brisingamen [0] (2630) | - | Brisingamen (INT+6) |

### Scholar (Professor) - WoE / Party support (Dispel, Land Protector, Spider Web, Magic Rod) VIT/DEX/INT

Source/basis: irowiki classic Professor / bRO "Sábios" support

**Mid tier (lv ~70-90)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Survivor's Rod [1] (1618) | - | Survivor's Rod [1] (DEX+3, HP+400) |
| Shield / Left hand | Magic Bible Vol1 [1] (2131) | Thara Frog (4058) | Magic Bible Vol1 [1], Thara Frog |
| Upper head | Feather Beret [0] (5170) | - | Feather Beret |
| Mid head | Sunglasses [1] (2202) | Nightmare (4127) | Sunglasses [1], Nightmare |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Robe of Cast [1] (2360) | Marc (4105) | Robe of Cast [1], Marc |
| Garment | Muffler [1] (2504) | Raydric (4133) | Muffler [1], Raydric |
| Shoes | Shoes [1] (2404) | Green Ferus (4381) | Shoes [1], Green Ferus |
| Accessory 1 | Clip [1] (2607) | Phen (4077) | Clip [1], Phen (no cast interruption) |
| Accessory 2 | Rosary [0] (2608) | - | Rosary: MDEF+5, LUK+2 |

**Endgame (lv 99)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Survivor's Rod [1] (1618) | - | Survivor's Rod [1] +10 (HP matters more than MATK here) |
| Shield / Left hand | Valkyrja's Shield [1] (2115) | Thara Frog (4058) | Valkyrja's Shield [1], Thara Frog |
| Upper head | Feather Beret [0] (5170) | - | Feather Beret |
| Mid head | Sunglasses [1] (2202) | Nightmare (4127) | Sunglasses [1], Nightmare |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Warlock's Battle Robe [1] (2379) | Marc (4105) | Warlock's Battle Robe [1], Marc |
| Garment | Commander's Manteau [1] (2539) | Raydric (4133) | Commander's Manteau [1], Raydric |
| Shoes | Combat Boots [1] (2436) | Green Ferus (4381) | Combat Boots [1], Green Ferus |
| Accessory 1 | Orleans's Glove [1] (2701) | Phen (4077) | Orleans's Glove [1], Phen |
| Accessory 2 | Rosary [1] (2626) | Alligator (4252) | Rosary [1] (lv90), Alligator (-5% ranged) |

## Sniper

_Equip-check identity: base job `Hunter`, class type `Upper`._

### Sniper - AGI/DEX Double Strafe (with auto-Blitz)

Source/basis: irowiki classic Sniper (DEX/AGI Power House), BR guides

**Mid tier (lv ~70-90)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Composite Bow [4] (1705) | 4x Archer Skeleton (4094) | Composite Bow [4], 4x Archer Skeleton (+10% ranged each); size cards (Minorous/Skel Worker) vs specific targets |
| Shield / Left hand | (two-handed weapon) | - | - |
| Upper head | Apple of Archer [0] (2285) | - | Apple of Archer: DEX+3 |
| Mid head | Robo Eye [0] (5325) | - | Robo Eye |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Tights [1] (2331) | Pupa (4003) | Tights [1] (DEX+1), Pupa (HP+700) |
| Garment | Muffler [1] (2504) | Raydric (4133) | Muffler [1], Raydric |
| Shoes | Shoes [1] (2404) | Verit (4107) | Shoes [1], Verit |
| Accessory 1 | Clip [1] (2607) | Zerom (4064) | Clip [1], Zerom (DEX+3) |
| Accessory 2 | Clip [1] (2607) | Zerom (4064) | Clip [1], Zerom |

**Endgame (lv 99)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Falken Blitz [2] (1745) | 2x Archer Skeleton (4094) | Falken Blitz [2] (trans-only; Double Strafe/Sharp Shooting/Charge Arrow +10%), 2x Archer Skeleton. Alt: Ballista [1] (145 ATK) |
| Shield / Left hand | (two-handed weapon) | - | - |
| Upper head | Ulle's Cap [1] (5123) | Vesper (4374) | Ulle's Cap [1] (DEX+2, AGI+1), Vesper (DEX+2) |
| Mid head | Robo Eye [0] (5325) | - | Robo Eye: DEX+1, +2% dmg |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil: DEX+2 |
| Armor | Valkyrian Armor [1] (2357) | Peco Peco (4031) | Valkyrian Armor [1], Peco Peco |
| Garment | Valkyrian Manteau [1] (2524) | Raydric (4133) | Valkyrian Manteau [1], Raydric |
| Shoes | Sleipnir [0] (2410) | - | Sleipnir |
| Accessory 1 | Orleans's Glove [1] (2701) | Zerom (4064) | Orleans's Glove [1] (DEX+2), Zerom (DEX+3) |
| Accessory 2 | Brisingamen [0] (2630) | - | Brisingamen |

### Sniper - Falconer / Sharp Shooting (DEX/LUK/INT)

Source/basis: irowiki classic Sniper (Pure Falconer, FAS WoE)

**Mid tier (lv ~70-90)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Gakkung Bow [2] (1716) | 2x Soldier Skeleton (4086) | Gakkung Bow [2], 2x Soldier Skeleton (CRIT+9 each) |
| Shield / Left hand | (two-handed weapon) | - | - |
| Upper head | Apple of Archer [0] (2285) | - | Apple of Archer |
| Mid head | Robo Eye [0] (5325) | - | Robo Eye |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Tights [1] (2331) | Pupa (4003) | Tights [1], Pupa |
| Garment | Muffler [1] (2504) | Raydric (4133) | Muffler [1], Raydric |
| Shoes | Shoes [1] (2404) | Verit (4107) | Shoes [1], Verit |
| Accessory 1 | Rosary [0] (2608) | - | Rosary: LUK+2 (auto-Blitz rate) |
| Accessory 2 | Clip [1] (2607) | Zerom (4064) | Clip [1], Zerom |

**Endgame (lv 99)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Falken Blitz [2] (1745) | 2x Soldier Skeleton (4086) | Falken Blitz [2], 2x Soldier Skeleton |
| Shield / Left hand | (two-handed weapon) | - | - |
| Upper head | Ulle's Cap [1] (5123) | Vesper (4374) | Ulle's Cap [1], Vesper |
| Mid head | Robo Eye [0] (5325) | - | Robo Eye: DEX+1, +2% dmg |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil: DEX+2 |
| Armor | Valkyrian Armor [1] (2357) | Peco Peco (4031) | Valkyrian Armor [1], Peco Peco |
| Garment | Valkyrian Manteau [1] (2524) | Raydric (4133) | Valkyrian Manteau [1], Raydric |
| Shoes | Sleipnir [0] (2410) | - | Sleipnir |
| Accessory 1 | Orleans's Glove [1] (2701) | Zerom (4064) | Orleans's Glove [1] (DEX+2), Zerom (DEX+3) |
| Accessory 2 | Brisingamen [0] (2630) | - | Brisingamen |

## Clown (Minstrel)

_Equip-check identity: base job `BardDancer`, class type `Upper`, gender `Male`._

### Clown (Minstrel) - Arrow Vulcan (DEX/AGI/STR)

Source/basis: irowiki classic Clown/Gypsy; BR guides (Arrow Vulcan is the bRO-favourite damage build)

**Mid tier (lv ~70-90)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Guitar [1] (1908) | Hydra (4035) | Guitar [1], Hydra |
| Shield / Left hand | - | - | - |
| Upper head | Apple of Archer [0] (2285) | - | Apple of Archer |
| Mid head | Robo Eye [0] (5325) | - | Robo Eye |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Tights [1] (2331) | Pupa (4003) | Tights [1], Pupa |
| Garment | Muffler [1] (2504) | Raydric (4133) | Muffler [1], Raydric |
| Shoes | Shoes [1] (2404) | Matyr (4097) | Shoes [1], Matyr |
| Accessory 1 | Clip [1] (2607) | Zerom (4064) | Clip [1], Zerom |
| Accessory 2 | Clip [1] (2607) | Mantis (4079) | Clip [1], Mantis |

**Endgame (lv 99)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Oriental Lute [2] (1922) | 2x Archer Skeleton (4094) | Oriental Lute [2] (Arrow Vulcan +10%), 2x Archer Skeleton |
| Shield / Left hand | - | - | - |
| Upper head | Ulle's Cap [1] (5123) | Vesper (4374) | Ulle's Cap [1], Vesper |
| Mid head | Robo Eye [0] (5325) | - | Robo Eye: DEX+1, +2% dmg |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil: DEX+2 |
| Armor | Valkyrian Armor [1] (2357) | Peco Peco (4031) | Valkyrian Armor [1], Peco Peco |
| Garment | Valkyrian Manteau [1] (2524) | Raydric (4133) | Valkyrian Manteau [1], Raydric |
| Shoes | Sleipnir [0] (2410) | - | Sleipnir |
| Accessory 1 | Orleans's Glove [1] (2701) | Zerom (4064) | Orleans's Glove [1] (DEX+2), Zerom (DEX+3) |
| Accessory 2 | Brisingamen [0] (2630) | - | Brisingamen |

### Clown (Minstrel) - Support / Ensemble (VIT/DEX/INT)

Source/basis: irowiki classic Bard/Dancer; Diabolus set is the common classic support set

**Mid tier (lv ~70-90)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Guitar [1] (1908) | - | Guitar [1] |
| Shield / Left hand | - | - | - |
| Upper head | Feather Beret [0] (5170) | - | Feather Beret |
| Mid head | Sunglasses [1] (2202) | Nightmare (4127) | Sunglasses [1], Nightmare |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Tights [1] (2331) | Peco Peco (4031) | Tights [1], Peco Peco |
| Garment | Muffler [1] (2504) | Raydric (4133) | Muffler [1], Raydric |
| Shoes | Shoes [1] (2404) | Green Ferus (4381) | Shoes [1], Green Ferus |
| Accessory 1 | Rosary [0] (2608) | - | Rosary |
| Accessory 2 | Necklace [0] (2603) | - | Necklace: VIT+2 |

**Endgame (lv 99)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Cello [3] (1925) | - | Cello [3] (trans-only; DEX+3 AGI+2) |
| Shield / Left hand | - | - | - |
| Upper head | Feather Beret [0] (5170) | - | Feather Beret |
| Mid head | Sunglasses [1] (2202) | Nightmare (4127) | Sunglasses [1], Nightmare |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Diabolus Robe [1] (2374) | Marc (4105) | Diabolus Robe [1] (trans-only; after-cast delay -10%, SP+150), Marc |
| Garment | Diabolus Manteau [1] (2537) | Raydric (4133) | Diabolus Manteau [1], Raydric |
| Shoes | Diabolus Boots [1] (2433) | Green Ferus (4381) | Diabolus Boots [1] (HP + BaseLv*10), Green Ferus |
| Accessory 1 | Diabolus Ring [1] (2729) | Phen (4077) | Diabolus Ring [1] (Robe+Ring combo: +3% dmg, +3% MATK), Phen |
| Accessory 2 | Brisingamen [0] (2630) | - | Brisingamen |

## Gypsy

_Equip-check identity: base job `BardDancer`, class type `Upper`, gender `Female`._

### Gypsy - Arrow Vulcan (DEX/AGI/STR)

Source/basis: irowiki classic Clown/Gypsy; BR guides (Arrow Vulcan is the bRO-favourite damage build)

**Mid tier (lv ~70-90)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Rante Whip [1] (1957) | Hydra (4035) | Rante Whip [1], Hydra |
| Shield / Left hand | - | - | - |
| Upper head | Apple of Archer [0] (2285) | - | Apple of Archer |
| Mid head | Robo Eye [0] (5325) | - | Robo Eye |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Tights [1] (2331) | Pupa (4003) | Tights [1], Pupa |
| Garment | Muffler [1] (2504) | Raydric (4133) | Muffler [1], Raydric |
| Shoes | Shoes [1] (2404) | Matyr (4097) | Shoes [1], Matyr |
| Accessory 1 | Clip [1] (2607) | Zerom (4064) | Clip [1], Zerom |
| Accessory 2 | Clip [1] (2607) | Mantis (4079) | Clip [1], Mantis |

**Endgame (lv 99)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Queen's Whip [2] (1976) | 2x Archer Skeleton (4094) | Queen's Whip [2] (Arrow Vulcan +10%), 2x Archer Skeleton |
| Shield / Left hand | - | - | - |
| Upper head | Ulle's Cap [1] (5123) | Vesper (4374) | Ulle's Cap [1], Vesper |
| Mid head | Robo Eye [0] (5325) | - | Robo Eye: DEX+1, +2% dmg |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil: DEX+2 |
| Armor | Valkyrian Armor [1] (2357) | Peco Peco (4031) | Valkyrian Armor [1], Peco Peco |
| Garment | Valkyrian Manteau [1] (2524) | Raydric (4133) | Valkyrian Manteau [1], Raydric |
| Shoes | Sleipnir [0] (2410) | - | Sleipnir |
| Accessory 1 | Orleans's Glove [1] (2701) | Zerom (4064) | Orleans's Glove [1] (DEX+2), Zerom (DEX+3) |
| Accessory 2 | Brisingamen [0] (2630) | - | Brisingamen |

### Gypsy - Support / Ensemble (VIT/DEX/INT)

Source/basis: irowiki classic Bard/Dancer; Diabolus set is the common classic support set

**Mid tier (lv ~70-90)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Rante Whip [1] (1957) | - | Rante Whip [1] |
| Shield / Left hand | - | - | - |
| Upper head | Feather Beret [0] (5170) | - | Feather Beret |
| Mid head | Sunglasses [1] (2202) | Nightmare (4127) | Sunglasses [1], Nightmare |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Tights [1] (2331) | Peco Peco (4031) | Tights [1], Peco Peco |
| Garment | Muffler [1] (2504) | Raydric (4133) | Muffler [1], Raydric |
| Shoes | Shoes [1] (2404) | Green Ferus (4381) | Shoes [1], Green Ferus |
| Accessory 1 | Rosary [0] (2608) | - | Rosary |
| Accessory 2 | Necklace [0] (2603) | - | Necklace: VIT+2 |

**Endgame (lv 99)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Whip of Balance [3] (1980) | - | Whip of Balance [3] (trans-only) |
| Shield / Left hand | - | - | - |
| Upper head | Feather Beret [0] (5170) | - | Feather Beret |
| Mid head | Sunglasses [1] (2202) | Nightmare (4127) | Sunglasses [1], Nightmare |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Diabolus Robe [1] (2374) | Marc (4105) | Diabolus Robe [1] (trans-only; after-cast delay -10%, SP+150), Marc |
| Garment | Diabolus Manteau [1] (2537) | Raydric (4133) | Diabolus Manteau [1], Raydric |
| Shoes | Diabolus Boots [1] (2433) | Green Ferus (4381) | Diabolus Boots [1] (HP + BaseLv*10), Green Ferus |
| Accessory 1 | Diabolus Ring [1] (2729) | Phen (4077) | Diabolus Ring [1] (Robe+Ring combo: +3% dmg, +3% MATK), Phen |
| Accessory 2 | Brisingamen [0] (2630) | - | Brisingamen |

## High Priest

_Equip-check identity: base job `Priest`, class type `Upper`._

### High Priest - Full Support (INT/VIT/DEX)

Source/basis: irowiki classic HP (INT/VIT support, DEX/VIT WoE); Kiel-D-01 is the classic endgame priest card

**Mid tier (lv ~70-90)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Healing Staff [0] (1625) | - | Healing Staff +7 (MATK+15%, Heal +1.5%/refine) |
| Shield / Left hand | Buckler [1] (2104) | Thara Frog (4058) | Buckler [1], Thara Frog |
| Upper head | Biretta [1] (2217) | Rideword (4185) | Biretta [1], Rideword (INT+2 for Acolyte classes) |
| Mid head | Sunglasses [1] (2202) | Nightmare (4127) | Sunglasses [1], Nightmare |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Holy Robe [1] (2373) | Marc (4105) | Holy Robe [1] (-15% Demon), Marc |
| Garment | Muffler [1] (2504) | Raydric (4133) | Muffler [1], Raydric |
| Shoes | Shoes [1] (2404) | Verit (4107) | Shoes [1], Verit |
| Accessory 1 | Rosary [0] (2608) | - | Rosary |
| Accessory 2 | Earring [0] (2602) | - | Earring |

**Endgame (lv 99)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Dea Staff [1] (2005) | - | Dea Staff [1] (trans-only 2H; INT+6 VIT+2, MATK+15%+, heal proc) - or Croce Staff [1] if you want a shield |
| Shield / Left hand | (two-handed weapon) | - | - |
| Upper head | Diadem [1] (5313) | Kiel-D-01 (4403) | Diadem [1] (top+mid), Kiel-D-01 (after-cast delay -30%) |
| Mid head | (covered by upper headgear) | - | - |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Diabolus Robe [1] (2374) | Marc (4105) | Diabolus Robe [1] (heal +6%, delay -10%), Marc |
| Garment | Valkyrian Manteau [1] (2524) | Raydric (4133) | Valkyrian Manteau [1], Raydric |
| Shoes | Sleipnir [0] (2410) | - | Sleipnir |
| Accessory 1 | Diabolus Ring [1] (2729) | Phen (4077) | Diabolus Ring [1] (heal +5%, combo with Robe), Phen |
| Accessory 2 | Brisingamen [0] (2630) | - | Brisingamen (INT+6) |

### High Priest - Battle Priest (STR/AGI/DEX, mace)

Source/basis: irowiki classic HP (AGI battle build)

**Mid tier (lv ~70-90)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Golden Mace [2] (1539) | 2x Skeleton Worker (4092) | Golden Mace [2] (unbreakable, +10% Undead), 2x Skeleton Worker |
| Shield / Left hand | Buckler [1] (2104) | Thara Frog (4058) | Buckler [1], Thara Frog |
| Upper head | Biretta [1] (2217) | Nightmare (4127) | Biretta [1], Nightmare |
| Mid head | Angel Wing Ears [0] (5074) | - | Angel Wing Ears |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Saint's Robe [1] (2326) | Peco Peco (4031) | Saint's Robe [1], Peco Peco |
| Garment | Muffler [1] (2504) | Raydric (4133) | Muffler [1], Raydric |
| Shoes | Shoes [1] (2404) | Matyr (4097) | Shoes [1], Matyr |
| Accessory 1 | Clip [1] (2607) | Mantis (4079) | Clip [1], Mantis |
| Accessory 2 | Clip [1] (2607) | Kukre (4027) | Clip [1], Kukre |

**Endgame (lv 99)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Lunakaligo [3] (1544) | 3x Skeleton Worker (4092) | Lunakaligo [3] (trans-only; STR>=77: ASPD+4%, stun), 3x Skeleton Worker (Strouf vs Demon) |
| Shield / Left hand | Valkyrja's Shield [1] (2115) | Thara Frog (4058) | Valkyrja's Shield [1], Thara Frog |
| Upper head | Orc Hero Headdress [1] (5375) | Vanberk (4411) | Orc Hero Headdress [1], Vanberk |
| Mid head | (covered by upper headgear) | - | - |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Valkyrian Armor [1] (2357) | Peco Peco (4031) | Valkyrian Armor [1] +7~9, Peco Peco (+10% MaxHP); Marc for freeze immunity |
| Garment | Valkyrian Manteau [1] (2524) | Raydric (4133) | Valkyrian Manteau [1], Raydric (-20% Neutral) |
| Shoes | Sleipnir [0] (2410) | - | Sleipnir: +20% HP/SP, +25% move speed (lv94) |
| Accessory 1 | Megingjard [0] (2629) | - | Megingjard: STR+40 (lv94) |
| Accessory 2 | Brisingamen [0] (2630) | - | Brisingamen: STR/AGI/VIT/INT+6, LUK+10 (lv94) |

## Champion

_Equip-check identity: base job `Monk`, class type `Upper`._

### Champion - Asura Strike / Guillotine Fist (STR/INT/DEX)

Source/basis: irowiki classic Champion (STR/INT MVP, STR/DEX/VIT WoE)

**Mid tier (lv ~70-90)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Studded Knuckles [3] (1806) | 3x Abysmal Knight (4140) | Studded Knuckles [3], 3x Abysmal Knight (+25% vs Boss) - use Hydra for PvP |
| Shield / Left hand | Buckler [1] (2104) | Thara Frog (4058) | Buckler [1], Thara Frog |
| Upper head | Hat of the Sun God [1] (5353) | Rideword (4185) | Hat of the Sun God [1] (top+mid; STR+3 INT+2), Rideword (INT+2 for Monk) |
| Mid head | (covered by upper headgear) | - | - |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Holy Robe [1] (2373) | Peco Peco (4031) | Holy Robe [1], Peco Peco |
| Garment | Muffler [1] (2504) | Raydric (4133) | Muffler [1], Raydric |
| Shoes | Shoes [1] (2404) | Verit (4107) | Shoes [1], Verit (SP% for Asura) |
| Accessory 1 | Clip [1] (2607) | Phen (4077) | Clip [1], Phen (uninterruptible Asura cast - wiki says "required") |
| Accessory 2 | Clip [1] (2607) | Mantis (4079) | Clip [1], Mantis |

**Endgame (lv 99)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Hatii Claw [1] (1815) | Abysmal Knight (4140) | Hatii Claw [1] +10 (152 ATK, Dark), Abysmal Knight |
| Shield / Left hand | Valkyrja's Shield [1] (2115) | Thara Frog (4058) | Valkyrja's Shield [1], Thara Frog |
| Upper head | Hat of the Sun God [1] (5353) | Rideword (4185) | Hat of the Sun God [1], Rideword |
| Mid head | (covered by upper headgear) | - | - |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Valkyrian Armor [1] (2357) | Peco Peco (4031) | Valkyrian Armor [1] +7~9, Peco Peco (+10% MaxHP); Marc for freeze immunity |
| Garment | Valkyrian Manteau [1] (2524) | Raydric (4133) | Valkyrian Manteau [1], Raydric (-20% Neutral) |
| Shoes | Sleipnir [0] (2410) | - | Sleipnir: +20% HP/SP, +25% move speed (lv94) |
| Accessory 1 | Clip [1] (2607) | Phen (4077) | Clip [1], Phen (keep one Phen; the other slot is Brisingamen) |
| Accessory 2 | Brisingamen [0] (2630) | - | Brisingamen: STR/AGI/VIT/INT+6, LUK+10 (lv94) |

### Champion - Combo (Triple Attack > Chain > Combo Finish) STR/AGI/DEX

Source/basis: irowiki classic Champion (STR/AGI Combo)

**Mid tier (lv ~70-90)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Combo Battle Glove [4] (1822) | 4x Andre (4043) | Combo Battle Glove [4] (+15/15/20% combo skills), 4x Andre (+20 ATK) |
| Shield / Left hand | - | - | - |
| Upper head | Magni's Cap [0] (5122) | - | Magni's Cap: STR+2 |
| Mid head | Angel Wing Ears [0] (5074) | - | Angel Wing Ears |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Holy Robe [1] (2373) | Peco Peco (4031) | Holy Robe [1], Peco Peco |
| Garment | Muffler [1] (2504) | Raydric (4133) | Muffler [1], Raydric |
| Shoes | Shoes [1] (2404) | Matyr (4097) | Shoes [1], Matyr |
| Accessory 1 | Clip [1] (2607) | Mantis (4079) | Clip [1], Mantis |
| Accessory 2 | Clip [1] (2607) | Kukre (4027) | Clip [1], Kukre |

**Endgame (lv 99)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Combo Battle Glove [4] (1822) | 2x Doppelganger (4142) + Skeleton Worker (4092) + Minorous (4126) | Combo Battle Glove [4] +10, 2x Doppelganger (ASPD) + Skeleton Worker + Minorous |
| Shield / Left hand | - | - | - |
| Upper head | Orc Hero Headdress [1] (5375) | Vanberk (4411) | Orc Hero Headdress [1], Vanberk |
| Mid head | (covered by upper headgear) | - | - |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Valkyrian Armor [1] (2357) | Peco Peco (4031) | Valkyrian Armor [1] +7~9, Peco Peco (+10% MaxHP); Marc for freeze immunity |
| Garment | Valkyrian Manteau [1] (2524) | Raydric (4133) | Valkyrian Manteau [1], Raydric (-20% Neutral) |
| Shoes | Sleipnir [0] (2410) | - | Sleipnir: +20% HP/SP, +25% move speed (lv94) |
| Accessory 1 | Megingjard [0] (2629) | - | Megingjard: STR+40 (lv94) |
| Accessory 2 | Brisingamen [0] (2630) | - | Brisingamen: STR/AGI/VIT/INT+6, LUK+10 (lv94) |

## Assassin Cross

_Equip-check identity: base job `Assassin`, class type `Upper`._

### Assassin Cross - Sonic Blow katar (STR/AGI/DEX, EDP)

Source/basis: irowiki classic SinX (STR/AGI SB), ratemyserver SB guides, bRO "Mercenários"

**Mid tier (lv ~70-90)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Katar [2] (1253) | 2x Hydra (4035) | Katar [2] (DEX+1), 2x Hydra (swap Minorous/Skel Worker for PvM) |
| Shield / Left hand | (two-handed weapon) | - | - |
| Upper head | Magni's Cap [0] (5122) | - | Magni's Cap: STR+2 |
| Mid head | Angel Wing Ears [0] (5074) | - | Angel Wing Ears |
| Lower head | Gangster Scarf [0] (5361) | - | Gangster Scarf: ATK+5 (lv60) |
| Armor | Ninja Suit [1] (2359) | Peco Peco (4031) | Ninja Suit [1] (AGI+1), Peco Peco |
| Garment | Manteau [1] (2506) | Raydric (4133) | Manteau [1], Raydric |
| Shoes | Boots [1] (2406) | Matyr (4097) | Boots [1], Matyr |
| Accessory 1 | Clip [1] (2607) | Mantis (4079) | Clip [1], Mantis |
| Accessory 2 | Clip [1] (2607) | Mantis (4079) | Clip [1], Mantis |

**Endgame (lv 99)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Infiltrator [1] (1266) | Hydra (4035) | Infiltrator [1] (+50% Demi-Human), Hydra - PvM alt: Blood Tears [2] w/ 2x Minorous |
| Shield / Left hand | (two-handed weapon) | - | - |
| Upper head | Orc Hero Headdress [1] (5375) | Vanberk (4411) | Orc Hero Headdress [1], Vanberk |
| Mid head | (covered by upper headgear) | - | - |
| Lower head | Gangster Scarf [0] (5361) | - | Gangster Scarf |
| Armor | Valkyrian Armor [1] (2357) | Peco Peco (4031) | Valkyrian Armor [1] +7~9, Peco Peco (+10% MaxHP); Marc for freeze immunity |
| Garment | Valkyrian Manteau [1] (2524) | Raydric (4133) | Valkyrian Manteau [1], Raydric (-20% Neutral) |
| Shoes | Sleipnir [0] (2410) | - | Sleipnir: +20% HP/SP, +25% move speed (lv94) |
| Accessory 1 | Megingjard [0] (2629) | - | Megingjard: STR+40 (lv94) |
| Accessory 2 | Brisingamen [0] (2630) | - | Brisingamen: STR/AGI/VIT/INT+6, LUK+10 (lv94) |

### Assassin Cross - Soul Destroyer (STR/INT/DEX)

Source/basis: irowiki classic SinX: "Zipper Bear carded weapons in both hands (or Ice Pick in left hand)"

**Mid tier (lv ~70-90)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Main Gauche [4] (1208) | 4x Andre (4043) | Main Gauche [4], 4x Andre (cheap flat ATK) |
| Shield / Left hand | Ice Pick [0] (1230) | - | Left hand: Ice Pick |
| Upper head | Hat of the Sun God [1] (5353) | Elder Willow (4052) | Hat of the Sun God [1] (top+mid), Elder Willow (INT+2) |
| Mid head | (covered by upper headgear) | - | - |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Ninja Suit [1] (2359) | Evil Druid (4141) | Ninja Suit [1], Evil Druid (INT+1) |
| Garment | Muffler [1] (2504) | Raydric (4133) | Muffler [1], Raydric |
| Shoes | Boots [1] (2406) | Green Ferus (4381) | Boots [1], Green Ferus |
| Accessory 1 | Clip [1] (2607) | Phen (4077) | Clip [1], Phen (no cast interruption) |
| Accessory 2 | Clip [1] (2607) | Mantis (4079) | Clip [1], Mantis |

**Endgame (lv 99)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Main Gauche [4] (1208) | 4x Zipper Bear (4281) | Main Gauche [4] +10, 4x Zipper Bear (+30 ATK each) |
| Shield / Left hand | Main Gauche [4] (1208) | 4x Zipper Bear (4281) | Left hand: 2nd Main Gauche [4] w/ 4x Zipper Bear (or Ice Pick) |
| Upper head | Hat of the Sun God [1] (5353) | Elder Willow (4052) | Hat of the Sun God [1], Elder Willow |
| Mid head | (covered by upper headgear) | - | - |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Valkyrian Armor [1] (2357) | Evil Druid (4141) | Valkyrian Armor [1], Evil Druid |
| Garment | Valkyrian Manteau [1] (2524) | Raydric (4133) | Valkyrian Manteau [1], Raydric (-20% Neutral) |
| Shoes | Sleipnir [0] (2410) | - | Sleipnir: +20% HP/SP, +25% move speed (lv94) |
| Accessory 1 | Megingjard [0] (2629) | - | Megingjard |
| Accessory 2 | Brisingamen [0] (2630) | - | Brisingamen: STR/AGI/VIT/INT+6, LUK+10 (lv94) |

## Stalker

_Equip-check identity: base job `Rogue`, class type `Upper`._

### Stalker - Melee dagger (STR/AGI/DEX, Sidewinder double attack)

Source/basis: irowiki classic Stalker (STR/AGI/DEX melee)

**Mid tier (lv ~70-90)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Gladius [3] (1220) | Sidewinder (4117) + 2x Hydra (4035) | Gladius [3], Sidewinder (Double Attack lv1) + 2x Hydra |
| Shield / Left hand | Buckler [1] (2104) | Thara Frog (4058) | Buckler [1], Thara Frog |
| Upper head | Magni's Cap [0] (5122) | - | Magni's Cap |
| Mid head | Angel Wing Ears [0] (5074) | - | Angel Wing Ears |
| Lower head | Gangster Scarf [0] (5361) | - | Gangster Scarf (ATK+5, gives Rogues Gangster Paradise) |
| Armor | Thief Clothes [1] (2336) | Peco Peco (4031) | Thief Clothes [1], Peco Peco (wiki) |
| Garment | Muffler [1] (2504) | Raydric (4133) | Muffler [1], Raydric |
| Shoes | Boots [1] (2406) | Matyr (4097) | Boots [1], Matyr |
| Accessory 1 | Clip [1] (2607) | Mantis (4079) | Clip [1], Mantis |
| Accessory 2 | Clip [1] (2607) | Mantis (4079) | Clip [1], Mantis |

**Endgame (lv 99)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Dagger of Hunter [3] (13038) | Sidewinder (4117) + 2x Hydra (4035) | Dagger of Hunter [3] (Rogue trans-only; STR+1 AGI+2 DEX+1, Back Stab +20%), Sidewinder + 2x Hydra |
| Shield / Left hand | Valkyrja's Shield [1] (2115) | Thara Frog (4058) | Valkyrja's Shield [1], Thara Frog |
| Upper head | Orc Hero Headdress [1] (5375) | Vanberk (4411) | Orc Hero Headdress [1], Vanberk |
| Mid head | (covered by upper headgear) | - | - |
| Lower head | Gangster Scarf [0] (5361) | - | Gangster Scarf |
| Armor | Valkyrian Armor [1] (2357) | Peco Peco (4031) | Valkyrian Armor [1] +7~9, Peco Peco (+10% MaxHP); Marc for freeze immunity |
| Garment | Valkyrian Manteau [1] (2524) | Raydric (4133) | Valkyrian Manteau [1], Raydric (-20% Neutral) |
| Shoes | Sleipnir [0] (2410) | - | Sleipnir: +20% HP/SP, +25% move speed (lv94) |
| Accessory 1 | Megingjard [0] (2629) | - | Megingjard: STR+40 (lv94) |
| Accessory 2 | Brisingamen [0] (2630) | - | Brisingamen: STR/AGI/VIT/INT+6, LUK+10 (lv94) |

### Stalker - Bow / Divest (DEX, Full Strip + Double Strafe)

Source/basis: irowiki classic Stalker bow set (gear taken from the wiki)

**Mid tier (lv ~70-90)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Composite Bow [4] (1705) | 4x Archer Skeleton (4094) | Composite Bow [4], 4x Archer Skeleton |
| Shield / Left hand | (two-handed weapon) | - | - |
| Upper head | Apple of Archer [0] (2285) | - | Apple of Archer |
| Mid head | Robo Eye [0] (5325) | - | Robo Eye |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Thief Clothes [1] (2336) | Anolian (4234) | Thief Clothes [1], Anolian (auto Improve Concentration when hit) or Peco Peco |
| Garment | Muffler [1] (2504) | Raydric (4133) | Muffler [1], Raydric |
| Shoes | Shoes [1] (2404) | Matyr (4097) | Shoes [1], Matyr |
| Accessory 1 | Clip [1] (2607) | Zerom (4064) | Clip [1], Zerom |
| Accessory 2 | Clip [1] (2607) | Marine Sphere (4084) | Clip [1], Marine Sphere (Magnum Break lv3 for Plagiarism combos) |

**Endgame (lv 99)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Gakkung Bow [2] (1716) | 2x Archer Skeleton (4094) | Gakkung Bow [2], 2x Archer Skeleton |
| Shield / Left hand | (two-handed weapon) | - | - |
| Upper head | Ulle's Cap [1] (5123) | Vesper (4374) | Ulle's Cap [1], Vesper |
| Mid head | Robo Eye [0] (5325) | - | Robo Eye |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Valkyrian Armor [1] (2357) | Peco Peco (4031) | Valkyrian Armor [1], Peco Peco |
| Garment | Wool Scarf [1] (2528) | Raydric (4133) | Wool Scarf [1] (trans-only), Raydric (wiki) |
| Shoes | Tidal Shoes [1] (2424) | Matyr (4097) | Tidal Shoes [1] (trans-only), Matyr (wiki) - or Sleipnir |
| Accessory 1 | Orleans's Glove [1] (2701) | Zerom (4064) | Orleans's Glove [1], Zerom |
| Accessory 2 | Clip [1] (2607) | Marine Sphere (4084) | Clip [1], Marine Sphere |

## Whitesmith (Mastersmith)

_Equip-check identity: base job `Blacksmith`, class type `Upper`._

### Whitesmith (Mastersmith) - Cart Termination (STR/DEX, Cart Boost + Maximize Power)

Source/basis: classic WS guides (ratemyserver), irowiki classic Mastersmith

**Mid tier (lv ~70-90)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Two-Handed Axe [2] (1361) | Minorous (4126) + Skeleton Worker (4092) | Two-Handed Axe [2], Minorous + Skeleton Worker |
| Shield / Left hand | (two-handed weapon) | - | - |
| Upper head | Majestic Goat [1] (5160) | Vanberk (4411) | Majestic Goat [1] (STR+1), Vanberk |
| Mid head | Angel Wing Ears [0] (5074) | - | Angel Wing Ears |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Assaulter Plate [1] (2376) | Peco Peco (4031) | Assaulter Plate [1] (lv80), Peco Peco |
| Garment | Captain's Manteau [1] (2538) | Raydric (4133) | Captain's Manteau [1] (lv80), Raydric |
| Shoes | Battle Greaves [1] (2435) | Green Ferus (4381) | Battle Greaves [1] (lv80), Green Ferus (Plate+Greaves+Manteau = WoE set combo) |
| Accessory 1 | Clip [1] (2607) | Mantis (4079) | Clip [1], Mantis |
| Accessory 2 | Clip [1] (2607) | Zerom (4064) | Clip [1], Zerom |

**Endgame (lv 99)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Giant Axe [1] (1387) | Minorous (4126) | Giant Axe [1] (trans-only, 330 ATK, Cart Termination +15%), Minorous (Hydra for PvP) |
| Shield / Left hand | (two-handed weapon) | - | - |
| Upper head | Orc Hero Headdress [1] (5375) | Vanberk (4411) | Orc Hero Headdress [1], Vanberk |
| Mid head | (covered by upper headgear) | - | - |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Valkyrian Armor [1] (2357) | Peco Peco (4031) | Valkyrian Armor [1] +7~9, Peco Peco (+10% MaxHP); Marc for freeze immunity |
| Garment | Valkyrian Manteau [1] (2524) | Raydric (4133) | Valkyrian Manteau [1], Raydric (-20% Neutral) |
| Shoes | Sleipnir [0] (2410) | - | Sleipnir: +20% HP/SP, +25% move speed (lv94) |
| Accessory 1 | Megingjard [0] (2629) | - | Megingjard: STR+40 (lv94) |
| Accessory 2 | Brisingamen [0] (2630) | - | Brisingamen: STR/AGI/VIT/INT+6, LUK+10 (lv94) |

### Whitesmith (Mastersmith) - Battle Axe / Hammerfall (STR/AGI, Adrenaline + Weapon Perfection)

Source/basis: irowiki classic Mastersmith (STR/AGI Battle)

**Mid tier (lv ~70-90)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | War Axe [1] (1306) | Skeleton Worker (4092) | War Axe [1] (DEX+2 LUK+2), Skeleton Worker |
| Shield / Left hand | Buckler [1] (2104) | Thara Frog (4058) | Buckler [1], Thara Frog |
| Upper head | Majestic Goat [1] (5160) | Nightmare (4127) | Majestic Goat [1], Nightmare |
| Mid head | Angel Wing Ears [0] (5074) | - | Angel Wing Ears |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Chain Mail [1] (2315) | Peco Peco (4031) | Chain Mail [1], Peco Peco |
| Garment | Manteau [1] (2506) | Raydric (4133) | Manteau [1], Raydric |
| Shoes | Boots [1] (2406) | Matyr (4097) | Boots [1], Matyr |
| Accessory 1 | Clip [1] (2607) | Mantis (4079) | Clip [1], Mantis |
| Accessory 2 | Clip [1] (2607) | Kukre (4027) | Clip [1], Kukre |

**Endgame (lv 99)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Heart Breaker [1] (1376) | Minorous (4126) | Heart Breaker [1] (trans-only; CRIT+20+refine, WS/Creator autocast Hammerfall), Minorous |
| Shield / Left hand | (two-handed weapon) | - | - |
| Upper head | Orc Hero Headdress [1] (5375) | Vanberk (4411) | Orc Hero Headdress [1], Vanberk |
| Mid head | (covered by upper headgear) | - | - |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Valkyrian Armor [1] (2357) | Peco Peco (4031) | Valkyrian Armor [1] +7~9, Peco Peco (+10% MaxHP); Marc for freeze immunity |
| Garment | Valkyrian Manteau [1] (2524) | Raydric (4133) | Valkyrian Manteau [1], Raydric (-20% Neutral) |
| Shoes | Sleipnir [0] (2410) | - | Sleipnir: +20% HP/SP, +25% move speed (lv94) |
| Accessory 1 | Megingjard [0] (2629) | - | Megingjard: STR+40 (lv94) |
| Accessory 2 | Brisingamen [0] (2630) | - | Brisingamen: STR/AGI/VIT/INT+6, LUK+10 (lv94) |

## Creator (Biochemist)

_Equip-check identity: base job `Alchemist`, class type `Upper`._

### Creator (Biochemist) - Acid Demonstration "Bomber" (INT/DEX/AGI 25)

Source/basis: irowiki classic Biochemist (Bomber) - endgame list taken from the wiki

**Mid tier (lv ~70-90)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Excalibur [0] (1137) | - | Excalibur (INT+5, LUK+10, Holy) |
| Shield / Left hand | Buckler [1] (2104) | Thara Frog (4058) | Buckler [1], Thara Frog |
| Upper head | Crown [0] (2235) | - | Crown: INT+2 |
| Mid head | Sunglasses [1] (2202) | Elder Willow (4052) | Sunglasses [1], Elder Willow (INT+2) |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Saint's Robe [1] (2326) | Evil Druid (4141) | Saint's Robe [1], Evil Druid |
| Garment | Manteau [1] (2506) | Raydric (4133) | Manteau [1], Raydric |
| Shoes | Boots [1] (2406) | Verit (4107) | Boots [1], Verit |
| Accessory 1 | Earring [0] (2602) | - | Earring: INT+2 |
| Accessory 2 | Glove [0] (2604) | - | Glove: DEX+2 |

**Endgame (lv 99)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Elemental Sword [3] (13414) | 3x Cecil Damon (4368) | Elemental Sword [3] (trans-only; INT+4, STR+2), 3x Cecil Damon (wiki) |
| Shield / Left hand | Valkyrja's Shield [1] (2115) | Thara Frog (4058) | Valkyrja's Shield [1], Thara Frog |
| Upper head | Ulle's Cap [1] (5123) | Stalactic Golem (4223) | Ulle's Cap [1] (or Parade Hat [1]), Stalactic Golem |
| Mid head | Sunglasses [1] (2202) | Stalactic Golem (4223) | Sunglasses [1], Stalactic Golem |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Valkyrian Armor [1] (2357) | Evil Druid (4141) | Valkyrian Armor [1], Evil Druid |
| Garment | Captain's Manteau [1] (2538) | Raydric (4133) | Captain's Manteau [1], Raydric (or Noxious) |
| Shoes | Battle Greaves [1] (2435) | Matyr (4097) | Battle Greaves [1], Matyr |
| Accessory 1 | Orleans's Glove [1] (2701) | Zerom (4064) | Orleans's Glove [1], Zerom (or Smokie) |
| Accessory 2 | Brisingamen [0] (2630) | - | Brisingamen |

### Creator (Biochemist) - Potion Pitcher / FCP support (VIT/DEX)

Source/basis: irowiki classic Biochemist (Aid Condensed Potion - "same equipment as Bomber"), adapted to VIT

**Mid tier (lv ~70-90)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Sword [4] (1102) | 4x Cecil Damon (4368) | Sword [4], 4x Cecil Damon (ASPD for faster throwing) |
| Shield / Left hand | Buckler [1] (2104) | Thara Frog (4058) | Buckler [1], Thara Frog |
| Upper head | Feather Beret [0] (5170) | - | Feather Beret |
| Mid head | Sunglasses [1] (2202) | Nightmare (4127) | Sunglasses [1], Nightmare |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Saint's Robe [1] (2326) | Marc (4105) | Saint's Robe [1], Marc |
| Garment | Manteau [1] (2506) | Raydric (4133) | Manteau [1], Raydric |
| Shoes | Boots [1] (2406) | Green Ferus (4381) | Boots [1], Green Ferus |
| Accessory 1 | Necklace [0] (2603) | - | Necklace: VIT+2 |
| Accessory 2 | Glove [0] (2604) | - | Glove: DEX+2 |

**Endgame (lv 99)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Elemental Sword [3] (13414) | 3x Cecil Damon (4368) | Elemental Sword [3], 3x Cecil Damon |
| Shield / Left hand | Valkyrja's Shield [1] (2115) | Thara Frog (4058) | Valkyrja's Shield [1], Thara Frog |
| Upper head | Feather Beret [0] (5170) | - | Feather Beret |
| Mid head | Sunglasses [1] (2202) | Nightmare (4127) | Sunglasses [1], Nightmare |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Assaulter Plate [1] (2376) | Marc (4105) | Assaulter Plate [1], Marc |
| Garment | Captain's Manteau [1] (2538) | Raydric (4133) | Captain's Manteau [1], Raydric |
| Shoes | Battle Greaves [1] (2435) | Green Ferus (4381) | Battle Greaves [1], Green Ferus (completes WoE set combo: VIT+3, HP+12%) |
| Accessory 1 | Orleans's Glove [1] (2701) | Zerom (4064) | Orleans's Glove [1], Zerom |
| Accessory 2 | Brisingamen [0] (2630) | - | Brisingamen |

## Star Gladiator

_Equip-check identity: base job `StarGladiator`, class type `Normal`._

### Star Gladiator - Melee Union / Warm Wind (STR/AGI/DEX) with book

Source/basis: irowiki classic Star Gladiator; books are the SG weapon class

**Mid tier (lv ~70-90)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Bible [2] (1551) | 2x Hydra (4035) | Bible [2], 2x Hydra (swap to size/race cards per map) |
| Shield / Left hand | Guard [1] (2102) | Thara Frog (4058) | Guard [1], Thara Frog |
| Upper head | Magni's Cap [0] (5122) | - | Magni's Cap |
| Mid head | Angel Wing Ears [0] (5074) | - | Angel Wing Ears |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Mink Coat [1] (2311) | Peco Peco (4031) | Mink Coat [1], Peco Peco |
| Garment | Muffler [1] (2504) | Raydric (4133) | Muffler [1], Raydric |
| Shoes | Boots [1] (2406) | Matyr (4097) | Boots [1], Matyr |
| Accessory 1 | Clip [1] (2607) | Mantis (4079) | Clip [1], Mantis |
| Accessory 2 | Clip [1] (2607) | Kukre (4027) | Clip [1], Kukre |

**Endgame (lv 99)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Hardcover Book [1] (1561) | Hydra (4035) | Hardcover Book [1] +10 (140 ATK, STR+3 DEX+2), Hydra |
| Shield / Left hand | Valkyrja's Shield [1] (2115) | Thara Frog (4058) | Valkyrja's Shield [1], Thara Frog |
| Upper head | Orc Hero Headdress [1] (5375) | Vanberk (4411) | Orc Hero Headdress [1], Vanberk |
| Mid head | (covered by upper headgear) | - | - |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Assaulter Plate [1] (2376) | Peco Peco (4031) | Assaulter Plate [1] (Valkyrian is trans-only), Peco Peco |
| Garment | Captain's Manteau [1] (2538) | Raydric (4133) | Captain's Manteau [1], Raydric |
| Shoes | Sleipnir [0] (2410) | - | Sleipnir |
| Accessory 1 | Megingjard [0] (2629) | - | Megingjard |
| Accessory 2 | Brisingamen [0] (2630) | - | Brisingamen |

## Soul Linker

_Equip-check identity: base job `SoulLinker`, class type `Normal`._

### Soul Linker - Esma / Kaahi support caster (INT/DEX)

Source/basis: irowiki classic Soul Linker

**Mid tier (lv ~70-90)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Wing Staff [0] (1616) | - | Wing Staff |
| Shield / Left hand | Magic Bible Vol1 [1] (2131) | Thara Frog (4058) | Magic Bible Vol1 [1], Thara Frog |
| Upper head | Mage Hat [0] (5027) | - | Mage Hat |
| Mid head | Robo Eye [0] (5325) | - | Robo Eye |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Robe of Cast [1] (2360) | Evil Druid (4141) | Robe of Cast [1], Evil Druid |
| Garment | Muffler [1] (2504) | Raydric (4133) | Muffler [1], Raydric |
| Shoes | Shoes [1] (2404) | Verit (4107) | Shoes [1], Verit |
| Accessory 1 | Glove [0] (2604) | - | Glove |
| Accessory 2 | Earring [0] (2602) | - | Earring |

**Endgame (lv 99)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Wizardry Staff [0] (1473) | - | Wizardry Staff +10 (2H; INT+6 DEX+2, MATK+15%) |
| Shield / Left hand | (two-handed weapon) | - | - |
| Upper head | Diadem [1] (5313) | Evil Snake Lord (4330) | Diadem [1] (top+mid), Evil Snake Lord |
| Mid head | (covered by upper headgear) | - | - |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Robe of Cast [1] (2360) | Marc (4105) | Robe of Cast [1], Marc |
| Garment | Survivor's Manteau [0] (2509) | - | Survivor's Manteau: VIT+10, MDEF+5 |
| Shoes | Sleipnir [0] (2410) | - | Sleipnir |
| Accessory 1 | Earring [1] (2622) | Phen (4077) | Earring [1], Phen |
| Accessory 2 | Brisingamen [0] (2630) | - | Brisingamen |

## Ninja

_Equip-check identity: base job `Ninja`, class type `Normal`._

### Ninja - Magic Ninja (INT/DEX, ninjutsu)

Source/basis: irowiki classic Ninja (Magic Ninja)

**Mid tier (lv ~70-90)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Asura [3] (13011) | - | Asura [3] (Ninja dagger, MATK+10%) |
| Shield / Left hand | - | - | - |
| Upper head | Crown [0] (2235) | - | Crown: INT+2 |
| Mid head | Robo Eye [0] (5325) | - | Robo Eye |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Ninja Suit [1] (2359) | Evil Druid (4141) | Ninja Suit [1], Evil Druid |
| Garment | Muffler [1] (2504) | Raydric (4133) | Muffler [1], Raydric |
| Shoes | Shoes [1] (2404) | Verit (4107) | Shoes [1], Verit |
| Accessory 1 | Glove [0] (2604) | - | Glove |
| Accessory 2 | Earring [0] (2602) | - | Earring |

**Endgame (lv 99)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Bazerald [0] (1231) | - | Bazerald +10 (INT+5, MATK+10%) - wiki alternative to Asura |
| Shield / Left hand | - | - | - |
| Upper head | Diadem [1] (5313) | Evil Snake Lord (4330) | Diadem [1] (top+mid), Evil Snake Lord |
| Mid head | (covered by upper headgear) | - | - |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Ninja Suit [1] (2359) | Marc (4105) | Ninja Suit [1], Marc |
| Garment | Captain's Manteau [1] (2538) | Raydric (4133) | Captain's Manteau [1], Raydric |
| Shoes | Sleipnir [0] (2410) | - | Sleipnir |
| Accessory 1 | Earring [1] (2622) | Phen (4077) | Earring [1], Phen |
| Accessory 2 | Brisingamen [0] (2630) | - | Brisingamen |

### Ninja - Throwing Huuma (STR/DEX)

Source/basis: irowiki classic Ninja (Throwing Ninja)

**Mid tier (lv ~70-90)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Huuma Giant Wheel Shuriken [4] (13302) | 4x Hydra (4035) | Huuma Giant Wheel Shuriken [4], 4x Hydra |
| Shield / Left hand | (two-handed weapon) | - | - |
| Upper head | Magni's Cap [0] (5122) | - | Magni's Cap |
| Mid head | Angel Wing Ears [0] (5074) | - | Angel Wing Ears |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Ninja Suit [1] (2359) | Peco Peco (4031) | Ninja Suit [1], Peco Peco |
| Garment | Muffler [1] (2504) | Raydric (4133) | Muffler [1], Raydric |
| Shoes | Battle Greaves [1] (2435) | Green Ferus (4381) | Battle Greaves [1], Green Ferus |
| Accessory 1 | Clip [1] (2607) | Mantis (4079) | Clip [1], Mantis |
| Accessory 2 | Clip [1] (2607) | Zerom (4064) | Clip [1], Zerom |

**Endgame (lv 99)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Huuma Calm Mind [2] (13304) | 2x Hydra (4035) | Huuma Calm Mind [2] (Throw Huuma +30%, no cast cancel), 2x Hydra. Alt: Huuma Blaze Shuriken (185 ATK, Fire) |
| Shield / Left hand | (two-handed weapon) | - | - |
| Upper head | Orc Hero Headdress [1] (5375) | Vanberk (4411) | Orc Hero Headdress [1], Vanberk |
| Mid head | (covered by upper headgear) | - | - |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Ninja Suit [1] (2359) | Peco Peco (4031) | Ninja Suit [1], Peco Peco |
| Garment | Captain's Manteau [1] (2538) | Raydric (4133) | Captain's Manteau [1], Raydric |
| Shoes | Sleipnir [0] (2410) | - | Sleipnir |
| Accessory 1 | Megingjard [0] (2629) | - | Megingjard |
| Accessory 2 | Brisingamen [0] (2630) | - | Brisingamen |

## Gunslinger

_Equip-check identity: base job `Gunslinger`, class type `Normal`._

### Gunslinger - Desperado revolver (DEX/VIT/INT)

Source/basis: irowiki classic Gunslinger (DEX/VIT/INT Desperado)

**Mid tier (lv ~70-90)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Garrison [2] (13105) | 2x Hydra (4035) | Garrison [2], 2x Hydra |
| Shield / Left hand | (two-handed weapon) | - | - |
| Upper head | Ulle's Cap [1] (5123) | Vesper (4374) | Ulle's Cap [1] (wiki), Vesper |
| Mid head | Robo Eye [0] (5325) | - | Robo Eye |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Odin's Blessing [1] (2353) | Pupa (4003) | Odin's Blessing [1] (wiki), Pupa |
| Garment | Muffler [1] (2504) | Raydric (4133) | Muffler [1], Raydric |
| Shoes | Boots [1] (2406) | Verit (4107) | Boots [1], Verit |
| Accessory 1 | Clip [1] (2607) | Zerom (4064) | Clip [1], Zerom |
| Accessory 2 | Clip [1] (2607) | Zerom (4064) | Clip [1], Zerom |

**Endgame (lv 99)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Wasteland's Outlaw [2] (13107) | 2x Hydra (4035) | Wasteland's Outlaw [2] +10 (ASPD/HIT from AGI), 2x Hydra |
| Shield / Left hand | (two-handed weapon) | - | - |
| Upper head | Ulle's Cap [1] (5123) | Vesper (4374) | Ulle's Cap [1], Vesper |
| Mid head | Robo Eye [0] (5325) | - | Robo Eye |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Odin's Blessing [1] (2353) | Peco Peco (4031) | Odin's Blessing [1], Peco Peco |
| Garment | Muffler [1] (2504) | Raydric (4133) | Muffler [1], Raydric (GS cannot wear Valkyrian/Captain/Commander manteaus) |
| Shoes | Sleipnir [0] (2410) | - | Sleipnir |
| Accessory 1 | Glove [1] (2624) | Zerom (4064) | Glove [1] (lv90), Zerom |
| Accessory 2 | Brisingamen [0] (2630) | - | Brisingamen |

### Gunslinger - Lever Action crit rifle (AGI/DEX/LUK)

Source/basis: irowiki classic Gunslinger (Lever Action build: 2x Drosera)

**Mid tier (lv ~70-90)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Dusk [1] (13153) | Soldier Skeleton (4086) | Dusk [1] (CRIT+10), Soldier Skeleton |
| Shield / Left hand | (two-handed weapon) | - | - |
| Upper head | Ulle's Cap [1] (5123) | Vesper (4374) | Ulle's Cap [1], Vesper |
| Mid head | Robo Eye [0] (5325) | - | Robo Eye |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Mink Coat [1] (2311) | Peco Peco (4031) | Mink Coat [1], Peco Peco |
| Garment | Muffler [1] (2504) | Raydric (4133) | Muffler [1], Raydric |
| Shoes | Boots [1] (2406) | Matyr (4097) | Boots [1], Matyr |
| Accessory 1 | Clip [1] (2607) | Zerom (4064) | Clip [1], Zerom |
| Accessory 2 | Rosary [0] (2608) | - | Rosary: LUK+2 |

**Endgame (lv 99)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Lever Action Rifle [2] (13170) | 2x Drosera (4421) | Lever Action Rifle [2] (CRIT+50), 2x Drosera (wiki) |
| Shield / Left hand | (two-handed weapon) | - | - |
| Upper head | Ulle's Cap [1] (5123) | Vesper (4374) | Ulle's Cap [1], Vesper |
| Mid head | Robo Eye [0] (5325) | - | Robo Eye |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Odin's Blessing [1] (2353) | Peco Peco (4031) | Odin's Blessing [1], Peco Peco |
| Garment | Muffler [1] (2504) | Raydric (4133) | Muffler [1], Raydric |
| Shoes | Sleipnir [0] (2410) | - | Sleipnir |
| Accessory 1 | Glove [1] (2624) | Zerom (4064) | Glove [1], Zerom |
| Accessory 2 | Brisingamen [0] (2630) | - | Brisingamen (LUK+10) |

## Super Novice

_Equip-check identity: base job `SuperNovice`, class type `Normal`._

### Super Novice - Battle Super Novice (STR/AGI/DEX, Angel set)

Source/basis: irowiki classic Super Novice; Angel set is the SN-exclusive set (combo: HP+900, SP+100, autocast Assumptio)

**Mid tier (lv ~70-90)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Cinquedea [2] (1246) | 2x Skeleton Worker (4092) | Cinquedea [2] (SN-only), 2x Skeleton Worker |
| Shield / Left hand | Angelic Guard [1] (2116) | Thara Frog (4058) | Angelic Guard [1] (set piece), Thara Frog |
| Upper head | Angel's Kiss [1] (5125) | Nightmare (4127) | Angel's Kiss [1] (set piece), Nightmare |
| Mid head | Angel Wing Ears [0] (5074) | - | Angel Wing Ears |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Angelic Protection [1] (2355) | Peco Peco (4031) | Angelic Protection [1] (MDEF+20, set piece), Peco Peco |
| Garment | Angelic Cardigan [1] (2521) | Raydric (4133) | Angelic Cardigan [1] (set piece), Raydric |
| Shoes | Angel's Reincarnation [1] (2420) | Matyr (4097) | Angel's Reincarnation [1] (set piece), Matyr |
| Accessory 1 | Clip [1] (2607) | Mantis (4079) | Clip [1], Mantis |
| Accessory 2 | Clip [1] (2607) | Mantis (4079) | Clip [1], Mantis |

**Endgame (lv 99)**

| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Angelic Wing Dagger [2] (13005) | Minorous (4126) + Skeleton Worker (4092) | Angelic Wing Dagger [2] (SN-only, 120 ATK), Minorous + Skeleton Worker |
| Shield / Left hand | Angelic Guard [1] (2116) | Thara Frog (4058) | Angelic Guard [1], Thara Frog |
| Upper head | Angel's Kiss [1] (5125) | Vanberk (4411) | Angel's Kiss [1], Vanberk (keep for the Angel set) |
| Mid head | Angel Wing Ears [0] (5074) | - | Angel Wing Ears |
| Lower head | Well-Chewed Pencil [0] (5574) | - | Well-Chewed Pencil |
| Armor | Angelic Protection [1] (2355) | Peco Peco (4031) | Angelic Protection [1], Peco Peco |
| Garment | Angelic Cardigan [1] (2521) | Raydric (4133) | Angelic Cardigan [1], Raydric |
| Shoes | Angel's Reincarnation [1] (2420) | Green Ferus (4381) | Angel's Reincarnation [1], Green Ferus (Sleipnir if you drop the set) |
| Accessory 1 | Megingjard [0] (2629) | - | Megingjard |
| Accessory 2 | Brisingamen [0] (2630) | - | Brisingamen |

## Shared / universal picks

Items that show up for many classes - good candidates for the permanent Cash Shop list.

| Item (Id) | AegisName | Slots | Lv | Who can equip | Why |
|---|---|---|---|---|---|
| Sleipnir (2410) | Sleipnir | 0 | 94 | all jobs | Sleipnir - lv94, +20% HP/SP, +25% speed, all jobs (incl. Super Novice) |
| Brisingamen (2630) | Brysinggamen | 0 | 94 | all jobs | Brisingamen - lv94, +6 STR/AGI/VIT/INT, +10 LUK, all jobs |
| Megingjard (2629) | Magingiorde | 0 | 94 | all jobs | Megingjard - lv94, STR+40, all jobs (melee BiS accessory) |
| Asprika (2541) | Asprika | 0 | 94 | all jobs | Asprika - lv94 garment, -30% all elements from weapon attacks, FLEE+30, Teleport lv1 |
| Valkyrian Armor (2357) | Valkyrie_Armor | 1 | 1 | all jobs except Novice, SuperNovice; **trans-only** | Valkyrian Armor - trans-only, all stats +1, class-dependent bonus |
| Valkyrian Manteau (2524) | Valkyrie_Manteau | 1 | 1 | all jobs except Novice, SuperNovice; **trans-only** | Valkyrian Manteau - trans-only |
| Valkyrian Shoes (2421) | Valkyrie_Shoes | 1 | 1 | all jobs except Novice, SuperNovice; **trans-only** | Valkyrian Shoes - trans-only |
| Valkyrja's Shield (2115) | Valkyrja's_Shield | 1 | 65 | all jobs except Novice, SuperNovice | Valkyrja's Shield - lv65, -20% Water/Fire/Shadow/Undead |
| Orc Hero Headdress (5375) | L_Orc_Hero_Helm | 1 | 1 | all jobs | Orc Hero Headdress - top+mid, STR+2, autocast Weapon Perfection; no job/level lock |
| Diadem (5313) | Diadem | 1 | 1 | all jobs | Diadem - top+mid, INT+1, MATK+3%, cast -3%, all jobs (caster BiS here) |
| Feather Beret (5170) | Feather_Beret | 0 | 1 | all jobs except Novice, SuperNovice | Feather Beret - -10% Demi-Human (WoE/PvP) |
| Sunglasses (2202) | Sunglasses_ | 1 | 1 | all jobs | Sunglasses [1] |
| Well-Chewed Pencil (5574) | Pencil_In_Mouth | 0 | 10 | all jobs | Well-Chewed Pencil - DEX+2, HIT+3, all jobs |
| Robo Eye (5325) | Robo_Eye | 0 | 10 | all jobs | Robo Eye - DEX+1, +2% dmg, +2% MATK |
| Angel Wing Ears (5074) | Ear_Of_Angel's_Wing | 0 | 70 | all jobs | Angel Wing Ears - STR+1 |
| Clip (2607) | Clip | 1 | 1 | all jobs | Clip [1] - the universal accessory card holder |
| Orleans's Glove (2701) | Orleans_Glove | 1 | 90 | all jobs except Novice, SuperNovice; **trans-only** | Orleans's Glove [1] - trans-only DEX+2 MATK+3% (2785 'Orlean's Gloves' is a duplicate variant) |
| Morrigane's Helm (5127) | Morrigane's_Helm | 0 | 61 | all jobs except Novice, SuperNovice | Morrigane's Helm (set with 2519/2650/2651: STR+2, LUK+9, CRIT+13, ATK+18) - crit Sin X/Stalker alt |
| Morpheus's Hood (5126) | Morpheus's_Hood | 0 | 33 | all jobs except Novice, SuperNovice | Morpheus's Hood (set with 2518/2649/2648: INT+5, no cast cancel, cast +25%) - Asura/caster alt |
| Assaulter Plate (2376) | Assaulter_Plate | 1 | 80 | Alchemist, Blacksmith, Crusader, Knight, Merchant, StarGladiator, Swordman, Taekwon | Assaulter Plate / Captain's Manteau (2538) / Battle Greaves (2435) - WoE set combo: VIT+3, MaxHP+12%, +10% healing received |
| Lord Kaho's Horn (5013) | Horn_Of_Lord_Kaho | 0 | 1 | all jobs | Lord Kaho's Horn - STR+5 AGI+10 VIT+10 INT+5 LUK+20, all jobs: very overpowered, only sell if you want a 'god item' |

**Universal cards**

| Card (Id) | Slot | Effect / use |
|---|---|---|
| Raydric Card (4133) | Garment | Raydric: -20% Neutral (every garment) |
| Noxious Card (4334) | Garment | Noxious: -10% ranged, -10% Neutral |
| Deviling Card (4174) | Garment | Deviling: -50% Neutral but +50% Water/Earth dmg taken |
| Thara Frog Card (4058) | Left_Hand | Thara Frog: -30% Demi-Human (shield) |
| Marc Card (4105) | Armor | Marc: freeze immunity |
| Evil Druid Card (4141) | Armor | Evil Druid: INT+1, undead armor (freeze/stone immune) |
| Peco Peco Card (4031) | Armor | Peco Peco: MaxHP +10% |
| Angeling Card (4054) | Armor | Angeling: Holy armor (Grand Cross) |
| Ghostring Card (4047) | Armor | Ghostring: Ghost armor |
| Green Ferus Card (4381) | Shoes | Green Ferus: VIT+1, HP+10% |
| Matyr Card (4097) | Shoes | Matyr: AGI+1, HP+10% |
| Verit Card (4107) | Shoes | Verit: HP/SP +8% |
| Mantis Card (4079) | Both_Accessory | Mantis: STR+3 |
| Zerom Card (4064) | Both_Accessory | Zerom: DEX+3 |
| Kukre Card (4027) | Both_Accessory | Kukre: AGI+2 |
| Phen Card (4077) | Both_Accessory | Phen: no cast interruption (cast +25%) |
| Smokie Card (4044) | Both_Accessory | Smokie: Hiding |
| Nightmare Card (4127) | Head_Low, Head_Mid, Head_Top | Nightmare: sleep immunity, AGI+1 |
| Vanberk Card (4411) | Head_Low, Head_Mid, Head_Top | Vanberk: STR+2, crit proc |
| Evil Snake Lord Card (4330) | Head_Low, Head_Mid, Head_Top | Evil Snake Lord: INT+3, blind/curse immunity |
| Kiel-D-01 Card (4403) | Head_Low, Head_Mid, Head_Top | Kiel-D-01: after-cast delay -30% |
| Hydra Card (4035) | Right_Hand | Hydra: +20% vs Demi-Human |
| Minorous Card (4126) | Right_Hand | Minorous: +15% vs Large |
| Skeleton Worker Card (4092) | Right_Hand | Skeleton Worker: +15% vs Medium |
| Abysmal Knight Card (4140) | Right_Hand | Abysmal Knight: +25% vs Boss |
| Doppelganger Card (4142) | Right_Hand | Doppelganger: ASPD +10% |
| Archer Skeleton Card (4094) | Right_Hand | Archer Skeleton: +10% ranged dmg |

## Verified item index (every Id used above)

| Id | AegisName | Name | Type | Slots | Lv | Who can equip |
|---|---|---|---|---|---|---|
| 1102 | Sword_ | Sword | Weapon/1hSword | 4 | 2 | Alchemist, Assassin, Blacksmith, Crusader, Knight, Merchant, Novice, Rogue, SuperNovice, Swordman, Thief |
| 1137 | Excalibur | Excalibur | Weapon/1hSword | 0 | 40 | Alchemist, Assassin, Blacksmith, Crusader, Knight, Merchant, Rogue, Swordman, Thief |
| 1145 | Holy_Avenger | Holy Avenger | Weapon/1hSword | 0 | 75 | Crusader |
| 1172 | Claymore_ | Claymore | Weapon/2hSword | 2 | 33 | Crusader, Knight |
| 1185 | Violet_Fear | Violet Fear | Weapon/2hSword | 2 | 80 | Crusader, Knight, Swordman; **trans-only** |
| 1208 | Main_Gauche_ | Main Gauche | Weapon/Dagger | 4 | 1 | Alchemist, Archer, Assassin, BardDancer, Blacksmith, Crusader, Hunter, Knight, Mage, Merchant, Ninja, Novice, Rogue, Sage, SoulLinker, SuperNovice, Swordman, Thief, Wizard |
| 1220 | Gladius_ | Gladius | Weapon/Dagger | 3 | 24 | Alchemist, Archer, Assassin, BardDancer, Blacksmith, Crusader, Hunter, Knight, Mage, Merchant, Ninja, Rogue, Sage, SoulLinker, Swordman, Thief, Wizard |
| 1230 | House_Auger | Ice Pick | Weapon/Dagger | 0 | 36 | Alchemist, Archer, Assassin, BardDancer, Blacksmith, Crusader, Hunter, Knight, Mage, Merchant, Ninja, Rogue, Sage, SoulLinker, Swordman, Thief, Wizard |
| 1231 | Bazerald | Bazerald | Weapon/Dagger | 0 | 36 | Alchemist, Archer, Assassin, BardDancer, Blacksmith, Crusader, Hunter, Knight, Mage, Merchant, Ninja, Rogue, Sage, SoulLinker, Swordman, Thief, Wizard |
| 1246 | Cinquedea_ | Cinquedea | Weapon/Dagger | 2 | 30 | Novice, SuperNovice |
| 1253 | Katar_ | Katar | Weapon/Katar | 2 | 33 | Assassin |
| 1266 | Infiltrator_ | Infiltrator | Weapon/Katar | 1 | 75 | Assassin |
| 1306 | War_Axe | War Axe | Weapon/1hAxe | 1 | 76 | Alchemist, Blacksmith |
| 1361 | Two_Handed_Axe_ | Two-Handed Axe | Weapon/2hAxe | 2 | 30 | Alchemist, Blacksmith, Crusader, Knight, Merchant, Swordman |
| 1376 | Heart_Breaker | Heart Breaker | Weapon/2hAxe | 1 | 70 | Alchemist, Blacksmith, Crusader, Knight, Merchant, Swordman; **trans-only** |
| 1387 | Giant_Axe | Giant Axe | Weapon/2hAxe | 1 | 50 | Alchemist, Blacksmith, Crusader, Knight, Merchant, Swordman; **trans-only** |
| 1408 | Pike_ | Pike | Weapon/1hSpear | 4 | 4 | Crusader, Knight, Swordman |
| 1422 | Hunting_Spear | Hunting Spear | Weapon/1hSpear | 1 | 60 | Crusader, Knight, Swordman; **trans-only** |
| 1473 | Wizardy_Staff | Wizardry Staff | Weapon/2hStaff | 0 | 90 | Mage, Sage, SoulLinker, Wizard |
| 1539 | Golden_Mace_ | Golden Mace | Weapon/Mace | 2 | 40 | Acolyte, Monk, Priest |
| 1544 | Lunakaligo | Lunakaligo | Weapon/Mace | 3 | 50 | Acolyte, Monk, Priest; **trans-only** |
| 1551 | Bible | Bible | Weapon/Book | 2 | 27 | Priest, Sage, StarGladiator |
| 1560 | Diary_Of_Great_Sage | Sage's Diary | Weapon/Book | 2 | 60 | Priest, Sage, StarGladiator |
| 1561 | Hardback | Hardcover Book | Weapon/Book | 1 | 55 | Priest, Sage, StarGladiator |
| 1616 | Staff_Of_Wing | Wing Staff | Weapon/Staff | 0 | 40 | Mage, Sage, SoulLinker, Wizard |
| 1618 | Survival_Rod_ | Survivor's Rod | Weapon/Staff | 1 | 24 | Acolyte, Mage, Monk, Priest, Sage, SoulLinker, Wizard |
| 1625 | Healing_Staff | Healing Staff | Weapon/Staff | 0 | 55 | Acolyte, Monk, Priest |
| 1633 | BF_Staff2 | Warlock's Battle Wand | Weapon/Staff | 0 | 80 | Acolyte, Mage, Monk, Priest, Sage, SoulLinker, Wizard |
| 1644 | Piercing_Staff_M | Staff of Piercing | Weapon/Staff | 0 | 70 | Acolyte, Mage, Monk, Priest, Sage, Wizard; **trans-only** |
| 1646 | La'cryma_Stick | La'cryma Stick | Weapon/Staff | 2 | 50 | Mage, Sage, Wizard; **trans-only** |
| 1705 | Composite_Bow_ | Composite Bow | Weapon/Bow | 4 | 4 | Archer, BardDancer, Hunter, Rogue, Thief |
| 1716 | Kakkung_ | Gakkung Bow | Weapon/Bow | 2 | 33 | Archer, BardDancer, Hunter, Rogue, Thief |
| 1745 | Falken_Blitz | Falken Blitz | Weapon/Bow | 2 | 50 | Archer, BardDancer, Hunter; **trans-only** |
| 1806 | Hora_ | Studded Knuckles | Weapon/Knuckle | 3 | 12 | Monk, Priest |
| 1815 | Claw_Of_Garm | Hatii Claw | Weapon/Knuckle | 1 | 70 | Monk, Priest |
| 1822 | Combo_Battle_Glove | Combo Battle Glove | Weapon/Knuckle | 4 | 60 | Monk, Priest |
| 1908 | Guitar_ | Guitar | Weapon/Musical | 1 | 27 | BardDancer; Male only |
| 1922 | Oriental_Lute_ | Oriental Lute | Weapon/Musical | 2 | 65 | BardDancer; Male only |
| 1925 | Cello | Cello | Weapon/Musical | 3 | 70 | BardDancer; **trans-only**; Male only |
| 1957 | Rante_ | Rante Whip | Weapon/Whip | 1 | 30 | BardDancer; Female only |
| 1976 | Queen's_Whip_ | Queen's Whip | Weapon/Whip | 2 | 65 | BardDancer; Female only |
| 1980 | Whip_Of_Balance | Whip of Balance | Weapon/Whip | 3 | 70 | BardDancer; **trans-only**; Female only |
| 2005 | Dea_Staff | Dea Staff | Weapon/2hStaff | 1 | 50 | Acolyte, Monk, Priest; **trans-only** |
| 2102 | Guard_ | Guard | Armor | 1 | 1 | all jobs |
| 2104 | Buckler_ | Buckler | Armor | 1 | 1 | Acolyte, Alchemist, Assassin, BardDancer, Blacksmith, Crusader, Knight, Merchant, Monk, Priest, Rogue, Swordman, Thief |
| 2115 | Valkyrja's_Shield | Valkyrja's Shield | Armor | 1 | 65 | all jobs except Novice, SuperNovice |
| 2116 | Angel's_Safeguard | Angelic Guard | Armor | 1 | 20 | Novice, SuperNovice |
| 2128 | Herald_Of_GOD_ | Sacred Mission | Armor | 1 | 83 | Crusader |
| 2130 | Cross_Shield | Cross Shield | Armor | 1 | 80 | Crusader |
| 2131 | Magic_Study_Vol1 | Magic Bible Vol1 | Armor | 1 | 70 | Mage, Sage, SoulLinker, Wizard |
| 2202 | Sunglasses_ | Sunglasses | Armor | 1 | 1 | all jobs |
| 2217 | Biretta_ | Biretta | Armor | 1 | 1 | Acolyte, Monk, Priest |
| 2229 | Helm_ | Helm | Armor | 1 | 1 | Crusader, Knight, Swordman |
| 2235 | Crown | Crown | Armor | 0 | 45 | all jobs except Novice, SuperNovice |
| 2285 | Apple_Of_Archer | Apple of Archer | Armor | 0 | 30 | all jobs except Novice, SuperNovice |
| 2311 | Mink_Coat | Mink Coat | Armor | 1 | 30 | all jobs except Novice, SuperNovice |
| 2315 | Chain_Mail_ | Chain Mail | Armor | 1 | 1 | Alchemist, Assassin, Blacksmith, Crusader, Knight, Merchant, Rogue, Swordman, Thief |
| 2317 | Plate_Armor_ | Full Plate | Armor | 1 | 40 | Crusader, Knight, Swordman |
| 2326 | Saint_Robe_ | Saint's Robe | Armor | 1 | 1 | Acolyte, Alchemist, Blacksmith, Merchant, Monk, Priest |
| 2331 | Tights_ | Tights | Armor | 1 | 45 | Archer, BardDancer, Hunter |
| 2336 | Thief_Clothes_ | Thief Clothes | Armor | 1 | 1 | Assassin, Ninja, Rogue, Thief |
| 2342 | Full_Plate_Armor_ | Legion Plate Armor | Armor | 1 | 70 | Crusader |
| 2353 | Odin's_Blessing | Odin's Blessing | Armor | 1 | 65 | all jobs except Novice, SuperNovice |
| 2355 | Angel's_Protection | Angelic Protection | Armor | 1 | 40 | Novice, SuperNovice |
| 2357 | Valkyrie_Armor | Valkyrian Armor | Armor | 1 | 1 | all jobs except Novice, SuperNovice; **trans-only** |
| 2359 | Ninja_Suit_ | Ninja Suit | Armor | 1 | 50 | Assassin, Ninja, Rogue, Thief |
| 2360 | Robe_Of_Casting_ | Robe of Cast | Armor | 1 | 75 | Sage, SoulLinker, Wizard |
| 2373 | Holy_Robe_ | Holy Robe | Armor | 1 | 60 | Acolyte, Monk, Priest |
| 2374 | Diabolus_Robe | Diabolus Robe | Armor | 1 | 55 | Acolyte, Archer, BardDancer, Hunter, Mage, Monk, Priest, Sage, Wizard; **trans-only** |
| 2376 | Assaulter_Plate | Assaulter Plate | Armor | 1 | 80 | Alchemist, Blacksmith, Crusader, Knight, Merchant, StarGladiator, Swordman, Taekwon |
| 2379 | Warlock_Battle_Robe | Warlock's Battle Robe | Armor | 1 | 80 | Mage, Sage, SoulLinker, Wizard |
| 2404 | Shoes_ | Shoes | Armor | 1 | 1 | all jobs except Novice, SuperNovice |
| 2406 | Boots_ | Boots | Armor | 1 | 1 | Alchemist, Archer, Assassin, BardDancer, Blacksmith, Crusader, Gunslinger, Hunter, Knight, Merchant, Rogue, StarGladiator, Swordman, Taekwon, Thief |
| 2410 | Sleipnir | Sleipnir | Armor | 0 | 94 | all jobs |
| 2420 | Angel's_Arrival | Angel's Reincarnation | Armor | 1 | 25 | Novice, SuperNovice |
| 2424 | Tidal_Shoes | Tidal Shoes | Armor | 1 | 55 | all jobs except Novice, SuperNovice; **trans-only** |
| 2433 | Diabolus_Boots | Diabolus Boots | Armor | 1 | 1 | Alchemist, Assassin, BardDancer, Blacksmith, Crusader, Hunter, Knight, Monk, Priest, Rogue, Sage, SoulLinker, StarGladiator, Wizard; **trans-only** |
| 2435 | Battle_Greave | Battle Greaves | Armor | 1 | 80 | Alchemist, Assassin, Blacksmith, Crusader, Knight, Merchant, Ninja, Rogue, StarGladiator, Swordman, Taekwon, Thief |
| 2436 | Combat_Boots | Combat Boots | Armor | 1 | 80 | Acolyte, Archer, BardDancer, Hunter, Mage, Monk, Priest, Sage, SoulLinker, Wizard |
| 2504 | Muffler_ | Muffler | Armor | 1 | 1 | all jobs except Novice, SuperNovice |
| 2506 | Manteau_ | Manteau | Armor | 1 | 1 | Alchemist, Assassin, Blacksmith, Crusader, Knight, Merchant, Rogue, StarGladiator, Swordman, Taekwon, Thief |
| 2509 | Clack_Of_Servival | Survivor's Manteau | Armor | 0 | 75 | Mage, Sage, SoulLinker, Wizard |
| 2514 | Pauldron | Pauldron | Armor | 1 | 80 | Alchemist, Assassin, Blacksmith, Crusader, Knight, Merchant, Rogue, Swordman, Thief |
| 2521 | Angel's_Warmth | Angelic Cardigan | Armor | 1 | 20 | Novice, SuperNovice |
| 2524 | Valkyrie_Manteau | Valkyrian Manteau | Armor | 1 | 1 | all jobs except Novice, SuperNovice; **trans-only** |
| 2528 | Wool_Scarf | Wool Scarf | Armor | 1 | 55 | all jobs except Novice, SuperNovice; **trans-only** |
| 2537 | Diabolus_Manteau | Diabolus Manteau | Armor | 1 | 1 | Alchemist, Assassin, BardDancer, Blacksmith, Crusader, Hunter, Knight, Monk, Priest, Rogue, Sage, SoulLinker, StarGladiator, Wizard; **trans-only** |
| 2538 | Commander_Manteau | Captain's Manteau | Armor | 1 | 80 | Alchemist, Assassin, Blacksmith, Crusader, Knight, Merchant, Ninja, Rogue, StarGladiator, Swordman, Taekwon, Thief |
| 2539 | Commander_Manteau_ | Commander's Manteau | Armor | 1 | 80 | Acolyte, Archer, BardDancer, Hunter, Mage, Monk, Priest, Sage, SoulLinker, Wizard |
| 2602 | Earring | Earring | Armor | 0 | 20 | all jobs except Novice, SuperNovice |
| 2603 | Necklace | Necklace | Armor | 0 | 20 | all jobs except Novice, SuperNovice |
| 2604 | Glove | Glove | Armor | 0 | 20 | all jobs except Novice, SuperNovice |
| 2607 | Clip | Clip | Armor | 1 | 1 | all jobs |
| 2608 | Rosary | Rosary | Armor | 0 | 20 | all jobs except Novice, SuperNovice |
| 2622 | Earring_ | Earring | Armor | 1 | 90 | all jobs except Novice, SuperNovice |
| 2624 | Glove_ | Glove | Armor | 1 | 90 | all jobs except Novice, SuperNovice |
| 2626 | Rosary_ | Rosary | Armor | 1 | 90 | all jobs except Novice, SuperNovice |
| 2629 | Magingiorde | Megingjard | Armor | 0 | 94 | all jobs |
| 2630 | Brysinggamen | Brisingamen | Armor | 0 | 94 | all jobs |
| 2701 | Orleans_Glove | Orleans's Glove | Armor | 1 | 90 | all jobs except Novice, SuperNovice; **trans-only** |
| 2729 | Diabolus_Ring | Diabolus Ring | Armor | 1 | 1 | Alchemist, Assassin, BardDancer, Blacksmith, Crusader, Hunter, Knight, Monk, Priest, Rogue, Sage, SoulLinker, StarGladiator, Wizard; **trans-only** |
| 4003 | Pupa_Card | Pupa Card | Card | 0 | 1 | card: Armor |
| 4027 | Kukre_Card | Kukre Card | Card | 0 | 1 | card: Both_Accessory |
| 4031 | Pecopeco_Card | Peco Peco Card | Card | 0 | 1 | card: Armor |
| 4035 | Hydra_Card | Hydra Card | Card | 0 | 1 | card: Right_Hand |
| 4043 | Andre_Card | Andre Card | Card | 0 | 1 | card: Right_Hand |
| 4044 | Smokie_Card | Smokie Card | Card | 0 | 1 | card: Both_Accessory |
| 4052 | Elder_Wilow_Card | Elder Willow Card | Card | 0 | 1 | card: Head_Low, Head_Mid, Head_Top |
| 4054 | Angeling_Card | Angeling Card | Card | 0 | 1 | card: Armor |
| 4058 | Thara_Frog_Card | Thara Frog Card | Card | 0 | 1 | card: Left_Hand |
| 4064 | Zerom_Card | Zerom Card | Card | 0 | 1 | card: Both_Accessory |
| 4077 | Phen_Card | Phen Card | Card | 0 | 1 | card: Both_Accessory |
| 4079 | Mantis_Card | Mantis Card | Card | 0 | 1 | card: Both_Accessory |
| 4084 | Marine_Sphere_Card | Marine Sphere Card | Card | 0 | 1 | card: Both_Accessory |
| 4086 | Soldier_Skeleton_Card | Soldier Skeleton Card | Card | 0 | 1 | card: Right_Hand |
| 4092 | Skel_Worker_Card | Skeleton Worker Card | Card | 0 | 1 | card: Right_Hand |
| 4094 | Archer_Skeleton_Card | Archer Skeleton Card | Card | 0 | 1 | card: Right_Hand |
| 4097 | Matyr_Card | Matyr Card | Card | 0 | 1 | card: Shoes |
| 4105 | Marc_Card | Marc Card | Card | 0 | 1 | card: Armor |
| 4107 | Verit_Card | Verit Card | Card | 0 | 1 | card: Shoes |
| 4117 | Side_Winder_Card | Sidewinder Card | Card | 0 | 1 | card: Right_Hand |
| 4126 | Minorous_Card | Minorous Card | Card | 0 | 1 | card: Right_Hand |
| 4127 | Nightmare_Card | Nightmare Card | Card | 0 | 1 | card: Head_Low, Head_Mid, Head_Top |
| 4133 | Daydric_Card | Raydric Card | Card | 0 | 1 | card: Garment |
| 4136 | Khalitzburg_Card | Khalitzburg Card | Card | 0 | 1 | card: Left_Hand |
| 4140 | Knight_Of_Abyss_Card | Abysmal Knight Card | Card | 0 | 1 | card: Right_Hand |
| 4141 | Evil_Druid_Card | Evil Druid Card | Card | 0 | 1 | card: Armor |
| 4142 | Doppelganger_Card | Doppelganger Card | Card | 0 | 1 | card: Right_Hand |
| 4185 | Rideword_Card | Rideword Card | Card | 0 | 1 | card: Head_Low, Head_Mid, Head_Top |
| 4223 | Stalactic_Golem_Card | Stalactic Golem Card | Card | 0 | 1 | card: Head_Low, Head_Mid, Head_Top |
| 4234 | Anolian_Card | Anolian Card | Card | 0 | 1 | card: Armor |
| 4252 | Alligator_Card | Alligator Card | Card | 0 | 1 | card: Both_Accessory |
| 4281 | Zipper_Bear_Card | Zipper Bear Card | Card | 0 | 1 | card: Right_Hand |
| 4330 | Dark_Snake_Lord_Card | Evil Snake Lord Card | Card | 0 | 1 | card: Head_Low, Head_Mid, Head_Top |
| 4366 | Katrinn_Card | Kathryne Keyron Card | Card | 0 | 1 | card: Head_Low, Head_Mid, Head_Top |
| 4368 | Shecil_Card | Cecil Damon Card | Card | 0 | 1 | card: Right_Hand |
| 4374 | Apocalips_H_Card | Vesper Card | Card | 0 | 1 | card: Head_Low, Head_Mid, Head_Top |
| 4381 | Ferus__Card | Green Ferus Card | Card | 0 | 1 | card: Shoes |
| 4403 | Kiel_Card | Kiel-D-01 Card | Card | 0 | 1 | card: Head_Low, Head_Mid, Head_Top |
| 4411 | Vanberk_Card | Vanberk Card | Card | 0 | 1 | card: Head_Low, Head_Mid, Head_Top |
| 4416 | Siroma_Card | Siroma Card | Card | 0 | 1 | card: Both_Accessory |
| 4421 | Drosera_Card | Drosera Card | Card | 0 | 1 | card: Right_Hand |
| 4429 | Salamander_Card | Salamander Card | Card | 0 | 1 | card: Garment |
| 4433 | Imp_Card | Imp Card | Card | 0 | 1 | card: Both_Accessory |
| 4435 | Zombie_Slaughter_Card | Zombie Slaughter Card | Card | 0 | 1 | card: Shoes |
| 4439 | Flame_Skull_Card | Flame Skull Card | Card | 0 | 1 | card: Left_Hand |
| 5027 | Wizardry_Hat | Mage Hat | Armor | 0 | 1 | Mage, Sage, SoulLinker, Wizard |
| 5074 | Ear_Of_Angel's_Wing | Angel Wing Ears | Armor | 0 | 70 | all jobs |
| 5081 | Mistress_Crown | Crown of Mistress | Armor | 0 | 75 | all jobs except Novice, SuperNovice |
| 5122 | Magni_Cap | Magni's Cap | Armor | 0 | 65 | all jobs except Novice, SuperNovice |
| 5123 | Ulle_Cap | Ulle's Cap | Armor | 1 | 65 | all jobs except Novice, SuperNovice |
| 5125 | Kiss_Of_Angel | Angel's Kiss | Armor | 1 | 50 | Novice, SuperNovice |
| 5160 | Magestic_Goat_ | Majestic Goat | Armor | 1 | 1 | Alchemist, Blacksmith, Crusader, Knight, Merchant, StarGladiator, Swordman, Taekwon |
| 5162 | Bone_Helm_ | Bone Helm | Armor | 1 | 70 | Alchemist, Blacksmith, Crusader, Knight, Merchant, Swordman |
| 5170 | Feather_Beret | Feather Beret | Armor | 0 | 1 | all jobs except Novice, SuperNovice |
| 5225 | Marcher_Hat | Parade Hat | Armor | 1 | 10 | all jobs |
| 5313 | Diadem | Diadem | Armor | 1 | 1 | all jobs |
| 5325 | Robo_Eye | Robo Eye | Armor | 0 | 10 | all jobs |
| 5353 | Helm_Of_Sun_ | Hat of the Sun God | Armor | 1 | 1 | Alchemist, Assassin, BardDancer, Blacksmith, Crusader, Hunter, Knight, Monk, Priest, Rogue, Sage, SoulLinker, StarGladiator, Wizard |
| 5361 | Gang_Scarf | Gangster Scarf | Armor | 0 | 60 | all jobs |
| 5375 | L_Orc_Hero_Helm | Orc Hero Headdress | Armor | 1 | 1 | all jobs |
| 5574 | Pencil_In_Mouth | Well-Chewed Pencil | Armor | 0 | 10 | all jobs |
| 13005 | Angelwing_Short_Sword | Angelic Wing Dagger | Weapon/Dagger | 2 | 50 | Novice, SuperNovice |
| 13011 | Asura_ | Asura | Weapon/Dagger | 3 | 12 | Ninja |
| 13038 | Dagger_Of_Hunter | Dagger of Hunter | Weapon/Dagger | 3 | 70 | Rogue; **trans-only** |
| 13105 | The_Garrison_ | Garrison | Weapon/Revolver | 2 | 55 | Gunslinger |
| 13107 | Wasteland_Outlaw | Wasteland's Outlaw | Weapon/Revolver | 2 | 70 | Gunslinger |
| 13153 | Dusk | Dusk | Weapon/Rifle | 1 | 56 | Gunslinger |
| 13170 | Lever_Action_Rifle | Lever Action Rifle | Weapon/Rifle | 2 | 70 | Gunslinger |
| 13302 | Huuma_Giant_Wheel_ | Huuma Giant Wheel Shuriken | Weapon/Huuma | 4 | 42 | Ninja |
| 13304 | Huuma_Calm_Mind | Huuma Calm Mind | Weapon/Huuma | 2 | 70 | Ninja |
| 13414 | Elemental_Sword | Elemental Sword | Weapon/1hSword | 3 | 70 | Alchemist, Assassin, Blacksmith, Crusader, Knight, Merchant, Rogue, Swordman, Thief; **trans-only** |

## Not found in DB / replaced

| Guide item | Status in pre-re DB | What I used instead |
|---|---|---|
| Elite Archer's Suit (iRO WoE armor, Sniper/FAS guide) | not in DB | Improved Tights / Tights [1] mid, Valkyrian Armor endgame |
| Meteor Plate (Paladin tank list) | not in DB | Legion Plate Armor [1] (2342) |
| Nidhoggur's Shadow Garb | not in DB | Valkyrian Manteau / Asprika |
| Diabolus Helmet | not in DB (rest of Diabolus set exists, trans-only) | Feather Beret |
| Orlean's Gown / Orlean's Server (BR Arquimago guide) | exist as Orleans's Gown (2365) / Orleans's Server (2123), trans-only - Gown is cast +15% (slower) so not used | Robe of Cast [1] / Valkyrian Armor |
| Orlean's Glove | exists twice: Orleans's Glove (2701) and Orlean's Gloves (2785, _M variant); **trans-only in this DB** | 2701 for trans classes; Glove/Earring for SL/Ninja/GS |
| Grimoire, Vestimenta Arcana, Sandálias Elegantes, Antique Pipe (BR guide) | not in DB (kRO/bRO-only or custom) | Magic Bible Vol1 [1], Robe of Cast, Shoes [1], Well-Chewed Pencil |
| Hades / Deuses / Natureza sets, 4-slot wings & 'Diadema de Aquário' (BR HP guide) | custom donate items of that BR server | not applicable |
| Kiss of Angel | named Angel's Kiss (5125), Novice/Super Novice only | used for Super Novice Angel set |
| Drooping Kitty | named Drooping Cat (5058) | not needed in builds |
| Holy Bonnet | named Monk Hat (2251) | not used |
| Munak Turban | named Munak Hat (2264) | not used |
| Opera Ghost Mask, Hermode's Cap, Bragi's..., Robe of Judgement, Mental Stick, Heavy Arrow, Memorize Book, Hair Protector, Dark Pinguicula | not in DB | not used |
| Garm card | named Hatii Card (4324) | - |
| Tirfing card | named Ogretooth Card (4254) | - |
| Fur Seal card | named Seal Card (4312) | - |
| Pecopeco card | named Peco Peco Card (4031) | used |
| Antique Firelock card | named Firelock Soldier Card (4160) | - |
| Valkyrie Randgris card | named Randgris Card (4407) | - |
| Jr. Baphomet, Clock Tower Manager, Bacsojin, Beelzebub, Scaraba cards | not in DB | not used |
| Medal of Honor / Brave-Valorous-Glorious weapons (BG rewards) | exist, but are Battleground reward gear | avoided on purpose (their big +% bonuses are meant for BG) |
| Holy Avenger in Paladin endgame (Glorious Holy Avenger) | exists (13418) but BG gear | plain Holy Avenger (1145) |

### Where guides disagreed

- **Lord Knight**: bRO (Esgrimistas) favours crit/LUK two-hand builds; iRO Classic pushes VIT spear (SVD) builds for WoE. Both are covered (spear + two-hand). Muramasa is noted as the crit alternative.
- **Assassin Cross Soul Destroyer**: the wiki only says "Zipper Bear weapons in both hands (or Ice Pick left)" - left-hand choice is debated; both options are listed.
- **High Priest**: iRO Classic = VIT/INT/DEX support; BR private-server guides centre on custom donate gear, so only archetypes were taken.
- **Sniper**: DS/AGI vs Falcon/LUK camps; both listed. Ballista vs Falken Blitz is a matter of taste (raw ATK vs +10% skill dmg).
- **Star Gladiator / Soul Linker / Super Novice**: guides give stat builds but almost no gear lists; gear here is my own pick restricted to what those jobs can equip in this DB.
