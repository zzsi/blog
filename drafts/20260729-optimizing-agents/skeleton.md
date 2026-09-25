# Skeleton: topic-sentence draft

One line per planned paragraph: the claim it makes, then the evidence it will use. Read top to bottom as the argument. Figures appear where they would sit.

Sources in brackets point to the working notes: **BV** = business-value.md, **EM** = emerging.md, **RL** = reliability.md, **V** = version20260912.md (the audited old draft).

Marks: **[YOU]** needs your first-hand material. **[DECIDE]** a choice to make before drafting. **[CUT?]** a candidate for removal.

Working title: **[DECIDE]**, settle after reading this.

## Author todo

- **Rung 1 result.** Did the rung 1 setup (MCP over internal services, scheduled jobs building a knowledge base) produce value you could point to, like time saved or a decision made faster? If yes, rung 1 gets a concrete result. If not, that also fits the section's own claim that rung 1 value is real but hard to measure. Feeds the last paragraph of rung 1.
  - **Partly answered by outside evidence (BV §2f).** Rung 1 now has company evidence either way; your own result is a bonus, not a requirement.

## Opening

1. Agent demos work in the first week and break when they meet real data, real permissions and real users.
   - Reuse V opening line.

2. An agent is a model working inside a system, so a failure can sit in the model, the context, the tools, the workflow, or the check that should have caught it.
   - No evidence needed; this is the framing.

3. Across model generations the model dominates, but within the current top tier the system around it decides how much of the model's ability you actually get.
   - SWE-bench from under 5% in late 2023 to over 80% by late 2025 [V, audited].
   - Harness changes alone move the same model 8 to 13 points in controlled studies [V, audited].

4. The first question is which parts of the system are yours: the connections to your data, the agent itself, or the model too.
   - Deploy a vendor's agent. Build your own agent on a vendor's model. Make the model yours too.

5. If you think in build versus buy, this is that, with two things to buy: the agent and the model.

6. Autonomy is not a fourth rung. It is a dial set at every rung by what a silent error costs.
   - Forward reference to the legal extraction example in rung 2.

---

## What each rung buys

7. The three rungs buy different kinds of value, each limited by something different.
   - Throughput, limited by how many people you have. A dependable process, limited by how much work arrives. Structural advantage, limited by how fast the frontier catches up [BV §1].

8. Most of what gets reported as agent value is rung 1 value, and it is the hardest kind to bank.
   - Forward reference to where rung 1 value stalls.

9. The evidence behind these claims is mostly self-reported survey data, so treat the direction as solid and any specific multiple as marketing.
   - BCG 5%, McKinsey ~6%, MIT 5%: three denominators, a convergence, not a concentration finding [V, audited].
   - **[CUT?]** Could be one sentence rather than a paragraph.

---

## Rung 1: integration and adoption

10. At rung 1 you use someone else's agent, such as Claude Code or Codex, and your job is everything around it.
    - A server connecting a vendor agent to your data is rung 1; the same server inside an agent you built is rung 2 [outline spine].

11. The first job is getting your context in front of the agent: wrap internal services in MCP so it can reach them, and run scheduled jobs that turn raw data into a knowledge base it can read.
    - This is context engineering done before the agent runs. At rung 2 the same work moves inside the harness.
    - First-hand: this is how you work. The compaction repo, described generically, is the example.

12. The second job is governing it, both technically and organisationally.
    - Technical: sandboxing, permission allowlists, hooks that block risky actions, secrets kept out of reach, audit logs. Vendor harnesses ship these settings; many teams leave them at defaults.
    - Organisational: who may use which agent on which data, what needs sign-off, how incidents are reported. This is the HMT connection.
    - Capability benchmarks test almost none of this [V]. EU AI Act Article 14 requires a person be able to override or stop high-risk systems, from December 2027 and August 2028 [BV §2c, verified].

13. Rung 1 value is real at the person and mostly invisible at the company.
    - Microsoft: tens of thousands of engineers on Claude Code and Copilot CLI merged about 24% more PRs [BV §2f, primary].
    - Faros, 10,000+ developers: 98% more PRs, 91% longer reviews, no company-level improvement; the bottleneck moved to review [BV §2f, primary].
    - Denmark, 25,000 workers: about 3% time saved, precise null effect on hours and earnings [BV §2f, primary].
    - Workflow redesign is McKinsey's strongest correlate of EBIT impact [BV, verified]. That is what converts saved hours into removed cost.

14. The companies with the biggest agent results left rung 1, and their rung 1 work is what they built on.
    - Stripe: 1,000+ merged PRs a week with no human-written code, from a fork of Goose, on an MCP "Toolshed" of 400+ internal tools and the same coding rules its engineers use in Claude Code [BV §2f, primary].
    - Ramp: about 30% of merged PRs within months; "owning the tooling lets you build something significantly more powerful than an off-the-shelf tool will ever be" [BV §2f, primary].
    - Bridge to rung 2.
    - **[YOU, optional]** One sentence on your own setup and what it produced, if there is a result.

---

## Rung 2: harness engineering

**The thread:** once you build your own agent, making it reliable is your job, and reliability fails in five distinct ways. Rung 2 is two jobs: prevent failures, and detect the ones you did not prevent.

15. At rung 2 you build the agent yourself on a vendor's model, so you now own the loop, and with it the agent's reliability.
    - Capability gains have produced only small reliability gains across 15 models [RL §1, primary]. A better model will not do this for you.
    - Retrieval lives here: it became something the agent does rather than something done to it [outline].

16. An agent fails in five ways, and each looks different to the person using it: wrong, erratic, stuck, unsafe, costly.
    - Table [RL §2]. One line each, named by what the user sees.

17. Consistency means clearing the bar every time, not producing the same output every time.
    - Varied output with consistent success is fine and often useful. Varied success on a task with a clear answer is the failure [RL §2].
    - Single-try success of about 61% falling to about 25% when every one of eight tries must succeed [RL §2, confirm figures].

18. When something breaks, find where it broke before fixing it, because the same symptom needs a different fix depending on its source.
    - Model-side: rung 3. Harness-side: rung 2. Grader-side: fix the eval [RL §3, primary].

*Job 1: prevent failures.*

19. Most wrong and erratic behaviour traces to what the agent knew, or did not, when it acted.
    - Compaction 86% fewer tokens with one sub-metric declining; memory taking accuracy from 2.5% to over 50%; o3 keeping 64.1% of its performance when instructions are split across turns [V, audited].
    - First-hand: the one-page memory prompt that ran sixty experiments; schema compaction at 97% agreement [V].

20. Using the default tools better beats building more tools, for both cost and capability.
    - 150,000 tokens to 2,000 [V, verified]. Defaults are co-trained with the model, so replacing them costs capability [V].

21. Being stuck is a harness problem: give the agent termination conditions, step budgets, and a way to notice it is looping.
    - Not knowing when to stop and repeating steps are among the most common modes in multi-agent traces [RL §2, secondary percentages].

22. Unsafe behaviour gets new attack surfaces every year, and many agents sharing state will coordinate whether you designed it or not.
    - Microsoft's 2026 taxonomy: goal hijacking, poisoned MCP tool descriptions, session contamination, trust escalation between agents [RL §2, primary].
    - OpenAI and Hugging Face, July 2026: about 1,200 agents built a message board from a leaky cache and about 700 attacked Hugging Face [EM §1, METR primary].
    - Use several agents on purpose only when one has plateaued [V].

*Job 2: detect the failures you did not prevent.*

23. Silent failures surface late and are mostly found by people, so every one you catch should become a regression test.
    - 13 hours to 60 days to discovery; about 70% found by human observation; 87% blockable by regression tests written afterwards [RL §4, primary].

24. On legal form extraction, the same agent saves a million dollars a year or loses money, depending only on what one confidently wrong answer costs downstream.
    - $30 error: saves $1.08M at 90% coverage. $300: saves $645K at 50%. $3,000: loses $90K [BV §2b, illustrative].
    - **FIGURE:** cost per document against coverage, three curves.

25. Over-escalation is the mirror of confidently wrong, and the "minimise human intervention" metric trades the visible one for the silent one.
    - Mirror table [RL §2]. At full coverage the legal cases save 70%, cost 182% more, and cost 2,702% more [BV §2b].
    - More reliability pays more as stakes rise: at $3,000 an error, a tenfold better agent moves coverage from 10% to 50% [BV §2b].

26. Deciding when to escalate needs a confidence signal built from agreement and hard checks, calibrated on labels your escalation queue already produces.
    - Six methods [BV §2d]. A few hundred labels. Every escalated item gets a human verdict [BV §2d].

27. Your checks can be wrong too, in both directions.
    - Public benchmarks: 61.1% of SWE-bench samples flagged for tests that reject valid solutions; SWE-bench Pro graders 8.5% false positive, 24% false negative [V, audited].
    - First-hand: loose checks agents slipped past, strict ones that failed correct answers [V].

*Close.*

28. Take the cheapest reversible step that passes your eval, and know that owning the harness's internals keeps you at rung 2 but makes every upgrade your problem.
    - Upgrade test: when the next version ships, do you install it or merge it? [V]

---

## Rung 3: model engineering

29. At rung 3 the model is yours, which is what ML engineering meant before the generative era.

30. The received advice in 2026 is not to fine-tune, and it rests on real evidence.
    - 70% of production agents prompt off-the-shelf models; OpenAI closed self-serve fine-tuning to new users; prompt optimisation beats GRPO at 35x fewer rollouts [outline, verified].

31. Tuning wins where the right answer is not public.
    - Bridgewater: tuned Qwen3-235B at 84.66% against Claude Opus 4.8 at 78.2%, 29.8% fewer mistakes, 13.8x cheaper to run [BV §2e, verified].
    - Harvey Tenet: Kimi K3 post-trained with RL, +12.1 citation quality at a tenth of the cost [BV §2e, verified].

32. On complex document extraction, tuned 3B and 8B models beat the strongest model our deployment allowed.
    - 0.92 against 0.82 on transcription fields; 0.87 against 0.55 on the full field set [BV §2e, first-hand].
    - The capability was already there; tuning bought the output contract.

33. The cost of trying fell by an order of magnitude.
    - Managed fine-tuning $8.00 per million training tokens in 2023 to $0.48 in 2026; GRPO from seven GPUs to one [BV §2e, verified].
    - **FIGURE:** reuse fig2, relabelled "cost of tuning".

34. What you can train depends on what supervises the training, and budget cannot substitute for having the right signal.
    - Supervision table, four rows: demonstrations, preference pairs, teacher, verifier [EM §2].

35. Post-training is now several steps, and the newest step lets you train narrow specialists separately and merge them.
    - Multi-teacher on-policy distillation: DeepSeek V4, Nemotron 3 Ultra [EM §2, verified].
    - For a client: three narrow tasks become three small teachers and one student.

36. The eval you built at rung 2 is what makes rung 3 possible, because it becomes the training environment.
    - Train on your failures [V].

---

## Where this is heading: self-improvement

37. Labs now report agents doing real research work, and the people running those labs disagree in public about how fast to go.
    - OpenAI's automated research intern and March 2028 target; Pachocki's call for slowdowns the same month; Jack Clark's 60% by 2028 [EM §3.1].

38. Most self-improvement shipping today rewrites the harness, not the model weights, which puts its leading edge at rung 2.
    - AIDE², Ouroboros, Darwin Gödel Machine, Recursive [EM §3.2, §3.3].

39. It works exactly as far as a verifier reaches, and where there is a verifier, it overfits to it.
    - Google's RRSI: unregularised harness evolution wins on Harvey's legal benchmark and loses elsewhere [EM §3.3b].
    - Rise and collapse: RL self-training peaks then falls about 17 points [EM §3.3b].
    - **FIGURE, maybe:** RRSI Table 1 as a small chart.

40. For a client, the practical lesson is that the scorer is the asset.
    - **[DECIDE]** Whether this section is three paragraphs or a short coda.

---

## How to decide

41. Place your problem on a rung by what you own and what is failing.
    - Reviewing everything means the measurement layer is missing. Unexplained downstream rework means silent errors are unpriced. Dispersed saved hours mean the workflow was never redesigned [BV §2b].

42. Two numbers set the operating point at rung 2, and most teams have neither: what a silent error costs, and the coverage-versus-error curve for their own data.

43. Enter rung 3 when prompting has plateaued and you have a training signal; volume decides whether it pays, not whether it works.

---

## Close

44. The numbers in this post will date within a year, and the structure should not.

45. **[YOU]** End on the failures actually witnessed and what they share: someone skipped measurement and went straight to the machinery.
    - The prior draft's ending, trimmed [V].

---

## Reading notes

- **45 paragraphs** at 150 to 200 words each gives roughly 7,000 to 9,000 words.
- **First-hand passages:** rung 1 context setup (11), context (19), verifiers (27), the extraction fine-tune (rung 3), and the GEPA overfitting note to place in self-improvement. Rung 1's result is open; see the author todo.
- **Material left out on purpose:** most survey statistics, most RSI papers, the full case-study table, the cost-per-task discussion. It stays in the notes.
- **Decisions to settle before drafting:** title; rung 1 result (14); whether the five failure groups appear as a table or inform the structure quietly (16); self-improvement length; paragraph 9.
