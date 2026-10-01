# Cash shop

Full explanation and procedures: [../CASHSHOP-AND-CLIENT.md](../CASHSHOP-AND-CLIENT.md).

# Cash shop research

Gear per class, researched from build guides (iRO Wiki, bROWiki, ROGGH, Brazilian guides) and checked against
this server's item database (every Id exists and the class can equip it). Each build has a **mid** and an
**endgame** table: slot, item (Id), card (Id), notes.

| File | Server | Classes |
|---|---|---|
| `builds-prerenewal-trans.md` | pre-renewal | transcendent classes + Star Gladiator, Soul Linker, Ninja, Gunslinger, Super Novice |
| `builds-renewal-3rd-part1.md` | renewal | Rune Knight, Royal Guard, Warlock, Sorcerer, Ranger, Minstrel, Wanderer |
| `builds-renewal-3rd-part2.md` | renewal | Arch Bishop, Sura, Guillotine Cross, Shadow Chaser, Mechanic, Genetic, Star Emperor, Soul Reaper, Kagerou/Oboro, Rebellion, Expanded Super Novice |

## The shop
Edit `shop.yml` (tabs, items, prices, worn-look replacements), then:
```bash
python3 cashshop/build_shop.py      # builds deploy/re_db_import/item_cash.yml + fixes every item for the client
./duds.sh package re                # the game zip gets the fixes (ragnaduds.grf, System/itemInfo_RD.lua)
./duds.sh up vm                     # the server gets the shop + look fixes
```
- `client_data.py`: what the game client can show (item list, look tables, files), cached in `.cache/`
- `item_assets.py`: real icons, collection pictures and English descriptions from divine-pride.net (cached)
- `build_shop.py`: fixes items the client can't show (all ~29k server items, not just the shop's) and writes the shop
Points: `deploy/cash_points.txt`.
