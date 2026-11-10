---
name: penn-abroad-portal
description: Track and help complete Penn Abroad PASSPORT (Terra Dotta / via-trm.com) forms, questionnaires and deadlines. Use for "what do I still owe Penn Abroad", form reminders, health form, commitment steps.
---
# Penn Abroad portal
- Mail comes from messages@via-trm.com and goabroad@upenn.edu to the Penn inbox. Search: `from:(via-trm.com OR goabroad@upenn.edu)`.
- Portal: Penn Abroad PASSPORT (linked in those emails). User signs in with PennKey (see CLAUDE.md logins).
1. List every application item (questionnaires, signature docs, uploads, learning content) with status and due date.
2. Mirror them into `me/deadlines.json` (category penn-abroad) and `me/tasks.json`; cite the portal page/email.
3. Helping fill a form: read the questions, draft answers from `me/` data, show the user, fill fields only after approval,
   and **stop before Submit** for an explicit yes. Health forms: ask the user for answers; don't infer medical info.
4. Record new generic facts (form names, typical deadlines) in `me/core-suggestions.md` for `knowledge/penn-abroad.md`.
