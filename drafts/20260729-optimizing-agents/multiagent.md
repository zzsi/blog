# One agent or several: when multi-agent helps, and what it costs

Research round, 2026-09-29. **[PRIMARY]** = I read the source itself. **[checked]** = I matched the quote against a saved copy of the source. **VENDOR** = the company is reporting on its own product. Web search was capped in this round, so sources were found through arXiv, OpenAlex, Semantic Scholar and known URLs.

## Verdict

With compute held equal, several agents pay off mainly in two cases:
- the parts of the work don't need each other's context (parallel search, separate modules, black-box checks);
- one agent can't already do the task well.

They hurt on sequential work.

A second agent is worth it as a checker when it can test against something outside the writer, or when it is at least as capable as the writer. Running it on a different model does not by itself make it independent.

Otherwise one agent is cheaper and fails in fewer ways.

## 1. When it helps and when it hurts

**Google Research, "Towards a Science of Scaling Agent Systems"** (Kim et al., arXiv 2512.08296; v1 Dec 9 2025, v3 Apr 8 2026) **[PRIMARY, checked v3]**
- **Compute matched:** "All systems matched for total reasoning tokens."
- **Wide range:** Finance Agent, centralized, "+80.8% (mean 0.631 vs. SAS 0.349)". PlanCraft degrades under every multi-agent variant, down to "MAS-Independent (-70.0%)". Overall mean "-0.3 %".
- **Ceiling:** "tasks where single-agent performance already exceeds 45% accuracy experience negative returns from additional agents" (p=0.004).
- **Sequential work:** "sequential interdependence, rather than complexity alone, determines coordination viability."
- **Agent count:** Gemini-2.0 Flash peaks at 7 agents, and communication overhead "grows superlinearly with agent count." They tested up to 9 agents.
- **Error amplification:** 17.2× for independent agents vs 4.4× for centralized. In v3 this is not statistically significant after controls.
- **Mixing models:** "no evidence that model mixing bypasses the capability-saturation threshold."
- **Version note:** v1 and the blog say 180 configurations and +80.9%; v3 says 260. Cite v3.

**Anthropic, "Building multi-agent systems: when and how to use them"** (Jan 23 2026) **[PRIMARY, checked, VENDOR]**
- Multi-agent helps in three situations: "when context pollution degrades performance, when tasks can run in parallel, and when specialization improves tool selection or task focus. Outside these situations, the coordination costs typically exceed the benefits."
- "multi-agent implementations typically use 3-10x more tokens than single-agent approaches for equivalent tasks."
- "teams invest months building elaborate multi-agent architectures only to discover that improved prompting on a single agent achieved equivalent results."
- "Work should only be split when context can be truly isolated."
- Apr 10 2026 follow-up: "For most use cases, we recommend starting with orchestrator-subagent."

**Anthropic multi-agent research system** (Jun 2025) **[PRIMARY, VENDOR]**
- Multi-agent beat single-agent Opus 4 by 90.2% on breadth-first research.
- "token usage by itself explains 80% of the variance."
- Not a good fit for tasks "that require all agents to share the same context"; "most coding tasks involve fewer truly parallelizable tasks than research."

**Cognition** **[PRIMARY, checked, VENDOR]**
- "Don't Build Multi-Agents" (Jun 2025): "just use a single-threaded linear agent."
- "Multi-Agents: What's Actually Working" (Apr 22 2026) narrows that view. The 2025 argument still holds "for parallel-writer swarms", but they now use "setups where multiple agents contribute intelligence to a task while writes stay single-threaded."
- On unstructured swarms: "mostly a distraction. The practical shape is map-reduce-and-manage." The big demos "all share… a simple, verifiable success criterion."

**Comparisons at the same budget**
- Tran & Kiela (arXiv 2604.02460, Apr 2026): single agents "consistently match or outperform" multi-agent on multi-hop reasoning when reasoning tokens are held constant. **[PRIMARY]**
- Debate: "Majority Voting alone accounts for most of the performance gains typically attributed to MAD" (arXiv 2508.17536). **[PRIMARY]**

## 2. Failure modes

- **MAST v3** (Oct 2025): 1,642 traces from GPT-4-era frameworks. System Design 44.2%, **Inter-Agent Misalignment 32.3%**, Task Verification 23.5%. These are shares of observed failures, not of runs. The largest inter-agent mode, reasoning-action mismatch (13.2%), also happens in single agents. **[PRIMARY]**
- **Anthropic Frontier Red Team, "Patterns and problems in emerging multiagent systems"** (Aug 13 2026) **[PRIMARY, checked, VENDOR research]**
  - Agents make the same mistakes together: "when one agent makes a bad decision, it is likely that many agents will make that same bad decision."
  - "18 out of 30 agents decided to create a git branch with the exact same branch name."
  - A job-queue test saw "2.4 million job requests and only 117 jobs accepted."
- **Errors correlate across models.**
  - Four GPT-4o instances "agree on the same wrong answer 56% of the time… versus 0.4% predicted under independence," and "family diversification does not reduce correlated hallucination" (Rai & Madisetti, ACM AI Letters, Sep 2026, abstract only).
  - "larger and more accurate models have highly correlated errors, even with distinct architectures and providers" (arXiv 2506.07962, 2025).
- **Error compounding is not automatic.** In 3-agent chains, hallucination fell from 0.422 at the first agent to 0.272 at the last (arXiv 2606.07937).
- **The "five chained agents at 95% give 77%" line** is arithmetic (0.95^5), not a measurement. It applies equally to one agent doing five steps, so present it as an illustration.

## 3. A second agent as checker

- **Shopify Dispatch** (Jul 29 2026): "Uses a different model than the Hunting agent. Adversarial review reduces noise and prevents blind spots." Why they need it: "In one audit, a model uncovered more than 30 candidate vulnerabilities. After validation, every one was downgraded… found to be a false positive, or reclassified." The verifier also writes and runs tests. **[PRIMARY, checked, VENDOR]**
- **Cross-model review** (arXiv 2607.21656, Jul 2026, workshop paper; 116 tasks; reviewer cannot execute tests) **[PRIMARY, checked]**
  - Claude reviewing Codex drafts raised the pass rate from 71.6% to 89.7%. Codex reviewing Claude drafts lowered it from 91.4% to 82.8%.
  - Codex reviewing its own drafts also helped (84.5%).
  - "the reviewer's contribution is bounded by its relative capability rather than guaranteed by simply adding a second pass."
- **Self-review** (arXiv 2605.21537): "31.7% are silently endorsed by the same model that produced them (83/262)." Recommendation: "an explicit behavioural oracle is required." **[PRIMARY]**
- **Anthropic** (Mar 2026): "tuning a standalone evaluator to be skeptical turns out to be far more tractable than making a generator critical of its own work"; "Out of the box, Claude is a poor QA agent." And Apr 2026: a verifier with no criteria "will rubber-stamp the generator's output." **[PRIMARY, VENDOR]**
- **Cognition Devin Review** (same model, clean context): "catches an average of 2 bugs per PR, of which roughly 58% are severe." **[VENDOR]**

## 4. Vendor features (rung 1)

- **Claude Code**
  - Custom subagents (Jul 2025). Docs: use them when "The work is self-contained and can return a summary."
  - Agent teams: research preview, Feb 5 2026, "token-intensive." Docs: "For sequential tasks, same-file edits, or work with many dependencies, a single session or subagents are more effective." And: "Start with 3-5 teammates."
  - Costs page: "Agent teams use approximately 7x more tokens than standard sessions when teammates run in plan mode." Agent-teams page: "Token costs scale linearly" and "beyond a certain point, additional teammates don't speed up work proportionally." **[checked, living docs accessed Sep 29 2026]**
- **OpenAI Codex**
  - Cloud tasks run "many tasks in parallel" (May 2025).
  - Subagent docs: "consume more tokens than comparable single-agent runs"; "use parallel agents for read-heavy tasks… Be more careful with parallel write-heavy workflows."
- **Cursor** **[checked]**
  - 2.0 (Oct 2025): up to eight agents in parallel.
  - Subagents (Jan 2026).
  - Docs: "Running five subagents in parallel uses roughly five times the tokens of a single agent." And: "The benefit is context isolation, not speed."

## 5. Large 2026 runs

- **Anthropic C compiler** (Carlini, Feb 5 2026) **[PRIMARY, VENDOR]**
  - Scale: 16 agents, nearly 2,000 sessions, $20,000, a 100,000-line compiler.
  - Flat peers with lock files; "I don't use an orchestration agent."
  - "the task verifier is nearly perfect, otherwise Claude will solve the wrong problem."
  - On the Linux kernel: "Every agent would hit the same bug, fix that bug, and then overwrite each other's changes." GCC used as an oracle fixed it.
- **Cursor, hundreds of agents** (Jan 14 and Feb 5 2026) **[PRIMARY, checked, VENDOR]**
  - Flat peers failed: "Twenty agents would slow down to the effective throughput of two or three." And: "With no hierarchy, agents became risk-averse."
  - Planner, worker and judge roles fixed most of it. The final design used recursive planners and peaked at "~1,000 commits per hour across 10M tool calls."
  - Critics found early commits didn't compile.
  - Jul 2026 follow-up: conflicts fell from 70,000+ to under 1,000. No single-agent comparison was made.
- **Kimi K2.5 Agent Swarm** (arXiv 2602.02276) **[PRIMARY, checked, VENDOR]**
  - A trained orchestrator creates frozen sub-agents.
  - Training failure modes: "serial collapse" and "spurious parallelism, a reward-hacking behavior."
  - BrowseComp: 78.4% vs 60.6% for the single agent. But the paper also reports the single agent at "74.9% with Discard-all context management", so the gain over a well-engineered single agent is **3.5 points**.
  - Execution time 3 to 4.5× faster.

## 6. The four-condition test, re-checked

| Old condition | Verdict | Revised |
|---|---|---|
| Splits into semi-independent parts | Strongly supported | The parts don't need each other's context |
| Synthesis adds value beyond overhead | Weak: the gains come from breadth, context isolation and tokens | Merge into the last condition |
| Single agent optimised and plateaued | "Optimised" holds; "plateaued" is risky, because above ~45% extra agents hurt | The single agent hits a limit that several agents address: context overflow, breadth, too many tools, lenient self-grading |
| Gain exceeds full coordination cost | Supported | Measured on the same token budget |
| *(missing)* | | Writes stay with one agent, or in separate files |
| *(missing)* | | A checker needs something external to test against, or must be at least as capable as the writer |

**Watch:** stronger models shrink the case for extra agents (Google's 45% ceiling; Anthropic dropped its evaluator on Opus 4.6 for tasks within the model's reach). Kimi's trained orchestrator suggests the balance could shift again.

## 7. Token cost against speed and output (research round 2026-09-29)

**Verdict:** the author's hunch holds. Token spend rises at least in proportion to the number of agents, and often faster, because each agent re-reads shared context and coordination adds turns. Wall-clock speedup and useful output grow more slowly.
- **Breadth-first search:** about 2x the speed for 4 agents (OpenAI); Kimi reports 3 to 4.5x.
- **Tightly coupled coding:** returns flatten or turn negative.
- **No public study** measures dollars against useful merged output for parallel coding agents.

**Speed against cost**
- **Noam Brown (OpenAI), Dwarkesh podcast, Sep 17 2026** **[PRIMARY transcript, checked, VENDOR]**
  - "if you have four agents working on the problem, it is done twice as fast. Because there are four agents working for half as long, you're paying 2x more to get an answer twice as quick."
  - Asked whether the speedup is sublinear: "It's slightly sublinear, though it does depend a lot on the problem. Math, for example, is quite parallelizable."
- **OpenAI GPT-5.6 "ultra"** (Jul 2026) runs "four agents in parallel by default, trading higher token use for stronger results and faster time-to-result." Single agent vs Ultra: Terminal-Bench 2.1 88.8% → 91.9%, BrowseComp 90.4% → 92.2%. Token multiples appear only in charts. **[PRIMARY via Wayback, VENDOR]**
- **Kimi K2.5** (arXiv 2602.02276): the swarm "reduces the execution time required to reach target performance by 3× ∼ 4.5×" on WideSearch. **No token cost is reported.** It measures critical steps, not total work. **[PRIMARY, checked, VENDOR]**
- **Anthropic research system** (2025): 3–5 subagents in parallel "cut research time by up to 90% for complex queries." "~15x" is against chat, not against a single agent (agents use about 4x chat). **[PRIMARY, VENDOR]**
- **CAID** (arXiv 2603.21489, Commit0-Lite, Sonnet 4.5): 4 agents scored 59.1 vs 53.1 for one, took 1583 s vs 693 s, and cost 8.1 vs 1.9. Performance fell at 8 agents. **[PRIMARY]**

**Output against number of agents**
- **CooperBench** (arXiv 2601.13295): "performance drops from 68.6% with 2 agents to 46.5% with 3 agents and further to 30.0% with 4 agents." **[PRIMARY, checked]**
- **Google** (2512.08296 v3): "SAS achieves 67.7 successes/1K tokens; Centralized drops to 21.5 (3.1× worse)… Hybrid to 13.6 (5.0× worse)." Multi-agent needs "1.6–6.2× token budgets relative to single-agent at matched performance." Turns grow as "T = 2.72 × (n + 0.5)^1.724." **[PRIMARY, checked]**
- **Claude Code docs:** "Token costs scale linearly"; "additional teammates don't speed up work proportionally"; agent teams use about 7x the tokens. **[PRIMARY, checked, VENDOR]**
- **Cursor** (Feb 2026): "Could we spend 10x more on compute to get 10x more meaningful throughput?" Flat coordination: "20 agents would slow to the throughput of 1-3." Their "linear scaling of token throughput" is linear in tokens, not in verified output. **[PRIMARY, checked, VENDOR]**
- **Cursor, "Agent swarms and the new model economics"** (Jul 20 2026) **[PRIMARY, checked, VENDOR]**
  - Similar quality at costs "from $1,339 for the Opus 4.8 hybrid to $10,565 for GPT-5.5 alone."
  - The old harness made 68,000 commits in two hours and 70,000+ conflicts.
  - Their conclusion: swarms scale through "context efficiency, more than… parallelism itself."
- **Anthropic C compiler** (Feb 2026): "2 billion input tokens and generated 140 million output tokens, a total cost just under $20,000." "Having 16 agents running didn't help because each was stuck solving the same task" on the kernel. Chris Lattner: "a competent textbook implementation." **[PRIMARY, checked, VENDOR]**
- **Practitioners**
  - Boris Cherny (Lenny's, Feb 2026): "at the moment I have, like, five agents running."
  - Yegge (Gas Town, Jan 2026): "20–30 at once, productively," but "typically I'll only have a dozen or so active," and "Do not use Gas Town if you care about money."
  - **[PRIMARY, VENDOR/practitioner]**
- **Company level:** DX, AI usage +65% but PR throughput +7.76%. OpenAI: "our bottleneck became human QA capacity" **[checked]**.

**Where the ceiling comes from, strongest evidence first**
1. **The serial part of the task:** C-compiler kernel stall, Google's −39 to −70% on sequential planning, Cursor's "slowest worker."
2. **Coordination overhead:** Cursor's lock contention, Google's turn exponent, the CooperBench decline.
3. **Merge conflicts and duplicated work.**
4. **Human review and QA capacity.**
5. **Duplicated context.** Gao et al. (arXiv 2505.18286, 2025): "MAS consumes 4–220× more input (prefill) tokens than its SAS counterpart." That is the old draft's source, found. The 220× is one outlier (AIME math debate), on academic frameworks with Gemini-2.0-Flash. **Quote as 4x to over 200x at most, or not at all.**

**Counter-evidence:** some gains are large (Anthropic +90.2%, Google +80.8% on finance), so "sublinear per token" does not mean "not worth it." Pairing a frontier planner with cheap workers cuts dollars sharply at similar quality (Cursor). Stronger models shrink the advantage.
