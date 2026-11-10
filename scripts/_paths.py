"""Where the user's private planner data lives.
Order: $PLANNER_DATA → ./planner-data (plugin mode: run from the user's Study Abroad folder) → <repo>/me (folder mode)."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def data_dir():
    env = os.environ.get("PLANNER_DATA")
    if env: return os.path.abspath(os.path.expanduser(env))
    here = os.path.join(os.getcwd(), "planner-data")
    if os.path.isdir(here): return here
    return os.path.join(ROOT, "me")
