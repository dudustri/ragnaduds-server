package main

import (
	"crypto/sha256"
	"hash"
	"io/fs"
	"net/http"
	"net/mail"
	"net/url"
	"regexp"
	"strconv"
	"strings"
	"time"
)

func sha256New() hash.Hash { return sha256.New() }

const sessionCookie = "rd_session"

var (
	reUsername = regexp.MustCompile(`^[A-Za-z0-9_]{4,23}$`)
	reName     = regexp.MustCompile(`^[\p{L}\p{M}' .-]{1,40}$`)
)

func (a *App) routes() http.Handler {
	mux := http.NewServeMux()
	static, _ := fs.Sub(assets, "static")
	mux.Handle("GET /portal-static/", http.StripPrefix("/portal-static/", http.FileServerFS(static)))
	mux.HandleFunc("GET /auth", a.auth)
	mux.HandleFunc("GET /login", a.loginPage)
	mux.HandleFunc("POST /login", a.loginPost)
	mux.HandleFunc("POST /logout", a.logout)
	mux.HandleFunc("GET /logout", a.logout) // the plain link on the site pages (at worst a forged link logs you out)
	mux.HandleFunc("GET /join", a.joinPage)
	mux.HandleFunc("POST /join", a.joinPost)
	mux.HandleFunc("GET /forgot", a.forgotPage)
	mux.HandleFunc("POST /forgot", a.forgotPost)
	mux.HandleFunc("GET /set-password", a.setPage)
	mux.HandleFunc("POST /set-password", a.setPost)
	mux.HandleFunc("GET /account", a.needUser(a.accountPage))
	mux.HandleFunc("POST /account/password", a.needUser(a.accountPassword))
	mux.HandleFunc("GET /admin", a.needAdmin(a.adminPage))
	mux.HandleFunc("POST /admin/request", a.needAdmin(a.adminRequest))
	mux.HandleFunc("POST /admin/user", a.needAdmin(a.adminUser))
	mux.HandleFunc("GET /admin/outbox", a.needAdmin(a.adminOutbox))
	mux.HandleFunc("GET /admin/mail/{id}", a.needAdmin(a.adminMail))
	return headers(mux)
}

func headers(h http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("X-Content-Type-Options", "nosniff")
		w.Header().Set("Referrer-Policy", "same-origin")
		w.Header().Set("X-Frame-Options", "SAMEORIGIN")
		w.Header().Set("Cache-Control", "no-store")
		h.ServeHTTP(w, r)
	})
}

// ---------- sessions ----------

func (a *App) currentUser(r *http.Request) (*User, string) {
	c, err := r.Cookie(sessionCookie)
	if err != nil || c.Value == "" {
		return nil, ""
	}
	u, err := a.store.SessionUser(c.Value)
	if err != nil {
		return nil, ""
	}
	return u, c.Value
}

func (a *App) setSession(w http.ResponseWriter, u *User) error {
	tok, err := a.store.NewSession(u.ID, a.cfg.SessionTTL)
	if err != nil {
		return err
	}
	http.SetCookie(w, &http.Cookie{Name: sessionCookie, Value: tok, Path: "/", HttpOnly: true, Secure: a.cfg.CookieSecure,
		SameSite: http.SameSiteLaxMode, MaxAge: int(a.cfg.SessionTTL.Seconds())})
	return nil
}

func safeNext(n string) string {
	if !strings.HasPrefix(n, "/") || strings.HasPrefix(n, "//") || strings.HasPrefix(n, "/login") {
		return "/"
	}
	return n
}

type userHandler func(http.ResponseWriter, *http.Request, *User, string)

func (a *App) needUser(h userHandler) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		u, sess := a.currentUser(r)
		if u == nil {
			http.Redirect(w, r, "/login?next="+r.URL.Path, http.StatusSeeOther)
			return
		}
		if r.Method == http.MethodPost && r.FormValue("csrf") != a.csrf(sess) {
			http.Error(w, "Expired form, go back and try again.", http.StatusForbidden)
			return
		}
		h(w, r, u, sess)
	}
}

func (a *App) needAdmin(h userHandler) http.HandlerFunc {
	return a.needUser(func(w http.ResponseWriter, r *http.Request, u *User, sess string) {
		if !u.IsAdmin {
			http.Error(w, "Admins only.", http.StatusForbidden)
			return
		}
		h(w, r, u, sess)
	})
}

// auth answers Caddy's forward_auth: 200 when logged in, otherwise a redirect to the login page.
func (a *App) auth(w http.ResponseWriter, r *http.Request) {
	if u, _ := a.currentUser(r); u != nil {
		w.Header().Set("X-Portal-User", u.Username)
		w.WriteHeader(http.StatusOK)
		return
	}
	http.Redirect(w, r, "/login?next="+safeNext(r.Header.Get("X-Forwarded-Uri")), http.StatusFound)
}

// ---------- rendering ----------

func (a *App) render(w http.ResponseWriter, r *http.Request, name string, data map[string]any) {
	if data == nil {
		data = map[string]any{}
	}
	u, sess := a.currentUser(r)
	data["Me"] = u
	data["CSRF"] = a.csrf(sess)
	data["Page"] = name // the header leaves out (or highlights) the link to the page you are on
	if _, ok := data["Msg"]; !ok {
		data["Msg"] = r.URL.Query().Get("msg")
	}
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	if err := a.pages[name].ExecuteTemplate(w, "layout.html", data); err != nil {
		logf("render %s: %v", name, err)
	}
}

func (a *App) slowDown(w http.ResponseWriter, r *http.Request, what string, n int, window time.Duration) bool {
	if a.limiter.Allow(what+":"+clientIP(r), n, window) {
		return false
	}
	http.Error(w, "Too many attempts. Wait a while and try again.", http.StatusTooManyRequests)
	return true
}

// ---------- login ----------

func (a *App) loginPage(w http.ResponseWriter, r *http.Request) {
	a.render(w, r, "login", map[string]any{"Next": safeNext(r.URL.Query().Get("next"))})
}

func (a *App) loginPost(w http.ResponseWriter, r *http.Request) {
	if a.slowDown(w, r, "login", 10, 10*time.Minute) {
		return
	}
	next := safeNext(r.FormValue("next"))
	u, err := a.store.UserByName(strings.TrimSpace(r.FormValue("username")))
	if err != nil || u.Disabled || u.PwHash == "" || !checkPassword(u.PwHash, r.FormValue("password")) {
		msg := "Wrong username or password."
		if err == nil && u.PwHash == "" && !u.Disabled {
			msg = "This account has no website password yet: use \"Forgot password\" (or the link in your welcome e-mail)."
		}
		a.render(w, r, "login", map[string]any{"Next": next, "Error": msg, "Username": r.FormValue("username")})
		return
	}
	if err := a.setSession(w, u); err != nil {
		http.Error(w, "Could not log in, try again.", http.StatusInternalServerError)
		return
	}
	a.store.Audit(u.Username, "login", clientIP(r))
	http.Redirect(w, r, next, http.StatusSeeOther)
}

func (a *App) logout(w http.ResponseWriter, r *http.Request) {
	if c, err := r.Cookie(sessionCookie); err == nil {
		a.store.DeleteSession(c.Value)
	}
	http.SetCookie(w, &http.Cookie{Name: sessionCookie, Value: "", Path: "/", MaxAge: -1, HttpOnly: true, Secure: a.cfg.CookieSecure})
	// and the browser drops every page it kept of this site, so nothing private shows again after logging out
	w.Header().Set("Clear-Site-Data", `"cache"`)
	http.Redirect(w, r, "/login?msg=You+are+logged+out.", http.StatusSeeOther)
}

// ---------- join (account request) ----------

func (a *App) joinPage(w http.ResponseWriter, r *http.Request) {
	a.render(w, r, "join", map[string]any{"Terms": a.cfg.TermsVersion})
}

func (a *App) joinPost(w http.ResponseWriter, r *http.Request) {
	if r.FormValue("website") != "" { // honeypot: bots fill every field
		a.render(w, r, "join_done", nil)
		return
	}
	if a.slowDown(w, r, "join", 5, time.Hour) {
		return
	}
	req := &Request{
		Username:     strings.TrimSpace(r.FormValue("username")),
		FirstName:    strings.TrimSpace(r.FormValue("first_name")),
		LastName:     strings.TrimSpace(r.FormValue("last_name")),
		Email:        strings.TrimSpace(r.FormValue("email")),
		Message:      strings.TrimSpace(r.FormValue("message")),
		TermsVersion: a.cfg.TermsVersion,
	}
	var errs []string
	if r.FormValue("agree_terms") != "yes" || r.FormValue("agree_gravity") != "yes" {
		errs = append(errs, "You must accept both statements.")
	}
	if !reUsername.MatchString(req.Username) {
		errs = append(errs, "Username: 4 to 23 letters, numbers or _ .")
	} else if a.usernameTaken(req.Username) {
		errs = append(errs, "That username is already taken or requested. Pick another one.")
	}
	if !reName.MatchString(req.FirstName) || !reName.MatchString(req.LastName) {
		errs = append(errs, "Please write your name and surname.")
	}
	if addr, err := mail.ParseAddress(req.Email); err != nil || addr.Address != req.Email || len(req.Email) > 120 {
		errs = append(errs, "Please write a valid e-mail address.")
	}
	if len([]rune(req.Message)) > 1000 {
		errs = append(errs, "The message can have at most 1000 characters.")
	}
	if len(errs) > 0 {
		a.render(w, r, "join", map[string]any{"Terms": a.cfg.TermsVersion, "Errors": errs, "Req": req, "Agreed": true})
		return
	}
	if err := a.store.AddRequest(req, sha(a.cfg.Secret+clientIP(r))); err != nil {
		logf("add request: %v", err)
		http.Error(w, "Could not save your request, try again later.", http.StatusInternalServerError)
		return
	}
	a.store.Audit(req.Username, "request", req.Email)
	a.Send(req.Email, "RagnaDuds: we got your request", "received", map[string]any{"Name": req.FirstName, "Username": req.Username})
	a.render(w, r, "join_done", map[string]any{"Name": req.FirstName})
}

func (a *App) usernameTaken(name string) bool {
	if _, err := a.store.UserByName(name); err == nil {
		return true
	}
	if a.store.PendingUsername(name) {
		return true
	}
	taken, err := a.game.Taken(name)
	if err != nil {
		logf("username check: %v", err)
		return true // can't check: be safe
	}
	return taken
}

// ---------- forgot / set password ----------

func (a *App) forgotPage(w http.ResponseWriter, r *http.Request) { a.render(w, r, "forgot", nil) }

func (a *App) forgotPost(w http.ResponseWriter, r *http.Request) {
	if a.slowDown(w, r, "forgot", 5, time.Hour) {
		return
	}
	email := strings.TrimSpace(r.FormValue("email"))
	users, _ := a.store.UsersByEmail(email)
	for _, u := range users {
		tok, err := a.store.NewToken(u.ID, "reset", 2*time.Hour)
		if err != nil {
			continue
		}
		a.Send(u.Email, "RagnaDuds: your username and a new password", "reset",
			map[string]any{"Username": u.Username, "Link": a.cfg.SiteURL + "/set-password?t=" + tok})
		a.store.Audit(u.Username, "reset-link", clientIP(r))
	}
	a.render(w, r, "message", map[string]any{"Title": "CHECK YOUR E-MAIL",
		"Text": "If that e-mail belongs to an account, we sent your username and a link to choose a new password. The link works for 2 hours."})
}

func (a *App) setPage(w http.ResponseWriter, r *http.Request) {
	t := r.URL.Query().Get("t")
	u, purpose, err := a.store.TokenUser(t)
	if err != nil {
		a.render(w, r, "message", map[string]any{"Title": "LINK EXPIRED",
			"Text": "This link was already used or has expired. Ask for a new one on the \"Forgot password\" page."})
		return
	}
	a.render(w, r, "setpw", map[string]any{"Token": t, "Username": u.Username, "Welcome": purpose == "set"})
}

func validPassword(pw, pw2 string) string {
	if pw != pw2 {
		return "The two passwords are different."
	}
	if n := len(pw); n < 6 || n > 23 {
		return "The password must have 6 to 23 characters (the game's limit)."
	}
	return ""
}

func (a *App) setPost(w http.ResponseWriter, r *http.Request) {
	if a.slowDown(w, r, "set", 20, time.Hour) {
		return
	}
	t := r.FormValue("t")
	u, purpose, err := a.store.TokenUser(t)
	if err != nil {
		a.render(w, r, "message", map[string]any{"Title": "LINK EXPIRED", "Text": "This link was already used or has expired."})
		return
	}
	pw := r.FormValue("password")
	if msg := validPassword(pw, r.FormValue("password2")); msg != "" {
		a.render(w, r, "setpw", map[string]any{"Token": t, "Username": u.Username, "Welcome": purpose == "set", "Error": msg})
		return
	}
	if err := a.changePassword(u, pw); err != nil {
		logf("set password %s: %v", u.Username, err)
		a.render(w, r, "setpw", map[string]any{"Token": t, "Username": u.Username, "Welcome": purpose == "set",
			"Error": "Could not save the password right now, try again in a minute."})
		return
	}
	a.store.UseToken(t)
	a.store.DeleteUserSessions(u.ID)
	a.setSession(w, u)
	http.Redirect(w, r, "/account?msg=Password+saved.+Use+it+in+the+game+and+on+this+website.", http.StatusSeeOther)
}

// changePassword: game accounts (both servers) first, then the website, so they never get out of step.
func (a *App) changePassword(u *User, pw string) error {
	if err := a.game.SetPassword(u.Username, pw, a.cfg.GameMD5); err != nil {
		return err
	}
	if err := a.store.SetPasswordHash(u.ID, hashPassword(pw)); err != nil {
		return err
	}
	a.store.Audit(u.Username, "password", "")
	return nil
}

// ---------- account ----------

func (a *App) accountPage(w http.ResponseWriter, r *http.Request, u *User, _ string) {
	a.render(w, r, "account", nil)
}

func (a *App) accountPassword(w http.ResponseWriter, r *http.Request, u *User, _ string) {
	if a.slowDown(w, r, "change", 10, time.Hour) {
		return
	}
	if !checkPassword(u.PwHash, r.FormValue("current")) {
		a.render(w, r, "account", map[string]any{"Error": "Your current password is wrong."})
		return
	}
	pw := r.FormValue("password")
	if msg := validPassword(pw, r.FormValue("password2")); msg != "" {
		a.render(w, r, "account", map[string]any{"Error": msg})
		return
	}
	if err := a.changePassword(u, pw); err != nil {
		logf("change password %s: %v", u.Username, err)
		a.render(w, r, "account", map[string]any{"Error": "Could not save the password right now, try again in a minute."})
		return
	}
	http.Redirect(w, r, "/account?msg=Password+changed+(game+and+website).", http.StatusSeeOther)
}

// ---------- admin ----------

func (a *App) adminPage(w http.ResponseWriter, r *http.Request, u *User, _ string) {
	pending, _ := a.store.Requests("pending", 200)
	approved, _ := a.store.Requests("approved", 15)
	rejected, _ := a.store.Requests("rejected", 15)
	users, _ := a.store.AllUsers()
	a.render(w, r, "admin", map[string]any{"Pending": pending, "Approved": approved, "Rejected": rejected,
		"Users": users, "SMTP": a.mail.Enabled(), "Link": r.URL.Query().Get("link")})
}

func (a *App) adminRequest(w http.ResponseWriter, r *http.Request, me *User, _ string) {
	id, _ := strconv.ParseInt(r.FormValue("id"), 10, 64)
	req, err := a.store.RequestByID(id)
	if err != nil || req.Status != "pending" {
		http.Redirect(w, r, "/admin?msg=That+request+was+already+handled.", http.StatusSeeOther)
		return
	}
	note := strings.TrimSpace(r.FormValue("note"))
	switch r.FormValue("action") {
	case "approve":
		if _, err := a.store.UserByName(req.Username); err == nil {
			http.Redirect(w, r, "/admin?msg=Username+already+exists:+reject+this+one.", http.StatusSeeOther)
			return
		}
		if err := a.game.CreateAccount(req.Username, req.Email); err != nil {
			logf("create game account %s: %v", req.Username, err)
			http.Redirect(w, r, "/admin?msg=Could+not+create+the+game+account:+"+err.Error(), http.StatusSeeOther)
			return
		}
		uid, err := a.store.CreateUser(&User{Username: req.Username, Email: req.Email, FirstName: req.FirstName, LastName: req.LastName})
		if err != nil {
			http.Redirect(w, r, "/admin?msg=Could+not+create+the+website+user:+"+err.Error(), http.StatusSeeOther)
			return
		}
		a.store.DecideRequest(id, "approved", me.Username, note)
		tok, _ := a.store.NewToken(uid, "set", 7*24*time.Hour)
		link := a.cfg.SiteURL + "/set-password?t=" + tok
		a.Send(req.Email, "Welcome to RagnaDuds!", "approved", map[string]any{"Name": req.FirstName, "Username": req.Username, "Link": link, "Note": note})
		a.store.Audit(me.Username, "approve", req.Username)
		http.Redirect(w, r, "/admin?msg=Approved+"+req.Username+".&link="+link, http.StatusSeeOther)
	case "reject":
		a.store.DecideRequest(id, "rejected", me.Username, note)
		if r.FormValue("notify") == "yes" {
			a.Send(req.Email, "RagnaDuds: about your request", "rejected", map[string]any{"Name": req.FirstName, "Note": note})
		}
		a.store.Audit(me.Username, "reject", req.Username)
		http.Redirect(w, r, "/admin?msg=Rejected+"+req.Username+".", http.StatusSeeOther)
	default:
		http.Error(w, "bad action", http.StatusBadRequest)
	}
}

func (a *App) adminUser(w http.ResponseWriter, r *http.Request, me *User, _ string) {
	id, _ := strconv.ParseInt(r.FormValue("id"), 10, 64)
	u, err := a.store.UserByID(id)
	if err != nil {
		http.Redirect(w, r, "/admin?msg=No+such+user.", http.StatusSeeOther)
		return
	}
	switch r.FormValue("action") {
	case "link":
		tok, _ := a.store.NewToken(u.ID, "set", 7*24*time.Hour)
		link := a.cfg.SiteURL + "/set-password?t=" + tok
		if u.Email != "" {
			a.Send(u.Email, "RagnaDuds: choose your password", "reset", map[string]any{"Username": u.Username, "Link": link})
		}
		a.store.Audit(me.Username, "link", u.Username)
		http.Redirect(w, r, "/admin?msg=New+link+for+"+u.Username+".&link="+link, http.StatusSeeOther)
		return
	case "email":
		email := strings.TrimSpace(r.FormValue("email"))
		if email != "" {
			if addr, err := mail.ParseAddress(email); err != nil || addr.Address != email || len(email) > 120 {
				http.Redirect(w, r, "/admin?msg="+url.QueryEscape("Not a valid e-mail: "+email), http.StatusSeeOther)
				return
			}
		}
		if err := a.game.SetEmail(u.Username, email); err != nil {
			logf("admin email %s: %v", u.Username, err)
			http.Redirect(w, r, "/admin?msg=Game+database+error,+nothing+changed.", http.StatusSeeOther)
			return
		}
		a.store.SetEmail(u.ID, email)
		a.store.Audit(me.Username, "email", u.Username+": "+u.Email+" -> "+email)
		if !strings.EqualFold(email, u.Email) {
			if email != "" { // welcome the new address
				a.Send(email, "RagnaDuds: your e-mail is linked to "+u.Username, "linked", map[string]any{"Username": u.Username})
			}
			if u.Email != "" { // and tell the old one, in case the change wasn't wanted
				a.Send(u.Email, "RagnaDuds: the e-mail of "+u.Username+" was changed", "email_changed",
					map[string]any{"Username": u.Username, "NewMasked": maskEmail(email)})
			}
		}
		http.Redirect(w, r, "/admin?msg="+url.QueryEscape("E-mail of "+u.Username+" is now "+email+"."), http.StatusSeeOther)
		return
	case "disable", "enable":
		if u.ID == me.ID {
			http.Redirect(w, r, "/admin?msg=You+can't+disable+yourself.", http.StatusSeeOther)
			return
		}
		a.store.SetFlag(u.ID, "disabled", r.FormValue("action") == "disable")
		a.store.DeleteUserSessions(u.ID)
	case "admin", "unadmin":
		if u.ID == me.ID {
			http.Redirect(w, r, "/admin?msg=You+can't+change+your+own+admin+flag.", http.StatusSeeOther)
			return
		}
		a.store.SetFlag(u.ID, "is_admin", r.FormValue("action") == "admin")
	default:
		http.Error(w, "bad action", http.StatusBadRequest)
		return
	}
	a.store.Audit(me.Username, r.FormValue("action"), u.Username)
	http.Redirect(w, r, "/admin?msg=Done:+"+r.FormValue("action")+"+"+u.Username+".", http.StatusSeeOther)
}

func (a *App) adminOutbox(w http.ResponseWriter, r *http.Request, _ *User, _ string) {
	mails, _ := a.store.Outbox(100)
	a.render(w, r, "outbox", map[string]any{"Mails": mails, "SMTP": a.mail.Enabled()})
}

func (a *App) adminMail(w http.ResponseWriter, r *http.Request, _ *User, _ string) {
	id, _ := strconv.ParseInt(r.PathValue("id"), 10, 64)
	mails, _ := a.store.Outbox(1000)
	for _, m := range mails {
		if m.ID == id {
			w.Header().Set("Content-Type", "text/html; charset=utf-8")
			w.Header().Set("Content-Security-Policy", "sandbox") // our own HTML, shown as-is but inert
			w.Write([]byte(m.HTML))
			return
		}
	}
	http.NotFound(w, r)
}

// maskEmail: "player1@gmail.com" -> "p*****1@gmail.com" (shown to the old address, which may not be the player's anymore)
func maskEmail(e string) string {
	if e == "" {
		return "(no e-mail)"
	}
	at := strings.LastIndex(e, "@")
	if at <= 0 {
		return "***"
	}
	local := e[:at]
	if len(local) <= 2 {
		return strings.Repeat("*", len(local)) + e[at:]
	}
	return local[:1] + strings.Repeat("*", len(local)-2) + local[len(local)-1:] + e[at:]
}
