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
| 2026 | Together AI, LoRA, models up to 16B | $0.48 per million tokens, cut to $0.34 for Qwen3.5-9B on Sep 11 2026 (see posttraining.md) |
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

## 2g. The return on rung 2 (research round 2026-09-28)

**Verdict:** the return on building your own agent is work that runs **unattended**, **inside your own systems**, on **the model you choose**. With the model held fixed, the harness moves benchmark scores by about 5 to 25 points and can cut cost per task by half or more. The company figures are all self-reported. **No public study compares an in-house agent with a vendor agent on the same work.**

**Why companies built their own**
- **Stripe Minions**, Feb 19 2026 **[PRIMARY, checked]**:
  - "Over 1,300 Stripe pull requests (up from 1,000 as of Part 1) merged each week are completely minion-produced, human-reviewed, but containing no human-written code."
  - Why build: "Off-the-shelf local coding agents are usually optimized for working through code changes as a companion to engineers, typically with one 'looking over its shoulder'… Minions, however, are fully unattended, so our agent harness can't use human-facing features such as interruptibility."
  - Toolshed has "nearly 500 MCP tools."
  - Stripe forked Goose in late 2024 and developed it toward its own needs, which means it diverges from upstream rather than keeping in sync.
  - https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2
- **Ramp Inspect**, Jan 12 2026: "~30% of all pull requests merged to our frontend and backend repos are written by Inspect." It is built on OpenCode, "supports all frontier models," and is "wired into Sentry, Datadog, LaunchDarkly, Braintrust, GitHub, Slack, and Buildkite." https://builders.ramp.com/post/why-we-built-our-background-agent **[PRIMARY]**
- **Harvey**, Jun 1 2026 **[PRIMARY, checked]**:
  - Built its own runtime because "a firm that wants to serve a broad client base will need to be able to run on essentially any model," and because of zero data retention.
  - Reports "3-5x cost reductions versus a frontier-only approach, depending on model and workload." No method is given.
  - https://www.harvey.ai/blog/why-we-built-our-own-cloud-agent-infrastructure
- **Shopify Dispatch** (a security harness), Jul 29 2026: "over 300 findings" across "over 80 unique applications" in about six weeks. Shopify values them at "over $400,000 in equivalent bug bounty payouts." A full scan costs $50–300. https://shopify.engineering/building-an-agentic-harness-that-outlasts-the-model **[PRIMARY]**
- **Fin (formerly Intercom)** has since moved to rung 3: its latest gain came from its own model.
- **Sierra and Decagon customers** buy a harness rather than own one, so for them this is rung 1.

**The harness alone, same model**
- **LangChain**, Feb 17 2026: "improve deepagents-cli… 13.7 points from 52.8 to 66.5 on Terminal Bench 2.0. We only tweaked the harness and kept the model fixed, gpt-5.2-codex." Caveat: tuned on the same 89 tasks it reports, and LangChain itself warns "Changes that overfit to a task are bad for generalization." **[PRIMARY, vendor, checked]**
- **Mak et al.**, arXiv 2609.11999, Table 1, Opus-4.8 on TheAgentCompany: typed tools 44.9% at $1.20 a task; bash alone 69.4% at $0.37. **[PRIMARY]**
- **Fan et al.**, arXiv 2609.20804 **[PRIMARY, checked]**:
  - Context management matters most on tight budgets: the gap is 35.7 points at the tightest budget, falling to 2.7 at the loosest.
  - Planning adds 11.6 points for Nemotron-3 30B. For the strong models it mostly cuts cost, by about 30%.
- **Xu et al.**, arXiv 2608.11386: resolve rate is "similar across tool architectures," but structured interfaces improve consistency "by up to 4.7×." **[PRIMARY]**
- **Terminal-Bench 2.0**, Wayback snapshot of Apr 26 2026, same model under different agents:
  - Verified spreads: Opus 4.6 4.9 points (Terminus 2 62.9% vs Claude Code 58.0%); GPT-5.3-Codex 10.4; GPT-5.2 8.9.
  - Larger spreads depend on unverified entries.
  - Anthropic: infrastructure alone moved Terminal-Bench 2.0 by "6 percentage points," so "leaderboard differences below 3 percentage points deserve skepticism." **[PRIMARY]**
- **OpenAI "Harness engineering"**, Feb 11 2026: about 1,500 PRs from three engineers, a million lines of code, runs of up to six hours. There is no baseline. **[PRIMARY via Wayback, vendor]**

**What it costs**
- **Team sizes** are not disclosed. OpenAI's team grew from three to seven engineers.
- **Harness gains decay:**
  - "Harnesses encode assumptions that go stale as models improve" (Anthropic, Apr 2026).
  - Vercel: "every model update meant re-calibrating our constraints."
  - Manus: "we've rebuilt our agent framework four times" (2025).
- **Upstream churn** (research agent's GitHub API count, 2026 to date): goose had 55 releases, OpenCode 230.
- **Run cost can rise.** Anthropic's full harness cost $200 over 6 hours against $9 over 20 minutes solo, on the same model, and the solo run's central feature "simply didn't work." Anthropic's rule: "worth the cost when the task sits beyond what the current model does reliably solo."

**Cheaper model plus tools (the author's view)**
- **Supported: weaker models gain more from tools.**
  - Fan et al. (checked): predefined tools raised Nemotron-3 30B from 10.2% to 25.2% on SWE-Bench. For the 550B model, bash alone was better (65.8% to 69.4%) and cut cost 53%.
  - Xu et al.: the largest consistency gain went to the weakest model.
  - Anthropic tool search: +25 points on Opus 4 and +8.6 on Opus 4.5.
- **Not shown: a cheaper model with tools matching a frontier model.**
  - In Fan et al., 30B with tools reached 25.2% against 69.4% for the 550B with bash.
  - Anthropic's advisor setup (Apr 9 2026, checked): "Haiku with an Opus advisor trails Sonnet solo by 29% in score but costs 85% less per task." Eve Legal, a customer, reports "matching frontier-model quality at 5× lower cost" on structured document extraction. That is a vendor-published customer quote.
- **Defensible:** giving a cheaper model more structure is a sound cost experiment, and the gain from tools is largest for weaker models. Whether it clears your bar is something you measure, not assume.

## 2h. The "one company in twenty" studies: dates, definitions, 2026 (research round 2026-09-28)

**Verdict:** "about one in twenty" holds only for surveys fielded in the first half of 2025. The three figures measure different things, all self-reported. No 2026 study measures the same bar again. Lower bars give far higher numbers.

- **BCG, "The Widening AI Value Gap"** (Sept 2025; n=1,250 CxOs and senior executives, 68 countries; fielding dates not stated) **[PRIMARY, checked]**
  - "Only 5% of companies in our 2025 study of more than 1,250 firms worldwide are achieving AI value at scale."
  - The 5% is the share scoring "future-built" (above 75 of 100) on a self-rated maturity score across 41 capabilities.
  - Its own caveats: "We drew insights on AI maturity and value from self-reported data… Results reflect the business area that the respondents know best—not always the full company. Unless explicitly stated as realized… reported numbers reflect expected future impact."
  - Trend: 4% in 2024, 5% in 2025.
- **McKinsey, "The state of AI in 2025"** (Nov 2025). The site blocked every fetch this round. The earlier audit had the figures about 6% of 1,993 respondents; fielding in mid-2025 is recalled but not confirmed. The Stanford AI Index 2026 calls McKinsey's data "self-reported and should be viewed as directional." **[PRIMARY for the AI Index quote]**
- **MIT NANDA, "The GenAI Divide"** (July 2025, "Preliminary Findings") **[PRIMARY]**
  - "Research Period: January – June 2025."
  - Sample: 300+ public initiatives, 52 interviews and 153 survey responses. That is **not a large study**; drop "large."
  - It uses three different denominators: 95% of organizations get "zero return," 5% of integrated pilots extract "millions in value," and 5% of task-specific tools "reached production."
  - It calls its own figures "directionally accurate based on individual interviews rather than official company reporting."
- **2026 evidence**
  - NBER w34836, the only independent source: fielded Nov 2025 to Jan 2026, nearly 6,000 executives, "89% report no impact on labor productivity." Already in paragraph 8. **[PRIMARY]**
  - Deloitte 2026 (fielded Aug–Sep 2025, n=3,235): "25% of leaders now reporting that AI is having a transformative effect… more than double from 12% a year ago"; 20% are already increasing revenue. **[PRIMARY, vendor]**
  - BCG, Jul 22 2026: "Nine in ten CEOs say they are starting to see initial value from AI." It gives no share clearing its own high-performer bar. **[PRIMARY via summary, vendor]**
  - Wharton/GBK (fielded Jun–Jul 2025, n=801): "Most already report positive ROI (74%)." **[PRIMARY]**
- **Agents specifically:** none of the 2026 studies measures realized financial value from agents separately. They report use and expectations only.
- **Not confirmed:** McKinsey's fielding dates and definitions; PwC's 29th CEO Survey "56%" (403); any McKinsey 2026 edition.

**Defensible line:** surveys fielded in the first half of 2025 put the share of companies getting substantial value from AI at about one in twenty. Each measures value differently, all are self-reported, and none has been repeated in 2026. The one independent 2026 survey found nine in ten executives saw no productivity impact.

## 2i. Rung 2 build paths: open-source agent, framework, or your own loop (research round 2026-09-28)

**Verdict:** both frameworks and hand-written loops are common in production. A framework or vendor SDK gives you the loop, state and tool plumbing on day one. In exchange, you follow its release schedule, and a vendor harness ties you to that vendor's models and data rules. Writing your own loop gives full control, and you re-tune it as models change. No study measures the upkeep of any path in hours.

**How common each path is**
- **Pan et al., "Measuring Agents in Production"**, arXiv 2512.04123 (v4 Jun 2026; data Apr–Nov 2025) **[PRIMARY, checked]**
  - Interviews: "85% (17/20) build custom in-house implementations with direct API calls; only 3 use external frameworks (LangChain/LangGraph, DSPy)."
  - Survey: "two-thirds (60.7%) use third-party agentic frameworks." LangChain/LangGraph leads at 25.0% and CrewAI follows at 10.7%, from about 28–29 respondents.
  - Two teams "report starting with frameworks like CrewAI during the experimental prototyping phase but migrating to custom in-house solutions for production deployment to reduce dependency overhead."
  - The reasons given are flexibility and simplicity: "core agent loops are straightforward to implement directly."
- **LangChain, State of Agent Engineering** (Nov–Dec 2025, n=1,340): no framework-versus-custom figure. **[V]**
- **Stack Overflow 2025:** "Among developers building agents, Ollama (51%) and LangChain (33%) are the most-used frameworks."
- **PyPI downloads** (pypistats, fetched Sep 28 2026, last month): langgraph 43.7M, claude-agent-sdk 28.9M, openai-agents 12.1M, google-adk 9.9M, pydantic-ai 5.3M, crewai 2.4M.
  - Over the last six months, claude-agent-sdk and google-adk rose, langgraph held steady, and openai-agents, crewai and pydantic-ai fell.
  - **These are not adoption measures:** the counts are driven by CI, inflated by dependencies (langchain requires langgraph), and volatile.

**Advice**
- **Anthropic, "Building effective agents"** (Dec 2024) **[PRIMARY, checked]**
  - "the most successful implementations weren't using complex frameworks or specialized libraries."
  - "We suggest that developers start by using LLM APIs directly: many patterns can be implemented in a few lines of code. If you do use a framework, ensure you understand the underlying code."
  - The live post has been edited to list the Claude Agent SDK instead of LangGraph, and now points readers to Managed Agents.
- **OpenAI Agents SDK docs:** "Use the Responses API directly when: you want to own the loop, tool dispatch, and state handling yourself." Also: "You do not need to choose one globally." **[PRIMARY]**
- **HumanLayer, 12-factor agents** (2025): founders "Get to 70-80% quality bar… Realize that getting past 80% requires reverse-engineering the framework… Start over from scratch." Factor 8 is "Own your control flow." **[PRIMARY, vendor]**

**Who switched, and why**
- **Octomind** (2024) removed LangChain after 12 months in production: "our team began spending as much time understanding and debugging LangChain as it did building features." That was pre-1.0 LangChain.
- **Manus** (2025): "rebuilt our agent framework four times."
- **Vercel** (Dec 2025), its own code: "every model update meant re-calibrating our constraints." It then removed 80% of its tools, reporting 100% success on only 5 queries.
- **Harvey** (Jun 2026) built its own layer to be multi-model and keep zero data retention: "A frontier lab's runtime ties you to that lab's models — maximum lock-in."
- **Shopify Dispatch** (Jul 2026) is "a thin Ruby client" orchestrating child processes labelled "pi coding agent" (the MIT-licensed Pi agent). Its rationale: "build a harness that allows you to quickly migrate to the latest model."
- **Stripe** forked Goose in late 2024 and "focused our feature development of goose on the needs of minions."

**Upkeep**
- **Framework churn**
  - OpenAI Agents SDK: breaking changes go in minor versions. It shipped 22 minor versions from Jun 2025 to Aug 2026, 14 with migration notes (research agent's count). Some changes alter behaviour without any API change, for example switching the default model.
  - LangGraph: "no breaking changes until 2.0" (Oct 2025), kept so far at 1.2.x.
  - Pydantic AI: 1.0 to 2.0 in about 9.5 months.
  - Google ADK: 2.0 in May 2026.
- **Framework bugs.** Across AutoGen, CrewAI, LangChain and LangGraph, "API Incompatibility (12.00%)" of 1,000 sampled bug reports, against 2.9% in deep-learning frameworks (arXiv 2602.21806).
- **Forks.** Upstream goose shipped 86 releases in 2025 and 55 so far in 2026; each is merged or skipped. Stripe publishes no fork-maintenance cost.
- **Your own loop.** No measured hours. Anthropic: "Harnesses encode assumptions that go stale as models improve"; its context resets "had become dead weight" one model later.

**Vendor harness as a library or service: between rung 1 and rung 2**
- **Claude Agent SDK:** "A library that runs the Claude Code binary" **[checked]**.
  - You control your infrastructure, tools, MCP servers, hooks, permissions, subagents and skills.
  - You don't control the loop internals (a closed binary), the model family (Claude only), or the pace of change (133 releases in 2026 so far).
- **OpenAI Codex SDK:** drives the Codex app-server. The Codex CLI is Apache-2.0, so it can be forked.
- **Anthropic Managed Agents** (hosted): "Pre-built, configurable agent harness that runs in managed infrastructure." It is in beta. It stores history and sandbox state server-side, so it "is not currently eligible for Zero Data Retention" **[checked]**. Anthropic pitches it as keeping the harness current for you; Harvey's objection is lock-in to one lab's models and data rules.

**Defensible line:** a framework or vendor SDK is the fastest way to a working agent, and you pay by following someone else's releases and, for a vendor harness, its models and data rules. Your own loop costs more to start and keeps needing re-tuning as models change, but most deployed teams in the one interview study chose it for the control.

## 2f. Rung 1 evidence from other companies

Researched 2026-09-25 to answer the author todo about rung 1 results. The evidence splits cleanly in two, and the split *is* the rung 1 argument.

### Gains are real at the level of the person

**Microsoft, Claude Code and Copilot CLI rollout, early 2026. [PRIMARY — Murphy-Hill, Butler, Savelieva, arXiv 2607.01418]**
Tens of thousands of engineers. Adopters "merged roughly 24% more pull requests than they would have otherwise," sustained over four months. Adoption spread through social networks rather than formal channels. The authors' own caveat: "a merged PR is not the same as the value it delivers." This is the cleanest large-scale rung 1 result: vendor agents, no custom harness, a measurable individual effect.

### Gains mostly fail to reach the company

**Faros AI, "The AI Productivity Paradox," July 2025. [PRIMARY — faros.ai; vendor telemetry]**
Over 10,000 developers across 1,255 teams. High-adoption teams completed 21% more tasks and merged 98% more pull requests, but review time rose 91%, average PR size 154%, and bugs per developer 9%. At company level: "we observed no significant correlation between AI adoption and improvements at the company level"; the gains "do not scale when aggregated." Mechanism: faster code generation fills a review queue that did not speed up.

**Humlum and Vestergaard, "Large Language Models, Small Labor Market Effects," NBER / Becker Friedman Institute 2025. [PRIMARY]**
Adoption surveys of over 25,000 workers in 7,000 Danish workplaces linked to administrative records. Average time saved about 3%. "Precise null effects on earnings and recorded hours at both the worker and workplace levels," ruling out effects above 2% two years on. The null held for intensive users, early adopters and heavily investing workplaces. Adoption led to task restructuring and job switching "without net changes in hours or earnings." The time saved was reabsorbed.

**Why this matters:** three independent sources, one at a single large company, one across 1,255 teams, one across an economy, all say the same thing. Rung 1 value is real at the person and mostly invisible at the company. That is the section's claim, now with evidence rather than an illustration. The Faros mechanism adds a detail worth using: the bottleneck moved to review, which is a workflow problem, not a model problem.

### The companies with dramatic results moved to rung 2

**Stripe, Minions, Feb 9 2026. [PRIMARY — stripe.dev]**
Over a thousand pull requests merged each week are "completely minion-produced," human-reviewed but with no human-written code. Built from a fork of Block's open-source agent Goose. Stripe built its own because vendor agents struggle with "hundreds of millions of lines" of custom Ruby with proprietary libraries, under financial-compliance constraints. What made it work: isolated devboxes, **MCP connectivity to an internal "Toolshed" of 400+ tools**, deterministic test layers, and "the same coding rules humans use in Cursor and Claude Code."

**Ramp, Inspect, 2026. [PRIMARY — builders.ramp.com, "Why We Built Our Own Background Agent"]**
About 30% of merged pull requests to its frontend and backend repos written by Inspect within a couple of months, with no mandate. Later reports put it at 40% and a single-day peak of 57%. **[SECONDARY for 40% and 57%]** Ramp's reason: "Owning the tooling lets you build something significantly more powerful than an off-the-shelf tool will ever be." Integrated with Sentry, Datadog, LaunchDarkly, Braintrust, GitHub, Slack and Buildkite, with sandboxed full dev environments so it can check its own work.

### What the pair of findings says

1. **The biggest reported agent results come from companies that left rung 1.** Stripe and Ramp both built their own agent. That is the rung 1 to rung 2 transition, documented by the companies themselves, with their reasons stated.
2. **Their rung 1 work carried over.** Stripe's 400-tool MCP Toolshed and its shared coding rules are exactly the rung 1 investments the post describes, and they became the foundation of the rung 2 agent. Ramp's integrations are the same. Rung 1 is not wasted when you climb; it is what you climb on.
3. **Both kept humans in review** and both built environments where the agent can verify its own work, which is rung 2's reliability work.

### Status

- Microsoft, Faros, Humlum and Vestergaard, Stripe and Ramp's first-party figures: **[PRIMARY]**.
- Faros is a vendor selling measurement; its telemetry is still the largest dataset here. Say so.
- Ramp 40% and 57%: **[SECONDARY]**.
- **Not used:** a claim that Microsoft discontinued Claude Code licences for most engineers over cost; a "median 6.4 hours per week" figure attributed to McKinsey and Slack; Duolingo's review-time figure; a "21,000 developer hours" figure for Stripe. None confirmed at source.

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
