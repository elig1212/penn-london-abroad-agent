#!/usr/bin/env python3
"""Fetch Queen Mary (QMUL) module facts from the public Module Directory.
Usage: python3 scripts/qm_module.py ECN317 ECN352 ...   (year defaults to 2026 = 2026/27)
Prints JSON lines: code, title, level, credits, semester(s), assessment, prerequisites, open-to-associates hints.
"""
import json, re, sys, time, urllib.request, urllib.parse, html

YEAR = "2026"

def strip(s):
    if s is None: return ""
    if not isinstance(s, str): s = json.dumps(s)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()

def fetch(code, year=YEAR):
    url = f"https://curriculum.qmul.ac.uk/subject/{year}/{code}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (study-abroad planner)"})
    h = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', h, re.S)
    pc = json.loads(m.group(1))["props"]["pageProps"].get("pageContent") or {}
    if not pc: return {"code": code, "error": "not found", "url": url}
    def g(k): return pc.get(k)
    offerings = []
    for k in ("offering", "unit_offering", "offerings"):
        if g(k): offerings = g(k)
    assess = [f'{a.get("name","").strip()} {a.get("weight","")}% ({a.get("assessment_subtype") or ""}, {a.get("duration") or ""})'
              for a in (g("assessment_data") or [])]
    def codes(o):
        found=[]
        if isinstance(o,dict):
            ai=o.get("academic_item")
            if isinstance(ai,dict) and str(ai.get("value","")).startswith("Module:"): found.append(ai["value"].split(":",1)[1].strip())
            for v in o.values(): found+=codes(v)
        elif isinstance(o,list):
            for v in o: found+=codes(v)
        return found
    reqs = [f'{r.get("requisite_type",{}).get("label","")}: any of {sorted(set(codes(r.get("containers"))))}' for r in (g("requisites") or [])]
    periods = sorted({o.get("teaching_period","") for o in (g("subject_offering") or [])})
    exam_like = any(re.search(r"exam", a, re.I) and not re.search(r"not centrally", a, re.I) for a in assess)
    return {"code": code, "title": g("title"), "level": g("aqf_level"), "credits": g("credit_points"),
            "periods": periods, "assessment": assess, "has_exam": exam_like,
            "requisites": reqs, "url": url}

def search(q, year=YEAR):
    out, frm = [], 0
    while True:
        url=f"https://curriculum.qmul.ac.uk/api/search/search-all?from={frm}&query={urllib.parse.quote(q)}&searchType=advanced&siteId=qmul-prod-pres&siteYear={year}&size=100"
        req=urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0 (study-abroad planner)"})
        d=json.loads(urllib.request.urlopen(req,timeout=30).read())["data"]
        out += [(r["code"], r["title"]) for r in d["results"] if "Module" in r.get("lines",[])]
        frm += 100
        if frm >= d["total"]: return out

if __name__ == "__main__":
    if sys.argv[1:2]==["--search"]:
        for c,t in search(sys.argv[2]): print(c, t)
        sys.exit()
    for c in sys.argv[1:]:
        try: print(json.dumps(fetch(c.upper()), ensure_ascii=False))
        except Exception as e: print(json.dumps({"code": c, "error": str(e)}))
