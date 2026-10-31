---
description: Produce ONE client-ready PDF that brings together everything done for the active client, ready to hand over and act on.
---

# /client-pack

Use the `chief-of-staff` skill. Follow `shared/context-protocol.md` and the consulting standard in the rules. The result is a single PDF the client can read on its own.

**Hard rules for this command**
- The ONLY deliverable is the PDF. Work only inside `clients/<slug>/outputs/client-pack/`. Never create any other summary or pack file, and never put files directly in `clients/<slug>/`.
- Never say the pack is done, and never give a file path, until you have listed `clients/<slug>/outputs/client-pack/` and seen the PDF there. Quote the build command's `PDF ready: ... (N pages)` line in your reply.
- If any command fails, or no PDF exists, say so plainly, show the exact error, and fix it. Never report success.
- Write one section file per edit and save after each. Save as UTF-8 and write the naira sign as ₦.
- Use `py` instead of `python` on Windows. If the `markdown` package is missing, run `pip install markdown`. If you cannot run commands, give the owner the exact commands to run in CMD.

**Steps**
1. **Prepare.** Run `python scripts/build_client_pack.py clients/<slug> --init`. This creates one small file per section in `clients/<slug>/outputs/client-pack/sections/`, from `templates/client-pack/sections/`.
2. **Gather.** Read the profile, `data/` notes, the decision log, every report in `clients/<slug>/outputs/reports/`, and the working files in `clients/<slug>/outputs/`. Use the newest version where reports overlap.
3. **Confirm three things** with the owner in one message, and ask nothing else: who the document is addressed to (default: the decision-maker in the profile), who it is from (default: the business name), and anything to leave out. If the owner does not answer, use the defaults and continue.
4. **Write the sections, one file at a time.** Open each file in `sections/`, read its `WRITE THIS SECTION` hint, do any research it asks for with web search (source URL and date for every finding), then replace the whole file with the finished text, keeping its heading. Write in this order: 04, 05, 06, 07, 08, 09, 12, 13, 14, 15, 16, 17, then 03, 02, 10, 11, 01 and finally 00.
   - Write for the client's decision-maker in plain language. Never mention officers, skills, workflows, commands, file names, or folders.
   - The document gives answers, not tasks. Never write "choose", "decide", "supply" or "provide" as an action for the client where research can answer it. State the chosen customer group, offer, price, prospects, scripts and plan. The client's only decisions are to approve or override.
   - Where material is missing from the reports (prospects, scripts, prices, costs, legal steps), research it now and write it in. Do not leave a gap and do not ask the owner for it.
   - Say "based on our research" for researched figures (with the source) and "you told us" for facts the owner gave. Keep every number's label (VERIFIED, ESTIMATE, ASSUMPTION) in capitals. Show the arithmetic for every forecast.
   - Never invent a business, contact, price or statistic. Prospect entries need a source URL.
5. **Check.** Run `python scripts/build_client_pack.py clients/<slug> --status`. It lists every section that is missing, unfinished or empty. Fix each one and run it again until it says all sections are complete.
6. **Quality gate.** Run `shared/quality-gate.md`, including the consulting test. Fix anything it finds.
7. **Build.** Run `python scripts/build_client_pack.py clients/<slug>`. Read any warnings (wording that hands work to the client, internal names, fewer than 30 prospects) and fix them, then build again.
8. **Verify and record.** List the folder and confirm the PDF is there. Add a line under the decision log table: `Client pack v<version> issued <date>: <file name>`.
9. **Hand back.** Tell the owner the PDF's location and the page count. Remind them to read it before sending, and that every recommendation still needs the client's own approval.
