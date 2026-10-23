# GRF work: your own maps, sprites and effects

Everything happens in this folder, on your PC. `grf/data/` is git-ignored (game files are Gravity's).

```bash
./duds.sh start local pre && ./duds.sh up local browser    # the local browser client: http://127.0.0.1:3338/
```

## 1. Find and copy a file
```bash
./duds.sh grf find poring                                     # list game files with "poring" in the path
./duds.sh grf get 'data\sprite\몬스터\poring.spr'             # copy it to grf/data/sprite/몬스터/poring.spr
```
A brand new file: create it in `grf/data/` with the path the game expects (same folders as in the game data).

## 2. Edit it (Windows tools, run with `wine`)
| What | Files | Tool |
|---|---|---|
| Maps | `.rsw` `.gnd` `.gat` (+ textures, models) | [BrowEdit 3](https://github.com/Borf/browedit3) |
| Sprites (monsters, items, headgears) | `.spr` `.act` | [Act Editor](https://github.com/Tokeiburu/ActEditor) |
| Effects | `.str` | [STR Editor](https://github.com/Tokeiburu/ActEditor) (inside Act Editor) |
| Icons, pictures | `.bmp` (magenta 255,0,255 = transparent) | any image editor |

## 3. See it
Run `./duds.sh grf refresh` after saving (it makes your files readable for the browser server and clears its
cache), then reload http://127.0.0.1:3338/ : the **Map, Model, STR, Effect and GRF viewers** and the game itself
read `grf/data/` **before** the game's GRF, so you see your version.

## 4. Use it in the real game client
```bash
./duds.sh grf pack        # grf/data/ → grf/ragnaduds_dev.grf
```
Put `ragnaduds_dev.grf` in the game folder and add it as the first line of its `DATA.INI` (`0=ragnaduds_dev.grf`,
renumber the others). To ship it to friends, add the files to the download (`client/package_client.py`).

**Example: your face as a hairstyle** (`grf/tools/face_head.py`): copy a head's `.act`/`.spr` to a new style number,
then redraw its frames from a cut-out photo:
```bash
./duds.sh grf get 'data\sprite\인간족\머리통\남\42_남.act'   # then rename both to 43_남.* (a new hairstyle 43)
uv run --no-project --with pillow python3 grf/tools/face_head.py <original 42_남.spr> 'grf/data/sprite/인간족/머리통/남/43_남.spr'
./duds.sh grf refresh
```
The server must allow the new number (`max_hair_style: 43` in the host's `battle_conf.txt`); a GM sets it with
`@hairstyle 43` (hair colour 0: dyes recolour the face).

**A new map** also needs the server side: its `.gat` in the map cache (rAthena `mapcache` tool), its name in
`map_index.txt` and a `map:` line in the host's `map_conf.txt`, then restart the map server.
