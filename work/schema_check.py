import json
j=json.load(open(r"D:\USTC-AI\chem-faculty\data\faculty.json",encoding="utf-8-sig"))
print("keys", list(j.keys()))
print("schools")
for s in j["schools"]:
    print("  ", s)
p=j["professors"][0]
print("sample rec keys:", list(p.keys()))
print("sample:", json.dumps({k:p[k] for k in ["name","name_local","school_key","school_en","title","is_academician","confidence"]}, ensure_ascii=False))
# missing fields?
miss=[k for k in ["name","school","school_key","school_en","department","title","research_directions","summary","publications","homepage","profile_url","email","confidence","verified","is_academician"] if k not in p]
print("missing in sample:", miss)
