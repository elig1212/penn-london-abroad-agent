---
name: reset-onboarding
description: Maintainer-only test helper. Undoes everything the onboarding skill set up so it can be tested again from a clean slate — disconnects the Gmail and Google Calendar connectors, signs Chrome out of the Google accounts, removes Claude in Chrome, and optionally deletes the calendar events, weekly check-in task and planner folder that onboarding created. Use for "reset onboarding", "undo my setup", "clean slate to test onboarding again". Never part of the shipped plugin.
---
# Reset onboarding (maintainer test helper)
Undo what `onboarding` (and `references/getting-connected.md` §A–C) set up, so the next onboarding run starts from "nothing connected".
This skill is **excluded from the plugin build** (`scripts/build_plugin.py`). Never run it for anyone except the maintainer on their own machine.

## Rules
- **One confirmation popup at the start is the approval** for everything ticked in it. Don't ask again per step, except for a
  permanent deletion that turns out larger than expected (e.g. more than 40 calendar events, or a planner folder that doesn't look like one).
- **Order matters.** Steps that need the Calendar connector or Claude in Chrome run *before* those are removed. Claude in Chrome is removed last.
- Never type passwords. Never touch Google account settings beyond signing out. Prefer Trash over permanent delete for files.
- **Never stop for one failed step:** note it in a "Still to do by hand" list and keep going.
- A progress line before each step ("Step 3 of 7: Disconnecting Gmail…") and a ✓ or ✗ result line after it.

## Step 0: What to reset (one AskUserQuestion call, multiSelect)
question "Which parts of the onboarding setup should I undo?", header "Reset", multiSelect true, options:
- **Core reset (Recommended)**: disconnect the Gmail and Calendar connectors, sign Chrome out of Google, remove Claude in Chrome
- **Calendar events**: delete the "[Abroad] …" events that onboarding added
- **Check-in task**: delete the weekly Monday check-in scheduled task
- **Planner folder**: move `~/Documents/Penn London Planner*` to the Trash and delete `~/.penn-london-planner`

Treat "Other" text as extra instructions. If nothing is ticked, stop.

## Step 1: Calendar events (if ticked; needs the Calendar connector, so do it first)
1. Find the planner data: `$PLANNER_DATA`, otherwise the folder in `~/.penn-london-planner` + `/planner-data`, otherwise this repo's `me/`.
2. Collect every `calendar_event_id` from `deadlines.json` (and `courses.json` if it has any).
3. Load the Google Calendar tools with ToolSearch. Delete each id. Also search the primary calendar for events whose summary starts with
   `[Abroad]` (the onboarding/calendar-sync format) and delete only those. Never delete any other event.
4. Result line: "✓ Deleted N [Abroad] events". If the connector is already gone, add the events to "Still to do by hand".

## Step 2: Weekly check-in task (if ticked)
ToolSearch `select:mcp__scheduled-tasks__list_scheduled_tasks,mcp__scheduled-tasks__delete_scheduled_task`. List tasks and delete the ones
whose prompt or name matches the weekly check-in (from `templates/weekly-checkin-prompt.md`: weekly / Monday / study abroad / planner).
If there are several candidates and it's unclear which, show them in one popup and let the user pick.

## Step 3: Disconnect the Gmail and Google Calendar connectors (core)
These are account-level claude.ai connectors. Turning them off for this session only (`set_session_connector_enabled`) is **not** enough.
1. Load the Claude in Chrome tools in one ToolSearch call:
   `select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__tabs_create_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__find,mcp__claude-in-chrome__computer,mcp__claude-in-chrome__read_page,mcp__claude-in-chrome__get_page_text`
   then `tabs_context_mcp` and open a **new** tab.
2. Navigate to `https://claude.ai/settings/connectors`. For **Gmail** and then **Google Calendar**: open the connector's row or menu
   (`find` "Gmail" / "Google Calendar", then its "…" / settings control), click **Disconnect**, and confirm the dialog if it asks.
   Read the page again to check that each one now shows **Connect**.
3. If Chrome isn't connected or the page layout has changed so that you can't find the control, fall back to by-hand steps:
   "Claude app → Settings → Connectors → Gmail → Disconnect; same for Google Calendar."
4. Note: this session may keep showing the Gmail/Calendar tools until the app is restarted or a new session starts. That's expected.
   Onboarding's re-check happens in a fresh session.

## Step 4: Sign Chrome out of the Google accounts (core)
1. In the same Chrome tab, check what is signed in: navigate to `https://mail.google.com/mail/u/0/`, `/u/1/`, `/u/2/` and read the titles
   (the "… - <address> - Gmail" format). Note the addresses in your result line. Don't store them anywhere.
2. Navigate to `https://accounts.google.com/Logout`. This signs out **every** Google account in that Chrome profile, which is what a clean
   onboarding test needs. It does **not** turn off Chrome sync or remove the Chrome profile.
3. Re-check `https://mail.google.com/mail/u/0/`: it should land on a Google sign-in / account chooser page, not an inbox.
4. Optional cleanup: the account chooser may still list the accounts as "Signed out". That doesn't affect onboarding (its check reads the
   inbox titles). Only remove them if the user asked: on `https://accounts.google.com/AccountChooser` → "Remove an account".
5. If the Chrome profile itself is signed in to Google with sync on (avatar at top-right shows "Sync is on"), say so in "Still to do by hand"
   only if the user wants a fully signed-out profile ("Chrome → Settings → You and Google → Turn off"). Don't change it yourself.

## Step 5: Remove Claude in Chrome (core; always last)
Extension pages (`chrome://…`) can't be driven by the extension itself, and computer use only gets read access to Chrome, so the user
clicks **Remove**. Claude opens the right page for them.
1. Find the extension id (don't guess): look for the manifest whose `"name"` contains "Claude" in
   `~/Library/Application Support/Google/Chrome/*/Extensions/*/*/manifest.json`
   (`grep -l '"name": *"Claude' …`; the id is the folder name after `Extensions/`). At last check it was
   `fcoeoabgfenejglbffodgkkbkcdhcgfn`. If the manifest search finds a different id, use that one.
2. Run `open -a "Google Chrome" "chrome://extensions/?id=<id>"` (or just `chrome://extensions` if no id was found).
3. One line: "In the Chrome window I just opened, click **Remove** under Claude, then confirm **Remove**."
   One AskUserQuestion popup: "Click when you've removed Claude in Chrome." with options "Done" · "Skip this".
4. Re-check: `tabs_context_mcp` should now fail, **and** the manifest search from step 1 should find nothing (Chrome deletes the folder
   within a few seconds; check again once if it is still there).

## Step 6: Planner folder (if ticked)
1. Read `~/.penn-london-planner` (a single folder path). Candidates: that folder, plus `~/Documents/Penn London Planner`,
   `~/Documents/Penn London Planner 2`, 3, ….
2. Only touch a folder that contains `planner-data/` (or is empty). Anything else → skip it and report it.
3. Move each to the Trash: `mv "<folder>" ~/.Trash/"<name> (reset $(date +%Y%m%d-%H%M%S))"`. Then `rm ~/.penn-london-planner`.
4. Never touch this repo's `me/` folder. If the user wants folder-mode data reset too, they say so explicitly.

## Step 7: Summary
A short table: item · ✓ done / ✗ still to do by hand. Then the "Still to do by hand" list, if any. Then:
"Ready to test. Open a **new** session (connector changes only show up in a fresh session) and run onboarding."
