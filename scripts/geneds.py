#!/usr/bin/env python3
"""Which XCAT precedents at my host school could satisfy a Penn gen-ed requirement?

Usage:
  python3 scripts/geneds.py --school qmul --need "sector 6"
  python3 scripts/geneds.py --school goldsmiths --need AUSO
  python3 scripts/geneds.py --school ucl --need "wharton social science"
  python3 scripts/geneds.py --school all --list          # every precedent with its attributes
  python3 scripts/geneds.py --codes                      # list requirement names and codes

Data: data-shared/xcat-precedents-<school>.csv + data-shared/penn-course-attributes.csv (refresh with
`python3 scripts/penn_attrs.py build`).

Rule [FACT, college.upenn.edu/node/234, checked 2026-11-10]: abroad/transfer credit counts toward a College sector only when
the department awards credit as a Penn course number that is itself approved for that sector. Study-abroad catch-all
numbers (e.g. HIST 18xx, URBS 298x, PSYC 298x/3985) are not in Penn's course search and are treated as NOT filling
any gen-ed requirement unless an XCAT decision says otherwise. Attributes come from one recent offering of the Penn
course and can change by term — always confirm in Path@Penn.
"""
import argparse, csv, glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DS = os.path.join(ROOT, "data-shared")

CODES = {
    # College sectors
    "AUSO": "College Sector 1: Society", "AUHT": "College Sector 2: History & Tradition",
    "AUAL": "College Sector 3: Arts & Letters", "AUHS": "College Sector 4: Humanities & Social Science",
    "AULW": "College Sector 5: The Living World", "AUPW": "College Sector 6: The Physical World",
    "AUNM": "College Sector 7: Natural Science Across the Disciplines",
    # College foundations
    "AUCC": "College Foundation: Cross Cultural Analysis", "AUCD": "College Foundation: Cultural Diversity in the U.S.",
    "AUFR": "College Foundation: Formal Reasoning & Analysis", "AUQD": "College Foundation: Quantitative Data Analysis",
    "AUFL": "College Foundation: Foreign Language", "AUFS": "College First-Year Seminar",
    # Wharton undergraduate general education
    "WUSS": "Wharton: Social Science (SS)", "WUHM": "Wharton: Humanities", "WUNM": "Wharton: Natural Science, Math & Engineering (NSME)",
    "WUGE": "Wharton: Global Economy, Business & Society (GEBS)", "WUTI": "Wharton: Technology, Innovation & Analytics (TIA)",
    "WUCN": "Wharton: Cross-Cultural Perspectives, non-US", "WUCU": "Wharton: Cross-Cultural Perspectives, US",
    "WUFG": "Wharton: Flex Core GenEd", "WUFC": "Wharton: Flex Core", "WUFL": "Wharton: Foreign Language",
    "WUDP": "Wharton: OIDD Decision Processes track elective",
}
ALIASES = {"sector 1": "AUSO", "society": "AUSO", "sector 2": "AUHT", "history and tradition": "AUHT",
           "sector 3": "AUAL", "arts and letters": "AUAL", "sector 4": "AUHS", "humanities and social science": "AUHS",
           "sector 5": "AULW", "living world": "AULW", "sector 6": "AUPW", "physical world": "AUPW",
           "sector 7": "AUNM", "natural science across": "AUNM", "cross cultural": "AUCC", "cultural diversity": "AUCD",
           "formal reasoning": "AUFR", "quantitative data": "AUQD", "wharton social science": "WUSS",
           "wharton humanities": "WUHM", "nsme": "WUNM", "wharton natural science": "WUNM", "gebs": "WUGE",
           "tia": "WUTI", "cross-cultural non-us": "WUCN", "cross-cultural us": "WUCU", "flex": "WUFG"}


def resolve(need):
    n = need.strip()
    if re.fullmatch(r"[A-Z]{4}", n.upper()) and n.upper() in CODES: return n.upper()
    low = n.lower()
    for k, v in ALIASES.items():
        if k in low: return v
    sys.exit(f"Unknown requirement {need!r}. Try --codes.")


def norm(c):
    m = re.match(r"\s*([A-Za-z]{2,5})\s*-?\s*(\d{3,4})", c)
    return f"{m.group(1).upper()} {m.group(2)}" if m else c.upper()


def load():
    attrs = {}
    p = os.path.join(DS, "penn-course-attributes.csv")
    if os.path.exists(p):
        for r in csv.DictReader(open(p)): attrs[r["penn_course"]] = r
    prec = {}
    for f in glob.glob(os.path.join(DS, "xcat-precedents-*.csv")):
        school = os.path.basename(f)[len("xcat-precedents-"):-4]
        prec[school] = list(csv.DictReader(open(f)))
    return attrs, prec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--school", default="all"); ap.add_argument("--need"); ap.add_argument("--list", action="store_true")
    ap.add_argument("--codes", action="store_true")
    a = ap.parse_args()
    if a.codes:
        for k, v in CODES.items(): print(f"{k}  {v}")
        return
    attrs, prec = load()
    schools = sorted(prec) if a.school == "all" else [a.school.lower()]
    want = resolve(a.need) if a.need else None
    for s in schools:
        rows = prec.get(s)
        if rows is None: print(f"No precedent table for {s!r}. Have: {', '.join(sorted(prec))}"); continue
        hits, unknown = [], 0
        for r in rows:
            pc = norm(r["penn_course"]); info = attrs.get(pc, {})
            codes = info.get("attributes", "").split()
            gen = [c for c in codes if c in CODES]
            if a.list:
                hits.append((r, pc, gen, info.get("status", "not looked up")))
            elif want in codes:
                hits.append((r, pc, gen, "found"))
            elif info.get("status") != "found":
                unknown += 1
        label = CODES.get(want, "all gen-ed attributes") if want else "all gen-ed attributes"
        print(f"\n== {s.upper()} · {label} ==")
        if not hits: print("No precedents found whose Penn equivalent carries this attribute.")
        for r, pc, gen, st in sorted(hits, key=lambda h: h[0]["expires"], reverse=True):
            tag = ", ".join(gen) if gen else ("none" if st == "found" else "study-abroad number: no gen-ed (College rule)")
            print(f"  {r['ext_id']:<14} {r['ext_title'][:44]:<44} → {pc:<10} [{tag}]  expires {r['expires']}")
        if want and unknown:
            print(f"  ({unknown} other precedents map to study-abroad-only numbers, which don't carry gen-ed attributes (College rule: only sector-approved Penn numbers count).)")
    if want:
        print("\nLabels: these are [PRECEDENT]s, not guarantees. Precedent expiry dates matter. If nothing fits, look for a host "
              "course that matches a sector-approved Penn course and request that exact Penn number in XCAT.")


if __name__ == "__main__":
    main()
