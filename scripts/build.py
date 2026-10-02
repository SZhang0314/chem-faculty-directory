# -*- coding: utf-8 -*-
"""Build the chemistry faculty aggregate page from data/faculty.json + template.html.

Outputs a single self-contained index.html (dark theme, school tabs, filters).
"""
import json, os, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "faculty.json")
TEMPLATE = os.path.join(ROOT, "template.html")
OUT = os.path.join(ROOT, "index.html")


def main():
    payload = json.load(open(DATA, encoding="utf-8-sig"))
    # refresh generated_at
    payload["generated_at"] = datetime.datetime.now().strftime("%Y-%m-%d")
    # refresh school counts from professors
    from collections import Counter
    cnt = Counter(p.get("school") for p in payload.get("professors", []))
    for s in payload.get("schools", []):
        s["count"] = cnt.get(s["name"], 0)

    data_json = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
    template = open(TEMPLATE, encoding="utf-8").read()
    html_out = template.replace("/*__DATA__*/", data_json)
    open(OUT, "w", encoding="utf-8").write(html_out)
    print(f"Wrote {OUT} ({len(payload.get('professors', []))} professors, "
          f"{os.path.getsize(OUT):,} bytes)")


if __name__ == "__main__":
    main()
