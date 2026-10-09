#!/usr/bin/env bash
# Duds Server command center (run on your PC).       ./duds.sh help
# Hosts: "local" (this PC) or "vm" (the cloud VM, reached with `ssh $DUDS_SSH`, default "duds").
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEPLOY="$ROOT/deploy"
SSH_HOST="${DUDS_SSH:-duds}"
REMOTE_DIR="${DUDS_REMOTE_DIR:-duds}"          # on the VM: ~/duds
REGISTRY="ghcr.io/dudustri"

# ---- output: green step headers with a progress bar (plain text when not a terminal or NO_COLOR is set) ----
if [[ -t 1 && -z "${NO_COLOR:-}" ]]; then G=$'\e[1;32m'; Y=$'\e[1;33m'; D=$'\e[2m'; N=$'\e[0m'; else G=; Y=; D=; N=; fi
STEP=0; STEPS=1; T0=$SECONDS
bar() {   # bar <done> <total>
    local w=24 f=$(( $1 * 24 / $2 )); local full empty
    full=$(printf '%*s' "$f" ''); empty=$(printf '%*s' $((w - f)) '')
    printf '%s%s' "${full// /█}" "${empty// /░}"
}
steps()  { STEP=0; STEPS="$1"; T0=$SECONDS; }
step()   { STEP=$((STEP + 1)); printf '\n%s━━ [%d/%d] %s %3d%%  %s%s\n' "$G" "$STEP" "$STEPS" "$(bar $((STEP - 1)) "$STEPS")" $(( (STEP - 1) * 100 / STEPS )) "$1" "$N"; }
finish() { printf '\n%s━━ [%d/%d] %s 100%%  ✔ %s%s %s(%ss)%s\n' "$G" "$STEPS" "$STEPS" "$(bar 1 1)" "$1" "$N" "$D" $((SECONDS - T0)) "$N"; }
warn()   { printf '%s%s%s\n' "$Y" "$*" "$N"; }

usage() { cat <<'EOF'
Build & release (PC → GitHub registry)
  release [image...]           build x86+ARM images and push (pre_renewal renewal db web; default: all)
                               tagged :latest and :<git commit>

Run (host = local | vm)
  up <host> [service...]       start/update everything (vm: sync files, pull images, then start)
  restart <host> <service...>  restart services, e.g. prere-map re-char web
  start <host> <pre|re|all>    start one game server (db + login + char + map)
  stop <host> <pre|re|all>     stop one game server (data stays in its volume; the website shows it OFFLINE)
  ps <host>                    container status
  logs <host> [service...]     follow logs (Ctrl+C to stop)
  online <host>                players online per server
  portal <host> <cmd>       website accounts: import | md5 | admin <user> | link <user> (set-password link)
  gm <host> <re|pre> @cmd   run a GM command on a running map server, no restart (e.g. gm vm re @reloadscript)

Configs (hosts/<host>/, never baked into images)
  config <host> [part]         vm: upload configs, no restart. part = pre | re | gm | env | all (default)
  set-password <host> <user>   login for the website (stored as a token, never the password)
  accounts <host>              create/update game accounts from hosts/<host>/accounts.txt on both servers
  add-user <host> <username> <M|F> [group]
                               add or change one game account: asks the password, the account number is automatic.
                               group: 0 = player (default), 99 = admin. Saved in hosts/<host>/accounts.txt

Client downloads
  package <pre|re> [address]   build a client zip into deploy/files/ (address: default VM_IP in hosts/vm/.env)
  files                        upload deploy/files/*.zip to the vm (resumable)

Other
  backup <host>                dump both databases to ./backups/<host>/
  autobackup vm                schedule deploy/backup.sh on the VM every 6 h (keeps 7 days in ~/duds/backups)
  ssh                          open a shell on the vm
EOF
}

compose_local() { (cd "$DEPLOY" && docker compose --env-file hosts/local/.env "$@"); }
compose_vm()    { ssh -t "$SSH_HOST" "cd ~/$REMOTE_DIR && docker compose --env-file hosts/vm/.env $(printf '%q ' "$@")"; }   # %q: args survive the remote shell
dc() { local host="$1"; shift; case "$host" in local) compose_local "$@" ;; vm) compose_vm "$@" ;; *) die "host must be local or vm";; esac; }
die() { echo "error: $*" >&2; exit 1; }
need_host() { [[ "${1:-}" == local || "${1:-}" == vm ]] || die "host must be local or vm"; }

# players online, as "pre-renewal: N, renewal: N" (0 if a server isn't running)
online_count() {
    local script
    script=$(cat <<EOS
set -a; . hosts/$1/.env; set +a
for s in prere re; do
  if [ \$s = prere ]; then p=\$PRERE_DB_PASS; else p=\$RE_DB_PASS; fi
  n=\$(docker compose --env-file hosts/$1/.env exec -T \$s-db mariadb -uragnarok -p"\$p" ragnarok -N -e 'select count(*) from \`char\` where online=1' 2>/dev/null) || n=0
  echo "\$s: \${n:-0}"
done
EOS
)
    if [[ "$1" == local ]]; then (cd "$DEPLOY" && bash -s <<<"$script")
    else ssh "$SSH_HOST" "cd ~/$REMOTE_DIR 2>/dev/null && bash -s" <<<"$script" || echo "(vm not set up yet)"; fi
}
confirm_if_online() {
    local out; out="$(online_count "$1")"; echo "$out" | sed "s/^/  /"
    if grep -qE ': [1-9]' <<<"$out"; then
        warn "Players are online and will be disconnected."
        read -rp "Continue? [y/N] " a; [[ "$a" == y* ]] || exit 1
    fi
}

sync_vm() {
    [[ -f "$DEPLOY/hosts/vm/.env" ]] || die "missing deploy/hosts/vm/.env (copy deploy/hosts/.env.example)"
    ssh "$SSH_HOST" "mkdir -p ~/$REMOTE_DIR/files"
    rsync -av --inplace --delete --exclude 'hosts/local/' --exclude 'files/' --exclude 'accounts.txt' \
        "$DEPLOY/compose.yml" "$DEPLOY/gm_commands.txt" "$DEPLOY/special_maps.txt" "$DEPLOY/re_db_import" \
        "$DEPLOY/welcome.txt" "$DEPLOY/motd.txt" "$DEPLOY/backup.sh" "$DEPLOY/buffer.txt" "$DEPLOY/status.sh" "$DEPLOY/cash_points.txt" "$DEPLOY/homunculus_room.txt" "$DEPLOY/ticket_refiner.txt" "$DEPLOY/jobmaster.txt" "$DEPLOY/stylist.txt" "$DEPLOY/fourth_quests.txt" "$DEPLOY/fourth_quests_a.txt" "$DEPLOY/fourth_quests_b.txt" "$DEPLOY/fourth_quests_c.txt" "$DEPLOY/fourth_quests_d.txt" "$DEPLOY/casino.txt" "$DEPLOY/mvp_room.txt" \
        "$DEPLOY/hosts" "$SSH_HOST:$REMOTE_DIR/"
}

cmd="${1:-help}"; shift || true
case "$cmd" in
  release)
    imgs=("$@"); [[ ${#imgs[@]} -eq 0 ]] && imgs=(pre_renewal renewal db web portal)
    export TAG="$(git -C "$ROOT" rev-parse --short HEAD)" BUILDX_BUILDER="${BUILDX_BUILDER:-multiarch}"
    steps ${#imgs[@]}
    echo "Releasing ${imgs[*]} as :latest and :$TAG (x86 + ARM)"
    for img in "${imgs[@]}"; do
      step "Build + push $img"
      (cd "$ROOT/build" && docker compose build --push "$img")
    done
    finish "Released ${imgs[*]}"
    echo "Deploy with: ./duds.sh up vm   (rollback: set TAG=<old commit> in hosts/vm/.env)";;
  up)
    host="${1:-}"; need_host "$host"; shift
    what="${*:-everything}"
    if [[ "$host" == vm ]]; then steps 4; else steps 2; fi
    step "Check players online ($host)"; confirm_if_online "$host"
    if [[ "$host" == vm ]]; then
      step "Sync config to the VM"; sync_vm
      step "Pull images: $what"; compose_vm pull "$@"
    fi
    step "Start: $what"; dc "$host" up -d "$@"
    finish "$host is up: $what";;
  restart)
    host="${1:-}"; need_host "$host"; shift; [[ $# -gt 0 ]] || die "name the services, e.g. prere-map"
    steps 2
    step "Check players online ($host)"; confirm_if_online "$host"
    step "Restart: $*"; dc "$host" restart "$@"
    finish "Restarted $*";;
  start|stop)
    host="${1:-}"; need_host "$host"; which="${2:-}"
    case "$which" in
      pre) svcs=(prere-db prere-login prere-char prere-map prere-web) ;;
      re)  svcs=(re-db re-login re-char re-map re-web) ;;
      all) svcs=(prere-db prere-login prere-char prere-map prere-web re-db re-login re-char re-map re-web) ;;
      *)   die "usage: $cmd <host> <pre|re|all>" ;;
    esac
    if [[ "$cmd" == stop ]]; then
      steps 2
      step "Check players online ($host)"; confirm_if_online "$host"
      step "Stop: ${svcs[*]}"; dc "$host" stop "${svcs[@]}"
      finish "Stopped $which on $host (website shows OFFLINE within 15 s)"
    else
      steps 1
      step "Start: ${svcs[*]}"; dc "$host" up -d status "${svcs[@]}"
      finish "Started $which on $host (map server needs ~20 s; website shows ONLINE when ready)"
    fi;;
  ps)      need_host "${1:-}"; dc "$1" ps --format 'table {{.Service}}\t{{.Status}}\t{{.Ports}}';;
  logs)    host="${1:-}"; need_host "$host"; shift; dc "$host" logs -f -t --tail 100 "$@";;
  online)  need_host "${1:-}"; online_count "$1";;
  portal)
    host="${1:-}"; need_host "$host"; shift; [[ $# -gt 0 ]] || die "usage: portal <host> import|md5|admin <user>|link <user>"
    dc "$host" exec -T portal portal "$@";;
  gm)
    host="${1:-}"; need_host "$host"; srv="${2:-}"
    [[ "$srv" == re || "$srv" == pre ]] && [[ $# -ge 3 ]] || die "usage: gm <host> <re|pre> @command [args]   e.g. gm vm re @reloadscript"
    shift 2; svc=$([[ "$srv" == re ]] && echo re-map || echo prere-map)
    # the map server reads console lines from stdin ("admin:@cmd"); print what it logged right after
    gm_script=$(cat <<EOS
cid=\$(docker compose --env-file hosts/$host/.env ps -q $svc); since=\$(date -u +%Y-%m-%dT%H:%M:%SZ)
printf '%s\\n' $(printf '%q' "admin:$*") | timeout -s KILL 3 docker attach --sig-proxy=false "\$cid" >/dev/null 2>&1
sleep 2; docker logs --since "\$since" "\$cid" 2>&1 | tail -20
EOS
)
    if [[ "$host" == local ]]; then (cd "$DEPLOY" && bash -s <<<"$gm_script")
    else ssh "$SSH_HOST" "cd ~/$REMOTE_DIR && bash -s" <<<"$gm_script"; fi;;
  config)
    host="${1:-}"; need_host "$host"; what="${2:-all}"
    if [[ "$host" == vm ]]; then
      V="$DEPLOY/hosts/vm"; [[ -d "$V" ]] || die "missing deploy/hosts/vm"
      steps 1; step "Upload config ($what) to the VM"
      ssh "$SSH_HOST" "mkdir -p ~/$REMOTE_DIR/hosts/vm/pre_renewal ~/$REMOTE_DIR/hosts/vm/renewal"
      case "$what" in
        pre)  scp -r "$V/pre_renewal/import" "$SSH_HOST:$REMOTE_DIR/hosts/vm/pre_renewal/" ;;
        re)   scp -r "$V/renewal/import"     "$SSH_HOST:$REMOTE_DIR/hosts/vm/renewal/" ;;
        gm)   scp "$DEPLOY/gm_commands.txt"  "$SSH_HOST:$REMOTE_DIR/" ;;
        env)  scp "$V/.env"                  "$SSH_HOST:$REMOTE_DIR/hosts/vm/" ;;
        all)  sync_vm ;;
        *)    die "config vm [pre|re|gm|env|all]" ;;
      esac
      finish "Config uploaded"
    fi
    cat <<'EOF'
Configs are in place. To apply them:
  battle settings (rates, drops...)  → in game: @reloadbattleconf        (no restart)
  NPC scripts / gm_commands.txt      → in game: @reloadscript            (no restart)
  login/char/map settings (IPs, name, ports, npc lines)
                                     → ./duds.sh restart <host> prere-map (or -char / -login, re-*)  ~15 s
EOF
    ;;
  set-password)
    host="${1:-}"; need_host "$host"; user="${2:?usage: set-password <host> <user>}"
    envf="$DEPLOY/hosts/$host/.env"; [[ -f "$envf" ]] || die "missing $envf"
    read -rsp "Password for $user: " pw; echo
    token=$(printf 'rd:%s:%s' "$user" "$pw" | sha256sum | cut -d' ' -f1)   # same as site/login.html computes
    grep -q '^DL_TOKEN=' "$envf" || echo 'DL_TOKEN=' >> "$envf"
    sed -i "s#^DL_USER=.*#DL_USER=$user#; s#^DL_TOKEN=.*#DL_TOKEN=$token#; /^DL_PASS_HASH=/d" "$envf"
    printf '%s✔ Saved in hosts/%s/.env.%s Apply: ./duds.sh up %s web\n' "$G" "$host" "$N" "$host";;
  accounts)
    host="${1:-}"; need_host "$host"; H="$DEPLOY/hosts/$host"; [[ -f "$H/accounts.txt" ]] || die "missing $H/accounts.txt"
    steps 2
    for s in prere re; do
      d=$([ $s = prere ] && echo pre_renewal || echo renewal); var=$([ $s = prere ] && echo PRERE_DB_PASS || echo RE_DB_PASS)
      step "Game accounts on $s ($host)"
      pw=$(sed -n "s/^$var=\([^ #]*\).*/\1/p" "$H/.env")
      sql=$(python3 "$DEPLOY/accounts_sql.py" "$H/accounts.txt" "$H/$d/import/char_conf.txt")
      run="docker compose --env-file hosts/$host/.env exec -T -e MYSQL_PWD=$pw $s-db mariadb -uragnarok ragnarok -t"
      if [[ "$host" == local ]]; then (cd "$DEPLOY" && bash -c "$run") <<<"$sql"
      else ssh "$SSH_HOST" "cd ~/$REMOTE_DIR && $run" <<<"$sql"; fi
    done
    finish "Accounts ready on both servers";;
  add-user)
    host="${1:-}"; need_host "$host"; user="${2:?usage: add-user <host> <username> <M|F> [group]}"; sex="${3:-}"; group="${4:-0}"
    [[ "$sex" == M || "$sex" == F ]] || die "sex must be M or F"
    [[ "$group" =~ ^[0-9]+$ ]] || die "group must be a number (0 = player, 99 = admin)"
    [[ ${#user} -ge 4 && ${#user} -le 23 && "$user" =~ ^[A-Za-z0-9_]+$ ]] || die "username: 4-23 letters, digits or _"
    read -rsp "Password for $user: " pw; echo; read -rsp "Again: " pw2; echo
    [[ "$pw" == "$pw2" ]] || die "passwords don't match"
    [[ ${#pw} -ge 4 && ${#pw} -le 32 && "$pw" != *" "* ]] || die "password: 4-32 characters, no spaces"
    A="$DEPLOY/hosts/$host/accounts.txt"
    [[ -f "$A" ]] || printf '# Game accounts (created on BOTH servers). Never commit this file.
# username    password             sex  group
' > "$A"
    chmod 600 "$A"
    grep -v "^$user[[:space:]]" "$A" > "$A.tmp" || true
    printf '%-13s %-20s %s    %s\n' "$user" "$pw" "$sex" "$group" >> "$A.tmp"; mv "$A.tmp" "$A"; chmod 600 "$A"
    printf '%s✔ Saved %s in hosts/%s/accounts.txt%s\n' "$G" "$user" "$host" "$N"
    "$0" accounts "$host";;
  autobackup)
    [[ "${1:-}" == vm ]] || die "usage: autobackup vm"
    steps 2
    step "Copy backup.sh to the VM"; sync_vm >/dev/null
    step "Schedule it every 6 hours (cron)"
    ssh "$SSH_HOST" "(crontab -l 2>/dev/null | grep -v duds-backup; echo '0 */6 * * * cd ~/$REMOTE_DIR && ./backup.sh vm >> backups/backup.log 2>&1  # duds-backup') | crontab - && crontab -l | grep duds-backup"
    finish "Backups every 6 h in ~/$REMOTE_DIR/backups on the VM (log: backups/backup.log)";;
  package)
    [[ "${1:-}" == pre || "${1:-}" == re ]] || die "usage: package <pre|re> [address]"
    addr="${2:-$(sed -n 's/^VM_IP=\([^ #]*\).*/\1/p' "$DEPLOY/hosts/vm/.env" 2>/dev/null)}"
    [[ -n "$addr" ]] || die "no address: pass one, or set VM_IP in deploy/hosts/vm/.env"
    steps 1; step "Package the $1 client for $addr"
    python3 "$ROOT/client/package_client.py" "$1" "$addr" "$DEPLOY/files"
    finish "Client zip in deploy/files/";;
  files)
    ls "$DEPLOY"/files/*.zip >/dev/null 2>&1 || die "no zips in deploy/files (run: ./duds.sh package ...)"
    steps 1; step "Upload client zips to the VM (resumable)"
    ssh "$SSH_HOST" "mkdir -p ~/$REMOTE_DIR/files"
    rsync -avP "$DEPLOY"/files/*.zip "$SSH_HOST:$REMOTE_DIR/files/"
    if [[ -d "$DEPLOY/files/patch" ]]; then     # the launcher's per-file updates (only changed files travel)
      rsync -a --delete --info=stats1 "$DEPLOY/files/patch/" "$SSH_HOST:$REMOTE_DIR/files/patch/"
    fi
    finish "Zips and patch files uploaded";;
  backup)
    host="${1:-}"; need_host "$host"; out="$ROOT/backups/$host"; mkdir -p "$out"; stamp=$(date +%F-%H%M)
    steps 2
    for s in prere re; do
      step "Dump the $s database ($host)"
      dump=$(cat <<EOS
set -a; . hosts/$host/.env; set +a
if [ $s = prere ]; then p=\$PRERE_DB_PASS; else p=\$RE_DB_PASS; fi
docker compose --env-file hosts/$host/.env exec -T $s-db mariadb-dump -uragnarok -p"\$p" ragnarok
EOS
)
      if [[ "$host" == local ]]; then (cd "$DEPLOY" && bash -s <<<"$dump") | gzip > "$out/$s-$stamp.sql.gz"
      else ssh "$SSH_HOST" "cd ~/$REMOTE_DIR && bash -s" <<<"$dump" | gzip > "$out/$s-$stamp.sql.gz"; fi
      echo "  $out/$s-$stamp.sql.gz ($(du -h "$out/$s-$stamp.sql.gz" | cut -f1))"
    done
    finish "Backups in backups/$host/";;
  ssh)     exec ssh "$SSH_HOST";;
  help|-h|--help) usage;;
  *) usage; exit 1;;
esac
