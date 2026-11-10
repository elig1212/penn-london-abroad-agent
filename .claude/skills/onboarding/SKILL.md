---
name: onboarding
description: Runs first for every new user, before anything else they ask. Guided, mostly automatic setup that assumes nothing is connected yet — one quick popup, then it walks the user through installing Claude in Chrome, connecting Gmail/Calendar and signing in to email, Path@Penn and Penn Abroad (asking permission with Yes/No popups), pulls their audit, forms, email and program dates, syncs the calendar and builds the dashboard. Use when me/profile.json is missing or onboarded is false, or the user says "set me up", "get started", or "redo my setup".
---
# Onboarding — guided automatic setup
Assume the user has **nothing** set up: no Claude in Chrome, no connectors, not signed in to email, Path@Penn or Penn Abroad.
The user should only answer one popup, click Yes/Done on a few popups, and sign in when asked. Claude does everything else, in
order, and pushes them toward the recommended choice. Target: 15–20 minutes including installs.

## Rules for the whole flow
- **Popups, not chat.** Use AskUserQuestion for every question. If it isn't available, ask the same thing as a short numbered list.
- **Permission popups** — whenever you need to do something on the user's behalf (install guidance, opening sites, reading accounts,
  adding calendar events, scheduling the check-in), ask exactly:
  question "Do I have your permission to <do X>? (HIGHLY RECOMMENDED)", options **Yes** · **No** (nothing else).
  On **No**: one line on what they'll miss, add it to a "Needs you" list, continue with the next step. Never re-ask in the same setup.
- **Check before asking.** If something already works (extension connected, already signed in), skip its permission popup entirely.
- **Never stop the whole setup** for one failed step: note it in "Needs you" and continue.
- **Progress lines:** before each step one line ("Step 4 of 10 — Signing you in to Path@Penn…"); after it one result line ("✓ …").
- **Save after every step** to `me/` so nothing is lost if the user stops. Answers and results only — never passwords, ID numbers.
- Never type passwords or 2FA codes; the user signs in (or the password manager fills, with their approval). Never submit, send,
  book or delete anything during setup.
- Detailed walkthroughs and checks: `references/getting-connected.md`; reading sites: `references/path-at-penn.md`,
  `references/penn-abroad-portal.md`.

## Step 0 — Planner folder and first request (no questions)
- **Plugin mode:** always create a **new** folder `~/Documents/Penn London Planner` (if that path exists but isn't a planner folder, use
  "Penn London Planner 2", 3, …). Never reuse another existing folder. Ask the app for access if needed and work there. Create
  `planner-data/`, copy `templates/me/*` into it, and write the folder's absolute path as the only line of `~/.penn-london-planner`.
  **Folder mode** (maintainer's repo): use `me/`.
- Save the user's first message to `me/pending-request.md`; it's answered at the very end.
- Say: "Welcome! I'll set up your study abroad planner — one quick question round, then I'll walk you through connecting Chrome and
  your accounts and do the rest myself. Afterwards I'll come back to your question."

## Step 1 — The only questions (one AskUserQuestion call)
| header | question | options |
|---|---|---|
| Host school | Where are you studying in London? | Queen Mary · UCL · Goldsmiths · Another London school |
| Constraints | Anything I should plan around? multiSelect | Back in US before June · Avoid final exams · No constraints |
| Booking | Should I ever book travel for you? | Plan only — I book (Recommended) · Book with my OK each time |
Name, Penn school, majors, minors, class year and term come from Path@Penn / Penn Abroad later — don't ask them.

## Step 2 — Claude in Chrome  (getting-connected.md §A)
Check; if not connected: permission popup "Do I have your permission to walk you through installing Claude in Chrome so I can read
Penn sites for you? (HIGHLY RECOMMENDED)" → walkthrough → "Done / Skip this" popup → re-check.

## Step 3 — Gmail + Google Calendar connectors  (§B)
Check; if missing: "Do I have your permission to walk you through connecting your Penn Gmail and Google Calendar? (HIGHLY RECOMMENDED)"
→ walkthrough → Done popup → re-check.

## Step 4 — Email signed in on Chrome  (§C)
Check which Google accounts are signed in on Chrome. If the personal (bookings) inbox isn't: "Do I have your permission to open Gmail in
Chrome so you can sign in to your personal email (where bookings and receipts go)? (HIGHLY RECOMMENDED)" → user signs in → Done popup →
record addresses in `profile.emails`.

## Step 5 — Path@Penn  (§D + path-at-penn.md)
Check; if not signed in: "Do I have your permission to open Path@Penn so you can sign in, and then read your degree audit for you?
(HIGHLY RECOMMENDED)" → user signs in + Duo → Done popup → read name, school, majors, minors, grad term, advisors and every requirement
(in-progress courses count as completed). Result line e.g. "✓ College · Economics + Consumer Psych · Class of 2028 · 6 requirements still needed".

## Step 6 — Penn Abroad portal  (§E + penn-abroad-portal.md)
Usually already signed in after Step 5. Read program, term, dates, application status and every form with its due date.

## Step 7 — Email scan
Run `inbox-scan` on the connected inbox and any Chrome-signed-in personal inbox: host-school key dates, ETA/visa approval (note-only),
bookings, trip receipts, housing. Save to deadlines/tasks/bookings/documents/expenses.

## Step 8 — Host school and course matches
Add the host school's key dates from `knowledge/institutions/<school>.md` if email didn't have them. Run a quick `gen-ed-finder` /
`xcat-research` pass and record precedents matching open requirements in `me/requirements.json` notes as [PRECEDENT]s.
No course recommendations yet.

## Step 9 — Calendar sync
If the calendar connector works: "Do I have your permission to add your N study-abroad dates to your Google Calendar, with reminders a
week and a day before? (HIGHLY RECOMMENDED)" → on Yes, create all events (see `calendar-sync`), save event ids.

## Step 10 — Weekly check-in
"Do I have your permission to set up a weekly Monday check-in that scans your email and portal and refreshes your dashboard?
(HIGHLY RECOMMENDED)" → on Yes, create the scheduled task from `templates/weekly-checkin-prompt.md` with this folder's path; say it runs
while the Claude app is open.

## Step 11 — Dashboard and wrap-up
Set `onboarded: true`; run `python3 scripts/check_data.py`; build and publish the dashboard (`dashboard` skill). Then show:
one-line profile · the 3 most urgent dates · what was connected and synced · the **Needs you** list · the dashboard link.
Finally, if `me/pending-request.md` exists: "Now, back to what you asked:" — answer it fully and delete the file. Otherwise one
AskUserQuestion "What next?": Plan my courses · Penn Abroad forms · Review my budget · I'm good for now.
