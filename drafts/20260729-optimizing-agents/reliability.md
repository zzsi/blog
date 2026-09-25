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

**Microsoft, "Taxonomy of Failure Modes in Agentic AI Systems" v2.0, June 4 2026. [PRIMARY]** Seven new failure modes from a year of red-teaming deployed agents: agentic supply-chain compromise; goal hijacking; inter-agent trust escalation, where a compromised agent inflates its permissions to an orchestrator; visual attacks on computer-use agents; session context contamination, where early data biases later steps; MCP and plugin abuse, including tool-description poisoning; and capability or architecture disclosure. Plus the Hugging Face incident (emerging.md §1) as the out-of-scope extreme.

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

**Why it matters:** measurement is a practice, not a setup step. Every silent failure caught should become a regression test, which is the "train on your failures" rule one level down.
