# AI Business Leadership Agent

A reusable team of ten AI "officers" that advises one client organization at a time on growth, clients, revenue, strategy, and operations. Built for Google Antigravity, and it works with any agent tool that supports `SKILL.md` skills or `AGENTS.md`.

You describe a client once. The team then reasons from that client's real profile and data, labels what is verified and what is assumed, and logs every recommendation so results can be tracked.

## The team

| Officer | Skill | Accountable for |
|---|---|---|
| Chief Growth Officer | `chief-growth-officer` | Overall growth agenda and prioritization |
| Business Growth Strategist | `growth-strategist` | Finding and designing growth options |
| Business Development Manager | `business-development-manager` | Prospects, partnerships, proposals, pipeline |
| Chief Strategy Officer | `chief-strategy-officer` | Long-term direction and strategic risk |
| Revenue Growth Manager | `revenue-growth-manager` | Pricing, retention, revenue quality |
| Head of Growth | `head-of-growth` | Campaigns, funnel, experiments |
| Chief Operating Officer | `chief-operating-officer` | Ability to deliver; capacity checks |
| **Chief of Staff** (added) | `chief-of-staff` | Routing, handoffs, conflicts, decision log |
| **Chief Financial Officer** (added) | `chief-financial-officer` | Cash, budgets, unit economics, ROI |
| **Risk and Compliance Officer** (added) | `risk-compliance-officer` | Legal, privacy, claims, reputational risk |

The three added officers fill gaps in the original seven: nobody coordinated the team, nobody owned the financial numbers, and nobody owned legal and privacy risk (especially for outreach).

## Quick start (Antigravity)

1. Clone this repo: `git clone <this-repo-url>`
2. Open the cloned folder in Antigravity (**File > Open Folder**).
3. Check the Rules, Skills, and Workflows panels. You should see the `leadership-system` rule, ten skills, and seven workflows.
4. In the agent chat, type `/new-client`. The agent interviews you and builds the client profile.
5. Then try `/growth-review`, or just ask a question such as "How do we get more clients?".

### Folder name note
Antigravity's workspace folder has been `.agent/` and newer versions default to `.agents/`, while keeping `.agent/` working. This repo uses `.agent/`. If your panels show nothing, rename `.agent` to `.agents` and reopen the folder.

## Commands

| Command | What it does |
|---|---|
| `/new-client` | Creates a client folder and interviews you to build the profile |
| `/switch-client` | Changes the active client and briefs you on its state |
| `/growth-review` | Full cross-officer review with prioritized actions |
| `/evaluate-opportunity` | Go, test-first, or no-go on a new market, product, or partnership |
| `/fill-gaps` | For a client with no data: researches the missing inputs and fills the profile with clearly labeled research-based figures |
| `/win-clients` | Go-to-market plan: best customer group, starter offer and price, named prospects, scripts, and a dated 90-day plan |
| `/monthly-review` | Checks past decisions against results and resets priorities |
| `/handover-report` | End-of-engagement summary |
| `/client-pack` | One client-ready PDF with the plan, actions, decisions, and appendices |

You can also ask in plain language. Each skill's description tells the agent when to use it.

## Working with several clients

All client information lives under `clients/`, one folder per client. `clients/ACTIVE` names the current one.

```
clients/
├── ACTIVE                  (contains: acme-logistics)
├── acme-logistics/
│   ├── profile.md          the client's business profile
│   ├── data/               their spreadsheets and exports
│   └── outputs/
│       ├── decision-log.md
│       └── reports/
└── another-client/
```

- Run `/switch-client` to change client. The agent reads only the active client's folder.
- **Start a new conversation when you switch clients**, so nothing from the previous client lingers in the chat.
- Nothing inside `clients/` is committed to Git (see `.gitignore`). Do not remove that rule. Client data is confidential.

## Handing the work to your client (one PDF)

When the work is done, run `/client-pack`. Instead of loose files, you get **one PDF** the client can read and act on: a cover and contents, an executive summary, findings, a dated action plan with owners, the decisions you need from them, the numbers and how reliable they are, risks and legal checks, and appendices (assumptions, prospects, experiments, decision record, sources).

1. Type `/client-pack`. The agent asks three quick questions (who it is addressed to, who it is from, and anything to leave out), then writes the client-facing document in plain language with no internal wording.
2. It builds the PDF and saves it in `clients/<slug>/outputs/client-pack/`.
3. Read it before you send it. Every recommendation is still the client's decision.

**If the agent stops before the PDF exists**, you can finish it yourself in CMD, without the agent:

- `py scripts\build_client_pack.py --status` lists which sections are missing or unfinished.
- `py scripts\build_client_pack.py` builds the PDF for the active client (or double-click `make-client-pack.bat`). It refuses to build until every section is complete, and tells you exactly what is missing.

One-time setup: `pip install markdown`. The PDF is made with Microsoft Edge or Google Chrome, which most computers already have. If neither is found, the script saves a web page and tells you how to print it to PDF.

## How the team works

- **Context first.** No advice until a client profile exists. See `shared/context-protocol.md`.
- **Evidence labels.** Every important claim is VERIFIED (with source), ESTIMATE (with method), or ASSUMPTION. No invented data. See `shared/evidence-standards.md`.
- **Handoff chain.** CSO, Strategist, CGO, then BDM / Head of Growth / Revenue, then COO, with CFO and Compliance review. See `shared/collaboration.md`.
- **Required reviews.** Customer commitments need a COO capacity check, money needs a CFO check, and outreach, data, and claims need a Compliance check.
- **Hard authority limits.** Officers recommend. They never commit pricing, contracts, spend, hiring, or send outreach without the owner's approval.
- **Conflicts go to the owner** with evidence and trade-offs, never resolved silently.
- **Decision log.** Every recommendation is logged with a review date and later compared with results.

## Repository layout

```
.agent/
  rules/leadership-system.md     always-on rule: routing, authority, evidence
  skills/<officer>/SKILL.md      one folder per officer
  skills/<officer>/references/   playbook: formulas, templates, frameworks
  workflows/                     the slash commands
shared/                          protocols every officer follows
templates/client/                blank client profile, data folder, decision log
clients/                         YOUR client data (not committed)
templates/client-pack/sections/  the client document, as one small file per section
scripts/build_client_pack.py     turns the client pack into one PDF
scripts/validate.py              structure checks
AGENTS.md                        entry point for other agent tools
```

## Customizing

- **Change an officer's behavior:** edit its `SKILL.md`. Keep the `description` written as "use when...", because that is what makes the agent pick the skill.
- **Add an officer:** copy a skill folder, change `name` to match the folder, write the description and accountability, add a row to `shared/collaboration.md` and the routing table in the rule file, then run `python3 scripts/validate.py`.
- **Add a workflow:** create a markdown file in `.agent/workflows/` with a `description` and numbered steps.
- Keep `.agent/rules/leadership-system.md` under 12,000 characters (the Antigravity limit per rule file).

Ideas for later officers: Marketing and Brand, Customer Success, Data and Analytics, Partnerships.

## Using with other tools

- **Claude Code:** copy `.agent/skills/*` to `.claude/skills/` and keep the repo's `AGENTS.md` and `shared/` folder. Point `CLAUDE.md` at the rule file.
- **Other agents:** most read `AGENTS.md`. Load `.agent/rules/leadership-system.md` as the system rule and let the agent open skills when a request matches.

## Validate

```
python3 scripts/validate.py
```

Checks skill names, descriptions, rule length, workflow files, and cross-file paths. The same check runs on GitHub through Actions.

## Limits

This is decision support, not professional advice. The agent can be wrong, and its quality depends on the profile and data you give it. Have a qualified lawyer, accountant, or adviser confirm anything legal, tax, or financial before acting. Always review outreach and public content before it goes out.

## License

MIT. See `LICENSE`.
