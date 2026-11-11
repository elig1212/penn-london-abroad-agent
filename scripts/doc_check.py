#!/usr/bin/env python3
"""Check a document before keeping a copy: flags ID details (passport/ID/visa numbers, SSN, driver's licence).
Usage: python3 scripts/doc_check.py FILE [FILE …]
Prints one line per file: OK (safe to keep a copy) or ID-SENSITIVE (keep a note only) with the reasons. Never prints the values.
PDF text is read with macOS PDFKit (osascript); .txt/.html/.eml are read directly. If the text can't be read, says UNKNOWN —
then ask the user before keeping a copy.
"""
import os, re, subprocess, sys, json

PATTERNS = {
    "passport number": r"passport\s*(number|no\.?|#)\s*[:\-]?\s*(?!that\b|ending\b|ends\b)[A-Z0-9]{6,}",  # a full number, not a masked "ends in NNNN"
    "ID/document number": r"(national\s+id|identity\s+card|document)\s*(number|no\.?|#)",
    "visa/BRP number": r"(visa|brp|residence\s+permit)\s*(number|no\.?|#)",
    "social security / national insurance": r"social\s+security|\bssn\b|national\s+insurance\s+(number|no)",
    "driver's licence": r"driv(er'?s|ing)\s+licen[cs]e",
}


def text_of(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in (".txt", ".html", ".htm", ".eml", ".md"):
        return open(path, errors="ignore").read()
    if ext == ".pdf" and sys.platform == "darwin":
        js = ("ObjC.import('PDFKit'); const d=$.PDFDocument.alloc.initWithURL($.NSURL.fileURLWithPath(%s)); "
              "d ? ObjC.unwrap(d.string) || '' : ''") % json.dumps(os.path.abspath(path))
        r = subprocess.run(["osascript", "-l", "JavaScript", "-e", js], capture_output=True, text=True)
        return r.stdout
    return ""


for f in sys.argv[1:]:
    t = text_of(f)
    if not t.strip():
        print(f"UNKNOWN       {os.path.basename(f)} — couldn't read its text; ask before keeping a copy"); continue
    hits = [k for k, p in PATTERNS.items() if re.search(p, t, re.I)]
    if hits:
        print(f"ID-SENSITIVE  {os.path.basename(f)} — contains: {', '.join(hits)} → keep a note only")
    else:
        print(f"OK            {os.path.basename(f)}")
