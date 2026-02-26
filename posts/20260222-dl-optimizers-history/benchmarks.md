---
listing: false
---

# Optimizer Benchmarks for This Post

This file tracks practical benchmark choices for comparing deep learning optimizers in a way that is both credible and runnable.

## Principles

- Keep comparisons fair: same model, data order, token/image budget, precision, and tuning budget.
- Report both quality and efficiency: final loss/accuracy and time/compute to target.
- Use multiple scales: a method that wins at small scale may fail at larger scale.
- Separate "quick sanity checks" from "publication-grade evidence".

## Recommended Benchmark Stack

## Tier 1: Quick sanity checks (hours)

Goal: catch obvious instability or poor defaults quickly.

- CIFAR-10 (optionally CIFAR-100) with small ResNet or ViT-tiny
  - Why: fast, cheap, easy to iterate.
  - Metrics: train loss curve, test accuracy, wall-clock.

- nanochat/nanochat (small language-model benchmark)
  - Why: reveals optimizer behavior on autoregressive objectives with low runtime.
  - Metrics: validation loss/perplexity vs steps and tokens.

Use case: smoke-test AdamW vs SGD+momentum vs one conditioning method.

## Tier 2: Mid-scale decision benchmarks (1-3 days)

Goal: choose optimizer for a real project setting.

- ImageNet-1k with ResNet-50 or ViT-B/16
  - Why: standard vision comparison regime used by many optimizer papers.
  - Metrics: top-1, throughput, time-to-target accuracy.

- GPT-style pretraining at ~100M-1B parameters on a fixed token budget
  - Why: directly relevant to modern optimizer claims.
  - Metrics: validation loss/perplexity vs tokens and wall-clock.

- Image generation on CelebA-HQ (or FFHQ) with a compact diffusion setup
  - Why: tests optimizer stability and quality under generative objectives.
  - Metrics: FID, training stability, time-to-target FID, and memory usage.

Use case: evaluate production candidate optimizers under matched tuning budgets.

## Tier 3: Frontier-scale evidence (large clusters)

Goal: validate scaling claims and conditioning behavior at large model size.

- GPT/LLaMA-style pretraining at multi-billion parameter scale
  - Why: this is where many new conditioning methods claim gains.
  - Metrics: loss-to-token, loss-to-FLOP, stability/failure rate, hardware efficiency.

- Optional MoE runs if your stack is MoE-first
  - Why: optimizer behavior can change with sparse activation and routing noise.

Use case: only for teams with enough compute and strict experiment control.

## Common Tasks Used in Optimizer Literature

- Vision: ImageNet-1k, CIFAR-10/100.
- Language: BERT/GPT-style pretraining and perplexity tracking.
- Translation (historically): WMT14 En-De (used in Adafactor-era work).
- Systems benchmarks: MLPerf Training.
- Optimizer research suite: DeepOBS.

## Metrics to Report (Minimum)

- Final quality metric: accuracy or perplexity/loss.
- Time-to-target quality.
- Compute-to-target quality (FLOPs or token budget).
- Peak memory and effective batch size.
- Stability metrics: divergence count and variance across >= 3 seeds.

## Fair Comparison Checklist

1. Same architecture and tokenizer/data pipeline.
2. Same training token/image budget.
3. Same data ordering or controlled shuffling.
4. Same precision and distributed settings.
5. Same hyperparameter tuning budget per optimizer.
6. Same stopping rule and evaluation cadence.

## Practical recommendation for this blog post

To keep examples useful for readers:

- Prioritize this triad for coverage:
  - CIFAR-10 classification.
  - nanochat/nanochat language modeling.
  - CelebA-HQ/FFHQ image generation.
- Provide 1-2 runnable demos from that triad (Tier 1 or small Tier 2).
- Include a benchmark matrix table for the rest.
- Clearly label evidence level: toy, mid-scale, or frontier.

## Suggested references

- Muon scalable LLM training: https://arxiv.org/abs/2502.16982
- NorMuon: https://arxiv.org/abs/2510.05491
- TEON: https://arxiv.org/abs/2601.23261
- Hyperparameter transfer (matrix preconditioners): https://arxiv.org/abs/2512.05620
- ARO: https://arxiv.org/abs/2602.09006
- LAMB: https://arxiv.org/abs/1904.00962
- LARS: https://arxiv.org/abs/1708.03888
- SAM: https://arxiv.org/abs/2010.01412
- Lion: https://arxiv.org/abs/2302.06675
- Adafactor: https://arxiv.org/abs/1804.04235
- MLPerf Training: https://mlcommons.org/benchmarks/training/
- DeepOBS: https://deepobs.github.io/
