# Portal: account requests, website login, password reset

`build/portal` (Go, one binary, SQLite in the `portal_data` volume), behind Caddy (`build/web/Caddyfile`).

## What players see
- **/join** (public): the terms → "I agree", the explicit "no connection with Gravity" statement → "I confirm",
  then an optional message, name, surname, e-mail and the username they want. Saved as *pending* with the
  terms version and both confirmations (date + time).
- **/login**: their own username/password (the same as in the game). Everything else on the site (home, features,
  downloads) needs it: Caddy asks the portal (`forward_auth /auth`).
- **/forgot**: e-mail → their username + a link to choose a new password (2 hours, one use).
- **/account**: change password (game on both servers + website).

## What you (admin) do
- **/admin**: pending requests → APPROVE (creates the game account on both servers and e-mails a
  "choose your password" link, 7 days) or REJECT (optional polite e-mail). Users: new link, disable, admin flag.
- **/admin/outbox**: every e-mail. With SMTP off they are only kept here: open one to copy its link.
- A daily e-mail to `ADMIN_EMAIL` when requests are waiting (`DIGEST_HOUR_UTC`, default 7).
- Admins: game accounts with group 99 were imported as admins. More: `./duds.sh portal vm admin <user>`.

## E-mail (provider)
E-mail goes out through the server's own Gmail (ragnaduds@gmail.com) with an app password (free, ~500 e-mails/day):
turn on 2-Step Verification on that account, create an app password at https://myaccount.google.com/apppasswords,
then in `deploy/hosts/vm/.env`: `SMTP_HOST=smtp.gmail.com`, `SMTP_PORT=587`, `SMTP_USER=ragnaduds@gmail.com`,
`SMTP_PASS=<app password, no spaces>`, `MAIL_FROM="RagnaDuds <ragnaduds@gmail.com>"` (with the quotes: duds.sh reads this file with bash), `ADMIN_EMAIL=<who gets the daily digest>`.
Apply: `./duds.sh config vm env && ./duds.sh up vm portal`. Any SMTP provider works (port 587 STARTTLS or 465 TLS).

## Passwords
- Game passwords are MD5 (`use_MD5_passwords: yes` in hosts/*/*/import/login_conf.txt); `./duds.sh accounts`
  and the portal write MD5. Website passwords: argon2id in SQLite.
- Existing accounts were imported once (`./duds.sh portal vm import`, their game password became their website
  password) and then converted (`./duds.sh portal vm md5`). Players without e-mail: `./duds.sh portal vm link <user>`
  prints a set-password link to send them.
- The launchers keep downloading updates with the shared token (`DL_TOKEN`, `./duds.sh set-password`).

## Privacy
Rejected requests are deleted after 30 days. Sessions last 30 days (`SESSION_DAYS`).
