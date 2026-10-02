# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re, json, os
out=[]
def show(name, path, enc, limit=2500):
    html=open(path,"rb").read().decode(enc,"replace")
    s=BeautifulSoup(html,"html.parser")
    txt=s.get_text("\n",strip=True)
    txt=re.sub(r"[ \t]+"," ",txt)
    txt=re.sub(r"\n{2,}","\n",txt)
    out.append("="*30+" "+name+" (len %d)"%len(txt))
    out.append(txt[:limit])
for n,p,e in [("ustc_chem_list",r"D:\USTC-AI\chem-faculty\work\probe_ustc_chem.html","utf-8"),
              ("ustc_dcp_list",r"D:\USTC-AI\chem-faculty\work\probe_ustc_dcp.html","utf-8")]:
    show(n,p,e)
open(r"D:\USTC-AI\chem-faculty\work\inspect2_out.txt","w",encoding="utf-8").write("\n".join(out))
print("ok")
