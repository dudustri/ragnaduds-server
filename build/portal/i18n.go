package main

import (
	"fmt"
	"html/template"
	"net/http"
	"strings"
)

// Page texts in the site's three languages. The language is the same choice as on the site: the "lang" cookie
// (set by the language buttons on every page), else the browser language, else English.
// Values are our own constants, so they may hold <b> tags; %s in a text is filled (escaped) by the "tf" func.
// The admin pages and the e-mails stay in English.
var texts = map[string]map[string]template.HTML{
	"en": {
		"nav_site": "SITE", "nav_account": "ACCOUNT", "nav_logout": "LOG OUT", "nav_login": "LOG IN", "nav_join": "REQUEST AN ACCOUNT",
		"footer": "Friends-only fan server. Not affiliated with, endorsed or sponsored by Gravity. Ragnarok Online belongs to its owners.",
		"title":  "Account",

		"login_title": "Log in", "login_h": "LOG IN", "login_user": "Username (same as in the game)", "login_pw": "Password",
		"login_go": "LOG IN ▶", "login_forgot": "Forgot your username or password?", "login_none": "No account yet?", "login_ask": "Request one",

		"join_title": "Request an account", "join_h": "JOIN RAGNADUDS",
		"join_sub":   "A private, friends-only fan server. Ask for an account below.",
		"join_s1":    "1 · THE TERMS",
		"join_t1":    "RagnaDuds is a <b>private, non-commercial fan project</b> run for friends. Nothing is sold; cash points are earned by playing.",
		"join_t2":    "RagnaDuds is <b>not affiliated with, endorsed, sponsored or approved by Gravity Co., Ltd.</b> or any official Ragnarok Online publisher. Ragnarok Online, its names, art and data belong to their owners.",
		"join_t3":    "Accounts are personal. Don't share them, don't cheat, don't use bots, and be decent to other players. Duds can suspend or remove any account at any time.",
		"join_t4":    "The server is offered as it is, without guarantees: it can go down, be wiped or close at any time.",
		"join_t5":    "We store only what you send here (name, e-mail, username, your message) to run your account and to contact you. Ask Duds at any time and it is deleted. Rejected requests are deleted after 30 days.",
		"join_t6":    "If you have any legal concern about this project, you agree to contact Duds first and to raise it only through proper, lawful channels.",
		"join_agree": "I have read and <b>agree to the terms</b> (version %s).", "join_agree_go": "I AGREE ▶",
		"join_s2": "2 · NO CONNECTION WITH GRAVITY", "join_confirm": "Please confirm, explicitly:",
		"join_g1":  "I am <b>not an employee, contractor, agent or representative of Gravity Co., Ltd.</b>, of any of its subsidiaries or licensees, or of any official Ragnarok Online publisher, and I am not asking for an account on their behalf.",
		"join_g2":  "I am not joining to collect evidence or information for any legal action. Any legal concern I may have will be raised with Duds first and only through lawful channels.",
		"join_gok": "I confirm I have <b>no connection with Gravity at all</b>.", "join_gok_go": "I CONFIRM ▶",
		"join_s3": "3 · ABOUT YOU", "join_msg": "Anything you'd like to tell us? (optional: who you know here, why you want to play...)",
		"join_first": "Name", "join_last": "Surname", "join_email": "E-mail (your approval and password link go here)",
		"join_user":    "Username you want (4 to 23 letters, numbers or _ ; for the game and this website)",
		"join_pwlater": "You choose your password later, from the link in the approval e-mail.", "join_send": "SEND MY REQUEST ▶",

		"done_title": "Request sent", "done_h": "REQUEST SENT!", "done_thanks": "Thanks!", "done_thanks_name": "Thanks, %s!",
		"done_queue": "Your request is in the queue. Duds goes through them every day.",
		"done_mail":  "When it's approved you get an e-mail with a link to <b>choose your password</b>. With it you log in to the game and to this website (downloads included).",
		"done_spam":  "Nothing in your inbox? Check the spam folder.",

		"acc_title": "Your account", "acc_h": "YOUR ACCOUNT", "acc_email": "E-mail:",
		"acc_noemail": "none (ask Duds to add one, it's how you reset your password)",
		"acc_same":    "Same username and password in the <b>game</b> (both servers) and on this website.",
		"acc_site":    "▶ GO TO THE SITE / DOWNLOADS", "acc_change": "CHANGE PASSWORD", "acc_current": "Current password",
		"acc_new": "New password (6 to 23)", "acc_again": "Again", "acc_go": "CHANGE ▶",

		"forgot_title": "Forgot password", "forgot_h": "FORGOT IT?",
		"forgot_text":  "Write the e-mail of your account. We send you your <b>username</b> and a link to choose a <b>new password</b> (game and website).",
		"forgot_email": "E-mail", "forgot_go": "SEND ME THE LINK ▶", "forgot_old": "No e-mail on your account (an old account)? Ask Duds for a link.",

		"set_title": "Choose your password", "set_welcome": "WELCOME!", "set_h": "NEW PASSWORD",
		"set_ready": "Your account <b>%s</b> is ready. Choose your password: it's the same for the <b>game</b> and this <b>website</b>.",
		"set_for":   "New password for <b>%s</b> (game and website).",
		"set_pw":    "Password (6 to 23 characters)", "set_again": "Same password again", "set_go": "SAVE ▶",

		"msg_back": "Back to the login",

		"e_login":      "Wrong username or password.",
		"e_nopw":       "This account has no website password yet: use \"Forgot password\" (or the link in your welcome e-mail).",
		"e_terms":      "You must accept both statements.",
		"e_user":       "Username: 4 to 23 letters, numbers or _ .",
		"e_taken":      "That username is already taken or requested. Pick another one.",
		"e_name":       "Please write your name and surname.",
		"e_email":      "Please write a valid e-mail address.",
		"e_msglen":     "The message can have at most 1000 characters.",
		"e_pwdiff":     "The two passwords are different.",
		"e_pwlen":      "The password must have 6 to 23 characters (the game's limit).",
		"e_save":       "Could not save the password right now, try again in a minute.",
		"e_current":    "Your current password is wrong.",
		"t_check":      "CHECK YOUR E-MAIL",
		"x_check":      "If that e-mail belongs to an account, we sent your username and a link to choose a new password. The link works for 2 hours.",
		"t_expired":    "LINK EXPIRED",
		"x_expired":    "This link was already used or has expired. Ask for a new one on the \"Forgot password\" page.",
		"m_logged_out": "You are logged out.",
		"m_pw_saved":   "Password saved. Use it in the game and on this website.",
		"m_pw_changed": "Password changed (game and website).",
	},
	"pt": {
		"nav_site": "SITE", "nav_account": "CONTA", "nav_logout": "SAIR", "nav_login": "ENTRAR", "nav_join": "PEDIR UMA CONTA",
		"footer": "Server de fãs só para amigos. Sem ligação, apoio ou patrocínio da Gravity. Ragnarok Online pertence aos seus donos.",
		"title":  "Conta",

		"login_title": "Entrar", "login_h": "ENTRAR", "login_user": "Usuário (o mesmo do jogo)", "login_pw": "Senha",
		"login_go": "ENTRAR ▶", "login_forgot": "Esqueceu o usuário ou a senha?", "login_none": "Ainda não tem conta?", "login_ask": "Peça uma",

		"join_title": "Pedir uma conta", "join_h": "ENTRE NO RAGNADUDS",
		"join_sub":   "Um server de fãs privado, só para amigos. Peça sua conta aqui embaixo.",
		"join_s1":    "1 · OS TERMOS",
		"join_t1":    "O RagnaDuds é um <b>projeto de fãs privado e sem fins comerciais</b>, feito para amigos. Nada é vendido; os cash points são ganhos jogando.",
		"join_t2":    "O RagnaDuds <b>não tem ligação com a Gravity Co., Ltd.</b>, nem é apoiado, patrocinado ou aprovado por ela ou por qualquer publicadora oficial de Ragnarok Online. Ragnarok Online, seus nomes, artes e dados pertencem aos seus donos.",
		"join_t3":    "As contas são pessoais. Não compartilhe, não trapaceie, não use bots e respeite os outros jogadores. O Duds pode suspender ou remover qualquer conta a qualquer momento.",
		"join_t4":    "O server é oferecido do jeito que está, sem garantias: ele pode cair, ser resetado ou fechar a qualquer momento.",
		"join_t5":    "Guardamos só o que você manda aqui (nome, e-mail, usuário, sua mensagem) para cuidar da sua conta e falar com você. Peça ao Duds a qualquer momento e tudo é apagado. Pedidos recusados são apagados depois de 30 dias.",
		"join_t6":    "Se você tiver qualquer questão jurídica sobre este projeto, você concorda em falar primeiro com o Duds e em levantá-la apenas pelos meios legais e adequados.",
		"join_agree": "Li e <b>concordo com os termos</b> (versão %s).", "join_agree_go": "CONCORDO ▶",
		"join_s2": "2 · NENHUMA LIGAÇÃO COM A GRAVITY", "join_confirm": "Confirme, de forma explícita:",
		"join_g1":  "Eu <b>não sou funcionário, prestador de serviço, agente ou representante da Gravity Co., Ltd.</b>, de nenhuma de suas subsidiárias ou licenciadas, nem de nenhuma publicadora oficial de Ragnarok Online, e não estou pedindo uma conta em nome delas.",
		"join_g2":  "Não estou entrando para juntar provas ou informações para qualquer ação jurídica. Qualquer questão jurídica que eu tiver será levada primeiro ao Duds e apenas pelos meios legais.",
		"join_gok": "Confirmo que <b>não tenho nenhuma ligação com a Gravity</b>.", "join_gok_go": "CONFIRMO ▶",
		"join_s3": "3 · SOBRE VOCÊ", "join_msg": "Quer contar algo pra gente? (opcional: quem você conhece aqui, por que quer jogar...)",
		"join_first": "Nome", "join_last": "Sobrenome", "join_email": "E-mail (a aprovação e o link da senha chegam aqui)",
		"join_user":    "Usuário que você quer (4 a 23 letras, números ou _ ; para o jogo e este site)",
		"join_pwlater": "Você escolhe a senha depois, pelo link do e-mail de aprovação.", "join_send": "ENVIAR MEU PEDIDO ▶",

		"done_title": "Pedido enviado", "done_h": "PEDIDO ENVIADO!", "done_thanks": "Valeu!", "done_thanks_name": "Valeu, %s!",
		"done_queue": "Seu pedido está na fila. O Duds olha os pedidos todo dia.",
		"done_mail":  "Quando for aprovado, você recebe um e-mail com um link para <b>escolher sua senha</b>. Com ela você entra no jogo e neste site (downloads incluídos).",
		"done_spam":  "Não chegou nada? Olhe a pasta de spam.",

		"acc_title": "Sua conta", "acc_h": "SUA CONTA", "acc_email": "E-mail:",
		"acc_noemail": "nenhum (peça ao Duds para colocar um, é com ele que você recupera a senha)",
		"acc_same":    "O mesmo usuário e senha no <b>jogo</b> (os dois servers) e neste site.",
		"acc_site":    "▶ IR PARA O SITE / DOWNLOADS", "acc_change": "TROCAR SENHA", "acc_current": "Senha atual",
		"acc_new": "Nova senha (6 a 23)", "acc_again": "De novo", "acc_go": "TROCAR ▶",

		"forgot_title": "Esqueci a senha", "forgot_h": "ESQUECEU?",
		"forgot_text":  "Escreva o e-mail da sua conta. Mandamos seu <b>usuário</b> e um link para escolher uma <b>nova senha</b> (jogo e site).",
		"forgot_email": "E-mail", "forgot_go": "ME MANDA O LINK ▶", "forgot_old": "Sua conta não tem e-mail (conta antiga)? Peça um link ao Duds.",

		"set_title": "Escolha sua senha", "set_welcome": "BEM-VINDO!", "set_h": "NOVA SENHA",
		"set_ready": "Sua conta <b>%s</b> está pronta. Escolha sua senha: é a mesma para o <b>jogo</b> e para este <b>site</b>.",
		"set_for":   "Nova senha para <b>%s</b> (jogo e site).",
		"set_pw":    "Senha (6 a 23 caracteres)", "set_again": "A mesma senha de novo", "set_go": "SALVAR ▶",

		"msg_back": "Voltar para o login",

		"e_login":      "Usuário ou senha errados.",
		"e_nopw":       "Esta conta ainda não tem senha do site: use \"Esqueceu o usuário ou a senha?\" (ou o link do seu e-mail de boas-vindas).",
		"e_terms":      "Você precisa aceitar as duas declarações.",
		"e_user":       "Usuário: 4 a 23 letras, números ou _ .",
		"e_taken":      "Esse usuário já existe ou já foi pedido. Escolha outro.",
		"e_name":       "Escreva seu nome e sobrenome.",
		"e_email":      "Escreva um e-mail válido.",
		"e_msglen":     "A mensagem pode ter no máximo 1000 caracteres.",
		"e_pwdiff":     "As duas senhas são diferentes.",
		"e_pwlen":      "A senha precisa ter de 6 a 23 caracteres (o limite do jogo).",
		"e_save":       "Não deu para salvar a senha agora, tente de novo em um minuto.",
		"e_current":    "Sua senha atual está errada.",
		"t_check":      "OLHE SEU E-MAIL",
		"x_check":      "Se esse e-mail for de uma conta, mandamos seu usuário e um link para escolher uma nova senha. O link vale por 2 horas.",
		"t_expired":    "LINK EXPIRADO",
		"x_expired":    "Este link já foi usado ou expirou. Peça um novo na página \"Esqueceu o usuário ou a senha?\".",
		"m_logged_out": "Você saiu da conta.",
		"m_pw_saved":   "Senha salva. Use no jogo e neste site.",
		"m_pw_changed": "Senha trocada (jogo e site).",
	},
	"da": {
		"nav_site": "SIDE", "nav_account": "KONTO", "nav_logout": "LOG UD", "nav_login": "LOG IND", "nav_join": "BED OM EN KONTO",
		"footer": "Fanserver kun for venner. Ikke tilknyttet, godkendt eller sponsoreret af Gravity. Ragnarok Online tilhører sine ejere.",
		"title":  "Konto",

		"login_title": "Log ind", "login_h": "LOG IND", "login_user": "Brugernavn (det samme som i spillet)", "login_pw": "Adgangskode",
		"login_go": "LOG IND ▶", "login_forgot": "Glemt dit brugernavn eller din adgangskode?", "login_none": "Ingen konto endnu?", "login_ask": "Bed om en",

		"join_title": "Bed om en konto", "join_h": "BLIV EN DEL AF RAGNADUDS",
		"join_sub":   "En privat fanserver kun for venner. Bed om en konto herunder.",
		"join_s1":    "1 · BETINGELSERNE",
		"join_t1":    "RagnaDuds er et <b>privat, ikke-kommercielt fanprojekt</b> for venner. Intet bliver solgt; cash points optjenes ved at spille.",
		"join_t2":    "RagnaDuds er <b>ikke tilknyttet, godkendt, sponsoreret eller anerkendt af Gravity Co., Ltd.</b> eller nogen officiel udgiver af Ragnarok Online. Ragnarok Online, dets navne, grafik og data tilhører deres ejere.",
		"join_t3":    "Konti er personlige. Del dem ikke, snyd ikke, brug ikke bots, og opfør dig ordentligt over for andre spillere. Duds kan til enhver tid suspendere eller fjerne en konto.",
		"join_t4":    "Serveren tilbydes, som den er, uden garantier: den kan gå ned, blive nulstillet eller lukke når som helst.",
		"join_t5":    "Vi gemmer kun det, du sender her (navn, e-mail, brugernavn, din besked), for at drive din konto og kontakte dig. Spørg Duds når som helst, så bliver det slettet. Afviste anmodninger slettes efter 30 dage.",
		"join_t6":    "Hvis du har juridiske spørgsmål om projektet, accepterer du at kontakte Duds først og kun at rejse dem gennem korrekte, lovlige kanaler.",
		"join_agree": "Jeg har læst og <b>accepterer betingelserne</b> (version %s).", "join_agree_go": "JEG ACCEPTERER ▶",
		"join_s2": "2 · INGEN FORBINDELSE TIL GRAVITY", "join_confirm": "Bekræft venligst udtrykkeligt:",
		"join_g1":  "Jeg er <b>ikke ansat, kontrahent, agent eller repræsentant for Gravity Co., Ltd.</b>, for nogen af dets datterselskaber eller licenstagere eller for nogen officiel udgiver af Ragnarok Online, og jeg beder ikke om en konto på deres vegne.",
		"join_g2":  "Jeg melder mig ikke ind for at indsamle beviser eller oplysninger til nogen retssag. Eventuelle juridiske spørgsmål tager jeg først op med Duds og kun gennem lovlige kanaler.",
		"join_gok": "Jeg bekræfter, at jeg <b>slet ingen forbindelse har til Gravity</b>.", "join_gok_go": "JEG BEKRÆFTER ▶",
		"join_s3": "3 · OM DIG", "join_msg": "Er der noget, du vil fortælle os? (valgfrit: hvem du kender her, hvorfor du vil spille...)",
		"join_first": "Fornavn", "join_last": "Efternavn", "join_email": "E-mail (din godkendelse og dit adgangskode-link kommer hertil)",
		"join_user":    "Ønsket brugernavn (4 til 23 bogstaver, tal eller _ ; til spillet og denne side)",
		"join_pwlater": "Du vælger din adgangskode senere via linket i godkendelses-e-mailen.", "join_send": "SEND MIN ANMODNING ▶",

		"done_title": "Anmodning sendt", "done_h": "ANMODNING SENDT!", "done_thanks": "Tak!", "done_thanks_name": "Tak, %s!",
		"done_queue": "Din anmodning er i køen. Duds går dem igennem hver dag.",
		"done_mail":  "Når den er godkendt, får du en e-mail med et link til at <b>vælge din adgangskode</b>. Med den logger du ind i spillet og på denne side (downloads inklusive).",
		"done_spam":  "Intet i indbakken? Tjek spam-mappen.",

		"acc_title": "Din konto", "acc_h": "DIN KONTO", "acc_email": "E-mail:",
		"acc_noemail": "ingen (bed Duds om at tilføje en, det er sådan du nulstiller din adgangskode)",
		"acc_same":    "Samme brugernavn og adgangskode i <b>spillet</b> (begge servere) og på denne side.",
		"acc_site":    "▶ GÅ TIL SIDEN / DOWNLOADS", "acc_change": "SKIFT ADGANGSKODE", "acc_current": "Nuværende adgangskode",
		"acc_new": "Ny adgangskode (6 til 23)", "acc_again": "Igen", "acc_go": "SKIFT ▶",

		"forgot_title": "Glemt adgangskode", "forgot_h": "GLEMT DEN?",
		"forgot_text":  "Skriv din kontos e-mail. Vi sender dit <b>brugernavn</b> og et link til at vælge en <b>ny adgangskode</b> (spil og side).",
		"forgot_email": "E-mail", "forgot_go": "SEND MIG LINKET ▶", "forgot_old": "Ingen e-mail på din konto (en gammel konto)? Bed Duds om et link.",

		"set_title": "Vælg din adgangskode", "set_welcome": "VELKOMMEN!", "set_h": "NY ADGANGSKODE",
		"set_ready": "Din konto <b>%s</b> er klar. Vælg din adgangskode: den er den samme i <b>spillet</b> og på denne <b>side</b>.",
		"set_for":   "Ny adgangskode til <b>%s</b> (spil og side).",
		"set_pw":    "Adgangskode (6 til 23 tegn)", "set_again": "Samme adgangskode igen", "set_go": "GEM ▶",

		"msg_back": "Tilbage til log ind",

		"e_login":      "Forkert brugernavn eller adgangskode.",
		"e_nopw":       "Denne konto har endnu ingen adgangskode til siden: brug \"Glemt dit brugernavn eller din adgangskode?\" (eller linket i din velkomst-e-mail).",
		"e_terms":      "Du skal acceptere begge erklæringer.",
		"e_user":       "Brugernavn: 4 til 23 bogstaver, tal eller _ .",
		"e_taken":      "Det brugernavn er allerede taget eller anmodet om. Vælg et andet.",
		"e_name":       "Skriv dit fornavn og efternavn.",
		"e_email":      "Skriv en gyldig e-mailadresse.",
		"e_msglen":     "Beskeden må højst have 1000 tegn.",
		"e_pwdiff":     "De to adgangskoder er forskellige.",
		"e_pwlen":      "Adgangskoden skal have 6 til 23 tegn (spillets grænse).",
		"e_save":       "Kunne ikke gemme adgangskoden lige nu, prøv igen om et minut.",
		"e_current":    "Din nuværende adgangskode er forkert.",
		"t_check":      "TJEK DIN E-MAIL",
		"x_check":      "Hvis den e-mail hører til en konto, har vi sendt dit brugernavn og et link til at vælge en ny adgangskode. Linket virker i 2 timer.",
		"t_expired":    "LINKET ER UDLØBET",
		"x_expired":    "Dette link er allerede brugt eller udløbet. Bed om et nyt på siden \"Glemt dit brugernavn eller din adgangskode?\".",
		"m_logged_out": "Du er logget ud.",
		"m_pw_saved":   "Adgangskoden er gemt. Brug den i spillet og på denne side.",
		"m_pw_changed": "Adgangskoden er skiftet (spil og side).",
	},
}

var htmlLang = map[string]string{"en": "en", "pt": "pt-BR", "da": "da-DK"}

// langOf: the "lang" cookie, else the browser's first language, else English.
func langOf(r *http.Request) string {
	if c, err := r.Cookie("lang"); err == nil && texts[c.Value] != nil {
		return c.Value
	}
	al := strings.ToLower(r.Header.Get("Accept-Language"))
	if len(al) >= 2 && texts[al[:2]] != nil {
		return al[:2]
	}
	return "en"
}

// tr: a text key in the page's language; anything else (e.g. an admin message) is shown as it is.
func tr(t map[string]template.HTML, s string) string {
	if v, ok := t[s]; ok {
		return string(v)
	}
	return s
}

// tf fills %s in a text with escaped values: {{tf .L.set_for .Username}}.
func tf(t template.HTML, args ...any) template.HTML {
	s := string(t)
	for _, a := range args {
		s = strings.Replace(s, "%s", template.HTMLEscapeString(fmt.Sprint(a)), 1)
	}
	return template.HTML(s)
}
