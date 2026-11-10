---
name: onboarding
description: Set up a new user (or re-run setup) — profile, degree requirements, host school, inboxes, logins. Use when me/profile.json is missing or onboarded is false, or the user says "set me up".
---
# Onboarding
Goal: a usable `me/` folder in ~10 minutes, asking only what's needed.

1. If `me/` is missing, copy `templates/me/*` into `me/` (never overwrite existing files).
2. Ask in ONE short batch (allow "skip"/"not sure"):
   - Name, Penn school (College / Wharton / SEAS / Nursing), major(s), minor(s), expected graduation term
   - Host school in London and term (e.g. Queen Mary, Spring 2027)
   - Constraints: must you be back in the US by a date? avoid the exam period?
   - Which email gets Penn Abroad mail, which gets bookings (the connected Gmail is read directly; another inbox is read through Chrome)
   - Allow the agent to make bookings (with approval each time)? yes/no
   - Do you have existing planning (planner, spreadsheet, Path@Penn worksheet PDF)? Paste, attach, or share a link → `import-planner` skill.
3. Program facts: search the connected inbox for the host school's welcome/countdown emails and Penn Abroad acceptance;
   fill `profile.program_dates` with [FACT]s + source. Check `knowledge/institutions/<school>.md`; if missing or stale, research
   the school (see `xcat-research` and `course-planner`) and propose a new page via `me/core-suggestions.md`.
4. Degree requirements: read Path@Penn → Degree Audit & Advising (user signs in; see CLAUDE.md logins) or an uploaded audit,
   and fill `me/requirements.json`. Program rules come from `knowledge/programs/` (Wharton students: `wharton.md`).
5. Entry permission: ask citizenship only as "Do you travel on a US passport?" — then use `knowledge/uk-entry.md` (recheck live).
6. Seed deadlines/tasks from email + `knowledge/penn-abroad.md` checklist. Set `onboarded: true`.
7. Offer the weekly check-in: create a scheduled task (Mondays 8am) using `templates/weekly-checkin-prompt.md`, with the user's folder path filled in.
8. Run `python3 scripts/check_data.py`, build the dashboard, and give the user a 5-line summary + top 3 next steps.
