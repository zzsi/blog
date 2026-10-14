# AI infrastructure in 2026: what matters for owning and running a model

Research notes for "How to Customize Agents, and When to Own Them". Collected 2026-10-11.

The question: which 2026 infrastructure developments matter to a company deciding whether to own and run a model, or to run agents at scale? Most of this belongs in the Layer 3 "run open weights" paragraph (9.2) and the training-cost paragraph (9.6).

Verification legend:
- **Checked by me**: I fetched the source and confirmed the quote or numbers myself.
- **Agent-verified**: a research agent fetched the source and quoted it; I have not re-read it.
- **Vendor self-report**: a vendor reporting on its own product or benchmark.

## Ranked findings

### 1. Agent traffic is mostly re-read context, so caching is the main cost lever, whether you rent or own

- **Source:** vLLM blog, "Mooncake store", May 6, 2026. https://vllm.ai/blog/2026-05-06-mooncake-store
- **Status:** checked by me.
- **Quotes:**
  - "Across the Codex/SWE-bench Pro dataset, comprising 610 traces with a median of 33 turns per trace, we observe: 94.2% cache hit rate 131:1 input-to-output ratio".
  - "If we can cache those prefixes, prefill for the cached portion becomes essentially free."
- **Agent-verified:**
  - A shared KV-cache store gave about 3.8x throughput, with the cache hit rate going from 1.7% to 92.2%.
  - Renting side: Anthropic's pricing page lists cache reads at 0.1x the base input price, and 0.025–0.05x on the newest models (live page, undated: https://platform.claude.com/docs/en/about-claude/pricing).
  - Anthropic's Claude Code team, April 30, 2026: "we run alerts on our prompt cache hit rate and declare SEVs if they're too low" (https://claude.dev/blog/lessons-from-building-claude-code-prompt-caching-is-everything/).
- **Fit:** 9.2 serving cost. It could also be a cost note in Layer 2 (2.5 governance on cost, or 3.4).

### 2. At full load, self-hosting can be far cheaper than a frontier API

This is the other side of the draft's 17.5x figure.

- **Source:** vLLM and Inferact, "vLLM on SemiAnalysis AgentX", September 8, 2026. https://vllm.ai/blog/2026-09-08-vllm-agentx
- **Status:** checked by me. Vendor self-report: the serving engine is benchmarking itself.
- **Quotes:**
  - "Across DeepSeek V4 Pro, MiniMax M3, and Kimi K3, vLLM delivers a 14.6×–106× serving-cost advantage over Opus 5 API pricing".
  - "The comparison is about serving cost, not model quality."
  - The comparison "excludes cache-write charges and long-context pricing premiums".
  - vLLM's figures assume "a theoretical cache hit rate of more than 96%".
- **Caveats:**
  - The models are different, so this is not like-for-like.
  - It assumes full saturation and an ideal cache.
  - It runs on GB300/B300 hardware.
- **The draft's 17.5x source:** arXiv 2606.11690, a single-author preprint from June 10, 2026 (agent-verified). It ran Mixtral 8x7B on one H100: $15.25 per million tokens at 1 request/s against $0.87 at 25 requests/s. The same paper finds that FP8 quantization carries the larger penalty at low load, and that the penalty "collapses to ≈1.0× by λ=50" requests/s. Quantization pays only with traffic.
- **Fit:** 9.2, paired with the existing 17.5x sentence: owning a model is a bet on your traffic.

### 3. Serving at scale is a distributed-systems job

- **Source:** vLLM project, "Disaggregated serving guide", September 29, 2026 (author from IBM Research). https://vllm-project.github.io/2026/09/29/disaggregated-serving-guide.html
- **Status:** checked by me.
- **Quotes:**
  - "The catch: you now operate three or four services instead of one and the KV transfer is a new failure mode."
  - "Collocated is still the right answer for plenty of deployments."
  - Recommendations include "Stay collocated or measure first."
- **Agent-verified:** splitting prefill from decode gave 2.4x goodput (73 of 100 requests met the latency targets, against 30 of 100).
- **Fit:** 9.2. It makes the hidden staffing cost concrete. The draft already says break-even studies "leave out the people who run the serving stack".

### 4. Post-training is now sold per token, so you no longer pay for idle GPUs when you train

- **Fireworks** pricing page (live, undated), https://fireworks.ai/pricing. Checked by me: "Serverless Training API … There's no provisioning and no idle cost. You pay only for the tokens you prefill, sample, and train."
- **Tinker** changelog, https://tinker-docs.thinkingmachines.ai/changelog/. Checked by me (2026-10-12) for the July 17 entry: on July 17, 2026, "prefill, sample, and training rates went up on standard context-length models"; Qwen3-8B now trains at $0.44 per million tokens. The reason given in some blogs ("rising compute costs") is secondary; the changelog gives no reason.
- **Amazon Bedrock** added reinforcement fine-tuning for open-weight models (qwen3-32b, gpt-oss-20b) on February 17, 2026. Agent-verified. https://aws.amazon.com/about-aws/whats-new/2026/02/amazon-bedrock-reinforcement-fine-tuning-openai
- **Fit:** 9.6 training cost. It also tempers the draft's price-cut sentence, because training prices moved in both directions in 2026.

### 5. Non-NVIDIA chips are a speed tier, not the cheap tier

- **OpenAI**, February 12, 2026, https://openai.com/index/introducing-gpt-5-3-codex-spark/. Agent-verified: "GPUs remain foundational … and deliver the most cost effective tokens for broad usage. Cerebras complements that foundation by excelling at workflows that demand extremely low latency." The model runs at over 1,000 tokens per second.
- **Anthropic**, April 6, 2026, https://www.anthropic.com/news/google-broadcom-partnership-compute. Agent-verified: "We train and run Claude on a range of AI hardware—AWS Trainium, Google TPUs, and NVIDIA GPUs."
- **Fit:** one clause at most. A company usually reaches these chips through someone else's API.

### 6. GPU-hour prices are volatile enough to hedge

- **Source:** CME Group press release, August 11, 2026. Agent-verified, archived copy. https://www.cmegroup.com/media-room/press-releases/2026/8/11/cme_group_and_silicondatatolaunchcomputefuturesonoctober5tounloc.html
- **Quote:** futures on H100 and B200 rental indexes from October 5, 2026, "pending regulatory review … hedging and investment vehicles to businesses looking to manage the cost of compute."
- **Not confirmed:** that the contracts actually launched.
- **Spot reference:** Fireworks lists on-demand H100 at $8/hr and B200 at $13/hr (agent-verified).
- **Fit:** optional, next to the "GPU prices rose in 2026" sentence in 9.6.

### 7. Run the agent loop on a different machine from the code it writes

- **Source:** OpenAI, April 15, 2026, https://openai.com/index/the-next-evolution-of-the-agents-sdk/. Checked by me via the archived copy.
- **Quotes:**
  - "Separating harness and compute helps keep credentials out of environments where model-generated code executes."
  - It names seven sandbox providers: Blaxel, Cloudflare, Daytona, E2B, Modal, Runloop and Vercel.
- **Fit:** the Layer 2 sandbox and security material (3.2–3.3, 7.6), not Layer 3. It matches the earlier harness-versus-sandbox discussion.

### 8. Custom kernels: big gains in isolation, small gains end to end

- **FastKernels**, arXiv 2605.23215, May 22, 2026, revised October 1. Checked by me: "kernel-level speedups of 1.6-6.6× shrink to at most 1.25× end to end, only 20% of winning kernel sets run correctly as-is".
- **Cursor and NVIDIA**, April 14, 2026, https://cursor.com/blog/multi-agent-kernels. Agent-verified: agents optimized 235 kernels for a 38% geometric-mean speedup, but the one attention kernel tested end to end gave a "3% speedup for time to first token."
- **Fit:** not needed for this audience. If used, one clause explaining why most companies should leave kernels to serving-engine vendors.

## Recommendation

**Add a short paragraph to 9.2, right after the 17.5x sentence.** The point: owning a model is a bet on your traffic. Draft:

&gt; That gap runs both ways. At full load, vLLM's benchmark of real coding-agent traffic puts open models on rented Blackwell GPUs at 15 to 106 times below Opus 5's API price, though for different models and on vLLM's own numbers. Agent traffic is what makes this possible: inputs outnumber outputs about 130 to 1, and over 94% of each prompt repeats the previous turn, so whoever caches best pays least, whether that is you or your API provider. Reaching full load is a distributed-systems job, and vLLM's own guide warns that the faster setups mean you "operate three or four services instead of one." If your traffic is low or bursty, rent tokens, and that now includes training: Fireworks bills post-training per token with "no idle cost."

**One-sentence alternative:**

&gt; At full load the gap reverses: on agent traffic, where over 94% of each prompt is already cached, vLLM measured open models at 15 to 106 times below a frontier API's price, so owning pays only if you can keep the GPUs busy.

**Custom kernels:** leave them out of this article. Kernels are the job of serving-engine vendors (vLLM, SGLang, Fireworks, Together) and labs. The 2026 evidence says even AI-written kernels give small end-to-end gains. Infrastructure deserves its own post if KUNGFU.AI wants to be known for it.

## Problems found in the current draft

- **9.6, "Together AI cut its training prices by 30 to 70% in September 2026."** The agent found no announcement of a cut. What I found (secondary trackers: pricingsaas.com, costbench.com) is a restructuring around September 11–12, 2026: three size tiers became a per-model table of 29 models, and the flat $4 job minimum became per-model minimums of $4–$60. Some models may be cheaper and others more expensive. **Resolved 2026-10-12:** the sentence was cut. Together's live price page (checked by me) lists $0.34 per million tokens for LoRA and $0.38 for full fine-tuning on its smallest models, including Qwen3.5 9B, so the figure's $17 and $19 hold; the caption now says "as of October 2026". The figure caption under 9.6 also cites "Together AI's price list after its September 2026 cut".
- **9.6, "H100 rental contracts got more expensive through 2026."** The figure usually quoted (one-year contracts from $1.70 to $2.35, October 2025 to March 2026, credited to SemiAnalysis) was found only in secondary sources. It needs a primary source. **Resolved 2026-10-12:** cut from the article and replaced with Tinker's July 2026 rate rise.
- **9.2, the 17.5x figure:** the source is a single-author, non-peer-reviewed preprint (arXiv 2606.11690), small models on an H100. Label it as such, and don't set it against an exact API price.

## Not verified

- **Self-hosting break-even including staffing:** no 2026 primary source. Pan et al. (arXiv 2509.18101) is from 2025 and doesn't mention staffing in its abstract; "0.5 FTE" style figures come from vendor blogs.
- **Cognition's VM hypervisor:** the posts are from 2025.
- **Modal's sandbox pricing:** secondary sources only.
- **Fireworks reinforcement fine-tuning "$7/hr":** secondary. The live page shows H100 at $8/hr and dedicated training billed per GPU hour.
- **Microsoft Foundry reinforcement fine-tuning** (April 16, 2026): no published pricing.
- **CME compute futures:** the October 5 launch is not confirmed.
