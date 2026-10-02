import json, os, glob
d = r"D:\USTC-AI\chem-faculty\data\raw"
total = 0
for f in sorted(glob.glob(os.path.join(d, "*.json"))):
    try:
        j = json.load(open(f, encoding="utf-8-sig"))
        ps = j.get("professors", [])
        total += len(ps)
        named = sum(1 for p in ps if p.get("name"))
        withurl = sum(1 for p in ps if p.get("profile_url"))
        depts = sorted({p.get("department","") for p in ps})
        print(f"{os.path.basename(f):16s} {len(ps):5d}  named={named:5d} url={withurl:5d}  schools={j.get('school')}")
        print(f"    depts: {', '.join(depts[:12])}")
    except Exception as e:
        print(f"{os.path.basename(f):16s} ERROR {e}")
print("TOTAL", total)
