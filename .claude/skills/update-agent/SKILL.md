---
name: update-agent
description: Update this agent's shared core from GitHub, or (maintainer) publish improvements; also first-time GitHub setup for friends. Use for "update yourself", "share this with my friends", "publish updates".
---
# Update agent
Shared core = everything except `me/` (gitignored). The user never needs to type git commands — you run them.
- **Update (friends):** `git status` (stash nothing in `me/`; it's ignored) → `git pull --ff-only`. If it fails, show why in
  plain English; never force. Then re-read CLAUDE.md, run `python3 scripts/check_data.py`, and summarise what changed (`git log -5 --oneline`).
- **First-time friend setup:** follow START-HERE.md. The repo is public (github.com/elig1212/penn-london-abroad-agent), so
  `git clone` and `git pull` need no GitHub account or sign-in. If git is missing, macOS offers the command line developer tools.
- **The repo is PUBLIC.** Before any maintainer commit, check `git diff --cached --name-only` contains nothing under `me/`
  and no personal data (names of private people, emails, IDs, addresses, grades) anywhere in the diff. If in doubt, stop and ask.
- **Maintainer publishing (Eli only):** review friends' `core-suggestions.md` items the maintainer pastes in, apply good ones to
  `knowledge/`/`data-shared/` with sources, show the diff, commit only when the maintainer says so, then push.
  Commits use the GitHub no-reply email configured in this repo.
