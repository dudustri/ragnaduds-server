package main

// The two rAthena databases (Renewal + Pre-Renewal): every player has the same account on both.
// Game passwords are stored as MD5 (login_conf use_MD5_passwords: yes), see "portal md5".

import (
	"database/sql"
	"fmt"
	"strings"

	_ "github.com/go-sql-driver/mysql"
)

type GameDB struct {
	Name string // "re" / "pre"
	db   *sql.DB
}

type Game struct{ dbs []*GameDB }

// openGame connects to every configured server ("name=dsn" pairs). A missing server is skipped with a warning.
func openGame(dsns map[string]string) *Game {
	g := &Game{}
	for _, name := range []string{"re", "pre"} {
		dsn := dsns[name]
		if dsn == "" {
			continue
		}
		db, err := sql.Open("mysql", dsn)
		if err != nil {
			logf("game db %s: %v", name, err)
			continue
		}
		db.SetMaxOpenConns(3)
		g.dbs = append(g.dbs, &GameDB{name, db})
	}
	return g
}

// Taken: the username exists on any server (accounts are case-insensitive in rAthena's default collation).
func (g *Game) Taken(username string) (bool, error) {
	for _, d := range g.dbs {
		var n int
		if err := d.db.QueryRow("SELECT COUNT(*) FROM login WHERE userid = ?", username).Scan(&n); err != nil {
			return false, fmt.Errorf("%s: %w", d.Name, err)
		}
		if n > 0 {
			return true, nil
		}
	}
	return false, nil
}

// CreateAccount adds the game account on every server, with an unusable random password until the
// player sets theirs through the link in the welcome e-mail. Existing accounts are left alone.
func (g *Game) CreateAccount(username, email string) error {
	for _, d := range g.dbs {
		_, err := d.db.Exec(`INSERT INTO login (userid, user_pass, sex, email, group_id)
			SELECT ?, MD5(?), 'M', ?, 0 FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM login WHERE userid = ?)`,
			username, randomToken(), gameEmail(email), username)
		if err != nil {
			return fmt.Errorf("%s: %w", d.Name, err)
		}
	}
	return nil
}

// SetPassword changes the game password on every server (never touches the server-to-server accounts).
func (g *Game) SetPassword(username, pw string, md5 bool) error {
	q := "UPDATE login SET user_pass = MD5(?) WHERE userid = ? AND sex <> 'S'"
	if !md5 {
		q = "UPDATE login SET user_pass = ? WHERE userid = ? AND sex <> 'S'"
	}
	for _, d := range g.dbs {
		if _, err := d.db.Exec(q, pw, username); err != nil {
			return fmt.Errorf("%s: %w", d.Name, err)
		}
	}
	return nil
}

// SetEmail changes the account e-mail on every server (the game asks for it to delete a character).
func (g *Game) SetEmail(username, email string) error {
	for _, d := range g.dbs {
		if _, err := d.db.Exec("UPDATE login SET email = ? WHERE userid = ? AND sex <> 'S'", gameEmail(email), username); err != nil {
			return fmt.Errorf("%s: %w", d.Name, err)
		}
	}
	return nil
}

// rAthena's e-mail column is 39 characters; the client asks for it when deleting a character.
func gameEmail(e string) string {
	if len(e) > 39 || e == "" {
		return "a@a.com"
	}
	return e
}

type GameAccount struct {
	Username, Password, Email string
	GroupID                   int
}

// Accounts lists the players (not the server-to-server logins), merged over both servers.
func (g *Game) Accounts() ([]GameAccount, error) {
	seen := map[string]bool{}
	var out []GameAccount
	for _, d := range g.dbs {
		rows, err := d.db.Query("SELECT userid, user_pass, email, group_id FROM login WHERE sex <> 'S' ORDER BY account_id")
		if err != nil {
			return nil, fmt.Errorf("%s: %w", d.Name, err)
		}
		for rows.Next() {
			var a GameAccount
			if err := rows.Scan(&a.Username, &a.Password, &a.Email, &a.GroupID); err != nil {
				rows.Close()
				return nil, err
			}
			if !seen[strings.ToLower(a.Username)] {
				seen[strings.ToLower(a.Username)] = true
				out = append(out, a)
			}
		}
		rows.Close()
	}
	return out, nil
}

// ConvertToMD5 turns every plain-text password (players AND the server-to-server logins) into MD5, once.
func (g *Game) ConvertToMD5() error {
	for _, d := range g.dbs {
		res, err := d.db.Exec("UPDATE login SET user_pass = MD5(user_pass) WHERE user_pass NOT REGEXP '^[0-9a-f]{32}$'")
		if err != nil {
			return fmt.Errorf("%s: %w", d.Name, err)
		}
		n, _ := res.RowsAffected()
		logf("%s: %d passwords converted to MD5", d.Name, n)
	}
	return nil
}
