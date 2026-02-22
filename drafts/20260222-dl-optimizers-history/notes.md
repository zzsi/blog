# History of Deep Learning Optimizers (to 2025)

This reference tracks how optimization methods evolved into the standard recipes used in modern deep learning.

## 0) What an optimizer is doing

At each training step, we turn a noisy gradient estimate `g_t` into an update `delta_theta_t`.

- Direction control: where to move in parameter space.
- Step-size control: how far to move.
- Stability control: avoid exploding or vanishing updates under noise and curvature.
- Resource control: memory footprint, compute overhead, and communication cost.

Most innovations are one of:

1. Acceleration (momentum-like methods).
2. Preconditioning (adaptive scaling and curvature approximation).
3. Regularization-aware updates (correct weight decay handling).
4. Large-scale stabilization (large-batch and distributed training).
5. Generalization-aware updates (flatness or sharpness-aware methods).
6. Systems-aware efficiency (low precision, sharding, paging).
7. Geometry-aware steps (natural gradient, orthogonalization).

## 1) Foundations before modern deep learning (1960s-2000s)

### 1.1 Polyak momentum (heavy ball)

Citation: [Polyak, 1964](https://doi.org/10.1016/0041-5553(64)90137-5)

Problem: vanilla gradient descent zig-zags in ill-conditioned valleys.

Idea: keep velocity over time.

- `v_{t+1} = beta v_t + g_t`
- `theta_{t+1} = theta_t - eta v_{t+1}`

Impact: momentum became a default acceleration tool and still underpins modern recipes.

### 1.2 Nesterov acceleration (NAG)

Citation: [Nesterov, 1983](https://www.mathnet.ru/eng/dan/v269/i3/p543)

Problem: momentum may overshoot.

Idea: compute gradients at a look-ahead position.

Impact: Nesterov momentum appears in many high-performing SGD recipes.

### 1.3 Natural gradient

Citation: [Amari, 1998](https://doi.org/10.1162/089976698300017746)

Problem: Euclidean descent is parameterization-dependent.

Idea: use Fisher geometry for invariant steepest descent.

Impact: too expensive directly, but inspired scalable approximations like K-FAC and Shampoo.

## 2) Early deep learning resurgence (2010-2014)

### 2.1 SGD + momentum as workhorse

Citation: [Sutskever et al., 2013](https://proceedings.mlr.press/v28/sutskever13.html)

Why it worked:

- Cheap updates.
- Strong synergy with augmentation and inductive bias.
- Simple scaling.

Limitation: sensitivity to learning rate and curvature.

### 2.2 AdaGrad (2011)

Citation: [Duchi et al., 2011](https://jmlr.org/papers/v12/duchi11a.html)

Problem: sparse coordinates need larger effective steps.

Idea: per-parameter scaling via accumulated squared gradients.

Strength: sparse, convex-ish settings.

Weakness for deep nets: steps can shrink too much over long training.

### 2.3 RMSProp (2012)

Citation: [Hinton lecture notes, 2012](https://www.cs.toronto.edu/~tijmen/csc321/slides/lecture_slides_lec6.pdf)

Problem: AdaGrad denominator grows monotonically.

Idea: exponential moving average of squared gradients.

Impact: practical default and precursor to Adam.

### 2.4 AdaDelta (2012)

Citation: [Zeiler, 2012](https://arxiv.org/abs/1212.5701)

Problem: reduce sensitivity to explicit learning-rate tuning.

Idea: normalize updates by running RMS of gradients and updates.

Impact: less common now, but important in adaptive optimizer evolution.

## 3) The Adam era (2014-2017)

### 3.1 Adam

Citation: [Kingma and Ba, 2014](https://arxiv.org/abs/1412.6980)

Problem: robust defaults under noisy gradients and changing curvature.

Idea: combine first-moment momentum (`m_t`) and second-moment scaling (`v_t`) with bias correction.

Why it spread: much lower tuning friction.

Tradeoff: convergence and generalization concerns surfaced.

### 3.2 AMSGrad (2017)

Citation: [Reddi et al., 2018](https://openreview.net/forum?id=ryQu7f-RZ)

Problem: pathological convergence behavior in some Adam settings.

Idea: enforce non-increasing effective learning rates via max-tracked second moments.

Impact: key theoretical clarification; in practice AdamW became the larger practical shift.

## 4) AdamW and decoupled weight decay (2017-2019)

### 4.1 The issue with Adam + L2-as-gradient

In adaptive optimizers, adding `lambda * theta` to gradients is not equivalent to true weight decay.

### 4.2 AdamW

Citation: [Loshchilov and Hutter, 2017](https://arxiv.org/abs/1711.05101)

Fix: decouple weight decay from adaptive gradient normalization.

Impact: standard default for Transformers and many modern architectures.

Key point: a theory-informed implementation correction with major practical impact.

## 5) Large-batch optimizers (2017-2020)

### 5.1 LARS

Citation: [You et al., 2017](https://arxiv.org/abs/1708.03888)

Problem: global LR scaling breaks at extreme batch sizes.

Idea: layer-wise trust ratio (`||w|| / ||g||`) to stabilize relative updates.

Use case: very large-batch CNN training.

### 5.2 LAMB

Citation: [You et al., 2019](https://arxiv.org/abs/1904.00962)

Problem: bring layer-wise scaling to Adam-like moments.

Use case: large-batch BERT-style training.

By 2025: still useful in niche throughput-first regimes; less universal than AdamW.

## 6) Memory and systems-aware optimizers (2018-2023)

### 6.1 Adafactor

Citation: [Shazeer and Stern, 2018](https://arxiv.org/abs/1804.04235)

Problem: Adam second moments are expensive at scale.

Idea: factored second-moment statistics for matrix parameters.

Impact: enables larger models under memory constraints (notably T5-style settings).

### 6.2 Low-precision states (8-bit Adam and related)

Citation: [Dettmers et al., 2021](https://arxiv.org/abs/2110.02861)

Problem: optimizer states dominate memory.

Idea: quantized moments with near-Adam behavior.

Impact: common in finetuning and increasingly in larger-scale training pipelines.

### 6.3 Communication-aware variants (e.g., 1-bit Adam)

Citation: [Tang et al., 2021](https://arxiv.org/abs/2102.02888)

Problem: distributed bandwidth bottlenecks.

Idea: compress communicated optimizer information aggressively.

Impact: useful in specific large distributed setups.

## 7) Curvature approximations at scale (2015-2023)

### 7.1 K-FAC

Citation: [Martens and Grosse, 2015](https://arxiv.org/abs/1503.05671)

Problem: second-order methods are expensive due to Hessian size.

Idea: Kronecker-factored curvature approximations.

Impact: strong in some regimes, but overhead limits broad default adoption.

### 7.2 Shampoo

Citation: [Gupta et al., 2018](https://arxiv.org/abs/1802.09568)

Problem: practical blockwise preconditioning for large models.

Idea: matrix preconditioners per block with scalable approximations.

Impact: competitive in selected large-training contexts; more complex than AdamW.

## 8) Generalization-aware wave (2020-2023)

### 8.1 SAM

Citation: [Foret et al., 2020](https://arxiv.org/abs/2010.01412)

Problem: sharp minima may generalize worse.

Idea: optimize worst-case local loss in a neighborhood.

Impact: strong results in vision and some other domains; extra compute overhead.

### 8.2 Tweaks and hybrids

RAdam, Lookahead, AdaBelief, AdaBound, etc.

Citations: [RAdam](https://arxiv.org/abs/1908.03265), [Lookahead](https://arxiv.org/abs/1907.08610), [AdaBelief](https://arxiv.org/abs/2010.07468), [AdaBound](https://arxiv.org/abs/1902.09843)

Pattern: improve warm-up behavior, stability, or coupling.

Impact: useful in pockets, but rarely displacing AdamW/SGD at scale.

### 8.3 Search-designed optimizers (Lion, 2023)

Citation: [Chen et al., 2023](https://arxiv.org/abs/2302.06675)

Problem: human-designed families may be too constrained.

Idea: discover compact update rules via symbolic/program search.

Impact: validates optimizer design as a search problem.

## 9) Geometry/interference-aware updates (2024-2025)

### 9.1 Muon and orthogonalization

Citations: [Muon implementation](https://github.com/KellerJordan/Muon), [modular-duality framing](https://arxiv.org/abs/2410.21265)

Problem framing: gradients may interfere across dominant directions in large models.

Idea: structured orthogonalization or preconditioning to reduce interference.

Why notable: strong geometric motivation with relatively simple implementation.

Adoption status (as of 2025): promising and increasingly tested, but AdamW remained the mainstream documented baseline.

## 10) What won by 2025

### 10.1 Frontier LLMs and VLMs

Typical default: AdamW + warmup + decay schedule + clipping + careful weight decay exclusions.

Why: robust, mature, scalable implementation and systems compatibility.

### 10.2 Vision

- CNNs: SGD + momentum stays strong.
- ViTs: AdamW is standard.

### 10.3 Diffusion and flow-matching models

Typical default: Adam or AdamW (EMA often used).

### 10.4 LARS and LAMB

Useful for specific extreme large-batch settings, but not dominant defaults in most frontier pipelines.

## 11) Innovation drivers: theory, empiricism, systems

### 11.1 Theory-driven

- Nesterov acceleration.
- Natural gradient -> K-FAC/Shampoo.
- AdamW correctness.
- SAM objective reformulation.
- Muon geometric framing.

### 11.2 Empiricism-driven

- RMSProp.
- Adam practice-first adoption.
- Many tweak-based optimizers.
- Lion search-based discovery.

### 11.3 Systems-driven

- LARS/LAMB for throughput.
- Adafactor for memory.
- 8-bit, paged, sharded states.
- 1-bit communication-aware updates.

## 12) Likely next directions

1. Deeper geometry and subspace control.
2. Budgeted or selective curvature.
3. Search or auto-discovered update rules.
4. Systems-first state/communication-efficient designs.
5. Objective-aware optimization for robustness and calibration.

## 13) Mental map of optimizer families

- SGD + Momentum/Nesterov: acceleration with simplicity; strong in vision.
- Adaptive (AdaGrad/RMSProp/Adam/AdamW): variance-based preconditioning; robust defaults.
- Layer-wise (LARS/LAMB): large-batch stabilization.
- Memory-efficient (Adafactor, low-precision states): Transformer scaling.
- Curvature-based (K-FAC/Shampoo): approximate natural gradient.
- Generalization-aware (SAM): flatter minima preference.
- Geometry/interference-aware (Muon): structured directional control.
- Search-designed (Lion): machine-discovered update rules.

## 14) Practical defaults (2025-ish)

- LLM/VLM pretraining: AdamW + warmup + decay + clipping.
- ViT training: AdamW with tuned weight decay and augmentation.
- CNN training: SGD + momentum + strong schedule.
- Diffusion/flow matching: Adam/AdamW with EMA often used.
- Try Muon when stability and scaling friction dominate.
- Try LARS/LAMB in extreme throughput-driven large-batch training.

## 15) Late-2025 to early-2026: conditioning-based wave

This section tracks the newest conditioning/preconditioning-heavy optimizer work after the 2025 baseline snapshot.

### 15.1 Matrix and tensor conditioning milestones

- Muon is Scalable for LLM Training (2025-02-24): practical scaling evidence for Muon-family conditioning.
  - Link: https://arxiv.org/abs/2502.16982
  - Evidence tags: `1B+`, `open-source impl`

- PolarGrad: matrix-gradient optimizers from a unifying preconditioning perspective (2025-05-27, revised 2026-02-05).
  - Link: https://arxiv.org/abs/2505.21799
  - Evidence tags: `theory`, `small-scale`

- NorMuon: neuron-wise normalized Muon, improving conditioning balance (2025-10-07).
  - Link: https://arxiv.org/abs/2510.05491
  - Evidence tags: `1B+`, `open-source impl`

- MARS-M: variance reduction plus matrix conditioning (2025-10-20).
  - Link: https://arxiv.org/abs/2510.21800
  - Evidence tags: `theory`, `small-scale`, `open-source impl`

- Hyperparameter Transfer Enables Consistent Gains of Matrix-Preconditioned Optimizers Across Scales (2025-12-05).
  - Link: https://arxiv.org/abs/2512.05620
  - Evidence tags: `1B+`, `scaling-law`, `protocol`

- Muon is Provably Faster with Momentum Variance Reduction (2025-12-18).
  - Link: https://arxiv.org/abs/2512.16598
  - Evidence tags: `theory`

- TEON: Tensorized Orthonormalization Beyond Layer-Wise Muon (2026-01-30).
  - Link: https://arxiv.org/abs/2601.23261
  - Evidence tags: `theory`, `1B-range`

- PRISM: adaptive computation of matrix functions for optimizer primitives (2026-01-29).
  - Link: https://arxiv.org/abs/2601.22137
  - Evidence tags: `systems`, `optimizer-primitive`

- MSign: stable-rank restoration for training stability (2026-02-02).
  - Link: https://arxiv.org/abs/2602.01734
  - Evidence tags: `stability`, `up-to-3B`

- ARO: Adaptively Rotated Optimization (2026-02-09).
  - Link: https://arxiv.org/abs/2602.09006
  - Evidence tags: `1B+`, `protocol`, `conditioning`

### 15.2 Conditioning taxonomy (for writing clarity)

- Layer-wise orthogonalization:
  Muon, NorMuon.

- Tensorized or cross-layer orthogonalization:
  TEON.

- Rotated-coordinate conditioning:
  ARO.

- Matrix preconditioners with scaling transfer:
  Shampoo/SOAP/Muon transfer rules (2512.05620).

- Conditioning + variance reduction hybrids:
  MARS-M, MVR-style Muon variants.

- Conditioning for stability restoration:
  MSign.

### 15.3 Evidence quality rubric (use this in comparisons)

When citing any new optimizer, label each claim with:

- `theory`: convergence or complexity result.
- `small-scale`: validated below ~1B parameters.
- `1B+`: demonstrated at >= 1B parameters.
- `open-source impl`: usable code exists.
- `independent replication`: separate team replication exists.
- `protocol`: paper provides controlled optimizer-comparison protocol.

### 15.4 Benchmark protocol for fair optimizer claims

For any benchmark table in the blog draft, require:

1. Same model architecture and tokenizer.
2. Same token budget and data ordering.
3. Same batch-size regime and precision setup.
4. Matched hyperparameter tuning budget per optimizer.
5. Report both wall-clock and token/FLOP efficiency to target loss.
6. Report instability/failure rate across seeds.

Rationale: recent 2025-2026 work shows many optimizer gains vanish under poor scaling transfer or unfair tuning budgets.

### 15.5 Community reports (non-peer-reviewed, separate from papers)

- Muon vs MuonClip vs Muon+AdamW (HF community, 2025-12-09):
  https://huggingface.co/blog/KingNish/optimizer-part1
- Reproducing and Validating Distributed Muon (HF community, 2025-12-12):
  https://huggingface.co/blog/bird-of-paradise/reproducing-and-validating-distributed-muon
- Scaling Is Not Plug-and-Play (HF community, 2026-01-04):
  https://huggingface.co/blog/bird-of-paradise/scaling-is-not-plug-and-play
