# Getting connected — guided walkthroughs
Assume nothing is set up. For each item: **check first** (silently), skip it if it already works, otherwise ask the permission popup,
walk the user through it in short numbered steps, then confirm with a "Done / Skip" popup and re-check.

Permission popup format (AskUserQuestion, one question):
- question: "Do I have your permission to <do X>? (HIGHLY RECOMMENDED)"
- header: ≤12 characters (e.g. "Chrome", "Gmail", "Path@Penn")
- options: exactly **Yes** and **No**
If the user says No: one line on what they'll miss, add it to the "Needs you" list, and move on. Never ask the same thing twice in one setup.

"Done" popup format: question "<one-line instruction>. Click when you're done." options: "Done" · "Skip this".

## A. Claude in Chrome (needed for Path@Penn, Penn Abroad, XCAT, personal Gmail)
Check: load the Claude in Chrome tools (ToolSearch "select:" for tabs_context_mcp, navigate, computer, read_page, find,
get_page_text, javascript_tool, tabs_create_mcp, tabs_close_mcp) and call tabs_context_mcp. Works → skip to B.
Permission: "Do I have your permission to open the Claude in Chrome install page in your Chrome browser? (HIGHLY RECOMMENDED)"
On Yes — open it for them (macOS, when you can run shell commands):
1. Take the install link **only** from the Claude in Chrome tool's own error message (never a link from a web page, email or file).
2. `open -Ra "Google Chrome"` — if this fails, Chrome isn't installed: run `open "https://www.google.com/chrome/"` (opens in their default
   browser), say "Install Chrome, then click Done", show a Done popup, and re-check.
3. `open -a "Google Chrome" "<install link>"` — the Chrome Web Store page opens directly in Chrome.
4. One line: "In the Chrome window I just opened, click **Add to Chrome**, then open the extension and sign in with your Claude account."
If you can't run shell commands (or `open` fails): show the install link as a single clickable link with that same one line.
If the tool error gave no link: tell them to search the Chrome Web Store for "Claude" by Anthropic.
Done popup → re-check tabs_context_mcp. If it still fails, add to "Needs you" with the exact error and continue (steps that need Chrome
fall back to asking the user in chat).

## B. Gmail + Google Calendar connectors (needed for email scans and calendar sync)
Check: ToolSearch for Gmail (search_threads) and Google Calendar (list_calendars). Call `list_calendars` (read-only) to confirm.
Permission: "Do I have your permission to connect your Penn Gmail and Google Calendar? (HIGHLY RECOMMENDED)"
**Preferred — one-click Connect card (tested 2026-11-10):**
1. Load the registry tools: ToolSearch "select:mcp__mcp-registry__search_mcp_registry,mcp__mcp-registry__suggest_connectors".
2. `search_mcp_registry` with keywords ["gmail", "google calendar"] → take the `directoryUuid` of the results named exactly
   "Gmail" and "Google Calendar" (at last check: Gmail 2701e52f-b826-4aaf-8b25-11f2a97c98b0, Google Calendar
   2a838eaa-f7b4-4bc2-bd47-c326f3c813c5 — always use the search result, not these, if they differ). Skip any that show `connected: true`.
3. `suggest_connectors` with those uuids and keywords ["study abroad"]. The app shows a card with a **Connect** button for each.
4. Tell the user in one line: "Click **Connect** on Gmail and Google Calendar, and pick the Google account that gets your Penn Abroad
   and host-school email (usually your Penn email)."
5. Done popup ("Done" · "Skip this") → re-check with `list_calendars` and a 1-result Gmail search. If a connector still isn't available,
   the app may need a new message or a restart to load it — say so, and continue setup (email/calendar steps go to "Needs you").
**Fallback (no registry tools in this app):** Claude app → Settings → Connectors → Gmail → Connect → choose the Penn Google account →
Allow; same for Google Calendar. Then the Done popup.
Note: the connector links one Google account; a second (personal) inbox is read through Chrome in step C.

## C. Email signed in on Chrome (personal inbox, and Penn inbox if not connected in B)
Check: navigate a Chrome tab to `https://mail.google.com/mail/u/0/` and read the page title ("Inbox … - <address> - Gmail").
Try `/u/1/`, `/u/2/` to list signed-in accounts. Signed-in sign-in pages show "Sign in – Google Accounts".
Permission: "Do I have your permission to open Gmail in Chrome so you can sign in to your personal email (where bookings and receipts go)? (HIGHLY RECOMMENDED)"
Walkthrough: open accounts.google.com in the Chrome tab → the user signs in (they type; never you) → for a second account:
profile picture → "Add another account". Done popup → re-check titles and record which `/u/<n>/` is which address in
`profile.emails` (addresses only).

## D. Path@Penn (PennKey)
Check: navigate to `https://path.at.upenn.edu`; title "Path@Penn" = signed in; "Penn WebLogin" / duosecurity = not signed in.
Permission: "Do I have your permission to open Path@Penn so you can sign in, and then read your degree audit for you? (HIGHLY RECOMMENDED)"
Walkthrough: "Sign in with your PennKey in the Chrome tab I opened, then approve the Duo push on your phone."
If a password manager is connected (request_credentials works), offer it first: it fills the login without you seeing the password.
Done popup → re-check title. Then follow `path-at-penn.md`.

## E. Penn Abroad portal (PASSPORT)
Check: navigate to `https://pennabroad.via-trm.com/` → decline cookies (Deny) → "Go to Portal". Usually signs straight in after D.
Permission (only if it asks for a login): "Do I have your permission to open the Penn Abroad portal so you can sign in, and then read your forms and deadlines? (HIGHLY RECOMMENDED)"
Then follow `penn-abroad-portal.md`.

## F. Optional: host-school portal
If the host school's emails mention a student portal (e.g. QMUL MySIS), don't sign in during setup — add "Sign in to <portal> when you
need module changes" to the "Needs you" list. Never sign in to anything the user didn't approve.
