#!/usr/bin/env bash
# Server status + Hall of Fame for the website. Every 15 s:
#  - status: do the login, char and map ports answer? (online / starting / offline)
#  - stats (read from each game database): players online, accounts, characters, top 10 characters by level
#    (each with MVP kills and PvP kills: PVP_KILLS from deploy/gm_commands.txt),
#    richest 3, top 3 MVP killers (needs log_mvpdrop: yes). GM accounts (group 99) are left out of the rankings.
# Writes status.json for the web container (served at /status/status.json, behind the website login).
# Runs in the "status" container (deploy/compose.yml): the db image (has the mariadb client), on both game networks.

port() { timeout 2 bash -c "</dev/tcp/$1/$2" 2>/dev/null; }

status() {
  local up=0 hp
  for hp in "$@"; do port "${hp%:*}" "${hp#*:}" && up=$((up + 1)); done
  if [ "$up" -eq "$#" ]; then echo online; elif [ "$up" -eq 0 ]; then echo offline; else echo starting; fi
}

SQL="SELECT JSON_OBJECT(
  'online',   (SELECT COUNT(*) FROM \`char\` WHERE online = 1),
  'accounts', (SELECT COUNT(*) FROM login WHERE sex <> 'S' AND group_id < 99),
  'chars',    (SELECT COUNT(*) FROM \`char\` c JOIN login l USING (account_id) WHERE l.group_id < 99),
  'top',      (SELECT JSON_ARRAYAGG(JSON_OBJECT('name', name, 'class', class, 'base', base_level, 'job', job_level, 'online', online,
                                                 'mvp', mvp, 'pvp', pvp)
                 ORDER BY base_level DESC, job_level DESC, base_exp DESC)
               FROM (SELECT c.name, c.class, c.base_level, c.job_level, c.base_exp, c.online,
                            (SELECT COUNT(*) FROM mvplog m WHERE m.kill_char_id = c.char_id) AS mvp,
                            (SELECT COALESCE(MAX(r.value), 0) FROM char_reg_num r
                              WHERE r.char_id = c.char_id AND r.\`key\` = 'PVP_KILLS' AND r.\`index\` = 0) AS pvp
                     FROM \`char\` c
                     JOIN login l USING (account_id) WHERE l.group_id < 99
                     ORDER BY c.base_level DESC, c.job_level DESC, c.base_exp DESC LIMIT 10) t),
  'rich',     (SELECT JSON_ARRAYAGG(JSON_OBJECT('name', name, 'zeny', zeny) ORDER BY zeny DESC)
               FROM (SELECT c.name, c.zeny FROM \`char\` c JOIN login l USING (account_id)
                     WHERE l.group_id < 99 AND c.zeny > 0 ORDER BY c.zeny DESC LIMIT 3) t),
  'mvp',      (SELECT JSON_ARRAYAGG(JSON_OBJECT('name', name, 'kills', kills) ORDER BY kills DESC)
               FROM (SELECT c.name, COUNT(*) AS kills FROM mvplog m JOIN \`char\` c ON c.char_id = m.kill_char_id
                     JOIN login l ON l.account_id = c.account_id WHERE l.group_id < 99
                     GROUP BY c.char_id ORDER BY kills DESC LIMIT 3) t))"

stats() {   # stats <db host> <password>  → JSON object, or null if the database doesn't answer
  local out
  out=$(MYSQL_PWD="$2" timeout 8 mariadb -h "$1" -uragnarok ragnarok -N -B -r -e "$SQL" 2>/dev/null)
  [ -n "$out" ] && echo "$out" || echo null
}

while true; do
  pre=$(status prere-login:6900 prere-char:6121 prere-map:5121)
  re=$(status re-login:6901 re-char:6122 re-map:5122)
  printf '{"updated":"%s","pre":{"status":"%s","stats":%s},"re":{"status":"%s","stats":%s}}\n' \
    "$(date -Iseconds)" "$pre" "$(stats prere-db "$PRERE_DB_PASS")" "$re" "$(stats re-db "$RE_DB_PASS")" > /out/status.json.tmp
  mv /out/status.json.tmp /out/status.json
  sleep 15
done
