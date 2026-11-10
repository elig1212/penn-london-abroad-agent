"""Where the user's private planner data lives.
Order: $PLANNER_DATA → ./planner-data → folder named in ~/.penn-london-planner (plugin mode) → <repo>/me (folder mode)."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def data_dir():
    env = os.environ.get("PLANNER_DATA")
    if env: return os.path.abspath(os.path.expanduser(env))
    here = os.path.join(os.getcwd(), "planner-data")
    if os.path.isdir(here): return here
    me = os.path.join(ROOT, "me")
    if os.path.abspath(os.getcwd()).startswith(ROOT) and os.path.isdir(me): return me
    ptr = os.path.expanduser("~/.penn-london-planner")
    if os.path.isfile(ptr):
        folder = open(ptr).readline().strip()
        if folder and os.path.isdir(os.path.join(folder, "planner-data")): return os.path.join(folder, "planner-data")
    return os.path.join(ROOT, "me")
