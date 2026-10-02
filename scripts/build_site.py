#!/usr/bin/env python3
"""Build a single self-contained index.html from faculty.json.

Inlines the data and the template's CSS/JS so the page needs no server and
no external assets — it works when opened by double-click AND on GitHub Pages.

Usage:
    python scripts/build_site.py --data data/faculty.json --out .
    python scripts/build_site.py --data data/faculty.json --out . --title "MIT CS Faculty"
"""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_TEMPLATE = HERE.parent / "assets" / "site_template.html"


def load_json(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def main():
    ap = argparse.ArgumentParser(description="Build self-contained faculty directory page")
    ap.add_argument("--data", default="data/faculty.json", help="path to faculty.json")
    ap.add_argument("--out", default=".", help="output directory for index.html")
    ap.add_argument("--template", default=str(DEFAULT_TEMPLATE), help="HTML template path")
    ap.add_argument("--title", default=None, help="override page title")
    args = ap.parse_args()

    data_path = Path(args.data)
    if not data_path.exists():
        print(f"ERROR: data file not found: {data_path}", file=sys.stderr)
        return 1

    template_path = Path(args.template)
    if not template_path.exists():
        print(f"ERROR: template not found: {template_path}", file=sys.stderr)
        return 1

    data = load_json(data_path)
    profs = data.get("professors", []) or []

    tmpl = template_path.read_text(encoding="utf-8")

    query = data.get("query") or {}
    schools = query.get("schools") or []
    default_title = "Faculty & Researcher Directory"
    if schools:
        default_title = f"{', '.join(schools)} — Faculty Directory"
    title = args.title or default_title

    schools_present = sorted({p.get("school", "") for p in profs if p.get("school")})
    depts_present = sorted({p.get("department", "") for p in profs if p.get("department")})
    generated = data.get("generated_at") or datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Escape for safe embedding inside <script>: prevent </script> breakout.
    payload = json.dumps({"professors": profs}, ensure_ascii=False)
    payload = payload.replace("</", "<\\/")

    html = (tmpl
            .replace("__TITLE__", esc(title))
            .replace("__DATA_JSON__", payload)
            .replace("__SCHOOL_OPTIONS__", json.dumps(schools_present, ensure_ascii=False))
            .replace("__DEPT_OPTIONS__", json.dumps(depts_present, ensure_ascii=False))
            .replace("__GENERATED__", esc(generated))
            .replace("__COUNT__", str(len(profs))))

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "index.html"
    out_file.write_text(html, encoding="utf-8")

    # .nojekyll so GitHub Pages serves everything as-is.
    (out_dir / ".nojekyll").write_text("", encoding="utf-8")

    print(f"Wrote {out_file} ({len(profs)} professors, {out_file.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
