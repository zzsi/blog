# Post-training: cost and methods

Research round, 2026-09-28. **[PRIMARY]** vendor page, paper or official post read directly; **[SECONDARY]** press or summary; **[DERIVED]** own arithmetic. 403s: openai.com/policies, thestreet.com; nature.com required login.

## 1. Is post-training getting cheaper? Cost per capability yes; compute prices no; budgets up

**The one-line version for the post:** the cost of getting a given capability into a small model keeps falling, the price of GPUs rose again in 2026, and what frontier teams choose to spend is going up.

### Falling

- **Together AI, Sep 11 2026**: training prices cut "starting from 30% and reaching 70%." LoRA SFT per 1M tokens: Qwen3.5-9B $0.48 → $0.34; gpt-oss-20b $1.50 → $0.40; gpt-oss-120b $5.00 → $2.50. Full fine-tune of Qwen3.5 9B now $0.38. [PRIMARY] **The $0.48 anchor in business-value.md §2e is stale.**
- **OpenAI, cheapest fine-tunable tier**: $8.00/M (gpt-3.5-turbo, 2023) → $3.00 (gpt-4o-mini, 2024) → $1.50 (gpt-4.1-nano, 2025). Flagship tier flat at $25. [PRIMARY — developers.openai.com/api/docs/pricing]
- **Fireworks**: LoRA SFT $0.50, LoRA DPO $1.00 per 1M tokens up to 16B. [PRIMARY]
- **LoRA Without Regret** (Thinking Machines, Sep 29 2025): "LoRA fully matches the learning performance of FullFT when running policy gradient algorithms," even at rank 1, at about two-thirds the FLOPs. [PRIMARY]
- **Tiny RL runs**: Tina, 1.5B, LoRA + RL, 43.33% AIME24 for "$9 USD" (arXiv 2504.15777) [PRIMARY]; Open-RS, ~$42 on 4× A40 for 24 hours, 46.7% AIME24 [PRIMARY].
- **Coding agents**: SERA (Ai2, arXiv 2601.20789), an SFT-only 32B coding agent for **$2,000** (40 GPU-days) reaching 49.5–54.2% SWE-bench Verified; $1,300 to specialise to one repository and match or beat the teacher; claims "26x cheaper than RL." Its appendix puts SkyRL-Agent at ~$9,200 and DeepSWE at ~$18,400. [PRIMARY]
- **RL frameworks**: verl 1.5–20x throughput; AReaL up to 2.77x from async RL; PipelineRL ~2x; OLMo 3's RL infrastructure 4x. Hugging Face surveyed 16 async RL libraries (Mar 2026). [PRIMARY]
- **DeepSeek-R1**: RL stages ~$294K at $2/H800-hour, versus ~$5.58M for the V3 base. [SECONDARY, via The Register citing Nature supplement]

### Rising

- **GPU rental rebounded.** H100 1-year contracts: $1.70/hr (Oct 2025) → $2.35 (Mar 2026), "almost 40%," attributed to agentic demand (SemiAnalysis) [PRIMARY]. H100 neo-cloud index $2.72/hr on Sep 28 2026 (Silicon Data) [PRIMARY]. Earlier: H100 median $7.76/hr in late 2023 down to $1.95 on marketplaces in late 2025 [PRIMARY]. So the long-run trend is down, the 2026 trend up.
- **Fireworks raised GPU prices Sep 1 2026**: H100 $7 → $8, B200 $10 → $13, B300 $12 → $15 — its first repricing of a published SKU. [old rates PRIMARY, increase SECONDARY]
- **Tinker raised prices Jul 17 2026**: prefill and sample about +50%, training about +10% (Qwen3-8B training $0.40 → $0.44). [SECONDARY; corroborated by PRIMARY price comparisons]
- **Google**: Gemini 3.5 Flash tuning $10/M vs $5 for 2.5 Flash; tuned endpoints from Gemini 3 priced at 1.5x the base model. [PRIMARY]
- **OpenAI**: GPT-5 family not fine-tunable; SFT/DPO only on gpt-4.1, RFT only on o4-mini. The lineup has not moved since April 2025. [PRIMARY]

### Budgets growing

- **"The Hidden Cost of Thinking"** (Morrison, Smith, Strubell, arXiv 2605.01158, on OLMo 3): "reasoning models are 17x more expensive to post-train than their instruction-tuned counterparts"; the RL generator is 87% of that energy; ablations and failed runs are 82% of total compute (91% for post-training). Agentic RL expected to amplify rollout length "potentially by orders of magnitude." [PRIMARY]
- ScaleRL: 400,000+ GPU-hours of experiments [PRIMARY]; Grok 4: RL "at pretraining scale" [PRIMARY]; o3 used 10x o1's RL compute [PRIMARY via Epoch].
- Multi-turn RL through per-token APIs re-prefills history each turn, so cost grows quadratically (Fireworks doc) [PRIMARY].

## 2. Methods

### SFT: cheap, small data, format and behaviour; memorises and forgets

- OpenAI: minimum 10 examples, "we recommend starting with 50 well-crafted demonstrations"; best for classification, format, correcting instruction-following. [PRIMARY]
- LIMA: 1,000 examples; answers equivalent or preferred to GPT-4's in 43% of cases. s1: 1,000 reasoning traces, Qwen2.5-32B SFT in "26 minutes on 16 NVIDIA H100 GPUs," beat o1-preview by up to 27%. [PRIMARY]
- Chu et al., ICML 2025: "SFT tends to memorize training data and struggles with out-of-distribution scenarios," yet "SFT remains essential for effective RL training." [PRIMARY]
- RL's Razor (arXiv 2509.04259): RL keeps prior capabilities better than SFT at equal new-task performance; forgetting tracks KL from the base. [PRIMARY]
- Thinking Machines: Qwen3-8B trained on internal documents dropped IF-eval from 85% to 45% (79% with a 70/30 mix); "no weighting … maintains the original performance." [PRIMARY]
- OLMo 3: continued SFT on a stronger model's chosen responses dropped the 7B average from 70.3 to 64.5 and "outright hurts." [PRIMARY]

### DPO and preference methods: pairs instead of demonstrations; fading from frontier recipes

- DPO trains offline on preference pairs, no reward model, no sampling (arXiv 2305.18290). [PRIMARY]
- Tülu 3: SFT → DPO → RLVR. 8B average 60.6 → 64.7 → 65.1. [PRIMARY]
- OLMo 3 "delta learning" DPO (chosen from Qwen3-32B, rejected from Qwen3-0.6B): SFT 70.1, SFT+DPO 72.7, SFT+RLVR 71.9, SFT+DPO+RLVR 74.1. DPO "remains a better starting point" for RL. [PRIMARY]
- Variants: SimPO (reference-free, up to +6.4 over DPO on AlpacaEval 2); KTO (needs only a good/bad label per example); ORPO (folds preference into SFT). [PRIMARY]
- Cost about 2–2.5x SFT per token. [PRIMARY]
- Nemotron 3 Ultra and MiMo-V2-Flash reports never mention DPO; RL plus on-policy distillation has taken its slot in 2026 frontier open recipes. [PRIMARY, grep check]

### Distillation: the most cost-effective way to move a teacher's skill into a small model

- **Off-policy (SFT on teacher outputs).** DeepSeek-R1: R1-Distill-Qwen-32B 72.6 on AIME24 vs 47.0 from running RL directly on Qwen-32B. "Distilling more powerful models into smaller ones yields excellent results, whereas smaller models relying on the large-scale RL … may not even achieve the performance of distillation." [PRIMARY]
- **On-policy (student samples, teacher grades every token).** Thinking Machines, Oct 27 2025: 60% → 70% AIME'24 in ~150 steps; 9–30x cheaper than the SFT route; personalisation example recovers IF-eval from 79% to 83% while raising internal QA to 41%. [PRIMARY] Qwen3 Table 21: on-policy distillation 74.4 AIME'24 at 1,800 GPU-hours vs RL 67.6 at 17,920 — "approximately only 1/10." [PRIMARY]
- **Multi-teacher (MOPD).** arXiv 2606.30406: normalized score 0.937 vs Mix-RL 0.882; reaches teacher plateau with ~25–30K samples vs 150–180K. [PRIMARY] Nemotron 3 Ultra: two MOPD rounds with 10+ teachers; SWE-bench Verified 65.8 → 71.7 (teacher 72.5); Terminal Bench 44.5 → 54.0, **beating its teacher's 50.0**; limit: works when the student can already sample the teacher's trajectories. [PRIMARY] DeepSeek V4: "independent cultivation of domain-specific experts … followed by unified model consolidation via on-policy distillation." [PRIMARY] arXiv titles with "on-policy distillation": 9 in 2024, 10 in 2025, 234 in 2026 to date. [PRIMARY, own query]
- **Enterprise product.** AWS Bedrock Model Distillation claims up to 500% faster, 75% cheaper, under 2% accuracy loss for RAG. [PRIMARY, vendor claim]

### The legal limit on distilling closed models

- Anthropic commercial terms: customers may not use the services "to build a competing product or service, including to train competing AI models." [PRIMARY]
- Google Gemini API terms: "You may not use the Services to develop models that compete with the Services." [PRIMARY]
- OpenAI terms: 403; recalled clause not verified. **Confirm before quoting.**
- Anthropic, Feb 23 2026, "Detecting and preventing distillation attacks": DeepSeek, Moonshot and MiniMax ran 16M+ exchanges through ~24,000 fraudulent accounts. Anthropic: "Distillation is a widely used and legitimate training method"; these campaigns broke its terms. [PRIMARY]
- **Practical reading:** distil from open-weight teachers, or through a vendor's own distillation product.

## Summary table

| Method | Use it for | Watch out for |
|---|---|---|
| SFT | Format, style, classification, a first stage | Memorises, forgets; SFT on stronger-model outputs can backfire |
| DPO family | Tone, preferences, a bridge into RL | 2–2.5x SFT cost; dropping out of frontier recipes |
| Distillation | Teacher-level skill in a small model, cheaply | Closed-model terms forbid competing models |
| MOPD | Merging several specialist teachers | Student must already be able to follow the teacher |
| RL | Behaviour the demonstrations never showed | Needs a verifier; rollouts dominate cost; can collapse past a peak |

## Agentic SFT: how much data, and how to filter it (research round 2026-09-28)

**Verdict:** a few hundred to a few thousand trajectories from a stronger model can lift a mid-size open model a lot. They must use the same tools and format as the harness the model will run in, or be spread across several harnesses. Keeping only successful runs is not clearly better. Almost all the evidence is from coding and terminal work.

**How much data**
- **SWE-Gym** (Dec 2024): "only 491 agent-environment interaction trajectories" gave "up to 19% absolute gains" on SWE-bench Verified and Lite. Performance was still rising at 491. **[PRIMARY, 2024]**
- **SWE-smith** (Apr 2025): 5,016 training trajectories, kept from a pool with a 36% resolve rate, reached 40.2% on SWE-bench Verified. It capped each task at 3 trajectories. **[PRIMARY, 2025]**
- **R2E-Gym** (Apr 2025): 3,321 trajectories reached 34.4%. Reasoning traces helped (34.2% vs 30.4%). **[PRIMARY, 2025]**
- **LIMI** (Sep 2025): "only 78 carefully designed training samples," averaging 42.4k tokens each. Its comparison against 10,000 samples used a different dataset, not a controlled test, and most of the gain disappears without the training CLI. **[PRIMARY, caveated]**
- **SWE-Lego** (Jan 2026): 18,000 validated trajectories reached 42.2% (8B) and 52.6% (32B). **[PRIMARY]**
- **Ai2 SERA** (report May 29 2026, checked): "Effectively specializing to a single repository requires approximately 8,000 trajectories ($1,300)," at which point the student matches its teacher. **[PRIMARY, author]**
- **Nemotron 3 Super** (Apr 2026): over 7M SFT samples, including 84,864 terminal samples and 1.5M tool-calling trajectories. **[PRIMARY, vendor]**

**Generation:** mostly teacher rollouts (Claude 3.7 Sonnet, Qwen3-Coder-480B, DeepSeek-V3.2, GLM-4.6). Some use humans with a model (LIMI), and some use synthetic tools (Kimi K2 used 20,000+).

**Filtering: what is used and what is measured**
- **In use:**
  - success only, via rejection sampling (SWE-Gym, SWE-smith, R2E-Gym, DeepSeek-V3.2);
  - rules on format and completion (Qwen3-Coder-Next);
  - LLM judges (Kimi K2, Nemotron);
  - decontamination: SWE-smith removed the 12 SWE-bench repos, and Nemotron-Terminal applies a 14-gram overlap filter.
- **Measured, 2026:**
  - Nemotron-Terminal (arXiv 2602.21193, Feb 24 2026, checked): "no filtering (12.4%) significantly surpasses both complete-only (6.74%) and success-only (5.06%) strategies," and "retaining unsuccessful trajectories appears to provide valuable supervision, exposing the model to realistic error states and recovery patterns."
  - SERA (checked): "no statistically significant difference between verification thresholds, H(3)=7.19, p=.066."
  - SWE-Lego: removing low-quality resolved runs gave a small gain (40.4 to 41.0, table value).
- **No ablations found** for LLM-judge filtering or deduplication.

**Failed trajectories and masking**
- GLM-5: "Erroneous segments within trajectories are retained but masked out in the loss function, allowing the model to learn error correction behaviors without reinforcing incorrect actions." **[PRIMARY, vendor]**
- SWE-Lego: masking error steps "improves model performance by over 2 points"; adding semi-resolved runs added +1.2%. **[PRIMARY]**

**Risks**
- **Format mismatch.** SERA (checked): "Deploying the model with a different agent scaffold, or even subtle formatting differences, degrades performance significantly." Nemotron 3 Super scored 60.47 on SWE-Bench in OpenHands and 53.73 in Codex, and trains across several harnesses for that reason. Qwen3-Coder-Next: more tool-call templates in training give more robustness.
- **Teacher habits and reward hacks.** SWE-Lego filters out runs that edit tests and removes git history. SWE-smith students loop far more than their teacher (over 25% vs under 4% of trajectories with a repeated sequence of length 10 or more). SFT on reward-hacking examples generalises the hacking (School of Reward Hacks, 2025).
- **Contamination.** SWE-Bench Illusion: models locate buggy files from the issue text alone "up to 76%" on SWE-bench, versus 53% elsewhere.
- **Forgetting.** NVIDIA: SFT "often degrades performance outside of the target domain." This agrees with the SFT section above.

**Enterprise practice:** no rigorous public case of multi-step agentic SFT built from production logs. The public cases use single-step distillation (NVIDIA Data Flywheel, 1B model at about 98% of a 70B on tool routing), RL on user accept/reject signals (Cursor Tab), memory (Databricks), or synthetic data from the company's own code (SERA: "Closed models haven't seen your internal code").
