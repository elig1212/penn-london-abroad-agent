#!/usr/bin/env python3
"""Expense ledger in me/expenses.csv (USD-normalised).
  add     --date YYYY-MM-DD --desc TEXT --amount N --currency GBP --category food [--source manual] [--ref ID]
  import  FILE.csv [--currency GBP] [--commit]     bank/card export; preview unless --commit; dedupes
  report  [--from YYYY-MM-DD] [--to YYYY-MM-DD]
"""
import argparse, csv, os, re, sys, datetime, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fx import to_usd
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from _paths import data_dir
LEDGER = os.path.join(data_dir(), "expenses.csv")
FIELDS = "date,description,category,amount,currency,usd,fx_rate,fx_date,source,ref".split(",")
CATS = {"food": r"tesco|sainsbury|pret|deliveroo|uber eats|restaurant|cafe|coffee|lidl|aldi|co-op|waitrose|m&s|starbucks",
        "transport": r"tfl|oyster|uber|bolt|national rail|trainline|lime|bus",
        "travel": r"ryanair|easyjet|british airways|eurostar|booking\.com|airbnb|hostel|hotel|flight",
        "phone": r"giffgaff|vodafone|ee |three|o2|lebara|esim", "housing": r"rent|deposit|landlord|accommodation"}

def rows():
    if not os.path.exists(LEDGER): return []
    return list(csv.DictReader(open(LEDGER)))

def key(r): return (r["date"], f'{float(r["amount"]):.2f}', r["description"].strip().lower()[:40])

def write(new):
    exist = rows(); seen = {key(r) for r in exist}; added = 0
    with open(LEDGER, "a", newline="") as f:
        w = csv.DictWriter(f, FIELDS)
        if not exist and os.path.getsize(LEDGER) == 0: w.writeheader()
        for r in new:
            if key(r) in seen: continue
            w.writerow(r); seen.add(key(r)); added += 1
    return added

def mk(date, desc, amount, currency, category, source, ref=""):
    usd, rt, d = to_usd(amount, currency, date)
    if not category:
        category = next((c for c, p in CATS.items() if re.search(p, desc, re.I)), "other")
    return dict(date=date, description=desc, category=category, amount=f"{float(amount):.2f}", currency=currency.upper(),
                usd=f"{usd:.2f}", fx_rate=f"{rt:.5f}", fx_date=d, source=source, ref=ref)

def parse_date(s):
    for f in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d %b %Y", "%d-%m-%Y", "%Y/%m/%d"):
        try: return datetime.datetime.strptime(s.strip(), f).date().isoformat()
        except ValueError: pass
    raise ValueError(f"unrecognised date {s!r}")

def do_import(path, currency, commit):
    rd = csv.DictReader(open(path, encoding="utf-8-sig")); cols = [c.lower() for c in rd.fieldnames]
    pick = lambda *names: next((rd.fieldnames[i] for i, c in enumerate(cols) if any(n in c for n in names)), None)
    dc, sc = pick("date"), pick("description", "merchant", "name", "details", "payee", "memo")
    ac, oc, ic = pick("amount", "value"), pick("debit", "paid out", "money out"), pick("credit", "paid in", "money in")
    cc = pick("currency")
    out = []
    for r in rd:
        if ac and r[ac].strip(): amt = float(re.sub(r"[^\d.\-]", "", r[ac]))
        elif oc and r[oc].strip(): amt = -float(re.sub(r"[^\d.\-]", "", r[oc]))
        else: continue
        if amt >= 0 and not (oc and not ac): continue          # skip refunds/income; spending is negative
        out.append(mk(parse_date(r[dc]), r[sc].strip(), abs(amt), (r[cc] if cc else currency) or currency, "", f"import:{os.path.basename(path)}"))
    print(f"columns: date={dc} desc={sc} amount={ac or oc} currency={cc or currency}; {len(out)} spending rows")
    for r in out[:10]: print(" ", r["date"], r["description"][:30], r["amount"], r["currency"], "→ $"+r["usd"], r["category"])
    if commit: print("added", write(out), "new rows (duplicates skipped)")
    else: print("Preview only — rerun with --commit to save.")

def report(frm, to):
    data = [r for r in rows() if (not frm or r["date"] >= frm) and (not to or r["date"] <= to)]
    bycat, bymon = collections.Counter(), collections.Counter()
    for r in data: bycat[r["category"]] += float(r["usd"]); bymon[r["date"][:7]] += float(r["usd"])
    tot = sum(bycat.values())
    print(f"Total: ${tot:,.2f} USD over {len(data)} expenses (FX: ECB reference rates — estimates)")
    for c, v in bycat.most_common(): print(f"  {c:12} ${v:,.2f}")
    for m in sorted(bymon): print(f"  {m}  ${bymon[m]:,.2f}")

if __name__ == "__main__":
    p = argparse.ArgumentParser(); s = p.add_subparsers(dest="cmd", required=True)
    a = s.add_parser("add"); a.add_argument("--date", required=True); a.add_argument("--desc", required=True)
    a.add_argument("--amount", required=True); a.add_argument("--currency", default="USD"); a.add_argument("--category", default="")
    a.add_argument("--source", default="manual"); a.add_argument("--ref", default="")
    i = s.add_parser("import"); i.add_argument("file"); i.add_argument("--currency", default="USD"); i.add_argument("--commit", action="store_true")
    r = s.add_parser("report"); r.add_argument("--from", dest="frm"); r.add_argument("--to")
    x = p.parse_args()
    if x.cmd == "add": print("added", write([mk(x.date, x.desc, x.amount, x.currency, x.category, x.source, x.ref)]))
    elif x.cmd == "import": do_import(x.file, x.currency, x.commit)
    else: report(x.frm, x.to)
