import json, os, glob
from collections import Counter
d = r"D:\USTC-AI\chem-faculty\data\raw"
out=[]
allt=Counter()
for f in sorted(glob.glob(os.path.join(d,"*.json"))):
    j=json.load(open(f,encoding="utf-8-sig"))
    for p in j.get("professors",[]):
        allt[(p.get("title") or "(empty)")]+=1
for t,c in allt.most_common(200):
    out.append(f"{c}\t{t}")
open(r"D:\USTC-AI\chem-faculty\work\all_titles.txt","w",encoding="utf-8").write("\n".join(out))
print("written", len(allt))
