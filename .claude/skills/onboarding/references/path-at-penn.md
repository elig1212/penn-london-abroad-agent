# Reading Path@Penn (tested 2026-11-10)
Read-only. Never register, drop or change anything.

1. Navigate to `https://path.at.upenn.edu`. If the tab lands on `weblogin.pennkey.upenn.edu` (title "Penn WebLogin") or a
   `duosecurity.com` page, the user must sign in (see onboarding Step 3). Poll the tab title every few seconds after they click
   "I've signed in"; continue when it shows "Path@Penn".
2. The landing page has an "Academic Planning & Registration" box. Click **"Degree planning and audit"** (use `find`), which opens
   a new tab at `courses.upenn.edu` ("Search Classes"). Use that tab.
3. Click **"DEGREE AUDIT & ADVISING"** (left column). An **Advising** panel opens with: first name, pronouns, Penn ID (don't store),
   expected graduation term, degree, major(s), minor(s), and advisors with roles and emails. Don't use `get_page_text` on this site —
   it returns a huge subject list; read the panel with JS instead:
   ```js
   const el=[...document.querySelectorAll('div,section,aside')].filter(e=>e.innerText&&e.innerText.includes('ADVISORS')&&e.innerText.length<4000).sort((a,b)=>a.innerText.length-b.innerText.length)[0]; el?el.innerText.replace(/\n+/g,' | '):'none'
   ```
4. Click **"Degree Audit"** (button under DEGREE PROGRESS). Rows appear: "Degree in …", "General Education, Foundations",
   "General Education, Sectors", "Major in …", "Minor in …", "Elective Coursework", each with a %. Use `find` to get their refs.
5. Click each row, wait ~4 s, then read its detail panel (replace the heading text):
   ```js
   const c=[...document.querySelectorAll('div,section')].filter(e=>e.innerText&&e.innerText.trim().startsWith('Major in Economics')&&e.innerText.includes('CU')).sort((a,b)=>a.innerText.length-b.innerText.length)[0]; window._r=(c?c.innerText:'none').replace(/\n+/g,' | '); window._r.length+' :: '+window._r.slice(0,950)
   ```
   Tool output is ~1,000 characters per call: read `window._r` in slices (`window._r.slice(950,1900)` …).
   In the text, items marked "completed" are done, "registered" = in progress this term, "partially completed" = still open;
   lines like "12 CU are required. You currently have 6" give totals; "Choose one course with attribute AUPW" names a gen-ed attribute.
6. **In-progress ("registered") courses count as completed.** For every requirement, write it to `me/requirements.json`:
   `{id, program: major|minor|gen-ed, name, needed_cu, done_cu, in_progress_cu, satisfied_by: ["ECON 2100", "ECON 2300 (in progress)"],
   notes, source: "Path@Penn audit <date>"}` — `done_cu` = completed, `in_progress_cu` = currently enrolled at Penn this term. Courses planned or taken abroad never count here until the credit is posted. A requirement whose
   completed + in-progress credits cover it is treated as **satisfied** (dashboards show it done, labelled "in progress"). Only
   requirements still short after counting in-progress courses are "still needed". Also save major/minor/school/grad term to the
   profile and advisors to `me/contacts.json` (`role`, `email`, `when_to_use`).
Wharton/SEAS/Nursing audits use different row names — read whatever rows appear the same way.
