#!/usr/bin/env bash
# Dumps both game databases to backups/ and keeps the last 7 days. Runs on the VM.
#   ./backup.sh [host]        (host = vm by default; the folder next to this script is ~/duds)
# Scheduled every 6 hours by: ./duds.sh autobackup vm   (cron line tagged "duds-backup")
set -euo pipefail
cd "$(dirname "$0")"
host="${1:-vm}"; env="hosts/$host/.env"
[[ -f "$env" ]] || { echo "missing $env"; exit 1; }
mkdir -p backups
stamp=$(date +%F-%H%M)
for s in prere re; do
  var=$([ $s = prere ] && echo PRERE_DB_PASS || echo RE_DB_PASS)
  pw=$(sed -n "s/^$var=\([^ #]*\).*/\1/p" "$env")
  out="backups/$s-$stamp.sql.gz"
  if docker compose --env-file "$env" exec -T -e MYSQL_PWD="$pw" $s-db \
       mariadb-dump -uragnarok --single-transaction --quick ragnarok 2>/dev/null | gzip > "$out.tmp" \
     && [ "$(gzip -dc "$out.tmp" | head -c 100 | wc -c)" -gt 0 ]; then
    mv "$out.tmp" "$out"; echo "$(date '+%F %T') ok $out ($(du -h "$out" | cut -f1))"
  else
    rm -f "$out.tmp"; echo "$(date '+%F %T') skipped $s (database not running?)"
  fi
done
find backups -name '*.sql.gz' -mtime +7 -delete   # keep 7 days (28 dumps per server)
