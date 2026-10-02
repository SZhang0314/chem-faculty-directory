import json
d=json.load(open(r"D:\USTC-AI\chem-faculty\data\faculty.json",encoding="utf-8-sig"))
ps=d["professors"]
print("total", len(ps))
print("fine", sum(1 for p in ps if p["confidence"]=="fine"))
print("with email", sum(1 for p in ps if p["email"]))
print("with research_directions", sum(1 for p in ps if p["research_directions"]))
print("with publications", sum(1 for p in ps if p["publications"]))
print("with homepage", sum(1 for p in ps if p["homepage"]))
