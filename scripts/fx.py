#!/usr/bin/env python3
"""Currency conversion to USD using Frankfurter (ECB reference rates; free, no key). Caches in me/.fx-cache.json.
Usage: python3 scripts/fx.py 12.40 GBP 2027-01-20   -> prints USD amount and rate
"""
import json, os, sys, urllib.request, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _paths import data_dir
CACHE = os.path.join(data_dir(), ".fx-cache.json")

def _load():
    try: return json.load(open(CACHE))
    except Exception: return {}

def rate(currency, date):
    """Return (usd_per_unit, rate_date). date 'YYYY-MM-DD'; future/today dates use latest."""
    currency = currency.upper()
    if currency == "USD": return 1.0, date
    cache = _load(); key = f"{currency}:{date}"
    if key in cache: return tuple(cache[key])
    d = date if date <= datetime.date.today().isoformat() else "latest"
    url = f"https://api.frankfurter.app/{d}?from={currency}&to=USD"
    data = json.loads(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "study-abroad-planner"}), timeout=20).read())
    r = (float(data["rates"]["USD"]), data["date"])
    cache[key] = r
    os.makedirs(os.path.dirname(CACHE), exist_ok=True); json.dump(cache, open(CACHE, "w"))
    return r

def to_usd(amount, currency, date):
    r, d = rate(currency, date)
    return round(float(amount) * r, 2), r, d

if __name__ == "__main__":
    amt, cur, date = sys.argv[1], sys.argv[2], (sys.argv[3] if len(sys.argv) > 3 else datetime.date.today().isoformat())
    usd, r, d = to_usd(amt, cur, date)
    print(f"{amt} {cur.upper()} = ${usd:.2f} USD (rate {r:.4f}, ECB {d})")
