# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
out=[]
def show(name, path, enc):
    html=open(path,"rb").read().decode(enc,"replace")
    s=BeautifulSoup(html,"html.parser")
    txt=s.get_text("\n",strip=True)
    txt=re.sub(r"\n{2,}","\n",txt)
    out.append("="*30+" "+name+" (len %d)"%len(txt))
    out.append(txt[:3000])
for n,p,e in [("tsinghua",r"D:\USTC-AI\chem-faculty\work\probe_tsinghua.html","utf-8-sig"),
              ("sjtu",r"D:\USTC-AI\chem-faculty\work\probe_sjtu.html","utf-8"),
              ("zju",r"D:\USTC-AI\chem-faculty\work\probe_zju.html","utf-8"),
              ("ucas",r"D:\USTC-AI\chem-faculty\work\probe_ucas.html","utf-8")]:
    show(n,p,e)
open(r"D:\USTC-AI\chem-faculty\work\inspect1_out.txt","w",encoding="utf-8").write("\n".join(out))
print("ok")
