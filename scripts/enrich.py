# -*- coding: utf-8 -*-
"""Enrich chemistry faculty profiles across 11 schools.

Fetches each profile page, caches raw HTML, extracts research directions,
summary, publications, email and homepage with per-school heuristics.
Writes <school>_fine.json.
"""
import json, os, re, sys, time, random
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings()

BASE = r"D:\USTC-AI\chem-faculty"
RAW = os.path.join(BASE, "data", "raw")
CACHE = os.path.join(BASE, "work", "cache")
os.makedirs(CACHE, exist_ok=True)

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
SESS = requests.Session()
SESS.headers.update({"User-Agent": UA, "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"})

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
BAD_EMAIL_DOM = ("example.", "sentry", "w3.org", "noreply")

DEPT_LABELS = ["研究方向", "主要研究方向", "研究领域", "研究兴趣", "科研方向",
               "主要研究领域", "招生方向", "研究方向和内容"]
PUB_LABELS = ["代表性论文专著", "代表性论文", "代表性成果", "代表性论著", "主要论著",
              "学术成果", "科研成果与代表作", "近期代表性论文", "发表论文", "著作论文",
              "出版信息", "主要 achievements", "代表性研究成果"]
BIO_LABELS = ["个人简介", "研究概况", "简历", "学术简历", "个人履历"]
STOP_LABELS = ["教育背景", "工作经历", "工作履历", "学术兼职", "荣誉", "奖励", "获奖",
               "科研项目", "教学工作", "教授课程", "人才培养", "人才需求", "联系方式",
               "办公地点", "办公电话", "电子邮箱", "个人主页", "招生信息", "团队成员",
               "指导学生", "专利", "基本信息", "学术任职", "授课情况", "荣誉奖励",
               "教育及科研经历", "荣誉和奖励", "工作内容", "主要岗位职责", "社会服务"]


def cache_path(school, url):
    import hashlib
    h = hashlib.md5(url.encode("utf-8")).hexdigest()[:16]
    return os.path.join(CACHE, f"{school}_{h}.html")


def fetch(school, url, verify=True):
    cp = cache_path(school, url)
    if os.path.exists(cp) and os.path.getsize(cp) > 200:
        return open(cp, "rb").read()
    for attempt in range(3):
        try:
            r = SESS.get(url, timeout=30, verify=verify)
            if r.status_code == 200 and len(r.content) > 200:
                open(cp, "wb").write(r.content)
                return r.content
            if r.status_code == 404:
                open(cp, "wb").write(b"")  # mark dead
                return None
        except Exception:
            time.sleep(0.5 + random.random())
    try:
        open(cp, "wb").write(b"")
    except Exception:
        pass
    return None


def to_soup(raw):
    if not raw:
        return None
    for enc in ("utf-8-sig", "utf-8", "gb18030", "gbk"):
        try:
            txt = raw.decode(enc)
            break
        except Exception:
            continue
    else:
        txt = raw.decode("utf-8", "replace")
    s = BeautifulSoup(txt, "html.parser")
    for t in s(["script", "style", "nav", "footer"]):
        t.decompose()
    return s


def clean(t):
    t = re.sub(r"[\u00a0\u3000]", " ", t)
    t = re.sub(r"[ \t]+", " ", t)
    return t.strip()


def lines_of(soup):
    txt = soup.get_text("\n", strip=True)
    out = []
    for ln in txt.split("\n"):
        ln = clean(ln)
        if ln:
            out.append(ln)
    return out


def extract_email(soup, lines):
    # prefer mailto links
    for a in soup.find_all("a", href=True):
        if a["href"].lower().startswith("mailto:"):
            e = a["href"][7:].split("?")[0].strip()
            if EMAIL_RE.fullmatch(e) and not any(b in e for b in BAD_EMAIL_DOM):
                return e.lower()
    for m in EMAIL_RE.finditer("\n".join(lines)):
        e = m.group(0)
        if not any(b in e.lower() for b in BAD_EMAIL_DOM):
            return e.lower()
    return ""


PUBLISHER_DOMS = ("nature.com", "science.org", "acs.org", "wiley.com", "springer",
                  "sciencedirect", "rsc.org", "webofscience", "clarivate",
                  "doi.org", "pubs.acs", "onlinelibrary", "ncbi.nlm", "pubmed")
def extract_homepage(soup, profile_url):
    from urllib.parse import urlparse
    phost = urlparse(profile_url).netloc
    skip = ("chem.", "people.ucas", "scce.", "person.zju", "polymer.",
            "chemistry.", "scu.edu", "jlu.edu", "nankai.edu", "pku.edu",
            "fudan.edu", "nju.edu", "zju.edu", "sjtu.edu", "ustc.edu",
            "ucas.ac", "tsinghua.edu", "iccas.ac", "cas.cn", "weibo",
            "beian", "miit", "x-mol.com", "baidu", "google", "scholar",
            "orcid.org", "researchgate", "linkedin", "zhihu")
    cands = []
    # look for anchors preceded by a homepage-ish label
    for a in soup.find_all("a", href=True):
        h = a["href"].strip()
        if not h.startswith("http"):
            continue
        dom = urlparse(h).netloc
        if dom == phost:
            continue
        if any(s in dom for s in skip) or any(p in dom for p in PUBLISHER_DOMS):
            continue
        # group/lab pages usually
        if any(k in h.lower() for k in ("group", "lab", "课题组")) or "lab." in dom \
           or dom.startswith("www.") and dom.count(".") <= 2:
            cands.insert(0, h)
        else:
            cands.append(h)
    return cands[0] if cands else ""


# Inline section markers that often trail the research-direction text on same line
INLINE_CUT = ["奖励与荣誉", "奖励和荣誉", "荣誉奖励", "主讲课程", "授课情况", "教学工作",
              "教育背景", "工作经历", "工作履历", "学术兼职", "科研项目", "代表性论文",
              "代表性论著", "学术成果", "代表性成果", "发表论文", "人才培养", "招生信息",
              "荣誉和奖励", "教育及科研经历", "学术任职", "个人简介", "简历", "个人信息",
              "联系方式", "团队成员", "指导学生", "课题组", "专利成果", "获奖情况",
              "研究兴趣包括", "2000年", "2001年", "2002年", "2003年", "2004年", "2005年"]

def cut_inline(txt):
    for m in INLINE_CUT:
        idx = txt.find(m)
        if idx > 0:
            # require the marker to look like a label boundary (preceded by space/punct)
            txt = txt[:idx]
    return txt.strip()


def section_text_after(lines, labels, stop_labels, max_lines=8, max_chars=400):
    """Find first line equal/starting with a label, return following lines until stop."""
    for i, ln in enumerate(lines):
        for lab in labels:
            base = ln.replace("：", "").replace(":", "").strip()
            if base == lab or ln.startswith(lab + "：") or ln.startswith(lab + ":"):
                val = ln[len(lab):].lstrip("：: ").strip()
                buf = [val] if val else []
                j = i + 1
                while j < len(lines) and len(buf) < max_lines:
                    nxt = lines[j]
                    base_n = nxt.replace("：", "").replace(":", "").strip()
                    if any(base_n == s or nxt.startswith(s + "：") or nxt.startswith(s + ":")
                           for s in stop_labels):
                        break
                    if any(nxt.startswith(s) for s in PUB_LABELS + DEPT_LABELS) and buf:
                        break
                    buf.append(nxt)
                    j += 1
                txt = " ".join(buf)
                txt = re.sub(r"\s+", " ", txt).strip()
                txt = cut_inline(txt)
                if txt:
                    return txt[:max_chars]
    return ""


def parse_pubs(lines, max_pubs=5):
    """Collect numbered publication lines after a pub label."""
    pubs = []
    start = -1
    for i, ln in enumerate(lines):
        b = ln.replace("：", "").replace(":", "").strip()
        for lab in PUB_LABELS:
            if b == lab or ln.startswith(lab + "：") or ln.startswith(lab + ":"):
                start = i
                break
        if start >= 0:
            break
    if start < 0:
        return pubs
    title_re = re.compile(r"^\s*[（(]?\d{1,2}[)）.]?\s+(.+)$")
    buf = []
    i = start + 1
    while i < len(lines) and len(pubs) < max_pubs * 2:
        ln = lines[i]
        base = ln.replace("：", "").replace(":", "").strip()
        if any(base == s for s in STOP_LABELS):
            break
        m = title_re.match(ln)
        if m:
            if buf:
                pubs.append(" ".join(buf))
            buf = [m.group(1)]
        elif buf:
            buf.append(ln)
        i += 1
    if buf:
        pubs.append(" ".join(buf))
    # trim and cap
    res = []
    for p in pubs:
        p = re.sub(r"\s+", " ", p).strip()
        if len(p) < 8:
            continue
        res.append(p[:300])
        if len(res) >= max_pubs:
            break
    return res


TITLE_WORDS = ["教授", "副教授", "讲师", "研究员", "副研究员", "助理教授", "院士",
               "博士生导师", "博导", "特聘", "准聘", "长聘", "青年研究员", "助理研究员",
               "准聘副教授", "特任", "讲席"]
def clean_title(raw, name=""):
    t = (raw or "").strip()
    if not t:
        return ""
    if name:
        t = t.replace(name, " ").strip(" ,，、;；:：")
    # keep only the portion likely to be a title
    # cut at first occurrence of a sentence-ish char
    for sep in ["，籍贯", "。", "；", " 博士，", "，博士"]:
        if sep in t:
            t = t.split(sep)[0]
    t = re.sub(r"^(技术职称|职称)[：:]\s*", "", t)
    t = re.sub(r"\s+", " ", t).strip(" ,，、;；:：")
    # if it's very long and contains a title word, trim around it
    if len(t) > 30:
        for w in TITLE_WORDS:
            idx = t.find(w)
            if idx > 0:
                t = t[max(0, idx - 6):]
                break
        t = t[:30]
    return t


def parse_pubs_struct(pub_strings):
    out = []
    for s in pub_strings:
        m = re.search(r"(19|20)\d{2}", s)
        year = int(m.group(0)) if m else None
        venue = ""
        for v in ("Nature", "Science", "J. Am. Chem. Soc", "Angew", "Chem. Rev",
                  "Chem. Soc. Rev", "Nat. Commun", "PNAS", "Adv. Mater",
                  "J. Chem. Phys", "Chem. Sci", "ACS Nano", "Nano Lett",
                  "Inorg. Chem", "Chem. Commun", "Macromolecules"):
            if v.lower() in s.lower():
                venue = v
                break
        out.append({"title": s, "venue": venue, "year": year})
    return out
