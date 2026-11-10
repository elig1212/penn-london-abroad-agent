---
name: dashboard
description: Build and publish the planning dashboard (timeline, tasks, courses with days, requirements, budget, bookings, documents). Use after data changes or when the user asks to see the dashboard / view on phone.
---
# Dashboard
1. `python3 scripts/check_data.py` then `python3 scripts/build_dashboard.py` → writes `me/dashboard.html` (self-contained).
2. Phone access: publish `me/dashboard.html` with the Artifact tool (private by default). Reuse the same file path so the
   URL stays the same; save the URL in `profile.json → dashboard_url`. Don't publish without the user's OK the first time.
3. The dashboard is read-only; edits happen by asking the agent (or editing `me/` files).
