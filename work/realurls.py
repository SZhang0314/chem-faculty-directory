# -*- coding: utf-8 -*-
import json
d=json.load(open(r"D:\USTC-AI\chem-faculty\work\faculty_all.json",encoding="utf-8"))
for s in ["北京大学","四川大学","复旦大学","南开大学","吉林大学"]:
    sp=[p for p in d["professors"] if p["school"]==s and p.get("profile_url")][:3]
    print("##",s)
    for p in sp:
        print("   ",p["name"],p["profile_url"])
