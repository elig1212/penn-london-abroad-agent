---
name: gen-ed-finder
description: Find host-school courses that could satisfy a Penn general-education requirement (College sectors/foundations, Wharton gen-ed) — first from XCAT precedents, then from new matches. Use for "I need Sector 6", "anything for Cross Cultural Analysis at UCL?", "Wharton humanities options at Goldsmiths".
---
# Gen-ed finder
**Rule that decides everything** [FACT, college.upenn.edu/node/234, checked 2026-11-10]: abroad credit counts toward a College
sector only when the department awards it as the number of a **Penn course approved for that sector**. Study-abroad catch-all
numbers (HIST 18xx/19xx, URBS 298x, PSYC 298x/3985, COMM 2985, x982 etc.) don't carry gen-ed attributes. Penn History
won't approve abroad courses for sectors at all. Sector courses must be taken for a letter grade.

## Step 1 — precedents at the user's school
`python3 scripts/geneds.py --school <qmul|ucl|goldsmiths|all> --need "<sector 6 | AUPW | wharton social science …>"`
(`--codes` lists names; `--list` shows every precedent with attributes). Report hits as [PRECEDENT] with expiry dates.
Data: `data-shared/xcat-precedents-*.csv` × `data-shared/penn-course-attributes.csv`. Attributes come from one recent Penn
offering; confirm in Path@Penn. If the precedent tables are older than ~3 months, refresh (`xcat-research`), then run
`python3 scripts/penn_attrs.py build`.

## Step 2 — no precedent? find a new match
1. Get the list of Penn courses carrying the attribute: `data-shared/penn-sector-lists.md` (AUPW saved) or, for others,
   read catalog.upenn.edu/attributes/<code>/ in Chrome (the catalog blocks scripts) and save the list there.
2. Search the host school's catalogue for modules whose content matches one of those Penn courses (intro astronomy ↔ ASTR 0001,
   physical geography/earth systems ↔ EESC 1000, phonetics ↔ LING 2210, …). QMUL: `python3 scripts/qm_module.py --search <prefix>`
   then `qm_module.py CODES…` for term, level, assessment, prerequisites. Check the user's term and exam constraints and timetable.
3. Present as [SUGGESTION]: host module · term · exam? · days · the specific sector-approved Penn course to request in XCAT ·
   risk notes (content overlap, level, department policy). Credit is only confirmed by an XCAT decision; prepare (don't submit) the request.
4. Record useful findings for everyone in `me/core-suggestions.md` (or, for the maintainer, in `data-shared/`).
