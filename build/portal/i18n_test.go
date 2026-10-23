package main

import (
	"bytes"
	"net/http"
	"os"
	"path/filepath"
	"regexp"
	"strings"
	"testing"
)

// Every text exists in every language, and every key the templates or handlers use exists
// (a missing key would show as an empty spot, not an error).
func TestTextsComplete(t *testing.T) {
	for lang, m := range texts {
		for k := range texts["en"] {
			if strings.TrimSpace(string(m[k])) == "" {
				t.Errorf("%s: missing %q", lang, k)
			}
		}
		if len(m) != len(texts["en"]) {
			t.Errorf("%s has %d texts, en has %d", lang, len(m), len(texts["en"]))
		}
	}
	used := map[string]bool{}
	files, _ := filepath.Glob("templates/*.html")
	files = append(files, "handlers.go")
	re := regexp.MustCompile(`\.L\.(\w+)|"((?:e|m|t|x)_\w+)"`)
	for _, f := range files {
		b, _ := os.ReadFile(f)
		for _, m := range re.FindAllStringSubmatch(string(b), -1) {
			used[m[1]+m[2]] = true
		}
	}
	for k := range used {
		if _, ok := texts["en"][k]; !ok {
			t.Errorf("key %q is used but has no text", k)
		}
	}
}

// Each player page renders in each language, with its own words and the html lang set.
func TestPagesRenderInEveryLanguage(t *testing.T) {
	a := &App{}
	a.loadTemplates()
	want := map[string]string{"en": "Password", "pt": "Senha", "da": "Adgangskode"}
	for _, page := range []string{"login", "join", "join_done", "account", "forgot", "setpw", "message"} {
		for lang, word := range want {
			d := map[string]any{"L": texts[lang], "Lang": htmlLang[lang], "LangKey": lang, "Page": page,
				"Me": &User{Username: "AnaRO"}, "Username": "AnaRO", "Terms": "1", "Name": "Ana", "Welcome": true,
				"Title": tr(texts[lang], "t_expired"), "Text": tr(texts[lang], "x_expired")}
			var b bytes.Buffer
			if err := a.pages[page].ExecuteTemplate(&b, "layout.html", d); err != nil {
				t.Fatalf("%s/%s: %v", page, lang, err)
			}
			out := b.String()
			if !strings.Contains(out, `lang="`+htmlLang[lang]+`"`) || !strings.Contains(out, `data-lang="`+lang+`" aria-pressed="true"`) {
				t.Errorf("%s/%s: html lang or pressed button missing", page, lang)
			}
			if page == "login" && !strings.Contains(out, word) {
				t.Errorf("login/%s: %q not on the page", lang, word)
			}
		}
	}
}

func TestLangOf(t *testing.T) {
	for _, c := range []struct{ cookie, accept, want string }{
		{"pt", "da-DK", "pt"}, {"", "da-DK,da;q=0.9", "da"}, {"", "pt-BR", "pt"}, {"xx", "fr", "en"}, {"", "", "en"},
	} {
		r, _ := http.NewRequest("GET", "/", nil)
		if c.cookie != "" {
			r.AddCookie(&http.Cookie{Name: "lang", Value: c.cookie})
		}
		r.Header.Set("Accept-Language", c.accept)
		if got := langOf(r); got != c.want {
			t.Errorf("cookie %q accept %q: got %s, want %s", c.cookie, c.accept, got, c.want)
		}
	}
}

// %s values are escaped, so a username can't inject HTML.
func TestTfEscapes(t *testing.T) {
	if got := string(tf(texts["en"]["set_for"], "<b>x")); !strings.Contains(got, "&lt;b&gt;x") {
		t.Errorf("not escaped: %s", got)
	}
}
