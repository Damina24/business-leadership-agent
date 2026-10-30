---
description: Evaluate a major opportunity such as a new market, product, partnership, or business model, and produce a go, no-go, or test recommendation.
---

# /evaluate-opportunity

Ask the owner to describe the opportunity in a sentence if they have not. Follow `shared/context-protocol.md`. Use the `chief-of-staff` skill to coordinate.

1. **Strategic fit** (`chief-strategy-officer`): run the strategic fit test and note strategic risks.
2. **Evidence** (`growth-strategist`): demand, competition, entry cost, and execution needs, with cited sources. Compare against "improve the core" and "do nothing".
3. **Economics** (`chief-financial-officer`): business case with base, downside, and upside cash views and the cash low point.
4. **Delivery** (`chief-operating-officer`): capacity check and what must change to deliver.
5. **Compliance** (`risk-compliance-officer`): regulatory, licensing, privacy, contract, and reputational check.
6. **Priority** (`chief-growth-officer`): how it ranks against other growth options. Recommend **Go**, **Test first** (with a smallest viable test and kill criteria), or **No-go**.
7. **Brief** (`chief-of-staff`): quality gate, then a decision brief or conflict memo for the owner.
8. Save the report to `clients/<slug>/outputs/reports/` and log the decision.

When the owner wants to hand the results to the client, offer `/client-pack` to turn everything into one client-ready PDF.
