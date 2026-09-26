# Deploy

Everything runs from your PC with `./duds.sh`. The VM only needs Docker, the configs and the images.

| | |
|---|---|
| VM | Oracle Cloud (US East), ARM, Ubuntu, `ssh duds` |
| Website | https://ragnaduds.duckdns.org |
| Game | `<VM_IP>:6900` (pre-renewal), `:6901` (renewal) |
| Images | `ghcr.io/dudustri/duds-server-{pre-renewal,renewal,db,web}` (private) |
| Private files | `deploy/hosts/vm/`: `.env` (passwords, `VM_IP`), `accounts.txt`, game configs. Never in git |

## 1. One-time setup
**Your PC**
```bash
sudo dnf install qemu-user-static                                  # build ARM images
docker buildx create --name multiarch --driver docker-container --bootstrap
gh auth refresh -h github.com -s write:packages
gh auth token | docker login ghcr.io -u dudustri --password-stdin
```
Add `Host duds` (VM IP, user `ubuntu`, your key) to `~/.ssh/config`.

**The VM**
1. Create it with `vm_provisioning/cloud-init.yaml` (installs Docker, opens the firewall). Reserve the IP.
2. Oracle Security List: open TCP 22, 80, 443, 6900, 6121, 5121, 6901, 6122, 5122, 8888, 8889. Never 3306.
3. Registry login (a GitHub classic token with only `read:packages`), on the VM:
   ` echo 'ghp_TOKEN' | docker login ghcr.io -u dudustri --password-stdin`
4. DuckDNS: point `ragnaduds` to the VM IP.

## 2. First deploy
```bash
./duds.sh release              # build + push the 4 images (~1 h the first time)
./duds.sh up vm                # copy configs, pull, start everything
./duds.sh accounts vm          # server login + all accounts in accounts.txt
./duds.sh autobackup vm        # database backup every 6 h (keeps 7 days)
./duds.sh package pre          # client zips (address = VM_IP)
./duds.sh package re
./duds.sh files                # upload the zips (resumable)
```

## 3. Check
- `./duds.sh ps vm`: 12 services "Up".
- Website: status card shows both servers ONLINE; both download buttons work.
- Log in with your account on both servers.

| Problem | Fix |
|---|---|
| can't connect at all | open ports (Security List), or wrong address in the client |
| stuck at server/char select | `char_ip` in `hosts/vm/<server>/import/char_conf.txt` |
| stuck after picking a character | `map_ip` in `map_conf.txt` |
| char/map say "can't connect to login" | `./duds.sh accounts vm` |

## 4. Friends
Send them: the website link, the website login, and their game account (`./duds.sh add-user vm <username> <M|F>`).
They download a zip, run `Install RagnaDuds.bat` (Windows) or `./install.sh` (Linux), press **Start and YEAAAAAAAAAAH!**, and type `/hoai` in game for the homunculus AI.

## 5. Day to day
| Task | Command |
|---|---|
| Website change | `./duds.sh release web` → `./duds.sh up vm web` (players stay online) |
| Config or script change | edit `deploy/…` → `./duds.sh up vm` → `./duds.sh restart vm prere-map re-map` |
| New game/db images | `./duds.sh release [pre_renewal renewal db]` → `./duds.sh up vm` |
| Roll back | `TAG=<old commit>` in `hosts/vm/.env` → `./duds.sh up vm` |
| Stop / start one server | `./duds.sh stop vm pre` · `./duds.sh start vm pre` (`re`, `all`) |
| New account | `./duds.sh add-user vm <username> <M\|F> [99]` |
| Who's online | `./duds.sh online vm` |
| New client zips | `./duds.sh package pre\|re` → `./duds.sh files` |
| Backup to your PC | `./duds.sh backup vm` (the VM keeps its own in `~/duds/backups`) |
| Restore | `gunzip -c <dump>.sql.gz \| ssh duds 'cd ~/duds && docker compose --env-file hosts/vm/.env exec -T prere-db mariadb -uragnarok -p<PRERE_DB_PASS> ragnarok'` (`re-db` / `RE_DB_PASS` for renewal) |

`up` and `restart` ask first if players are online. Keep it private: the game files are Gravity's.
