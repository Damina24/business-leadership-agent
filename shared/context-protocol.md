# Context Protocol

Every officer follows this before giving advice. It grounds advice in the real client and stops facts leaking between clients.

## 1. Identify the active client
1. Read `clients/ACTIVE` (one line: the client slug).
2. If it is missing or empty, ask the owner which client this is, or run `/new-client`. Give no business advice yet.
3. Work only inside `clients/<slug>/`. Never open other folders under `clients/`.
4. If this conversation earlier discussed a different client, tell the owner to start a fresh conversation. Earlier facts may bleed in.

## 2. Check the profile
Open `clients/<slug>/profile.md`.
- `status: incomplete`: run the intake from `/new-client` for the missing sections before advising. If the owner has no data to give (for example a brand-new company), run `/fill-gaps` to research the missing inputs instead. If the owner insists on proceeding, state exactly which gaps exist and label every dependent claim ASSUMPTION.
- `status: complete`: read it fully. It is the source of truth for the business model, constraints, and approval authority.

## 3. Read the evidence
- List `clients/<slug>/data/` and read the files relevant to the question (sales records, CRM exports, price lists, financials).
- Read `clients/<slug>/outputs/decision-log.md` and list `clients/<slug>/outputs/reports/`. Build on earlier work instead of repeating it (Rule 11) and check what happened to past recommendations (Rule 10).

## 4. Fill gaps honestly
- Ask at most three targeted questions when a gap would materially change the answer.
- Otherwise proceed, label the dependent claims ASSUMPTION, and list the data that would replace them.
- For external facts (markets, competitors, regulations, prices), use web search when available and cite the source and date. If you cannot search, say so and label the claim ASSUMPTION. Never invent. Label the Basis of each figure: Owner-provided, Based on research, or Assumed (`shared/evidence-standards.md`). Never copy figures from samples or templates.

## 5. Save your work
- Reports: `clients/<slug>/outputs/reports/YYYY-MM-DD-<officer>-<topic>.md`, using `shared/report-format.md`.
- Every recommendation the owner may act on gets one row in `clients/<slug>/outputs/decision-log.md`.
- Working files (prospect lists, experiment backlogs, forecasts) go in `clients/<slug>/outputs/`.
