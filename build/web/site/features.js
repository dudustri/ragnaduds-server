// RagnaDuds server features page (features.html). Texts per language (EN / PT / DA); every section and NPC row
// says which server it's on: "re" (Renewal), "pre" (Pre-Renewal) or "both". A section's body can differ per server
// ({ re: "...", pre: "..." }). The switch at the top shows one server; the language and server are remembered.

const NPCS = [   // [name, where, servers, { en, pt, da } what]
  ["Warper", "Prontera 159,192 · 45 towns", "both", { en: "Teleports to towns, fields and dungeons", pt: "Teleporta pra cidades, campos e cavernas", da: "Teleporterer til byer, marker og dungeons" }],
  ["Healer", "Prontera 162,193 · 36 towns", "both", { en: "Full heal", pt: "Cura total", da: "Fuld heal" }],
  ["Job Master", "Prontera 153,193", "both", { en: "Instant job change, quest skills included", pt: "Troca de classe na hora, com as skills de quest", da: "Jobskift med det samme, quest-skills inkluderet" }],
  ["Agente VIP", "36 spots · Prontera 146,93", "both", { en: "Free Blessing + Increase AGI Lv 10 (bRO's VIP spots)", pt: "Bênção + Aumentar Agilidade Lv 10 grátis (os lugares do VIP do bRO)", da: "Gratis Blessing + Increase AGI Lv 10 (bRO's VIP-steder)" }],
  ["Reset Girl", "Prontera 150,193", "re", { en: "Reset stats and/or skills", pt: "Reseta status e/ou skills", da: "Nulstil stats og/eller skills" }],
  ["Platinum Skill NPC", "Prontera 128,200", "re", { en: "Your class' quest skills", pt: "Skills de quest da sua classe", da: "Din klasses quest-skills" }],
  ["Stylist", "Prontera 170,180", "re", { en: "Hair style, hair colour, clothes colour", pt: "Penteado, cor do cabelo, cor da roupa", da: "Frisure, hårfarve, tøjfarve" }],
  ["Private MVP Room", "Prontera 148,174", "re", { en: "Rent a room (100k zeny, 1 hour, party/guild/account) and summon MVPs (100k) or bosses (50k). These MVPs give no cash points.", pt: "Aluga uma sala (100k zeny, 1 hora, grupo/clã/conta) e invoca MVPs (100k) ou chefes (50k). Esses MVPs não dão pontos de cash.", da: "Lej et rum (100k zeny, 1 time, party/guild/konto) og tilkald MVP'er (100k) eller bosser (50k). Disse MVP'er giver ingen cash points." }],
  ["Refine Master", "Prontera 184,177", "re", { en: "Safe refine with the +14 / +19 certificates", pt: "Refino seguro com os certificados +14 / +19", da: "Sikker refine med +14 / +19 certifikaterne" }],
  ["Shadow Blacksmith", "Prontera 187,177", "re", { en: "Refine window, shadow gear too", pt: "Janela de refino, inclusive equipamento sombrio", da: "Refine-vindue, også shadow gear" }],
  ["Homunculus Trainer", "Prontera 190,177", "re", { en: "Private Homunculus Room (alchemists)", pt: "Sala do Homúnculo privada (alquimistas)", da: "Privat Homunculus Room (alchemister)" }],
  ["Nanaru", "Morroc 152,272", "re", { en: "Mapas Especiais (8 monster rooms)", pt: "Mapas Especiais (8 salas de monstros)", da: "Mapas Especiais (8 monsterrum)" }],
  ["Portal Fantasma", "Comodo 208,187", "re", { en: "Cheffenia (4 MVP rooms)", pt: "Cheffenia (4 salas de MVP)", da: "Cheffenia (4 MVP-rum)" }],
  ["Mateus Alem", "Geffen 128,117", "re", { en: "Turn In hunting quest", pt: "Quest de caça Turn In", da: "Turn In jagt-quest" }],
  ["Vomars · Happy Marry · Sister Lisa", "prt_church", "re", { en: "Weddings", pt: "Casamentos", da: "Bryllupper" }],
];

const T = {
  en: {
    back: "◀ BACK", title: "SERVER FEATURES", tagline: "Everything RagnaDuds has, on one page.",
    note: { re: "Renewal · 2026 client · 3rd & 4th jobs · level 275", pre: "Pre-Renewal · 2021 client · classic 99/70" },
    tag: { re: "RENEWAL", pre: "PRE-RENEWAL", both: "BOTH SERVERS" },
    npchead: ["NPC", "WHERE", "WHAT"], npctip: "Tip: type <code>/navi prontera 187/177</code> in game to get a route to any spot.",
    footer: "Friends-only fan server. Not affiliated with Gravity. Ragnarok Online belongs to its owners.",
    sections: [
      ["rates", "both", "RATES", {
        re: `<div class="grid"><div class="stat"><span class="v">10x</span><span class="l">EXP</span></div><div class="stat"><span class="v">10x</span><span class="l">drops (cards too)</span></div><div class="stat"><span class="v">275</span><span class="l">max base level</span></div></div>
          <ul><li><b>No EXP penalty for level difference</b>: kill anything, any level, full EXP.</li>
          <li><b>Parties share everything</b>: EXP Even Share, items shared, up to <b>999 levels</b> apart. New parties are set automatically.</li></ul>`,
        pre: `<div class="grid"><div class="stat"><span class="v">10x</span><span class="l">EXP</span></div><div class="stat"><span class="v">3x</span><span class="l">drops (cards too)</span></div><div class="stat"><span class="v">99/70</span><span class="l">base / job cap</span></div></div>
          <ul><li><b>Parties share everything</b>: EXP Even Share, items shared, up to <b>999 levels</b> apart. New parties are set automatically.</li></ul>` }],
      ["shop", "re", "CASH SHOP &amp; POINTS", `
        <p>Earn <b>cash points</b> by playing, spend them in the Cash Shop (the shop button in game). Type <code>@points</code> to see yours.</p>
        <table><tr><th>HOW</th><th>POINTS</th></tr>
          <tr><td>First login of the day</td><td class="c">+1,000</td></tr>
          <tr><td>Every hour played (not AFK)</td><td class="c">+500</td></tr>
          <tr><td>Every MVP you kill (last hit)</td><td class="c">+5,000</td></tr>
          <tr><td>Every PvP kill (not the same victim twice in 10 min)</td><td class="c">+3,000</td></tr></table>
        <p>Tabs: <em>Beginner</em> (rush gear), <em>2nd Class</em>, <em>3rd Class</em>, <em>Endgame</em> (full sets per build), <em>MVP Cards</em>, <em>Refine</em>, <em>Items &amp; Pets</em> (manuals, speed, stat foods, acid packs, Kafra card, pet eggs) and <em>Visuals</em> (the ride and costumes: wings, auras, halos, crowns).</p>`],
      ["refine", "re", "REFINING", `<ul>
          <li><b>Refine Master</b> (Prontera 184,177): safe refine with the <em>Safe to +14</em> / <em>Safe to +19</em> certificates from the shop.</li>
          <li><b>Shadow Blacksmith</b> (Prontera 187,177): opens the Refine window, also for shadow gear. Safe up to +4; from +5, HD ores only drop it one level.</li>
          <li><b>Shadow 9 Refine Hammer</b> (shop): any shadow piece up to +8 becomes <b>+9</b>, no risk. <b>Shadow Refine Hammer</b>: random +1 to +10.</li>
          <li>HD and Enriched Elunium / Oridecon, Blacksmith Blessing and costume enchant stones in the <em>Refine</em> tab.</li></ul>`],
      ["maps", "re", "SPECIAL MAPS (bRO EVENTS)", `
        <div class="scroll"><table><tr><th>WHAT</th><th>WHERE</th><th>WHAT'S INSIDE</th></tr>
          <tr><td><b>Mapas Especiais</b></td><td class="c">Nanaru · Morroc 152,272</td><td>8 rooms packed with monsters that respawn instantly, no EXP loss on death. Base 70+. Ticket: 1 point.</td></tr>
          <tr><td><b>Cheffenia</b></td><td class="c">Portal Fantasma · Comodo 208,187</td><td>4 MVP rooms, bosses with double HP and +50% damage. Free storage and healer inside. After 1,000 kills a day, no drops there until tomorrow. Base 90+. Ticket: 1 point.</td></tr>
          <tr><td><b>Turn In</b></td><td class="c">Mateus Alem · Geffen 128,117</td><td>Kill 400 of one monster, get 400x its EXP. Once a day. Hunting caves by level.</td></tr></table></div>`],
      ["homun", "both", "HOMUNCULUS", {
        re: `<p><b>Homunculus Room</b> · <b>Homunculus Trainer</b>, Prontera 190,177. Alchemist line only, free, enter as often as you want.</p>
          <ul><li>Your own private round arena. 30 monsters stand still around you, so they never scatter and your homunculus reaches every one. They come back within 3 seconds.</li>
          <li>9 monster sets by homunculus level, from Poring/Lunatic (Lv 1-15) and Spore/Rocker (15-30) up to Beholder/Imp (120+). Change set with the Guide inside.</li></ul>
          <p>And everywhere:</p>`,
        pre: "", after: `<ul><li>Your homunculus is <b>kept fed</b>: it never starves, never loses intimacy, never runs away.</li>
          <li>It <b>stays out when you die</b> (not sent to rest).</li>
          <li>Smart AI shipped with the game: type <code>/hoai</code> once and it hunts by itself.</li>
          <li><b>Its loot comes to you</b>: type <code>@autoloot</code> (or <code>@alootid +item</code> for chosen items) and whatever your homunculus kills on its own goes straight into your bag. Your own kills you still pick up by hand.</li></ul>` }],
      ["npcs", "both", "NPC DIRECTORY", "NPCS"],
      ["client", "both", "THE CLIENT", {
        re: `<ul><li>Kingdom of Ragnarok 2026 client, everything in English: items, skills, NPCs, maps. Every item has a picture and a description.</li>
          <li>Text in <b>Arial</b>, like the old bRO.</li>
          <li>Login and loading screens of our own, no web pages popping up on exit or in the shop.</li>
          <li>Installers for Windows and Linux (with uninstall) on the home page.</li></ul>`,
        pre: `<ul><li>Classic 2021 client, everything in English.</li>
          <li>Login and loading screens of our own, no web pages popping up on exit.</li>
          <li>Installers for Windows and Linux (with uninstall) on the home page.</li></ul>` }],
    ],
  },
  pt: {
    back: "◀ VOLTAR", title: "O QUE TEM NO SERVER", tagline: "Tudo do RagnaDuds numa página só.",
    note: { re: "Renewal · cliente 2026 · classes 3 e 4 · nível 275", pre: "Pre-Renewal · cliente 2021 · clássico 99/70" },
    tag: { re: "RENEWAL", pre: "PRE-RENEWAL", both: "OS DOIS SERVERS" },
    npchead: ["NPC", "ONDE", "O QUE FAZ"], npctip: "Dica: digite <code>/navi prontera 187/177</code> no jogo pra ver o caminho até qualquer lugar.",
    footer: "Servidor de fãs só pra amigos. Sem ligação com a Gravity. Ragnarok Online pertence aos donos.",
    sections: [
      ["rates", "both", "RATES", {
        re: `<div class="grid"><div class="stat"><span class="v">10x</span><span class="l">EXP</span></div><div class="stat"><span class="v">10x</span><span class="l">drop (cartas também)</span></div><div class="stat"><span class="v">275</span><span class="l">nível base máximo</span></div></div>
          <ul><li><b>Sem penalidade de EXP por diferença de nível</b>: mata qualquer coisa, qualquer nível, EXP cheia.</li>
          <li><b>Grupo divide tudo</b>: EXP dividida igual, itens compartilhados, até <b>999 níveis</b> de diferença. Grupo novo já vem configurado.</li></ul>`,
        pre: `<div class="grid"><div class="stat"><span class="v">10x</span><span class="l">EXP</span></div><div class="stat"><span class="v">3x</span><span class="l">drop (cartas também)</span></div><div class="stat"><span class="v">99/70</span><span class="l">nível base / classe</span></div></div>
          <ul><li><b>Grupo divide tudo</b>: EXP dividida igual, itens compartilhados, até <b>999 níveis</b> de diferença. Grupo novo já vem configurado.</li></ul>` }],
      ["shop", "re", "CASH SHOP E PONTOS", `
        <p>Ganhe <b>pontos de cash</b> jogando e gaste na Cash Shop (o botão da loja no jogo). Digite <code>@points</code> pra ver os seus.</p>
        <table><tr><th>COMO</th><th>PONTOS</th></tr>
          <tr><td>Primeiro login do dia</td><td class="c">+1.000</td></tr>
          <tr><td>Cada hora jogada (sem AFK)</td><td class="c">+500</td></tr>
          <tr><td>Cada MVP que você mata (último golpe)</td><td class="c">+5.000</td></tr>
          <tr><td>Cada kill de PvP (não a mesma vítima 2x em 10 min)</td><td class="c">+3.000</td></tr></table>
        <p>Abas: <em>Beginner</em> (equipamento pra upar), <em>2nd Class</em>, <em>3rd Class</em>, <em>Endgame</em> (sets completos por build), <em>MVP Cards</em>, <em>Refine</em>, <em>Items &amp; Pets</em> (manuais, velocidade, comidas de status, pacotes de ácido, cartão Kafra, ovos de mascote) e <em>Visuals</em> (a montaria e visuais: asas, auras, auréolas, coroas).</p>`],
      ["refine", "re", "REFINO", `<ul>
          <li><b>Refine Master</b> (Prontera 184,177): refino seguro com os certificados <em>Safe to +14</em> / <em>Safe to +19</em> da loja.</li>
          <li><b>Shadow Blacksmith</b> (Prontera 187,177): abre a janela de refino, inclusive pra equipamento sombrio. Seguro até +4; a partir do +5, minério HD só faz cair um nível.</li>
          <li><b>Shadow 9 Refine Hammer</b> (loja): qualquer peça sombria até +8 vira <b>+9</b>, sem risco. <b>Shadow Refine Hammer</b>: aleatório de +1 a +10.</li>
          <li>Elunium / Oridecon HD e Enriquecido, Bênção do Ferreiro e pedras de encantamento de visual na aba <em>Refine</em>.</li></ul>`],
      ["maps", "re", "MAPAS ESPECIAIS (EVENTOS DO bRO)", `
        <div class="scroll"><table><tr><th>O QUE</th><th>ONDE</th><th>O QUE TEM</th></tr>
          <tr><td><b>Mapas Especiais</b></td><td class="c">Nanaru · Morroc 152,272</td><td>8 salas lotadas de monstros que renascem na hora, sem perder EXP ao morrer. Base 70+. Ingresso: 1 ponto.</td></tr>
          <tr><td><b>Cheffenia</b></td><td class="c">Portal Fantasma · Comodo 208,187</td><td>4 salas de MVP, chefes com o dobro de HP e +50% de dano. Armazém e curandeira grátis lá dentro. Depois de 1.000 kills no dia, sem drop lá até amanhã. Base 90+. Passe: 1 ponto.</td></tr>
          <tr><td><b>Turn In</b></td><td class="c">Mateus Alem · Geffen 128,117</td><td>Mate 400 de um monstro e ganhe 400x a EXP dele. Uma vez por dia. Cavernas de caça por nível.</td></tr></table></div>`],
      ["homun", "both", "HOMÚNCULO", {
        re: `<p><b>Sala do Homúnculo</b> · <b>Homunculus Trainer</b>, Prontera 190,177. Só pra linha do Alquimista, grátis, entra quantas vezes quiser.</p>
          <ul><li>Sua própria arena redonda e privada. 30 monstros parados ao seu redor: nunca se espalham e o homúnculo alcança todos. Voltam em até 3 segundos.</li>
          <li>9 grupos de monstros por nível do homúnculo, de Poring/Lunatic (Lv 1-15) e Esporo/Rocker (15-30) até Beholder/Imp (120+). Troque com o Guia lá dentro.</li></ul>
          <p>E em todo lugar:</p>`,
        pre: "", after: `<ul><li>Seu homúnculo <b>fica sempre alimentado</b>: nunca passa fome, nunca perde intimidade, nunca foge.</li>
          <li>Ele <b>continua fora quando você morre</b> (não vai descansar).</li>
          <li>IA esperta que vem com o jogo: digite <code>/hoai</code> uma vez e ele caça sozinho.</li>
          <li><b>O loot vem pra você</b>: digite <code>@autoloot</code> (ou <code>@alootid +item</code> pra itens escolhidos) e o que o homúnculo mata sozinho vai direto pra sua mochila. O que você mesmo mata, ainda pega na mão.</li></ul>` }],
      ["npcs", "both", "LISTA DE NPCS", "NPCS"],
      ["client", "both", "O CLIENTE", {
        re: `<ul><li>Cliente kRO 2026, tudo em inglês: itens, skills, NPCs, mapas. Todo item tem imagem e descrição.</li>
          <li>Texto em <b>Arial</b>, igual ao bRO antigo.</li>
          <li>Telas de login e carregamento nossas, nenhuma página da web abrindo ao sair ou na loja.</li>
          <li>Instaladores pra Windows e Linux (com desinstalador) na página inicial.</li></ul>`,
        pre: `<ul><li>Cliente clássico 2021, tudo em inglês.</li>
          <li>Telas de login e carregamento nossas, nenhuma página da web abrindo ao sair.</li>
          <li>Instaladores pra Windows e Linux (com desinstalador) na página inicial.</li></ul>` }],
    ],
  },
  da: {
    back: "◀ TILBAGE", title: "SERVERENS FEATURES", tagline: "Alt hvad RagnaDuds har, på én side.",
    note: { re: "Renewal · 2026-klient · 3. og 4. job · level 275", pre: "Pre-Renewal · 2021-klient · klassisk 99/70" },
    tag: { re: "RENEWAL", pre: "PRE-RENEWAL", both: "BEGGE SERVERE" },
    npchead: ["NPC", "HVOR", "HVAD"], npctip: "Tip: skriv <code>/navi prontera 187/177</code> i spillet for at få vejen til ethvert sted.",
    footer: "Fan-server kun for venner. Ikke tilknyttet Gravity. Ragnarok Online tilhører sine ejere.",
    sections: [
      ["rates", "both", "RATES", {
        re: `<div class="grid"><div class="stat"><span class="v">10x</span><span class="l">EXP</span></div><div class="stat"><span class="v">10x</span><span class="l">drops (også kort)</span></div><div class="stat"><span class="v">275</span><span class="l">max base level</span></div></div>
          <ul><li><b>Ingen EXP-straf for niveauforskel</b>: dræb hvad som helst, ethvert niveau, fuld EXP.</li>
          <li><b>Parties deler alt</b>: EXP Even Share, delte items, op til <b>999 niveauer</b> fra hinanden. Nye parties sættes op automatisk.</li></ul>`,
        pre: `<div class="grid"><div class="stat"><span class="v">10x</span><span class="l">EXP</span></div><div class="stat"><span class="v">3x</span><span class="l">drops (også kort)</span></div><div class="stat"><span class="v">99/70</span><span class="l">base / job loft</span></div></div>
          <ul><li><b>Parties deler alt</b>: EXP Even Share, delte items, op til <b>999 niveauer</b> fra hinanden. Nye parties sættes op automatisk.</li></ul>` }],
      ["shop", "re", "CASH SHOP OG POINTS", `
        <p>Tjen <b>cash points</b> ved at spille, og brug dem i Cash Shop (butiksknappen i spillet). Skriv <code>@points</code> for at se dine.</p>
        <table><tr><th>HVORDAN</th><th>POINTS</th></tr>
          <tr><td>Dagens første login</td><td class="c">+1.000</td></tr>
          <tr><td>Hver time spillet (ikke AFK)</td><td class="c">+500</td></tr>
          <tr><td>Hver MVP du dræber (sidste slag)</td><td class="c">+5.000</td></tr>
          <tr><td>Hvert PvP-kill (ikke samme offer 2x på 10 min)</td><td class="c">+3.000</td></tr></table>
        <p>Faner: <em>Beginner</em> (rush-gear), <em>2nd Class</em>, <em>3rd Class</em>, <em>Endgame</em> (fulde sæt pr. build), <em>MVP Cards</em>, <em>Refine</em>, <em>Items &amp; Pets</em> (manualer, speed, stat-mad, syrepakker, Kafra-kort, kæledyrsæg) og <em>Visuals</em> (ridedyret og kostumer: vinger, auraer, glorier, kroner).</p>`],
      ["refine", "re", "REFINING", `<ul>
          <li><b>Refine Master</b> (Prontera 184,177): sikker refine med <em>Safe to +14</em> / <em>Safe to +19</em> certifikaterne fra butikken.</li>
          <li><b>Shadow Blacksmith</b> (Prontera 187,177): åbner refine-vinduet, også til shadow gear. Sikkert op til +4; fra +5 får HD-malm den kun til at falde ét niveau.</li>
          <li><b>Shadow 9 Refine Hammer</b> (butik): enhver shadow-del op til +8 bliver <b>+9</b>, ingen risiko. <b>Shadow Refine Hammer</b>: tilfældigt +1 til +10.</li>
          <li>HD og Enriched Elunium / Oridecon, Blacksmith Blessing og costume-enchant-sten i <em>Refine</em>-fanen.</li></ul>`],
      ["maps", "re", "SPECIAL MAPS (bRO-EVENTS)", `
        <div class="scroll"><table><tr><th>HVAD</th><th>HVOR</th><th>HVAD ER DER</th></tr>
          <tr><td><b>Mapas Especiais</b></td><td class="c">Nanaru · Morroc 152,272</td><td>8 rum fyldt med monstre der respawner med det samme, intet EXP-tab ved død. Base 70+. Billet: 1 point.</td></tr>
          <tr><td><b>Cheffenia</b></td><td class="c">Portal Fantasma · Comodo 208,187</td><td>4 MVP-rum, bosser med dobbelt HP og +50% skade. Gratis storage og healer derinde. Efter 1.000 kills på en dag: ingen drops der før i morgen. Base 90+. Billet: 1 point.</td></tr>
          <tr><td><b>Turn In</b></td><td class="c">Mateus Alem · Geffen 128,117</td><td>Dræb 400 af ét monster, få 400x dets EXP. Én gang om dagen. Jagtgrotter efter niveau.</td></tr></table></div>`],
      ["homun", "both", "HOMUNCULUS", {
        re: `<p><b>Homunculus Room</b> · <b>Homunculus Trainer</b>, Prontera 190,177. Kun Alchemist-linjen, gratis, gå ind så tit du vil.</p>
          <ul><li>Din egen private runde arena. 30 monstre står stille omkring dig, så de spreder sig aldrig, og din homunculus når dem alle. De kommer tilbage inden for 3 sekunder.</li>
          <li>9 monstersæt efter homunculus-niveau, fra Poring/Lunatic (Lv 1-15) og Spore/Rocker (15-30) op til Beholder/Imp (120+). Skift sæt hos Guiden derinde.</li></ul>
          <p>Og overalt:</p>`,
        pre: "", after: `<ul><li>Din homunculus <b>holdes mæt</b>: sulter aldrig, mister aldrig intimacy, stikker aldrig af.</li>
          <li>Den <b>bliver ude, når du dør</b> (sendes ikke til hvile).</li>
          <li>Smart AI med i spillet: skriv <code>/hoai</code> én gang, så jager den selv.</li>
          <li><b>Dens loot kommer til dig</b>: skriv <code>@autoloot</code> (eller <code>@alootid +item</code> for udvalgte items), og hvad din homunculus dræber alene, ryger direkte i din taske. Dine egne kills samler du stadig op i hånden.</li></ul>` }],
      ["npcs", "both", "NPC-OVERSIGT", "NPCS"],
      ["client", "both", "KLIENTEN", {
        re: `<ul><li>kRO 2026-klient, alt på engelsk: items, skills, NPC'er, maps. Hvert item har et billede og en beskrivelse.</li>
          <li>Tekst i <b>Arial</b>, ligesom det gamle bRO.</li>
          <li>Vores egne login- og loadingskærme, ingen websider der popper op ved afslutning eller i butikken.</li>
          <li>Installere til Windows og Linux (med afinstallation) på forsiden.</li></ul>`,
        pre: `<ul><li>Klassisk 2021-klient, alt på engelsk.</li>
          <li>Vores egne login- og loadingskærme, ingen websider der popper op ved afslutning.</li>
          <li>Installere til Windows og Linux (med afinstallation) på forsiden.</li></ul>` }],
    ],
  },
};
const LOCALE = { en: "en", pt: "pt-BR", da: "da-DK" };
const store = (k, v) => { try { return v === undefined ? localStorage.getItem(k) : localStorage.setItem(k, v) } catch { return null } };

let LANG = store("lang") || ({ pt: "pt", da: "da" }[(navigator.language || "").toLowerCase().slice(0, 2)] || "en");
if (!T[LANG]) LANG = "en";
let SRV = new URLSearchParams(location.search).get("server") || store("server") || "re";
if (SRV !== "re" && SRV !== "pre") SRV = "re";

const on = (where) => where === "both" || where === SRV;

function npcTable(t) {
  const rows = NPCS.filter(n => on(n[2])).map(([name, where, , what]) =>
    `<tr><td><b>${name}</b></td><td class="c">${where}</td><td>${what[LANG]}</td></tr>`).join("");
  return `<div class="scroll"><table><tr>${t.npchead.map(h => `<th>${h}</th>`).join("")}</tr>${rows}</table></div><p>${t.npctip}</p>`;
}

function render() {
  const t = T[LANG];
  document.documentElement.lang = LOCALE[LANG] || "en";
  document.querySelectorAll("[data-i18n]").forEach(e => e.innerHTML = t[e.dataset.i18n]);
  document.querySelectorAll("[data-lang]").forEach(b => b.setAttribute("aria-pressed", b.dataset.lang === LANG));
  document.querySelectorAll("[data-srv]").forEach(b => b.setAttribute("aria-pressed", b.dataset.srv === SRV));
  document.getElementById("srvnote").textContent = t.note[SRV];
  const shown = t.sections.filter(([, where]) => on(where));
  document.getElementById("toc").innerHTML = shown.map(([id, , title]) => `<a href="#${id}">${title}</a>`).join("");
  document.getElementById("sections").innerHTML = shown.map(([id, where, title, body]) => {
    let html = body === "NPCS" ? npcTable(t) : typeof body === "string" ? body : (body[SRV] || "") + (body.after || "");
    const tag = where === "both" ? SRV : where;   // the badge says which server you're looking at
    return `<section class="frame" id="${id}"><h2>${title}<span class="tag ${tag}">${t.tag[tag]}</span></h2>${html}</section>`;
  }).join("");
  store("lang", LANG); store("server", SRV);
}
document.querySelectorAll("[data-lang]").forEach(b => b.addEventListener("click", () => { LANG = b.dataset.lang; render(); }));
document.querySelectorAll("[data-srv]").forEach(b => b.addEventListener("click", () => { SRV = b.dataset.srv; render(); }));
render();
if (location.hash) document.querySelector(location.hash)?.scrollIntoView();
