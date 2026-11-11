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
4. In the **same message**, always show the link too, on its own line, as a markdown link — e.g.
   "I've opened the install page in Chrome. If you don't see it, use this link:" then `[Install Claude in Chrome](<install link>)`.
   Then: "Click **Add to Chrome**, then open the extension and sign in to Claude with the same account you use in this app."
   Never refer to "the link above" — the link must be in the message you're sending.
If you can't run shell commands (or `open` fails): the same message without "I've opened…".
If the tool error gave no link: open `https://chromewebstore.google.com` in Chrome (and show that link) and tell them to search
"Claude" and pick the extension by Anthropic.
Done popup → re-check tabs_context_mcp. If it still fails, add to "Needs you" with the exact error and continue (steps that need Chrome
fall back to asking the user in chat).

## B. Gmail + Google Calendar connectors (needed for email scans and calendar sync)
Check: ToolSearch for Gmail (search_threads) and Google Calendar (list_calendars). Call `list_calendars` (read-only) to confirm.
Only after §A is finished (the extension is installed and signed in to Claude). Before the permission popup, say clearly:
"Next we connect Gmail and Google Calendar. When Google asks which account to use, choose your **school** email (<school email>) —
even if your Claude account uses a different email."
Permission: "Do I have your permission to connect your school Gmail and Google Calendar? (HIGHLY RECOMMENDED)"
**Preferred — one-click Connect card (tested 2026-11-10):**
1. Load the registry tools: ToolSearch "select:mcp__mcp-registry__search_mcp_registry,mcp__mcp-registry__suggest_connectors".
2. `search_mcp_registry` with keywords ["gmail", "google calendar"] → take the `directoryUuid` of the results named exactly
   "Gmail" and "Google Calendar" (at last check: Gmail 2701e52f-b826-4aaf-8b25-11f2a97c98b0, Google Calendar
   2a838eaa-f7b4-4bc2-bd47-c326f3c813c5 — always use the search result, not these, if they differ). Skip any that show `connected: true`.
3. `suggest_connectors` with those uuids and keywords ["study abroad"]. The app shows a card with a **Connect** button for each.
4. Tell the user: "Click **Connect** on Gmail, and when Google shows its account list, pick **<school email>**. Then do the same for
   Google Calendar."
5. Done popup ("Done" · "Skip this") → re-check with `list_calendars` and a 1-result Gmail search, and confirm the Gmail connector is the
   school account (the result's recipient/viewUrl shows the address). Wrong account → explain: Settings → Connectors → Gmail →
   Disconnect, then Connect again and pick the school address. If a connector still isn't available,
   the app may need a new message or a restart to load it — say so, and continue setup (email/calendar steps go to "Needs you").
**Fallback (no registry tools in this app):** Claude app → Settings → Connectors → Gmail → Connect → choose the Penn Google account →
Allow; same for Google Calendar. Then the Done popup.
Note: the connector links one Google account; a second (personal) inbox is read through Chrome in step C.

## C. Both email accounts signed in on Chrome (school + personal)
**Why (say this once, briefly):** "Claude reads your email through Chrome, so Chrome needs to be signed in to **both** your school email
and your personal email — that's how I find your Penn Abroad and host-school dates, bookings and receipts to build your dashboard and
answer your questions. Any Chrome profile is fine, as long as it's the one where Claude in Chrome is installed."

**C1 — Ask for the two addresses** (onboarding Step 2). Plain chat messages, one at a time — no popup, no options:
"Please type your **school** email address." → wait → "Now please type your **personal** email address." Assume everyone has both.
Save to `profile.emails = {school, personal}` — addresses only. Don't remind them to check spelling; a typo just fails at sign-in.

**C2 — Check what's already signed in:** navigate a tab to `https://mail.google.com/mail/u/0/` and read the title
("Inbox … - <address> - Gmail"); repeat for `/u/1/`, `/u/2/`. Any address already signed in → skip it.

**C3 — Sign in, one tab per address** (only for addresses not yet signed in). Permission popup:
"Do I have your permission to open Gmail sign-in in Chrome and fill in your email addresses, so you just enter your passwords?
(HIGHLY RECOMMENDED)" — Yes · No. On Yes, for each missing address, in its **own new tab**:
1. Navigate to `https://accounts.google.com/AddSession?continue=https://mail.google.com/mail/` (adds an account without signing out
   any other). Never put the email address in a URL.
2. Find the "Email or phone" field, type the address (`form_input` or click + type), then click **Next**.
3. Stop there. Say: "Enter your password in this tab (and approve 2-step verification). For your Penn email you'll be sent to PennKey
   sign-in — sign in there." **Never type passwords or codes.**
Then one Done popup for both tabs ("Done" · "Skip this") → re-check `/u/0/`, `/u/1/`, … titles, and record which `/u/<n>/` belongs to
which address in `profile.emails.chrome_index`. Any still missing → "Needs you".

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
