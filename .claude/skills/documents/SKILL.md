---
name: documents
description: Keep track of important documents (acceptance letter, lease, ETA, insurance, bookings) with key dates. Use for "save this document", "where is my lease", "when does my ETA expire".
---
# Documents
- ID documents (passport, ETA, visas, national ID): `kind: "note-only"` — type, issued/expiry dates, where the original is.
  Never store document numbers or scans.
- Everyday documents: may save a copy to `me/documents/<yyyy-mm-dd>-<slug>.<ext>` (`kind: "copy"`), after asking.
- Gmail attachments: use the attachment download tool into `me/documents/`, then record in `me/documents.json`.
- Add expiries and key dates (lease start/end, deposit return, notice periods) to `me/deadlines.json`.
- Passport must be valid for the whole stay; check gov.uk entry rules for the user's nationality before departure.
