import re
h=open(r"D:\USTC-AI\chem-faculty\index.html",encoding="utf-8").read()
print("has TITLE:", "中国十一校化学方向教师目录" in h)
print("data embedded:", "__DATA_JSON__" not in h)
print("has search input:", 'type="search"' in h or 'placeholder' in h.lower())
print("count occurrences of 清华大学:", h.count("清华大学"))
print("professors key:", h.count('"professors"'))
