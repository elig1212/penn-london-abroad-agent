#!/usr/bin/env python3
"""Validate me/ files: JSON parses, required fields, dates, duplicate ids, and timetable clashes among registered courses."""
import json, os, re, sys, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _paths import data_dir
ME = data_dir()
REQ = {"requirements.json": ["id", "name"], "courses.json": ["id", "title", "status"], "deadlines.json": ["id", "date", "title"],
       "tasks.json": ["id", "title", "status"], "bookings.json": ["id", "type"], "documents.json": ["id", "kind"], "contacts.json": ["id", "name"]}
problems = []
for fn, fields in REQ.items():
    p = os.path.join(ME, fn)
    if not os.path.exists(p): problems.append(f"missing {fn}"); continue
    try: data = json.load(open(p))
    except Exception as e: problems.append(f"{fn}: invalid JSON ({e})"); continue
    ids = [r.get("id") for r in data]
    for d in {i for i in ids if ids.count(i) > 1}: problems.append(f"{fn}: duplicate id {d}")
    for r in data:
        for f in fields:
            if not r.get(f): problems.append(f"{fn}: {r.get('id')} missing {f}")
        for k in ("date", "due", "expires", "issued"):
            v = r.get(k)
            if v and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(v)): problems.append(f"{fn}: {r.get('id')} {k}={v} not YYYY-MM-DD")
        if fn == "documents.json" and r.get("kind") == "copy" and re.search(r"passport|visa|id card|driv", (r.get("type","")+r.get("title","")), re.I):
            problems.append(f"documents.json: {r['id']} looks like an ID document — must be note-only")
try:
    cs = [c for c in json.load(open(os.path.join(ME, "courses.json"))) if c.get("status") == "registered" and "DROP" not in c.get("verdict", "")]
    slots = [(c["id"], d) for c in cs for d in c.get("days", []) if "option" not in d.get("type", "").lower()]
    for i in range(len(slots)):
        for j in range(i + 1, len(slots)):
            (a, x), (b, y) = slots[i], slots[j]
            if a != b and x["day"] == y["day"] and x["start"] < y["end"] and y["start"] < x["end"]:
                problems.append(f"clash: {a} {x['day']} {x['start']}-{x['end']} vs {b} {y['start']}-{y['end']}")
except Exception as e: problems.append(f"courses.json clash check failed: {e}")
try: list(csv.DictReader(open(os.path.join(ME, "expenses.csv"))))
except Exception as e: problems.append(f"expenses.csv: {e}")
print("OK — no problems found" if not problems else "\n".join("• " + p for p in problems))
sys.exit(1 if problems else 0)
