# -*- coding: utf-8 -*-
import sys, json, os, re
sys.path.insert(0, r"D:\USTC-AI\chem-faculty\work")
from enrich import *

schools = {
 "tsinghua": ("清华大学", True),
 "ustc": ("中国科学技术大学", True),
 "ucas": ("中国科学院大学", True),
 "zju": ("浙江大学", True),
 "sjtu": ("上海交通大学", True),
 "pku": ("北京大学", False),   # ssl
 "nankai": ("南开大学", True),
 "jilin": ("吉林大学", True),
 "scu": ("四川大学", True),
 "fudan": ("复旦大学", True),
 "nju": ("南京大学", True),
}

def enrich_school(key, limit=None):
    src = json.load(open(os.path.join(RAW, key+".json"), encoding="utf-8-sig"))
    name = schools[key][0]
    verify = schools[key][1]
    profs = src.get("professors", [])
    # UCAS: keep 专任教师 only (already filtered in faculty_all, but reapply)
    if key == "ucas":
        profs = [p for p in profs if "专任教师" in (p.get("title") or "")]
    if limit:
        profs = profs[:limit]
    out = []
    nfine = 0
    for idx, p in enumerate(profs):
        url = p.get("profile_url") or ""
        rec = dict(p)
        rec["school"] = name
        rec.setdefault("name_en", "")
        rec.setdefault("title", "")
        rec.setdefault("research_area", "")
        rec.setdefault("department", rec.get("department") or "")
        rec["research_directions"] = []
        rec["focus_areas"] = []
        rec["summary"] = ""
        rec["publications"] = []
        rec["homepage"] = ""
        rec["email"] = ""
        rec["sources"] = [url] if url else []
        rec["confidence"] = "coarse"
        rec["verified"] = False
        if url:
            raw = fetch(key, url, verify=verify)
            soup = to_soup(raw)
            if soup:
                lines = lines_of(soup)
                if len("\n".join(lines)) > 60:
                    email = extract_email(soup, lines)
                    home = extract_homepage(soup, url)
                    dept = section_text_after(lines, DEPT_LABELS, STOP_LABELS)
                    bio = section_text_after(lines, BIO_LABELS, STOP_LABELS)
                    pub_strings = parse_pubs(lines)
                    pub_struct = parse_pubs_struct(pub_strings)
                    if email: rec["email"] = email
                    if home: rec["homepage"] = home
                    if dept: rec["research_directions"] = [x.strip() for x in re.split(r"[;；。\n]", dept) if x.strip()][:6]
                    if bio: rec["summary"] = bio[:300]
                    if pub_struct: rec["publications"] = pub_struct
                    ct = clean_title(rec.get("title"), rec.get("name", ""))
                    if ct: rec["title"] = ct
                    if dept or bio or pub_struct or email:
                        rec["confidence"] = "fine"
                        rec["verified"] = True
                        nfine += 1
        out.append(rec)
        if (idx+1) % 20 == 0:
            print(f"  {key}: {idx+1}/{len(profs)} fine={nfine}", flush=True)
    json.dump({"school": name, "professors": out},
              open(os.path.join(RAW, key+"_fine.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"DONE {key}: {len(out)} records, {nfine} fine", flush=True)

if __name__ == "__main__":
    import sys as _sys
    only = _sys.argv[1] if len(_sys.argv) > 1 else None
    lim = int(_sys.argv[2]) if len(_sys.argv) > 2 else None
    keys = [only] if only else list(schools.keys())
    for k in keys:
        enrich_school(k, limit=lim)
