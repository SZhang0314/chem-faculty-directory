# -*- coding: utf-8 -*-
"""Consolidate all <school>_fine.json into the final data/faculty.json."""
import json, os, glob, re
from datetime import datetime, timezone

BASE = r"D:\USTC-AI\chem-faculty"
RAW = os.path.join(BASE, "data", "raw")
OUT = os.path.join(BASE, "data", "faculty.json")

SCHOOL_ORDER = ["清华大学", "北京大学", "中国科学院大学", "浙江大学", "上海交通大学",
                "复旦大学", "南京大学", "南开大学", "吉林大学", "中国科学技术大学",
                "四川大学"]

def slugify(name):
    # keep Chinese chars; replace spaces/punct
    s = re.sub(r"\s+", "-", name.strip())
    s = re.sub(r"[（）()，,、。·/\\]+", "-", s)
    return s.strip("-")

profs = []
seen = set()
for f in sorted(glob.glob(os.path.join(RAW, "*_fine.json"))):
    j = json.load(open(f, encoding="utf-8-sig"))
    for p in j.get("professors", []):
        name = (p.get("name") or "").strip()
        if not name:
            continue
        url = (p.get("profile_url") or "").strip()
        key = (j.get("school", ""), name, url)
        if key in seen:
            continue
        seen.add(key)
        home = (p.get("homepage") or "").strip()
        if home and not re.match(r"^https?://[A-Za-z0-9]", home):
            home = ""
        rec = {
            "id": "",
            "name": name,
            "name_en": (p.get("name_en") or "").strip(),
            "school": j.get("school", p.get("school", "")),
            "department": (p.get("department") or "").strip(),
            "title": (p.get("title") or "").strip(),
            "subject": "化学",
            "research_area": (p.get("research_area") or "").strip(),
            "research_directions": [x for x in (p.get("research_directions") or []) if x][:6],
            "focus_areas": p.get("focus_areas") or [],
            "summary": (p.get("summary") or "").strip()[:400],
            "publications": p.get("publications") or [],
            "homepage": home,
            "profile_url": url,
            "email": (p.get("email") or "").strip(),
            "sources": p.get("sources") or ([url] if url else []),
            "confidence": p.get("confidence", "coarse"),
            "verified": bool(p.get("verified", False)),
        }
        profs.append(rec)

# assign stable ASCII ids: <schoolcode>-<index>
SCHOOL_CODE = {
    "清华大学": "tsinghua", "北京大学": "pku", "中国科学院大学": "ucas",
    "浙江大学": "zju", "上海交通大学": "sjtu", "复旦大学": "fudan",
    "南京大学": "nju", "南开大学": "nankai", "吉林大学": "jilin",
    "中国科学技术大学": "ustc", "四川大学": "scu",
}
counters = {}
for r in profs:
    code = SCHOOL_CODE.get(r["school"], "school")
    counters[code] = counters.get(code, 0) + 1
    r["id"] = f"{code}-{counters[code]:04d}"

# sort by school order then name
def sk(r):
    si = SCHOOL_ORDER.index(r["school"]) if r["school"] in SCHOOL_ORDER else 99
    return (si, r["name"])
profs.sort(key=sk)

data = {
    "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "query": {
        "schools": SCHOOL_ORDER,
        "departments": ["化学学院/化学系", "高分子", "材料", "化工", "化学生物学"],
        "topics": ["化学"],
    },
    "professors": profs,
}
json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

fine = sum(1 for r in profs if r["confidence"] == "fine")
nemail = sum(1 for r in profs if r["email"])
nhome = sum(1 for r in profs if r["homepage"])
npub = sum(1 for r in profs if r["publications"])
nrd = sum(1 for r in profs if r["research_directions"])
print(f"TOTAL {len(profs)}  fine={fine}  email={nemail}  homepage={nhome}  pubs={npub}  research={nrd}")
for s in SCHOOL_ORDER:
    sp = [r for r in profs if r["school"] == s]
    print(f"  {len(sp):5d}  {s}")
