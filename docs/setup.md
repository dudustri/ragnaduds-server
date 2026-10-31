# Setup: local servers

The same servers can run locally to test changes before they go to the VM.

```bash
./duds.sh up local web status          # website + status checker only
./duds.sh start local pre              # one game server: pre, re or all
./duds.sh stop local all
./duds.sh add-user local <username> <M|F> [99]
```

- Local uses the same `deploy/compose.yml` as the VM; only the host folder differs (`deploy/hosts/local/`).
- Local databases live in Docker volumes. `docker compose down -v` deletes them, so it is never used here.
- Local runs at 1x rates, without the VM's extra NPCs (see [config.md](config.md)).
- The server address lives in `char_ip` (char_conf) and `map_ip` (map_conf). `login_ip: login`,
  `char_ip: char` and `*_ip: db` must stay as they are: those are Docker names.
- The game client must match the server's packet version. How the clients are prepared is kept out of this
  public repo (private notes in `docs/private/`, git-ignored).

## Private files (not in git)
- `deploy/hosts/local/`, `deploy/hosts/vm/`: passwords, `accounts.txt`, game configs
- `deploy/files/`: the player downloads
- `backups/`: database dumps
- `docs/private/`: private notes

They're listed in `.gitignore`, so a new clone never commits them.
