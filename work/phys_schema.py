import json, glob, os
# find the physics data json
for root,_,files in os.walk(r"D:\USTC-AI\physics-faculty-directory"):
    for f in files:
        if f.endswith(".json"):
            p=os.path.join(root,f)
            try:
                j=json.load(open(p,encoding="utf-8-sig"))
                if isinstance(j,dict) and "professors" in j:
                    print(p, "| keys:", list(j.keys()), "| nprof", len(j["professors"]))
                    if j["professors"]:
                        print("  sample:", json.dumps(j["professors"][0], ensure_ascii=False)[:800])
            except Exception as e:
                pass
