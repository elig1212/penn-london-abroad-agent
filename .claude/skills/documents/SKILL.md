---
name: documents
description: Keep a clickable archive of important documents (offer/acceptance letter, ETA approval, lease, insurance, bookings) with key dates — saved from email attachments or files the user shares. Use for "save this document", "where is my lease", "when does my ETA expire", "add my offer letter".
---
# Documents
- **Copies allowed:** offer/acceptance letters, ETA approval, lease, insurance card, booking confirmations, receipts, host-school letters.
- **Never copies:** passport, national ID, driver's licence, visa/BRP, or any file showing a passport/ID/SSN number (most application
  forms) → `kind: "note-only"` with type, issued/expiry dates and where the original is. No numbers, no scans.
- **Before saving any copy** run `python3 scripts/doc_check.py FILE`: `OK` → save; `ID-SENSITIVE` → note only (tell the user why);
  `UNKNOWN` → ask the user.
- **Where:** `me/documents/<yyyy-mm-dd>-<short-name>.<ext>` and a record in `me/documents.json`:
  `{id, type, title, kind: "copy", path: "documents/<file>", issued, expires, where_original, notes}`. The dashboard lists every copy
  as a clickable link (archive), and publishing the dashboard uploads the copies alongside it.
- **From email:** find the message (Gmail tools), list its attachments, and save the relevant one with the Gmail attachment download tool
  into `me/documents/`. For important emails without an attachment (e.g. ETA approval), save the email body as a `.html` file.
- **From the user:** files they share (drag in, a path, WhatsApp/Downloads) → check, copy into `me/documents/`, record.
- Each person's documents stay in their own folder. Never put anyone's documents into the shared core (`knowledge/`, `data-shared/`,
  the plugin, or GitHub), and never add one person's documents to another person's planner.
- Add expiries and key dates (lease start/end, deposit return, notice periods, ETA expiry) to `me/deadlines.json`.
