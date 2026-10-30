# Worked Example: A New Digital Solutions Company in Abuja

This walkthrough shows the agent start to finish for a **fictional** company, Demo Digital Solutions Ltd. All company figures are invented owner estimates (marked ASSUMPTION). Market facts come from cited sources.

> Note: these files were produced by following the skills' instructions, as a demonstration. When you run the agent in Antigravity, the wording and detail will differ, but the structure and the rules should match.

All output files are in the `client/` folder next to this file.

---

## Step 1: Onboard the client with `/new-client`

**You type:** `/new-client`

**The agent asks** two to four questions at a time and writes each answer into `profile.md` straight away. A condensed version of the interview:

| Round | Agent asks | Owner answers (summary) |
|---|---|---|
| 1 | Organization name, what it does, how old, team size? | Demo Digital Solutions Ltd; websites, business apps, automations; 2 months old; 3 people |
| 2 | What do you sell, at what price, and what does each cost you to deliver? | Starter Website ₦350,000; Business Web App ₦1,800,000; Care Plan ₦50,000 per month; variable costs and hours per job |
| 3 | Who are your customers today, and how much cash do you have? | No customers; 2 warm contacts; ₦6,000,000 cash; ₦1,100,000 fixed costs per month |
| 4 | Who approves pricing, discounts, spending, outreach, and contracts? | The founder approves everything; no pre-approved limits except the growth budget |

**What to notice**
- The agent labels every number ASSUMPTION because the owner has no documents yet.
- It asks for a bank statement, supplier quotes, and time logs, and records them as data gaps.
- It marks the profile `status: complete` only after the key sections and the approval table are filled.

Result: `client/profile.md`

---

## Step 2: Ask for a plan with `/win-clients`

**You type:** `/win-clients`

The Chief of Staff runs the officers in order. The agent first reads the profile, the data folder, and the (empty) decision log, as `shared/context-protocol.md` requires.

| Step | Officer | What they produced |
|---|---|---|
| 1 | Business Development Manager | An ideal customer profile (clearly marked as a hypothesis, since there are no customers yet) |
| 2 | Business Development Manager | A pipeline with 2 real warm contacts and **0 invented prospects**, plus a plan to source 30 real ones with URLs and dates |
| 3 | Head of Growth | Three experiments with success and stop thresholds, fitted into the ₦150,000 budget |
| 4 | Revenue Growth Manager | An offer ladder, discount maths, 50/50 payment terms, and a proposal for a 10% founding-client discount |
| 5 | Chief Operating Officer | Capacity check: **Go with conditions** |
| 6 | Chief Financial Officer | Base and downside cash cases: **Clear with conditions** |
| 7 | Risk and Compliance Officer | **Clear with conditions** for outreach; **Needs professional review** for the data-protection registration and contracts |
| 8 | Chief Growth Officer | Scored and ranked five initiatives |
| 9 | Chief of Staff | Quality gate, then a one-page decision brief |

Results: `client/outputs/reports/2026-10-25-win-clients-plan.md`, `client/outputs/prospect-pipeline.md`, `client/outputs/experiment-backlog.md`

---

## Step 3: What the agent found that the owner might have missed

1. **Care Plans are the best use of hours.** Contribution per delivery hour: Care Plan ₦10,500, Starter Website ₦5,083, Business Web App ₦4,000. The big custom app looks attractive but earns the least per hour.
2. **Runway, not demand, is the problem.** With no revenue the company has about 4.8 months of cash. In the base case it reaches monthly cash break-even in month 9, with cash never below about ₦2.7 million. At about half the sales pace, cash runs out in month 8.
3. **A single app would break capacity.** One Business Web App needs about 200 hours a month for two months, which together with one new website exceeds the 256 plannable hours.
4. **A discount can cost more than it wins.** A 20% discount needs about 30% more volume to break even, and the team has no spare capacity to deliver extra volume.
5. **Data protection applies from day one.** The company will hold other people's personal data, so the registration tier and a lawyer-reviewed contract come before the first signature.

---

## Step 4: A disagreement goes to the owner

The Business Development Manager wants a 20% founding-client discount. The Revenue Growth Manager wants 10%. The Chief of Staff does not pick a winner. The brief shows both positions with costs, trade-offs, what evidence would settle it, and a suggested compromise. The founder decides. See `client/outputs/reports/2026-10-25-decision-brief.md`.

---

## Step 5: The owner decides, and everything is logged

The brief ends with five numbered decisions, each with a recommended option and an alternative. Eight actionable items are logged in `client/outputs/decision-log.md`, each with a review date. No pricing, discount, spending, or outreach is committed, because every item says **Proposed** until the founder approves it.

---

## Step 6: Hand it to the client with `/client-pack`

**You type:** `/client-pack`

The agent asks three quick questions (who it is addressed to, who it is from, anything to leave out). It then writes one plain-language document for the client's decision-maker and builds a single PDF. The document leads with what to do (a dated 90-day plan and the decisions needed), then the numbers and how reliable they are, the risks and legal checks, and appendices. It never mentions the AI team, skills, or file names.

Result: `client/outputs/client-pack/demo-digital-solutions-ltd-client-pack-2026-10-28.pdf` (13 pages). The source document is `client-pack.md` in the same folder.

---

## Step 7: Later in the engagement

| When | You type | What happens |
|---|---|---|
| 2026-11-25 | `/monthly-review` | The agent compares each decision with actual results, updates the scorecard, and resets priorities |
| 2027-01-23 | `/monthly-review` | The month-3 checkpoint: fewer than 4 websites signed triggers the cost-cut or bridge plan |
| When a bigger opportunity appears | `/evaluate-opportunity` | Strategy, finance, capacity, and compliance checks, then go, test first, or no-go |
| End of the contract | `/handover-report` | A summary of decisions, results, and lessons |

---

## Try it yourself

On Windows, from the project folder:

```
xcopy examples\abuja-digital-demo\client clients\demo-digital-abuja /E /I
echo demo-digital-abuja> clients\ACTIVE
```

Then open the folder in Antigravity, start a new conversation, and type `/switch-client` or ask a question such as "How should we price our first three website projects?". Delete `clients\demo-digital-abuja` and the `ACTIVE` file when you are done. (The `clients/` folder is excluded from Git, so the copy will not be published.)
