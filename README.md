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

## Web planner
`web/planner.template.html` + `scripts/build_web.py` → `web/planner.html`, published on claude.ai (the same link for everyone; each
viewer's data is stored privately per person by claude.ai). After changing `knowledge/` or `data-shared/`, run
`python3 scripts/build_web.py` and republish `web/planner.html` with the Artifact tool (same file path keeps the link).
`web/friend-test.html` is a one-minute capability test for new viewers.

## Claude plugin (recommended for friends)
`python3 scripts/build_plugin.py [version]` builds `dist/penn-london-planner.plugin` from this repo: the core rules
(`plugin-src/core/SKILL.md`), every skill in `.claude/skills/` (paths rewritten for plugin mode), `knowledge/`, `data-shared/`,
`scripts/` and `templates/`. In plugin mode each user's data lives in `planner-data/` inside their own "Study Abroad" folder
(scripts find it via `scripts/_paths.py`). Bump the version and send friends the new file after changing the shared core.
