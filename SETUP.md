# Setup: local servers + game clients

| | Pre-renewal | Renewal |
|---|---|---|
| Ports | 6900 / 6121 / 5121 | 6901 / 6122 / 5122 |
| Client exe | kRO `2021-11-03_Ragexe_1635926200` | kRO `2026-01-07_Ragexe_1767686776` |
| Client data | kRO full client 2021-11-05 | kRO 2026 package (`Data2026_.rar`, rAthena forum) |
| Game folder | `~/games/kro2021/wine/drive_c/Gravity/RagnarokKRO` | `~/games/kro2026/wine/drive_c/Gravity/kRO2026` |

**Golden rule:** the exe date, the server's packet version and the game data must match. Pre-renewal vs renewal is only a server build flag.

## 1. Local servers
Same `deploy/compose.yml` as the VM; only the host folder differs (`deploy/hosts/local/`).
```bash
./duds.sh up local web status                                 # website + status only (http://localhost:8088)
./duds.sh start local pre                                     # a game server (or re, all)
./duds.sh stop local all
./duds.sh add-user local <username> <M|F> [99]
```
- Local databases use the old volumes (`docker_rathenadb`, `rathena-renewal_db`). Never run `docker compose down -v`.
- Local runs at 1x rates, without the VM's extra NPCs (see [CONFIG.md](CONFIG.md)).
- The server address lives in `char_ip` (char_conf) and `map_ip` (map_conf), never in the exe. Don't touch `login_ip: login`, `char_ip: char` or `*_ip: db` (Docker names).

## 2. Game clients (Linux + Wine)
A client is four parts:
- **exe**: must match the server's date
- **data**: GRF files and `System/`
- **WARP patches**: point the exe at our server and prefer our files
- **`data/clientinfo.xml`**: the server address

Use one Wine setup per client (`export WINEPREFIX=…`). Tools: `sudo dnf install wine winetricks`.

### Patching an exe with WARP
WARP writes a **new**, patched exe; the original stays. The patch lists (sessions) are saved in the repo.
- 2021: `git clone --depth 1 -b rock_win32 https://github.com/Neo-Mind/WARP.git`, session `client/warp_session_2021.yml` (40 patches)
- 2026: `git clone --depth 1 https://github.com/zVictorHG/WARP2026-Project.git WARP2026`, session `client/warp_session_2026.yml` (55 patches)
```bash
cd <WARP folder>                     # the session file goes inside it
wine win32/WARP_console.exe -using <session.yml> -from <original.exe> -to <patched.exe>
cp <patched.exe> "$GAME/"
```

### Pre-renewal client (2021)
1. `export WINEPREFIX=~/games/kro2021/wine && winetricks -q cjkfonts`
2. Data: `curl -LO http://rofull.gnjoy.com/RAG_SETUP_211105.exe && LANG=ko_KR.UTF-8 wine RAG_SETUP_211105.exe`. Don't run its patcher.
3. Exe: `http://ropatch.gnjoy.com/Patchfile_Test/2021-11-03_Ragexe_1635926200.rgz` (sha256 `7d6d0f5400b5cfc8fe6aa366fa293f310f54e3580f0baef5dae617f7b7b575cf`). The `.rgz` holds one file, `RagexeRE.exe`:
   ```bash
   python3 -c 'import gzip,struct;f=gzip.open("2021-11-03_Ragexe_1635926200.rgz")
   while (t:=f.read(1)) not in (b"",b"e"):
       n=f.read(f.read(1)[0])
       if t==b"f": open("2021-11-03_Ragexe_1635926200.exe","wb").write(f.read(struct.unpack("<L",f.read(4))[0]))'
   ```
4. Patch with WARP (session 2021): it includes `DataFolderFirst`, no anti-cheat, and no `1rag1` needed.
5. English: `git clone --depth 1 https://github.com/llchrisll/ROenglishRE.git`, then `client/build_english_prere.sh ROenglishRE english-prere 2021-10-28 && cp -a english-prere/. "$GAME/"`.
6. `data/clientinfo.xml` (also as `sclientinfo.xml`): address `127.0.0.1`, port `6900`, version `55`, `<yellow><admin>2000000</admin></yellow>`.
7. Fixes (the translation is newer than the 2021 data):
   - copy `System/PetEvolutionCln_true.lub` → `_sak.lub`, `monster_size_effect_new.lub` → `monster_size_effect_sak_new.lub`, `SystemEN/PrivateAirplane.lub` → `System/PrivateAirplane_Sakray.lub`, and `AI` → `AI_sakray`
   - run `client/fix_translation_ids.py` in `$GAME`
   - rename `Enchant/EnchantList.lub` and `ItemReform/ItemReformSystem.lub` (in `data/luafiles514/lua files`) to `*.disabled`
8. Run: `cd "$GAME" && wine ragexe_2021_patched.exe`

### Renewal client (2026)
1. `export WINEPREFIX=~/games/kro2026/wine`
2. From rAthena forum topic 149414 (login needed):
   - `2026-01-07_Ragexe_1767686776_VHL_clientinfo_fixed.exe` (an unpacked community copy)
   - `Data2026_.rar` (4.2 GB: kRO 2026 + English + the DLLs the exe needs)
3. Extract with real RAR support (`unar` corrupts files):
   `docker run --rm -v "$PWD":/w:z -w /w debian:stable-slim sh -c 'sed -i "s/Components: main/Components: main non-free/" /etc/apt/sources.list.d/debian.sources && apt-get update && apt-get install -y 7zip 7zip-rar && 7z x Data2026_.rar && chown -R 1000:1000 Data2026'`, then move `Data2026` to the game folder.
4. Patch with WARP2026 (session 2026, with `DataFolderFirst` so our clientinfo wins).
5. `clientinfo.xml`: like pre-renewal, with port `6901`, version `1`.
6. Run: `cd "$GAME" && wine ragexe_2026_patched.exe 1rag1` (this exe needs `1rag1`).
7. Custom items (the event tickets) are in `System/itemInfo_C.lua`.

Portuguese (LatamRO) was tried and dropped: the kRO exe can't use LatamRO's files.

### Launchers
`client/ro2021` / `client/ro2026` start the local server if needed, then the game in the background (log: `~/games/kro20xx/client.log`).
Install them: `cp client/ro20* ~/.local/bin/`.

## 3. Troubleshooting
| Symptom | Fix |
|---|---|
| Client closes at once | missing DLL: `WINEDEBUG=err+module wine …` shows which |
| "cannot open System\X_sak.lub" | copy the existing file to that name |
| "table index is nil" popups | translation newer than the data: remove the line or use the GRF original (`client/grf.py <grf> list/get`) |
| Unknown Korean popup | `WINEDEBUG=-all,+msgbox wine …` logs its text |
| Disconnect at char select | exe date ≠ server packet version |
| Crash in `DDRAW.dll` (2021) | window bigger than the screen: use e.g. 1600×900, windowed |

## 4. Private files (not in git)
- `deploy/hosts/local/`, `deploy/hosts/vm/`: passwords, `accounts.txt`, game configs
- `deploy/files/*.zip`: client zips
- `backups/`: database dumps

On a new clone, add them to `.git/info/exclude` before `git add`:
```
/duds_server/deploy/hosts/*/
/duds_server/deploy/files/*.zip
/duds_server/backups/
```
Old leftovers you can delete: `pre_renewal/`, `renewal/`, `downloads/`, the root `gm_commands.txt`.
