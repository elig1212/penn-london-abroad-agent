#!/usr/bin/env python3
"""Look up Penn course attributes (College sectors/foundations, Wharton gen-ed, etc.) from Penn's public course
search (courses.upenn.edu), and build data-shared/penn-course-attributes.csv for every Penn course that appears in
the XCAT precedent tables.

Usage:
  python3 scripts/penn_attrs.py build                 # refresh the CSV from all data-shared/xcat-precedents-*.csv
  python3 scripts/penn_attrs.py lookup "PSYC 1310" …  # print attributes for specific courses

Notes: a course only has attributes here if Penn offered it in one of the TERMS searched. Study-abroad-only
numbers (e.g. HIST 1820, URBS 2984, PSYC 3985) never appear in course search → status "not-in-course-search".
"""
import csv, glob, json, os, re, sys, time, html, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data-shared", "penn-course-attributes.csv")
API = "https://courses.upenn.edu/api/?page=fose&route="
TERMS = ["202710", "202630", "202610", "202530", "202510", "202430", "202410", "202330", "202310"]  # Spring=10, Summer=20, Fall=30
_subject_cache = {}


def post(route, body):
    req = urllib.request.Request(API + route, data=json.dumps(body).encode(), method="POST",
                                 headers={"Content-Type": "application/json", "User-Agent": "study-abroad-planner"})
    return json.loads(urllib.request.urlopen(req, timeout=30).read())


def norm(code):
    m = re.match(r"\s*([A-Za-z]{2,5})\s*-?\s*(\d{3,4})", code)
    return f"{m.group(1).upper()} {m.group(2)}" if m else code.strip().upper()


def find_section(code):
    subj = code.split()[0]
    for t in TERMS:
        key = (subj, t)
        if key not in _subject_cache:
            try:
                _subject_cache[key] = post("search", {"other": {"srcdb": t}, "criteria": [{"field": "subject", "value": subj}]}).get("results", [])
            except Exception:
                _subject_cache[key] = []
            time.sleep(0.2)
        for r in _subject_cache[key]:
            if r["code"] == code:
                return t, r["crn"], r.get("title", "")
    return None


def attributes(code):
    code = norm(code)
    hit = find_section(code)
    if not hit:
        return {"penn_course": code, "status": "not-in-course-search", "term": "", "title": "", "attributes": ""}
    t, crn, title = hit
    d = post("details", {"group": f"code:{code}", "key": f"crn:{crn}", "srcdb": t, "matched": f"crn:{crn}"})
    txt = html.unescape(re.sub(r"<[^>]+>", "|", d.get("attributes_detail", "") or ""))
    attrs = sorted({m for m in re.findall(r"\(([A-Z0-9]{4})\)", txt)})
    return {"penn_course": code, "status": "found", "term": t, "title": title, "attributes": " ".join(attrs)}


def build():
    codes = set()
    for f in glob.glob(os.path.join(ROOT, "data-shared", "xcat-precedents-*.csv")):
        for r in csv.DictReader(open(f)):
            codes.add(norm(r["penn_course"]))
    rows = []
    for c in sorted(codes):
        try:
            rows.append(attributes(c))
        except Exception as e:
            rows.append({"penn_course": c, "status": f"error: {e}", "term": "", "title": "", "attributes": ""})
        print(rows[-1]["penn_course"], rows[-1]["status"], rows[-1]["attributes"], file=sys.stderr)
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, ["penn_course", "status", "term", "title", "attributes", "retrieved"])
        w.writeheader()
        for r in rows:
            w.writerow(r | {"retrieved": time.strftime("%Y-%m-%d")})
    print(f"wrote {OUT}: {len(rows)} courses, {sum(r['status']=='found' for r in rows)} with attributes")


if __name__ == "__main__":
    if sys.argv[1:2] == ["build"]:
        build()
    elif sys.argv[1:2] == ["lookup"]:
        for c in sys.argv[2:]:
            print(json.dumps(attributes(c)))
    else:
        print(__doc__)
