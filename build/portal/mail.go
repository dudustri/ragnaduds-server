package main

// E-mail through any SMTP provider (Gmail with an app password, Brevo, ...). Every mail is kept in the outbox; with no SMTP
// configured it is only kept there (the admin page shows it, links included), so nothing is lost.

import (
	"bytes"
	"crypto/tls"
	"fmt"
	"mime"
	"net"
	"net/smtp"
	"strings"
	"time"
)

type Mailer struct {
	Host, Port, User, Pass, From string
	store                        *Store
}

func (m *Mailer) Enabled() bool { return m.Host != "" && m.From != "" }

// Send renders template "mail/<name>.html" into the shared mail layout and sends (or queues) it.
func (a *App) Send(to, subject, name string, data map[string]any) {
	if data == nil {
		data = map[string]any{}
	}
	data["Subject"], data["Site"] = subject, a.cfg.SiteURL
	var body bytes.Buffer
	if err := a.mailTpl.ExecuteTemplate(&body, name+".html", data); err != nil {
		logf("mail template %s: %v", name, err)
		return
	}
	id, err := a.store.QueueMail(to, subject, body.String())
	if err != nil {
		logf("outbox: %v", err)
		return
	}
	if !a.mail.Enabled() {
		logf("mail to %s (%s) kept in the outbox: SMTP not configured", to, subject)
		return
	}
	go func() {
		err := a.mail.deliver(to, subject, body.String())
		if err != nil {
			logf("mail to %s: %v", to, err)
			a.store.MarkMail(id, false, err.Error())
			return
		}
		a.store.MarkMail(id, true, "")
	}()
}

func (m *Mailer) deliver(to, subject, html string) error {
	addr := net.JoinHostPort(m.Host, m.Port)
	msg := "From: " + m.From + "\r\nTo: " + to + "\r\nSubject: " + mime.QEncoding.Encode("utf-8", subject) +
		"\r\nMIME-Version: 1.0\r\nContent-Type: text/html; charset=utf-8\r\nDate: " + time.Now().Format(time.RFC1123Z) + "\r\n\r\n" + html
	fromAddr := m.From
	if i := strings.LastIndex(fromAddr, "<"); i >= 0 {
		fromAddr = strings.Trim(fromAddr[i:], "<> ")
	}
	var auth smtp.Auth
	if m.User != "" {
		auth = smtp.PlainAuth("", m.User, m.Pass, m.Host)
	}
	if m.Port == "465" { // implicit TLS
		conn, err := tls.Dial("tcp", addr, &tls.Config{ServerName: m.Host})
		if err != nil {
			return err
		}
		c, err := smtp.NewClient(conn, m.Host)
		if err != nil {
			return err
		}
		defer c.Close()
		if auth != nil {
			if err := c.Auth(auth); err != nil {
				return err
			}
		}
		if err := c.Mail(fromAddr); err != nil {
			return err
		}
		if err := c.Rcpt(to); err != nil {
			return err
		}
		w, err := c.Data()
		if err != nil {
			return err
		}
		if _, err := w.Write([]byte(msg)); err != nil {
			return err
		}
		if err := w.Close(); err != nil {
			return err
		}
		return c.Quit()
	}
	return smtp.SendMail(addr, auth, fromAddr, []string{to}, []byte(msg)) // 587: STARTTLS
}

// digestLoop mails the admin once a day (at DigestHourUTC) when requests are waiting, and does housekeeping.
func (a *App) digestLoop() {
	for {
		time.Sleep(10 * time.Minute)
		a.store.Cleanup()
		a.store.PurgeRejected(30 * 24 * time.Hour)
		t := time.Now().UTC()
		day := t.Format("2006-01-02")
		if t.Hour() < a.cfg.DigestHourUTC || a.store.Meta("digest_day") == day {
			continue
		}
		a.store.SetMeta("digest_day", day)
		n := a.store.CountPending()
		if n == 0 || a.cfg.AdminEmail == "" {
			continue
		}
		a.Send(a.cfg.AdminEmail, fmt.Sprintf("RagnaDuds: %d account request(s) waiting", n), "digest",
			map[string]any{"Count": n, "Link": a.cfg.SiteURL + "/admin"})
	}
}
