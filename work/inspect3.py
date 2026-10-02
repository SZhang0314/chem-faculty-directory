# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
out=[]
def show(name, path, enc, limit=2200):
    html=open(path,"rb").read().decode(enc,"replace")
    s=BeautifulSoup(html,"html.parser")
    for t in s(["script","style","nav"]): t.decompose()
    txt=s.get_text("\n",strip=True)
    txt=re.sub(r"[ \t\u00a0]+"," ",txt)
    txt=re.sub(r"\n{2,}","\n",txt)
    out.append("="*30+" "+name+" (len %d)"%len(txt))
    out.append(txt[:limit])
for n,p,e in [("nankai",r"D:\USTC-AI\chem-faculty\work\probe_nankai.html","utf-8"),
              ("jilin",r"D:\USTC-AI\chem-faculty\work\probe_jilin.html","utf-8-sig"),
              ("pku",r"D:\USTC-AI\chem-faculty\work\probe_pku.html","utf-8"),
              ("fudan_prof",r"D:\USTC-AI\chem-faculty\work\probe_fudan_prof.html","utf-8-sig")]:
    show(n,p,e)
open(r"D:\USTC-AI\chem-faculty\work\inspect3_out.txt","w",encoding="utf-8").write("\n".join(out))
print("ok")
