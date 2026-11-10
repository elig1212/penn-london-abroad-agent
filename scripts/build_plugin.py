#!/usr/bin/env python3
"""Build the Claude plugin (dist/penn-london-planner.plugin) from the shared core.

Usage: python3 scripts/build_plugin.py [VERSION]        (default version 0.1.0)

Sources: plugin-src/core/SKILL.md (core rules), .claude/skills/* (job skills, paths rewritten for plugin mode),
knowledge/, data-shared/, scripts/, templates/. Personal data (me/) is never included.
"""
import json, os, re, shutil, sys, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = "penn-london-planner"
OUT = os.path.join(ROOT, "dist", NAME)
PR = "${CLAUDE_PLUGIN_ROOT}"
SKIP_SCRIPTS = {"build_plugin.py", "build_web.py"}

PLUGIN_UPDATES = """---
name: plugin-updates
description: Explains how this study abroad planner gets updated and how to send improvements to the maintainer. Use for "update yourself", "is there a newer version", "share this with my friends", or "send my suggestions".
---
# Plugin updates and sharing
Read the **study-abroad-planner** skill first for the core rules.
- This planner is a Claude plugin. Its shared knowledge (Penn/London facts, XCAT precedents) is bundled inside it and was
  snapshotted on the date shown in `${CLAUDE_PLUGIN_ROOT}/data-shared/README.md`.
- **Updating:** the maintainer (Eli) sends a newer `penn-london-planner.plugin` file. The user adds it the same way as the first
  time (open the file in the Claude app and accept). Their `planner-data/` folder is untouched by updates.
- **Sharing:** friends get the same `.plugin` file plus the one-page setup steps in the plugin README.
- **Suggesting improvements:** collect new generic facts (with sources) in `planner-data/core-suggestions.md`; offer to draft an
  email or message to the maintainer with them (send only after the user approves).
- Never edit files inside the plugin folder.
"""

README = """# Penn London Planner (Claude plugin)
A study-abroad planner for Penn students spending a semester in London (Queen Mary, UCL, Goldsmiths).
It tracks deadlines, Penn Abroad forms, courses and Penn credit (XCAT precedents and gen-ed/sector matches), budget in USD,
bookings, documents, housing and trips, and can read your Gmail and the Penn sites you sign in to (with Claude in Chrome).

## Setup (about 5 minutes)
1. Install the Claude desktop app (claude.ai/download) and sign in.
2. Install the **Claude in Chrome** extension and sign in with the same account (lets Claude read Penn sites after you sign in).
3. Optional but useful: in Claude → Settings → Connectors, connect **Gmail** and **Google Calendar**.
4. Open the `penn-london-planner.plugin` file in the Claude app and accept it.
5. In Cowork, open or create a folder called **Study Abroad**, then say: **"Set me up for study abroad."**

## Privacy
Your plan is saved only in `Study Abroad/planner-data/` on your computer. Claude never types your passwords, and it always asks
before submitting forms, sending email, adding calendar events or booking anything. Passport/ETA/visa details are kept as notes only.
Credit is only confirmed by an XCAT decision; precedents are hints, not guarantees.
"""


def rewrite(text):
    text = re.sub(r"python3 scripts/([\w/.\-]+)", lambda m: f'python3 "{PR}/scripts/{m.group(1)}"', text)
    for d in ("scripts/", "knowledge/", "data-shared/", "templates/"):
        text = re.sub(r"(?<![\w/}])" + re.escape(d), PR + "/" + d, text)
    text = re.sub(r"(?<![\w/.-])me/", "planner-data/", text)
    text = text.replace("CLAUDE.md", "the study-abroad-planner core skill")
    text = text.replace("git pull", "(plugin mode: no git)")
    return text


def build(version):
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, ".claude-plugin"))
    json.dump({"name": NAME, "version": version,
               "description": "Study-abroad planner for Penn students in London: deadlines, Penn Abroad forms, XCAT/gen-ed credit, budget, bookings, housing and trips.",
               "author": {"name": "Eli Garber"}, "repository": "https://github.com/elig1212/penn-london-abroad-agent",
               "keywords": ["study-abroad", "penn", "london", "xcat"]},
              open(os.path.join(OUT, ".claude-plugin", "plugin.json"), "w"), indent=2)
    sk = os.path.join(OUT, "skills"); os.makedirs(sk)
    shutil.copytree(os.path.join(ROOT, "plugin-src", "core"), os.path.join(sk, "study-abroad-planner"))
    for name in sorted(os.listdir(os.path.join(ROOT, ".claude", "skills"))):
        if name == "update-agent": continue
        src = open(os.path.join(ROOT, ".claude", "skills", name, "SKILL.md")).read()
        fm_end = src.index("---", 3) + 3
        body = rewrite(src[fm_end:])
        if name == "dashboard":
            body += ("\n4. Plugin mode: if no publish tool is available, open `planner-data/dashboard.html` in the browser instead "
                     "and tell the user where the file is.\n")
        if name == "onboarding":
            body = body.replace("copy `" + PR + "/templates/me/*` into `planner-data/`",
                                "create `planner-data/` in the user's Study Abroad folder and copy `" + PR + "/templates/me/*` into it")
        os.makedirs(os.path.join(sk, name))
        open(os.path.join(sk, name, "SKILL.md"), "w").write(re.sub(r"(?<![\w/.-])me/", "planner-data/", src[:fm_end]) + "\nRead the **study-abroad-planner** skill first for the core rules.\n" + body)
        sdir = os.path.join(ROOT, ".claude", "skills", name)
        for dp, _, fs in os.walk(sdir):
            for f in fs:
                if dp == sdir and f == "SKILL.md": continue
                src_f = os.path.join(dp, f); dst_f = os.path.join(sk, name, os.path.relpath(src_f, sdir))
                os.makedirs(os.path.dirname(dst_f), exist_ok=True)
                if f.endswith(".md"): open(dst_f, "w").write(rewrite(open(src_f).read()))
                else: shutil.copy2(src_f, dst_f)
    os.makedirs(os.path.join(sk, "plugin-updates"))
    open(os.path.join(sk, "plugin-updates", "SKILL.md"), "w").write(PLUGIN_UPDATES)
    for d in ("knowledge", "data-shared", "templates"):
        shutil.copytree(os.path.join(ROOT, d), os.path.join(OUT, d), ignore=shutil.ignore_patterns(".DS_Store"))
    shutil.copytree(os.path.join(ROOT, "scripts"), os.path.join(OUT, "scripts"),
                    ignore=lambda d, fs: [f for f in fs if f in SKIP_SCRIPTS or f == "__pycache__" or f.endswith(".pyc")])
    open(os.path.join(OUT, "README.md"), "w").write(README)
    pkg = os.path.join(ROOT, "dist", NAME + ".plugin")
    if os.path.exists(pkg): os.remove(pkg)
    with zipfile.ZipFile(pkg, "w", zipfile.ZIP_DEFLATED) as z:
        for dp, _, fs in os.walk(OUT):
            for f in fs:
                if f == ".DS_Store": continue
                full = os.path.join(dp, f); z.write(full, os.path.relpath(full, OUT))
    n = sum(len(fs) for _, _, fs in os.walk(OUT))
    print(f"built {OUT} ({n} files) → {pkg} ({os.path.getsize(pkg)//1024} KB), version {version}")


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else "0.1.0")
