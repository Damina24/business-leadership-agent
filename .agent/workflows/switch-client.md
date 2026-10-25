---
description: Switch the active client. Updates clients/ACTIVE and gives a short briefing on that client's state.
---

# /switch-client

Use the `chief-of-staff` skill.

1. List the folders in `clients/` (ignore `README.md`) and ask which client to activate. If the owner gave a name, match it to a slug.
2. Write the slug as the only line of `clients/ACTIVE`.
3. Read only that client's `profile.md` and `outputs/decision-log.md`.
4. Reply with a short briefing: engagement scope, profile status, the five most recent decisions and their status, any decisions past their review date, and the biggest data gaps.
5. Tell the owner to **start a new conversation** if this one earlier covered a different client, so facts from the previous client cannot carry over.
