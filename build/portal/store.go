package main

// SQLite: account requests, website users, sessions, one-time links, the e-mail outbox and an audit log.

import (
	"crypto/rand"
	"crypto/sha256"
	"crypto/subtle"
	"database/sql"
	"encoding/base64"
	"encoding/hex"
	"errors"
	"fmt"
	"strings"
	"time"

	"golang.org/x/crypto/argon2"
	_ "modernc.org/sqlite"
)

const schema = `
CREATE TABLE IF NOT EXISTS users (
	id INTEGER PRIMARY KEY,
	username TEXT NOT NULL UNIQUE COLLATE NOCASE,
	email TEXT NOT NULL DEFAULT '',
	first_name TEXT NOT NULL DEFAULT '',
	last_name TEXT NOT NULL DEFAULT '',
	pw_hash TEXT NOT NULL DEFAULT '',
	is_admin INTEGER NOT NULL DEFAULT 0,
	disabled INTEGER NOT NULL DEFAULT 0,
	created_at INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS users_email ON users(email COLLATE NOCASE);
CREATE TABLE IF NOT EXISTS requests (
	id INTEGER PRIMARY KEY,
	created_at INTEGER NOT NULL,
	username TEXT NOT NULL,
	first_name TEXT NOT NULL,
	last_name TEXT NOT NULL,
	email TEXT NOT NULL,
	message TEXT NOT NULL DEFAULT '',
	terms_version TEXT NOT NULL,
	agreed_terms_at INTEGER NOT NULL,
	agreed_gravity_at INTEGER NOT NULL,
	ip_hash TEXT NOT NULL DEFAULT '',
	status TEXT NOT NULL DEFAULT 'pending',
	decided_at INTEGER NOT NULL DEFAULT 0,
	decided_by TEXT NOT NULL DEFAULT '',
	note TEXT NOT NULL DEFAULT ''
);
CREATE TABLE IF NOT EXISTS sessions (
	token_hash TEXT PRIMARY KEY,
	user_id INTEGER NOT NULL,
	expires_at INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS tokens (
	token_hash TEXT PRIMARY KEY,
	user_id INTEGER NOT NULL,
	purpose TEXT NOT NULL,
	expires_at INTEGER NOT NULL,
	used INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS outbox (
	id INTEGER PRIMARY KEY,
	created_at INTEGER NOT NULL,
	to_addr TEXT NOT NULL,
	subject TEXT NOT NULL,
	html TEXT NOT NULL,
	sent INTEGER NOT NULL DEFAULT 0,
	error TEXT NOT NULL DEFAULT ''
);
CREATE TABLE IF NOT EXISTS audit (
	id INTEGER PRIMARY KEY,
	ts INTEGER NOT NULL,
	actor TEXT NOT NULL,
	action TEXT NOT NULL,
	detail TEXT NOT NULL DEFAULT ''
);
CREATE TABLE IF NOT EXISTS meta (k TEXT PRIMARY KEY, v TEXT NOT NULL);
`

type Store struct{ db *sql.DB }

type User struct {
	ID                  int64
	Username, Email     string
	FirstName, LastName string
	PwHash              string
	IsAdmin, Disabled   bool
	CreatedAt           time.Time
}

type Request struct {
	ID                                   int64
	CreatedAt                            time.Time
	Username, FirstName, LastName, Email string
	Message, TermsVersion, Status, Note  string
	DecidedBy                            string
	DecidedAt                            time.Time
}

type Mail struct {
	ID        int64
	CreatedAt time.Time
	To        string
	Subject   string
	HTML      string
	Sent      bool
	Error     string
}

func openStore(path string) (*Store, error) {
	db, err := sql.Open("sqlite", "file:"+path+"?_pragma=busy_timeout(5000)&_pragma=journal_mode(WAL)&_pragma=foreign_keys(1)")
	if err != nil {
		return nil, err
	}
	db.SetMaxOpenConns(1) // SQLite: one writer, keep it simple
	if _, err := db.Exec(schema); err != nil {
		return nil, fmt.Errorf("schema: %w", err)
	}
	return &Store{db}, nil
}

func now() int64 { return time.Now().Unix() }

// ---------- secrets ----------

func randomToken() string {
	b := make([]byte, 32)
	if _, err := rand.Read(b); err != nil {
		panic(err)
	}
	return base64.RawURLEncoding.EncodeToString(b)
}

func sha(s string) string { h := sha256.Sum256([]byte(s)); return hex.EncodeToString(h[:]) }

// argon2id, encoded like the reference implementation: $argon2id$v=19$m=65536,t=2,p=1$salt$hash
func hashPassword(pw string) string {
	salt := make([]byte, 16)
	if _, err := rand.Read(salt); err != nil {
		panic(err)
	}
	h := argon2.IDKey([]byte(pw), salt, 2, 64*1024, 1, 32)
	return fmt.Sprintf("$argon2id$v=19$m=65536,t=2,p=1$%s$%s",
		base64.RawStdEncoding.EncodeToString(salt), base64.RawStdEncoding.EncodeToString(h))
}

func checkPassword(hash, pw string) bool {
	parts := strings.Split(hash, "$")
	if len(parts) != 6 || parts[1] != "argon2id" {
		return false
	}
	var m, t uint32
	var p uint8
	if _, err := fmt.Sscanf(parts[3], "m=%d,t=%d,p=%d", &m, &t, &p); err != nil {
		return false
	}
	salt, err1 := base64.RawStdEncoding.DecodeString(parts[4])
	want, err2 := base64.RawStdEncoding.DecodeString(parts[5])
	if err1 != nil || err2 != nil {
		return false
	}
	got := argon2.IDKey([]byte(pw), salt, t, m, p, uint32(len(want)))
	return subtle.ConstantTimeCompare(got, want) == 1
}

// ---------- users ----------

const userCols = "id, username, email, first_name, last_name, pw_hash, is_admin, disabled, created_at"

func scanUser(sc interface{ Scan(...any) error }) (*User, error) {
	var u User
	var created int64
	if err := sc.Scan(&u.ID, &u.Username, &u.Email, &u.FirstName, &u.LastName, &u.PwHash, &u.IsAdmin, &u.Disabled, &created); err != nil {
		return nil, err
	}
	u.CreatedAt = time.Unix(created, 0)
	return &u, nil
}

func (s *Store) UserByName(name string) (*User, error) {
	return scanUser(s.db.QueryRow("SELECT "+userCols+" FROM users WHERE username = ?", name))
}

func (s *Store) UserByID(id int64) (*User, error) {
	return scanUser(s.db.QueryRow("SELECT "+userCols+" FROM users WHERE id = ?", id))
}

func (s *Store) UsersByEmail(email string) ([]*User, error) {
	return s.users("SELECT "+userCols+" FROM users WHERE email = ? COLLATE NOCASE AND disabled = 0", email)
}

func (s *Store) AllUsers() ([]*User, error) {
	return s.users("SELECT " + userCols + " FROM users ORDER BY username COLLATE NOCASE")
}

func (s *Store) users(q string, args ...any) ([]*User, error) {
	rows, err := s.db.Query(q, args...)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var out []*User
	for rows.Next() {
		u, err := scanUser(rows)
		if err != nil {
			return nil, err
		}
		out = append(out, u)
	}
	return out, rows.Err()
}

// CreateUser adds a website user. pwHash may be empty (no password yet: they get a set-password link).
func (s *Store) CreateUser(u *User) (int64, error) {
	res, err := s.db.Exec("INSERT INTO users (username, email, first_name, last_name, pw_hash, is_admin, created_at) VALUES (?,?,?,?,?,?,?)",
		u.Username, u.Email, u.FirstName, u.LastName, u.PwHash, u.IsAdmin, now())
	if err != nil {
		return 0, err
	}
	return res.LastInsertId()
}

func (s *Store) SetPasswordHash(id int64, hash string) error {
	_, err := s.db.Exec("UPDATE users SET pw_hash = ? WHERE id = ?", hash, id)
	return err
}

func (s *Store) SetEmail(id int64, email string) error {
	_, err := s.db.Exec("UPDATE users SET email = ? WHERE id = ?", email, id)
	return err
}

func (s *Store) SetFlag(id int64, col string, v bool) error {
	if col != "disabled" && col != "is_admin" {
		return errors.New("bad column")
	}
	_, err := s.db.Exec("UPDATE users SET "+col+" = ? WHERE id = ?", v, id)
	return err
}

// ---------- requests ----------

const reqCols = "id, created_at, username, first_name, last_name, email, message, terms_version, status, note, decided_by, decided_at"

func scanRequest(sc interface{ Scan(...any) error }) (*Request, error) {
	var r Request
	var created, decided int64
	if err := sc.Scan(&r.ID, &created, &r.Username, &r.FirstName, &r.LastName, &r.Email, &r.Message, &r.TermsVersion,
		&r.Status, &r.Note, &r.DecidedBy, &decided); err != nil {
		return nil, err
	}
	r.CreatedAt, r.DecidedAt = time.Unix(created, 0), time.Unix(decided, 0)
	return &r, nil
}

func (s *Store) AddRequest(r *Request, ipHash string) error {
	t := now()
	_, err := s.db.Exec(`INSERT INTO requests (created_at, username, first_name, last_name, email, message, terms_version,
		agreed_terms_at, agreed_gravity_at, ip_hash) VALUES (?,?,?,?,?,?,?,?,?,?)`,
		t, r.Username, r.FirstName, r.LastName, r.Email, r.Message, r.TermsVersion, t, t, ipHash)
	return err
}

func (s *Store) Requests(status string, limit int) ([]*Request, error) {
	rows, err := s.db.Query("SELECT "+reqCols+" FROM requests WHERE status = ? ORDER BY id DESC LIMIT ?", status, limit)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var out []*Request
	for rows.Next() {
		r, err := scanRequest(rows)
		if err != nil {
			return nil, err
		}
		out = append(out, r)
	}
	return out, rows.Err()
}

func (s *Store) RequestByID(id int64) (*Request, error) {
	return scanRequest(s.db.QueryRow("SELECT "+reqCols+" FROM requests WHERE id = ?", id))
}

func (s *Store) PendingUsername(name string) bool {
	var n int
	s.db.QueryRow("SELECT COUNT(*) FROM requests WHERE status = 'pending' AND username = ? COLLATE NOCASE", name).Scan(&n)
	return n > 0
}

func (s *Store) CountPending() int {
	var n int
	s.db.QueryRow("SELECT COUNT(*) FROM requests WHERE status = 'pending'").Scan(&n)
	return n
}

func (s *Store) DecideRequest(id int64, status, by, note string) error {
	res, err := s.db.Exec("UPDATE requests SET status = ?, decided_at = ?, decided_by = ?, note = ? WHERE id = ? AND status = 'pending'",
		status, now(), by, note, id)
	if err != nil {
		return err
	}
	if n, _ := res.RowsAffected(); n == 0 {
		return errors.New("request is not pending any more")
	}
	return nil
}

// PurgeRejected deletes rejected requests older than the given age (privacy).
func (s *Store) PurgeRejected(age time.Duration) {
	s.db.Exec("DELETE FROM requests WHERE status = 'rejected' AND decided_at < ?", time.Now().Add(-age).Unix())
}

// ---------- sessions ----------

func (s *Store) NewSession(userID int64, ttl time.Duration) (string, error) {
	tok := randomToken()
	_, err := s.db.Exec("INSERT INTO sessions (token_hash, user_id, expires_at) VALUES (?,?,?)", sha(tok), userID, time.Now().Add(ttl).Unix())
	return tok, err
}

func (s *Store) SessionUser(tok string) (*User, error) {
	var id int64
	if err := s.db.QueryRow("SELECT user_id FROM sessions WHERE token_hash = ? AND expires_at > ?", sha(tok), now()).Scan(&id); err != nil {
		return nil, err
	}
	u, err := s.UserByID(id)
	if err != nil || u.Disabled {
		return nil, errors.New("no user")
	}
	return u, nil
}

func (s *Store) DeleteSession(tok string) {
	s.db.Exec("DELETE FROM sessions WHERE token_hash = ?", sha(tok))
}

func (s *Store) DeleteUserSessions(userID int64) {
	s.db.Exec("DELETE FROM sessions WHERE user_id = ?", userID)
}

// ---------- one-time links (set / reset password) ----------

func (s *Store) NewToken(userID int64, purpose string, ttl time.Duration) (string, error) {
	tok := randomToken()
	s.db.Exec("UPDATE tokens SET used = 1 WHERE user_id = ? AND purpose = ? AND used = 0", userID, purpose) // one live link each
	_, err := s.db.Exec("INSERT INTO tokens (token_hash, user_id, purpose, expires_at) VALUES (?,?,?,?)",
		sha(tok), userID, purpose, time.Now().Add(ttl).Unix())
	return tok, err
}

// TokenUser returns the user a live link belongs to (without using it up).
func (s *Store) TokenUser(tok string) (*User, string, error) {
	var id int64
	var purpose string
	if err := s.db.QueryRow("SELECT user_id, purpose FROM tokens WHERE token_hash = ? AND used = 0 AND expires_at > ?",
		sha(tok), now()).Scan(&id, &purpose); err != nil {
		return nil, "", err
	}
	u, err := s.UserByID(id)
	return u, purpose, err
}

func (s *Store) UseToken(tok string) {
	s.db.Exec("UPDATE tokens SET used = 1 WHERE token_hash = ?", sha(tok))
}

// ---------- outbox + audit ----------

func (s *Store) QueueMail(to, subject, html string) (int64, error) {
	res, err := s.db.Exec("INSERT INTO outbox (created_at, to_addr, subject, html) VALUES (?,?,?,?)", now(), to, subject, html)
	if err != nil {
		return 0, err
	}
	return res.LastInsertId()
}

func (s *Store) MarkMail(id int64, sent bool, errText string) {
	s.db.Exec("UPDATE outbox SET sent = ?, error = ? WHERE id = ?", sent, errText, id)
}

func (s *Store) Outbox(limit int) ([]*Mail, error) {
	rows, err := s.db.Query("SELECT id, created_at, to_addr, subject, html, sent, error FROM outbox ORDER BY id DESC LIMIT ?", limit)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var out []*Mail
	for rows.Next() {
		var m Mail
		var created int64
		if err := rows.Scan(&m.ID, &created, &m.To, &m.Subject, &m.HTML, &m.Sent, &m.Error); err != nil {
			return nil, err
		}
		m.CreatedAt = time.Unix(created, 0)
		out = append(out, &m)
	}
	return out, rows.Err()
}

func (s *Store) Audit(actor, action, detail string) {
	s.db.Exec("INSERT INTO audit (ts, actor, action, detail) VALUES (?,?,?,?)", now(), actor, action, detail)
}

func (s *Store) Meta(k string) string {
	var v string
	s.db.QueryRow("SELECT v FROM meta WHERE k = ?", k).Scan(&v)
	return v
}

func (s *Store) SetMeta(k, v string) {
	s.db.Exec("INSERT INTO meta (k, v) VALUES (?,?) ON CONFLICT(k) DO UPDATE SET v = excluded.v", k, v)
}

// Cleanup removes expired sessions and links.
func (s *Store) Cleanup() {
	t := now()
	s.db.Exec("DELETE FROM sessions WHERE expires_at < ?", t)
	s.db.Exec("DELETE FROM tokens WHERE expires_at < ?", t-7*86400)
}
