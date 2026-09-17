# The business value story

Working note for the three-rung post. Written 2026-09-16.
Every outside claim below carries a verification status. Nothing here goes into the post at status UNVERIFIED without being checked first.

---

## 1. The arc

The three rungs do not buy more of the same thing. Each buys a categorically different kind of value, and the kind is what makes the frame worth having.

| Rung | Buys | Bound by | Runs out when |
|---|---|---|---|
| 1. Set up to use agents well | Throughput | Labor input | You stop hiring |
| 2. Harness engineering | A dependable process | Demand reaching the business | The work stops arriving |
| 3. Reduce frontier dependency | Structural advantage | The frontier's rate of advance | A general model catches up |

**Throughput, then process, then structural advantage.** Bound to labor, then to demand, then to time.

### What "bound by" means

The limiting factor. The thing you run out of, not merely the thing that drives the value.

- **Rung 1 is bound by labor input.** Value equals hours saved times people. It is a multiplier on existing labor, linear in headcount, and it stops when hiring stops.
- **Rung 2 is bound by demand.** Once the agent runs without a human on every run, output decouples from headcount and the cap moves to how much work actually arrives.
- **Rung 3 is not unbounded.** Two corrections to the tempting version of this claim. Its cost-structure component still needs volume to amortize, so it inherits rung 2's demand bound rather than escaping it. Only the moat and capability component behaves differently, and even that is bound, by how fast the frontier erodes the advantage.

### Why unbounded would not be desirable anyway

A constraint doubles as a validation check. Rung 1 and rung 2 tell you when to stop, because you can see yourself running out of people or running out of work. Rung 3 gives no such signal, which is exactly why it needs a deliberate gate on entry and a scheduled re-check. "Assume the base model is deprecated within twelve months, re-benchmark quarterly" is the practical form of that missing signal.

---

## 2. Per-rung detail

### Rung 1: throughput, bound by labor

The evidence is real, highly variable, and occasionally negative. Say so rather than quoting the best number.

- Controlled study: 55.8% speedup, 95 freelance developers, single scoped task, confidence interval 21% to 89%. **[VERIFIED — arXiv 2302.06590]**
- Larger field experiments: pooled 26% increase in completed tasks across 4,867 developers. **[VERIFIED — MIT working paper]**
- Counter-evidence: experienced open-source maintainers were 19% *slower*. **[VERIFIED — arXiv 2507.09089]**

The catch: high adoption does not become enterprise impact on its own. This is where workflow redesign, governance, and adoption enter, and it is the HMT hook.

- Workflow redesign is McKinsey's strongest correlate of EBIT impact, stronger than any technology factor tested. **[VERIFIED — McKinsey State of AI, Nov 2025]**

### Rung 2: a dependable process, bound by demand

- 70% success is a demo. 95% at a known cost per run is a process. **[framing, not a claim]**
- Klarna: 2.3 million conversations, resolution time 11 minutes to 2, company-reported profit improvement around $40M. **[VERIFIED — company disclosures; note it is company-reported]**
- Most teams find most of the margin available to them here, before owning anything. **[JUDGMENT — the specific 60-80% stacked-savings band is vendor marketing with no study behind it; do not quote a percentage]**

**The reliability-beats-price argument.** A large unit-cost advantage is worth little if the agent only handles part of the volume, because failures still reach a human. Worth making with an explicit worked example using assumed inputs, clearly labeled as illustrative. Do not present the inputs as measured. See the excluded claims below for why.

### Rung 3: structural advantage, bound by the frontier

- Cost advantage erodes; capability and moat do not erode the same way. Fixed-capability prices have fallen roughly 10x a year. **[VERIFIED for the a16z measurement in 2024; the continuation through 2026 is extrapolation, not a fresh measurement]**
- Our own extraction result: tuned 3B and 8B checkpoints at 0.92 against the production model's 0.82 on transcription fields, and 0.87 against 0.55 on the full field set including checkboxes. **[FIRST-HAND — strongest evidence in the post; keep generic, no client detail]**
- The gate: a plateau plus a learnable signal. Volume decides whether the economics work, not whether the technique applies. **[JUDGMENT]**

---

## 2b. Why adopting agents often shows no return

Observed in client work, then modelled. This is the strongest argument we have and it is not in the prior draft.

### The per-task arithmetic does not explain it

Start with the simple model. An agent attempts every task, and failures still reach a human.

    effective cost = agent attempt + (failure rate x human cost)

Breakeven reliability is just the inverse of the cost multiple. If the agent costs a twelfth of a human, it breaks even above about 8% reliability. So almost any working agent avoids *some* cost, and the unit economics cannot be what produces a negative return. The model is not wrong, it is incomplete.

Two things sit between cost avoided and money returned.

### Gap 1: the cost of not knowing which runs failed

The simple model quietly assumes you can tell a success from a failure, which is what lets you route only failures to a human. Without measurement you cannot, and both fallbacks are expensive.

Illustrative, with a human at $7.40, an agent attempt at $0.62, a review costing about 30% of doing the task yourself, and an agent that is right 60% of the time:

| Posture | Effective cost | Versus the human |
|---|---|---|
| Review every output | $5.80 | saves 22% |
| Review nothing, escaped error costs the same as a normal handling | $3.58 | saves 52% |
| Review nothing, escaped error costs 3x | $9.50 | **costs 28% more** |
| Review only what a confidence policy flags: 40% flagged, catching 90% of failures | $4.47 | saves 40% |

Reviewing everything throws away most of the prize. Reviewing nothing is a gamble on the cost of an escaped error, and loses badly when that cost is above par. A confidence policy is what converts reliability into realised savings, which is why measurement is the first layer of rung 2 rather than a nicety.

This is the verifier story from the evals section, restated in money.

### Gap 2: the saving is real and nobody banks it

A saving reaches the P&L two ways only. You pay for less labour, or you serve more demand. Neither happens on its own, and this is where the rungs diverge sharply.

**Rung 1 value is dispersed.** An hour a day back for a hundred people is 23,000 hours a year, close to $2M at a loaded rate. But it arrives one hour at a time across a hundred people, and you cannot bank an eighth of a person a hundred times over.

| What changes | Banked |
|---|---|
| Nobody's role changes | $0 |
| Some capacity redeployed to revenue work | ~$293K |
| Team restructured around the new capacity | ~$782K |

Against roughly $48K a year of licences and tokens for a hundred seats. If no role changes, the P&L shows $48K of cost added and nothing removed. **The value is real and unbankable at the same time.** That is the honest limit of rung 1 and it should be stated there.

**Rung 2 value is concentrated.** One workflow at 50,000 tasks a month saving $2.85 a task is a similar theoretical figure, but it lands on a single queue.

| What changes | Banked |
|---|---|
| Queue shrinks, staffing unchanged | ~$171K |
| Team of 12 reviewers becomes 7 | ~$1.03M |
| Human removed from the loop | ~$1.54M |

The difference is not the arithmetic. It is that a concentrated saving is visible and someone can act on it.

### Why this matters to the post

1. It gives rung 1 an honest limit, which the frame currently lacks.
2. It supplies a **mechanism** for the pilot-to-production dip, replacing an asserted curve shape.
3. It explains why workflow redesign is the strongest correlate of profit impact: redesign is what converts dispersed hours into a removed cost. Our HMT hook stops being a citation and becomes an argument.
4. It says which rung a stalled client is actually on. Reviewing everything means the measurement layer is missing. Dispersed unbanked hours mean the workflow was never redesigned. Neither is fixed by a better model.

### Status and cautions

- **[FIRST-HAND observation, MODELLED illustration.]** The pattern is observed. Every number above is assumed, and the conversion rates in particular are the weakest input.
- Present as a worked example with stated assumptions, or better, run it on a client's own two figures: what a human handling costs, and what share of runs the agent gets right.
- **Do not** dress the assumed inputs as measured. The circulating per-task figures are disowned by the sources that carry them, see the excluded claims.
- The leverage result is the durable part and survives any inputs: **a point of reliability is worth the cost multiple between human and agent.** At 12x cheaper, one point of reliability is worth twelve points of unit price. Below roughly 80% reliability, rung 2 beats rung 3 regardless of how attractive rung 3 looks.

---

## 3. Outside views, for comparison

### a16z: per-seat pricing breaks — **[VERIFIED]**

https://a16z.com/newsletter/december-2024-enterprise-newsletter-ai-is-driving-a-shift-towards-outcome-based-pricing/

> "Per-seat is no longer the atomic unit of software."

Their worked example: Zendesk at $115 per month per seat. If AI resolves a sizable share of tickets, companies need fewer human support agents and therefore fewer seats, so vendors move toward charging for outcomes.

**Why it matters to us.** This is the rung 1 to rung 2 transition described from the revenue side rather than the delivery side. Seats are headcount-bound. Outcomes are demand-bound. An independent route to the same boundary is worth citing, because it shows the line is not an artifact of our framing.

### BCG: AI as a worker — **[PARTIALLY VERIFIED]**

https://www.bcg.com/publications/2026/the-200-billion-dollar-ai-opportunity-in-tech-services

BCG defines agentic systems as capable of "autonomous, multistep reasoning, decision making, and execution across workflows — not just generating outputs but driving outcomes."

**Status.** The "driving outcomes, not just generating outputs" contrast is BCG's own and maps onto our rung 1 / rung 2 line. The neat "AI as a tool, you ask and it answers / AI as a worker, you assign and it executes" phrasing is **not** BCG's wording; it came from an aggregator. Use the quoted definition, not the slogan.

### Consulting consensus on workflow — **[UNVERIFIED WORDING, VERIFIED SUBSTANCE]**

The circulating line is that the most expensive failure mode is deploying agents without workflow redesign, because an agent dropped into an existing process inherits that process's inefficiencies. Punchier than our McKinsey citation and says the same thing. **Attribute to no one until the primary source is found, or write it in our own words and cite McKinsey for the substance.**

### NVIDIA: nine techniques ordered by cost — **[VERIFIED]**

https://developer.nvidia.com/blog/mastering-agentic-techniques-ai-agent-customization/

Prompting, RAG, tool and skill injection, SFT, PEFT/LoRA, DPO, RLHF, RLVR, GRPO. Ordered by computational cost and reversibility. Guidance is to start with system prompts, tools and skills, and retrieval, then apply training later.

**Why it matters to us.** Validates the escalation rule. But it starts at prompting and has nothing to say about the work before that, which is precisely our rung 1. The contrast is the argument for why rung 1 belongs in the frame.

### The externalization literature: weights, then context, then harness — **[VERIFIED]**

https://arxiv.org/abs/2604.08224

Reads the field's history as a progression from weights to context to harness, with harness as the unification layer coordinating memory, skills, and protocols into governed execution.

**Why it matters to us.** The field's direction of travel is the inverse of a client's. The field went weights first and harness last. A client goes harness first and weights last. That inversion is the single most interesting outside fact we have, and it is worth one paragraph.

---

## 4. Claims deliberately excluded

Recorded so they do not creep back in.

1. **Agentic AI is ~17% of enterprise AI value today, rising to ~29% by 2028.** Attributed to BCG by aggregators. Not present in either BCG source checked. **Do not use.**
2. **An agent resolves a task for $0.62 versus $7.40 for a human, with median tier-1 deflection at 41.2%.** The article carrying these figures says of the underlying numbers: "Circulating numbers range from $6.00 to $13.50 and credit Gartner, Forrester and SQM variously, yet none of those firms publishes the number under its own name." The deflection rate is described as internally calculated, not a published benchmark. **Do not use as measured figures.** The structural argument survives as an illustration with assumed inputs.
3. **Stacked cost reductions of 60 to 80%.** Vendor blogs with no study; competing vendors publish incompatible ranges. Already cut from the prior draft.

Two Gartner items are attributable by date but have no retrievable link: agentic models using 5 to 30 times more tokens per task than a standard chatbot (March 2026), and agentic routing raising provider inference costs at least fivefold (August 2026). **Use only if a primary link is found.**

---

## 5. Open

- Find a primary source for the workflow-redesign line, or write it in our own words.
- Decide whether the reliability-beats-price worked example earns its place, given every input has to be assumed.
- Rung 1 needs a first-hand story. The enablement program is the obvious source and none of it is written up yet.
