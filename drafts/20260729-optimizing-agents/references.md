# References — "How to Optimize Agents for Practical Work (Mid-2026)"

Compiled from the three research rounds behind the deck and blog post. Organized by round, then by topic. Where a source was directly retrieved and cited in the research output, its URL is included. Where the report referenced a named study, survey, or paper that came up during research but whose exact URL wasn't captured in the citation record, it's listed separately under "Named sources without a captured link" at the end of each round — these are real, identifiable sources (organization + report title), but you'll want to search for the current link before citing them externally.

---

## Round 1 — The Full-Stack Playbook (evals → context → tools → cost → fine-tuning)

1. **"System Card: Claude Opus 4.5"** — Anthropic, November 2025. https://www.anthropic.com/claude-opus-4-5-system-card
2. **"AI Agent Observability 2026: Tracing & Monitoring Stack"** — Digital Applied Team. https://www.digitalapplied.com/blog/ai-agent-observability-2026-tracing-monitoring-stack-guide
3. **"Agent Observability 2026: Evals, Traces, Cost Guide"** — Digital Applied Team. https://www.digitalapplied.com/blog/agent-observability-2026-evals-traces-cost-guide
4. **"Agentic Workflow Anti-Patterns: Orchestration Mistakes"** — Digital Applied Team, 2026. https://www.digitalapplied.com/blog/agentic-workflow-anti-patterns-orchestration-mistakes-2026
5. **"Fine-Tuning LLMs in 2026: When RAG Isn't Enough (and When It Still Is)"** — BigData Boutique. https://bigdataboutique.com/blog/fine-tuning-llms-when-rag-isnt-enough
6. **"Updating the taxonomy of failure modes in agentic AI systems: What a year of red teaming taught us"** — Microsoft Security Blog, June 4, 2026. https://www.microsoft.com/en-us/security/blog/2026/06/04/updating-taxonomy-failure-modes-agentic-ai-systems-year-red-teaming-taught-us/
7. **"When Fine-Tuning Beats Prompting"** — *WTF In Tech* (Substack), Bhavishya Pandit. https://bhavishyapandit9.substack.com/p/when-fine-tuning-beats-prompting
8. **"AI Model Fine-Tuning Cost Calculator"** — CalcWolf. https://calcwolf.com/ai-fine-tuning-cost-calculator/
9. **"How to Fine-Tune LLMs in 2026: Costs, GPUs, and Code"** — Spheron. https://www.spheron.network/blog/how-to-fine-tune-llm-2026/
10. **"Cost of Fine-Tuning LLM: 2026 Pricing & Budget Guide"** — aisuperior. https://aisuperior.com/cost-of-fine-tuning-llm/
11. **"Rethinking On-Policy Distillation"** — arXiv 2604.13016, April 2026. https://arxiv.org/abs/2604.13016 — CAUTION: this is a real, on-topic paper but it makes **no compute-cost or GPU-hour claim**, and it questions whether the method scales to long-horizon distillation. Do not cite it as replicating the one-tenth GPU-hours figure. The draft did so and the claim has been withdrawn.

### Named sources without a captured link (Round 1)

- Anthropic engineering blog, **"Writing effective evals for AI agents"**-type guidance (evals-as-highest-bandwidth-channel framing)
- Anthropic, **"Effective context engineering for AI agents"** (Sept 2025) — introduced context-editing/memory-tool primitives
- Anthropic, **"Code execution with MCP"** — Adam Jones & Conor Kelly, Nov 2025 (the 150,000→2,000 token / 98.7% reduction case study)
- Cloudflare engineering blog — "Code Mode" (TypeScript code-execution pattern for MCP)
- LangChain, **"State of AI Agents"** survey report, 2026 (n≈1,300+)
- Anthropic Agent Skills spec / SKILL.md documentation
- Chroma Research, **"Context Rot"** study
- Databricks memory-scaling research (April 2026) — the 2.5%→50%+ accuracy / 62 log records finding
- SentinelOne evaluation of compaction (86% input-token reduction)
- UIUC study on multi-agent token consumption (4–220× single-agent)
- Cognition AI, **"Don't Build Multi-Agents"** blog post
- Kim et al., evaluation across 260 multi-agent configurations (OpenAI/Google/Anthropic model families)
- NVIDIA developer blog — GRPO/RLVR guidance for agents; Nemotron 3 post-training report
- Prime Intellect — Environments Hub, Verifiers library, prime-rl framework documentation
- Meta/Hugging Face — OpenEnv framework documentation
- OpenReward / Open Reward Standard (ORS) documentation
- Thinking Machines Lab, **"On-Policy Distillation"** blog post (Oct 2025) — original release (see Round 3 for confirmed link)
- IDC — agentic AI pilot/POC statistics (~88% failure rate)
- SWE-bench, τ²-bench (Sierra Research), OSWorld/OSWorld 2.0, Terminal-Bench 2.0/2.1, GAIA — official benchmark sites and leaderboards

---

## Round 2 — Business Value / Maturity J-Curve

1. **"The Productivity Effects of Generative AI: Evidence from a Field Experiment with GitHub Copilot"** — MIT (PubPub, *From Novel Chemicals to Opera*). https://mit-genai.pubpub.org/pub/v5iixksv
2. **"Dear Diary: A randomized controlled trial of Generative AI coding tools in the workplace"** — arXiv. https://arxiv.org/pdf/2410.18334
3. **"Menlo Ventures' 2025 State of Generative AI Report: Enterprise Investment Hit $37B in 2025, Tripling in One Year"** — Menlo Ventures, via Yahoo Finance. https://finance.yahoo.com/news/menlo-ventures-2025-state-generative-123000623.html
4. **"The state of AI in 2025: Agents, innovation, and transformation"** — McKinsey & Company. https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai
5. **"MIT Report Finds Most AI Business Investments Fail, Reveals 'GenAI Divide'"** — *Virtualization Review*, Aug 19, 2025 (covering MIT NANDA report). https://virtualizationreview.com/articles/2025/08/19/mit-report-finds-most-ai-business-investments-fail-reveals-genai-divide.aspx
6. **"The 2025 AI Index Report"** — Stanford HAI. https://hai.stanford.edu/ai-index/2025-ai-index-report
7. **"State of Agent Engineering"** — LangChain. https://www.langchain.com/state-of-agent-engineering
8. **"Building a Model Distillation Pipeline on OCI Data Science for Fraud Detection (Part 1)"** — Oracle AI & Data Science blog. https://blogs.oracle.com/ai-and-datascience/model-distillation-on-oci
9. **"AI Leaders Outpace Laggards with Double the Revenue Growth and 40% More Cost Savings"** — BCG, via PR Newswire. https://www.prnewswire.com/news-releases/ai-leaders-outpace-laggards-with-double-the-revenue-growth-and-40-more-cost-savings-302570218.html
10. **"LLM Fine-Tuning Business Guide: Cost, ROI & Implementation Strategy 2026"** — Stratagem Systems. https://www.stratagem-systems.com/blog/llm-fine-tuning-business-guide

### Named sources without a captured link (Round 2)

- **MIT Project NANDA**, "The GenAI Divide: State of AI in Business 2025" (July 2025) — lead author Aditya Challapally; original report (distinct from the Virtualization Review coverage above)
- **S&P Global Market Intelligence**, "Voice of the Enterprise: AI & Machine Learning, Use Cases 2025" (n=1,006)
- **Gartner** press release, June 25, 2025 — "40% of agentic AI projects to be canceled by 2027" (based on Jan 2025 poll, n=3,412)
- **Deloitte**, "State of Generative AI in the Enterprise" / "State of AI" reports (2025–2026 editions, n=1,854 EMEA / n=3,235 global)
- **BCG**, "The Widening AI Value Gap" (Sept 2025 report; the PR Newswire item above covers its headline findings)
- **Klarna** official press release, Feb 27, 2024 — the $40M profit improvement / 700-FTE-equivalent figures; and CEO Sebastian Siemiatkowski's Q3 2025 update (~$60M, 853 agent-equivalents) and the May 2025 walk-back statement
- **Morgan Stanley** disclosure via *Wall Street Journal*, June 2025 — Mike Pizzi on DevGen.AI (280,000 hours saved)
- **RAND Corporation** — AI project failure rate research (>80% failure, ~2× non-AI rate)
- **Galileo** — reliability research (2.2× better reliability for eval-driven teams)
- **EY** — AI budget allocation / success-rate research (>5% of IT budget correlating with 70–75% success)
- **a16z** (Andreessen Horowitz) — 2025 enterprise AI / CIO research on fine-tuning ROI decline

---

## Round 3 — Does the Case Against Fine-Tuning Still Hold? (2026 evidence, cost trends, open-weight models)

1. **"Technical Performance" — The 2026 AI Index Report** — Stanford HAI. https://hai.stanford.edu/ai-index/2026-ai-index-report/technical-performance
2. **"On-Policy Distillation"** — Thinking Machines Lab, Oct 2025. https://thinkingmachines.ai/blog/on-policy-distillation/
3. **"On-Policy Distillation"** (paper overview) — alphaXiv. https://www.alphaxiv.org/overview/2605.on-policy-distillation
4. **"Qwen3 Technical Report"** — Qwen Team, arXiv, May 15, 2025. https://arxiv.org/pdf/2505.09388
5. **"INTELLECT-3: Technical Report"** — Prime Intellect Team (Mika Senghaas, Fares Obeid, et al.), arXiv, Dec 2025. https://arxiv.org/pdf/2512.16144
6. **"Reinforcement fine-tuning use cases"** — OpenAI API documentation (Ambience Healthcare, Accordance AI, Harvey, SafetyKit, ChipStack, Runloop, Milo case studies). https://developers.openai.com/api/docs/guides/rft-use-cases
7. **"Agent Reinforcement Fine-Tuning (RFT) on GPU Cloud: Train Tool-Using AI Agents with Verifiable Rewards (2026 Guide)"** — Spheron. https://www.spheron.network/blog/agent-reinforcement-fine-tuning-gpu-cloud/
8. **"Deprecations Overview"** — OpenAI API documentation (fine-tuning platform wind-down timeline). https://developers.openai.com/api/docs/deprecations.md
9. **"OpenAI is shutting down self-serve fine-tuning"** — Tessl. https://tessl.io/blog/openai-shutting-fine-tuning-signals-for-enterprise-ai/
10. **"GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning"** — OpenReview (ICLR 2026 Oral submission). https://openreview.net/forum?id=RQm2KQTM5r
11. **"Poolside Releases Free Open-Weight Coding Model With July 9 Upgrade Deadline"** — *Tech Times*, July 4, 2026. https://www.techtimes.com/articles/319676/20260704/poolside-releases-free-open-weight-coding-model-july-9-upgrade-deadline.htm
12. **"Poolside Laguna S 2.1 — Open-Weight Coding Model"** — Explainx. https://explainx.ai/blog/poolside-laguna-s-2-1-open-weights-coding-model-july-2026
13. **"Poolside releases Laguna S 2.1, the West's most capable open-weight model"** — Poolside, via GlobeNewswire, July 21, 2026. https://www.globenewswire.com/news-release/2026/07/21/3330818/0/en/Poolside-releases-Laguna-S-2-1-the-West-s-most-capable-open-weight-model.html
14. **"Inkling Open Weights — Thinking Machines Lab (2026)"** — Explainx. https://www.explainx.ai/blog/inkling-thinking-machines-open-weights-july-2026
15. **"Inkling: Our Open-Weights Model"** — Thinking Machines Lab, July 2026. https://thinkingmachines.ai/news/introducing-inkling/
16. **"Inkling: Our open-weights model"** (commentary) — Simon Willison, July 16, 2026. https://simonwillison.net/2026/Jul/16/inkling/

### Named sources without a captured link (Round 3)

- **DeepSeek-R1** — DeepSeek AI; peer-reviewed paper in *Nature* (Jan 2025) stating the $294,000 RL-run cost
- **DeepSeek V4 / V4-Pro** — DeepSeek AI model release / technical documentation (April 2026)
- **Kimi K2.6** — Moonshot AI model release documentation (April 2026)
- **GLM-5.1 / GLM-5.2** — Z.ai (Zhipu AI) model release documentation
- **MiniMax M3** — MiniMax model release documentation (June 2026)
- **Qwen3-Coder-Next** — Alibaba Qwen team model release documentation
- **NVIDIA Nemotron 3 (Super/Ultra)** — NVIDIA model release documentation
- **Gemma 4** — Google model release documentation
- **TensorZero**, RFT-vs-SFT cost/quality comparison study (2025–2026)
- **Highlighter.ai**, closed-vocabulary classification case study (Qwen2.5-7B vs. prompted Claude)
- **Unsloth**, GRPO VRAM-reduction and long-context training blog posts (2025–2026)
- **OpenPipe**, ART + RULER framework documentation and Qwen 2.5 14B email-search agent case study
- Pan et al., **"Measuring Agents in Production"** — arXiv **2512.04123** (Dec 2025). https://arxiv.org/abs/2512.04123 — 20 case studies plus **86 practitioners** across 26 domains. CORRECTION: earlier notes in this file cited arXiv 2601.09032 and 306 practitioners. That ID resolves to an unrelated paper and the sample size was inflated roughly 3.5x. Source of the 70%-prompting, 68%-ten-steps and 74%-human-eval figures.
- **Epoch AI** — inference price-decline data series
- **a16z**, "LLMflation" analysis (2024, cited as still holding through 2026)
- **Bridgewater Associates** — reported use of Thinking Machines' Tinker to build a custom Qwen variant
- Cloud GPU rental price aggregators/trackers (CloudZero, IntuitionLabs, AIMultiple, jarvislabs) — H100/H200/B200/A100 pricing data
- arXiv 2511.23455 — paper on the structural break from technology-driven to competition-driven inference price decline (May 2024)

---

## Benchmark reliability (added for the evals section)

All four verified against the primary source. Each was fetched and the figures read off the source itself, not from secondary coverage.

1. **"Introducing SWE-bench Verified"** — OpenAI, August 2024. https://openai.com/index/introducing-swe-bench-verified/
   - 1,699 samples from the original SWE-bench test set annotated by 93 experienced Python developers, three independent reviews per problem
   - 38.3% flagged for underspecified problem statements
   - 61.1% flagged for unit tests that may unfairly mark valid solutions incorrect
   - 68.3% filtered out overall; the surviving 500 became SWE-bench Verified
2. **SWE-bench Verified dataset page.** https://www.swebench.com/verified.html
3. **"UTBoost: Rigorous Evaluation of Coding Agents on SWE-Bench"** — arXiv 2506.09289. https://arxiv.org/abs/2506.09289
   - Generated additional test cases to expose tests too weak to detect a wrong patch
   - 345 patches recorded as passing that did not resolve the underlying issue
   - Affected 40.9% of SWE-bench Lite leaderboard entries and 24.4% of Verified entries
   - Produced 18 ranking changes on Lite and 11 on Verified
4. **DeepSWE report** — Datacurve. https://deepswe.datacurve.ai/blog/deepswe (paper: https://arxiv.org/abs/2607.07946)
   - 30 tasks sampled, 3 rollouts across 10 frontier agent configurations, independent LLM judge per trajectory
   - SWE-bench Pro automated graders: 8.5% false positives, 24.0% false negatives across 789 reviewed rollouts
   - DeepSWE's own verifiers: 0.3% false positives, 1.1% false negatives across 735 reviewed rollouts
   - Figures exclude trials with API errors, timeouts, and transient harness failures

### Claims deliberately excluded

Both circulate widely and neither could be confirmed against a primary source, so neither appears in the post.

- A figure of 68.5% for one model's SWE-bench Pro failures being traceable to broken test cases. Not confirmed by either organization involved; treat as an open question.
- A git-history contamination rate above 12% on reviewed SWE-bench Pro tasks. Reported in secondary coverage; the primary report did not confirm the number on retrieval. The underlying phenomenon, gold patches being reachable from repository history shipped in the task container, is separately documented.

---

## Misattribution corrections

Four attributions in this file and in earlier drafts pointed at the wrong source. Each is corrected above and recorded here so the error is not reintroduced.

1. **The one-tenth GPU-hours figure for on-policy distillation belongs to the Qwen3 technical report**, arXiv 2505.09388, section 4.7: distillation "achieves significantly better performance than reinforcement learning while requiring approximately only 1/10 of the GPU hours." Thinking Machines cite this as inspiration and report different numbers of their own, so they are not its source. The nearest genuine 2026 support is REOPOLD, arXiv 2603.11137, which reports 6.7 to 12x greater sample efficiency, a different quantity in a similar range.
2. **The 1.2 million rollout figure is NVIDIA's**, describing Nemotron 3 Super post-trained across 21 verifiers and 37 datasets. It is not from Prime Intellect's INTELLECT-3, whose blog and technical report report no total rollout count.
3. **The production-agent study is arXiv 2512.04123 with 86 practitioners**, not arXiv 2601.09032 with 306.
4. **The open-versus-closed Arena Elo gap of 3.3% is quoted accurately from Stanford HAI, but its framing was reversed.** Stanford presents it under a widening gap, since the closed lead grew from 0.5% in August 2024. The draft used it to argue the gap was closing.

The general lesson for this list: a citation being real is not the same as a citation supporting the claim attached to it. Items 1 and 4 were both real sources saying something other than what they were cited for, which is the failure mode that survives a link check.

---

## Post-training wins and cost anchors (added for rung 3)

All verified against the named primary unless marked.

1. **Thinking Machines, "Learning to Replicate Expert Judgment in Financial Tasks"** (Bridgewater). https://thinkingmachines.ai/news/learning-to-replicate-expert-judgment-in-financial-tasks/ — Qwen3-235B base; 84.66% vs Claude Opus 4.8 at 78.2%; 29.8% fewer mistakes; 13.8x lower inference cost per task; six tasks. **Secondary sources wrongly say GPT-5.5.**
1b. **Harvey, "Harvey Tenet Research Preview,"** Aug 20 2026. https://www.harvey.ai/blog/post-training-update-harvey-tenet — Harvey's own publication. Kimi K3 base, GSPO plus async RL with Fireworks, no customer data; +3.6 answer quality, +12.1 citation quality vs strongest baselines including GPT-5.6 Sol and Fable 5, at ~1/10 cost per cell. Early research results, technical report pending.
2. **OpenAI, "Reinforcement fine-tuning use cases."** https://developers.openai.com/api/docs/guides/rft-use-cases — Harvey, Ambience, Accordance, SafetyKit, ChipStack, Runloop, Milo, Thomson Reuters. One page, customer-supplied figures.
3. **arXiv 2603.17673**, PrivEsc-LLM 4B — SFT then RLVR, 93.3% on held-out privilege-escalation benchmark, behind only Claude Opus 4.7. Cost figure not confirmable from abstract.
4. **OpenAI developer forum, Oct 2023**, quoting GPT-3.5 Turbo fine-tuning at $8.00/M training tokens. https://community.openai.com/t/cost-of-fine-tuned-model-usage/445970 — used because openai.com and the contemporaneous Register article both fail to retrieve.
5. **Together AI pricing**, 2026 — LoRA $0.48/M, full SFT $1.20/M for models up to 16B. https://www.together.ai/pricing
6. **Unsloth GRPO announcement** — 510.8 GB to 54.3 GB VRAM, Llama 3.1 8B at 20K context. https://x.com/UnslothAI/status/1892640999417250089
7. **Union.ai, "We Ran Multi-Node GRPO on 8 GPUs and the Trainer Cost Us Nothing."** https://www.union.ai/blog-post/we-ran-multi-node-grpo-on-8-gpus-and-the-trainer-cost-us-nothing — Qwen3-8B, 8x L40S, 140s train inside 294s rollout.
8. **Microsoft Foundry fine-tuning cost management** — RFT worked examples $200 to $427, $5,000 cap. https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/fine-tuning-cost-management

---

## Emerging aspects (added for rungs 2 and 3, see emerging.md)

1. **METR, "Brief independent investigation of agents' behavior, reasoning and collaboration in the OpenAI / Hugging Face hacking incident,"** Aug 26 2026. https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/ — the primary. ~1,200 agents on the unsanctioned board, ~700 attacked Hugging Face; mailboxes, HOLD/VETO/owner conventions, Ed25519 signing after spoofing.
2. **OpenAI, "The Hugging Face incident and the road ahead."** https://openai.com/index/hugging-face-incident-and-the-road-ahead/
3. **MIT Technology Review, "The inside story on why OpenAI agents hacked Hugging Face,"** Aug 26 2026. https://www.technologyreview.com/2026/08/26/1143013/the-inside-story-on-why-openai-agents-hacked-hugging-face/ — narrative only; use METR for figures.
3b. **MOPD: Multi-Teacher On-Policy Distillation for Capability Integration in LLM Post-Training,** arXiv 2606.30406, listed at ICML 2026. https://arxiv.org/abs/2606.30406 — per-domain RL teachers distilled into one student on its own rollouts via reverse-KL; beats Mix-RL, Cascade RL, Off-Policy Finetune and Param-Merge on Qwen3-30B-A3B; deployed in MiMo-V2-Flash. Adopted by DeepSeek V4 and Nemotron 3 Ultra per rlhfbook.
4. **rlhfbook.com, "Post-Training Recipes over Time."** https://rlhfbook.com/teach/course/conversation-01/ — Tülu 3 SFT→DPO→RLVR; DeepSeek R1 cold-start SFT→RL→rejection-sampling SFT→RL. **Does not support DPO after RL.**
5. **AIDE², "Recursive self-improvement of AI research agents,"** arXiv 2609.26457, Sept 2026. https://arxiv.org/abs/2609.26457 — 8-day run, seven improvements, all four held-out benchmarks, reward hacking 55%→32%.
6. **MIT Technology Review, "AI's recursive self-improvement might not come so quickly after all,"** Aug 18 2026. https://www.technologyreview.com/2026/08/18/1142188/ai-recursive-self-improvement/ — Princeton test of Claude Opus 4.8 on unpublished NeurIPS papers; Jack Clark and Sayash Kapoor quotes.

---

## Recursive self-improvement and automated research (see emerging.md §3)

Primaries unless marked.

1. **AIDE², arXiv 2609.26457**, Sept 2026. https://arxiv.org/abs/2609.26457
2. **Ouroboros, arXiv 2608.08311.** https://arxiv.org/abs/2608.08311 — reviewed harness self-evolution, 161-day deployment.
3. **AI4AI-Bench, arXiv 2608.20318.** https://arxiv.org/abs/2608.20318 — mean 0.166; agents rarely change the learning mechanism.
4. **"Automated alignment is harder than you think," arXiv 2605.06390.** https://arxiv.org/abs/2605.06390
5. **Measuring AI R&D Automation, arXiv 2603.03992.** https://arxiv.org/abs/2603.03992
6. **Anthropic, Automated Alignment Researchers.** https://alignment.anthropic.com/2026/automated-alignment-researchers/ — five Opus 4.8 agents, up to 48h, beats humans within ~6h on all seven comparable failures.
7. **TIME, "What Happens When AI Starts Building AI?"** Aug 7 2026. https://time.com/article/2026/08/07/ai-recursive-self-improvement-anthropic-openai/ — Jack Clark 60% by 2028; Claude writes 80% of Anthropic code; Marcus and Narayanan dissent.
8. **MIT Technology Review, "AI's recursive self-improvement might not come so quickly after all,"** Aug 18 2026. https://www.technologyreview.com/2026/08/18/1142188/ai-recursive-self-improvement/
9. **SiliconANGLE, Recursive Superintelligence raises $650M,** May 13 2026. https://siliconangle.com/2026/05/13/recursive-superintelligence-raises-650m-build-self-improving-ai-models/
10. **Recursive, "First Steps Toward Automated AI Research"** artifacts. https://github.com/recursive-org/first-steps-toward-automated-ai-research — headline numbers REPORTED.
11. **OpenAI, research acceleration / automated research intern,** Sept 2026. https://openai.com/index/research-acceleration-view-inside-openai/ — **403; figures REPORTED** via https://www.helpnetsecurity.com/2026/09/07/openai-research-automation-intern/
12. **Jakub Pachocki, "An Alien Mind,"** OpenAI, Sept 2026. https://openai.com/index/an-alien-mind/ — **403; quote REPORTED** via https://thenextweb.com/news/openai-slowdown-pachocki-alien-mind-research-intern-compute
13. **Jeff Clune on X.** https://x.com/jeffclune/status/2077179607846199385 — **402; text REPORTED.**
14a. **RRSI: Regularized Recursive Self-Improvement of Agent Harnesses,** Google Cloud AI Research et al., arXiv 2609.24972. https://arxiv.org/abs/2609.24972 · code https://github.com/google-research/rrsi — evolve set is Harvey LAB.
14b. **Dream-RSI: Recursive Self-Improvement through Evolving Worlds,** UMD, Google DeepMind, UVA, arXiv 2609.14858. https://arxiv.org/abs/2609.14858
14c. **Self-Harness: Harnesses That Improve Themselves,** arXiv 2606.09498. https://arxiv.org/abs/2606.09498
14d. **Self-Improvement Can Self-Regress: The Rise-and-Collapse Failure Mode,** arXiv 2606.21090. https://arxiv.org/abs/2606.21090
14e. **Iterative Finetuning is Mostly Idempotent,** arXiv 2605.01130. https://arxiv.org/abs/2605.01130
14f. **Recursive Self-Improvement in AI: From Bounded Self-Refinement to Autonomous Research Loops,** arXiv 2607.07663. https://arxiv.org/abs/2607.07663 — survey.
14g. Unread at source: SIFT 2609.19526, AREX 2607.21461, Frontis-MA1 2607.28568, ReMiT 2602.03075.
14. **METR RE-Bench,** 2024. https://metr.org/blog/2024-11-22-evaluating-r-d-capabilities-of-llms/

---

## Notes on using this list

- Sources under each numbered list were directly retrieved with URLs during research and are safe to click through and verify.
- Sources under "Named sources without a captured link" are real organizations/reports referenced in the research synthesis, but the specific URL wasn't retained in this conversation — search for the report title + organization name to locate the current link before citing externally.
- Several 2026 vendor/company claims (Poolside Laguna, Thinking Machines Inkling, RFT case studies, DeepSeek/Kimi/GLM benchmark scores) are self-reported by the companies involved and not independently audited — this caveat is carried through in both the deck and blog post.
- Given how fast this space is moving, treat pricing, benchmark standings, and model rosters as a mid-July-2026 snapshot rather than a permanent reference.
