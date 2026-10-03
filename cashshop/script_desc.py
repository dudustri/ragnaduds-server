"""English item description built from the server's item script (db/re/item_db_*.yml).

Used when there is no official English text for an item (divine-pride only has a placeholder, or Japanese/Korean
text). It reads what the server really applies: "bonus bStr,3;" -> "STR +3", "if (.@r>=7) {" -> "Refine +7 or higher:",
"5*.@r" -> "+5 per refine level". Statements it doesn't know are left out (the stat lines are still right).
"""
import os, re, yaml

RATHENA = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SEP = "________________________"

STAT = {  # bonus <name>,<value>   ->  label, unit ("" or "%" or "s" for ms->seconds)
    "bStr": ("STR", ""), "bAgi": ("AGI", ""), "bVit": ("VIT", ""), "bInt": ("INT", ""), "bDex": ("DEX", ""),
    "bLuk": ("LUK", ""), "bAllStats": ("All Stats", ""), "bPow": ("POW", ""), "bSta": ("STA", ""),
    "bWis": ("WIS", ""), "bSpl": ("SPL", ""), "bCon": ("CON", ""), "bCrt": ("CRT", ""),
    "bAllTraitStats": ("All Trait Stats", ""),
    "bBaseAtk": ("ATK", ""), "bAtk": ("ATK", ""), "bAtk2": ("ATK", ""), "bMatk": ("MATK", ""),
    "bAtkRate": ("ATK", "%"), "bMatkRate": ("MATK", "%"), "bDef": ("DEF", ""), "bMdef": ("MDEF", ""),
    "bDefRate": ("DEF", "%"), "bMdefRate": ("MDEF", "%"), "bDef2": ("Soft DEF", ""), "bMdef2": ("Soft MDEF", ""),
    "bPAtk": ("P.ATK", ""), "bSMatk": ("S.MATK", ""), "bRes": ("RES", ""), "bMRes": ("MRES", ""),
    "bHPlus": ("H.PLUS", ""), "bCRate": ("C.RATE", ""),
    "bMaxHP": ("MaxHP", ""), "bMaxSP": ("MaxSP", ""), "bMaxHPrate": ("MaxHP", "%"), "bMaxSPrate": ("MaxSP", "%"),
    "bMaxAP": ("MaxAP", ""), "bHit": ("HIT", ""), "bFlee": ("FLEE", ""), "bFlee2": ("Perfect Dodge", ""),
    "bCritical": ("CRIT", ""), "bCritAtkRate": ("Critical damage", "%"), "bAspd": ("ASPD", ""),
    "bAspdRate": ("ASPD", "%"), "bLongAtkRate": ("Ranged physical damage", "%"),
    "bShortAtkRate": ("Melee physical damage", "%"), "bDelayrate": ("Global cooldown (after-cast delay)", "%"),
    "bVariableCastrate": ("Variable cast time", "%"), "bFixedCastrate": ("Fixed cast time", "%"),
    "bFixedCast": ("Fixed cast time", "s"), "bVariableCast": ("Variable cast time", "s"),
    "bHealPower": ("Healing skills effectiveness", "%"), "bHealPower2": ("Healing received", "%"),
    "bAddItemHealRate": ("Healing items effectiveness", "%"), "bUseSPrate": ("SP cost of skills", "%"),
    "bHPrecovRate": ("Natural HP recovery", "%"), "bSPrecovRate": ("Natural SP recovery", "%"),
    "bPerfectHitAddRate": ("Perfect hit chance", "%"), "bLongAtkDef": ("Resistance to ranged physical attacks", "%"),
    "bNearAtkDef": ("Resistance to melee physical attacks", "%"), "bMagicDamageReturn": ("Reflect magic", "%"),
    "bShortWeaponDamageReturn": ("Reflect melee damage", "%"), "bSpeedRate": ("Movement speed", "%"),
    "bSPGainValue": ("SP gained per kill", ""), "bHPGainValue": ("HP gained per kill", ""),
    "bCastrate": ("Cast time", "%"), "bNoCastCancel": None,
}
FLAGS = {
    "bUnbreakableWeapon": "Weapon can't be destroyed.", "bUnbreakableArmor": "Armor can't be destroyed.",
    "bUnbreakableHelm": "Headgear can't be destroyed.", "bUnbreakableShoes": "Shoes can't be destroyed.",
    "bUnbreakableGarment": "Garment can't be destroyed.", "bUnbreakableShield": "Shield can't be destroyed.",
    "bNoKnockback": "Can't be knocked back.", "bNoSizeFix": "No size penalty.", "bNoCastCancel": "Casting can't be interrupted.",
    "bNoGemStone": "Skills need no gemstones.", "bNoWalkDelay": "No walk delay when hit.", "bRestartFullRecover": "Full HP/SP when resurrected.",
}
PAIR = {  # bonus2 <name>,<target>,<value>
    "bAddRace": "Physical damage against {} monsters", "bMagicAddRace": "Magical damage against {} monsters",
    "bSubRace": "Resistance to {} monsters", "bAddEle": "Physical damage against {} property",
    "bMagicAddEle": "Magical damage against {} property", "bSubEle": "Resistance to {} property",
    "bMagicAtkEle": "{} property magical damage", "bAddSize": "Physical damage against {} monsters",
    "bMagicAddSize": "Magical damage against {} monsters", "bSubSize": "Resistance to {} monsters",
    "bAddClass": "Physical damage against {} monsters", "bMagicAddClass": "Magical damage against {} monsters",
    "bSubClass": "Resistance to {} monsters", "bIgnoreDefRaceRate": "Ignore DEF of {} monsters",
    "bIgnoreMdefRaceRate": "Ignore MDEF of {} monsters", "bIgnoreDefClassRate": "Ignore DEF of {} monsters",
    "bIgnoreMdefClassRate": "Ignore MDEF of {} monsters", "bExpAddRace": "EXP from {} monsters",
    "bSkillAtk": "Damage of {}", "bSkillHeal": "Healing of {}", "bSkillCooldown": "Cooldown of {}",
    "bSkillUseSP": "SP cost of {}", "bSkillUseSPrate": "SP cost of {}", "bVariableCastrate": "Variable cast time of {}",
    "bFixedCastrate": "Fixed cast time of {}", "bSkillFixedCast": "Fixed cast time of {}",
    "bSkillVariableCast": "Variable cast time of {}", "bResEff": "Resistance to {}", "bAddEff": "Chance to inflict {}",
    "bHPRegenRate": None, "bSPRegenRate": None, "bHPDrainRate": None, "bSPDrainRate": None,
}
UNIT2 = {"bSkillCooldown": "s", "bSkillFixedCast": "s", "bSkillVariableCast": "s", "bSkillUseSP": "",
         "bResEff": "%%", "bAddEff": "%%"}   # %% = value is 1/100 of a percent


def _consts(prefix_map):
    out = {}
    for pre, nice in prefix_map.items():
        out[pre] = nice
    return out


RACE = {"All": "all", "Formless": "Formless", "Undead": "Undead", "Brute": "Brute", "Plant": "Plant",
        "Insect": "Insect", "Fish": "Fish", "Demon": "Demon", "DemiHuman": "Demi-Human", "Angel": "Angel",
        "Dragon": "Dragon", "Player_Human": "Human player", "Player_Doram": "Doram player"}
ELE = {"All": "all", "Neutral": "Neutral", "Water": "Water", "Earth": "Earth", "Fire": "Fire", "Wind": "Wind",
       "Poison": "Poison", "Holy": "Holy", "Dark": "Shadow", "Ghost": "Ghost", "Undead": "Undead"}
SIZE = {"All": "all sizes of", "Small": "Small", "Medium": "Medium", "Large": "Large"}
CLASS = {"All": "all", "Normal": "normal", "Boss": "Boss", "Guardian": "Guardian"}


class Describer:
    def __init__(self):
        self.skills = {}
        for f in ("skill_db.yml",):
            for s in yaml.safe_load(open(os.path.join(RATHENA, "db", "re", f)))["Body"]:
                self.skills[s["Name"]] = s.get("Description") or s["Name"]

    # --- names -----------------------------------------------------------------------------------------------
    def target(self, t):
        t = t.strip().strip('"')
        for pre, table in (("RC_", RACE), ("Ele_", ELE), ("Size_", SIZE), ("Class_", CLASS)):
            if t.startswith(pre):
                return table.get(t[len(pre):], t[len(pre):].replace("_", " "))
        if t.startswith("Eff_"):
            return t[4:].capitalize()
        return f"[{self.skills.get(t, t.replace('_', ' ').title())}]"

    TERM = re.compile(r'readparam\(b\w+\)|getskilllv\("?\w+"?\)|getrefine\(\)|getenchantgrade\(\)|\.@r\b|\.@g\b|BaseLevel|JobLevel')

    def term(self, e, n=1):
        """Plain words for a script term (.@r, readparam(bStr), getskilllv("X"), BaseLevel...), n = how many."""
        e = e.strip()
        many = n != 1
        if e in (".@r", "getrefine()"): return "refine levels" if many else "refine level"
        if e in (".@g", "getenchantgrade()"): return "grades" if many else "grade"
        if e == "BaseLevel": return "base levels" if many else "base level"
        if e == "JobLevel": return "job levels" if many else "job level"
        m = re.fullmatch(r"readparam\(b(\w+)\)", e)
        if m: return {"Str": "STR", "Agi": "AGI", "Vit": "VIT", "Int": "INT", "Dex": "DEX", "Luk": "LUK"}.get(m[1], m[1])
        m = re.fullmatch(r'getskilllv\("?(\w+)"?\)', e)
        if m: return f"{'levels' if many else 'level'} of [{self.skills.get(m[1], m[1])}]"
        return None

    def norm(self, expr, alias):
        """Expression with variables replaced by what they hold, and each term replaced by T0, T1..."""
        e = expr.replace(" ", "")
        for _ in range(2):
            for k, v in alias.items():
                e = re.sub(re.escape(k) + r"\b", v.replace(" ", "").replace("\\", "\\\\"), e)
        terms = []
        def sub(m):
            terms.append(m.group(0)); return f"T{len(terms) - 1}"
        return self.TERM.sub(sub, e), terms

    def value(self, expr, alias):
        """(5, '') for constants; (5, ' per refine level') for 5*.@r; None when too complex."""
        e, terms = self.norm(expr, alias)
        e = re.sub(r"^\((.*)\)$", r"\1", e)
        if re.fullmatch(r"-?\d+", e):
            return int(e), ""
        m = re.fullmatch(r"(?:(-?\d+)\*)?\(?T(\d)(?:/(\d+))?\)?(?:\*(-?\d+))?", e)    # a*(T/b), T/b, a*T, T
        if not m:
            m2 = re.fullmatch(r"\(?min\(T(\d),\d+\)\*?(-?\d+)?\)?", e)              # min(T,cap)*a
            if m2: return int(m2[2] or 1), f" per {self.term(terms[int(m2[1])])}"
            m3 = re.fullmatch(r"(-?\d+)\+T(\d)", e)                                     # 1+T
            if m3: return int(m3[1]), f" (+1 per {self.term(terms[int(m3[2])])})"
            m4 = re.fullmatch(r"(-?\d+)\+(-?\d+)\*\(?T(\d)(?:/(\d+))?\)?", e)           # a+b*T
            if m4:
                b = int(m4[4] or 1); t = terms[int(m4[3])]
                return int(m4[1]), f" (+{m4[2]} per {str(b) + ' ' if b > 1 else ''}{self.term(t, b)})"
            return None
        t = terms[int(m[2])]
        a = int(m[1] or m[4] or 1); b = int(m[3] or 1)
        return a, f" per {str(b) + ' ' if b > 1 else ''}{self.term(t, b)}"

    @staticmethod
    def fmt(v, unit, per=""):
        if unit == "s":
            v = v / 1000
            v = int(v) if v == int(v) else v
            unit = " sec"
        elif unit == "%%":
            v = v / 100
            v = int(v) if v == int(v) else v
            unit = "%"
        return f"{'+' if v >= 0 else ''}{v}{unit}{per}"

    # --- statements --------------------------------------------------------------------------------------------
    def stmt(self, s, alias):
        s = s.strip().rstrip(";").strip()
        m = re.fullmatch(r"bonus\s+(b\w+)(?:\s*,\s*(.+))?", s)
        if m:
            name, arg = m[1], m[2]
            if name in FLAGS and not arg: return FLAGS[name]
            if name == "bNoRegen": return "Disables natural " + ("HP" if arg.strip() == "1" else "SP") + " recovery."
            spec = STAT.get(name)
            if not spec or arg is None: return None
            v = self.value(arg, alias)
            if v is None: return f"{spec[0]} increases with {self.describe_expr(arg, alias)}."
            return f"{spec[0]} {self.fmt(v[0], spec[1], v[1])}"
        m = re.fullmatch(r"bonus2\s+(b\w+)\s*,\s*([^,]+)\s*,\s*(.+)", s)
        if m:
            name, tgt, arg = m[1], m[2], m[3]
            if name in ("bHPDrainRate", "bSPDrainRate"):
                parts = [p.strip() for p in (tgt + "," + arg).split(",")]
                if len(parts) == 2 and all(re.fullmatch(r"\d+", p) for p in parts):
                    return f"{int(parts[0]) / 10:g}% chance to absorb {parts[1]}% of damage dealt as {'HP' if 'HP' in name else 'SP'}"
                return None
            if name in ("bHPRegenRate", "bSPRegenRate"):
                return f"Regain {arg.strip()} {'HP' if 'HP' in name else 'SP'} every {int(tgt) / 1000:g} sec" if tgt.strip().isdigit() else None
            label = PAIR.get(name)
            if not label: return None
            v = self.value(arg, alias)
            unit = UNIT2.get(name, "%")
            if v is None: return f"{label.format(self.target(tgt))} increases with {self.describe_expr(arg, alias)}."
            return f"{label.format(self.target(tgt))} {self.fmt(v[0], unit, v[1])}"
        m = re.fullmatch(r'itemskill\s+"ITEM_ENCHANTARMS"\s*,\s*(\d+)', s)
        if m and 1 <= int(m[1]) <= 10:     # level = element + 1 (Elemental Converters, Cursed Water, Ghost Converter)
            ele = ["Neutral", "Water", "Earth", "Fire", "Wind", "Poison", "Holy", "Dark", "Ghost", "Undead"][int(m[1]) - 1]
            return f"Gives your weapon the {ele} property for 20 minutes"
        m = re.fullmatch(r'skill\s+"?(\w+)"?\s*,\s*(\d+)', s)
        if m:
            return f"Enables [{self.skills.get(m[1], m[1])}] Lv {m[2]}"
        m = re.fullmatch(r'bonus3\s+bAutoSpell\s*,\s*"?(\w+)"?\s*,\s*(\d+)\s*,\s*(\d+)', s)
        if m:
            return f"{int(m[3]) / 10:g}% chance to cast [{self.skills.get(m[1], m[1])}] Lv {m[2]} when attacking"
        m = re.fullmatch(r'bonus3\s+bAutoSpellWhenHit\s*,\s*"?(\w+)"?\s*,\s*(\d+)\s*,\s*(\d+)', s)
        if m:
            return f"{int(m[3]) / 10:g}% chance to cast [{self.skills.get(m[1], m[1])}] Lv {m[2]} when hit"
        m = re.fullmatch(r'bonus4\s+bAutoSpellOnSkill\s*,\s*"?(\w+)"?\s*,\s*"?(\w+)"?\s*,\s*(\d+)\s*,\s*(\d+)', s)
        if m:
            return f"{int(m[4]) / 10:g}% chance to cast [{self.skills.get(m[2], m[2])}] Lv {m[3]} when using [{self.skills.get(m[1], m[1])}]"
        if s.startswith("autobonus"):
            m = re.search(r"\"\{(.*?)\}\"\s*,\s*(\d+)\s*,\s*(\d+)", s)
            if m:
                inner = [self.stmt(x, alias) for x in m[1].split(";") if x.strip()]
                inner = [x for x in inner if x]
                if inner:
                    when = "when attacking" if s.startswith("autobonus ") or s.startswith("autobonus\t") else \
                        "when hit" if s.startswith("autobonus2") else "when using a skill"
                    return f"{int(m[2]) / 10:g}% chance {when}: {', '.join(inner)} for {int(m[3]) / 1000:g} sec"
        return None

    def describe_expr(self, e, alias):
        _, terms = self.norm(e, alias)
        words = list(dict.fromkeys(w for w in (self.term(t) for t in terms) if w))
        return " and ".join(words) if words else "conditions"

    def cond(self, c, alias):
        c = c.replace(" ", "")
        for k, v in alias.items():
            c = re.sub(re.escape(k) + r"\b", v.replace(" ", "").replace("\\", "\\\\"), c)
        m = re.fullmatch(r"\(?(\.@r|getrefine\(\))>=(\d+)\)?", c)
        if m: return f"Refine +{m[2]} or higher:"
        m = re.fullmatch(r"\(?(\.@g|getenchantgrade\(\))>=(ENCHANTGRADE_)?(\w+)\)?", c)
        if m: return f"Grade {m[3]} or higher:"
        m = re.fullmatch(r'\(?getskilllv\("?(\w+)"?\)(==|>=)(\d+)\)?', c)
        if m: return f"When [{self.skills.get(m[1], m[1])}] is level {m[3]}{' or higher' if m[2] == '>=' else ''}:"
        m = re.fullmatch(r"\(?BaseLevel>=(\d+)\)?", c)
        if m: return f"Base level {m[1]} or higher:"
        m = re.fullmatch(r"\(?readparam\(b(\w+)\)>=(\d+)\)?", c)
        if m: return f"With base {m[1].upper()} {m[2]} or higher:"
        m = re.fullmatch(r"\(?BaseJob==Job_(\w+)\)?", c)
        if m: return f"When the class is {m[1].replace('_', ' ')}:"
        m = re.fullmatch(r"\(?eaclass\(\)&EAJL_THIRD\)?", c)
        if m: return "For 3rd classes:"
        m = re.fullmatch(r"\(?isequipped\(([\d,]+)\)\)?", c)
        if m: return "When equipped together with items " + m[1].replace(",", ", ") + ":"
        return "Under certain conditions:"

    # --- whole script ------------------------------------------------------------------------------------------
    def effects(self, script):
        alias, lines, stack = {}, [], []
        src = re.sub(r"/\*.*?\*/|//[^\n]*", "", script or "", flags=re.S)
        # one token per statement / brace
        toks = re.findall(r'\s*(if\s*\((?:[^()]|\([^()]*(?:\([^()]*\))*[^()]*\))*\)|else\b|\{|\}|(?:"(?:\\.|[^"\\])*"|[^;{}"])+;)', src)
        # Conditions are shown flat: a header line ("Refine +7 or higher:") with its effects indented under it.
        # A nested condition gets its own header (they read as thresholds, like the official texts).
        pending, shown = None, None      # shown = header the last effect line was written under
        def emit(text, header):
            nonlocal shown
            if header != shown:
                if header: lines.append(header)
                shown = header
            lines.append(("  " if header else "") + text[0].upper() + text[1:])
        for t in toks:
            t = t.strip()
            if not t: continue
            if t.startswith("if"):
                pending = self.cond(t[2:].strip()[1:-1], alias); continue
            if t == "else":
                pending = "Otherwise:"; continue
            if t == "{":
                outer = next((h for h in reversed(stack) if h), None)
                stack.append(pending or outer)
                pending = None; continue
            if t == "}":
                if stack: stack.pop()
                continue
            m = re.fullmatch(r"(\.@\w+)\s*=\s*(.+);", t)
            if m:
                alias[m[1]] = m[2].strip(); continue
            text = self.stmt(t, alias)
            header = pending or next((h for h in reversed(stack) if h), None)
            pending = None          # an if without braces covers one statement
            if text:
                emit(text, header)
        # drop condition headers with nothing under them
        out = []
        for i, l in enumerate(lines):
            if l.rstrip().endswith(":"):
                d = len(l) - len(l.lstrip())
                nxt = lines[i + 1] if i + 1 < len(lines) else ""
                if not nxt or len(nxt) - len(nxt.lstrip()) <= d:
                    continue
            out.append(l)
        return out

    def describe(self, item):
        lines = self.effects(item.get("Script"))
        typ = item.get("Type", "Item")
        sub = item.get("SubType")
        locs = ", ".join(l.replace("_", " ") for l in (item.get("Locations") or {}))
        info = [f"Type: {sub or typ}"]
        if locs: info.append(f"Location: {locs}")
        if item.get("Attack"): info.append(f"Attack: {item['Attack']}")
        if item.get("MagicAttack"): info.append(f"MATK: {item['MagicAttack']}")
        if item.get("Defense"): info.append(f"Defense: {item['Defense']}")
        if item.get("WeaponLevel"): info.append(f"Weapon Level: {item['WeaponLevel']}")
        if item.get("ArmorLevel"): info.append(f"Armor Level: {item['ArmorLevel']}")
        info.append(f"Weight: {(item.get('Weight') or 0) // 10}")
        info.append(f"Required Level: {item.get('EquipLevelMin', 1)}")
        jobs = [j for j, ok in (item.get("Jobs") or {}).items() if ok]
        if jobs and "All" not in jobs: info.append("Jobs: " + ", ".join(j.replace("_", " ") for j in jobs))
        return (lines + [SEP] if lines else []) + info
