#!/usr/bin/env python3
"""Build the web planner (web/planner.html) from web/planner.template.html + the shared core.

Bakes in: every knowledge/*.md page (as chat-readable topics), the XCAT precedent tables, and Penn course
attributes. Personal data is never baked in — each viewer's data lives in the page's private per-person storage.

Usage: python3 scripts/build_web.py      then publish web/planner.html with the Artifact tool (same file path = same link).
"""
import csv, glob, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def topics():
    out = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "knowledge", "**", "*.md"), recursive=True)):
        rel = os.path.relpath(f, os.path.join(ROOT, "knowledge"))[:-3]
        if rel == "README": continue
        text = open(f).read()
        meta = {}
        m = re.match(r"---\n(.*?)\n---\n", text, re.S)
        if m:
            for line in m.group(1).splitlines():
                if ":" in line: k, v = line.split(":", 1); meta[k.strip()] = v.strip()
            text = text[m.end():]
        title = (re.search(r"^#\s+(.+)$", text, re.M) or [None, rel])[1]
        out[rel] = {"title": title, "last_checked": meta.get("last_checked", ""), "recheck_by": meta.get("recheck_by", ""), "text": text.strip()}
    sl = os.path.join(ROOT, "data-shared", "penn-sector-lists.md")
    if os.path.exists(sl):
        out["penn-sector-lists"] = {"title": "Penn courses approved for each gen-ed attribute + QMUL Sector 6 candidates",
                                    "last_checked": "2026-11-10", "recheck_by": "", "text": open(sl).read().strip()}
    return out


def precedents():
    attrs = {}
    p = os.path.join(ROOT, "data-shared", "penn-course-attributes.csv")
    if os.path.exists(p):
        for r in csv.DictReader(open(p)):
            attrs[r["penn_course"]] = r["attributes"].split() if r["status"] == "found" else None
    rows = []
    for f in sorted(glob.glob(os.path.join(ROOT, "data-shared", "xcat-precedents-*.csv"))):
        school = os.path.basename(f)[len("xcat-precedents-"):-4]
        for r in csv.DictReader(open(f)):
            pc = re.sub(r"^([A-Z]+)\s*(\d+)$", r"\1 \2", r["penn_course"].strip().upper())
            a = attrs.get(pc)
            rows.append({"school": school, "ext_id": r["ext_id"], "ext_title": r["ext_title"], "penn": pc,
                         "cu": r["cu"], "expires": r["expires"], "attrs": a if a is not None else [], "abroad_number": a is None})
    return rows


def main():
    tpl = open(os.path.join(ROOT, "web", "planner.template.html")).read()
    data = {"built": __import__("datetime").date.today().isoformat(), "topics": topics(), "precedents": precedents()}
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = tpl.replace("__SHARED_DATA__", blob)
    out = os.path.join(ROOT, "web", "planner.html")
    open(out, "w").write(html)
    print(f"wrote {out}: {len(html)//1024} KB · {len(data['topics'])} topics · {len(data['precedents'])} precedents")


if __name__ == "__main__":
    main()
