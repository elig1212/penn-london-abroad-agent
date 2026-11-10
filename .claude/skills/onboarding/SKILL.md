---
name: onboarding
description: Runs first for every new user, before anything else they ask. Sets up the planner almost hands-free — one round of quick popups, then Claude signs into Penn sites with the user, pulls their degree audit, Penn Abroad forms, email and program dates, syncs the calendar and builds the dashboard. Use when me/profile.json is missing or onboarded is false, or the user says "set me up", "get started", or "redo my setup".
---
# Onboarding — automatic setup
The user should mostly sit back: answer **one popup round**, sign in when asked, and click a few approvals. Claude does the rest,
in order, without stopping to chat. Target: 10–15 minutes, about 5 clicks plus sign-ins.

## Principles
- **Ask everything up front, once.** After the opening popup, never ask anything that a site, email or earlier answer can tell you.
  Use **AskUserQuestion** popups (≤4 questions, 2–4 options, recommended option first with "(Recommended)"; it adds "Other"
  and Skip automatically). If that tool isn't available, ask the same as a numbered multiple-choice message.
- **Keep going.** If a stage fails (not signed in, a site changed, no connector), note it in a "Needs you" list, then continue with
  the next stage. Never stop the whole setup for one problem.
- **Show progress, not chatter.** Before each stage, post one line like "Step 3 of 8 — Reading your Path@Penn degree audit…".
  After it, one line with the result ("✓ Economics major, Consumer Psych minor — 7 requirements left").
- **Save after every stage** to `me/`, so stopping loses nothing.
- **Approvals still apply:** sign-ins are the user's (never type passwords; use the password manager if connected), calendar events
  need one approval, nothing is submitted, sent, booked or deleted.

## Step 0 — Create the planner folder (no questions)
Onboarding starts as soon as the user sends any first message; save that message to `me/pending-request.md` right after this step
and answer it only after Step 9.
- **Plugin mode** (running from the plugin): always create a **new, dedicated folder** — `~/Documents/Penn London Planner` — even if
  a "Study Abroad" or similar folder already exists. Never reuse or write into another existing folder. If that exact path already
  exists and isn't a planner folder (no `planner-data/profile.json`), use `~/Documents/Penn London Planner 2` (3, …) instead.
  Ask the app for access to the new folder if needed and work there. Create `planner-data/` inside it, copy `templates/me/*` into it,
  and write the folder's absolute path as the only line of `~/.penn-london-planner`.
- **Folder mode** (this repo on the maintainer's Mac): use `me/` in the repo as usual.
One line to the user: "Created your planner folder: Documents/Penn London Planner."

## Step 1 — the only questions (one AskUserQuestion call)
Say first: "I'll ask 4 quick questions, then set everything up myself. You'll just sign in to Penn once and approve a couple of things."
| header | question | options |
|---|---|---|
| Host school | Where are you studying in London? | Queen Mary · UCL · Goldsmiths · Another London school |
| Constraints | Anything I should plan around? multiSelect | Back in US before June · Avoid final exams · No constraints |
| Set up | What should I set up for you? multiSelect | Read Penn sites for me (Recommended) · Scan my email · Sync dates to my calendar · Weekly Monday check-in |
| Booking | Should I ever book travel for you? | Plan only — I book (Recommended) · Book with my OK each time |
Save to `me/profile.json` (`host_school`, `preferences.avoid_exam_period`, `back_by` if given, `preferences.features`,
`preferences.allow_booking`). Term, name, school, major, minor and class year come from Path@Penn/Penn Abroad in later steps.
If the user picked "Read Penn sites" but Claude in Chrome isn't connected, add it to "Needs you" and fall back to asking those facts in
one more popup at the end.

## Step 2 — Get Chrome ready
Load the Claude in Chrome tools in one ToolSearch call, open a new tab. If the extension isn't connected, show the install link from
the tool's error message and mark Steps 3–4 as "Needs you".

## Step 3 — Path@Penn (sign in once)
Follow `references/path-at-penn.md`. Open path.at.upenn.edu. If the PennKey login page shows:
use the password manager if connected; otherwise post an AskUserQuestion: "Please sign in to Path@Penn in the Chrome tab I opened
(and approve Duo). Click when done." options: "I've signed in" · "Skip Penn sites". Then read, without asking:
- name (first name), Penn school, major(s), minor(s), expected graduation term, advisors (→ `me/contacts.json`)
- degree audit: every requirement still open, by major / minor / gen-ed (→ `me/requirements.json`, source "Path@Penn audit <date>")
- current-term registered courses (to know what's in progress)
Post the result line, e.g. "✓ College · Economics + Consumer Psych minor · Class of 2028 · 7 requirements left".

## Step 4 — Penn Abroad portal (same sign-in)
Follow `references/penn-abroad-portal.md`. Read the program name, term and dates, application status, and every To Do form with
status and due date → `me/profile.json` (`term`, `penn_abroad_status`) and `me/deadlines.json` (category penn-abroad).

## Step 5 — Email (if picked)
Run the `inbox-scan` skill on the connected Gmail (and the personal Gmail through Chrome if it's signed in there): host-school
welcome/countdown emails → `profile.program_dates` and host deadlines (module registration, housing, arrival, orientation, exams);
ETA/visa approvals → note-only documents; bookings and trip receipts. Add what's needed to `me/deadlines.json`/`tasks.json`.

## Step 6 — Host school and courses
Read `knowledge/institutions/<school>.md` and add its key dates if email didn't have them (as [FACT] with source). Run a quick
`gen-ed-finder`/`xcat-research` pass: precedents at their school that match any open requirement → note them in
`me/requirements.json` (`notes`) as [PRECEDENT]s. Don't recommend specific course choices yet — just record the matches.

## Step 7 — Calendar (if picked) — one approval
Collect every open deadline from today onward. Post one AskUserQuestion:
"Add N study-abroad dates to your Google Calendar? (reminders 7 days and 1 day before)" options:
"Add all N (Recommended)" · "Only the next 30 days" · "Skip for now". Then create the events (see `calendar-sync`), saving each
event id. No further questions.

## Step 8 — Weekly check-in (if picked)
Create a scheduled task (Mondays 8am) from `templates/weekly-checkin-prompt.md` with this folder's absolute path filled in. One line:
"✓ Weekly check-in set for Mondays 8am (runs when the Claude app is open)."

## Step 9 — Finish
Set `onboarded: true`; run `python3 scripts/check_data.py`; build and publish the dashboard (`dashboard` skill). Then show:
- one-line profile, the 3 most urgent dates, what was synced, and the **Needs you** list (sign-ins skipped, items to confirm);
- the dashboard link;
- then, if `me/pending-request.md` exists, say "Now, back to what you asked:", answer that request fully, and delete the file;
- otherwise one last AskUserQuestion — "What next?": Plan my courses · Penn Abroad forms · Review my budget · I'm good for now.
