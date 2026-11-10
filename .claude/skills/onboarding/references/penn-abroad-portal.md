# Reading the Penn Abroad portal (tested 2026-11-10)
Read-only unless the user explicitly asks to fill a form (then stop before Submit).

1. Navigate to `https://pennabroad.via-trm.com/`. A cookie banner appears — click **Deny** (most private choice).
2. Click **"Go to Portal"** (PennKey). If Path@Penn was just signed in, this usually passes straight through; otherwise ask the user to
   sign in as in onboarding Step 3.
3. The Traveler Dashboard shows **"My To Do List"** and **"My Programs"**. Read them with JS in slices:
   ```js
   const t=document.body.innerText; const i=t.indexOf('My To Do List'); window._p=t.slice(i).replace(/\n+/g,' | '); window._p.slice(0,950)
   ```
   Each form appears as `Form name | Not Started | Due: | Nov 15, 2026 | View / Edit`. "My Programs" shows e.g.
   `SA: Queen Mary, University of London (BQM) | Spring 2027; Jan 2027 - Jun 2027 | Application | Committed | Forms | 7 of 18 Accepted`.
4. Save: each form → `me/deadlines.json` `{id: "pa-<slug>", date, title: "PASSPORT form: <name> (<status>)", category: "penn-abroad",
   status: "open", source: "Penn Abroad portal <date>"}`; program/term/status → `profile.penn_abroad_status` and `profile.term`.
