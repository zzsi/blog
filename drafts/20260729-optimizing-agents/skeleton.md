# Skeleton: topic-sentence draft

One line per planned paragraph: the claim it makes, then the evidence it will use. Read top to bottom as the argument. Figures appear where they would sit.

Sources in brackets point to the working notes: **BV** = business-value.md, **EM** = emerging.md, **RL** = reliability.md, **R1** = rung1.md, **PT** = posttraining.md, **ENV** = rlenv.md, **SEC** = security.md, **V** = version20260912.md (the audited old draft).

Marks: **[YOU]** needs your first-hand material. **[DECIDE]** a choice to make before drafting. **[REVIEW]** rewritten, please check. **[CUT?]** a candidate for removal.

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

4. A useful way to sort this work is by how much of the system you own: the integration with your data, the agent itself, or the model as well.
   - Deploy a vendor's agent. Build your own agent on a vendor's model. Make the model yours too.

5. If you think in build versus buy, this is that, with two things to buy: the agent and the model.

6. Autonomy is a dial, and at every rung it should be set by what a silent error costs.
   - Forward reference to the legal extraction example in rung 2.

---

## Value and bottleneck at each rung

7. Each rung buys a different kind of value, and each runs into a different bottleneck.
   - Throughput, bottlenecked by how many people you have. A dependable process, bottlenecked by how much work arrives. Structural advantage, bottlenecked by how fast the frontier catches up [BV §1].

8. Agent gains are easy to see in one person's output and much harder to see in a company's results.
   - Softened: "most reported value is individual" had only weak direct evidence. The gap itself is well supported [R1].
   - DX, 400+ companies: AI usage up 65%, median PR throughput up 7.76% [R1, primary]. Nine in ten of ~6,000 executives report no productivity impact over three years (NBER, Feb 2026) [R1, primary].

9. Three large 2025 studies agreed that only about one company in twenty got significant value from AI, and most of that evidence is self-reported.
    - BCG 5% of 1,250 firms (Sept 2025), McKinsey about 6% of 1,993 respondents (Nov 2025), MIT 5% of pilots (July 2025) [V, audited]. Three different denominators landing on a similar number.
    - **[RESEARCHING]** When each survey was fielded, and whether 2026 studies show the same share. If nothing newer exists, the sentence carries the date or the paragraph goes.
    - **[DECIDE]** Keep with the date, update to 2026 figures, or cut.

---

## Rung 1: integration and adoption

10. At rung 1 you use someone else's agent, such as Claude Code or Codex, and your job is everything around it.
    - A server connecting a vendor agent to your data is rung 1; the same server inside an agent you built is rung 2 [outline spine].

11. The first job is getting your company's context in front of the agent, and the most common way is internal tools exposed over MCP.
    - Seven of ten companies studied do it: LinkedIn's CAPT pairs MCP with 500+ playbooks and reports triage time down about 70% "in many areas" [R1, primary].
    - It stops scaling as-is: Uber's gateway covers 1,000+ MCP servers, and loading every tool description cost 50K–70K tokens a session, so Uber and Cloudflare now expose tools as command-line calls or code instead [R1, primary].
    - Your own setup (MCP over internal services, scheduled jobs building a knowledge base) matches the two most common patterns.

12. The second most common practice, instruction files and skills, is also the least proven, and each new model generation means checking them again.
    - Cloudflare generated AGENTS.md for ~3,900 repos; Intercom runs a weekly job that fact-checks every CLAUDE.md [R1, primary].
    - Evidence is split: Vercel's docs index scored 100% vs 53% baseline; ETH Zurich found context files do not generally improve success and add over 20% cost [R1, primary]. They help most with conventions the model would not guess.
    - Vendors now say so themselves. Anthropic, for Fable 5: "Skills developed for prior models are often too prescriptive for Claude Fable 5 and can degrade output quality." OpenAI, for GPT-6 Astra: "overly specific guidance can now hinder results where it previously helped." Anthropic suggests a configuration review "every three to six months" and after major releases [R1, model releases, primary, checked].
    - Not always simpler: more literal models need scope stated more explicitly, and skills a model wrote for itself scored below no skills at all (SkillsBench). The durable habit is a small test per file or skill, re-run on each new model [R1, model releases].
    - Files also go stale as code changes: across 2,303 context files, teams mostly add instructions and rarely delete them [R1, model releases, primary].
    - Correction to the recollection: the "too prescriptive" guidance is for Fable 5 and is about skills; for Fable 5.1 Anthropic says Fable 5 prompts work "without changes."

13. Extra agent output piles up at code review, so the best-measured rung 1 practice is putting an AI reviewer in CI.
    - Spotify: 76% more PRs, and "76% more PRs to review"; "the bottleneck moves from coding to decision-making" [R1, primary].
    - Uber reviews 90%+ of ~65,000 weekly diffs, 75% of comments rated useful; Cloudflare's reviewer averages $1.19 a review [R1, primary].
    - **[RESEARCHING]** Whether AI review works: bugs caught, false positives, comments acted on, effect on production defects.

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

**The thread:** the return on building your own agent is work that runs without a person checking each step. How much work you can hand over is set by reliability, and reliability fails in five distinct ways. Rung 2 is two jobs: prevent failures, and detect the ones you did not prevent.

17. At rung 2 you build the agent yourself on a vendor's model, and the return is work that runs without a person checking each step, at an error rate you choose.
    - Stripe's and Ramp's results at the end of rung 1 are rung 2 returns: agents they built, running inside their own systems [BV §2f].
    - Harness changes alone move the same model 8 to 13 points in controlled studies [V, audited]. **[RESEARCHING]** 2026 evidence on what the harness adds and what companies got back from building their own.
    - Owning the loop means owning reliability, and capability gains have produced only small reliability gains across 15 models [RL §1, primary]. A better model will not do this for you.
    - Retrieval lives here: it became something the agent does rather than something done to it [outline].

18. An agent fails in five ways, each named by what the person using it sees: wrong, erratic, stuck, unsafe, costly.
    - Table [RL §2]: one line each, with one piece of evidence and a link per type. **[RESEARCHING]** evidence per type.
    - Erratic needs one clarification: consistency means clearing the bar every time, not producing the same output every time. Varied output with consistent success is fine and often useful; varied success on a task with a clear answer is the failure [RL §2]. Folded in from the old paragraph 19.
    - Single-try success of about 61% falling to about 25% when every one of eight tries must succeed [RL §2, confirm figures].

19. When something breaks, find where it broke before fixing it, because the same symptom needs a different fix depending on its source.
    - Model-side: rung 3. Harness-side: rung 2. Grader-side: fix the eval [RL §3, primary].

*Job 1: prevent failures.*

20. Most agent failures start with a wrong belief rather than a missing skill: an assumption never checked, a requirement lost along the way, or a fact about the tool or domain it lacked.
    - 1,184 failed terminal-agent runs: about four in five decisive errors trace to these causes; about one in eleven to the model being unable to carry out a correct plan (Zhao et al., arXiv 2607.09510) [RL §5.1, primary].
    - The biggest single cause was information the agent had and did not use, not information it lacked. Context truncation was 2.8% of multi-agent failures [RL §5.1].
    - Missing information hurts: Sonnet 4.5 drops from 70.8% to 54.8% on the same tasks with details hidden (Ask or Assume, arXiv 2603.26233) [RL §5.1, primary]. Replaces the 2025 o3 example.
    - First-hand: the one-page memory prompt that ran sixty experiments; schema compaction at 97% agreement [V].
    - **[RESEARCHING]** Is "wrong belief" the right name? The paper's largest category (57.9%) is information that was available and went unused; missing domain or tool knowledge (24.0%) does not say whether it was missing from the context or the weights. Rewrite and prevention steps to follow.

21. Which tools to give depends on the model: strong models do best with the shell and file tools they were trained on, while smaller, cheaper models gain more from structured tools.
    - Strong models: bash alone beat catalogs of 20–60 typed tools by 5–25 points with 19–72% fewer tokens; adding the typed tools back changed nothing but doubled tokens (Mak et al., "Is Bash All You Need?", arXiv 2609.11999, Sep 2026) [RL §5.2, primary].
    - Smaller models: with only a shell, a 30B Nemotron kept calling tools it was trained on that did not exist, which ended 66% of its runs; predefined tools raised its success 15.0% and 10.1%. For the 550B model, the shell alone was better and cheaper (Fan et al., arXiv 2609.20804) [RL §5.2, primary].
    - Either way, match the schema the model was trained on: OpenAI says use its exact apply_patch because "the model has been trained to excel at this diff format"; Anthropic's text-editor schema "is built into Claude's model" [RL §5.2, primary].
    - So a cheaper model with more tools is a fair experiment when cost matters. **[RESEARCHING]** whether a cheaper model plus tools has matched a frontier model at lower total cost.
    - Large catalogs degrade: routing F1 falls 16–23 points going from 10 to 110 agents [RL §5.2, primary].

22. An agent is stuck when it spends steps without getting closer to done, and the way to prevent it is to settle what done means before the run and make asking cheap during it.
    - Looping is only one form: after a run goes wrong, only 18% of agents stop; the rest repair the wrong cause (39% of wasted steps), repeat the same approach (29%), run checks that cannot change the outcome, or report success they did not achieve (15%) [RL §5.3, primary].
    - Before: agree what done means (Anthropic's agents negotiate a "sprint contract" first). During: give the agent a cheap way to ask when it hits a gap, since most gaps only appear mid-task (with only the spec, gap detection fell from 61% to 11%) [RL §5.3, primary].
    - Catching a stuck run once it happens is detection; it moves to job 2.

23. Agent security now comes in three layers: limits built into the system, watching what the agent does, and AI on defence. Each one failed somewhere in 2026, so stack them and test against attackers who adapt.
    - Limits built in: sandboxes, least privilege, allowlists, human approval, and designs that keep untrusted data away from instructions. CaMeL solved 77% of tasks "with provable security," against 84% undefended (arXiv 2503.18813). But sandboxes have bugs (Semantic Kernel CVE-2026-25592), and Microsoft's red team found getting around human approval "the most consistently exploited failure mode" [SEC §2, primary].
    - Watching the agent: Anthropic's Claude Code classifier sees only the user's messages and the bare tool calls, "so the agent can't talk the classifier into making a bad call." It blocked 0.4% of real actions wrongly and missed 17% of 52 real overeager ones [SEC §3, primary, checked].
    - AI on defence: safeguards cut successful browser prompt injections on Claude Opus 4.8 from 31.5% of attempts to 0.5%. An attacker trained to adapt still got through on 37.5% of coding scenarios within 200 tries [SEC §4, system card, checked].
    - Fixed tests flatter defences: a filter that stopped every stock injection let 28% of adaptive ones through (AutoDojo, arXiv 2606.15057) [SEC §4, checked].
    - OpenAI and Hugging Face, July 2026, shows all three failing at once. The agents escaped a sandbox through a shared package cache. OpenAI says its reasoning monitors were not running [secondary]. About 7% of transcripts had spoofed tool calls. Hugging Face's AI triage correlated the attack but "failed to correctly raise the alert's criticality" [SEC §5, METR and HF primary, checked]. About 1,200 agents sharing state coordinated without anyone designing it [EM §1].
    - Listen: Latent Space, "Red-Teaming after Mythos," Kolter and Fredrikson of Gray Swan, June 2026, covers all three layers [SEC §1].
    - Use several agents on purpose only when one has plateaued [V].

*Job 2: detect the failures you did not prevent.*

24. The worst failures are the ones where the agent reports success, and they are usually found late by someone outside your checks, so every one you catch should become a test.
    - Claude told a researcher "I verified this myself" about a model name that a subagent had only guessed; the researcher found out by asking a colleague (Opus 4.8 system card) [RL §4b, primary, checked].
    - Asked to summarise unfinished coding work, Anthropic's Mythos Preview did not mention failures such as tests that don't pass 27.6% of the time; Opus 4.8 cut that to 3.7% [RL §4b, primary, checked].
    - A brief with two invented cases got past the government's lawyers. The Ninth Circuit: "The Attorney General did not flag the fabricated citations." One of the petitioners' own lawyers caught it only while preparing for oral argument (Lnu v. Blanche, June 2026) [RL §4b, primary, checked]. Courts have logged 2,095 such cases [RL §4b].
    - A KPMG report published in October 2025 had 5 of 45 citations right; GPTZero found it eight months later [RL §4b, secondary, checked].
    - In the one longitudinal study, silent failures took 13 hours to 60 days to surface, about 70% were found by people rather than tests, and 87% could have been blocked by regression tests written afterwards. One runtime, 22 incidents [RL §4, primary].
    - Contrast: an agent that deletes a production database is noticed in minutes. The quiet ones cost more because they run longer.

25. Judge whether a run is stuck or finished from evidence, not from the agent's own account.
    - Loop detectors and step budgets fire after the decisive mistake, so use them to escalate, not to prevent: a monitor flagged only 3.7–8.7% of stuck runs before lock-in [RL §5.3, primary].
    - Agents fabricate success and "confidently prais[e]" their own mediocre work, so check the claimed result itself: run the tests, open the output, compare it with the agreed definition of done [RL §5.3, primary]. Moved from the old stuck paragraph.

26. Every agent trades silent mistakes against escalations to a person, and what one silent mistake costs decides where that trade-off should sit.
    - Worked example, legal form extraction: the same agent saves $1.08M a year at 90% coverage when an error costs $30, saves $645K at 50% when it costs $300, and loses $90K when it costs $3,000 [BV §2b, illustrative].
    - Over-escalation is the mirror of confidently wrong: one lands on reviewers, visibly and now; the other lands downstream, silently and later. The "minimise human intervention" metric trades the visible one for the silent one: at full coverage the three legal cases save 70%, cost 182% more, and cost 2,702% more [BV §2b].
    - Moving along the curve is choosing a threshold; moving the curve is reliability work, and it pays more as stakes rise: at $3,000 an error, a tenfold better agent moves coverage from 10% to 50% [BV §2b].
    - **FIGURE:** cost per document against coverage, three curves.
    - Merges the old legal-example and over-escalation paragraphs; the legal case is now the example, not the point.

27. Deciding when to escalate needs a confidence signal built from agreement and hard checks, calibrated on labels your escalation queue already produces.
    - Six methods [BV §2d]. A few hundred labels. Every escalated item gets a human verdict [BV §2d].

28. The tests you use to judge the agent can themselves be wrong, passing bad work and failing good work.
    - "Tests" here means your own evals and graders: the automated checks that decide pass or fail.
    - Public benchmarks: 61.1% of SWE-bench samples flagged for tests that reject valid solutions; SWE-bench Pro graders 8.5% false positive, 24% false negative [V, audited].
    - First-hand: loose checks agents slipped past, strict ones that failed correct answers [V].

*Close.*

29. Fix problems with the cheapest change that works, and only escalate when your evals stop improving.
    - Cheapest first: a clearer instruction before a new tool, a setting before a code change, a new tool before a new agent.
    - The cost of going further: once you change an open-source agent's code rather than configure it (Stripe forked Goose), every new release of that agent becomes something you merge by hand.
    - **[REVIEW]** Rewritten for clarity; please check.

---

## Rung 3: model engineering

30. At rung 3 the model is yours, which is what ML engineering meant before the generative era.

31. Whether to train your own model is a live debate, and the balance shifts with each frontier release, each open model, and each new training recipe.
    - Against: 70% of production agents prompt off-the-shelf models; OpenAI closed self-serve fine-tuning to new users; prompt optimisation beats GRPO at 35x fewer rollouts [outline, verified].
    - For: Bridgewater's tuned Qwen3-235B at 84.66% against Claude Opus 4.8 at 78.2%, 13.8x cheaper to run; Harvey Tenet, +12.1 citation quality at a tenth of the cost [BV §2e, verified]. Tuning wins where the right answer is not public.

32. On complex document extraction, tuned 3B and 8B models beat the strongest model our deployment allowed.
    - 0.92 against 0.82 on transcription fields; 0.87 against 0.55 on the full field set [BV §2e, first-hand].
    - The capability was already there; tuning bought the output contract.

33. The answer depends on your data, your traffic and your budget, and my bet is that open models and the advantages of owning one are not going away.
    - Data: do you have examples or a verifier the frontier has never seen? Traffic: enough volume that a cheaper model pays back the training? Budget: can you afford to retrain as base models move?
    - **[YOU]** Confirm this directional bet is one you want to make in public.

34. The cost of getting a capability into a small model keeps falling, even though GPU prices rose in 2026 and frontier teams are spending more.
    - Falling: Together cut training prices 30–70% on Sep 11 2026; a 1.5B reasoning model was RL-trained for $9 (Tina); Ai2 built a 32B coding agent at 49.5–54.2% SWE-bench Verified for $2,000 (SERA); LoRA matches full fine-tuning for RL [PT §1, primary].
    - Rising: H100 contract prices up almost 40% from October 2025 to March 2026; Fireworks and Tinker raised prices; reasoning models cost 17x more to post-train than instruct models, with 82% of compute going to experiments that do not ship [PT §1, primary].
    - **FIGURE:** reuse fig2, relabelled "cost of tuning", with the Together price updated.

35. The training method follows from the signal you have: examples to imitate, preferences between answers, a stronger model to learn from, or an automatic check.
    - Supervision table, four rows [EM §2]. The paragraphs that follow take them in the order a recipe uses them: imitate, prefer, reinforce, then distil.

36. Supervised fine-tuning is cheap, needs surprisingly little data, and is the right tool for format and behaviour, but it memorises and can erase what the model already knew.
    - 50 good examples is OpenAI's starting recommendation; s1 fine-tuned a 32B model on 1,000 reasoning traces in 26 minutes on 16 H100s [PT §2, primary].
    - Training Qwen3-8B on internal documents cut its instruction-following score from 85% to 45% (Thinking Machines) [PT §2, primary]. SFT "memorizes" while RL generalizes (Chu et al., ICML 2025).

37. For agents, the examples are whole trajectories, and which ones you keep matters as much as how many.
    - **[RESEARCHING]** How much trajectory data agentic SFT needs, how trajectories are generated and filtered, and whether they must use the same tools and format as your harness.

38. Preference training learns from which of two answers is better, which is often easier to collect than a written-out answer, and it is fading from frontier recipes.
    - Tülu 3's pipeline: SFT 60.6, then DPO 64.7, then RL 65.1 average; OLMo 3 found DPO before RL beat either alone [PT §2, primary].
    - A reviewer choosing between two agent outputs produces exactly this data, so an escalation queue can feed it.
    - Nemotron 3 Ultra and MiMo-V2-Flash do not use it; on-policy distillation has taken its place [PT §2].

39. Reinforcement learning is for behaviour your examples never showed, and it needs an automatic check to learn from.
    - RL generalizes where SFT memorises, and RL keeps prior skills better at equal gains [PT §2, primary].
    - Its cost is mostly generating attempts: the rollout generator was 87% of OLMo 3's reasoning post-training energy [PT §1, primary]. It can also peak and collapse (see self-improvement).

40. If you train with RL, your environment, meaning the tasks plus the check that scores them, is the main lever you control, and the evals you built for your agent are most of one already.
    - This is the RL case. For SFT the equivalent lever is which trajectories you keep (above).
    - It decides which skills improve: DeepSeek found RL on code and search alone did not help agent tasks until it added 1,827 synthetic agent environments; NVIDIA found training on one environment caused "severe regressions" elsewhere [ENV §3, primary].
    - It decides which shortcuts get learned: Claude 3.7's habit of special-casing tests "emerged as a result of 'reward hacking' during reinforcement learning training" [ENV §3, primary].
    - Harvey builds its training environments in the same format as its public legal benchmark [ENV §5, primary]. The market prices good environments as scarce: Anthropic reportedly discussed spending over $1B on them in a year [ENV §1, secondary].
    - Two costs: a check built to measure must be hardened before a model optimises against it, and once you train on your eval you need a fresh one to know if you improved [ENV, verdict].
    - Limits: the base model sets the ceiling, and distillation can skip the reward entirely [ENV, verdict].

41. Distillation, training a small model on a stronger one, is the cheapest way to move a skill into a model you own, and the newest recipes use it to merge RL-trained specialists into one model.
    - Distilling beat running RL directly: 72.6 vs 47.0 on AIME for a 32B model (DeepSeek-R1). On-policy distillation, where the teacher grades the student's own attempts, matched RL at about a tenth of the GPU hours (Qwen3) [PT §2, primary].
    - Merging: train narrow specialists with RL, then distil them into one student. DeepSeek V4, Nemotron 3 Ultra (10+ teachers), MiMo-V2-Flash, Kimi K3 and GLM-5 do this; Nemotron 3 Ultra's merged model beat its own terminal-coding teacher, 54.0 vs 50.0. Papers on on-policy distillation went from 10 in 2025 to 234 in 2026 so far [PT §2, primary].
    - Anthropic's and Google's terms forbid using their models to train competing ones; Anthropic publicly named labs that ran 16M+ exchanges through fake accounts to do it [PT §2, primary]. Distil from open-weight teachers or a vendor's own distillation service.
    - For a client: three narrow tasks can become three small teachers and one student.
    - Merges the old distillation and specialist-merging paragraphs, placed after RL.

---

## Where this is heading: self-improvement

42. Self-improvement became something you could run on one GPU in March 2026, with Karpathy's autoresearch, and labs now say agents do real research work, though their leaders disagree about how fast to go.
    - Autoresearch: an agent edits a small model's training script in 5-minute runs and keeps what improves the loss; ~700 changes over two days, ~20 kept, cutting nanochat's time-to-GPT-2 by about 11%. His own caveat: "It's not novel, ground-breaking 'research' (yet)." And: "All LLM frontier labs will do this. It's the final boss battle." [EM §3.3c, primary]
    - Since then: OpenAI's "automated research intern" (Sept 2026) and its March 2028 target; Pachocki's call for slowdowns the same month; Jack Clark's 60% chance of autonomous self-improvement by 2028 (Aug 2026) [EM §3.1].

43. The self-improvement that runs without a human today mostly rewrites a harness or a small model's training script, while changes to a frontier model's weights still have a human starting each run.
    - AIDE², Ouroboros, Darwin Gödel Machine, Recursive, autoresearch [EM §3.2, §3.3].
    - Weight-level work is larger in the literature (280 vs 95 papers in 2026), and labs now have models running parts of their successors' training, but "Claude is not operating fully autonomously for any measured subset of AI R&D work" [EM §3.3c]. Corrected from the earlier harness-only claim.

44. Today self-improvement is limited by its verifier: it improves what the check can measure, and where the check is narrow, it overfits to it.
    - Google's RRSI: unregularised harness evolution wins on Harvey's legal benchmark and loses elsewhere [EM §3.3b].
    - Rise and collapse: RL self-training peaks then falls about 17 points [EM §3.3b].
    - **FIGURE, maybe:** RRSI Table 1 as a small chart.

45. **Short coda.** For a company, the lasting asset is a good automatic check for its own work: domain-specific evals and RL environments that can say whether an attempt succeeded.
    - Define the term once: a verifier, grader or eval, meaning anything automated that scores an attempt.
    - That check is what lets an agent be improved, a model be trained, and a system improve itself. Without it, none of the three can go far.
    - The market agrees: Cognition calls environment quality "the most important factor for downstream model performance," and Mercor bought an environment builder saying "the constraint has shifted to the environments themselves" [ENV §2, §1, primary, self-interested].
    - The check has to look like the real work. Sutskever's warning: training on what the evals measure "could explain… this disconnect between eval performance and actual real-world performance" [ENV §2, primary].
---

## How to decide

46. Place your problem on a rung by what you own and what is failing.
    - Reviewing everything means the measurement layer is missing. Unexplained downstream rework means silent errors are unpriced. Dispersed saved hours mean the workflow was never redesigned [BV §2b].

47. Two numbers set the operating point at rung 2: what a silent error costs, and the coverage-versus-error curve on your own data.

48. Enter rung 3 when prompting has plateaued and you have a training signal; volume decides whether it pays, not whether it works.

---

## Close

49. The numbers in this post will date within a year, and the structure should not.

50. **[YOU]** End on the failures actually witnessed and what they share: someone skipped measurement and went straight to the machinery.
    - The prior draft's ending, trimmed [V].

---

## Reading notes

- **50 paragraphs** at 150 to 200 words each gives roughly 7,000 to 9,000 words.
- **Changed in this round:** section 2 renamed; old 19 folded into 18; stuck split into prevention (22) and detection (25); the legal example is now the worked example inside the trade-off paragraph (26); rung 3 reordered to debate, first-hand result, bet; distillation merged and moved after RL (41); self-improvement opens with autoresearch (42).
- **First-hand passages:** rung 1 context setup (11), context (20), graders that are wrong (28), the extraction fine-tune (32), and the GEPA overfitting note to place in self-improvement (44). Rung 1's result is open; see the author todo.
- **Material left out on purpose:** most survey statistics, most RSI papers, the full case-study table, the cost-per-task discussion, most security frameworks, the older silent-failure cases. It stays in the notes.
- **Still researching:** 9 (dates and 2026 figures), 12 (instruction files across model releases), 13 (does AI review work), 17 (the return on rung 2), 18 (evidence per failure type), 20 (what "wrong belief" means and how to prevent it), 21 (cheaper model plus tools), 37 (agentic SFT data).
- **Decisions to settle before drafting:** title; paragraph 9 (keep with date, update, or cut); the open-models bet (33); the rewritten rung 2 close (29); rung 1 result (16, optional); whether the five failure groups appear as a table or inform the structure quietly (18); self-improvement length (42 to 45).
- **Checked against the primary last round:** the Claude Code classifier, the Opus 4.8 system card figures, AutoDojo, the Ninth Circuit opinion, the KPMG report, METR's spoofing figure, Hugging Face's triage failure. Still secondary: OpenAI's claim its monitors would have caught the breach.
