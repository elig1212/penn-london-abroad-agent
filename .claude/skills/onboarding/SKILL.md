---
name: onboarding
description: Runs first for every new user, before anything else they ask. Guided setup in three phases — a few quick questions, then every connection and sign-in (Claude in Chrome, Gmail/Calendar connectors, both email accounts in Chrome, Path@Penn, Penn Abroad), then Claude collects everything on its own and publishes the dashboard, ending with an overview of what the planner can do. Use when me/profile.json is missing or onboarded is false, or the user says "set me up", "get started", or "redo my setup".
---
# Onboarding — guided setup
Assume the user has **nothing** set up. Three phases, strictly in order:
**A. Questions → B. Connections and sign-ins → C. "Please hold" while Claude collects everything → finish message.**
**Never read any site, inbox or audit during Phases A–B.** Phase B only connects and signs in; all reading happens in Phase C, so the user
never waits on Claude while they still have things to do.

## Rules for the whole flow
- **Multiple-choice questions → AskUserQuestion popups.** Free-text answers (email addresses) → a plain chat message asking the user to
  type it; never a popup with "Other". If AskUserQuestion isn't available, use a short numbered list.
- **Permission popups** for anything done on the user's behalf: question "Do I have your permission to <do X>? (HIGHLY RECOMMENDED)",
  options exactly **Yes** · **No**. On No: one line on what they'll miss, add to the "Needs you" list, continue. Never re-ask.
  Ask **all** permissions in Phases A–B (including calendar sync and the weekly check-in) so Phase C runs with no interruptions.
- **Check before asking:** skip any step that already works.
- **Links:** whenever the user needs to click a link, put the full link **in the same message** as a markdown link on its own line.
  Never write "the link above" or "click the link" without the link right there.
- **Never stop setup** for one failed step — note it in "Needs you" and continue.
- **Progress lines:** "Step 3 of 9 — …" before each step, "✓ …" after it.
- **Save after every step** to `me/`. Never store passwords or ID numbers. Never type passwords or 2-step codes.
  Never submit, send, book or delete anything during setup.
- Walkthroughs and checks: `references/getting-connected.md`. Reading sites: `references/path-at-penn.md`,
  `references/penn-abroad-portal.md`.

## Step 0 — Planner folder and first request (no questions)
- **Plugin mode:** always create a **new** folder `~/Documents/Penn London Planner` ("… 2", "… 3" if that path exists but isn't a planner
  folder). Never reuse another existing folder. Get folder access if needed and work there. Create `planner-data/`, copy
  `templates/me/*` into it, and write the folder's absolute path as the only line of `~/.penn-london-planner`.
  **Folder mode** (maintainer's repo): use `me/`.
- Save the user's first message to `me/pending-request.md` (answered at the very end).
- Say: "Welcome! I'll set up your study abroad planner. First a few quick questions, then I'll help you connect your accounts and sign in,
  and then I'll gather everything and build your dashboard while you relax."

# Phase A — Questions

## Step 1 — Three quick choices (one AskUserQuestion call)
| header | question | options |
|---|---|---|
| Host school | Where are you studying in London? | Queen Mary · UCL · Goldsmiths · Another London school |
| Constraints | Anything I should plan around? multiSelect | Back in US before June · Avoid final exams · No constraints |
| Booking | Should I ever book travel for you? | Plan only — I book (Recommended) · Book with my OK each time |
Name, Penn school, majors, minors, class year and term come from Path@Penn / Penn Abroad later — don't ask them.

## Step 2 — Your two email addresses (plain chat, one at a time)
First one line on why: "Chrome needs to be signed in to **both** your school email and your personal email — that's how I find your Penn
Abroad and host-school dates, bookings and receipts to build your dashboard and answer your questions. Any Chrome profile is fine, as long
as it's the one where Claude in Chrome is installed."
Then ask, as plain messages (wait for each reply):
1. "Please type your **school** email address."
2. "Now please type your **personal** email address."
Assume everyone has both. Save to `profile.emails = {school, personal}`.

# Phase B — Connections and sign-ins (no reading yet)

## Step 3 — Claude in Chrome: install and sign in  (getting-connected.md §A)
If not connected: "Do I have your permission to open the Claude in Chrome install page in your Chrome browser? (HIGHLY RECOMMENDED)" →
open it in Chrome and **also** show the link in the message → "Click **Add to Chrome**, then open the extension and sign in to Claude
with the same account you use in this app." → Done popup → re-check. This step is only about the extension and the Claude sign-in;
don't mention Gmail here.

## Step 4 — Gmail + Google Calendar connectors  (§B) — only after Step 3 is done
Say clearly first: "Next we connect Gmail and Google Calendar. When Google asks which account to use, choose your **school** email
(<school email>) — even if your Claude account uses a different email. That's the inbox and calendar your Penn and study-abroad
messages go to." Then "Do I have your permission to connect your school Gmail and Google Calendar? (HIGHLY RECOMMENDED)" → Connect card
→ Done popup → re-check, and confirm the connected Gmail is the school address (one search; compare the recipient address). If it's
the wrong account, explain how to disconnect and reconnect with the school address.

## Step 5 — Both email accounts signed in on Chrome  (§C2–C3)
Skip addresses already signed in. Otherwise: "Do I have your permission to open Gmail sign-in in Chrome and fill in your email
addresses, so you just enter your passwords? (HIGHLY RECOMMENDED)" → one tab per address, type the address, click Next → user enters
passwords / PennKey + 2-step → Done popup → re-check.

## Step 6 — Path@Penn and Penn Abroad sign-in  (§D, §E) — sign in only
"Do I have your permission to open Path@Penn and the Penn Abroad portal so you can sign in? (HIGHLY RECOMMENDED)" → open Path@Penn;
user signs in with PennKey + Duo → Done popup → open the Penn Abroad portal (decline cookies, "Go to Portal"); it usually signs straight
in; if not, the user signs in → Done popup. Only confirm the page titles show signed in — **don't read anything yet.**

## Step 7 — Last permissions (one popup each, back to back)
- If the calendar connector works: "Do I have your permission to add your study-abroad dates to your Google Calendar, with reminders a
  week and a day before? (HIGHLY RECOMMENDED)"
- "Do I have your permission to set up a weekly Monday check-in that scans your email and portal and refreshes your dashboard?
  (HIGHLY RECOMMENDED)"

# Phase C — Collect everything (user waits)
Say: "You're all signed in — thank you! Please hold while I collect your information and build your dashboard. This takes about
5–10 minutes; you don't need to do anything." Then run without questions, one progress line each:
1. **Path@Penn** (path-at-penn.md): name, school, majors, minors, grad term, advisors, every requirement grouped by major / minor /
   gen-ed (in-progress courses count as completed).
2. **Penn Abroad portal** (penn-abroad-portal.md): program, term, dates, status, every form and due date.
3. **Email** (`inbox-scan`, both inboxes): host-school key dates, ETA/visa approval (note-only), bookings — **apply the booking rules
   (cancellations/changes, final price)** — trip receipts, housing.
4. **Host school** (`knowledge/institutions/<school>.md`): key dates email didn't have; quick `gen-ed-finder` / `xcat-research` pass,
   recording precedents that match open requirements as [PRECEDENT] notes. No course recommendations yet.
5. **Your modules and class times:** record every module the user is registered for (host-school registration/decision emails, or the
   host portal if signed in) in `me/courses.json` with `status: "registered"`. Then look up **days and times for each one** — QMUL:
   timetables.qmul.ac.uk (see `course-planner`), UCL: the module page's timetable link, Goldsmiths: the module finder / student timetable —
   and save them to `days` (`provisional: true` until the school finalises timetables). If a time isn't published yet, leave `days`
   empty and set `notes: "times not published yet (checked <date>)"` — the dashboard shows these under the timetable.
6. **Calendar** (if permitted): create all events (`calendar-sync`). **Weekly check-in** (if permitted): create the scheduled task from
   `templates/weekly-checkin-prompt.md` with this folder's path.
7. Set `onboarded: true`; run `python3 scripts/check_data.py`; build and publish the dashboard (`dashboard` skill).

# Finish message (use this structure; no popup at the end)
1. **"Setup is done and your dashboard is published:"** followed by the dashboard link on its own line.
2. **"Here's what I've done:"** one short paragraph in plain words, e.g. "I've collected your degree requirements and how far along you
   are, where you're studying abroad and your program's start and end dates, your Penn Abroad forms and deadlines, and your
   study-abroad emails and bookings. I also have Penn's XCAT approval history for Queen Mary, UCL and Goldsmiths, and I can look up
   modules in all three schools' course catalogs." Only claim what actually succeeded; mention anything on the "Needs you" list in one
   line ("Still to do: …").
3. **"Here's everything I can help with:"** the numbered list in `references/what-i-can-do.md`, word for word (it's written for students).
4. If `me/pending-request.md` exists: "You asked earlier: '…'" — answer it, then delete the file.
5. End with: "Let me know what you'd like to work on next, or ask me anything."
