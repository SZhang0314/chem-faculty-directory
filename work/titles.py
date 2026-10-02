import json, os, glob
from collections import Counter
d = r"D:\USTC-AI\chem-faculty\data\raw"
for f in sorted(glob.glob(os.path.join(d,"*.json"))):
    j=json.load(open(f,encoding="utf-8-sig"))
    ps=j.get("professors",[])
    tc=Counter((p.get("title") or "(empty)") for p in ps)
    print("==", os.path.basename(f), len(ps))
    for t,c in tc.most_common(20):
        print(f"    {c:5d}  {t}")
