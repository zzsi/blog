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

Rung 2 has a sharper definition than "make it reliable": move the coverage-versus-error curve, then find the new optimum on it. See 2b.
| 3. Reduce frontier dependency | Structural advantage | The frontier's rate of advance | A general model catches up |

**Throughput, then process, then structural advantage.** Bound to labor, then to demand, then to time.

### What "bound by" means

The limiting factor. The thing you run out of, not merely the thing that drives the value.

- **Rung 1 is bound by labor input.** Value equals hours saved times people. It is a multiplier on existing labor, linear in headcount, and it stops when hiring stops.
- **Rung 2 is bound by demand.** Once the agent runs without a human on every run, output decouples from headcount and the cap moves to how much work actually arrives. It is also bound by what a silent error costs, which sets how much of the work you can let run unsupervised at all. See 2b.
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

- Cost advantage erodes; capability and moat do not erode the same way. Fixed-capability prices have fallen roughly 10x a year. **[VERIFIED for the a16z measurement in 2024; the continuation through 2026 is extrapolation]**
- The gate: a plateau plus a learnable signal. Volume decides whether the economics work, not whether the technique applies. **[JUDGMENT]**
- The evidence for the payoff and the evidence that the cost is falling are in 2e below.

---

## 2e. Post-training: the wins and the cost curve

Two questions a sceptical reader asks about rung 3. Does tuning actually beat the frontier in production, and is it getting cheaper? Both now have answers with primary sources.

### The wins, strongest first

**Bridgewater with Thinking Machines. [VERIFIED — thinkingmachines.ai, primary]**
Qwen3-235B base, fine-tuned on Tinker. Average accuracy **84.66%** across six financial-judgment tasks, against **78.2%** for the best frontier model tested, which was **Claude Opus 4.8**. The custom model "makes 29.8% fewer mistakes than the best frontier model" at a **13.8x reduction in inference cost per task**. The post's explanation of why the frontier lost is the thesis of rung 3 in one sentence: "An explicit prompt can only convey the intuition an expert is able to put into words, while the judgments that matter most are often the hardest to articulate."

*Correction recorded:* every secondary source we found said it beat GPT-5.5. The primary says Claude Opus 4.8. Do not repeat the secondary version.

**Harvey Tenet, in Harvey's own words. [VERIFIED — harvey.ai, Aug 20 2026]**
This is the newer and independently published Harvey result, distinct from the older one on OpenAI's page below. Kimi K3 base, post-trained with Fireworks using group-sequence policy optimisation and asynchronous RL "in realistic legal work settings," with no customer data. Against the strongest baselines named, which include GPT-5.6 Sol and Fable 5, the review-table result is **answer quality up 3.6 points and citation quality up 12.1 points at roughly one-tenth the cost per cell.** Evaluated across LAB, APEX, Redline Bench, PRBench, LegalBench, CUAD and MAUD. Harvey's own caveat: "early research results," technical report forthcoming.

Note what changed between Harvey's two results. The 2025 one tuned an OpenAI model through a vendor's managed RFT. The 2026 one post-trains an **open base** with their own RL partner and beats the vendor's frontier model on their task at a tenth of the cost. That is the rung 3 path in one company's timeline.

**Our own extraction result. [FIRST-HAND]** Tuned 3B and 8B checkpoints at 0.92 against the production model's 0.82 on transcription fields, 0.87 against 0.55 on the full field set including checkboxes. Keep generic, no client detail.

**Eight customer results on OpenAI's reinforcement fine-tuning page. [VERIFIED — one vendor page, customer-supplied figures, not independently audited]**

| Company | Task | Result | Baseline |
|---|---|---|---|
| Harvey (2025 result) | Legal citation extraction | F1 0.563 to 0.6765; won or tied 93% of head-to-heads, faster | GPT-4o |
| Ambience | ICD-10 medical coding | From 6 points behind trained physicians to 12 ahead; roughly a quarter fewer coding errors | Physician panel |
| Accordance | Tax analysis | 38.89% improvement | Base models, own benchmark |
| SafetyKit | Content moderation | F1 86% to 90%; set to replace dozens of GPT-4o calls per pipeline run | GPT-4o |
| ChipStack | Binding design interfaces to verification IP | About 12 points on both o1-mini and o3-mini | Same models, untuned |
| Runloop | Stripe API snippets that compile and pass AST checks | 12% average improvement | o3-mini |
| Milo | Schedule management: classification, recurrence, conflicts | 0.86 to 0.91 average; 0.46 to 0.71 on hard cases | GPT-4o prompting and SFT |
| Thomson Reuters | Legal review, comparison, summary | "Consistently better", preliminary, no figures | o3-mini and o1 |

These are one source, not eight. Say so in the post.

**A paper-sourced small-model result. [VERIFIED capability, cost unverified]** A 4B model post-trained with SFT then RL with verifiable rewards reached 93.3% on a held-out Linux privilege-escalation benchmark, "behind only Claude Opus 4.7 at this budget" (arXiv 2603.17673). A circulating figure of about $85 for 104 A100-hours could not be confirmed from the abstract. Use the capability claim, not the dollar figure.

### The pattern in the wins

Every strong result is on **tacit or proprietary judgment**: an investment professional's filter, a physician's coding, a firm's citation standard, a nested schema nobody published. None is on general capability. That is the same finding four times over, and it is what "capability the frontier lacks" means concretely. It also says where rung 3 does *not* pay: anywhere the right answer is public.

### Is the cost coming down? Yes, with two anchors

**Managed fine-tuning, per training token. [VERIFIED at both ends]**

| Date | Offer | Training price |
|---|---|---|
| Oct 2023 | OpenAI GPT-3.5 Turbo fine-tuning | $8.00 per million tokens |
| 2026 | Together AI, LoRA, models up to 16B | $0.48 per million tokens |
| 2026 | Together AI, full SFT, models up to 16B | $1.20 per million tokens |

Roughly **17x cheaper for LoRA and 7x for full fine-tuning in three years**. Not like-for-like, since 2023 was a closed 175B-class model behind an API and 2026 is an open model you can run, so state it as "the price of getting a model tuned to your task," which is the number a buyer cares about. Sources: OpenAI's own developer forum quoting the 2023 price contemporaneously; together.ai/pricing for 2026.

**Reinforcement learning, by hardware required. [VERIFIED]**
GRPO on Llama 3.1 8B at 20K context needed 510.8 GB of VRAM on the standard stack. Unsloth's implementation needs 54.3 GB. That moves the run from about seven datacentre GPUs to one, February 2025.

**Reinforcement learning, by orchestration. [VERIFIED — union.ai]**
Qwen3-8B GRPO on eight L40S GPUs: a 140-second training step run entirely inside the 294-second rollout window it was waiting on anyway, by launching the next rollouts before awaiting the trainer. Trainer marginal cost approaches zero. Sequential execution cost 434 seconds per iteration instead. The lesson is that RL cost is now dominated by rollouts, and rollouts overlap.

**Managed reinforcement fine-tuning, in dollars. [VERIFIED — Microsoft Foundry docs]**
Worked examples at $200, $400 and $427 per job, with billing capped at $5,000. The cap is a ceiling, not a typical spend.

**On-policy distillation. [VERIFIED — Qwen3 technical report §4.7]**
Beat reinforcement learning outright at roughly one tenth of the GPU hours on the Qwen3-8B AIME comparison. One team's measurement, not a settled constant; a 2026 follow-up questions its scaling to long horizons.

**Run cost, not train cost. [VERIFIED — Bridgewater]** 13.8x lower inference cost per task for the tuned model. That is the part that compounds with volume.

### What to say in the post

1. The received view against fine-tuning is real and sourced (see the rung 3 outline note). State it first.
2. Then: tuning wins where the answer is not public, and it wins by margins that survive audit, with Bridgewater as the headline and our own result as the first-hand one.
3. The cost of trying fell by an order of magnitude at the managed layer and by a hardware class at the RL layer, so the gate is now learnable signal and plateau, not budget.
4. The evidence base is still narrow: one vendor page, one platform vendor's flagship customer, one paper, and us. Say that too. It is more credible than pretending the field is full of independent replications.

---

## 2b. Why adopting agents often shows no return

Observed in client work, then modelled. This is the strongest argument we have and it is not in the prior draft.

### Three outcomes, not two

Most cost models for agents have two outcomes: the agent succeeds, or it fails and a human picks it up. That model is too kind, and it cannot explain a negative return. Real deployments have three.

1. **Correct and confident.** Ships. You pay only the agent.
2. **Escalated.** The agent flags low confidence, or the document is out of scope. A human intervenes. Visible, budgeted, and the thing everyone measures.
3. **Confidently wrong.** Ships with no flag. The error surfaces later, somewhere that nobody attributes to the agent.

The third outcome is invisible in the metric most teams track and it dominates the economics.

    cost per task = agent + (escalation rate x intervention) + (coverage x error rate x cost of a silent error)

**Coverage** is the share handled without a human. **Error rate** is the share of covered work that is wrong. This is the automation coverage and automation precision pair from the document AI post, and the coverage-versus-error figure in that post is the curve used below.

### Worked example: legal form extraction

100,000 documents a year. A human extracts from scratch for $15. An agent attempt costs $0.30. An escalated review costs $12. Error rates by coverage are read off the published coverage-versus-error curve.

Only one thing changes across these three cases: what a confidently wrong extraction costs downstream. The agent is identical.

| Cost of one silent error | Cheapest coverage | Result |
|---|---|---|
| $30, caught in QA | 90% | saves $1.08M a year |
| $300, reaches a filing | 50% | saves $645K a year |
| $3,000, causes exposure | 30% | **loses $90K a year** |

Same agent, same accuracy. A million-dollar saving becomes a loss, and the right operating point moves from 90% coverage to 30%, purely because of a number that sits outside the AI system entirely.

### The metric everyone tracks is dangerous on its own

"Amount of human intervention" is the natural business metric and it is the visible one. Optimising it means driving coverage up, which drives outcome 3 up with it. Push coverage to 100%:

| Silent error costs | Result at full coverage |
|---|---|
| $30 | saves 70% |
| $300 | **costs 182% more than the human** |
| $3,000 | **costs 2,702% more than the human** |

The metric points the same way in all three cases. The economics point in opposite directions. A team can hit its intervention target and destroy value doing it, and the damage lands downstream where nobody connects it to the agent.

### Reliability is still the highest-leverage lever

Two moves get confused, and separating them resolves the apparent contradiction above.

**Move along the curve.** Pick a confidence threshold. Free, instant, reversible, and it has an optimum you can overshoot. This is where the danger above lives.

**Move the curve.** Make the agent better, so the error rate falls at every coverage level. Costs engineering. Raises the ceiling instead of trading against it.

Each agent operated at its own best threshold:

| Silent error costs | Today | 2x better | 4x better | 10x better |
|---|---|---|---|---|
| $30 | $1.08M | $1.26M | $1.37M | $1.43M |
| $300 | $645K | $766K | $900K | $1.08M |
| $3,000 | $240K | $330K | $454K | $645K |

**Read the rows.** Where errors are cheap, the first doubling adds $180K and later ones add less, because you start near the ceiling. Where errors are expensive, each doubling adds *more* than the last, $90K then $124K then $191K, and ten times better still has room.

**The mechanism is coverage unlocked.** At $3,000 a silent error, today's agent can be trusted with 10% of documents. Ten times better earns 50%. The gain is not fewer mistakes on work already automated. It is work that could not be automated at all.

So the value of reliability **rises** with the stakes, which is the opposite of the intuition that high-stakes work is where agents cannot help.

### What this means for rung 2

Rung 2 is not "make the agent reliable enough to remove the human." It is two things together:

1. **Move the curve**, which is the engineering: evals, context, tools, model selection.
2. **Find the new optimum on it**, which needs one number almost nobody measures: what a silent error costs.

Without the first you stay stuck at low coverage. Without the second you blow past the optimum chasing an intervention target. This is the calibrated-reliability argument from the document AI post, with the economics attached.

### Gap 2: the saving is real and nobody banks it

Even a correctly-tuned agent produces nothing unless the saving reaches the P&L, and it reaches it two ways only. You pay for less labour, or you serve more demand.

**Rung 1 value is dispersed.** An hour a day back for a hundred people is 23,000 hours a year, close to $2M at a loaded rate. But it arrives one hour at a time across a hundred people, and you cannot bank an eighth of a person a hundred times over.

| What changes | Banked |
|---|---|
| Nobody's role changes | $0 |
| Some capacity redeployed to revenue work | ~$293K |
| Team restructured around the new capacity | ~$782K |

Against roughly $48K a year of licences and tokens for a hundred seats. If no role changes, the P&L shows $48K added and nothing removed. **The value is real and unbankable at the same time.** That is the honest limit of rung 1.

**Rung 2 value is concentrated.** One workflow at 50,000 tasks a month saving $2.85 a task is a similar theoretical figure, but it lands on a single queue.

| What changes | Banked |
|---|---|
| Queue shrinks, staffing unchanged | ~$171K |
| Team of 12 reviewers becomes 7 | ~$1.03M |
| Human removed from the loop | ~$1.54M |

The difference is not the arithmetic. A concentrated saving is visible and someone can act on it.

### Why this matters to the post

1. It gives rung 1 an honest limit, which the frame currently lacks.
2. It supplies a **mechanism** for the pilot-to-production dip, replacing an asserted curve shape.
3. It explains why workflow redesign is the strongest correlate of profit impact: redesign is what converts dispersed hours into a removed cost. The HMT hook stops being a citation and becomes an argument.
4. It makes a stalled client diagnosable. Reviewing everything means the measurement layer is missing. An intervention target with unexplained downstream rework means outcome 3 is unpriced. Dispersed unbanked hours mean the workflow was never redesigned. None of the three is fixed by a better model.

### Status and cautions

- **[FIRST-HAND observation, MODELLED illustration.]** The pattern is observed. Every number is assumed. The error-rate curve comes from our own published figure, which is itself labelled illustrative.
- Run it on a client's own three numbers: what a human handling costs, what an escalated review costs, and **what a silent error costs**. The third is the one nobody has and the one that decides the answer.
- **Do not** dress assumed inputs as measured. See the excluded claims.
- **Superseded:** an earlier version of this note used a two-outcome model and claimed breakeven reliability of 8.4% and that a point of reliability is worth the human-to-agent cost multiple. Both were artefacts of ignoring outcome 3. The real multiplier is the ratio between a silent error and a handling, which at $3,000 against $15 is two hundred to one, not twelve.

---

## 2c. Where the pattern generalises

The document extraction case is not a document problem. It is the shape of a whole class of work.

### The signature

All four have to be present:

1. **High volume of per-item decisions.** One judgement per document, claim, ticket, or transaction.
2. **A confidence signal exists**, so escalation can be selective rather than all-or-nothing.
3. **A human fallback exists** and is cheaper than living with the error.
4. **Asymmetric error cost.** A silent error costs far more than an escalation.

Where all four hold, the three-outcome model applies and the operating point is a business decision, not a modelling one.

### Domains that fit

| Domain | Coverage decision | What the silent error costs |
|---|---|---|
| Document and form extraction | Which fields auto-post | Downstream rework, filing error, exposure |
| Insurance claims, straight-through processing | Which claims skip an adjuster | Wrong payout, leakage, regulatory finding |
| Medical coding | Which codes submit unreviewed | Denied claim, audit, clawback |
| Content moderation | What publishes without review | Harm, brand damage, regulatory penalty |
| Underwriting and credit decisioning | Which applications auto-decide | Bad book, discrimination exposure |
| Invoice and accounts payable | Which invoices auto-approve | Duplicate or fraudulent payment |
| Customer support deflection | Which tickets resolve unaided | Churn, escalation, reputational cost |

Reported straight-through processing rates in insurance moved from 10-15% in 2022 to 70-90% on standard lines, with 30-50% of standard claims running without human intervention. **[UNVERIFIED — vendor and SEO content only; useful for choosing examples, not for quoting]**

### The inverted case is worth studying

In fraud detection the asymmetry is mirrored. The **visible** cost is the false positive, a legitimate claim you flagged and investigated. The **silent** cost is the fraud you missed. Reported figures: 60-85% false positive rates for rules-based systems, under 10% for ML scoring, and investigation teams confirming only 15-40% of referrals. **[UNVERIFIED — same caveat]**

The lesson is general. **Whichever side of the error is invisible is the side that eats the return.** In extraction it is the confident mistake. In fraud it is the miss. Teams instrument the visible side because it is the side that generates tickets.

### A problem for the whole framework

The model needs a usable confidence signal, and getting one is the hard part. See 2d.

The short version: a single self-reported score is not enough, which is what the document AI post already argues. Confidence should come from **agreement** across OCR, a vision-language model, an LLM and validators, because those fail in less correlated ways than one model asked twice. Production content moderation does the same thing, escalating on four independent triggers rather than one: calibrated confidence, novelty, policy match, and contradiction.

### Regulation puts a floor under the escalation rate

In some domains the operating point is not purely an economic choice.

EU AI Act Article 14 requires that high-risk systems be designed so a person can "disregard, override or reverse the output" and can stop the system. For biometric identification under Annex III point 1(a), no action may be taken unless the identification "has been separately verified and confirmed by at least two natural persons." **[VERIFIED — artificialintelligenceact.eu/article/14]**

**Correct the date.** Widely repeated secondary sources still give August 2, 2026 for high-risk obligations. They were delayed: **December 2, 2027** for Annex III systems, **August 2, 2028** for Annex I. Deferred because standards and national authorities were not ready, not abandoned. **[VERIFIED]**

Annex III covers creditworthiness assessment, life and health insurance underwriting, employment and worker management, education, and access to essential services. **Those are the same domains where a silent error is most expensive.** The economics and the regulation point the same way, which is a useful thing to be able to tell a client.

---

## 2d. Where the confidence score comes from

Everything in 2b and 2c rests on being able to separate outcome 1 from outcome 3. That separation is a confidence signal, and it is the weakest link in the chain.

### How it is estimated, cheapest first

| Method | What it costs | What it is good for | Catch |
|---|---|---|---|
| Ask the model | Nothing | Any API, no internals needed | Clusters on round numbers |
| Log-probabilities | Nothing, where exposed | Theoretically grounded | Measures fluency, not correctness; no single number for a multi-step agent |
| Sample N times, measure agreement | Nx inference | Strong signal; for agents, whether it takes the same *path* twice | Correlated errors survive the vote |
| A second model judges the first | One extra call | Flexible | Moves the calibration problem rather than solving it |
| **Agreement across heterogeneous components** | Already paid for | OCR vs VLM vs LLM fail in less correlated ways | Needs more than one component |
| **Deterministic validators** | Near nothing | Checksums, schema, cross-field consistency | Only where the task admits one |

The last two are the ones to build on. The first four all ask one model how it feels.

**[CORRECTION to an earlier version of this note.]** It said RLHF-trained models are systematically miscalibrated and their highest stated confidence often correlates with wrong answers. That was the standard finding and it has partly reversed. Work in 2026 argues the advice to prefer log-probabilities no longer holds on post-2025 models, where verbalized confidence is the better signal, tested across three benchmarks and up to 18 models. **[VERIFIED — arXiv 2609.10996]** Read it precisely: the paper claims *relative* superiority over logprobs and explicitly does not claim verbalized confidence is now well calibrated. Ranking improved. Calibration did not.

### Yes, calibration needs ground truth

"A score of 0.8 means 80% correct" is an empirical claim about your data. Nothing about the model establishes it. But three things make this cheaper than it sounds.

**You need less data than you expect.** Reported practice puts Platt scaling on a couple of hundred labelled examples at cutting expected calibration error by 30 to 60%. That is a week of one person's work, not a data programme. **[UNVERIFIED — secondary source; check before quoting the range]**

**You may not need a calibrated probability at all.** For setting a threshold, what you need is the empirical curve: at each threshold, what coverage you get and what error rate comes with it. That is directly measurable from labelled examples, and it is exactly the coverage-versus-error curve in the document AI post. A score that ranks well but calibrates badly still yields a usable curve.

**The labels have a source you are already paying for.** Every escalated item goes to a human who produces a verdict, and that verdict is a label. **The escalation queue is a labelling pipeline.** Start conservative with high escalation, harvest labels from the reviews, recalibrate, lower the threshold as the curve firms up. The expensive early phase funds the cheap later one.

That last point is worth making loudly in the post. It reframes the cost of early over-escalation from waste into investment, and it is the same move as "your eval failures are your best training set", one layer down.

### The principled version

Conformal risk control states a target error rate **among accepted outputs** and returns the threshold that guarantees it, from a calibration set. That is the formal version of the hand-modelling in 2b, and it fits this problem because the guarantee lands exactly where silent errors live. Worth naming in the post as the rigorous option, without a tutorial.

### Calibration decays

The document mix shifts, the model version changes, someone edits the prompt. Calibration is a standing measurement, not a setup step. Another reason the escalation queue matters: it is the only label source that keeps producing.

### What this adds to the argument

Setting the operating point needs **two** numbers, and most teams have neither:

1. What a silent error costs. A business number, knowable in an afternoon, nobody measures it.
2. The coverage-versus-error curve for your own data. An engineering number, needs a few hundred labels, and the escalation queue produces them for free.

Rung 2 is the work of getting both.

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
3. **EU AI Act high-risk obligations apply from August 2, 2026.** Still asserted across secondary sources. Wrong. Delayed to December 2, 2027 (Annex III) and August 2, 2028 (Annex I). **Do not use the 2026 date.**
4. **Stacked cost reductions of 60 to 80%.** Vendor blogs with no study; competing vendors publish incompatible ranges. Already cut from the prior draft.

Two Gartner items are attributable by date but have no retrievable link: agentic models using 5 to 30 times more tokens per task than a standard chatbot (March 2026), and agentic routing raising provider inference costs at least fivefold (August 2026). **Use only if a primary link is found.**

---

## 5. Open

- Find a primary source for the workflow-redesign line, or write it in our own words.
- Decide whether the reliability-beats-price worked example earns its place, given every input has to be assumed.
- Rung 1 needs a first-hand story. The enablement program is the obvious source and none of it is written up yet.
