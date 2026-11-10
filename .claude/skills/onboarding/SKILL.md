---
name: onboarding
description: Set up a new user (or re-run setup) with quick multiple-choice popups — profile, Penn program, host school, semester constraints, features, inboxes, existing plans. Use when me/profile.json is missing or onboarded is false, or the user says "set me up", "get started", or "redo my setup".
---
# Onboarding (popup flow)
Goal: a usable `me/` folder in about 3 minutes, with the user mostly clicking options instead of typing.

## How to ask
- Use the **AskUserQuestion** tool for every round below: up to 4 questions per call, 2–4 options per question, short labels
  (1–5 words), a header of ≤12 characters, and put the recommended option first with "(Recommended)". The popup always adds an
  "Other" box for typing and a Skip button — never add your own "Other"/"None" options; tell the user once that they can type in
  "Other" or skip anything.
- Use `multiSelect: true` only where several answers can be true (majors, features, existing plans).
- Adapt each round to earlier answers (e.g. Wharton gets concentration options). Don't re-ask what you already know
  (from an existing `me/profile.json`, the user's earlier messages, or their connected email).
- If the AskUserQuestion tool isn't available, ask the same round as one short numbered multiple-choice message
  (e.g. "1) Penn school: a. College b. Wharton c. SEAS d. Nursing") and accept replies like "1a 2c".
- Between rounds, say one short line about what you'll do with the answers. Save answers to `me/profile.json` after every round,
  so nothing is lost if the user stops.

## Before the first round
If `me/` is missing, copy `templates/me/*` into `me/` (never overwrite existing files). Send one line:
"Let's set you up — four quick rounds of questions, mostly clicks. Type in 'Other' or skip anything."

## Round 1 — Basics
| header | question | options |
|---|---|---|
| Name | What should I call you? | "Use my account name" · "Skip for now" (they can type a name in Other) |
| Penn school | Which Penn school are you in? | College · Wharton · SEAS · Nursing |
| Host school | Where are you studying in London? | Queen Mary · UCL · Goldsmiths · Another London school |
| Term | When are you abroad? | Spring 2027 · Fall 2027 · Full year 2026–27 · Spring 2028 |

## Round 2 — Studies (adapt options to Round 1)
| header | question | options |
|---|---|---|
| Major | What's your major (or concentration)? multiSelect | College: Economics · Psychology · Political Science · PPE — Wharton: Finance · Marketing · Management · BEPP — SEAS: Computer Science · Bioengineering · Mechanical Eng · Systems Eng — Nursing: Nursing · Health & Societies |
| Minor | Do you have a minor? | No minor · Not declared yet (typed minors go in Other) |
| Class | What's your class year? | Class of 2028 · Class of 2027 · Class of 2029 · Class of 2030 |
| Audit | How should I learn what requirements you still need? | "Read Path@Penn for me (Recommended)" · "I'll upload my audit PDF" · "I'll tell you in chat" · "Skip for now" |

## Round 3 — Your semester
| header | question | options |
|---|---|---|
| Back by | Do you need to be back in the US by a certain date? | No fixed date · Before the end of May · Before mid-June · Before July |
| Exams | How do you feel about final exams in the host school's exam period? | "Avoid them if I can" · "Exams are fine" |
| Housing | What's your housing situation? | Host school halls · Private lease signed · Still looking · Not sure yet |
| UK entry | Which passport will you travel on? | US passport (ETA) · Already have ETA/visa · Other passport · Not sure |
Only ask for passport details as above — never numbers. Use `knowledge/uk-entry.md` (recheck live) to explain what they need.

## Round 4 — How the planner helps
| header | question | options |
|---|---|---|
| Features | What should I help with? multiSelect | Scan email for deadlines · Sync to Google Calendar · Track spending in USD · Weekly Monday check-in |
| Booking | Should I ever book travel for you? | "Plan only — I book (Recommended)" · "Book with my OK each time" |
| Inboxes | Where does your study-abroad email go? | Penn email only · Penn + personal Gmail · Personal Gmail only |
| Old plans | Do you have plans to bring in? multiSelect | Old Claude planner · Spreadsheet or CSV · Notes I can paste · Nothing yet |
Map answers into `profile.preferences` (`allow_booking`, `avoid_exam_period`, `features`, `inboxes`) and `profile.back_by`.

## After the popups (do these automatically; show short progress lines)
1. **Program facts:** search the connected inbox for the host school's welcome/countdown emails and the Penn Abroad acceptance;
   fill `profile.program_dates` with [FACT]s + source. Use `knowledge/institutions/<school>.md`; if missing or stale, research the
   school and propose a page in `me/core-suggestions.md`.
2. **Requirements:** per the Audit answer — read Path@Penn → Degree Audit & Advising in Chrome (the user signs in themselves; see
   the logins rules), read the uploaded PDF, or ask in chat — and fill `me/requirements.json`. Program rules: `knowledge/programs/`
   (Wharton: `wharton.md`).
3. **Old plans:** run the `import-planner` skill for each source picked.
4. **Email:** if "Scan email" was picked, run `inbox-scan` once now.
5. **Deadlines:** seed `me/deadlines.json`/`me/tasks.json` from email and the `knowledge/penn-abroad.md` checklist.
6. **Weekly check-in:** if picked, create a scheduled task (Mondays 8am) from `templates/weekly-checkin-prompt.md` with the
   user's folder path filled in. Tell them it runs while the Claude app is open.
7. Set `onboarded: true`, run `python3 scripts/check_data.py`, build the dashboard.

## Finish
Show a short summary (profile in one line, the 3 most urgent dates, what's turned on), then one last AskUserQuestion:
| header | question | options |
|---|---|---|
| Next | What would you like to do first? | Show my dashboard · Plan my courses · Penn Abroad forms · Check my email |
Then do what they picked.
