# Start here — Penn-in-London Study Abroad Agent

An AI planner for Penn students spending a semester in London. It tracks your courses and Penn credit (XCAT),
Penn Abroad forms, deadlines, housing, budget, bookings, documents and trips, and gives you a dashboard you can open on your phone.

It runs inside the **Claude desktop app** on your own Mac. Your personal data stays on your computer, in a `me/` folder that is never shared.

## One-time setup (about 10 minutes, no GitHub account needed)
1. **Install the Claude desktop app** (free with your Claude plan): https://claude.ai/download — sign in.
2. **Install Claude in Chrome** (the browser extension) and sign in with the same Claude account. This lets the agent read
   Penn sites like Path@Penn and XCAT *after you sign in yourself*.
3. In the Claude desktop app, open the **Code** tab, start a new session in any folder, and paste:
   > Set up the Penn-in-London study abroad agent for me. Run `git clone https://github.com/elig1212/penn-london-abroad-agent.git ~/AI_Agent_Abroad`,
   > move this session to ~/AI_Agent_Abroad, and run onboarding.
   Approve the prompts it shows you. If your Mac asks to install "command line developer tools" (needed for git), click Install and tell Claude when it's done.
4. Answer the onboarding questions. Skip anything you don't know yet.
5. Optional: connect **Gmail** and **Google Calendar** in Claude's settings → Connectors, so the agent can read Penn Abroad mail
   and add deadlines to your calendar. If your Penn Abroad mail and your booking confirmations go to different inboxes,
   connect one and the agent will read the other in Chrome.

## Using it
Just ask in plain English, for example:
- "What's due this week?"
- "Which modules should I take at UCL for my Wharton concentration?"
- "Has Penn approved Goldsmiths PS52003T before?"
- "Check my email for anything new."  ·  "Log £14 dinner."  ·  "Import this bank statement."
- "Plan a weekend in Edinburgh in February." (It books only if you turned booking on, and asks you every time.)
- "Show my dashboard on my phone."
- **"Update yourself"** — pulls the latest shared Penn/London knowledge. You never need to type git commands.

## What it will and won't do
- It labels things as **fact** (with a source), **precedent** (Penn approved it before; not a guarantee), or **suggestion**.
- It never types your passwords. Sign in yourself when it asks (or use a connected password manager), and approve Duo yourself.
- It always asks before submitting a form, sending an email, booking, or paying. It won't submit XCAT requests unless you ask.
- Only an XCAT decision confirms Penn credit. Advisors can't pre-approve.
- ID documents (passport, ETA) are kept as notes only, never copies or numbers.

## Privacy
The shared files (rules, skills, general Penn/London knowledge, XCAT precedent tables, scripts) are in a public GitHub repo.
Your own data lives only in `~/AI_Agent_Abroad/me/` on your Mac. It is excluded from git and is never uploaded.
Suggestions for improving the shared files go in `me/core-suggestions.md`; send them to Eli.
