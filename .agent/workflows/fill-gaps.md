---
description: For a client with little or no data (for example a brand-new company), research the missing inputs and fill the profile with clearly labeled, research-based working figures so planning can start right away.
---

# /fill-gaps

Use when the profile has empty or "unknown" sections and the owner cannot supply them yet. Use the `chief-of-staff` skill to coordinate. Follow `shared/context-protocol.md` and `shared/evidence-standards.md`. Never read the examples folder or any other client's folder, and never copy figures from a sample.

The aim is speed without pretending. Every figure carries a **Basis** the owner can see at a glance:
- **Owner-provided**: the owner told us (only for things the owner actually said).
- **Based on research**: found by research, with source and date.
- **Assumed**: a working guess, used only when research finds nothing, with what would confirm it.

1. **List the gaps.** Read `clients/<slug>/profile.md` and `clients/<slug>/data/`. Note every empty, "unknown" or missing item.
2. **Ask only for what is truly the owner's own.** In one message, ask at most three short questions: cash available, number of people and hours per month on client work, and rough monthly running costs. If the owner does not know or does not answer, do not make up scenarios. Research real benchmarks for comparable businesses in the same country and city (for example typical start-up capital for a small software company, realistic productive hours per developer per month, typical monthly costs) and use those as the working figures, with Basis "Based on research", the source and the date. Say clearly that the owner's own figure may differ and that the plan should be rerun when it is known.
3. **Research the rest** using web search, with source URL and access date for each finding. Prefer official or primary sources. Try several searches and sources before giving up on a figure. Only if nothing reliable exists, write "no reliable data found" and say how to get it; do not substitute a made-up scenario.
   - Market and best first customer group (`growth-strategist`, `chief-strategy-officer`).
   - Starter offers and price ranges in the local currency, low, middle and high (`revenue-growth-manager`).
   - Delivery hours and delivery cost per offer, as ranges (`chief-operating-officer`).
   - Typical monthly running costs for this kind of business and place (`chief-financial-officer`).
   - Outreach and conversion benchmarks, sales cycle length, and the best channels (`business-development-manager`, `head-of-growth`).
   - Licences, data protection and contract steps needed before the first sale (`risk-compliance-officer`).
4. **Write the findings** to `clients/<slug>/data/researched-baseline.md` as a table: Item | Value (range) | Basis | Label (VERIFIED, ESTIMATE or ASSUMPTION) | Source and date | Confidence. Put this line at the top: "Items marked Based on research or Assumed have not been confirmed by the owner."
5. **Update the profile** with the same values, each tagged with its Basis, for example "₦X to ₦Y (Based on research, source, date)". Never write "owner-stated" for anything the owner did not say. Leave genuine unknowns as "unknown".
6. **Show the owner a short summary** in three lists: Provided by you, Based on research, Assumed. Highlight the five figures that matter most to check. The owner may change any line; do not wait for approval before continuing.
7. **Speed plan.** If the owner wants to start soon, add a days 1 to 3 launch checklist: choose the starter offer, set its price from the research range, write a one-page proposal, book a lawyer review of the contract template, build a list of 30 real prospects, and draft the first 10 outreach messages for the owner to send. Treat early customer conversations as sales conversations that run alongside selling, not as a delay.
8. Log each proposed assumption in `clients/<slug>/outputs/decision-log.md` and offer `/win-clients` as the next step.

Research gives a starting point, not proof. Say so, and say which figures to replace first as real results arrive.
