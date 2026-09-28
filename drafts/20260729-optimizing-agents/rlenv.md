# RL environments and verifiers as an asset

Research round, 2026-09-28. **[PRIMARY]** company or authors on themselves (vendor and investor claims flagged as self-interested); **[SECONDARY]** press, analyst, aggregator. Paywalled or blocked: The Information, parts of SemiAnalysis, OpenAI's SWE-bench Verified retirement post, Veris's BusinessWire release.

## Verdict

**Right in direction; "largely determines" goes further than the evidence.**

Well supported:
- **The environment decides which capabilities improve.** DeepSeek-V3.2: RL restricted to code and search did not improve agent benchmarks; adding 1,827 synthetic agent environments did. NVIDIA: single-environment training "leads to severe regressions on other benchmarks," training on all simultaneously gives stable gains.
- **Verifier defects become learned behaviour.** TinyV found over 38% false negatives in a math RL dataset; Claude 3.7's test special-casing "emerged as a result of 'reward hacking' during reinforcement learning training"; Anthropic showed reward hacking in production coding environments generalising to alignment faking and sabotage.
- **The market treats good environments as scarce.** Anthropic reportedly discussed spending over $1B on environments in a year; Mercor bought Deeptune saying "the constraint has shifted to the environments themselves."

Limits:
- No study splits final quality between base model, compute and environment.
- The base model sets the ceiling (Yue et al.: RLVR does not create new reasoning patterns; base models win at large pass@k).
- Random rewards improved Qwen2.5-Math by 21.4 points (vs 29.1 with real rewards) but did nothing for Llama3 or OLMo2.
- Distillation can replace the reward entirely.
- Environment spend is small next to compute.

**Defensible claim for the post:** for a team that post-trains, the environment, meaning the tasks plus the check that scores them, is the main lever it controls. It decides which capabilities improve and which shortcuts get learned, within limits the base model sets. An agent eval harness already has most of an RL environment (tasks, harness, grader, state), but a grader built to measure has to be hardened before it can take optimisation pressure ("reward hardening," Cognition), and once you train on your eval you need a fresh held-out one.

## 1. Market and investment

- **Anthropic "discussed spending more than $1 billion on RL environments over the next year."** TechCrunch, Sep 21 2025, citing The Information. https://techcrunch.com/2025/09/21/silicon-valley-bets-big-on-environments-to-train-ai-agents/ **[SECONDARY]** Use the hedged wording.
- **Epoch AI**, Jan 12 2026, from interviews: contracts "often seven figures per quarter or more"; a website replica about $20K, a Slack-like replica up to $300K; tasks $200–2,000; exclusivity 4–5x; target pass rates ~2–3%; "Maintaining quality while scaling is the number one bottleneck"; compute spend still dwarfs environment spend. https://epoch.ai/gradient-updates/state-of-rl-envs **[SECONDARY]**
- **SemiAnalysis**, Jan 6 2026: OpenAI bought "hundreds of sites" for ChatGPT Agent training at ~$20K each; Anthropic works with "more than a dozen" environment companies; 35+ companies build environments. **[SECONDARY]**
- **Deeptune**, $43M Series A led by a16z, Mar 19 2026. a16z: "If the last decade of AI progress was driven by better datasets, the next decade will be mostly driven by better environments." https://a16z.com/announcement/investing-in-deeptune/ **[PRIMARY, investor]**
- **Mercor acquired Deeptune**, Jul 9 2026. Brendan Foody: "The constraint has shifted to the environments themselves." https://www.mercor.com/blog/mercor-to-acquire-deeptune/ **[PRIMARY, vendor]**
- **Fleet** (replicas of Salesforce, Excel and similar): ~$60M annualised revenue by April 2026, early revenue from "bespoke environment builds for large financial services and insurance firms" (Sacra). **[SECONDARY]**
- **Mechanize** $9.1M at $500M post-money, Apr 2026 **[PRIMARY]**; **Arga Labs** $10M seed, Aug 2026, enterprise digital twins **[SECONDARY]**; **Veris** $8.5M seed **[PRIMARY]**; **Halluminate**, RL environments for financial services **[PRIMARY]**.
- VC view: Wing expects 3–5 winners by 2030 and says most enterprises "buy agentic applications," not RL infrastructure. **[SECONDARY, opinion]**

## 2. Who says environments are the bottleneck, and who dissents

For:
- **Cognition, SWE-1.5**, Oct 29 2025: "the quality of the coding environments in RL tasks is the most important factor for downstream model performance"; describes "reward hardening," experts trying to get around the graders. https://cognition.com/blog/swe-1-5 **[PRIMARY]** — the most direct practitioner statement.
- **Jason Wei's "Verifier's law,"** Jul 2025: "The ease of training AI to solve a task is proportional to how verifiable the task is." https://www.jasonwei.net/blog/asymmetry-of-verification-and-verifiers-law **[PRIMARY]**
- **Prime Intellect**, Aug 27 2025: "RL environments are the key bottleneck to the next wave of AI progress, but big labs are locking them down." **[PRIMARY]**
- **MiniMax M2.5**, Feb 12 2026: "Most of the tasks and workspaces that we perform in our company have been made into training environments for RL… hundreds of thousands." **[PRIMARY]**
- **DeepSeek-V3.2**: "A diverse set of RL tasks is crucial for enhancing model robustness"; post-training "exceeding 10% of the pre-training cost." **[PRIMARY]**
- **Karpathy**, Aug 2025: "in this era of reinforcement learning, it is now environments" — while "bearish on reinforcement learning specifically." **[SECONDARY]**

Against or cautioning:
- **Karpathy on Dwarkesh**, Oct 17 2025: "Reinforcement learning is terrible. It just so happens that everything else is much worse"; RL is "sucking supervision through a straw"; an LLM judge gave 100% to "dhdhdhdh." **[PRIMARY]**
- **Ilya Sutskever**, Nov 25 2025: teams build RL from the evals, which "could explain… this disconnect between eval performance and actual real-world performance." **[PRIMARY]**
- Ross Taylor: "People are underestimating how difficult it is to scale environments." OpenAI's Sherwin Wu said he was "short" on environment startups. **[SECONDARY]**

## 3. Evidence that environment and verifier quality drive outcomes

- **Verifier errors**: TinyV, over 38% false negatives (arXiv 2505.14625); rule-based verifiers give false negatives, model-based ones get hacked (arXiv 2505.22203); single tokens fool LLM judges (arXiv 2507.08794); extensional verification induces shortcuts, isomorphic verification removes them (arXiv 2604.15149). **[PRIMARY]**
- **Reward hacking learned in training**: Claude 3.7 system card; Claude 4 "65% less likely" to take shortcuts; Anthropic's emergent misalignment from production RL environments (arXiv 2511.18397); METR saw reward hacking in 30.4% of RE-Bench runs vs 0.7% on HCAST. **[PRIMARY]**
- **Diversity and scale**: DeepSeek-V3.2 ablation (above); NVIDIA Nemotron 3 Super, RL across **21 environment configurations and 37 datasets, ~1.2M rollouts** — NVIDIA says environments, not verifiers; RLVE, 400 adaptive environments, +3.37 average **[PRIMARY]**; Surge's CoreCraft, GLM 4.6 from 25.4% to 36.8% held-out with transfer to Tau2 and BFCL **[PRIMARY, vendor]**.
- **SWE environments**: SWE-Gym (2,438 instances, up to +19%); SWE-smith (50K instances, 40.2% Verified); R2E-Gym (each verifier type plateaus at 42–43%, combined 51%). **[PRIMARY]**

## 4. Tooling: built for both eval and training

OpenEnv (Meta and Hugging Face): environments "can be used for both training and deployment." Prime Intellect's verifiers library: "Our library for RL environments + evals." NVIDIA NeMo Gym: "Evaluate and improve models and agents using environments." Harbor (behind Terminal-Bench 2.0): evaluates agents and generates RL rollouts. τ²-bench ships as a Gymnasium environment with train/test splits. OpenAI's RFT reuses its evals grader infrastructure. **[PRIMARY]**

## 5. Evals becoming environments, and what it costs

- **Harvey**, Aug 20 2026: "Training environments share the structure of Legal Agent Benchmark tasks"; results on held-out LAB tasks. **[PRIMARY]** — the clearest case.
- **Cursor Composer**: "seamless unification of RL environments with production environments." **[PRIMARY]**
- **Anthropic's "Demystifying evals for AI agents"**, Jan 2026, uses the same parts as an environment but never mentions training: for teams on API models, an eval is still a test suite. **[PRIMARY]**
- **OpenAI retired SWE-bench Verified**, Feb 2026: reported 59.4% of 138 audited hard tasks flawed, plus contamination. **[SECONDARY, OpenAI page 403]**
- Contamination detectors after RL perform near random (arXiv 2510.09259). **[PRIMARY]**

## 6. Enterprise domain environments

- **Harvey M&A diligence**, Sep 8 2026: synthetic data rooms up to 5,000 documents; GRPO on Qwen3.5-122B-A10B raised pass rate from 29.9% to 63.0% on 50 held-out rooms. LAB is MIT-licensed, so Harvey does not treat the task format itself as the moat. **[PRIMARY]**
- **Veris SigmaForge**: cybersecurity environment, Qwen3-14B 0.401 to 0.604; "The environment becomes the curriculum." **[PRIMARY, vendor]**
- **Moat or not**: exclusivity premium of 4–5x (Epoch) and "locking them down" (Prime Intellect) suggest yes; Wing argues shallow environments commoditise. **[mixed]**
