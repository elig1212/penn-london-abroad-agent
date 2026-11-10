# Penn-in-London Study Abroad Agent
New here? Read **[START-HERE.md](START-HERE.md)**.

| Folder | Contents |
|---|---|
| `CLAUDE.md` | The agent's rules (truthfulness labels, approvals, privacy) |
| `.claude/skills/` | One skill per job: onboarding, course-planner, xcat-research, penn-abroad-portal, inbox-scan, documents, budget, calendar-sync, housing-and-london, trip-planner, health-and-insurance, during-program, return-and-reconcile, dashboard, update-agent |
| `knowledge/` | Shared facts with sources and recheck dates (Penn Abroad, XCAT, Penn programs, host schools, UK entry, London) |
| `data-shared/` | XCAT precedent tables (QMUL, UCL, Goldsmiths) and host-school module lists |
| `scripts/` | `qm_module.py` (QMUL module directory), `fx.py`, `expenses.py`, `check_data.py`, `build_dashboard.py` — Python 3 standard library only |
| `templates/me/` | Blank personal files + schema (`README.md`) |
| `me/` | Your private data — git-ignored, never shared |
