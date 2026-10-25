---
description: Onboard a new client organization. Creates its folder, interviews the owner, and builds the client profile.
---

# /new-client

Run this once per client, before any advice is given. Use the `chief-of-staff` skill.

1. Ask for the organization's name. Create a slug (lowercase letters, numbers, hyphens), and confirm it with the owner.
2. If `clients/<slug>/` already exists, ask whether to continue that profile. If not, pick another slug.
3. Create the folder from `templates/client/`: `clients/<slug>/profile.md`, `clients/<slug>/data/`, `clients/<slug>/outputs/decision-log.md`, and `clients/<slug>/outputs/reports/`.
4. Write the slug as the only line of `clients/ACTIVE`.
5. Interview the owner section by section, following `clients/<slug>/profile.md`. Ask two to four plain-language questions at a time. After each answer, write it into the profile immediately.
   - If the owner does not know a number, write "unknown" and note how to find it. Never invent.
   - Tag numbers VERIFIED, ESTIMATE, or ASSUMPTION.
   - Ask for supporting files (sales records, price list, financials, CRM export) and tell the owner to put them in `clients/<slug>/data/`.
   - Insist on section 10 (approval authority). Every officer depends on it.
6. If data files are present, read them and check them against what the owner said. Note any differences in section 12.
7. Set `status: complete` and `last_updated` once sections 0 to 3, 8, and 10 are filled. List the remaining gaps in section 12.
8. Summarize the profile in five lines, list the three most important data gaps, and suggest a first step (usually `/growth-review`).

Remind the owner that this client folder is confidential and is excluded from Git.
