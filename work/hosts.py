import json, os
from collections import Counter
d=json.load(open(r"D:\USTC-AI\chem-faculty\work\faculty_all.json",encoding="utf-8"))
ps=d["professors"]
# check profile_url patterns per school
import urllib.parse
for s in sorted(set(p["school"] for p in ps)):
    sp=[p for p in ps if p["school"]==s]
    hosts=Counter(urllib.parse.urlparse(p.get("profile_url") or "").netloc for p in sp)
    print(s, len(sp))
    for h,c in hosts.most_common(6):
        print("     ", c, h)
