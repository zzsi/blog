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
11. **"Rethinking On-Policy Distillation"** — arXiv, April 2026. https://arxiv.org/pdf/2604.13016

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
- Production-agent survey paper, arXiv 2601.09032 (Jan 2026), citing Pan et al. 2025 — 306 practitioners / 20 case studies / 26 domains
- **Epoch AI** — inference price-decline data series
- **a16z**, "LLMflation" analysis (2024, cited as still holding through 2026)
- **Bridgewater Associates** — reported use of Thinking Machines' Tinker to build a custom Qwen variant
- Cloud GPU rental price aggregators/trackers (CloudZero, IntuitionLabs, AIMultiple, jarvislabs) — H100/H200/B200/A100 pricing data
- arXiv 2511.23455 — paper on the structural break from technology-driven to competition-driven inference price decline (May 2024)

---

## Notes on using this list

- Sources under each numbered list were directly retrieved with URLs during research and are safe to click through and verify.
- Sources under "Named sources without a captured link" are real organizations/reports referenced in the research synthesis, but the specific URL wasn't retained in this conversation — search for the report title + organization name to locate the current link before citing externally.
- Several 2026 vendor/company claims (Poolside Laguna, Thinking Machines Inkling, RFT case studies, DeepSeek/Kimi/GLM benchmark scores) are self-reported by the companies involved and not independently audited — this caveat is carried through in both the deck and blog post.
- Given how fast this space is moving, treat pricing, benchmark standings, and model rosters as a mid-July-2026 snapshot rather than a permanent reference.
