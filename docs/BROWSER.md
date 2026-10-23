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
  fields (`patches/robrowser/0001-…`). Login, characters and maps work; newer UIs may still be missing in places.

## Put it on the VM
```bash
./duds.sh release browser web     # the client image + the site with /play and /play-renewal
./duds.sh browser-data            # upload both game folders once (~3.4 GB + ~5 GB, resumable)
./duds.sh up vm browser browser-re web
```
`BROWSER_PRE_GAME` and `BROWSER_RE_GAME` in `deploy/hosts/local/.env` point at your game folders (the source of the
upload and of the local services). The VM keeps its copies in `~/duds/browser-data/pre` and `re`.

## On your PC: viewers and GRF work
`./duds.sh start local pre && ./duds.sh up local browser`, then http://127.0.0.1:3338/ (Renewal: `start local re`,
`up local browser-re`, http://127.0.0.1:3339/): the full launcher with the game and the Map, Model, STR, Effect
and GRF viewers. Making your own maps, sprites and effects:
[grf/README.md](../grf/README.md). On the site the launcher and viewers answer 404.
