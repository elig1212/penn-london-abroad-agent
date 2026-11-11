---
name: dashboard
description: Build and publish the planning dashboard (timeline, tasks, courses with days, requirements, budget, bookings, documents). Use after data changes or when the user asks to see the dashboard / view on phone.
---
# Dashboard
1. `python3 scripts/check_data.py` then `python3 scripts/build_dashboard.py` → writes `me/dashboard.html` (self-contained).
2. Phone access: publish `me/dashboard.html` with the Artifact tool (private by default), passing every saved copy in
   `me/documents.json` (`kind: "copy"`) as `files` — key = its `path` (e.g. `documents/2026-09-10-offer-letter.pdf`), value = the file
   on disk — so the archive's Open links work online. Never upload note-only documents. Reuse the same file path so the
   URL stays the same; save the URL in `profile.json → dashboard_url`. Don't publish without the user's OK the first time.
3. The dashboard is read-only; edits happen by asking the agent (or editing `me/` files).

**What the dashboard shows:** only registered courses (`me/courses.json`), requirements grouped Major / Minor / Gen eds — **every** requirement, completed ones included with the courses that filled them — with **CU left** (done + currently enrolled at Penn count as complete; courses planned abroad do not), confirmed bookings (cancelled ones marked), the document archive (saved copies as links; ID documents as notes), and an itemized budget (each expense and confirmed booking with what it was for). Open questions are not shown on the dashboard.
