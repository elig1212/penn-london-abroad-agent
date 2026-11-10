---
name: xcat-research
description: Look up and refresh XCAT precedents for any host school, and prepare (not submit) XCAT requests. Use for "has Penn approved X before", "what courses have precedent", "draft my XCAT request".
---
# XCAT research
Public precedent search (no login): https://xcat.at.upenn.edu/searchPrecedents
1. Institution field is fuzzy; type part of the name and read ALL matching options — schools appear under several names
   (QMUL: "Study Abroad at Queen Mary, University of London" = "Study Abroad Queen Mary College (BQM)").
   Also search External Course ID by code prefix (e.g. "ECN") with no institution, to catch odd listings.
2. Set "Rows per page" to 100. Extract rows with JS from `[role=row]` cells (credit type, country, institution, ext id,
   ext title, Penn course, Penn title, subject, CU, expiration). Tool output is ~1,000 chars per call — slice it.
3. Save to `data-shared/xcat-precedents-<school>.csv` (columns: credit_type,xcat_institution,ext_id,ext_title,penn_course,cu,expires,retrieved)
   and update `data-shared/README.md`. On a friend's machine, propose via `me/core-suggestions.md` instead of editing.
4. Interpreting: precedent ≠ approval; expired precedents still hint at how reviewers think; Penn equivalents like
   ECON 4982 / PSYC 3985 / HIST 1865 are study-abroad catch-alls.

## Preparing a request (do NOT submit unless the user explicitly asks for that request)
Gather: host syllabus/module outline (QMUL: study-abroad@qmul.ac.uk ≤8 syllabi per email, or AskQM; Econ QMPlus page),
contact hours, assessment, prerequisites, the Penn course or requirement requested, and a short justification.
Save the draft in `me/xcat-drafts/<code>.md`, set `courses.json → xcat.status = "drafted"`, add a task.
Penn Econ evaluation takes ~2 weeks; approval must come before taking the course. Track status by reading XCAT (logged in)
and update `xcat.status`/`decision`.
