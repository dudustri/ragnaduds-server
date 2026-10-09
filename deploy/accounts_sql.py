#!/usr/bin/env python3
"""Print the SQL that sets up game accounts in one rAthena database (used by ./duds.sh accounts <host>).

  python3 accounts_sql.py hosts/vm/accounts.txt hosts/vm/pre_renewal/import/char_conf.txt

- Passwords are stored as MD5 (login_conf use_MD5_passwords: yes).
- Server-to-server login (account 1): set to the userid/passwd in char_conf.txt (a fresh database has s1/p1).
- Every line of accounts.txt ("username password sex group"): created if missing, otherwise password/sex/group
  updated. The account number (account_id) is given by the database automatically.
  Characters and items are never touched. Running it again is safe.
"""
import re, sys


def esc(s):
    return s.replace("\\", "\\\\").replace("'", "\\'")


def conf_value(path, key):
    for line in open(path, encoding="utf-8"):
        m = re.match(rf"^\s*{key}\s*:\s*(\S+)", line)
        if m: return m.group(1)
    sys.exit(f"{key} not found in {path}")


def main(accounts_path, char_conf_path):
    sql = [f"UPDATE login SET userid='{esc(conf_value(char_conf_path, 'userid'))}', "
           f"user_pass=MD5('{esc(conf_value(char_conf_path, 'passwd'))}'), sex='S' WHERE account_id=1;"]
    for n, line in enumerate(open(accounts_path, encoding="utf-8"), 1):
        line = line.split("#", 1)[0].strip() if line.lstrip().startswith("#") else line.strip()
        if not line: continue
        parts = line.split()
        if len(parts) != 4: sys.exit(f"accounts.txt line {n}: need 'username password sex group'")
        user, pw, sex, group = parts
        if not 4 <= len(user) <= 23: sys.exit(f"line {n}: username must be 4-23 characters")
        if not 4 <= len(pw) <= 32: sys.exit(f"line {n}: password must be 4-32 characters")
        if sex not in ("M", "F"): sys.exit(f"line {n}: sex must be M or F")
        if not group.isdigit(): sys.exit(f"line {n}: group must be a number (0 = player, 99 = admin)")
        u, p = esc(user), esc(pw)
        sql.append(f"INSERT INTO login (userid, user_pass, sex, email, group_id) SELECT '{u}', MD5('{p}'), '{sex}', "
                   f"'a@a.com', {group} FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM login WHERE userid='{u}');")
        sql.append(f"UPDATE login SET user_pass=MD5('{p}'), sex='{sex}', group_id={group} WHERE userid='{u}';")
    sql.append("SELECT account_id, userid, sex, group_id FROM login ORDER BY account_id;")
    print("\n".join(sql))


if __name__ == "__main__":
    if len(sys.argv) != 3: sys.exit(__doc__)
    main(*sys.argv[1:])
