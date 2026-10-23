# RagnaDuds Cash Shop: 3rd-class gear, part 1 of 2 (RENEWAL)

Classes covered: Rune Knight, Royal Guard, Warlock, Sorcerer, Ranger, Minstrel, Wanderer.
Server: rAthena RENEWAL, 10x EXP / 3x drop, max base level 200 for 3rd classes.

Every item and card ID below was looked up in `db/re/item_db_equip.yml` / `db/re/item_db_etc.yml` and checked for
Jobs / Classes / Gender for that class. The last check was a script over this file (see "Verification" at the end). Refine targets and
set notes come from the item `Script:` fields in this DB, not only from the guides.

## Main sources

bRO / LATAM (Portuguese). Per the owner's request these carry the most weight:
- bROWiki class pages (the "Rota básica de Equipamentos" progression): https://browiki.org/wiki/Cavaleiros_R%C3%BAnicos ,
  https://browiki.org/wiki/Guardi%C3%B5es_Reais , https://browiki.org/wiki/Arcanos , https://browiki.org/wiki/Feiticeiros ,
  https://browiki.org/wiki/Sentinelas
- bROWiki "Equipamentos de Honra" (Noblesse / Imperial / Grace skill sets): https://browiki.org/wiki/Equipamentos_de_Honra
- bROWiki "Equipamentos Cinzentos" (Gray Wolf set, level 190+): https://browiki.org/wiki/Equipamentos_Cinzentos
- bROWiki "Equipamento Inicial": https://browiki.org/wiki/Equipamento_Inicial
- The Clutch (BR), "RO LATAM: melhores builds Cavaleiro Rúnico": https://theclutch.com.br/games/ragnarok-online-latam-melhores-builds-cavaleiro-runico/

iRO / international:
- iRO Wiki class pages (Equipment sections): https://irowiki.org/wiki/Rune_Knight , https://irowiki.org/wiki/Royal_Guard ,
  https://irowiki.org/wiki/Warlock , https://irowiki.org/wiki/Sorcerer , https://irowiki.org/wiki/Ranger ,
  https://irowiki.org/wiki/Minstrel , https://irowiki.org/wiki/Severe_Rainstorm
- ROGGH Library: https://roggh.com/pvm-dragon-breath-rune-knight-by-overdrive/ , https://roggh.com/general-ranger-guide/ ,
  https://roggh.com/wargys-wandering-sorcerer-guide/ , https://roggh.com/jareks-warlock-guide/ (seen only in search summaries)
- NovaRO wiki guides (Halves' Royal Guard, Ara's Sorcerer, Wolve's Minstrel, DualityDiscretion's Maestro/Wanderer). I only saw
  these through search-result summaries because the site did not resolve from here, so they back up the choices but were not read directly.

### How the tiers map to the bRO equipment route
bROWiki gives the same basic progression for every 3rd class:
Eden (1-100) → Initial Equipment (100-120) → Excelion / Mora relics (100-130) → **Honor equipment (Noblesse 100 / Imperial 125 / Grace 150) + Temporal Boots** (100-150)
→ **Illusion** (130-160) → **Automatic ("Automatron")** (160-200) → **Gray Wolf ("Cinzentos")** (190-220).
- **Mid tier (base 100-160)** = Honor (Grace) armor for the skill, Grace Attack/Magic garment, boots and ring, Temporal Boots, the class's
  lv100-150 skill weapon, and the Booster shadow set.
- **Endgame (175-200)** = the class's lv170-190 weapon (-LT / -AD / Adulter Fides / "Patent" = Awakened), the Old (lv170) or Temporal (lv170)
  class headgear, Automatic → Gray Wolf armor pieces, and the skill shadow sets.

Legend: `[n]` = slots. "A-type"/"Attack" = physical, "B-type"/"Magic" = magical. Lower-tier Honor pieces with the same bonuses exist:
Noblesse (lv100) and Imperial (lv125) versions of every Grace item. Their IDs are in the Shared section.

---

<!-- job:Knight -->
## Rune Knight

### Build 1: Ignition Break (STR/DEX, two-handed sword; Sonic Wave works as well)
Source consensus: iRO Wiki Ignition Break list, bRO "Especialista em Espadas", ROGGH.

#### Mid (base 100-160)
| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Illusion Tae Goo Lyeon (21050) [2] | Minorous Card (4126) + Skeleton Worker Card (4092) | +9/+10. bRO's Tae Goo Lyeon pick. Cheaper alternative: Ignition Wave Booster Two-handed Sword (600012) [0], which completes the Booster shadow set |
| Upper | Mighty Crown of Ashes (400647) [1] | Kiel-D-01 Card (4403) | bRO `_BR` item. At +7: ATK+50, ASPD+10%. Kiel gives -30% after-cast delay (ACD) |
| Mid | Purified Pigeon (410342) [1] | Purple Ferus Card (300015) | All stats +12, ACD -5% |
| Lower | Old Camouflage Scarf (420110) | – | +1% damage (physical and magic) per 10 base levels |
| Armor | Grace Knight Armor (450087) [1] | Polluted Raydric Card (27354) | bRO Honor set. +9: ATK+100, ASPD+7%, crit damage +10% |
| Garment | Grace Attack Manteau (480018) [1] | Rune Knight Seyren Card (4679) | +9: ACD -5%, +10% vs all. The card is a Rune Knight-only bonus: ASPD+2, +15% vs all races |
| Shoes | Temporal Str Boots (22006) [1] | Green Ferus Card (4381) | +9. Buy the 1-slot version |
| Accessory R | Grace Attack Ring (490019) [1] | Chaotic Mantis Card (27338) | ASPD+7%, VCT -10%, crit damage +10% |
| Accessory L | Jasper Ring (490113) [1] | Chaotic Mantis Card (27338) | STR+7, Ignition Break damage +(BaseLv/3)% |
| Shadow | Rune Knight's Booster Shadow Weapon (24589) + Booster Shadow Armor/Shield/Shoes/Earring/Pendant (24584-24588) | – | Full-set bonus: Ignition Break cooldown -0.5s, autocasts Ignition Break, ignores 70% DEF |

#### Endgame (base 175-200)
| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Thanatos Great Sword-AD (600016) [2] | True Seyren Windsor Card (4689) + Polluted Wanderer Card (27361) | Lv190. Aim for +12 to +14. True Seyren boosts Ignition Break. Alternative: Volar (21051) [2], which has an Ignition Break bonus |
| Upper | Old Rune Circlet (18971) [1] | Kiel-D-01 Card (4403) | +10 or higher. Ignition Break / Hundred Spear +20% per refine pair. At lv180 the Helm of Faith (Rune Knight) (400226) also works |
| Mid | Exiled Ninja's Eyes (410362) [1] | Purple Ferus Card (300015) | ATK+20% (also MATK+20%) |
| Lower | Loyal Servant of the Demon Lord Morroc (420236) | – | iRO pick. Its P.ATK/S.MATK only matter for 4th jobs. It still gives +5% vs demi-human and angel |
| Armor | Automatic Armor Type A (450127) [1] → Gray Wolf Suit (450177) [1] at lv190 | Polluted Raydric Card (27354) (damage) or Amitera Card (300254) (HP) | +9 or higher. Gray Wolf Suit is bRO's lv190 armor |
| Garment | Royal Prontera Cape (480479) [1] | Rune Knight Seyren (MVP) Card (27063) | ATK+20% and an Ignition Break bonus. The MVP card gives ATK+15% and ASPD+2 |
| Shoes | Gray Wolf Boots (470087) [1] (or Automatic Leg Type A (470022) before lv190) | Green Ferus Card (4381) | +7 or higher: +7% ranged damage |
| Accessory R | Document Swordsman (490605) [1] | Chaotic Mantis Card (27338) | Ignition Break +30%, ATK+100, ACD -10% |
| Accessory L | Jasper Ring (490113) [1] | True Seyren Windsor Card (27073) (accessory version) | Stacks Ignition Break bonuses |
| Shadow | Keep the Booster set at +10 (24584-24589), or use Full Penetration Shadow Armor/Shoes/Earring/Pendant (24663, 24664, 24661, 24662) | – | Full Penetration pieces are generic and have no level requirement |

### Build 2: Dragon Breath (VIT/INT/DEX; damage scales with Max HP/SP)
Source consensus: ROGGH (OverDrive), iRO Wiki Dragon Breath list, bRO "Especialista em Dragão".

#### Mid (base 100-160)
| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Dragonic Slayer (600004) [2] | Archer Skeleton Card (4094) x2 | +9/+11. Dragon Breath is ranged damage, so +10% ranged cards apply |
| Upper | Red Baby Dragon (19116) [1] | Bungisngis Card (4582) | +8: Dragon Breath +45%, HP/SP +5% |
| Mid | Purified Pigeon (410342) [1] | Kiel-D-01 Card (4403) | Stats and ACD |
| Lower | Twinhead Dragon Scale (420329) | – | HP+15%, ranged damage +15% |
| Armor | Grace Breath Armor (450086) [1] | Tao Gunka Card (4302) | bRO Honor. HP+20%, VCT -20% at +9. Tao Gunka: HP+100% |
| Garment | Fafnir Breath (480084) [1] | Menblatt Card (4593) | +11 (iRO and ROGGH). Menblatt: +1% ranged damage per 10 DEX |
| Shoes | Temporal Vit Boots (22007) [1] | Green Ferus Card (4381) | ROGGH beginner setup |
| Accessory R | Twin Head Dragon Ring (490413) [1] | Boiling Phen Card (300118) | HP/SP +15%, ACD -15%, Dragon Breath bonus |
| Accessory L | Temporal Ring (28594) [1] | Boiling Phen Card (300118) | ROGGH. Boiling Phen: HP+10%, STR+2 |
| Shadow | Rune Knight's Booster Shadow Weapon (24589) + Booster set (24584-24588) | – | Ignores 70% DEF |

#### Endgame (base 175-200)
| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Dragonic Slayer-LT (600024) [2] (lv190), or Patent Dragonic Slayer (21058) [2] (lv150, "Awakened") | Enhanced Archer Skeleton Card (4633) x2 | +11 or higher |
| Upper | Temporal Circlet (Rune Knight) (19474) [1] | Bungisngis Card (4582) | Dragon Breath +15% per 3 refines. Alternatives: Fafnir Helm (400177), Baby Red Dragon Hat-LT (400400) |
| Mid | Exiled Ninja's Eyes (410362) [1] | Kiel-D-01 Card (4403) | |
| Lower | Twinhead Dragon Scale (420329) | – | |
| Armor | Twinhead Dragon Mail (450216) [1] | Tao Gunka Card (4302) | +12 or higher (iRO). Alternative: Apollo Armor-LT (450295) |
| Garment | Fafnir Breath (480084) [1] | Rune Knight Seyren (MVP) Card (27063) | +11 or higher |
| Shoes | Twinhead Dragon Boots (470274) [1] | Green Ferus Card (4381) | +13 (iRO) |
| Accessory R | Twin Head Dragon Ring (490413) [1] | Boiling Phen Card (300118) | |
| Accessory L | Memento Mori (490207) [1] | Boiling Phen Card (300118) | All stats +10, ATK/MATK +10%, ACD -10% |
| Shadow | Booster set +10 (24584-24589) | – | |

---

<!-- job:Crusader -->
## Royal Guard

### Build 1: Banishing Point / Cannon Spear (STR/DEX/AGI, one-handed spear + shield)
Source consensus: iRO Wiki (Banishing Point and Cannon Spear), NovaRO Halves (search summary), bRO Honor "Traje Perfurante".

#### Mid (base 100-160)
| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Imperial Spear (1433) [1] | Minorous Card (4126) | +9/+10. Banishing Point and Cannon Spear +20%, plus 3% per 2 refines. Alternative: Boost Lance-OS (32019) [2] |
| Shield | Imperial Guard (2153) [1] | Ominous Turtle General Card (27119) | Shield Press bonus. The card gives -25% damage taken from all sizes |
| Upper | Mighty Crown of Ashes (400647) [1] | Kiel-D-01 Card (4403) | bRO `_BR` item |
| Mid | Purified Pigeon (410342) [1] | Purple Ferus Card (300015) | |
| Lower | Arbitrator Shawl (420246) | – | ATK+10%, ACD -5% (iRO) |
| Armor | Grace Spear Armor (450088) [1] | Polluted Raydric Card (27354) | bRO Honor. ATK+100, ASPD, +10% ranged damage at +9 |
| Garment | Grace Attack Manteau (480018) [1] | Royal Guard Randel Card (4680) | The card is Royal Guard-only: DEF+350, +10% vs all races |
| Shoes | Imperial Boots (22207) [0] | – | Banishing Point +10% per level of Cannon Spear. Alternative: Temporal Str Boots (22006) [1] + Green Ferus (4381) |
| Accessory R | Grace Attack Ring (490019) [1] | Chaotic Mantis Card (27338) | |
| Accessory L | Imperial Glove (28551) [1] | Chaotic Mantis Card (27338) | +5% vs all, VCT -10%, casting can't be interrupted |
| Shadow | Royal Guard's Booster Shadow Weapon (24590) + Booster set (24584-24588) | – | Cannon Spear cooldown -0.5s, ignores 70% DEF |

#### Endgame (base 175-200)
| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Aquatic Spear-LT (530019) [2] (lv190), or Patent Aquatic Spear (530006) [2] (lv150) | Polluted Wanderer Card (27361) x2 | +12 to +14. iRO rates Awakened Aquatic Spear the best. Alternative: Boost Lance-OSAD (530031) |
| Shield | Alice Body Pillow (460084) [1] | Ominous Turtle General Card (27119) | +12 (iRO). Its P.ATK/S.MATK bonuses are 4th-job only. It still gives HP/SP +10% and damage per refine |
| Upper | Old Casket of Protection (18983) [1] | Kiel-D-01 Card (4403) | +10 or higher (Cannon Spear). Alternative: Temporal Circlet (Royal Guard) (19475) |
| Mid | Exiled Ninja's Eyes (410362) [1] | Purple Ferus Card (300015) | |
| Lower | Arbitrator Shawl (420246) | – | |
| Armor | Platinum Arbitrator (450257) [1] | Polluted Raydric Card (27354) | +11. Cannon Spear / Pinpoint Attack bonuses |
| Garment | Royal Prontera Cape (480479) [1] | Royal Guard Randel (MVP) Card (27064) | +14 (iRO: large Cannon Spear boost). Alternative: Fallen Protect Manteau (480365), Royal Guard only |
| Shoes | Gray Wolf Boots (470087) [1] | Green Ferus Card (4381) | Alternative from iRO: Ancient Mechanic Greaves (470289) |
| Accessory R | Document Swordsman (490605) [1] | Chaotic Mantis Card (27338) | ATK+100, +10% vs all, ACD -10% |
| Accessory L | Imperial Glove (490600) [1] (lv170, Royal Guard version) | Chaotic Mantis Card (27338) | |
| Shadow | Banishing Cannon Shadow Armor/Shield/Shoes (24578, 24579, 24580) + Royal Guard Shadow Weapon (24289) + Full Penetration Shadow Earring/Pendant (24661, 24662) | – | Set bonus boosts Banishing Point and Cannon Spear |

### Build 2: Genesis Ray (INT/VIT, holy magic, one-handed sword + shield)
Source consensus: iRO Wiki (Genesis Ray: Themis Balance, Themis Helm, Light Blade), bRO Honor "Traje Exorcista".

#### Mid (base 100-160)
| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Light Blade (500003) [2] | Mutated White Knight Card (27384) x2 | +9/+10. Genesis Ray bonus |
| Shield | Themis Balance (28973) [1] | – | Genesis Ray +BaseLv/5 %. At +11, less Genesis Ray cooldown |
| Upper | Themis Helm (15892) [1] | Kiel-D-01 Card (4403) | MATK+25%, ACD -10% |
| Mid | Floating Ball (19380) | – | MATK+35 to +105 depending on DEX |
| Lower | Mob Scarf (28502) | – | |
| Armor | Grace Genesis Armor (450089) [1] | Sweet Nightmare Card (27101) | bRO Honor. MATK+100, holy magic +20% at +9 |
| Garment | Grace Magic Manteau (480019) [1] | Raydric Card (4133) | Defensive. There is no Royal Guard magic garment card in this DB |
| Shoes | Grace Magic Boots (470021) [1] | Verit Card (4107) | +7: fixed cast -0.5s |
| Accessory R | Grace Magic Ring (490020) [1] | – | +10% magic damage, all elements |
| Accessory L | Magician's Gloves (28538) [1] | – | bRO `_BR` item |
| Shadow | Royal Guard's Booster Shadow Weapon (24590) + Booster set (24584-24588) | – | +10% holy magic |

#### Endgame (base 175-200)
| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Light Blade-LT (500038) [2] (lv190), or Adulter Fides Guardian Sword (500025) [2] (lv180) | Mutated White Knight Card (27384) x2 | +11 or higher |
| Shield | Ancient Prontera Book (460092) [1] | – | +10: +20% magic, all elements. At +12: -30% VCT |
| Upper | Helm of Faith (Royal Guard) (400200) [1] | Kiel-D-01 Card (4403) | Lv180, Genesis Ray bonus. Alternative: Divine Guard Hat (5900) |
| Mid | Exiled Ninja's Eyes (410362) [1] | Plaga Card (27310) | |
| Lower | Mob Scarf (28502) | – | |
| Armor | Automatic Armor Type B (450128) [1] → Gray Wolf Robe (450178) [1] | Sweet Nightmare Card (27101) | |
| Garment | Royal Geffen Cape (480520) [1] | Raydric Card (4133) | +20% magic damage, all elements, plus more per refine |
| Shoes | Gray Wolf Shoes (470088) [1] | Verit Card (4107) | |
| Accessory R | Gray Wolf Earring (490108) [1] | – | MATK+7% |
| Accessory L | Gray Wolf Necklace (490109) [1] | – | MATK+7% |
| Shadow | Genesis Shadow Weapon/Pendant/Earring (24581, 24582, 24583) + Royal Guard Shadow Shield (24302) + Full Tempest Shadow Armor/Shoes (24667, 24666) | – | Genesis Ray set bonus |

---

<!-- job:Wizard -->
## Warlock

### Build 1: Crimson Rock (fire; the most beginner-friendly)
Source consensus: iRO Wiki (True Kathryne Keyron, Crimson Rose Stick, Mavka), bRO Honor "Traje Escarlate".

#### Mid (base 100-160)
| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Crimson Rose Stick (26168) [1] (lv100) | Red Pitaya Card (300106) | One-handed staff. Red Pitaya: fire magic +10% with a staff, more at +10 |
| Shield | Excelion Shield (28941) [1] | – | +10 |
| Upper | Magic Crown of Ashes (400646) [1] | Kiel-D-01 Card (4403) | bRO `_BR` item. At +7: MATK+50, VCT -10% |
| Mid | Purified Pigeon (410342) [1] | Plaga Card (27310) | |
| Lower | Mob Scarf (28502) | – | |
| Armor | Grace Crimson Robe (450110) [1] | Sweet Nightmare Card (27101) | bRO Honor. MATK+100, VCT -20%, fire +10% |
| Garment | Grace Magic Manteau (480019) [1] | Warlock Kathryne Card (4678) | Warlock-only card: MATK+15% |
| Shoes | Temporal Int Boots (22009) [1] | Verit Card (4107) | |
| Accessory R | Grace Magic Ring (490020) [1] | Mavka Card (27161) | Mavka: fire/earth magic +20% |
| Accessory L | Ring of Pazuzu (490098) [1] | Mavka Card (27161) | Crimson Rock bonus |
| Shadow | Warlock's Booster Shadow Weapon (24595) + Booster set (24584-24588) | – | +10% magic, all elements |

#### Endgame (base 175-200)
| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Crimson Rose Stick (26158) [2] (lv170) | True Kathryne Keyron Card (4686) + Red Pitaya Card (300106) | +10 or higher. True Kathryne gives Crimson Rock +20% to +60% |
| Shield | Ancient Prontera Book (460092) [1] | – | +10 or higher |
| Upper | Old Magic Stone Hat (18978) [1] | Kiel-D-01 Card (4403) | +10 or higher (iRO) |
| Mid | Exiled Ninja's Eyes (410362) [1] | Plaga Card (27310) | Crimson Rock bonus, MATK+20% |
| Lower | Old Camouflage Scarf (420110) | – | |
| Armor | Automatic Armor Type B (450128) [1] → Gray Wolf Robe (450178) [1] | Sweet Nightmare Card (27101) | |
| Garment | Royal Geffen Cape (480520) [1] | Warlock Kathryne (MVP) Card (27062) | |
| Shoes | Zodiac Boots (Mage) (470258) [1], or Gray Wolf Shoes (470088) | Verit Card (4107) | Zodiac Boots have a Crimson Rock bonus |
| Accessory R | Document Mage (490608) [1] | Mavka Card (27161) | MATK+100/+10%, ACD -10% |
| Accessory L | Record of Mage 2 (490418) [1] | Mavka Card (27161) | |
| Shadow | Crimson Shadow Armor/Shield/Shoes (24518, 24519, 24520) + Warlock Shadow Weapon (24296) + Full Tempest Shadow Earring/Pendant (24665, 24668) | – | Crimson Rock set bonus |

### Build 2: Comet (neutral, screen-wide AoE; add Soul Expansion for ghost monsters)
Source consensus: iRO Wiki Comet (Document Mage, Record of Mage vol.2, Old Magic Stone Hat, Kardui Ears), bRO "Arcanos: Cometa".

#### Mid (base 100-160)
| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Illusion Wizardry Staff (2039) [2] | Spell Addicted Plaga Card (300114) x2 | Two-handed staff. Spell Addicted Plaga: neutral magic +10% with a staff, more at +10 |
| Upper | Magic Crown of Ashes (400646) [1] | Kiel-D-01 Card (4403) | |
| Mid | Kardui Ears (19252) | – | bRO `_BR` item. VCT down at DEX 108 and 120 |
| Lower | Mob Scarf (28502) | – | |
| Armor | Four of a Kind (450226) [1] | Sweet Nightmare Card (27101) | Comet bonus (iRO) |
| Garment | Grace Magic Manteau (480019) [1] | Warlock Kathryne Card (4678) | |
| Shoes | Temporal Int Boots (22009) [1] | Verit Card (4107) | |
| Accessory R | Grace Magic Ring (490020) [1] | True Kathryne Keyron Card (27070) | Accessory version: Comet +50% |
| Accessory L | Geffenia Ice Magic Tool (490029) [1] | True Kathryne Keyron Card (27070) | Comet / Jack Frost bonus |
| Shadow | Warlock's Booster Shadow Weapon (24595) + Booster set (24584-24588) | – | |

#### Endgame (base 175-200)
| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Adulter Fides Two-Handed Staff (640019) [2] (lv180) | Spell Addicted Plaga Card (300114) x2 | Comet bonus. Alternatives: Pride Stone (640005) [2] (lv150, iRO), Iron Staff-LT (640027) |
| Upper | Helm of Faith II (Warlock) (400179) [1] (lv180), or Old Magic Stone Hat (18978) | Kiel-D-01 Card (4403) | Both have Comet bonuses |
| Mid | Exiled Ninja's Eyes (410362) [1] | Plaga Card (27310) | |
| Lower | Mob Scarf (28502) | – | |
| Armor | Gray Wolf Robe (450178) [1] | Sweet Nightmare Card (27101) | |
| Garment | Royal Geffen Cape (480520) [1] | Warlock Kathryne (MVP) Card (27062) | |
| Shoes | Gray Wolf Shoes (470088) [1] | Verit Card (4107) | |
| Accessory R | Document Mage (490608) [1] | True Kathryne Keyron Card (27070) | Comet +30% and a Warlock-only Comet bonus (iRO: -20s cooldown) |
| Accessory L | Record of Mage 2 (490418) [1] | True Kathryne Keyron Card (27070) | Comet +30%, VCT -10% |
| Shadow | Warlock Booster set +10, or Full Tempest Shadow Armor/Shoes/Earring/Pendant (24667, 24666, 24665, 24668) | – | |

---

<!-- job:Sage -->
## Sorcerer

### Build 1: Psychic Wave (neutral AoE, the main damage build)
Source consensus: iRO Wiki (Shadow Staff, Sixth Sense Ring, Professor's Mini Glasses, Book of Sorcery, Temporal Circlet (Sorcerer)), ROGGH Wargy, bRO Honor "Traje Psíquico".

#### Mid (base 100-160)
| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Shadow Staff (26118) [2] | Spell Addicted Plaga Card (300114) x2 | +9/+11. One-handed staff. At +9: VCT -10% |
| Shield | Excelion Shield (28941) [1] | – | iRO beginner pick |
| Upper | Magic Crown of Ashes (400646) [1] | Plaga Card (27310) | |
| Mid | Professor's Mini Glasses (410067) [1] | Plaga Card (27310) | +10% magic vs all sizes, Psychic Wave fixed-cast reduction |
| Lower | Book of Sorcery (420182) | – | Sorcerer only. +3% magic vs all sizes per Psychic Wave level |
| Armor | Grace Psychic Robe (450112) [1] | Sweet Nightmare Card (27101) | bRO Honor. MATK+100, VCT -20%, neutral +10% |
| Garment | Grace Magic Manteau (480019) [1] | Sorcerer Celia Card (4671) | Sorcerer-only card: MATK+10%, HP+10% |
| Shoes | Temporal Int Boots (22009) [1] | Verit Card (4107) | |
| Accessory R | Grace Magic Ring (490020) [1] | – | |
| Accessory L | Sixth Sense Ring (490038) [1] | – | INT+7, Psychic Wave +BaseLv/5 % |
| Shadow | Sorcerer's Booster Shadow Weapon (24596) + Booster set (24584-24588) | – | |

#### Endgame (base 175-200)
| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Shadow Staff-LT (550045) [2] (lv190), or Patent Shadow Staff (550012) [2] (lv150, "Awakened") | Spell Addicted Plaga Card (300114) x2 | +11 or higher. Alternative: Thanos Staff-AD (550023) |
| Shield | Ancient Prontera Book (460092) [1] | – | iRO endgame pick |
| Upper | Temporal Circlet (Sorcerer) (19483) [1] | Plaga Card (27310) | iRO: best Psychic Wave headgear |
| Mid | Professor's Mini Glasses (410067) [1], or Exiled Ninja's Eyes (410362) | Plaga Card (27310) | |
| Lower | Book of Sorcery (420182) | – | |
| Armor | Celine's Dress (450179) [1] → Gray Wolf Robe (450178) | Sweet Nightmare Card (27101) | ROGGH endgame: Celine's Dress |
| Garment | Royal Geffen Cape (480520) [1] | Sorcerer Celia (MVP) Card (27055) | |
| Shoes | Fifth Element (470192) [1] | Verit Card (4107) | Scales with elemental summon levels |
| Accessory R | Sixth Sense Ring (490038) [1] | – | Both-hand accessory, so it can go in either slot |
| Accessory L | Record of Mage 2 (490418) [1] | – | Psychic Wave +30% |
| Shadow | Psychic Shadow Armor/Shield/Shoes (24554, 24555, 24556) + Sorcerer Shadow Weapon (24297) + Full Tempest Shadow Earring/Pendant (24665, 24668) | – | Psychic Wave set bonus |

### Build 2: Varetyr Spear (wind; strong single target and boss killing)
Source consensus: ROGGH Wargy (True Celia Alde, Mamaragan, Old Wind Whisper), iRO Wiki, bRO Honor.

#### Mid (base 100-160)
| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Psychic Spear Rod (26169) [1] (lv100) | True Celia Alde Card (4692) | True Celia Alde: Varetyr Spear +20% to +60% |
| Shield | Excelion Shield (28941) [1] | – | |
| Upper | King Of Spirit Circlet (19426) | – | Varetyr bonus, fixed-cast reduction per refine |
| Mid | Purified Pigeon (410342) [1] | Plaga Card (27310) | |
| Lower | Mob Scarf (28502) | – | |
| Armor | Elemental Possession (450242) [1] | Sweet Nightmare Card (27101) | Varetyr bonus (iRO) |
| Garment | Grace Magic Manteau (480019) [1] | Abysmal Phen Card (300149) | Wind magic +3% per refine |
| Shoes | Mamaragan (22243) | – | Varetyr Spear cooldown -1s |
| Accessory R | Grace Magic Ring (490020) [1] | Elvira Card (4577) | Wind/ghost magic +20% |
| Accessory L | Magician's Gloves (28538) [1] | Elvira Card (4577) | bRO `_BR` item |
| Shadow | Varetyr Shadow Weapon/Pendant/Earring (24557, 24558, 24559) + Sorcerer Shadow Shield (24310) | – | Lv99 set, fine for mid tier |

#### Endgame (base 175-200)
| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Psychic Spear Rod (26159) [2] (lv170) | True Celia Alde Card (4692) + Mutated White Knight Card (27384) | Also boosts Psychic Wave. Alternative: Chilling Cane-LT (550046) |
| Shield | Ancient Prontera Book (460092) [1] | – | |
| Upper | Old Wind Whisper (18980) [1] | Plaga Card (27310) | Sorcerer only, Varetyr bonus |
| Mid | Eye of the Storm (410313) | – | Varetyr bonus, +10% vs bosses |
| Lower | Mob Scarf (28502) | – | |
| Armor | Elemental Possession (450242) [1] (+12), or Gray Wolf Robe (450178) | Sweet Nightmare Card (27101) | |
| Garment | Royal Geffen Cape (480520) [1] | Sorcerer Celia (MVP) Card (27055) | |
| Shoes | Fifth Element (470192) [1] | Verit Card (4107) | |
| Accessory R | Document Mage (490608) [1] | Elvira Card (4577) | Varetyr Spear +30% |
| Accessory L | Gray Wolf Necklace (490109) [1] | Elvira Card (4577) | |
| Shadow | Varetyr set (24557-24559) + Sorcerer Shadow Shield (24310) + Full Tempest Shadow Armor/Shoes (24667, 24666) | – | |

---

<!-- job:Hunter -->
## Ranger

### Build 1: Arrow Storm (DEX/AGI, AoE leveling; the most popular build in bRO)
Source consensus: bROWiki Sentinelas ("Tempestade de Flechas" is the most popular), ROGGH Cykie, iRO Wiki (Autumn Headband, Royal Bow).

#### Mid (base 100-160)
| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Royal Bow (18164) [2] | Archer Skeleton Card (4094) x2 | +9/+11. Arrow Storm +12% per 3 refines. Use elemental arrows |
| Upper | Autumn Headband (5898) [1] | Kiel-D-01 Card (4403) | Ranger only. Arrow Storm VCT -100%. At +9, bonus damage |
| Mid | Purified Pigeon (410342) [1] | Purple Ferus Card (300015) | |
| Lower | Old Camouflage Scarf (420110) | – | |
| Armor | Grace Sharp Suit (450090) [1] | Polluted Raydric Card (27354) | bRO Honor "Traje Preciso". ATK+100, ranged damage +10% at +9 |
| Garment | Grace Attack Manteau (480018) [1] | Ranger Cecil Card (4676) | Ranger-only card: bow damage +15%, CRIT+20 |
| Shoes | Temporal Dex Boots (22008) [1] | Green Ferus Card (4381) | |
| Accessory R | Grace Attack Ring (490019) [1] | – | |
| Accessory L | Ring of Ceryneian (490145) [1] | – | DEX+7, ATK+10%, Arrow Storm and Aimed Bolt bonus |
| Shadow | Ranger's Booster Shadow Weapon (24599) + Booster set (24584-24588) | – | |

#### Endgame (base 175-200)
| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Royal Bow-LT (700045) [2] (lv190), or Patent Royal Bow (700018) [2] (lv150) | Enhanced Archer Skeleton Card (4633) x2 | +12 or higher. Alternative: Adulter Fides Ballista (700031) |
| Upper | Temporal Circlet (Ranger) (19484) [1] | Kiel-D-01 Card (4403) | Arrow Storm / Aimed Bolt +20% per 3 refines. Alternative: Helm of Faith (Ranger) (400198) |
| Mid | Exiled Ninja's Eyes (410362) [1] | Purple Ferus Card (300015) | |
| Lower | Old Camouflage Scarf (420110) | – | |
| Armor | Automatic Armor Type A (450127) [1] → Gray Wolf Suit (450177) [1] | Polluted Raydric Card (27354) | |
| Garment | Royal Payon Cape (480504) [1] | Ranger Cecil (MVP) Card (27060) | Ranged damage +20% or more, Arrow Storm bonus |
| Shoes | Ancient Ranger Shoes (470329) [1] | Green Ferus Card (4381) | Arrow Storm / Aimed Bolt bonus |
| Accessory R | Document Archer (490609) [1] | – | ATK+100, +10% vs all, ACD -10% |
| Accessory L | Ring of Ceryneian (490145) [1] | – | |
| Shadow | Booster set +10, or Full Penetration Shadow Armor/Shoes/Earring/Pendant (24663, 24664, 24661, 24662) | – | This DB has no Arrow Storm-specific shadow set for 3rd-class Rangers |

### Build 2: Aimed Bolt (single target; pairs with Warg Strike)
Source consensus: iRO Wiki, ROGGH, bRO Honor "Traje Certeiro".

#### Mid (base 100-160)
| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Scarlet Dragon Leather Bow (700003) [2] | Archer Skeleton Card (4094) x2 | +9: Aimed Bolt +35%. At +11, less cooldown |
| Upper | Wolf Officer Hat (400203) [1] | Kiel-D-01 Card (4403) | Arrow Storm +15%, ACD -10%. Extra bonus with Aimed Bolt 10 |
| Mid | Purified Pigeon (410342) [1] | Purple Ferus Card (300015) | |
| Lower | Old Camouflage Scarf (420110) | – | |
| Armor | Grace Aimed Suit (450091) [1] | Polluted Raydric Card (27354) | bRO Honor |
| Garment | Grace Attack Manteau (480018) [1] | Ranger Cecil Card (4676) | |
| Shoes | Sniping Shoes (470007) [1] | Green Ferus Card (4381) | Aimed Bolt bonus |
| Accessory R | Grace Attack Ring (490019) [1] | – | |
| Accessory L | Ring of Ceryneian (490145) [1] | – | |
| Shadow | Ranger's Booster Shadow Weapon (24599) + Booster set (24584-24588) | – | |

#### Endgame (base 175-200)
| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Scarlet Leather Dragon Bow-LT (700046) [2] (lv190), or Adulter Fides Aiming Bow (700032) [2] (lv180) | Enhanced Archer Skeleton Card (4633) x2 | |
| Upper | Helm of Faith II (Ranger) (400199) [1], or Temporal Circlet (Ranger) (19484) | Kiel-D-01 Card (4403) | |
| Mid | Exiled Ninja's Eyes (410362) [1] | Purple Ferus Card (300015) | |
| Lower | Old Camouflage Scarf (420110) | – | |
| Armor | Assault Suits (450251) [1] | Polluted Raydric Card (27354) | Arrow Storm and Aimed Bolt bonuses. Alternative: Ceres Leather Armor-LT (450293) |
| Garment | Erymanthian Skin (480094) [1] | Ranger Cecil (MVP) Card (27060) | Aimed Bolt bonus |
| Shoes | Ancient Ranger Shoes (470329) [1] | Green Ferus Card (4381) | |
| Accessory R | Document Archer (490609) [1] | – | |
| Accessory L | Ring of Artemis (490471) [1] (lv200) | – | ATK+10%, Aimed Bolt fixed cast -100%. Use Ring of Ceryneian (490145) below lv200 |
| Shadow | Full Penetration Shadow set (24661-24664), or Booster set +10 | – | |

---

<!-- job:BardDancer gender:Male -->
## Minstrel (male Bard line: instruments or bows)

### Build 1: Severe Rainstorm (AGI/DEX, bow; the standard PvM build)
Source consensus: iRO Wiki Severe Rainstorm page (the most detailed), NovaRO Wolve (search summary), bRO Honor "Traje Temporal/Musical".

#### Mid (base 100-160)
| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Narcissus Bow (18170) [2] | Archer Skeleton Card (4094) x2 | iRO: +9 gives Severe Rainstorm +10%, +11 gives -2s cooldown |
| Upper | Crown of Ashes (400648) [1] | Kiel-D-01 Card (4403) | bRO `_BR` (ranged version) |
| Mid | Purified Pigeon (410342) [1] | Purple Ferus Card (300015) | |
| Lower | Old Camouflage Scarf (420110) | – | |
| Armor | Grace Severe Suit (450092) [1] | Polluted Raydric Card (27354) | bRO Honor. ATK+100, VCT -20%, ranged +10% |
| Garment | Grace Attack Manteau (480018) [1] | Menblatt Card (4593) | Wanderer Trentini cards only work for Dancer-line (female) characters |
| Shoes | Jade Crystal Boots (470098) [1] | Green Ferus Card (4381) | Severe Rainstorm and Arrow Vulcan bonus |
| Accessory R | Grace Attack Ring (490019) [1] | – | |
| Accessory L | Record of Archer 2 (490430) [1] | – | Severe Rainstorm +30% |
| Shadow | Minstrel&Wanderer's Booster Shadow Weapon (24600) + Booster set (24584-24588) | – | |

#### Endgame (base 175-200)
| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Narcissus Bow-LT (700049) [2] (lv190) | True Trentini Card (4695) + Enhanced Archer Skeleton Card (4633) | Alternatives: Wind Gale (18188), MH-P89-OSAD (700055), Pigritia Rhythm (700009) |
| Upper | Old Minstrel Song's Hat (18976) [1] | Kiel-D-01 Card (4403) | Male only. Severe Rainstorm +15% per 2 refines. Combines with Record of Archer (iRO) |
| Mid | Exiled Ninja's Eyes (410362) [1] | Purple Ferus Card (300015) | |
| Lower | Old Camouflage Scarf (420110) | – | |
| Armor | Gray Wolf Suit (450177) [1] (or Automatic Armor Type A (450127)) | Polluted Raydric Card (27354) | |
| Garment | Royal Payon Cape (480504) [1] | Menblatt Card (4593) | Severe Rainstorm bonus |
| Shoes | Jade Crystal Boots-LT (470269) [1] | Green Ferus Card (4381) | |
| Accessory R | Document Archer (490609) [1] | – | Severe Rainstorm +30%. On a Maestro/Wanderer, -4s cooldown (iRO) |
| Accessory L | Ring of Storm (490427) [1] | – | Bard/Dancer only. DEX+20, ATK+10%, Severe Rainstorm bonus. Record of Archer (490400) is an alternative for the Old hat combo |
| Shadow | Rainstorm Shadow Armor/Shield/Shoes (24500, 24501, 24502) + Maestro Shadow Weapon (24299) + Full Penetration Shadow Earring/Pendant (24661, 24662) | – | Rainstorm set bonus. Shield + Maestro weapon also ignores 40% DEF |

### Build 2: Metallic Sound / Reverberation (INT, magic, instrument)
Source consensus: iRO Wiki Wanderer (two Sound Amplifiers are required), NovaRO DualityDiscretion (search summary), bRO Honor "Traje Musical".

#### Mid (base 100-160)
| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Trumpet Shell (570002) [2] | Mutated White Knight Card (27384) x2 | Metallic Sound and Reverberation bonus |
| Upper | Magic Crown of Ashes (400646) [1] | Kiel-D-01 Card (4403) | |
| Mid | Floating Ball (19380) | – | |
| Lower | Mob Scarf (28502) | – | |
| Armor | Grace Reverb Suit (450093) [1] | Sweet Nightmare Card (27101) | bRO Honor. MATK+100, neutral magic +20% |
| Garment | Grace Magic Manteau (480019) [1] | – | |
| Shoes | Temporal Int Boots (22009) [1] | Verit Card (4107) | |
| Accessory R | Sound Amplification Device (2899) [1] | – | Metallic Sound +150%, VCT -50% |
| Accessory L | Sound Amplification Device (2899) [1] | – | iRO: wear two |
| Shadow | Minstrel&Wanderer's Booster Shadow Weapon (24600) + Booster set (24584-24588) | – | |

#### Endgame (base 175-200)
| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Trumpet Shell-LT (570027) [2] (lv190) | Mutated White Knight Card (27384) x2 (or True Alphoccio Basil Card (4696) for Reverberation) | Alternative: Adulter Fides Harp (570018) |
| Upper | Temporal Circlet (Wanderer & Minstrel) (19485) [1] | Kiel-D-01 Card (4403) | Metallic Sound and Reverberation +20% per 3 refines |
| Mid | Exiled Ninja's Eyes (410362) [1] | Plaga Card (27310) | |
| Lower | Mob Scarf (28502) | – | |
| Armor | Loud Park (450258) [1] | Sweet Nightmare Card (27101) | Needs Frigg's Song / Gloomy Day learned. Alternative: Gray Wolf Robe (450178) |
| Garment | Royal Geffen Cape (480520) [1] | – | |
| Shoes | Jade Crystal Boots-LT (470269) [1] | Verit Card (4107) | Metallic Sound and Reverberation bonus |
| Accessory R | Metal Pick (490141) [1] | – | INT+7, Metallic Sound +BaseLv/3 % |
| Accessory L | Sound Amplification Device (2899) [1] | True Trentini Card (27079) | The accessory card gives Reverberation +50% |
| Shadow | Metallic Shadow Armor/Shield/Shoes (24506, 24507, 24508) + Vibrating Shadow Weapon/Vibration Shadow Pendant/Earring (24509, 24510, 24511) | – | Metallic Sound and Reverberation set bonuses |

---

<!-- job:BardDancer gender:Female -->
## Wanderer (female Dancer line: whips or bows)

Same skills and most slots as the Minstrel. Only the weapon, upper headgear and garment card differ.

### Build 1: Severe Rainstorm (AGI/DEX, bow)

#### Mid (base 100-160)
| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Narcissus Bow (18170) [2] | Archer Skeleton Card (4094) x2 | Same as Minstrel |
| Upper | Lyrica Hat (5905) [1] | Kiel-D-01 Card (4403) | This DB marks it Female only. At +9: Severe Rainstorm +25% (iRO) |
| Mid | Purified Pigeon (410342) [1] | Purple Ferus Card (300015) | |
| Lower | Old Camouflage Scarf (420110) | – | |
| Armor | Grace Severe Suit (450092) [1] | Polluted Raydric Card (27354) | |
| Garment | Grace Attack Manteau (480018) [1] | Wanderer Trentini Card (4683) | Wanderer only: HP+10%, SP+15%, stats at lv175+ and +10. For damage, use Menblatt (4593) instead |
| Shoes | Jade Crystal Boots (470098) [1] | Green Ferus Card (4381) | |
| Accessory R | Grace Attack Ring (490019) [1] | – | |
| Accessory L | Record of Archer 2 (490430) [1] | – | |
| Shadow | Minstrel&Wanderer's Booster Shadow Weapon (24600) + Booster set (24584-24588) | – | |

#### Endgame (base 175-200)
| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Narcissus Bow-LT (700049) [2] (lv190) | True Trentini Card (4695) + Enhanced Archer Skeleton Card (4633) | Alternatives: Wind Gale (18188), Pigritia Rhythm (700009) |
| Upper | Old Dying Swan (18981) [1] | Kiel-D-01 Card (4403) | Female only. Severe Rainstorm +15% per 2 refines |
| Mid | Exiled Ninja's Eyes (410362) [1] | Purple Ferus Card (300015) | |
| Lower | Old Camouflage Scarf (420110) | – | |
| Armor | Gray Wolf Suit (450177) [1] | Polluted Raydric Card (27354) | |
| Garment | Royal Payon Cape (480504) [1] | Wanderer Trentini (MVP) Card (27067) or Menblatt Card (4593) | |
| Shoes | Jade Crystal Boots-LT (470269) [1] | Green Ferus Card (4381) | |
| Accessory R | Document Archer (490609) [1] | – | Severe Rainstorm -4s cooldown on a Wanderer |
| Accessory L | Ring of Storm (490427) [1] | – | |
| Shadow | Rainstorm Shadow Armor/Shield/Shoes (24500, 24501, 24502) + Wanderer Shadow Weapon (24300) + Full Penetration Shadow Earring/Pendant (24661, 24662) | – | |

### Build 2: Metallic Sound / Reverberation (INT, magic, whip)

#### Mid (base 100-160)
| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Barbed Wire Whip (580002) [2] | Mutated White Knight Card (27384) x2 | Metallic Sound and Reverberation bonus |
| Upper | Magic Crown of Ashes (400646) [1] | Kiel-D-01 Card (4403) | |
| Mid | Floating Ball (19380) | – | |
| Lower | Mob Scarf (28502) | – | |
| Armor | Grace Reverb Suit (450093) [1] | Sweet Nightmare Card (27101) | |
| Garment | Grace Magic Manteau (480019) [1] | Wanderer Trentini Card (4683) | |
| Shoes | Temporal Int Boots (22009) [1] | Verit Card (4107) | |
| Accessory R | Sound Amplification Device (2899) [1] | – | |
| Accessory L | Sound Amplification Device (2899) [1] | – | |
| Shadow | Minstrel&Wanderer's Booster Shadow Weapon (24600) + Booster set (24584-24588) | – | |

#### Endgame (base 175-200)
| Slot | Item (Id) | Card (Id) | Notes |
|---|---|---|---|
| Weapon | Barbed Wire Whip-LT (580027) [2] (lv190) | Mutated White Knight Card (27384) x2 | Alternatives: Adulter Fides Ribbon (580018), Thanatos Whip-AD (580016, better for Severe Rainstorm and melee) |
| Upper | Temporal Circlet (Wanderer & Minstrel) (19485) [1] | Kiel-D-01 Card (4403) | |
| Mid | Exiled Ninja's Eyes (410362) [1] | Plaga Card (27310) | |
| Lower | Mob Scarf (28502) | – | |
| Armor | Loud Park (450258) [1] | Sweet Nightmare Card (27101) | |
| Garment | Royal Geffen Cape (480520) [1] | Wanderer Trentini (MVP) Card (27067) | |
| Shoes | Jade Crystal Boots-LT (470269) [1] | Verit Card (4107) | |
| Accessory R | Metal Pick (490141) [1] | – | |
| Accessory L | Sound Amplification Device (2899) [1] | True Trentini Card (27079) | |
| Shadow | Metallic Shadow Armor/Shield/Shoes (24506, 24507, 24508) + Vibrating Shadow Weapon/Vibration Shadow Pendant/Earring (24509, 24510, 24511) | – | |

---

## Shared / universal picks (many 3rd classes, good cash-shop "bundles")

<!-- job:ANY -->
| Group | Items (Id) | Notes |
|---|---|---|
| Honor sets (bRO "Equipamentos de Honra"), generic pieces | Noblesse / Imperial / Grace **Attack Manteau** (480012, 480016, 480018), **Magic Manteau** (480014, 480017, 480019), **Attack Boots** (470016, 470018, 470020), **Magic Boots** (470017, 470019, 470021), **Attack Ring** (490014, 490017, 490019), **Magic Ring** (490015, 490018, 490020) | Lv100 / 125 / 150. Every class can wear them. The armor is skill-specific (see each class above). Other honor armors in this DB: Noblesse Breath/Knight (450018/450019), Imperial Breath/Knight (450052/450053), and the same pattern for the other skills |
| Temporal Boots | Str (22006), Agi (22010), Vit (22007), Int (22009), Dex (22008), Luk (22005) | The 1-slot versions (Luk 22005 has no slot). bRO route lv100-150 |
| Temporal garments/ring | Temporal Str/Agi/Vit/Int Manteau (20963, 20964, 20965, 20966), Temporal Ring (28594) | |
| Illusion set (lv130) | Illusion Armor A/B (15376/15377), Engine Wing A/B (20933/20934), Leg A/B (22196/22197), Booster R/L (32207/32208), Illusion Shield I/II (460004/460014) | bRO lv130-160 step. A = physical, B = magical |
| Automatic set (lv160) | Armor A/B (450127/450128), Engine Wing A/B (480020/480021), Leg A/B (470022/470023), Booster R/L (490024/490025, physical), Battle Chip R/L (490026/490027, magical), Automatic Shield I/II (460015/460016) | bRO "Automatron", lv160-200. Real servers enchant these at the Automatic NPC. Cash-shop copies come unenchanted |
| Gray Wolf set (lv190) | Suit/Robe (450177/450178), Manteau/Muffler (480091/480090), Boots/Shoes (470087/470088), Pendant/Ring (490106/490107, physical), Earring/Necklace (490108/490109, magical) | bRO "Equipamentos Cinzentos", the final step of the level-200 route |
| Universal headgear | Exiled Ninja's Eyes (410362) (ATK/MATK +20%), Purified Pigeon (410342), Demons Familiar (410071), Old Camouflage Scarf (420110), Mob Scarf (28502), Crown of Ashes / Mighty / Magic Crown of Ashes (400648/400647/400646) | The Crowns are bRO `_BR` items |
| Universal armor/garment | Royal Prontera Cape (480479) (physical), Royal Payon Cape (480504) (ranged), Royal Geffen Cape (480520) (magic), Memento Mori (490207) | |
| Booster shadow set | Booster Shadow Armor/Shield/Shoes/Earring/Pendant (24584-24588) + class Booster weapon (Rune Knight 24589, Royal Guard 24590, Warlock 24595, Sorcerer 24596, Ranger 24599, Minstrel/Wanderer 24600) | The best cheap shadow set. Lv100 |
| Generic endgame shadows | Full Penetration (24661-24664) for physical, Full Tempest (24665-24668) for magic | No level requirement. At refine sum 18 or more: 100% DEF/MDEF ignore on normal monsters |
| Key cards | Kiel-D-01 (4403), Purple Ferus (300015), Plaga (27310), Sweet Nightmare (27101), Polluted Raydric (27354), Tao Gunka (4302), Green Ferus (4381), Verit (4107), Menblatt (4593), Mutated White Knight (27384), Polluted Wanderer (27361), Archer Skeleton / Enhanced (4094/4633), Spell Addicted Plaga (300114), Red Pitaya (300106), Chaotic Mantis (27338), Boiling Phen (300118) | |
| Class MVP garment cards | Rune Knight Seyren (4679 / MVP 27063), Royal Guard Randel (4680 / 27064), Warlock Kathryne (4678 / 27062), Sorcerer Celia (4671 / 27055), Ranger Cecil (4676 / 27060), Wanderer Trentini (4683 / 27067) | Each works only for its own 3rd class (see the card scripts). There is no Minstrel equivalent |
| Optional costume stones (Etc items) | Rune Knight Stone (Garment) (25448) / II (1000296), Royal Guard Stone (Garment) (25713) / II (1000217), Warlock Stone (Garment) (25456) / II (1000213), Wanderer Minstrel Stone (Garment) (25501) / II (1000304), Ranger Stone (Garment) (25416) / II (1000011), Sorcerer Stone (Garment) (25420) / II (25801) | They only work if the costume-enchant flow exists on the server (see npc/re/merchants/malangdo_costume.txt). Test before selling |

---

## Not found in DB / rejected

| Guide item | Why | Replaced with |
|---|---|---|
| Chaos Sword (iRO, Ignition Break) | Not in DB | Thanatos Great Sword-AD (600016) / Illusion Tae Goo Lyeon (21050) |
| Thanatos Fighter Helmet-LT, Thanatos Warrior Helmet (iRO) | Not in DB | Old Rune Circlet (18971), Helm of Faith (Rune Knight) (400226) |
| Smiling Eyes, Grey Wolf Cub in Mouth (iRO) | Only the costume version exists, or missing entirely | Purified Pigeon (410342), Exiled Ninja's Eyes (410362), Old Camouflage Scarf (420110) |
| Abyss Lake Roaring Armor-LT, Black Cat Backpack, Legendary Dragon Shoes (iRO) | Not in DB | Automatic / Gray Wolf pieces, Royal Prontera Cape |
| Awakened Dragonic Slayer (ROGGH) | Not under that name | Patent Dragonic Slayer (21058). "Patent" is the kRO name for Awakened. The same applies to Awakened Aquatic Spear → Patent Aquatic Spear (530006) and Awakened Shadow Staff → Patent Shadow Staff (550012) |
| Abydos Morning Star, Will of Ingrid, Dragon Eye Ring, Saint Knight Armor (iRO) | Not in DB | Dragonic Slayer-LT, Fafnir Breath, Twin Head Dragon Ring |
| Great Hero's Boots (ROGGH) | Name mismatch. The DB has **Great Hero Boots (22238)**, which works as an alternative for any class | – |
| Powerful Archer Skeleton Card (ROGGH) | Not in DB | Enhanced Archer Skeleton Card (4633) |
| Mutating White Knight Card (iRO) | Exists as **Mutated White Knight Card (27384)** | Used as is |
| Rekenber High Guard Card (iRO) | Not in DB | Polluted Wanderer Card (27361) |
| D.Y Card (ROGGH Sorcerer) | Not in DB | Spell Addicted Plaga Card (300114) |
| Pecopeco Card (ROGGH) | Not in DB as a card | Tao Gunka Card (4302) |
| **Sacred Lapel (420187)** (iRO Dragon Breath lower) | **Exists but is Priest-only (Arch Bishop)**, so a Rune Knight can't equip it | Twinhead Dragon Scale (420329) |
| Violent Dragon Shadow Armor-LT, Will of Karasu, Hero's Grace, Reforming Magic Cloak, Magic Compressor (iRO casters) | Not in DB under those names. Magic Compression (480317) does exist | Gray Wolf Robe, Royal Geffen Cape, Grace Magic Manteau |
| Mythical Moonlight Paw (iRO casters) | Not in DB | Gray Wolf Shoes (470088), Fifth Element (470192) |
| Ears of Abyss, Constellation Orb (iRO casters) | Not in DB. Constellation's Protection (420231) is lv250 | Floating Ball, Mob Scarf |
| Speculation (450401) | Exists but is **4th class only (Arch Mage)** | Four of a Kind (450226) |
| Heroic Backpack (iRO Ranger/Minstrel) | Not in DB | Royal Payon Cape (480504) |
| Sound Amplifier (iRO name) | Exists as **Sound Amplification Device (2899)** | Used as is |
| Night Sparrow Hat (iRO Wanderer) | Not in DB | Lyrica Hat (5905) (Female in this DB), Old Dying Swan (18981) |
| **Lyrica Hat for Minstrel** | This DB marks Lyrica Hat (5905) **Gender: Female**, so a Minstrel can't wear it | Old Minstrel Song's Hat (18976) / Crown of Ashes (400648) |
| Wanderer Trentini garment card for Minstrel | Its script only applies to the Dancer line | Menblatt (4593) |
| Helm of Faith (non-II) for Rune Knight / Royal Guard / Sorcerer etc. | They exist, but the 210+ bonuses are 4th-job only. The lv180 part still works | Kept only where it boosts the build's skill |
| Adulter Fides items are fine. **Vivatus Fides** (lv210) and all "M. xxx Shadow" / Time Gap / Furious / Good and Evil gear | Classes: Fourth only, or EquipLevelMin above 200 | Not used |

### Verification
A python3 + PyYAML script parsed every `(Id)` in each class section of this file and checked that it exists and that the section's job
(Knight, Crusader, Wizard, Sage, Hunter, BardDancer + gender) passes the Jobs, Classes (All_Third/Third/Third_Upper) and Gender fields.
Cards were checked for `Type: Card`. The only IDs that fail the check are the rejected ones listed above.
