import json
d=json.load(open(r"D:\USTC-AI\chem-faculty\data\raw\tsinghua_fine.json",encoding="utf-8"))
out=[]
for p in d["professors"]:
    out.append(json.dumps({k:p.get(k) for k in ["name","title","research_directions","summary","email","homepage","confidence"]}, ensure_ascii=False, indent=1))
open(r"D:\USTC-AI\chem-faculty\work\testout.txt","w",encoding="utf-8").write("\n".join(out))
print("ok")
