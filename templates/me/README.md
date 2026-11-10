# Personal data files (copied to `me/` during onboarding)
Every JSON file is a list of records. Common fields: `id` (short slug), `status`, `source`, `updated` (YYYY-MM-DD).
Labels for `confidence`: "fact" | "precedent" | "suggestion" | "unverified".

| File | Record fields |
|---|---|
| profile.json (object, not list) | name, penn_school (College/Wharton/SEAS/Nursing), majors[], minors[], grad_term, host_school, term, program_dates{arrive_by, orientation, teaching_start, teaching_end, exams_start, exams_end, depart_after}, home_city, emails{penn, personal}, citizenship_note, entry_permission (ETA/Visitor/Student visa), preferences{allow_booking, currency_display:"USD", avoid_exam_period, notes}, health_notes, onboarded |
| requirements.json | id, program (major/minor/gen-ed), name, needed_cu, done_cu, satisfied_by[], notes, source |
| courses.json | id (host code), title, host_school, level, credits_host, term, days[] e.g. [{"day":"Thu","start":"16:00","end":"18:00","type":"Lecture","provisional":true}], assessment, has_exam_in_exam_period, penn_equivalent, penn_requirement, xcat{status: none/precedent/drafted/submitted/approved/denied, precedent_expires, request_date, decision}, host_registration (requested/approved/rejected/dropped), status (considering/registered/dropped/completed), grade, confidence, source |
| deadlines.json | id, date (YYYY-MM-DD), time, tz, title, category (academic/penn-abroad/visa/housing/travel/money/health/other), status (open/done/missed), source, calendar_event_id |
| tasks.json | id, title, due, category, priority (high/med/low), status (todo/doing/done/blocked), notes, source |
| bookings.json | id, type (flight/train/hotel/hostel/bus/event/other), provider, confirmation_ref, start, end, from, to, cost{amount, currency, usd}, status, source (email id) |
| documents.json | id, type, title, kind ("copy" or "note-only"), path (if copy), where_original, issued, expires, notes |
| expenses.csv | date,description,category,amount,currency,usd,fx_rate,fx_date,source,ref |
| budget.json (object) | total_budget_usd, categories{name: planned_usd}, emergency_fund_usd |
| contacts.json | id, name, role, org, email, phone, when_to_use |
| open-questions.md | Unanswered questions, newest first |
| core-suggestions.md | Proposed improvements to shared knowledge (maintainer reviews) |
