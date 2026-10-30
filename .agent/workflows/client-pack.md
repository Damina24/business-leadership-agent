---
description: Produce ONE client-ready PDF that brings together everything done for the active client, ready to hand over and act on.
---

# /client-pack

Use the `chief-of-staff` skill. Follow `shared/context-protocol.md`. The result is a single PDF the client can read on its own, with no loose files.

1. **Gather.** Read the profile, the decision log, every report in `clients/<slug>/outputs/reports/`, the working files in `clients/<slug>/outputs/` (prospect pipeline, experiment backlog, and so on), and `data/` notes. Use the newest version where reports overlap.
2. **Confirm three things** with the person running this, in one message, and ask nothing else:
   - Who the document is addressed to (name and role). Default: the decision-maker in profile section 0.
   - Who it is from (consultant or business name, and contact details).
   - Anything to leave out because it is confidential or not for the client.
3. **Write one document** at `clients/<slug>/outputs/client-pack/client-pack.md` using `templates/client-pack/client-pack-template.md`. Keep its section order. Rules:
   - Write for the client's decision-maker in plain language. Explain any term the first time it appears.
   - Fold in everything that matters from the reports, pipeline, experiments, and decision log. Put detail in the appendices so the first pages stay short.
   - Never mention officers, skills, workflows, file names, or folders. Do not copy internal notes, review chatter, or working labels.
   - Say "Based on our research" for figures we researched (with the source) and "you told us" for facts the owner gave. Do not blur the two.
   - Keep every number's label (VERIFIED, ESTIMATE, ASSUMPTION), in capital letters. List all assumptions and data gaps in Appendix A with how to confirm each one.
   - Every recommendation states the action, who, by when, cost, expected result, and how it is measured.
   - State plainly what needs the client's approval. Nothing is presented as already decided.
   - Include other officers' disagreements fairly, with the trade-off, as in the decision brief.
   - Replace every `[[...]]` placeholder. Delete the author guide comment.
4. **Client-ready check.** Run `shared/quality-gate.md`, then check: no facts from any other client, no personal details beyond what the client already owns, arithmetic re-checked, dates consistent, version and date filled in.
5. **Build the PDF.** From the project folder run:
   `python scripts/build_client_pack.py clients/<slug>`
   Use `py` instead of `python` on Windows if needed. If the `markdown` package is missing, run `pip install markdown`. The script refuses to build while placeholders remain, warns about internal wording, and saves `<slug>-client-pack-<date>.pdf` beside `client-pack.md`.
6. **Check the result.** Confirm the script printed a page count, that the PDF text has no leftover `[[`, and that tables and sections look complete. Fix and rebuild if not.
7. **Record it.** Add a line under the decision log table: `Client pack v<version> issued <date>: <file name>`.
8. **Hand back.** Tell the person where the PDF is. Remind them to read it before sending, and that every recommendation still needs the client's own approval.
