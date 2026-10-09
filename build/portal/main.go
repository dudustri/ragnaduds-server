// RagnaDuds portal: account requests (terms + "no connection with Gravity"), admin approvals, website login,
// password set/reset by e-mail. One static binary behind Caddy on the game VM (see build/web/Caddyfile).
//
//	portal serve            the website part (default)
//	portal import           one time: copy the existing game accounts into the website users (their current
//	                        plain-text game password becomes their website password)
//	portal md5              one time: store every game password as MD5 (with login_conf use_MD5_passwords: yes)
//	portal admin <user>     make a website user an admin
//	portal link <user>      print a fresh set-password link (e.g. for a player with no e-mail)
package main

import (
	"crypto/hmac"
	"embed"
	"fmt"
	"html/template"
	"io/fs"
	"log"
	"net"
	"net/http"
	"os"
	"strconv"
	"strings"
	"sync"
	"time"
)

//go:embed templates static
var assets embed.FS

func logf(format string, a ...any) { log.Printf(format, a...) }

type Config struct {
	Listen, SiteURL, DBPath string
	GameDSN                 map[string]string
	GameMD5                 bool
	AdminEmail              string
	DigestHourUTC           int
	SessionTTL              time.Duration
	CookieSecure            bool
	TermsVersion            string
	Secret                  string // for the CSRF tokens
}

func env(k, def string) string {
	if v := os.Getenv(k); v != "" {
		return v
	}
	return def
}

func loadConfig() Config {
	hour, _ := strconv.Atoi(env("DIGEST_HOUR_UTC", "7"))
	days, _ := strconv.Atoi(env("SESSION_DAYS", "30"))
	site := strings.TrimRight(env("SITE_URL", "http://localhost"), "/")
	dsn := func(pass, host string) string {
		if pass == "" {
			return ""
		}
		if !strings.Contains(host, ":") {
			host += ":3306"
		}
		return fmt.Sprintf("ragnarok:%s@tcp(%s)/ragnarok?timeout=5s", pass, host)
	}
	return Config{
		Listen:        env("LISTEN", ":8000"),
		SiteURL:       site,
		DBPath:        env("PORTAL_DB", "/data/portal.db"),
		GameDSN:       map[string]string{"re": dsn(os.Getenv("RE_DB_PASS"), env("RE_DB_HOST", "re-db")), "pre": dsn(os.Getenv("PRERE_DB_PASS"), env("PRERE_DB_HOST", "prere-db"))},
		GameMD5:       env("GAME_MD5", "1") == "1",
		AdminEmail:    os.Getenv("ADMIN_EMAIL"),
		DigestHourUTC: hour,
		SessionTTL:    time.Duration(days) * 24 * time.Hour,
		CookieSecure:  strings.HasPrefix(site, "https://"),
		TermsVersion:  env("TERMS_VERSION", "2026-10"),
		Secret:        env("PORTAL_SECRET", ""),
	}
}

type App struct {
	cfg     Config
	store   *Store
	game    *Game
	mail    *Mailer
	pages   map[string]*template.Template
	mailTpl *template.Template
	limiter *limiter
}

func main() {
	log.SetFlags(log.LstdFlags | log.Lmsgprefix)
	log.SetPrefix("portal: ")
	cfg := loadConfig()
	store, err := openStore(cfg.DBPath)
	if err != nil {
		log.Fatal(err)
	}
	if cfg.Secret == "" { // CSRF key survives restarts without needing configuration
		if cfg.Secret = store.Meta("secret"); cfg.Secret == "" {
			cfg.Secret = randomToken()
			store.SetMeta("secret", cfg.Secret)
		}
	}
	app := &App{cfg: cfg, store: store, game: openGame(cfg.GameDSN),
		mail: &Mailer{Host: os.Getenv("SMTP_HOST"), Port: env("SMTP_PORT", "587"), User: os.Getenv("SMTP_USER"),
			Pass: os.Getenv("SMTP_PASS"), From: os.Getenv("MAIL_FROM"), store: store},
		limiter: &limiter{hits: map[string][]time.Time{}}}
	app.loadTemplates()

	cmd := "serve"
	if len(os.Args) > 1 {
		cmd = os.Args[1]
	}
	switch cmd {
	case "serve":
		go app.digestLoop()
		logf("listening on %s (site %s, SMTP %v)", cfg.Listen, cfg.SiteURL, app.mail.Enabled())
		srv := &http.Server{Addr: cfg.Listen, Handler: app.routes(), ReadHeaderTimeout: 10 * time.Second}
		log.Fatal(srv.ListenAndServe())
	case "import":
		app.importAccounts()
	case "md5":
		if err := app.game.ConvertToMD5(); err != nil {
			log.Fatal(err)
		}
	case "admin":
		if len(os.Args) < 3 {
			log.Fatal("usage: portal admin <username>")
		}
		u, err := store.UserByName(os.Args[2])
		if err != nil {
			log.Fatalf("no website user %q", os.Args[2])
		}
		store.SetFlag(u.ID, "is_admin", true)
		fmt.Printf("%s is now an admin\n", u.Username)
	case "link":
		if len(os.Args) < 3 {
			log.Fatal("usage: portal link <username>")
		}
		u, err := store.UserByName(os.Args[2])
		if err != nil {
			log.Fatalf("no website user %q", os.Args[2])
		}
		tok, _ := store.NewToken(u.ID, "set", 7*24*time.Hour)
		fmt.Printf("%s/set-password?t=%s\n", cfg.SiteURL, tok)
	default:
		log.Fatalf("unknown command %q", cmd)
	}
}

// importAccounts copies existing game accounts into the website users (one time, before "portal md5").
func (a *App) importAccounts() {
	accs, err := a.game.Accounts()
	if err != nil {
		log.Fatal(err)
	}
	added := 0
	for _, acc := range accs {
		if _, err := a.store.UserByName(acc.Username); err == nil {
			continue
		}
		u := &User{Username: acc.Username, IsAdmin: acc.GroupID >= 99}
		if acc.Email != "a@a.com" && strings.Contains(acc.Email, "@") {
			u.Email = acc.Email
		}
		if !isMD5(acc.Password) { // plain text: becomes their website password too
			u.PwHash = hashPassword(acc.Password)
		}
		if _, err := a.store.CreateUser(u); err != nil {
			logf("import %s: %v", acc.Username, err)
			continue
		}
		added++
		fmt.Printf("imported %-24s admin=%v email=%q password=%v\n", u.Username, u.IsAdmin, u.Email, u.PwHash != "")
	}
	fmt.Printf("%d accounts imported\n", added)
}

func isMD5(s string) bool {
	if len(s) != 32 {
		return false
	}
	for _, c := range s {
		if !strings.ContainsRune("0123456789abcdef", c) {
			return false
		}
	}
	return true
}

// ---------- templates ----------

func (a *App) loadTemplates() {
	funcs := template.FuncMap{
		"date": func(t time.Time) string { return t.UTC().Format("2006-01-02 15:04 UTC") },
		"dict": func(kv ...any) map[string]any { // {{template "button" (dict "Link" .Link "Label" "...")}}
			m := map[string]any{}
			for i := 0; i+1 < len(kv); i += 2 {
				m[fmt.Sprint(kv[i])] = kv[i+1]
			}
			return m
		},
	}
	a.pages = map[string]*template.Template{}
	entries, _ := fs.Glob(assets, "templates/*.html")
	for _, e := range entries {
		name := strings.TrimSuffix(strings.TrimPrefix(e, "templates/"), ".html")
		if name == "layout" {
			continue
		}
		a.pages[name] = template.Must(template.New("layout.html").Funcs(funcs).ParseFS(assets, "templates/layout.html", e))
	}
	a.mailTpl = template.Must(template.New("mail").Funcs(funcs).ParseFS(assets, "templates/mail/*.html"))
}

// ---------- small helpers ----------

// limiter: at most n hits per key per window (per IP for the public forms).
type limiter struct {
	mu   sync.Mutex
	hits map[string][]time.Time
}

func (l *limiter) Allow(key string, n int, window time.Duration) bool {
	l.mu.Lock()
	defer l.mu.Unlock()
	cut := time.Now().Add(-window)
	keep := l.hits[key][:0]
	for _, t := range l.hits[key] {
		if t.After(cut) {
			keep = append(keep, t)
		}
	}
	if len(keep) >= n {
		l.hits[key] = keep
		return false
	}
	l.hits[key] = append(keep, time.Now())
	return true
}

// clientIP: Caddy puts the visitor's address in X-Forwarded-For.
func clientIP(r *http.Request) string {
	if xf := r.Header.Get("X-Forwarded-For"); xf != "" {
		return strings.TrimSpace(strings.Split(xf, ",")[0])
	}
	host, _, _ := net.SplitHostPort(r.RemoteAddr)
	return host
}

// csrf: a token bound to the session (forms that change something carry it).
func (a *App) csrf(session string) string {
	m := hmac.New(sha256New, []byte(a.cfg.Secret))
	m.Write([]byte("csrf:" + session))
	return fmt.Sprintf("%x", m.Sum(nil))[:32]
}
