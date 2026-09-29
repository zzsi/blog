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
  - The "7x tokens" figure was not found in saved copies. Do not use it.
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
