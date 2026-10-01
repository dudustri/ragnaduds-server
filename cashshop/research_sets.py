"""Read the gear sets out of the research files (builds-*.md), for building shop.yml.

  third_class_sets()  {class: {build: {"mid": [ids], "end": [ids]}}}   from builds-renewal-3rd-part1/2.md
  first_second_sets() [{"class": ..., "items": [ids]}]                  from builds-renewal-1st-2nd.md
Only the gear column is read (the first "(id)" of each slot row), not the recommended cards.
"""
import os, re, yaml

HERE = os.path.dirname(os.path.abspath(__file__))
SLOT = re.compile(r"(?i)^(weapon|alt(ernative)? weapon|shield|left hand|upper|top|mid|middle|lower|low|head|"
                  r"armou?r|garment|robe|shoes|footgear|acc|accessory|shadow)")


def third_class_sets():
    out = {}
    for f in ("builds-renewal-3rd-part1.md", "builds-renewal-3rd-part2.md"):
        cls = build = tier = None
        for line in open(os.path.join(HERE, f), encoding="utf-8"):
            m = re.match(r"^(#{2,5})\s+(.*)", line)
            if m:
                h, level = m.group(2).strip(), len(m.group(1))
                if re.search(r"(?i)end-?\s?game", h): tier = "end"
                elif re.search(r"(?i)\bmid\b", h): tier = "mid"
                elif level == 2: cls, build, tier = h, None, None
                else: build, tier = h, None
                continue
            if not tier or not line.startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 2 or not SLOT.match(re.sub(r"[*_]", "", cells[0])):
                continue
            ids = [int(x) for x in re.findall(r"\((\d{3,7})\)", cells[1].split("<br>")[0])]
            if ids:
                out.setdefault(cls, {}).setdefault(build or "-", {}).setdefault(tier, []).append(ids[0])
    return out


def first_second_sets():
    text = open(os.path.join(HERE, "builds-renewal-1st-2nd.md"), encoding="utf-8").read()
    return yaml.safe_load(re.findall(r"```yaml\n(.*?)```", text, re.S)[-1])["sets"]


if __name__ == "__main__":
    s3 = third_class_sets()
    print(len(s3), "3rd classes,", sum(len(b) for b in s3.values()), "builds;", len(first_second_sets()), "1st/2nd sets")
