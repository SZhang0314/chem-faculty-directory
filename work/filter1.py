import json, os, glob, re
d = r"D:\USTC-AI\chem-faculty\data\raw"
EXCLUDE_PAT = re.compile(r"行政|职员|工勤|退休|离退休|实验技术|实验员|工程师|博士后|科研助理|管理|教辅|辅导员|学报编辑|后勤")
rows=[]
for f in sorted(glob.glob(os.path.join(d,"*.json"))):
    j=json.load(open(f,encoding="utf-8-sig"))
    for p in j.get("professors",[]):
        p["_file"]=os.path.basename(f)
        rows.append(p)
print("raw", len(rows))
# UCAS filter: keep only 专任教师 (title contains 专任教师) 
ucas=[r for r in rows if r["_file"]=="ucas.json"]
keep_ucas=[r for r in ucas if r.get("title")=="专任教师" or "专任教师" in (r.get("title") or "")]
print("ucas total", len(ucas), "keep专任教师", len(keep_ucas))
