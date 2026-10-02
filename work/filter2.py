# -*- coding: utf-8 -*-
import json, os, glob, re
d = r"D:\USTC-AI\chem-faculty\data\raw"

# Drop-list: contain these substrings -> admin/staff/retired/non-teaching
DROP = ["职员","工勤","初级","实验师","实验技术","实验员","管理服务",
        "其他教职工","科研助理","博士后","学报编辑","教辅","辅导员",
        "技术职称","工程师（","高级工程师","教授级高工","工程师)",
        "(工程师"]
# But keep anyone whose title ALSO has a clear faculty rank
FACULTY = ["教授","研究员","讲师","院士","助理教授","专任教师","博导"]

def is_faculty(title):
    t = (title or "").strip()
    if not t: return True   # empty -> keep (couldn't classify; enrich will tell)
    for dw in DROP:
        if dw in t:
            # keep if it also has a faculty rank besides engineer
            if any(fw in t for fw in ["教授","研究员","讲师","院士"]):
                return True
            return False
    return True

rows=[]
for f in sorted(glob.glob(os.path.join(d,"*.json"))):
    j=json.load(open(f,encoding="utf-8-sig"))
    school=j.get("school")
    for p in j.get("professors",[]):
        p["school"]=school
        p["_src"]=os.path.basename(f)
        rows.append(p)

# UCAS: keep only 专任教师
uc=[r for r in rows if r["_src"]=="ucas.json"]
keep_uc=[r for r in uc if "专任教师" in (r.get("title") or "")]
others=[r for r in rows if r["_src"]!="ucas.json"]
after_ucas = others + keep_uc
print("after UCAS filter:", len(after_ucas))

kept=[r for r in after_ucas if is_faculty(r.get("title"))]
dropped=[r for r in after_ucas if not is_faculty(r.get("title"))]
print("kept (teaching faculty):", len(kept))
print("dropped (admin/staff/retired/postdoc):", len(dropped))

from collections import Counter
print("--- dropped sample titles ---")
for t,c in Counter(r.get("title") for r in dropped).most_common(40):
    print(f"  {c}  {t}")
json.dump({"professors":kept}, open(r"D:\USTC-AI\chem-faculty\work\faculty_all.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
# school counts
print("--- kept per school ---")
for s,c in Counter(r["school"] for r in kept).most_common():
    print(f"  {c:5d}  {s}")
