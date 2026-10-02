import re, glob
for f in [r"D:\USTC-AI\physics-faculty-directory\index.html",
          r"D:\USTC-AI\cas-physics-directory\index.html",
          r"D:\USTC-AI\fudan-physics-directory\index.html",
          r"D:\USTC-AI\nju-physics-directory\index.html",
          r"D:\USTC-AI\pku-physics-directory\index.html",
          r"D:\USTC-AI\sjtu-physics-directory\index.html",
          r"D:\USTC-AI\ucas-physics-directory\index.html"]:
    h=open(f,encoding="utf-8",errors="replace").read()
    m=re.search(r"<title>(.*?)</title>", h, re.S)
    print(f.split("\\")[-2], "|", (m.group(1).strip() if m else "?")[:80], "| len", len(h))
