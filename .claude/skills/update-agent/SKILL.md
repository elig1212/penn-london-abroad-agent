---
name: update-agent
description: Update this agent's shared core from GitHub, or (maintainer) publish improvements; also first-time GitHub setup for friends. Use for "update yourself", "share this with my friends", "publish updates".
---
# Update agent
Shared core = everything except `me/` (gitignored). The user never needs to type git commands — you run them.
- **Update (friends):** `git status` (stash nothing in `me/`; it's ignored) → `git pull --ff-only`. If it fails, show why in
  plain English; never force. Then re-read CLAUDE.md, run `python3 scripts/check_data.py`, and summarise what changed (`git log -5 --oneline`).
- **First-time friend setup:** follow START-HERE.md. Needs a free GitHub account + accepted invite; `gh auth login --web`
  (install `gh` via Homebrew if missing, with the user's OK).
- **Maintainer publishing:** review friends' `core-suggestions.md` items the maintainer pastes in, apply good ones to
  `knowledge/`/`data-shared/` with sources, show the diff, commit only when the maintainer says so, then push.
- If GitHub proves too hard for a friend: fallback is a shared Google Drive folder containing the core (no `me/`), with the
  maintainer as the only editor.
