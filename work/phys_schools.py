import json
j=json.load(open(r"D:\USTC-AI\physics-faculty-directory\data\faculty.json",encoding="utf-8-sig"))
print(json.dumps(j.get("schools"), ensure_ascii=False, indent=1))
print("generated_at", j.get("generated_at"))
# count is_academician
ps=j["professors"]
print("academicians", sum(1 for p in ps if p.get("is_academician")))
# distinct school_key
print(sorted({p.get("school_key") for p in ps}))
