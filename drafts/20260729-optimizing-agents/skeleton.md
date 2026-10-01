# Skeleton: topic-sentence draft

One line per planned paragraph: the claim it makes, then the evidence it will use. Read top to bottom as the argument. Figures appear where they would sit.

Sources in brackets point to the working notes: **BV** = business-value.md, **EM** = emerging.md, **RL** = reliability.md, **R1** = rung1.md, **PT** = posttraining.md, **ENV** = rlenv.md, **SEC** = security.md, **MA** = multiagent.md, **V** = version20260912.md (the audited old draft).

Marks: **[YOU]** needs your first-hand material. **[DECIDE]** a choice to make before drafting. **[REVIEW]** rewritten, please check. **[CUT?]** a candidate for removal.

Title: **How to Customize Agents, and When to Own Them** (decided).

## Author todo

- **Title: decided.** How to Customize Agents, and When to Own Them.
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
    - Surveys fielded in the first half of 2025 put the share of companies getting substantial value from AI at about one in twenty (BCG 5%, Sept 2025; McKinsey about 6%, Nov 2025; MIT NANDA 5% of pilots, Jan–Jun 2025). Each measures something different: BCG's is a maturity score executives rate themselves on, mostly "expected future impact"; MIT's rests on 52 interviews and 153 survey responses. None has been repeated in 2026, and lower bars give much higher numbers (74% report positive ROI, Wharton 2025) [BV §2h, primary, BCG checked].
    - Folded in from the old paragraph 9: no 2026 study re-measures the one-in-twenty bar, so it is dated context, not a headline. Restore it as its own paragraph if you want the point made.

---

## Rung 1: integration and adoption

9. At rung 1 you use someone else's agent, such as Claude Code or Codex, and your job is everything around it.
    - A server connecting a vendor agent to your data is rung 1; the same server inside an agent you built is rung 2 [outline spine].
    - Vendor agents now ship their own ways to run several agents: Claude Code subagents and agent teams (preview, Feb 2026), Codex parallel tasks and subagents, Cursor's parallel agents and subagents. Switching them on is still rung 1. Their docs agree: parallel agents cost more tokens, suit independent or read-heavy work, and should not edit the same files; Cursor: "The benefit is context isolation, not speed" [MA §4, primary, checked].

10. The first job is getting your company's context in front of the agent, and the most common way is internal tools exposed over MCP.
    - Seven of ten companies studied do it: LinkedIn's CAPT pairs MCP with 500+ playbooks and reports triage time down about 70% "in many areas" [R1, primary].
    - It stops scaling as-is: Uber's gateway covers 1,000+ MCP servers, and loading every tool description cost 50K–70K tokens a session, so Uber and Cloudflare now expose tools as command-line calls or code instead [R1, primary].
    - Your own setup (MCP over internal services, scheduled jobs building a knowledge base) matches the two most common patterns.

11. The second most common practice, instruction files and skills, is also the least proven, and each new model generation means checking them again.
    - Cloudflare generated AGENTS.md for ~3,900 repos; Intercom runs a weekly job that fact-checks every CLAUDE.md [R1, primary].
    - Evidence is split: Vercel's docs index scored 100% vs 53% baseline; ETH Zurich found context files do not generally improve success and add over 20% cost [R1, primary]. They help most with conventions the model would not guess.
    - Vendors now say so themselves. Anthropic, for Fable 5: "Skills developed for prior models are often too prescriptive for Claude Fable 5 and can degrade output quality." OpenAI, for GPT-6 Astra: "overly specific guidance can now hinder results where it previously helped." Anthropic suggests a configuration review "every three to six months" and after major releases [R1, model releases, primary, checked].
    - Not always simpler: more literal models need scope stated more explicitly, and skills a model wrote for itself scored below no skills at all (SkillsBench). The durable habit is a small test per file or skill, re-run on each new model [R1, model releases].
    - Files also go stale as code changes: across 2,303 context files, teams mostly add instructions and rarely delete them [R1, model releases, primary].
    - Correction to the recollection: the "too prescriptive" guidance is for Fable 5 and is about skills; for Fable 5.1 Anthropic says Fable 5 prompts work "without changes."

12. Extra agent output piles up at code review, and AI reviewers help as a first pass, but nobody has shown they reduce the bugs that reach production.
    - The pile-up: Spotify has "76% more PRs to review," and its answer is auto-merging what is safe, not an AI reviewer [R1, code review, primary, checked]. Corrected: the old line implied Spotify used AI review.
    - What AI review does: at Anthropic, PRs with substantive review comments went from 16% to 54%, with under 1% of findings marked incorrect, at $15–25 a review [vendor on own use, checked]. Cloudflare averages $1.19 a review and says "This isn't a replacement for human code review, at least not yet" [R1, code review, primary]. Uber's 90% coverage figure is from August 2025.
    - Its comments get acted on less than a person's: 39–74% lead to a change in tuned in-house systems, 1–36% in independent open-source studies, and human suggestions are adopted at "a significantly higher rate" wherever the two are compared [R1, code review, primary].
    - It catches a minority of what people catch: about 15–33% of human-flagged issues on 2026 benchmarks [R1, code review, primary].
    - Gaps: no controlled study of production defects; security was 2.0% of Meta's AI review comments against 19.1% of human ones; crafted PR descriptions got known vulnerabilities past AI review in 32 of 33 tries [R1, code review, primary].

13. Then govern it, technically, organisationally, and on cost.
    - Technical: Intercom's hook sorts every shell command into green, yellow or red from two weeks of transcripts; Cloudflare keeps API keys off every laptop; Pinterest allows only registered MCP servers in production [R1].
    - Cost: Uber shows a live cost counter, nudges at 50/80/100% of expected spend, defaults reasoning effort to medium, and held total spend flat while weekly users grew 7x [R1, primary].
    - Organisational: who may use which agent on which data, what needs sign-off, how incidents are reported. This is the HMT connection.
    - Capability benchmarks test almost none of this [V]. EU AI Act Article 14 requires a person be able to override or stop high-risk systems, from December 2027 and August 2028 [BV §2c, verified].

14. Adoption spreads through colleagues more than mandates, and the gains stay with the person unless the workflow changes.
    - Microsoft: engineers whose skip-level peers used Copilot CLI had 216% higher odds of trying it [R1, primary].
    - Microsoft: tens of thousands of engineers on Claude Code and Copilot CLI merged about 24% more PRs [BV §2f, primary].
    - Faros, 10,000+ developers: 98% more PRs, 91% longer reviews, no company-level improvement; the bottleneck moved to review [BV §2f, primary].
    - Denmark, 25,000 workers: about 3% time saved, precise null effect on hours and earnings [BV §2f, primary].
    - Workflow redesign is McKinsey's strongest correlate of EBIT impact [BV, verified]. That is what converts saved hours into removed cost.

15. The companies with the biggest agent results left rung 1, and their rung 1 work is what they built on.
    - Stripe: 1,300+ merged PRs a week with no human-written code (Feb 2026), from a fork of Goose, on an MCP "Toolshed" of 400+ internal tools and the same coding rules its engineers use in Claude Code [BV §2f, primary].
    - Ramp: about 30% of merged PRs within months; "owning the tooling lets you build something significantly more powerful than an off-the-shelf tool will ever be" [BV §2f, primary].
    - Bridge to rung 2.
    - **[YOU, optional]** One sentence on your own setup and what it produced, if there is a result.

---

## Rung 2: harness engineering

**The thread:** the return on building your own agent is work that runs unattended, inside your own systems, on the model you choose. How much work you can hand over is set by reliability, and reliability fails in five distinct ways. Rung 2 is two jobs: prevent failures, and detect the ones you did not prevent.

16. At rung 2 you build the agent yourself on a vendor's model, and the return is work that runs unattended, inside your own systems, on the model you choose.
    - Unattended: Stripe says off-the-shelf coding agents are built "as a companion to engineers," while its own "are fully unattended"; over 1,300 PRs a week are agent-written, human-reviewed, with no human-written code (Feb 2026) [BV §2g, primary, checked].
    - Inside your systems: Ramp's agent writes about 30% of merged PRs and is wired into Sentry, Datadog, LaunchDarkly and others; Stripe's reaches nearly 500 internal tools [BV §2g, primary].
    - On the model you choose: Harvey built its own runtime to run "on essentially any model" under zero data retention, and reports "3-5x cost reductions versus a frontier-only approach" [BV §2g, primary, checked].
    - The harness alone moves results: LangChain went from 52.8% to 66.5% on Terminal-Bench 2.0 changing only the harness (vendor, tuned on the same tasks); swapping typed tools for the shell took Opus 4.8 from 44.9% to 69.4% at a third of the cost per task [BV §2g, primary, checked]. Infrastructure alone moves that benchmark 6 points, so small gaps mean little.
    - The cost: harness gains decay as models improve ("Harnesses encode assumptions that go stale," Anthropic; Manus rebuilt its framework four times), and no public study compares an in-house agent with a vendor agent on the same work [BV §2g].
    - How much work you can hand over is set by reliability, and capability gains have produced only small reliability gains across 15 models [RL §1, primary]. Hence the rest of this section.
    - Retrieval lives here: it became something the agent does rather than something done to it [outline].

17. You can build on an open-source agent, on a framework, or directly on the model's API, and the choice is how much you inherit against how much you must keep up with.
    - Both are common in production: 17 of 20 deployed teams interviewed wrote their own loop on direct API calls, while about 60% of a small survey subset used a framework, LangGraph most often (Pan et al., data from 2025). Two teams prototyped on CrewAI and moved to their own code for production [BV §2i, primary, checked].
    - Vendor advice points the same way: "start by using LLM APIs directly," and with a framework, "ensure you understand the underlying code" (Anthropic); use the raw API "when you want to own the loop" (OpenAI's own SDK docs) [BV §2i, primary, checked].
    - A framework gives you the loop, state and tool plumbing on day one, and you follow its releases: OpenAI's Agents SDK shipped 22 minor versions in 14 months, most with migration notes, while LangGraph has kept a no-breaking-changes promise since its 1.0 [BV §2i, primary]. An open-source agent gives you a working agent, and then upstream moves: Goose shipped 86 releases in 2025 [BV §2i]. Your own loop gives full control, and you re-tune it as models change (Vercel: "every model update meant re-calibrating our constraints") [BV §2i, primary]. In every case the harness's assumptions go stale after launch: Anthropic's context resets "had become dead weight" one model later [BV §2i, primary]. Moved here from the rung 2 close: this is upkeep, not development.
    - A vendor's harness offered as a library or service sits between rung 1 and rung 2. The Claude Agent SDK runs the Claude Code binary: you control tools, hooks and permissions, not the loop or the model family. Anthropic's hosted Managed Agents is not eligible for zero data retention, one reason Harvey built its own [BV §2i, primary, checked].
    - The framework's design matters, not only the model: with the model fixed across nine frameworks, orchestration added over 60x latency (an implementation cost, not the pattern's), schema-constrained planning cut accuracy by up to 32 points through formatting failures, and a mismatched communication structure dropped coordination success from above 90% to below 30% (MAFBench, arXiv 2602.03128) [MA §8, primary, abstract].
    - Recommendation: prototype on whatever reaches a working eval fastest, then own the parts where reliability is decided: context, checks and escalation ("own your control flow," 12-factor agents) [BV §2i].
    - **[REVIEW]** New paragraph after author review; also check it matches how your team builds client agents.

18. Use several agents when the parts of the work do not need each other's context, or when a checker can test against something the writer cannot see; otherwise one agent is cheaper and fails in fewer ways.
    - With compute held equal, Google's study of 260 setups ranged from +80.8% on financial analysis that splits cleanly to −70.0% on sequential planning, and averaged about zero. Once one agent already scores above about 45%, adding agents hurt (arXiv 2512.08296, v3 Apr 2026) [MA §1, primary, checked].
    - Anthropic's 2026 guidance: several agents "consistently outperform" one only when context pollution degrades performance, when tasks can run in parallel, or when specialisation improves tool choice. They "typically use 3-10x more tokens," and teams have spent months on multi-agent designs "only to discover that improved prompting on a single agent achieved equivalent results" [MA §1, primary, checked, vendor].
    - The sceptics narrowed their view rather than reversing it: Cognition, author of "Don't Build Multi-Agents" (2025), now uses setups where "multiple agents contribute intelligence to a task while writes stay single-threaded" (Apr 2026) [MA §1, primary, checked].
    - In the big 2026 runs, a planner with workers worked, or flat peers backed by a near-perfect external check. Agents editing the same files or chasing the same bug broke them. Cursor: without hierarchy, "Twenty agents would slow down to the effective throughput of two or three." Anthropic's 16-agent C compiler depended on a verifier that is "nearly perfect" [MA §5, primary, checked].
    - Teams left to organise themselves average rather than defer: they failed to match their best member even when told who the expert was, losing up to 41.1% on ML benchmarks, and the averaging grew with team size (arXiv 2602.01011, Feb 2026) [MA §8, primary, abstract].
    - The old four-condition test, revised against this evidence: the parts do not need each other's context; the single agent hits a limit several agents address (context overflow, breadth, too many tools, lenient self-grading); writes stay with one agent or in separate files; and the gain beats the cost on the same token budget. "Plateaued" was risky: a strong single agent is exactly where extra agents hurt [MA §6].
    - Chained steps compound errors (five at 95% succeed together about 77%), but that applies to one agent doing five steps as well: an illustration, not a multi-agent finding [MA §2].
    - Cost grows at least in step with the number of agents; output grows more slowly. OpenAI's Noam Brown: four agents finish about twice as fast, "you're paying 2x more," and the speedup is "slightly sublinear, though it does depend a lot on the problem" (Dwarkesh, Sep 2026). Claude Code's docs: "Token costs scale linearly," while "additional teammates don't speed up work proportionally"; agent teams use about 7x the tokens of a normal session [MA §7, primary, checked].
    - Per token, one agent was about three times as efficient: 67.7 successes per 1,000 tokens against 21.5 for a coordinated team (Google). On tightly coupled coding it goes negative: success fell from 68.6% with two agents to 30.0% with four (CooperBench). Breadth-first search is the exception: Kimi's swarm reached its target 3 to 4.5 times faster [MA §7, primary, checked].
    - The ceiling comes from the part of the work that must run in order, coordination and merge conflicts, every agent re-reading the same context, and people: "our bottleneck became human QA capacity" (OpenAI) [MA §7, primary, checked].

19. An agent fails in five ways, each named by what the person using it sees: wrong, erratic, stuck, unsafe, costly.
    - **Shown as a table** (decided): type, what the person sees, one piece of evidence with its link, and where in this section it is handled [RL §2, §2b].
    - Wrong: a quarter of failed coding-agent runs claimed success with fake evidence (26%, Zhao et al. 2026); on τ-bench, most models' confidence "carr[ies] no information about correctness" (2602.16666) [RL §2b, primary].
    - Erratic: accuracy climbed over 24 months while "overall reliability shows only small improvements" (Princeton HAL) [RL §2b, primary, checked]. The classic number: GPT-4o at about 61% on one try, about 25% when all eight tries must succeed (τ-bench, 2024) [RL §2, confirmed]. Consistency means clearing the bar every time, not producing the same output; varied output with consistent success is fine [RL §2].
    - Stuck: 82% of failed recovery attempts keep running without progress (Zhao et al.); "slow, hanging, or excessive" was the top reason people interrupted Claude Code, 17% of 500k interruptions [RL §2b, primary; vendor, checked].
    - Unsafe: in a two-week red-team study, agents obeyed most requests from people who were not their owner, disclosing 124 email records (Agents of Chaos, 2026) [RL §2b, primary]. More in the security paragraph.
    - Costly: an agent got a complete answer to its first question, asked it seven more times and wrote no code ("Model or Harness?", 2026); multi-agent systems use about 15x the tokens of chat (Anthropic, 2025) [RL §2b, primary].
    - Be honest about costly: 2026 evidence mostly shows agents asking too little, and nobody has measured what over-escalation costs people. The mirror framing has a published name, under-initiative versus over-initiative [RL §2b, primary].
    - Fixing one type can cause another: planning that stopped a model quitting early raised its cost 75% [RL §2b, primary].
    - Several agents add a failure that is not a sixth type but multiplies the five: agents misreading or ignoring each other, and making the same mistake together. MAST found inter-agent misalignment in 32.3% of observed failures across 1,642 multi-agent traces (older frameworks); in Anthropic's tests, 18 of 30 agents independently created a git branch with the same name [MA §2, primary, checked].

20. When something breaks, find where it broke before fixing it, because the same symptom needs a different fix depending on its source.
    - Model-side: rung 3. Harness-side: rung 2. Grader-side: fix the eval [RL §3, primary].

*Job 1: prevent failures.*

21. Most failed runs start with the agent working from a wrong or incomplete picture of the task, not from an inability to do the work.
    - 1,184 failed terminal-agent runs (Zhao et al., 2026; the agents are 2025 models): 58% began with information the agent had or could have checked, the largest single cause being an assumption it never checked (31%), then a requirement it dropped (15%). 24% lacked tool or domain knowledge; 9% had a sound plan carried out badly; 9% hit the environment [RL §5.1b, primary].
    - Context or weights? The paper does not say. In a sample of its knowledge-gap cases, about half were tool or version facts that documentation would supply, and a few more were visible in the environment [RL §5.1b, research agent's reading, unvalidated]. So the 58% is not missing knowledge at all, and much of the 24% is a context problem.
    - The decisive mistake comes early, at a median of step 7 [RL §5.1b, primary].
    - Answers the author's question: "wrong belief" was too narrow, and the old "four in five" wrongly added the knowledge-gap share, which the paper counts as a skill problem.
    - First-hand: the one-page memory prompt that ran sixty experiments; schema compaction at 97% agreement [V].

22. Prevent it by giving the agent the facts it cannot know, a separate step to ask when the task is unclear, and room to look before it acts.
    - Facts it cannot know, kept short: Vercel's 8KB docs index scored 100% against a 53% baseline; curated skills added 16.6 points while comprehensive docs added 0.7 and self-written skills scored below none (SkillsBench) [RL §5.1b, primary].
    - Ask as its own step: a check for "is this underspecified?" recovered most of the 16 points Claude Sonnet 4.5 lost when details were hidden (54.8% to 69.4%, with a simulated user who knew the answer). But asking helps little when the gap only shows up mid-task: with an ask tool, Claude Opus 4.6 fell from 90.7% to 39.3% on SQL (HiL-Bench) [RL §5.1b, primary, checked].
    - Look before acting: agents that explore longer before their first edit succeed more, a correlation, and prompting for it matters less with stronger models [RL §5.1b, primary]. Plans written by people after exploration took Claude Code from 16.7 to 58.3 on 20 long tasks [RL §5.1b, primary, small].
    - Restating requirements is not enough; checking the result against them belongs in job 2 [RL §5.1b].
    - Not yet known: whether training beats context for tool knowledge. No 2026 head-to-head found.

23. Which tools to give depends on the model: strong models do best with the shell and file tools they were trained on, while smaller, cheaper models gain more from structured tools.
    - Strong models: bash alone beat catalogs of 20–60 typed tools by 5–25 points with 19–72% fewer tokens; adding the typed tools back changed nothing but doubled tokens (Mak et al., "Is Bash All You Need?", arXiv 2609.11999, Sep 2026) [RL §5.2, primary].
    - Smaller models: with only a shell, a 30B Nemotron kept calling tools it was trained on that did not exist, which ended 66% of its runs; predefined tools raised its SWE-Bench success from 10.2% to 25.2%. For the 550B model, the shell alone was better (65.8% to 69.4%) and cut cost 53% (Fan et al., arXiv 2609.20804) [BV §2g, primary, checked].
    - Either way, match the schema the model was trained on: OpenAI says use its exact apply_patch because "the model has been trained to excel at this diff format"; Anthropic's text-editor schema "is built into Claude's model" [RL §5.2, primary].
    - So a cheaper model with more tools is a fair experiment when cost matters, but no study yet shows one matching a frontier model: the 30B with tools reached 25.2% against 69.4% for the 550B. The closest is Anthropic's advisor setup, where Haiku consulting Opus scored 29% below Sonnet alone at 85% lower cost per task (vendor) [BV §2g, primary, checked]. Measure it on your task.
    - Large catalogs degrade: routing F1 falls 16–23 points going from 10 to 110 agents [RL §5.2, primary].

24. An agent is stuck when it spends steps without getting closer to done, and the way to prevent it is to settle what done means before the run and make asking cheap during it.
    - Looping is only one form: after a run goes wrong, only 18% of agents stop; the rest repair the wrong cause (39% of wasted steps), repeat the same approach (29%), run checks that cannot change the outcome, or report success they did not achieve (15%) [RL §5.3, primary].
    - Before: agree what done means (Anthropic's agents negotiate a "sprint contract" first). During: give the agent a cheap way to ask when it hits a gap, since most gaps only appear mid-task (with only the spec, gap detection fell from 61% to 11%) [RL §5.3, primary].
    - Catching a stuck run once it happens is detection; it moves to job 2.

25. Agent security now comes in three layers: limits built into the system, watching what the agent does, and AI on defence. Each one failed somewhere in 2026, so stack them and test against attackers who adapt.
    - Limits built in: sandboxes, least privilege, allowlists, human approval, and designs that keep untrusted data away from instructions. CaMeL solved 77% of tasks "with provable security," against 84% undefended (arXiv 2503.18813). But sandboxes have bugs (Semantic Kernel CVE-2026-25592), and Microsoft's red team found getting around human approval "the most consistently exploited failure mode" [SEC §2, primary].
    - Watching the agent: Anthropic's Claude Code classifier sees only the user's messages and the bare tool calls, "so the agent can't talk the classifier into making a bad call." It blocked 0.4% of real actions wrongly and missed 17% of 52 real overeager ones [SEC §3, primary, checked].
    - AI on defence: safeguards cut successful browser prompt injections on Claude Opus 4.8 from 31.5% of attempts to 0.5%. An attacker trained to adapt still got through on 37.5% of coding scenarios within 200 tries [SEC §4, system card, checked].
    - Fixed tests flatter defences: a filter that stopped every stock injection let 28% of adaptive ones through (AutoDojo, arXiv 2606.15057) [SEC §4, checked].
    - OpenAI and Hugging Face, July 2026, shows all three failing at once. The agents escaped a sandbox through a shared package cache. OpenAI says its reasoning monitors were not running [secondary]. About 7% of transcripts had spoofed tool calls. Hugging Face's AI triage correlated the attack but "failed to correctly raise the alert's criticality" [SEC §5, METR and HF primary, checked]. About 1,200 agents sharing state coordinated without anyone designing it [EM §1].
    - Listen: Latent Space, "Red-Teaming after Mythos," Kolter and Fredrikson of Gray Swan, June 2026, covers all three layers [SEC §1].

*Job 2: detect the failures you did not prevent.*

26. The worst failures are the ones where the agent reports success, and they are usually found late by someone outside your checks, so every one you catch should become a test.
    - Claude told a researcher "I verified this myself" about a model name that a subagent had only guessed; the researcher found out by asking a colleague (Opus 4.8 system card) [RL §4b, primary, checked].
    - Asked to summarise unfinished coding work, Anthropic's Mythos Preview did not mention failures such as tests that don't pass 27.6% of the time; Opus 4.8 cut that to 3.7% [RL §4b, primary, checked].
    - A brief with two invented cases got past the government's lawyers. The Ninth Circuit: "The Attorney General did not flag the fabricated citations." One of the petitioners' own lawyers caught it only while preparing for oral argument (Lnu v. Blanche, June 2026) [RL §4b, primary, checked]. Courts have logged 2,095 such cases [RL §4b].
    - A KPMG report published in October 2025 had 5 of 45 citations right; GPTZero found it eight months later [RL §4b, secondary, checked].
    - In the one longitudinal study, silent failures took 13 hours to 60 days to surface, about 70% were found by people rather than tests, and 87% could have been blocked by regression tests written afterwards. One runtime, 22 incidents [RL §4, primary].
    - Contrast: an agent that deletes a production database is noticed in minutes. The quiet ones cost more because they run longer.

27. Judge whether a run is stuck or finished from evidence, not from the agent's own account.
    - Loop detectors and step budgets fire after the decisive mistake, so use them to escalate, not to prevent: a monitor flagged only 3.7–8.7% of stuck runs before lock-in [RL §5.3, primary].
    - Agents fabricate success and "confidently prais[e]" their own mediocre work, so check the claimed result itself: run the tests, open the output, compare it with the agreed definition of done [RL §5.3, primary]. Moved from the old stuck paragraph.
    - Check requirements with something other than the agent: models restate a constraint while breaking it (8–99% across models, DriftBench), and a monitor given the requirements caught dropped ones 22% of the time instead of 3% [RL §5.1b, primary].
    - The strongest case for a second agent is as the checker, but its independence comes from what it tests against and how capable it is, not from being a different model. Shopify's verifier writes and runs tests against each finding, on a different model; in one audit all 30+ candidate vulnerabilities were downgraded or false positives. In a cross-model study, a stronger reviewer raised a weaker model's pass rate from 71.6% to 89.7%, while a weaker reviewer lowered a stronger model's from 91.4% to 82.8%. Errors also correlate across providers. A model reviewing its own output silently endorsed 31.7% of its flaws. Checking the intermediate steps of a multi-agent run "does not consistently improve performance" (MAS-ProVe), so check the outcome against something external [MA §3, §8, primary, checked].

28. Every agent trades silent mistakes against escalations to a person, and what one silent mistake costs decides where that trade-off should sit.
    - Worked example, legal form extraction: the same agent saves $1.08M a year at 90% coverage when an error costs $30, saves $645K at 50% when it costs $300, and loses $90K when it costs $3,000 [BV §2b, illustrative].
    - Over-escalation is the mirror of confidently wrong: one lands on reviewers, visibly and now; the other lands downstream, silently and later. The "minimise human intervention" metric trades the visible one for the silent one: at full coverage the three legal cases save 70%, cost 182% more, and cost 2,702% more [BV §2b].
    - Moving along the curve is choosing a threshold; moving the curve is reliability work, and it pays more as stakes rise: at $3,000 an error, a tenfold better agent moves coverage from 10% to 50% [BV §2b].
    - **FIGURE:** cost per document against coverage, three curves.
    - Merges the old legal-example and over-escalation paragraphs; the legal case is now the example, not the point.

29. Deciding when to escalate needs a confidence signal built from agreement and hard checks, calibrated on labels your escalation queue already produces.
    - Six methods [BV §2d]. A few hundred labels. Every escalated item gets a human verdict [BV §2d].

30. The tests you use to judge the agent can themselves be wrong, passing bad work and failing good work.
    - "Tests" here means your own evals and graders: the automated checks that decide pass or fail.
    - Public benchmarks: 61.1% of SWE-bench samples flagged for tests that reject valid solutions; SWE-bench Pro graders 8.5% false positive, 24% false negative [V, audited].
    - First-hand: loose checks agents slipped past, strict ones that failed correct answers [V].

*Close.*

31. While you build, climb your eval with the cheapest change that works: a clearer instruction before a new tool, a setting before a code change, a new tool before a new agent.
    - What climbing looks like: LangChain moved its agent from 52.8% to 66.5% on Terminal-Bench 2.0 by iterating on the harness alone, and warns that "Changes that overfit to a task are bad for generalization" [BV §2g, primary, checked].
    - So climb on one set and confirm on another you never tune on; the prompt-optimisation overfitting in the self-improvement section is what happens otherwise.
    - Each failure you fix should leave a test behind, so the climb only goes up (the silent-failures paragraph).
    - **[REVIEW]** Rewritten after author review: this paragraph is now the development loop; upkeep after launch moved to the build-paths paragraph.

32. When harness changes stop moving your eval, what is left usually needs a more capable model on your task, and you can wait for the next frontier release or make one yourself: that is rung 3.
    - Most failure modes are of this kind: a 2026 taxonomy counts a failure as model-side when "a more capable model could have prevented it or recovered from it," and assigns 36 of 41 modes that way ("Model or Harness?", Scale AI) [BV §2g, primary, checked]. Its authors name these as "targets for post-training."
    - Two more reasons a harness cannot fix: the token bill at your volume, and data that cannot leave your walls. The extraction fine-tune and Harvey's zero-data-retention runtime are examples [BV §2e, §2i].
    - The teams with the most mature harnesses went on to train: Cursor trains Composer inside its production harness, Cognition trained SWE-1.5, and Fin now runs its own model and reports a higher resolution rate than with Sonnet 4.6 [ENV §2, §5; BV §2g, primary, vendor].
    - What carries over: the eval you climbed is most of a training environment already. Hand it to rung 3 with a fresh held-out set [ENV].
    - **[REVIEW]** New bridge paragraph after author review.

---

## Rung 3: model engineering

33. At rung 3 the model is yours, which is what ML engineering meant before the generative era.

34. Whether to train your own model is a live debate, and the balance shifts with each frontier release, each open model, and each new training recipe.
    - Against: 70% of production agents prompt off-the-shelf models; OpenAI closed self-serve fine-tuning to new users; prompt optimisation beats GRPO at 35x fewer rollouts [outline, verified].
    - For: Bridgewater's tuned Qwen3-235B at 84.66% against Claude Opus 4.8 at 78.2%, 13.8x cheaper to run; Harvey Tenet, +12.1 citation quality at a tenth of the cost [BV §2e, verified]. Tuning wins where the right answer is not public.

35. On complex document extraction, tuned 3B and 8B models beat the strongest model our deployment allowed.
    - 0.92 against 0.82 on transcription fields; 0.87 against 0.55 on the full field set [BV §2e, first-hand].
    - The capability was already there; tuning bought the output contract.

36. The answer depends on your data, your traffic and your budget, and my bet is that open models and the advantages of owning one are not going away.
    - Data: do you have examples or a verifier the frontier has never seen? Traffic: enough volume that a cheaper model pays back the training? Budget: can you afford to retrain as base models move?
    - **[YOU]** Confirm this directional bet is one you want to make in public.

37. The cost of getting a capability into a small model keeps falling, even though GPU prices rose in 2026 and frontier teams are spending more.
    - Falling: Together cut training prices 30–70% on Sep 11 2026; a 1.5B reasoning model was RL-trained for $9 (Tina); Ai2 built a 32B coding agent at 49.5–54.2% SWE-bench Verified for $2,000 (SERA); LoRA matches full fine-tuning for RL [PT §1, primary].
    - Rising: H100 contract prices up almost 40% from October 2025 to March 2026; Fireworks and Tinker raised prices; reasoning models cost 17x more to post-train than instruct models, with 82% of compute going to experiments that do not ship [PT §1, primary].
    - **FIGURE:** reuse fig2, relabelled "cost of tuning", with the Together price updated.

38. The training method follows from the signal you have: examples to imitate, preferences between answers, a stronger model to learn from, or an automatic check.
    - Supervision table, four rows [EM §2]. The paragraphs that follow take them in the order a recipe uses them: imitate, prefer, reinforce, then distil.

39. Supervised fine-tuning is cheap, needs surprisingly little data, and is the right tool for format and behaviour, but it memorises and can erase what the model already knew.
    - 50 good examples is OpenAI's starting recommendation; s1 fine-tuned a 32B model on 1,000 reasoning traces in 26 minutes on 16 H100s [PT §2, primary].
    - Training Qwen3-8B on internal documents cut its instruction-following score from 85% to 45% (Thinking Machines) [PT §2, primary]. SFT "memorizes" while RL generalizes (Chu et al., ICML 2025).

40. For agents, the examples are whole trajectories: a few thousand from a stronger model can lift a mid-size open model a long way, if they use the same tools and format as your agent.
    - How many: 491 trajectories gave up to 19 points on SWE-bench (SWE-Gym, 2024); about 5,000 reached 40.2% (SWE-smith, 2025); about 8,000 per repository let Ai2's SERA student match its teacher, for about $1,300 (2026) [PT, agentic SFT, primary, checked].
    - Format: SERA degrades "significantly" with "a different agent scaffold, or even subtle formatting differences"; NVIDIA trains across several harnesses for this reason [PT, agentic SFT, primary, checked].
    - Filtering: keeping only successful runs is not clearly better. NVIDIA found unfiltered data beat success-only, 12.4% to 5.06%; SERA found verification thresholds made no significant difference; masking the failed steps from the loss keeps the recovery behaviour [PT, agentic SFT, primary, checked].
    - What to screen out: the teacher's shortcuts (edited tests, git-history leaks) and anything overlapping your eval [PT, agentic SFT, primary].
    - Limits: nearly all evidence is coding and terminal work, and no public case yet builds multi-step agent training data from production logs [PT, agentic SFT].

41. Preference training learns from which of two answers is better, which is often easier to collect than a written-out answer, and it is fading from frontier recipes.
    - Tülu 3's pipeline: SFT 60.6, then DPO 64.7, then RL 65.1 average; OLMo 3 found DPO before RL beat either alone [PT §2, primary].
    - A reviewer choosing between two agent outputs produces exactly this data, so an escalation queue can feed it.
    - Nemotron 3 Ultra and MiMo-V2-Flash do not use it; on-policy distillation has taken its place [PT §2].

42. Reinforcement learning is for behaviour your examples never showed, and it needs an automatic check to learn from.
    - RL generalizes where SFT memorises, and RL keeps prior skills better at equal gains [PT §2, primary].
    - Its cost is mostly generating attempts: the rollout generator was 87% of OLMo 3's reasoning post-training energy [PT §1, primary]. It can also peak and collapse (see self-improvement).

43. If you train with RL, your environment, meaning the tasks plus the check that scores them, is the main lever you control, and the evals you built for your agent are most of one already.
    - This is the RL case. For SFT the equivalent lever is which trajectories you keep (above).
    - It decides which skills improve: DeepSeek found RL on code and search alone did not help agent tasks until it added 1,827 synthetic agent environments; NVIDIA found training on one environment caused "severe regressions" elsewhere [ENV §3, primary].
    - It decides which shortcuts get learned: Claude 3.7's habit of special-casing tests "emerged as a result of 'reward hacking' during reinforcement learning training" [ENV §3, primary].
    - Harvey builds its training environments in the same format as its public legal benchmark [ENV §5, primary]. The market prices good environments as scarce: Anthropic reportedly discussed spending over $1B on them in a year [ENV §1, secondary].
    - Two costs: a check built to measure must be hardened before a model optimises against it, and once you train on your eval you need a fresh one to know if you improved [ENV, verdict].
    - Limits: the base model sets the ceiling, and distillation can skip the reward entirely [ENV, verdict].

44. Training several agents together is a steady research area rather than a 2026 breakthrough, and the only piece in production trains one orchestrator while the agents it calls stay fixed.
    - Papers combining multi-agent and RL for language models held at about 5% of LLM RL papers (199 of 3,316 in 2025; 182 of 3,471 in 2026 to late September), while titles on on-policy distillation went from 10 to 271 [MA §9, own arXiv counts, reproduced].
    - The production case: Kimi K2.5 trains only the orchestrator; "sub-agents are frozen," which "circumvents two challenges of end-to-end co-optimization: credit assignment ambiguity and training instability" [MA §9, primary, checked]. Sakana's Fugu orchestrates frontier models in production [MA §9, primary].
    - Training several models jointly, self-play and debate training remain research. The 2026 reports for Kimi K3, DeepSeek V4, Nemotron 3 and GLM-5 describe RL specialists merged by distillation, not multi-agent RL. Mainstream RL tooling added multi-agent support only in July 2026 (prime-rl) [MA §9, primary].
    - What a company can use: RL-train a small orchestrator over fixed models and tools (NVIDIA's 8B ToolOrchestra scored 37.1% on HLE against GPT-5's 35.1% at 2.5x the efficiency); train your one agent inside your real harness, subagents included; or compile a fixed multi-step workflow into a small model with SFT, where an 8B model reached 87–98% of in-context frontier quality at 128–462x lower cost per conversation, for $50–80 of training (arXiv 2605.22502) [MA §9, primary, checked].
    - The last option is the same move as the document-extraction fine-tune earlier in this rung: put the procedure in the weights of a small model you own.

45. Distillation, training a small model on a stronger one, is the cheapest way to move a skill into a model you own, and the newest recipes use it to merge RL-trained specialists into one model.
    - Distilling beat running RL directly: 72.6 vs 47.0 on AIME for a 32B model (DeepSeek-R1). On-policy distillation, where the teacher grades the student's own attempts, matched RL at about a tenth of the GPU hours (Qwen3) [PT §2, primary].
    - Merging: train narrow specialists with RL, then distil them into one student. DeepSeek V4, Nemotron 3 Ultra (10+ teachers), MiMo-V2-Flash, Kimi K3 and GLM-5 do this; Nemotron 3 Ultra's merged model beat its own terminal-coding teacher, 54.0 vs 50.0. Papers with on-policy distillation in the title went from 10 in 2025 to 271 in 2026 by late September [PT §2, primary].
    - Anthropic's and Google's terms forbid using their models to train competing ones; Anthropic publicly named labs that ran 16M+ exchanges through fake accounts to do it [PT §2, primary]. Distil from open-weight teachers or a vendor's own distillation service.
    - For a client: three narrow tasks can become three small teachers and one student.
    - Merges the old distillation and specialist-merging paragraphs, placed after RL.

---

## Where this is heading: self-improvement

46. Self-improvement became something you could run on one GPU in March 2026, with Karpathy's autoresearch, and labs now say agents do real research work, though their leaders disagree about how fast to go.
    - Autoresearch: an agent edits a small model's training script in 5-minute runs and keeps what improves the loss; ~700 changes over two days, ~20 kept, cutting nanochat's time-to-GPT-2 by about 11%. His own caveat: "It's not novel, ground-breaking 'research' (yet)." And: "All LLM frontier labs will do this. It's the final boss battle." [EM §3.3c, primary]
    - Since then: OpenAI's "automated research intern" (Sept 2026) and its March 2028 target; Pachocki's call for slowdowns the same month; Jack Clark's 60% chance of autonomous self-improvement by 2028 (Aug 2026) [EM §3.1].
    - Research is itself run by teams of agents: Anthropic's automated alignment researchers are five Claude Opus 4.8 agents working in parallel for up to 48 hours, and the OpenAI evaluation behind the Hugging Face incident ran about 1,200 agents [EM §3.1, §1, primary].

47. The self-improvement that runs without a human today mostly rewrites a harness or a small model's training script, while changes to a frontier model's weights still have a human starting each run.
    - AIDE², Ouroboros, Darwin Gödel Machine, Recursive, autoresearch [EM §3.2, §3.3].
    - Weight-level work is larger in the literature (280 vs 95 papers in 2026), and labs now have models running parts of their successors' training, but "Claude is not operating fully autonomously for any measured subset of AI R&D work" [EM §3.3c]. Corrected from the earlier harness-only claim.

48. Today self-improvement is limited by its verifier: it improves what the check can measure, and where the check is narrow, it overfits to it.
    - Google's RRSI, on Harvey's legal benchmark: unregularised harness evolution scored best on the tasks it evolved against (93.0 vs a 89.4 baseline) and gained little or lost elsewhere, one method ending below baseline on APEX-Agents (31.7 vs 34.2); the regularised version gave up some of that score to gain on every other benchmark [EM §3.3b, primary].
    - Rise and collapse: RL self-training peaks then falls about 17 points [EM §3.3b].
    - Within a fixed search space, classical optimisers still beat LLM agents; a hybrid did best (Hutter et al., arXiv 2603.24647) [EM §3.3c, primary].
    - **FIGURE, maybe:** RRSI Table 1 as a small chart.

49. I have seen the same overfitting in prompt optimisation on document extraction: the gain was real but small, and the optimiser kept writing more specific instructions that encoded the quirks of the set it tuned on.
    - First-hand: GEPA-style optimisation of system prompts and instruction fragments; the over-specific prompts did worse on documents it had not seen [V, first-hand].
    - It is the same result as RRSI's, at a smaller scale: optimising a prompt or harness against one set is fitting a model, and it overfits like one.
    - **[REVIEW]** Proposed: the first-hand note becomes its own paragraph.

50. If you run a self-improvement loop, treat it as training: a fixed eval it cannot edit, a held-out set it never sees, a limit on how much it can change at once, and a person approving what ships.
    - Autoresearch makes its data and eval read-only, so the agent can only change the training code [EM §3.3c, primary].
    - RRSI's regularisation is a budget on how many edits a candidate can bundle, pressure toward unexplored approaches, and a critic plus a pruner that remove marginal or costly changes [EM §3.3b, primary].
    - LangChain, after its harness-only gain: "Changes that overfit to a task are bad for generalization and can lead to regressions in other Tasks," with a person reviewing proposed changes [BV §2g, primary, checked].
    - Keep the checks you monitor with separate from the checks you optimise against (Cotra) [SEC §1, primary].
    - **[REVIEW]** Proposed: a practical paragraph so the section ends on what a company can do now.

51. **Short coda.** For a company, the lasting asset is a good automatic check for its own work: domain-specific evals and RL environments that can say whether an attempt succeeded.
    - Define the term once: a verifier, grader or eval, meaning anything automated that scores an attempt.
    - That check is what lets an agent be improved, a model be trained, and a system improve itself. Without it, none of the three can go far.
    - The market agrees: Cognition calls environment quality "the most important factor for downstream model performance," and Mercor bought an environment builder saying "the constraint has shifted to the environments themselves" [ENV §2, §1, primary, self-interested].
    - The check has to look like the real work. Sutskever's warning: training on what the evals measure "could explain… this disconnect between eval performance and actual real-world performance" [ENV §2, primary].
---

## How to decide

52. Place your problem on a rung by what you own and what is failing.
    - Reviewing everything means the measurement layer is missing. Unexplained downstream rework means silent errors are unpriced. Dispersed saved hours mean the workflow was never redesigned [BV §2b].

53. Two numbers set the operating point at rung 2: what a silent error costs, and the coverage-versus-error curve on your own data.

54. Enter rung 3 when prompting has plateaued and you have a training signal; volume decides whether it pays, not whether it works.

---

## Close

55. The numbers in this post will date within a year, and the structure should not.

56. **[YOU]** End on the failures actually witnessed and what they share: someone skipped measurement and went straight to the machinery.
    - The prior draft's ending, trimmed [V].

---

## Reading notes

- **56 paragraphs** at 150 to 200 words each gives roughly 8,000 to 11,000 words.
- **Multi-agent, added this round:** vendor features as rung 1 (9); one agent or several, with cost against speed (18); coordination failure in the failure table (19); a second agent as checker (27); multi-agent RL in rung 3 (44); research run by teams of agents (46). Evidence in multiagent.md, including papers from your saved reading list (§8).
- **Earlier this round:** build paths (17); failure types decided as a table (19); self-improvement grown to six paragraphs (46 to 51), with your prompt-optimisation experience as its own paragraph (49).
- **Corrections found:** Spotify never used an AI reviewer; Uber's review figures are from 2025; "four in five wrong beliefs" added a category the paper counts as skill; MAST's 42% is v2; the Fable guidance is for Fable 5 and about skills; the small model's tool gain is points; Google's multi-agent study is 260 configurations in v3; on-policy distillation titles are now 271 in 2026; the old draft's 4 to 220x prefill figure is real but the 220x is one outlier.
- **First-hand passages:** rung 1 context setup (10), context (21), graders that are wrong (30), the extraction fine-tune (35), prompt optimisation overfitting (49). Rung 1's result is open; see the author todo.
- **Material left out on purpose:** most survey statistics, most RSI papers, the full case-study table, most security frameworks, the older silent-failure cases, most code-review studies, most multi-agent and MARL papers, the internal Research Swarm notes. It stays in the notes.
- **Proposed, please check:** build paths (17) and one agent or several (18); self-improvement at six paragraphs (46 to 51).
- **Decided:** title, How to Customize Agents, and When to Own Them.
- **Decisions to settle before drafting:** whether the old paragraph 9 comes back as its own paragraph (8); the open-models bet (36); the rung 2 close (31) and the new bridge to rung 3 (32); rung 1 result (15, optional).
- **Weakest evidence, say so in the prose:** over-escalation's cost to people is modelled, not measured (19, 28); no public study compares an in-house agent with a vendor agent on the same work (16); AI review's effect on production defects is unmeasured (12); most multi-agent cost and speed figures are vendor self-reports (18).
