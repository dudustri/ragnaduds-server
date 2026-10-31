# Deploy

Everything runs from the development machine with `./duds.sh`. The VM only needs Docker, the configs and the images.

| | |
|---|---|
| VM | Oracle Cloud (US East), ARM, Ubuntu, `ssh duds` |
| Website | https://ragnaduds.duckdns.org |
| Game | the VM address; the ports are in `deploy/compose.yml` |
| Images | `ghcr.io/dudustri/duds-server-{pre-renewal,renewal,db,web,portal}` |
| Private files | `deploy/hosts/vm/`: `.env` (passwords, `VM_IP`), `accounts.txt`, game configs. Never in git |

## 1. One-time setup
**Development machine**
```bash
sudo dnf install qemu-user-static                                  # build ARM images
docker buildx create --name multiarch --driver docker-container --bootstrap
gh auth refresh -h github.com -s write:packages
gh auth token | docker login ghcr.io -u dudustri --password-stdin
```
Add `Host duds` (VM IP, user `ubuntu`, SSH key) to `~/.ssh/config`.

**The VM**
1. Create it with `vm_provisioning/cloud-init.yaml` (installs Docker, opens the firewall). Reserve the IP.
2. Oracle Security List: open SSH, HTTP/HTTPS and the game and rAthena web ports published in `deploy/compose.yml`.
   Never the database port.
3. Registry login (a GitHub classic token with only `read:packages`), on the VM:
   ` echo 'ghp_TOKEN' | docker login ghcr.io -u dudustri --password-stdin`
4. DuckDNS: point `ragnaduds` to the VM IP.

## 2. First deploy
```bash
./duds.sh release              # build + push the images (~1 h the first time)
./duds.sh up vm                # copy configs, pull, start everything
./duds.sh accounts vm          # server login + all accounts in accounts.txt
./duds.sh autobackup vm        # database backup every 6 h (keeps 7 days)
./duds.sh package pre          # player downloads (address = VM_IP)
./duds.sh package re
./duds.sh files                # upload them (resumable)
```

## 3. Check
- `./duds.sh ps vm`: 12 services "Up".
- Website: status card shows both servers ONLINE; both download buttons work.
- An account can log in on both servers.

| Problem | Fix |
|---|---|
| can't connect at all | ports not open (Security List), or the download has the wrong address |
| stuck at server/char select | `char_ip` in `hosts/vm/<server>/import/char_conf.txt` |
| stuck after picking a character | `map_ip` in `map_conf.txt` |
| char/map say "can't connect to login" | `./duds.sh accounts vm` |

## 4. New players
A new player needs the website link, a website login and a game account (`./duds.sh add-user vm <username> <M|F>`).
The game is downloaded from the website. The installer sets it up, **Start and YEAAAAAAAAAAH!** launches it, and `/hoai` in game turns on the homunculus AI.

## 5. Day to day
| Task | Command |
|---|---|
| Website change | `./duds.sh release web portal` → `./duds.sh up vm web portal` (players stay online) |
| Config or script change | edit `deploy/…` → `./duds.sh up vm` → `./duds.sh restart vm prere-map re-map` (`up` alone doesn't reload scripts) |
| New game/db images | `./duds.sh release [pre_renewal renewal db]` → `./duds.sh up vm` |
| Roll back | `TAG=<old commit>` in `hosts/vm/.env` → `./duds.sh up vm` |
| Stop / start one server | `./duds.sh stop vm pre` · `./duds.sh start vm pre` (`re`, `all`) |
| New account | `./duds.sh add-user vm <username> <M\|F> [99]` |
| Who's online | `./duds.sh online vm` |
| New downloads | `./duds.sh package pre\|re` → `./duds.sh files` |
| Backup to the local machine | `./duds.sh backup vm` (the VM keeps its own in `~/duds/backups`) |
| Restore | `gunzip -c <dump>.sql.gz \| ssh duds 'cd ~/duds && docker compose --env-file hosts/vm/.env exec -T prere-db mariadb -uragnarok -p<PRERE_DB_PASS> ragnarok'` (`re-db` / `RE_DB_PASS` for renewal) |

`up` and `restart` ask first if players are online. The server stays private because the game files are Gravity's.
