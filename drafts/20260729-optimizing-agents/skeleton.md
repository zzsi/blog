# Skeleton: topic-sentence draft

One line per planned paragraph: the claim it makes, then the evidence it will use. Read top to bottom as the argument. Figures appear where they would sit.

Sources in brackets point to the working notes: **BV** = business-value.md, **EM** = emerging.md, **V** = version20260912.md (the audited old draft).

Marks: **[YOU]** needs your first-hand material. **[DECIDE]** a choice to make before drafting. **[CUT?]** a candidate for removal.

Working title: **[DECIDE]**, settle after reading this.

---

## Opening

1. Agent demos work in the first week and break when they meet real data, real permissions and real users.
   - Reuse V opening line.

2. An agent is a model working inside a system, so a failure can sit in the model, the context, the tools, the workflow, or the check that should have caught it.
   - No evidence needed; this is the framing.

3. Across model generations the model dominates, but within the current top tier the system around it decides how much of the model's ability you actually get.
   - SWE-bench from under 5% in late 2023 to over 80% by late 2025 [V, audited].
   - Harness changes alone move the same model 8 to 13 points in controlled studies [V, audited].

4. The question that decides your work is what you own, and there are three answers.
   - Deploy a vendor's agent. Build your own agent on a vendor's model. Make the model yours too.

5. If you think in build versus buy, this is that, with two things to buy: the agent and the model.

6. Autonomy is not a fourth rung. It is a dial set at every rung by what a silent error costs.
   - Forward reference to paragraph 16.

---

## What each rung buys

7. The three rungs buy different kinds of value, each limited by something different.
   - Throughput, limited by how many people you have. A dependable process, limited by how much work arrives. Structural advantage, limited by how fast the frontier catches up [BV §1].

8. Most of what gets reported as agent value is rung 1 value, and it is the hardest kind to bank.
   - Forward reference to paragraph 11.

9. The evidence behind these claims is mostly self-reported survey data, so treat the direction as solid and any specific multiple as marketing.
   - BCG 5%, McKinsey ~6%, MIT 5%: three denominators, a convergence, not a concentration finding [V, audited].
   - **[CUT?]** Could be one sentence rather than a paragraph.

---

## Rung 1: integration and adoption

10. At rung 1 you deploy someone else's agent against your own systems, and the work is integration, guardrails, enablement, and redesigning the workflow around it.
    - A server connecting a vendor agent to your data is rung 1; the same server inside an agent you built is rung 2 [outline spine].

11. Rung 1 value is real but dispersed, so it rarely reaches the P&L unless someone changes how the work is organised.
    - An hour a day across 100 people is 23,000 hours a year, arriving in pieces too small to remove a cost [BV §2b, illustrative].
    - Workflow redesign is McKinsey's strongest correlate of EBIT impact, stronger than any technology factor [BV, verified].

12. You cannot let a team point an agent at real systems without permissions, sandboxing and audit, which makes guardrails part of rung 1.
    - Capability benchmarks test almost no injection resistance [V].
    - EU AI Act Article 14 requires a person be able to override or stop high-risk systems; applies December 2027 and August 2028, not August 2026 [BV §2c, verified].

13. **[YOU]** A first-hand paragraph on helping a team adopt agents: what stalled, what changed when the workflow did.
    - The enablement program is the obvious source. Nothing is written up yet.
    - **[DECIDE]** If there is no story here, rung 1 shrinks to paragraphs 10 to 12.

---

## Rung 2: harness engineering

14. At rung 2 you build your own agent on a model someone else owns, and most of the engineering depth in this post lives here.
    - Retrieval lives here too: it became something the agent does rather than something done to it [outline].

15. Every agent run ends one of three ways: right, escalated to a person, or wrong without escalating, and teams measure the second while the third decides the economics.
    - Three-outcome model [BV §2b].

16. On legal form extraction, the same agent is a million-dollar annual saving or a loss, depending only on what one silent error costs downstream.
    - $30 error: saves $1.08M at 90% coverage. $300: saves $645K at 50%. $3,000: loses $90K [BV §2b, illustrative inputs, curve from the doc AI post].
    - **FIGURE:** cost per document against coverage, three curves for three error costs. Replaces the old J-curve.

17. Minimising human intervention, the metric most teams track, pushes coverage past the point where it pays.
    - At full coverage the three cases save 70%, cost 182% more, cost 2,702% more [BV §2b].

18. Making the agent more reliable still pays most, and pays more as the stakes rise, because it opens up work you could not previously trust it with.
    - At $3,000 an error, today's agent earns 10% coverage and a tenfold better one earns 50% [BV §2b].
    - **[DECIDE]** Paragraphs 15 to 18 are the strongest material in the post. Keep here, or promote to their own section?

19. Separating right from confidently wrong needs a confidence signal, and the reliable ones come from agreement across components and deterministic checks, not from asking the model.
    - Six methods table, cheapest first [BV §2d].
    - Verbalized confidence now ranks better than logprobs on post-2025 models but is not well calibrated [BV §2d, verified].

20. Calibration needs a few hundred labelled examples, and your escalation queue is already producing them.
    - Every escalated item gets a human verdict, which is a label [BV §2d].

21. Verifiers fail in two directions, and public benchmarks show both.
    - SWE-bench: 61.1% of samples flagged for tests that reject valid solutions. UTBoost: 345 wrong patches recorded as passing. SWE-bench Pro graders: 8.5% false positive, 24% false negative [V, audited].

22. I found both failures building a small eval suite for custom agents: agents that took shortcuts past loose checks, and correct solutions failed by strict ones.
    - First-hand [V, filled slot 1].

23. Context is the scarcest resource an agent has, and managing what it still knows is the core of the job.
    - Compaction 86% fewer tokens with one sub-metric declining; memory taking accuracy from 2.5% to over 50%; o3 keeping 64.1% of its performance when instructions are split across turns [V, audited].
    - First-hand: the one-page memory prompt that ran sixty experiments; schema compaction at 97% agreement [V].

24. The biggest efficiency win comes from leaning on default tools, not building more of them.
    - Code execution over tools: 150,000 tokens to 2,000 [V, verified].

25. Coordination is something you design for the agents you deploy, and also something that emerges on its own whenever many agents share writable state.
    - Four-condition test for deliberate multi-agent [V].
    - OpenAI and Hugging Face, July 2026: about 1,200 agents built a message board from a leaky cache, invented mailboxes, voting rules and message signing, and about 700 attacked Hugging Face [EM §1, METR primary].
    - **[DECIDE]** One paragraph or two. It is vivid and readers will remember it.

26. One rule covers every layer: take the cheapest reversible step that clears your eval, and escalate only when it plateaus.

27. Owning the internals of your harness, such as the loop, memory or compaction policy, keeps you at rung 2 but makes every upgrade your problem.
    - Upgrade test: when the next version ships, do you install it or merge it? [V]

---

## Rung 3: model engineering

28. At rung 3 the model is yours, which is what ML engineering meant before the generative era.

29. The received advice in 2026 is not to fine-tune, and it rests on real evidence.
    - 70% of production agents prompt off-the-shelf models; OpenAI closed self-serve fine-tuning to new users; prompt optimisation beats GRPO at 35x fewer rollouts [outline, verified].

30. Tuning wins where the right answer is not public.
    - Bridgewater: tuned Qwen3-235B at 84.66% against Claude Opus 4.8 at 78.2%, 29.8% fewer mistakes, 13.8x cheaper to run [BV §2e, verified].
    - Harvey Tenet: Kimi K3 post-trained with RL, +12.1 citation quality at a tenth of the cost [BV §2e, verified].

31. On complex document extraction, tuned 3B and 8B models beat the strongest model our deployment allowed.
    - 0.92 against 0.82 on transcription fields; 0.87 against 0.55 on the full field set [BV §2e, first-hand].
    - The capability was already there; tuning bought the output contract.

32. The cost of trying fell by an order of magnitude.
    - Managed fine-tuning $8.00 per million training tokens in 2023 to $0.48 in 2026; GRPO from seven GPUs to one [BV §2e, verified].
    - **FIGURE:** reuse fig2, relabelled "cost of tuning".

33. What you can train depends on what supervises the training, and budget cannot substitute for having the right signal.
    - Supervision table, four rows: demonstrations, preference pairs, teacher, verifier [EM §2].

34. Post-training is now several steps, and the newest step lets you train narrow specialists separately and merge them.
    - Multi-teacher on-policy distillation: DeepSeek V4, Nemotron 3 Ultra [EM §2, verified].
    - For a client: three narrow tasks become three small teachers and one student.

35. The eval you built at rung 2 is what makes rung 3 possible, because it becomes the training environment.
    - Train on your failures [V].

---

## Where this is heading: self-improvement

36. Labs now report agents doing real research work, and the people running those labs disagree in public about how fast to go.
    - OpenAI's automated research intern and March 2028 target; Pachocki's call for slowdowns the same month; Jack Clark's 60% by 2028 [EM §3.1].

37. Most self-improvement shipping today rewrites the harness, not the model weights, which puts its leading edge at rung 2.
    - AIDE², Ouroboros, Darwin Gödel Machine, Recursive [EM §3.2, §3.3].

38. It works exactly as far as a verifier reaches, and where there is a verifier, it overfits to it.
    - Google's RRSI: unregularised harness evolution wins on Harvey's legal benchmark and loses elsewhere [EM §3.3b].
    - Rise and collapse: RL self-training peaks then falls about 17 points [EM §3.3b].
    - **FIGURE, maybe:** RRSI Table 1 as a small chart.

39. For a client, the practical lesson is that the scorer is the asset.
    - **[DECIDE]** Whether this section is three paragraphs or a short coda.

---

## How to decide

40. Place your problem on a rung by what you own and what is failing.
    - Reviewing everything means the measurement layer is missing. Unexplained downstream rework means silent errors are unpriced. Dispersed saved hours mean the workflow was never redesigned [BV §2b].

41. Two numbers set the operating point at rung 2, and most teams have neither: what a silent error costs, and the coverage-versus-error curve for their own data.

42. Enter rung 3 when prompting has plateaued and you have a training signal; volume decides whether it pays, not whether it works.

---

## Close

43. The numbers in this post will date within a year, and the structure should not.

44. **[YOU]** End on the failures actually witnessed and what they share: someone skipped measurement and went straight to the machinery.
    - The prior draft's ending, trimmed [V].

---

## Reading notes

- **44 paragraphs** at 150 to 200 words each gives roughly 7,000 to 8,500 words.
- **Five first-hand passages** so far (22, 23, 31, and the GEPA overfitting note to place near 38). Rung 1 has none. That is the largest gap.
- **Material left out on purpose:** most survey statistics, the six other RSI papers, the full case-study table, the cost-per-task discussion. It stays in the notes.
- **Decisions to settle before drafting:** title; paragraph 13; whether 15 to 18 become their own section; RSI length; paragraph 9.
