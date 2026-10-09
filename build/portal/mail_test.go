package main

import (
	"bytes"
	"testing"
)

func TestMailTemplates(t *testing.T) {
	a := &App{}
	a.loadTemplates()
	t.Log(a.mailTpl.DefinedTemplates())
	for _, n := range []string{"received", "approved", "rejected", "reset", "digest"} {
		var b bytes.Buffer
		err := a.mailTpl.ExecuteTemplate(&b, n+".html", map[string]any{"Subject": "s", "Site": "https://x", "Name": "Ana", "Username": "AnaRO", "Link": "https://x/set?t=1", "Count": 2, "Note": "hi"})
		if err != nil {
			t.Errorf("%s: %v", n, err)
		}
	}
}
