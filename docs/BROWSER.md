# Play in the browser

Friends play in the browser on the website (behind the website login), no install, straight to the game login:
**/play** for Pre-Renewal and **/play-renewal** for Renewal. Each server has its own `browser` service
(`browser` and `browser-re`): same image, its own game files and settings (`deploy/browser/pre|re/`).

```mermaid
flowchart LR
    P["Browser<br/>/play"] -->|"HTTPS (site login)"| WEB["web (Caddy)"]
    WEB --> BR["browser<br/>roBrowserLegacy + game files + proxy"]
    BR -->|"WebSocket → TCP<br/>only our 3 game servers"| G["pre-renewal<br/>login · char · map"]
    BR -.->|reads| D[("game folder<br/>(Gravity's files, never in git)")]
```

How a session works:
```mermaid
sequenceDiagram
    participant B as Browser (roBrowser, WebGL)
    participant C as Caddy (site login)
    participant S as browser service
    participant G as Game servers
    B->>C: GET /play (website session cookie)
    C->>S: page + Online.js
    B->>C: GET /play/data/... (maps, sprites, sounds)
    C->>S: files read from the GRF (cached in the browser afterwards)
    B->>C: WebSocket /play/ws/ (login packets)
    C->>S: same WebSocket
    S->>G: plain TCP to login, then char, then map
    G-->>B: game packets back through the same pipe
```
The browser does all the drawing; the server only moves files and game packets, exactly like the desktop client
talks to rAthena.

- **Client**: [roBrowserLegacy](https://github.com/MrAntares/roBrowserLegacy) (GPL-3.0), the `robrowser/` submodule,
  pinned to a tested commit, plus our fixes in `patches/robrowser/` (applied when the image is built). Settings:
  `deploy/browser/<pre|re>/Config.local.js` (same file on your PC and on the site).
- **Game files + proxy**: [roBrowserLegacy-RemoteClient-JS](https://github.com/FranciscoWallison/roBrowserLegacy-RemoteClient-JS),
  pinned in `build/browser/Dockerfile`. The proxy only reaches our three pre-renewal servers and only accepts pages
  from our site (`BROWSER_ORIGINS`).
- **Image**: `build/browser/` → `ghcr.io/dudustri/duds-server-browser`. No game files inside: they're mounted at run time.
- **Renewal (2026 client)** needed two fixes: its GRFs start with "Event Horizon" instead of "Master of Magic"
  (same format otherwise; the image patches the file server to accept it), and our cash shop sends the item preview
  fields (`patches/robrowser/0001-…`); `0002-…` keeps fast cutin animations (the casino) from stacking up. Login, characters and maps work; newer UIs may still be missing in places.

## Put it on the VM
```bash
./duds.sh release browser web     # the client image + the site with /play and /play-renewal
./duds.sh browser-data            # both game folders from the downloads (~3.4 GB + ~5 GB the first time, then only changes)
./duds.sh up vm browser browser-re web
```
The browser's game folders are made **from the friends' downloads** (`client/browser_data.py`, run by
`./duds.sh browser-data` into `deploy/browser-data/`): the same GRFs in the same order, the music, and the item list
the exe ends up with (its layered loader run once in Lua 5.1 and written out as `System/itemInfo_browser.lua`),
the English System files where roBrowser looks for them (`SystemEN/`), and our login picture under the names
roBrowser asks for (`ragnaduds_browser.grf`). Your local GRF work (`grf/`) is mounted only on your PC
(`BROWSER_DEV_DATA` in `deploy/hosts/local/.env`); the VM gets an empty folder. So
after `build_shop.py` → `./duds.sh package re`, run `./duds.sh browser-data` and both clients match. The VM keeps its
copies in `~/duds/browser-data/pre` and `re`.

## On your PC: viewers and GRF work
`./duds.sh start local pre && ./duds.sh up local browser`, then http://127.0.0.1:3338/ (Renewal: `start local re`,
`up local browser-re`, http://127.0.0.1:3339/): the full launcher with the game and the Map, Model, STR, Effect
and GRF viewers. Making your own maps, sprites and effects:
[grf/README.md](../grf/README.md). On the site the launcher and viewers answer 404.
