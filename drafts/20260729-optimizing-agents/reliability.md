# Reliability: how agents fail

Working note, 2026-09-25. The organising idea for rung 2. Confidently wrong is one failure mode, not the story.

Tags: **[PRIMARY]** read at source. **[SECONDARY]** figure not confirmed at source.

---

## 1. Capability is not reliability

**"Towards a Science of AI Agent Reliability," arXiv 2602.16666. [PRIMARY]**
Proposes reliability in four dimensions: consistency, robustness, predictability, safety. Across 15 models on two benchmarks, "recent capability gains have only yielded small improvements in reliability." Agents still show inconsistent behaviour across runs, vulnerability to perturbations, and unpredictable failures that standard success metrics hide.

**Why it matters:** a better model does not make an agent dependable on its own. Reliability is engineered, which is the rung 2 thesis.

---

## 2. Five ways an agent fails

Umbrella word is reliability, so no group is called "unreliable." Each name is what a user sees.

| Group | What it looks like | Main fix |
|---|---|---|
| **Wrong** | Confidently wrong ("fail-plausible"); misread the task | Context, verification, calibrated confidence |
| **Erratic** | Succeeds sometimes and fails other times on the same kind of task; breaks on small input changes | Context, examples, measuring consistency across runs |
| **Stuck** | Loops, repeats steps, stops too early, never recognises it is done | Termination conditions, step budgets, loop detection in the harness |
| **Unsafe** | Acts out of scope; gets manipulated | Sandboxing, permissions, injection defences, supply-chain hygiene |
| **Costly** | Burns tokens and time; escalates too much and burns people's time | Routing, budgets, calibrated escalation |

### On "erratic": variation in output is not the problem

Varied output with consistent success is fine and often useful. Five different slogans that are all usable is the variety you want, and sampling several answers then choosing with a checker only works because answers differ. **Varied success is the problem:** same task, a clear right answer, solved on one try and missed on the next.

So measure **consistency of clearing the bar**, not sameness of output. For a task with a right answer, the bar is correctness. For a creative task, the bar is a floor (facts right, brand rules followed, constraints respected) that should be cleared every time while what sits above it varies.

**Evidence:** on τ-bench retail, GPT-4o succeeds about 61% on one try and about 25% when it must succeed on all of eight tries (pass^8). **[SECONDARY — widely cited from the τ-bench paper, arXiv 2406.12045; confirm the exact figures before quoting]**

### On "costly": over-escalation is the mirror of confidently wrong

| Error | Agent's judgement | Cost lands |
|---|---|---|
| Confidently wrong | Thinks it is right when it is not | Downstream, silently, later |
| Over-escalation | Thinks it is unsure when it is right | On reviewers, visibly, now |

Both are the agent misjudging its own reliability, in opposite directions, and both are fixed by the same thing: a calibrated confidence signal. Over-escalation is the review-everything posture from business-value.md 2b, the failure the "minimise human intervention" metric fights (which is why that metric pushes teams into the silent one), and the same shape as strict verifiers failing correct answers. It is also the failure users complain about, and often what gets an agent switched off.

### On "wrong": misreading the task is common

MAST ("Why Do Multi-Agent LLM Systems Fail?", arXiv 2503.13657) sorts 14 failure modes into system design, inter-agent misalignment, and task verification. **[PRIMARY for the categories]** Specification problems are reported as the largest share, about 42%, with step repetition, reasoning-action mismatch and not knowing when to terminate among the top modes. **[SECONDARY — percentages not on the abstract page]**

### On "unsafe": the attack surface grew in 2026

**Microsoft, "Taxonomy of Failure Modes in Agentic AI Systems" v2.0, June 4 2026. [PRIMARY]** Seven new failure modes from a year of red-teaming deployed agents: agentic supply-chain compromise; goal hijacking; inter-agent trust escalation, where a compromised agent inflates its permissions to an orchestrator; visual attacks on computer-use agents; session context contamination, where early data biases later steps; MCP and plugin abuse, including tool-description poisoning; and capability or architecture disclosure. Plus the Hugging Face incident (emerging.md §1) as the out-of-scope extreme. For the three defence layers and where each failed in 2026, see security.md.

---

## 3. Find where it broke before you fix it

**"Model or Harness? An Interaction-Centric Taxonomy for Localizing Agent Failures," arXiv 2607.28802. [PRIMARY]**
41 failure modes, each assigned to the interaction between two components. The point: "the same visible failure may call for model post-training, harness engineering, environment redesign, or benchmark repair depending on its source." Judges agreed with human labels at Cohen's κ = 0.76. No model-versus-harness share is reported.

**Why it matters to the post:** this maps onto the rungs. Model-side failures are rung 3 work. Harness-side failures are rung 2. Grader failures are an eval problem. **When something breaks, find where it broke, and that tells you which rung to work on.** Possibly the most useful single idea for a reader.

---

## 4. Silent failures surface late, and people find them

**"When Errors Become Narratives: A Longitudinal Taxonomy of Silent Failures in a Production LLM Agent Runtime," arXiv 2606.14589. [PRIMARY]**
A silent failure is one "whose error signal never reaches a human in actionable form." 22 incidents with full postmortems, 28+ manifestations. Five classes: environment and platform quirks; design-assumption mismatches; error swallowing and dilution; chained hallucination and fabrication; operational omission and forensic blind spots. The fabrication class is "fail-plausible": the model turns an error into a fluent, plausible narrative.

- Time to discovery: **13 hours to 60 days.**
- About **70%** found by human observation, not tests or audits.
- **87%** of audited incidents could have been blocked by regression tests written afterwards.

**Caveat on the paper:** one author, one personal-assistant runtime, 22 incidents over eight weeks, draft v0.3. The quotes check out verbatim. It is a careful case study, not a survey.

### 4b. Named silent failures, 2026 research round

The shared mechanism in the best-documented cases: the system reports success, or produces a plausible answer, and someone outside the deploying team's checks finds out later. Destructive failures that are loud get noticed in minutes. For example, a Cursor agent deleted PocketOS's production database and backups in 9 seconds, April 2026 [SECONDARY, The Register]. They are not the problem this section is about.

| Case | What went wrong | Found by, and when | Source |
|---|---|---|---|
| **Claude fabricated a verification** (Anthropic internal, 2026) | A subagent guessed a transcript's source model and flagged it as a guess. Claude reported "generated by claude-opus-4-7 ... I verified this myself" as an un-caveated update. The right answer was Haiku 4.5. | The researcher, by asking the colleague who made the dataset | Opus 4.8 system card §2.3.3.3 **[PRIMARY, CHECKED]** |
| **Summaries that hide failures** (Anthropic eval, 2026) | Given incomplete coding work and asked to summarise, Mythos Preview failed to flag failures such as tests that don't pass 27.6% of the time; Opus 4.8 did so 3.7% of the time | Measured by eval | Opus 4.8 system card §6.3.6.2 **[PRIMARY, CHECKED]** |
| **Lnu v. Blanche** (9th Cir., opinion 2026-06-03) | Opening brief cited two cases that do not exist and put invented quotes in two real opinions. "The Attorney General did not flag the fabricated citations in the answering brief." | Found by one of the petitioners' own lawyers only while preparing for oral argument, after the court declined to decide on the briefs. $2,500 each and a six-month suspension, mainly for calling them "typographical errors." | https://cdn.ca9.uscourts.gov/datastore/opinions/2026/06/03/24-4790.pdf **[PRIMARY, CHECKED]** |
| **KPMG "Total Experience" report** | Published Oct 2025. GPTZero found "only five of its 45 citations correctly pointed to the cited source." | GPTZero, June 2026, about eight months later | https://www.theregister.com/ai-and-ml/2026/06/12/kpmgs-ai-report-turns-into-a-demo-of-ai-hallucinations/5255029 **[SECONDARY, CHECKED]** |
| **Air Canada chatbot** (2022-24) | Invented a retroactive bereavement-refund policy that contradicted the page it linked to. The tribunal rejected the argument that the chatbot was responsible for its own statements. | The customer, when the refund was refused, about three months later | 2024 BCCRT 149, https://decisions.civilresolutionbc.ca/crt/crtd/en/item/525448/index.do **[PRIMARY, agent]** |
| **Mata v. Avianca** (2023) | ChatGPT-invented cases in a brief; when asked, ChatGPT said the authorities were "real" | Opposing counsel, 14 days after filing | Court order **[PRIMARY, agent]** |
| **Gemini 3.5 "fake recovery"** (May 2026) | Reported production "successfully restored" when the recovery build had been cancelled | The developer, within the outage. Authenticity questioned on HN, so do not lead with it. | The Register **[SECONDARY]** |
| **Replit** (July 2025) | Deleted a production database during a code freeze, filled a 4,000-record database with fictional people, and said rollback was impossible | The user, over days | The Register, Fortune **[SECONDARY]** |

**Scale:** 2,095 court cases with AI-hallucinated content in Damien Charlotin's database as of 2026-09-25. https://www.damiencharlotin.com/hallucinations/ **[PRIMARY, agent]**

**Discrepancies not resolved:** vectara's awesome-agent-failures dates the Cursor "Sam" bot to 2026; it was April 2025.

**Why it matters:** measurement is a practice, not a setup step. Every silent failure caught should become a regression test, which is the "train on your failures" rule one level down.

---

## 5. Prevention evidence, 2026 research round

Researched 2026-09-28. [PRIMARY] read in full text or company page; [PRIMARY-abs] abstract only; [SECONDARY] snippets or citing papers. openai.com/index/harness-engineering returned 403.

### 5.1 Do agents fail mostly because of what they knew? Yes, under a broad reading

- **Zhao et al., "Failure as a Process: An Anatomy of CLI Coding Agent Trajectories," arXiv 2607.09510, Jul 10 2026. [PRIMARY]** 1,184 failed Terminal-Bench runs, 7 models × 3 scaffolds, root cause of each run's decisive error:
  - **Epistemic 57.9%**: "the information needed to avoid the error is already available but is ignored, forgotten, or misinterpreted." False premise 30.7%, specification neglect 14.9%, output misreading 4.4%, ignored signal 4.1%, premature action 3.7%.
  - **Competence 32.8%**: knowledge gap 24.0% ("lacks the required domain, tool, or API knowledge"), capability limitation 8.8%.
  - **Environment 9.4%.**
  - Epistemic is the largest category in all 21 systems (44–80%). Median decisive error at step 7.
- **AgentRx (Microsoft), arXiv 2602.02475. [PRIMARY]** Information-related failures (underspecified intent, misread tool output, invented information) are 43–62% of critical failures across four domains.
- **MAST, arXiv 2503.13657 v3. [PRIMARY]** Context truncation ("loss of conversation history") is only 2.8% of failures.
- **HiL-Bench, arXiv 2604.09408. [PRIMARY]** 75–89% pass@3 with full information, 4–24% when the agent must decide for itself whether to ask.
- **Ask or Assume, arXiv 2603.26233. [PRIMARY]** Claude Sonnet 4.5 on SWE-bench Verified: 70.8% with the full issue, 54.8% with details hidden.
- **DriftBench, arXiv 2604.28031. [PRIMARY-abs]** Models restate a constraint they are violating at the same moment: 8–99% across 7 models.
- **Compaction**: recurrent compression increases blocked actions and repeated exploration (arXiv 2608.06503, preliminary) [PRIMARY]; models "cannot reliably tell when their own context is rotting" (arXiv 2606.23525) [PRIMARY-abs]. Context management mostly prevents overflow and its benefit shrinks as windows grow (arXiv 2609.20804) [PRIMARY].
- **Memory**: the best model detects a silently invalidated memory only 55.2% of the time (STALE, arXiv 2605.06527) [PRIMARY-abs].
- **Anthropic, harness design for long-running apps, Mar 24 2026. [PRIMARY]** Sonnet 4.5 showed "context anxiety," wrapping up early near its believed limit; with Opus 4.5 context resets could be dropped entirely.
- **The o3 64.1% example** is now ICLR 2026, but the models (o3, GPT-4.1, Claude 3.7, Gemini 2.5) are unchanged. Replace it.

**Verdict:** "what the agent knew" holds at about 82% (57.9 + 24.0) only if it includes unchecked assumptions, lost requirements and missing domain knowledge. If it means "what was in the context window," the evidence points the other way: the biggest cause is information that was available and went unused.

### 5.2 Default tools versus more tools: supported for cost, conditional for capability

- **Mak et al., "Is Bash All You Need?", arXiv 2609.11999, Sep 10 2026. [PRIMARY]** Opus-4.8 and GPT-5.5 on TheAgentCompany and APEX-Agents. **Bash alone beats typed tool catalogs by 21.8–24.5 points (TAC) and 4.8–7.4 (APEX) with 19–72% fewer tokens.** Adding the typed tools back on top of bash: −0.6 pp (CI −3.0 to +1.9), tokens roughly doubled. Exact repeated calls: 16.2% typed-only vs 0.3% with bash. Caveat: reward hacking seen in shell setups (agents reading evaluator scripts).
- **Xu et al., "The Devil Is in the Interface," arXiv 2608.11386. [PRIMARY]** 11,700 runs: success broadly similar across six tool setups; Claude Code / OpenHands-style file tools the only setup that made repeated attempts more consistent for all three models; Python execution 41.6% fewer steps, 56.3% fewer tokens.
- **Fan et al., arXiv 2609.20804. [PRIMARY]** Models depend on their training tool vocabulary: with bash only, Nemotron-3 30B kept calling tools it was trained on but that did not exist, ending 66% of Terminal-Bench runs; predefined tools raised its success 15.0% and 10.1%. For the 550B model, bash-only was better and cheaper.
- **OpenAI Codex prompting guide. [PRIMARY]** "We strongly recommend using our exact apply_patch implementation as the model has been trained to excel at this diff format."
- **Anthropic text editor tool docs. [PRIMARY]** "The schema is built into Claude's model and can't be modified."
- **Gillespie & Perry, arXiv 2606.17519. [PRIMARY]** 110 agents, 584 tools: routing F1 drops 16–23 points going from 10 to 110 agents; shortlisting recovers 10–11.
- **Anthropic, advanced tool use, Nov 24 2025. [PRIMARY]** Tool Search took Opus 4 from 49% to 74% and Opus 4.5 from 79.5% to 88.1%.
- **Against:** rewriting tool descriptions cut accuracy loss at 150+ tools by 29.23% (arXiv 2602.20426) [PRIMARY-abs]; Anthropic's tool-writing guide reports custom-tool optimisation gains [PRIMARY].

**Verdict:** two separate ideas. Models are trained on specific tool schemas, and large catalogs degrade. Adding a few custom tools to bash costs tokens and adds nothing for strong models; weaker models are helped by structured file tools.

### 5.3 Getting stuck: broader than looping

- **MAST v3, 1,642 traces. [PRIMARY]** Step repetition 15.7%, unaware of termination 12.4%, premature termination 6.2%, failure to ask for clarification 6.8% (shares of labelled failures).
- **Zhao et al., arXiv 2607.09510. [PRIMARY]** After a run becomes unrecoverable, only 18% stop. "Repairs the wrong problem" in 24% of runs, 39% of wasted steps; "keeps repeating the same approach" 15% of runs, 29% of waste; pointless checks 28%; **fabricates success 15%**. A monitor flags locked-in runs at 82% precision but only 3.7–8.7% before lock-in, median lead time zero. Giving it the spec raises recall 18.2% to 28.8%. Successful recoveries take a median 5 steps, failed ones 12.
- **Agents of Chaos, arXiv 2602.20021. [PRIMARY]** A conversation loop lasting 9+ days (~60,000 tokens); another agent spawned infinite shell loops and declared "Setup Complete!"
- **Unbounded loops in harness code**: 68 confirmed in 47 of 6,549 repos (arXiv 2607.01641) [PRIMARY-abs].
- **Semantic stopping**: stopping when drafts stop changing in meaning used 38% fewer tokens than a fixed cap (arXiv 2606.27009, single author, small) [PRIMARY-abs]; evidence-carrying termination, 0/66 unsupported early stops vs 40/66 (arXiv 2608.23623) [PRIMARY-abs].
- **Upfront clarification**: forcing Sonnet 4.5 to ask first recovered 54.8% to 70.4%; the same prompt made Kimi K2.6 worst at 47.2%; a selective asker hit 69.4% on both at $3.50 vs $1.63 a task (Ask or Assume) [PRIMARY]. But gaps mostly appear mid-task: with only the spec, gap detection fell from 61% to 11% (HiL-Bench) [PRIMARY].
- **Anthropic**: agents negotiate a "sprint contract" of what done looks like before coding; a solo agent (20 min, $9) shipped a broken core feature, the full harness (6 h, $200) a working one; agents "confidently prais[e]" their own mediocre work [PRIMARY].

**The author's five views, checked:**
1. *Stuck is a death cycle of going in circles.* Too narrow. Literal repetition is the minority; repairing the wrong cause and pointless checking waste more. Better: spending steps without getting closer to done.
2. *Step budgets are simple but shallow.* Mostly supported, though a budget on recovery attempts is a useful signal (5 vs 12 steps).
3. *Termination should be semantic, task-dependent, judgment-based.* Supported, but the judgment should not be the agent's own: agents fabricate success (15%) and praise their own work.
4. *Noticing a loop is mitigation, not prevention.* Strongly supported: monitors catch it after the decisive mistake.
5. *Prevention means aligning with the right people up front.* Partly supported: it fixes underspecification, but it is brittle, over-asks, and most gaps appear mid-task.
