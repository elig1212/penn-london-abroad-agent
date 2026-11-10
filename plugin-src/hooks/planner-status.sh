#!/bin/sh
# Penn London Planner: tell Claude where the student's planner folder is, or that setup must run first.
# Pointer file ~/.penn-london-planner holds the folder path (written by onboarding). Default folder: ~/Documents/Penn London Planner
MODE="$1"
PTR="$HOME/.penn-london-planner"
DIR=""
[ -f "$PTR" ] && DIR="$(head -n 1 "$PTR")"
[ -z "$DIR" ] && DIR="$HOME/Documents/Penn London Planner"
PROFILE="$DIR/planner-data/profile.json"
if [ -f "$PROFILE" ] && grep -Eq '"onboarded"[[:space:]]*:[[:space:]]*true' "$PROFILE"; then
  if [ "$MODE" = "start" ]; then
    echo "Penn London Planner is set up for this student. Their planner folder is: $DIR (personal data in planner-data/). Work in that folder (ask the app for access if it isn't open) and read the study-abroad-planner skill before helping with anything study-abroad related."
  fi
  exit 0
fi
cat <<MSG
PENN LONDON PLANNER — FIRST-TIME SETUP REQUIRED.
Before answering the user's message, whatever it is: (1) tell them in one line that you'll set up their planner first (about 10 minutes, mostly clicks) and then come straight back to their request; (2) read the study-abroad-planner and onboarding skills and run onboarding to completion — it creates a NEW folder for the planner (default: $HOME/Documents/Penn London Planner) even if another study-abroad folder already exists; (3) save the user's original request to planner-data/pending-request.md as soon as the folder exists; (4) only after onboarding is fully complete, answer that saved request and then delete the file.
MSG
exit 0
