# Skeleton: topic-sentence draft

One line per planned paragraph: the claim it makes, then the evidence it will use. Read top to bottom as the argument. Figures appear where they would sit.

Sources in brackets point to the working notes: **BV** = business-value.md, **EM** = emerging.md, **RL** = reliability.md, **R1** = rung1.md, **V** = version20260912.md (the audited old draft).

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

3. Between model generations, the model decides what is possible; within the current top tier, the system around it decides how much of that you actually get.
   - This is about capability, not cost. Token cost is a separate axis, and it is part of the rung 3 argument.
   - SWE-bench from under 5% in late 2023 to over 80% by late 2025 [V, audited].
   - Harness changes alone move the same model 8 to 13 points in controlled studies [V, audited].

4. A useful way to sort this work is by how much of the system you own: the connections to your data, the agent itself, or the model as well.
   - Deploy a vendor's agent. Build your own agent on a vendor's model. Make the model yours too.

5. If you think in build versus buy, this is that, with two things to buy: the agent and the model.

6. Autonomy is a dial, and at every rung it should be set by what a silent error costs.
   - Forward reference to the legal extraction example in rung 2.

---

## What each rung buys

7. Each rung buys a different kind of value, and each runs into a different bottleneck.
   - Throughput, bottlenecked by how many people you have. A dependable process, bottlenecked by how much work arrives. Structural advantage, bottlenecked by how fast the frontier catches up [BV §1].

8. Agent gains are easy to see in one person's output and much harder to see in a company's results.
   - Softened: "most reported value is individual" had only weak direct evidence. The gap itself is well supported [R1].
   - DX, 400+ companies: AI usage up 65%, median PR throughput up 7.76% [R1, primary]. Nine in ten of ~6,000 executives report no productivity impact over three years (NBER, Feb 2026) [R1, primary].

9. Three large studies agree that only about one company in twenty gets significant value from AI, and most of that evidence is self-reported.
   - BCG 5% of 1,250 firms, McKinsey about 6% of 1,993 respondents, MIT 5% of pilots [V, audited]. Three different denominators landing on a similar number.
   - Kept as one short paragraph: the named sources are worth having.

---

## Rung 1: integration and adoption

10. At rung 1 you use someone else's agent, such as Claude Code or Codex, and your job is everything around it.
    - A server connecting a vendor agent to your data is rung 1; the same server inside an agent you built is rung 2 [outline spine].

11. The first job is getting your company's context in front of the agent, and the most common way is internal tools exposed over MCP.
    - Seven of ten companies studied do it: LinkedIn's CAPT pairs MCP with 500+ playbooks and reports triage time down about 70% "in many areas" [R1, primary].
    - It stops scaling as-is: Uber's gateway covers 1,000+ MCP servers, and loading every tool description cost 50K–70K tokens a session, so Uber and Cloudflare now expose tools as command-line calls or code instead [R1, primary].
    - Your own setup (MCP over internal services, scheduled jobs building a knowledge base) matches the two most common patterns.

12. The second most common practice, instruction files in each repo, is also the least proven.
    - Cloudflare generated AGENTS.md for ~3,900 repos; Intercom runs a weekly job that fact-checks every CLAUDE.md [R1, primary].
    - Evidence is split: Vercel's docs index scored 100% vs 53% baseline; ETH Zurich found context files do not generally improve success and add over 20% cost [R1, primary]. They help most with conventions the model would not guess.

13. Extra agent output piles up at code review, so the best-measured rung 1 practice is putting an AI reviewer in CI.
    - Spotify: 76% more PRs, and "76% more PRs to review"; "the bottleneck moves from coding to decision-making" [R1, primary].
    - Uber reviews 90%+ of ~65,000 weekly diffs, 75% of comments rated useful; Cloudflare's reviewer averages $1.19 a review [R1, primary].

14. Then govern it, technically, organisationally, and on cost.
    - Technical: Intercom's hook sorts every shell command into green, yellow or red from two weeks of transcripts; Cloudflare keeps API keys off every laptop; Pinterest allows only registered MCP servers in production [R1].
    - Cost: Uber shows a live cost counter, nudges at 50/80/100% of expected spend, defaults reasoning effort to medium, and held total spend flat while weekly users grew 7x [R1, primary].
    - Organisational: who may use which agent on which data, what needs sign-off, how incidents are reported. This is the HMT connection.
    - Capability benchmarks test almost none of this [V]. EU AI Act Article 14 requires a person be able to override or stop high-risk systems, from December 2027 and August 2028 [BV §2c, verified].

15. Adoption spreads through colleagues more than mandates, and the gains stay with the person unless the workflow changes.
    - Microsoft: engineers whose skip-level peers used Copilot CLI had 216% higher odds of trying it [R1, primary].
    - Microsoft: tens of thousands of engineers on Claude Code and Copilot CLI merged about 24% more PRs [BV §2f, primary].
    - Faros, 10,000+ developers: 98% more PRs, 91% longer reviews, no company-level improvement; the bottleneck moved to review [BV §2f, primary].
    - Denmark, 25,000 workers: about 3% time saved, precise null effect on hours and earnings [BV §2f, primary].
    - Workflow redesign is McKinsey's strongest correlate of EBIT impact [BV, verified]. That is what converts saved hours into removed cost.

16. The companies with the biggest agent results left rung 1, and their rung 1 work is what they built on.
    - Stripe: 1,000+ merged PRs a week with no human-written code, from a fork of Goose, on an MCP "Toolshed" of 400+ internal tools and the same coding rules its engineers use in Claude Code [BV §2f, primary].
    - Ramp: about 30% of merged PRs within months; "owning the tooling lets you build something significantly more powerful than an off-the-shelf tool will ever be" [BV §2f, primary].
    - Bridge to rung 2.
    - **[YOU, optional]** One sentence on your own setup and what it produced, if there is a result.

---

## Rung 2: harness engineering

**The thread:** once you build your own agent, making it reliable is your job, and reliability fails in five distinct ways. Rung 2 is two jobs: prevent failures, and detect the ones you did not prevent.

17. At rung 2 you build the agent yourself on a vendor's model, so you now own the loop, and with it the agent's reliability.
    - Capability gains have produced only small reliability gains across 15 models [RL §1, primary]. A better model will not do this for you.
    - Retrieval lives here: it became something the agent does rather than something done to it [outline].

18. An agent fails in five ways, and each looks different to the person using it: wrong, erratic, stuck, unsafe, costly.
    - Table [RL §2]. One line each, named by what the user sees.

19. Consistency means clearing the bar every time, not producing the same output every time.
    - Varied output with consistent success is fine and often useful. Varied success on a task with a clear answer is the failure [RL §2].
    - Single-try success of about 61% falling to about 25% when every one of eight tries must succeed [RL §2, confirm figures].

20. When something breaks, find where it broke before fixing it, because the same symptom needs a different fix depending on its source.
    - Model-side: rung 3. Harness-side: rung 2. Grader-side: fix the eval [RL §3, primary].

*Job 1: prevent failures.*

21. Most agent failures start with a wrong belief rather than a missing skill: an assumption never checked, a requirement lost along the way, or a fact about the tool or domain it lacked.
    - 1,184 failed terminal-agent runs: about four in five decisive errors trace to these causes; about one in eleven to the model being unable to carry out a correct plan (Zhao et al., arXiv 2607.09510) [RL §5.1, primary].
    - The biggest single cause was information the agent had and did not use, not information it lacked. Context truncation was 2.8% of multi-agent failures [RL §5.1].
    - Missing information hurts: Sonnet 4.5 drops from 70.8% to 54.8% on the same tasks with details hidden (Ask or Assume, arXiv 2603.26233) [RL §5.1, primary]. Replaces the 2025 o3 example.
    - First-hand: the one-page memory prompt that ran sixty experiments; schema compaction at 97% agreement [V].

22. Start with the tools the model was trained on, and add custom tools only when the shell cannot reach something.
    - Bash alone beat catalogs of 20–60 typed tools by 5–25 points with 19–72% fewer tokens; adding the typed tools back changed nothing but doubled tokens (Mak et al., "Is Bash All You Need?", arXiv 2609.11999, Sep 2026) [RL §5.2, primary].
    - Models are trained on specific tool schemas: OpenAI says use its exact apply_patch because "the model has been trained to excel at this diff format"; Anthropic's text-editor schema "is built into Claude's model" [RL §5.2, primary].
    - Exceptions: weaker models do better with structured file tools, and security rules can require a fixed catalog [RL §5.2].
    - Large catalogs degrade: routing F1 falls 16–23 points going from 10 to 110 agents [RL §5.2, primary].

23. An agent is stuck when it spends steps without getting closer to done, and looping is only one way that happens.
    - After a run goes wrong, only 18% of agents stop; the rest repair the wrong cause (39% of wasted steps), repeat the same approach (29%), run checks that cannot change the outcome, or report success they did not achieve (15%) [RL §5.3, primary].
    - Loop detectors and step budgets catch it after the decisive mistake, so they are for escalation, not prevention: a monitor flagged only 3.7–8.7% of stuck runs before lock-in [RL §5.3, primary].
    - Prevention happens before and during the run. Before: agree what done means (Anthropic's agents negotiate a "sprint contract" first). During: give the agent a cheap way to ask when it hits a gap, since most gaps only appear mid-task (with only the spec, gap detection fell from 61% to 11%) [RL §5.3, primary].
    - Deciding it is done should rest on evidence, not the agent's own judgement: agents fabricate success and "confidently prais[e]" their own mediocre work [RL §5.3, primary].

24. Unsafe behaviour gets new attack surfaces every year, and many agents sharing state will coordinate whether you designed it or not.
    - **[RESEARCHING]** Evidence under review; this line may change.
    - Microsoft's 2026 taxonomy: goal hijacking, poisoned MCP tool descriptions, session contamination, trust escalation between agents [RL §2, primary].
    - OpenAI and Hugging Face, July 2026: about 1,200 agents built a message board from a leaky cache and about 700 attacked Hugging Face [EM §1, METR primary].
    - Use several agents on purpose only when one has plateaued [V].

*Job 2: detect the failures you did not prevent.*

25. Silent failures surface late and are mostly found by people, so every one you catch should become a regression test.
    - **[RESEARCHING]** Evidence under review; this line may change.
    - 13 hours to 60 days to discovery; about 70% found by human observation; 87% blockable by regression tests written afterwards [RL §4, primary].

26. On legal form extraction, the same agent saves a million dollars a year or loses money, depending only on what one confidently wrong answer costs downstream.
    - $30 error: saves $1.08M at 90% coverage. $300: saves $645K at 50%. $3,000: loses $90K [BV §2b, illustrative].
    - **FIGURE:** cost per document against coverage, three curves.

27. Over-escalation is the mirror of confidently wrong, and the "minimise human intervention" metric trades the visible one for the silent one.
    - Mirror table [RL §2]. At full coverage the legal cases save 70%, cost 182% more, and cost 2,702% more [BV §2b].
    - More reliability pays more as stakes rise: at $3,000 an error, a tenfold better agent moves coverage from 10% to 50% [BV §2b].

28. Deciding when to escalate needs a confidence signal built from agreement and hard checks, calibrated on labels your escalation queue already produces.
    - Six methods [BV §2d]. A few hundred labels. Every escalated item gets a human verdict [BV §2d].

29. The tests you use to judge the agent can themselves be wrong, passing bad work and failing good work.
    - "Tests" here means your own evals and graders: the automated checks that decide pass or fail.
    - Public benchmarks: 61.1% of SWE-bench samples flagged for tests that reject valid solutions; SWE-bench Pro graders 8.5% false positive, 24% false negative [V, audited].
    - First-hand: loose checks agents slipped past, strict ones that failed correct answers [V].

*Close.*

30. Fix problems with the cheapest change that works, and only escalate when your evals stop improving.
    - Cheapest first: a clearer instruction before a new tool, a setting before a code change, a new tool before a new agent.
    - The cost of going further: once you modify an agent framework's code rather than configure it, every vendor update becomes something you have to merge by hand.
    - **[REVIEW]** Rewritten for clarity; please check.

---

## Rung 3: model engineering

31. At rung 3 the model is yours, which is what ML engineering meant before the generative era.

32. Whether to train your own model is a live debate, and the balance shifts with each frontier release, each open model, and each new training recipe.
    - Against: 70% of production agents prompt off-the-shelf models; OpenAI closed self-serve fine-tuning to new users; prompt optimisation beats GRPO at 35x fewer rollouts [outline, verified].
    - For: Bridgewater's tuned Qwen3-235B at 84.66% against Claude Opus 4.8 at 78.2%, 13.8x cheaper to run; Harvey Tenet, +12.1 citation quality at a tenth of the cost [BV §2e, verified]. Tuning wins where the right answer is not public.

33. The answer depends on your data, your traffic and your budget, and our bet is that open models and the advantages of owning one are not going away.
    - Data: do you have examples or a verifier the frontier has never seen? Traffic: enough volume that a cheaper model pays back the training? Budget: can you afford to retrain as base models move?
    - **[YOU]** Confirm this directional bet is one you want to make in public.

34. On complex document extraction, tuned 3B and 8B models beat the strongest model our deployment allowed.
    - 0.92 against 0.82 on transcription fields; 0.87 against 0.55 on the full field set [BV §2e, first-hand].
    - The capability was already there; tuning bought the output contract.

35. The cost of trying fell by an order of magnitude.
    - **[RESEARCHING]** Evidence under review; this line may change.
    - Managed fine-tuning $8.00 per million training tokens in 2023 to $0.48 in 2026; GRPO from seven GPUs to one [BV §2e, verified].
    - **FIGURE:** reuse fig2, relabelled "cost of tuning".

36. The training method follows from the signal you have: examples to imitate, preferences between answers, a stronger model to learn from, or an automatic check.
    - Supervision table, four rows [EM §2].
    - **[RESEARCHING]** Dedicated paragraphs on SFT, preference methods (DPO), and RL to follow.

37. Post-training is now several steps, and the newest step lets you train narrow specialists separately and merge them.
    - **[RESEARCHING]** Evidence under review; this line may change.
    - Multi-teacher on-policy distillation: DeepSeek V4, Nemotron 3 Ultra [EM §2, verified].
    - For a client: three narrow tasks become three small teachers and one student.

38. The eval you built at rung 2 is what makes rung 3 possible, because it becomes the training environment.
    - **[RESEARCHING]** Evidence under review; this line may change.
    - Train on your failures [V].

---

## Where this is heading: self-improvement

39. Labs now report agents doing real research work, and the people running those labs disagree in public about how fast to go.
    - OpenAI's automated research intern and March 2028 target; Pachocki's call for slowdowns the same month; Jack Clark's 60% by 2028 [EM §3.1].
    - Karpathy's autoresearch, March 2026: an agent edits a small model's training script in 5-minute runs and keeps what improves the loss; ~700 changes over two days, ~20 kept, cutting nanochat's time-to-GPT-2 by about 11%. "All LLM frontier labs will do this. It's the final boss battle." [EM §3.3c, primary]

40. The self-improvement that runs without a human today mostly rewrites a harness or a small model's training script, while changes to a frontier model's weights still have a human starting each run.
    - AIDE², Ouroboros, Darwin Gödel Machine, Recursive, autoresearch [EM §3.2, §3.3].
    - Weight-level work is larger in the literature (280 vs 95 papers in 2026), and labs now have models running parts of their successors' training, but "Claude is not operating fully autonomously for any measured subset of AI R&D work" [EM §3.3c]. Corrected from the earlier harness-only claim.

41. It works exactly as far as a verifier reaches, and where there is a verifier, it overfits to it.
    - Google's RRSI: unregularised harness evolution wins on Harvey's legal benchmark and loses elsewhere [EM §3.3b].
    - Rise and collapse: RL self-training peaks then falls about 17 points [EM §3.3b].
    - **FIGURE, maybe:** RRSI Table 1 as a small chart.

42. **Short coda.** For a company, the lasting asset is a good automatic check for its own work: domain-specific evals and RL environments that can say whether an attempt succeeded.
    - Define the term once: a verifier, grader or eval, meaning anything automated that scores an attempt.
    - That check is what lets an agent be improved, a model be trained, and a system improve itself. Without it, none of the three can go far.
---

## How to decide

43. Place your problem on a rung by what you own and what is failing.
    - Reviewing everything means the measurement layer is missing. Unexplained downstream rework means silent errors are unpriced. Dispersed saved hours mean the workflow was never redesigned [BV §2b].

44. Two numbers set the operating point at rung 2: what a silent error costs, and the coverage-versus-error curve on your own data.

45. Enter rung 3 when prompting has plateaued and you have a training signal; volume decides whether it pays, not whether it works.

---

## Close

46. The numbers in this post will date within a year, and the structure should not.

47. **[YOU]** End on the failures actually witnessed and what they share: someone skipped measurement and went straight to the machinery.
    - The prior draft's ending, trimmed [V].

---

## Reading notes

- **47 paragraphs** at 150 to 200 words each gives roughly 7,000 to 9,000 words.
- **First-hand passages:** rung 1 context setup (11), context (19), verifiers (27), the extraction fine-tune (rung 3), and the GEPA overfitting note to place in self-improvement. Rung 1's result is open; see the author todo.
- **Material left out on purpose:** most survey statistics, most RSI papers, the full case-study table, the cost-per-task discussion. It stays in the notes.
- **Decisions to settle before drafting:** title; rung 1 result (14); whether the five failure groups appear as a table or inform the structure quietly (16); self-improvement length; paragraph 9.
