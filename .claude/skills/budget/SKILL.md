---
name: budget
description: Track spending and budget in USD — receipts from email, bank/card CSV imports, manual entries, FX conversion, reports. Use for "log £12 lunch", "import my statement", "how much have I spent", "expense report".
---
# Budget
- Ledger: `me/expenses.csv`. Plan: `me/budget.json`. Display USD first.
- Add: `python3 scripts/expenses.py add --date 2027-01-20 --desc "Tesco" --amount 12.40 --currency GBP --category food --source manual`
- Import a bank/card CSV: `python3 scripts/expenses.py import path/to.csv` (auto-detects date/description/amount columns,
  asks nothing — prints a preview; then rerun with `--commit`). Dedupes on (date, amount, description).
- FX: `scripts/fx.py` uses Frankfurter (ECB reference rates, free, no key; cached in `me/.fx-cache.json`). Rate is the
  transaction date's (or the previous business day's). Card issuer rates differ slightly — label totals as estimates.
- Report: `python3 scripts/expenses.py report [--from … --to …]` → totals by category and month, in USD.
- Categories: tuition-fees, housing, food, transport, travel, phone, health, admin (visa/ETA/fees), personal, other.
- Budget planning: Penn Abroad budget sheets/costs come from Penn Abroad (cite); London costs must be cited and dated.
- Never move money, connect bank logins, or give investment advice.
