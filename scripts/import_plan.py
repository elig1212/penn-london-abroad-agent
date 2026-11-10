#!/usr/bin/env python3
"""Import an existing course plan (JSON list or CSV) into me/courses.json.

Usage:
  python3 scripts/import_plan.py PLAN.json|PLAN.csv [--source "where it came from"]            # preview
  python3 scripts/import_plan.py PLAN.json|PLAN.csv --source "…" --commit                       # write

Accepts flexible column names (case-insensitive):
  code/course/course_code · title/name · term/semester · place/school/institution · counts_as/requirement/fulfills ·
  status · note/notes · cu/credits
Existing records (same course code + term) are never overwritten — they're listed as "kept". New records get
status "planned" (Penn) or "considering" (abroad), confidence "unverified", and the given source.
Use it for: an old planner artifact's data, a spreadsheet export, a Path@Penn "plan", or a list the user pastes
(save the paste as CSV first).
"""
import argparse, csv, datetime, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _paths import data_dir
ME = data_dir()
KEYS = {"code": ["code", "course", "course_code", "module", "module_code"], "title": ["title", "name", "course_title"],
        "term": ["term", "semester"], "place": ["place", "school", "institution", "where"],
        "counts_as": ["counts_as", "requirement", "fulfills", "counts", "penn_requirement"],
        "status": ["status"], "note": ["note", "notes", "comment"], "cu": ["cu", "credits", "credit"]}


def pick(row, k):
    low = {str(a).lower().strip(): v for a, v in row.items()}
    for name in KEYS[k]:
        if name in low and low[name] not in (None, ""):
            return str(low[name]).strip()
    return ""


def load(path):
    if path.lower().endswith(".csv"):
        return list(csv.DictReader(open(path, encoding="utf-8-sig")))
    d = json.load(open(path))
    if isinstance(d, dict):
        d = next((v for v in d.values() if isinstance(v, list)), [])
    return d


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("file"); ap.add_argument("--source", default="")
    ap.add_argument("--commit", action="store_true"); a = ap.parse_args()
    rows = load(a.file)
    p = os.path.join(ME, "courses.json"); courses = json.load(open(p)) if os.path.exists(p) else []
    key = lambda code, term: (re.sub(r"\s+", "", code).upper(), term.lower())
    have = {key(c["id"], c.get("term", "")) for c in courses}
    ids = {c["id"] for c in courses}
    today = datetime.date.today().isoformat(); new, kept = [], []
    for r in rows:
        code, term = pick(r, "code"), pick(r, "term")
        if not code: continue
        if key(code, term) in have and not any(n["id"].startswith(code) and n["term"] == term for n in new):
            kept.append(f"{code} ({term})"); continue
        base, i = code, 2
        while code in ids: code, i = f"{base} #{i}", i + 1
        place = pick(r, "place") or "Penn"
        abroad = place.lower() not in ("penn", "upenn", "university of pennsylvania")
        new.append({"id": code, "title": pick(r, "title"), "host_school": place, "level": "", "credits_host": "",
                    "term": term, "days": [], "assessment": "", "has_exam_in_exam_period": None,
                    "penn_equivalent": pick(r, "counts_as") if abroad else code, "penn_requirement": "",
                    "xcat": {"status": "none" if abroad else "n/a", "precedent_expires": None}, "host_registration": "",
                    "status": "considering" if abroad else "planned", "verdict": pick(r, "status") or "",
                    "notes": pick(r, "note"), "counts_as": pick(r, "counts_as"), "cu": pick(r, "cu"),
                    "confidence": "unverified", "source": a.source or f"import:{os.path.basename(a.file)}", "updated": today})
        have.add(key(base, term)); ids.add(code)
    print(f"{len(rows)} rows read · {len(new)} new · {len(kept)} already in courses.json (kept as is)")
    for n in new: print(f"  + {n['term']:<12} {n['host_school'][:12]:<12} {n['id']:<10} {n['title'][:40]:<40} → {n['counts_as'][:40]}")
    for k in kept: print(f"  = {k}")
    if a.commit:
        json.dump(courses + new, open(p, "w"), indent=1, ensure_ascii=False); print("written to me/courses.json")
    else:
        print("Preview only — rerun with --commit to save.")


if __name__ == "__main__":
    main()
