#!/usr/bin/env python3
"""Validate a faculty.json produced by the search_prof skill.

Checks schema, required fields, id uniqueness, URL sanity, and flags
records that look suspicious (duplicate names, missing sources, etc.).
Exit code 0 = no errors (warnings allowed), 1 = errors found.
"""
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

REQUIRED = ["id", "name", "school"]
CONFIDENCE = {"coarse", "fine"}
URL_RE = re.compile(r"^https?://", re.I)


def load(path):
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            return json.load(f), None
    except FileNotFoundError:
        return None, f"file not found: {path}"
    except json.JSONDecodeError as e:
        return None, f"invalid JSON: {e}"


def is_url(v):
    return isinstance(v, str) and bool(URL_RE.match(v.strip()))


def validate(data):
    errors, warnings = [], []
    profs = data.get("professors")
    if not isinstance(profs, list):
        return ["top-level 'professors' must be a list"], warnings

    seen_ids = set()
    name_school = Counter()

    for i, p in enumerate(profs):
        where = f"professors[{i}]"
        if not isinstance(p, dict):
            errors.append(f"{where}: not an object")
            continue

        for field in REQUIRED:
            if not p.get(field):
                errors.append(f"{where}: missing required '{field}'")

        pid = p.get("id")
        if pid:
            if pid in seen_ids:
                errors.append(f"{where}: duplicate id '{pid}'")
            seen_ids.add(pid)
            if not re.match(r"^[a-z0-9][a-z0-9\-]*$", str(pid)):
                warnings.append(f"{where}: id '{pid}' is not slug-like (lowercase/digits/hyphens)")

        name, school = p.get("name"), p.get("school")
        if name and school:
            name_school[(str(name).strip().lower(), str(school).strip().lower())] += 1

        conf = p.get("confidence")
        if conf is None:
            warnings.append(f"{where}: missing 'confidence' (expected 'coarse' or 'fine')")
        elif conf not in CONFIDENCE:
            errors.append(f"{where}: confidence '{conf}' not in {sorted(CONFIDENCE)}")

        for field in ("homepage", "profile_url", "scholar_url"):
            if p.get(field) and not is_url(p[field]):
                errors.append(f"{where}: {field} is not an http(s) URL: {p[field]!r}")

        for field in ("research_directions", "focus_areas", "publications", "sources"):
            if field in p and p[field] is not None and not isinstance(p[field], list):
                errors.append(f"{where}: '{field}' must be a list")

        if not p.get("sources"):
            warnings.append(f"{where} ({name}): no 'sources' — every record should cite evidence URLs")

        if conf == "fine":
            if not p.get("research_directions"):
                warnings.append(f"{where} ({name}): fine record without research_directions")
            if not p.get("homepage"):
                warnings.append(f"{where} ({name}): fine record without homepage")

        for j, pub in enumerate(p.get("publications") or []):
            if not isinstance(pub, dict) or not pub.get("title"):
                errors.append(f"{where}.publications[{j}]: missing title")
            y = (pub or {}).get("year")
            if y is not None and not isinstance(y, int):
                warnings.append(f"{where}.publications[{j}]: year should be an integer")

    for (name, school), n in name_school.items():
        if n > 1:
            warnings.append(f"possible duplicate person: '{name}' at '{school}' appears {n} times")

    return errors, warnings


def main():
    ap = argparse.ArgumentParser(description="Validate faculty.json for search_prof")
    ap.add_argument("--data", default="data/faculty.json", help="path to faculty.json")
    args = ap.parse_args()

    data, err = load(args.data)
    if err:
        print(f"ERROR: {err}", file=sys.stderr)
        return 1

    errors, warnings = validate(data)
    profs = data.get("professors", [])
    fine = sum(1 for p in profs if isinstance(p, dict) and p.get("confidence") == "fine")
    print(f"Checked {len(profs)} professors ({fine} fine, {len(profs) - fine} coarse)")

    for w in warnings:
        print(f"  WARN  {w}")
    for e in errors:
        print(f"  ERROR {e}")

    if errors:
        print(f"\nFAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"\nOK: 0 errors, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
