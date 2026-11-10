---
name: course-planner
description: Choose and track host-school courses against Penn degree requirements — fit, credit, exams, timetable clashes, prerequisites. Use for "which classes should I take", module changes, add/drop, schedule questions.
---
# Course planner
Inputs: `me/requirements.json`, `me/courses.json`, `me/profile.json`, `data-shared/xcat-precedents-<school>.csv`,
`knowledge/institutions/<school>.md`, `knowledge/programs/<penn school or major>.md`.

For each candidate course collect (and cite):
- Host facts: term offered, level, credits, assessment (is there an exam in the central exam period?), prerequisites,
  **days/times** (mark `provisional: true` until the school finalises timetables), open to visiting students?
  - Queen Mary: `python3 scripts/qm_module.py CODE…` (directory) and timetables.qmul.ac.uk → Modules (max 8 per query, List view).
  - Other schools: use their module catalogue/timetable in Chrome; if you build a fetcher, add `scripts/<school>_module.py`
    and note it in `me/core-suggestions.md`.
- Penn side: XCAT precedent (exact code match, expiry), likely Penn equivalent, which requirement it could fill
  (major / minor / gen-ed sector or foundation). Check gen-ed attributes of the Penn equivalent in Path@Penn course search
  (attributes like AUPW = Physical World). Study-abroad catch-all numbers (e.g. x98x) usually don't carry sector attributes.
- Department rules in `knowledge/programs/` (e.g. Penn Econ: no credit for business courses; ≥6 ECON CU at Penn).

Output a table: course · term · level · exam? · days/times · precedent/needs XCAT · requirement filled · risks · verdict
(KEEP / ADD / DROP / MAYBE), labelled [FACT]/[PRECEDENT]/[SUGGESTION]. Check for timetable clashes across the whole plan.
Remember: only an XCAT decision confirms credit — advisors can't pre-confirm.
Update `me/courses.json` and add deadline/tasks (registration window, add/drop dates) after the user agrees.
