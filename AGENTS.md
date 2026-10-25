# AGENTS.md

This repository is an AI Business Leadership System: a team of ten specialist "officers" that advises one client organization at a time.

Before doing anything, read:
1. `.agent/rules/leadership-system.md` (operating rules, routing, authority limits)
2. `shared/context-protocol.md` (how to find and use the active client's profile)

Officers are skills in `.agent/skills/<name>/SKILL.md`. Slash-command workflows are in `.agent/workflows/`. Client data lives in `clients/` and is confidential: never commit it, never mix clients.

If your tool does not read `.agent/` natively, load the rule file as your system instructions and read a skill's `SKILL.md` when a request matches its description.
