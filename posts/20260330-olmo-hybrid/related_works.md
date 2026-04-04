---
listing: false
---

# From the 1960s Delta Rule to DeltaNet and Chunk-Parallel Training

## Purpose

This note connects the classical **delta rule** from the 1960s to modern **DeltaNet / Gated DeltaNet** style sequence models. It also consolidates the points from our discussion:

* why Gated DeltaNet is **linear-time** yet **sequential at autoregressive inference**,
* why standard attention is **quadratic in sequence length** yet highly **parallelizable**,
* how **DeltaNet training** can still be parallelized using **chunk-parallel** algorithms,
* and the detailed math of that chunkwise parallelism.

The goal is to show a conceptual line from:

1. the original **delta learning rule**,
2. to **online memory updates**,
3. to **fast-weight / linear-memory** views of sequence processing,
4. to **DeltaNet** as a modern recurrent sequence layer with efficient chunk-parallel training.

---

# 1. The 1960s: the delta rule

## 1.1 Historical role

The term **delta rule** is classically associated with early gradient-based learning for linear units and perceptron-like models. In modern notation, suppose we have an input vector

$$
x \in \mathbb{R}^d,
$$

a weight vector

$$
w \in \mathbb{R}^d,
$$

a scalar prediction

$$
\hat y = w^\top x,
$$

and a target

$$
y \in \mathbb{R}.
$$

Using squared error,

$$
\mathcal L = \frac{1}{2}(y - \hat y)^2,
$$

the gradient with respect to $w$ is

$$
\nabla_w \mathcal L
= -(y - \hat y)x.
$$

A gradient descent step gives

$$
w \leftarrow w - \eta \nabla_w \mathcal L
= w + \eta (y - \hat y)x,
$$

where $\eta > 0$ is the learning rate.

This is the **delta rule**:

$$
\Delta w = \eta (y - \hat y)x.
$$

The word “delta” refers to the error term

$$
\delta := y - \hat y.
$$

So the update is just

$$
\Delta w = \eta \delta x.
$$

## 1.2 Why it matters conceptually

This rule already contains the key pattern that will keep reappearing:

* there is a **current memory / parameter state**,
* a new example arrives,
* the system computes an **error or residual**,
* and the memory is updated by an **outer-product-like correction**.

Even though this is classical supervised learning rather than sequence modeling, the structural idea is important:

$$
\text{state} \leftarrow \text{state} + \text{correction based on residual and current input}.
$$

That line of thought later reappears in adaptive filters, online learning, associative memory, fast weights, linear attention, and DeltaNet.

---

# 2. A matrix-memory view of the delta rule

## 2.1 Scalar output, vector weights

The update

$$
w \leftarrow w + \eta(y - w^\top x)x
$$

can be interpreted as saying:

* $w$ stores what the model currently “believes,”
* the mismatch $y - w^\top x$ measures how wrong the memory is on the current key $x$,
* and the model patches memory in the direction of $x$.

## 2.2 From vector weights to associative memory

Now consider a matrix memory

$$
S \in \mathbb{R}^{d_v \times d_k}.
$$

Think of:

* a **key** $k \in \mathbb{R}^{d_k}$,
* a **value** $v \in \mathbb{R}^{d_v}$,
* and retrieval by

$$
\hat v = S k.
$$

A natural delta-rule-like correction is

$$
S \leftarrow S + \beta (v - Sk)k^\top,
$$

where $\beta$ is a step size or gate.

Expanding:

$$
S \leftarrow S + \beta v k^\top - \beta S k k^\top.
$$

Rearrange:

$$
S \leftarrow S(I - \beta k k^\top) + \beta v k^\top.
$$

This form is already extremely close to the modern DeltaNet update.

---

# 3. From online delta-style updates to sequence models

Suppose tokens arrive sequentially. For each token $t$, produce:

* a key $k_t \in \mathbb{R}^{d_k}$,
* a value $v_t \in \mathbb{R}^{d_v}$,
* a query $q_t \in \mathbb{R}^{d_k}$,
* and a scalar gate or learning rate $\beta_t$.

Maintain a recurrent memory state

$$
S_t \in \mathbb{R}^{d_v \times d_k}.
$$

A delta-style online memory update becomes

$$
S_t = S_{t-1} + \beta_t(v_t - S_{t-1}k_t)k_t^\top.
$$

Expanding gives

$$
S_t = S_{t-1} + \beta_t v_t k_t^\top - \beta_t S_{t-1} k_t k_t^\top,
$$

so

$$
S_t = S_{t-1}(I - \beta_t k_t k_t^\top) + \beta_t v_t k_t^\top.
$$

This is the core DeltaNet-style recurrence.

The token output is typically read via

$$
o_t = S_t q_t.
$$

This is the bridge from the old delta rule to modern recurrent sequence memory.

---

# 4. DeltaNet recurrence and interpretation

## 4.1 Sequential update

The main recurrent update is

$$
S_t = S_{t-1}(I - \beta_t k_t k_t^\top) + \beta_t v_t k_t^\top.
$$

Interpretation:

* $\beta_t v_t k_t^\top$ is a **write** to memory,
* $(I - \beta_t k_t k_t^\top)$ edits or partially erases memory along the direction $k_t$,
* the update is **online** and **stateful**.

This is a learned associative memory update, not just a simple sum.

## 4.2 Relation to the delta rule

Using the retrieval prediction

$$
\hat v_t = S_{t-1} k_t,
$$

the update can be rewritten as

$$
S_t = S_{t-1} + \beta_t (v_t - \hat v_t)k_t^\top.
$$

This is exactly the delta-rule structure:

$$
\text{new memory} = \text{old memory} + \text{learning rate} \times \text{residual} \times \text{key}^\top.
$$

So DeltaNet is not just vaguely inspired by the delta rule. In a precise matrix-memory sense, it **is** a delta-rule-like online memory update.

---

# 5. Comparison to attention

## 5.1 Standard softmax attention

For a sequence of length $L$, standard causal attention computes pairwise interactions between positions. In full prefill / training form, the main score matrix is

$$
QK^\top \in \mathbb{R}^{L \times L},
$$

so time and memory scale roughly as

$$
O(L^2)
$$

for full-sequence computation.

But this computation is highly parallelizable because the main operations are large batched matrix multiplies.

## 5.2 DeltaNet / Gated DeltaNet

DeltaNet-style recurrence has a different profile.

### Inference / autoregressive decoding

At decode step $t$, we update

$$
S_t = S_{t-1}(I - \beta_t k_t k_t^\top) + \beta_t v_t k_t^\top,
$$

then compute

$$
o_t = S_t q_t.
$$

This is **sequential over time** because step $t$ depends on $S_{t-1}$.

However, the state size does not grow with context length in the same way that attention’s KV cache does. So the recurrent state is fixed-size with respect to sequence length.

### Training / prefill

Naively, the recurrence is still sequential. But modern DeltaNet methods derive **chunk-parallel** algorithms so training can use large matrix multiplications within chunks.

So the correct comparison is:

* **attention:** quadratic in sequence length, but very parallel during training/prefill,
* **DeltaNet / Gated DeltaNet:** linear-style recurrent inference, sequential at decode, but training can be chunk-parallelized.

---

# 6. Why naive DeltaNet training is sequential

Suppose the sequence length is $L$. A direct forward pass computes

$$
S_1, S_2, \dots, S_L
$$

via

$$
S_t = S_{t-1}(I - \beta_t k_t k_t^\top) + \beta_t v_t k_t^\top.
$$

This creates a dependency chain

$$
S_1 \to S_2 \to \cdots \to S_L.
$$

A GPU does not like doing one tiny update after another for a long sequence. That is why naive recurrent training is inefficient on modern hardware.

---

# 7. Unrolling the recurrence

Let

$$
A_t := I - \beta_t k_t k_t^\top,
\qquad
B_t := \beta_t v_t k_t^\top.
$$

Then

$$
S_t = S_{t-1}A_t + B_t.
$$

Unrolling gives

$$
S_t = S_0 \Bigl(\prod_{j=1}^{t} A_j\Bigr)

* \sum_{i=1}^{t} B_i \Bigl(\prod_{j=i+1}^{t} A_j\Bigr).
  $$

If we ignore $S_0$ or absorb it into notation, a common form is

$$
S_t
===

\sum_{i=1}^{t}
\beta_i v_i k_i^\top
\left(
\prod_{j=i+1}^{t}
(I - \beta_j k_j k_j^\top)
\right).
$$

Interpretation:

* token $i$ writes a rank-1 memory piece,
* later tokens transform that contribution by a chain of transition matrices.

This is richer than pure linear attention, where the memory is just a sum of outer products.

---

# 8. Chunking the sequence

Let the sequence be partitioned into chunks of size $C$.

* chunk index: $[t]$,
* position inside the chunk: $r \in {1,\dots,C}$.

Define:

* $S[t]$: the memory entering chunk $t$,
* $S^r_{[t]}$: the state after processing the first $r$ positions inside chunk $t$.

The key chunk decomposition is

$$
S^r_{[t]} = S[t]P^r_{[t]} + H^r_{[t]}.
$$

This separates the within-chunk state into:

1. **carry-over from previous chunks**: $S[t]P^r_{[t]}$,
2. **new contribution from this chunk itself**: $H^r_{[t]}$.

---

# 9. Chunk-local transition and write terms

Define the within-chunk transition prefix

$$
P^r_{[t]} = \prod_{i=1}^{r} \bigl(I - \beta^i_{[t]} k^i_{[t]} k^{i\top}_{[t]}\bigr),
$$

and the within-chunk contribution

$$
H^r_{[t]} =
\sum_{i=1}^{r}
\left(
\beta^i_{[t]} v^i_{[t]} k^{i\top}*{[t]}
\prod*{j=i+1}^{r}
\bigl(I - \beta^j_{[t]} k^j_{[t]} k^{j\top}_{[t]}\bigr)
\right).
$$

Then

$$
S^r_{[t]} = S[t]P^r_{[t]} + H^r_{[t]}.
$$

At the end of the chunk,

$$
S[t+1] = S^C_{[t]} = S[t]P_{[t]} + H_{[t]},
$$

where

$$
P_{[t]} := P^C_{[t]},
\qquad
H_{[t]} := H^C_{[t]}.
$$

This means the full sequence-level dependence is now only across chunk boundaries:

$$
S[1] \to S[2] \to \cdots \to S[T],
$$

where $T = L/C$.

That is already a big reduction in sequential depth.

---

# 10. Why this still looks expensive

The formulas for $P^r_{[t]}$ and $H^r_{[t]}$ appear to involve full matrix products and sums of transformed outer products. If we materialized all of them directly for every prefix $r$, training would still be too expensive.

So the next step is to exploit the special rank-1 structure of the transition matrices.

---

# 11. Structured representation inside a chunk

DeltaNet uses the special form

$$
I - \beta_t k_t k_t^\top,
$$

which is a rank-1 modification of identity. Products of such matrices admit structured representations.

A useful chunkwise representation is

$$
P^r_{[t]} = I - \sum_{i=1}^{r} w^i_{[t]} k^{i\top}_{[t]},
$$

and

$$
H^r_{[t]} = \sum_{i=1}^{r} u^i_{[t]} k^{i\top}_{[t]}.
$$

The vectors $w^r_{[t]}$ and $u^r_{[t]}$ satisfy recurrences

$$
w^r_{[t]}
=========

\beta^r_{[t]}
\left(
k^r_{[t]}
---------

\sum_{i=1}^{r-1}
w^i_{[t]},(k^{i\top}*{[t]}k^r*{[t]})
\right),
$$

$$
u^r_{[t]}
=========

\beta^r_{[t]}
\left(
v^r_{[t]}
---------

\sum_{i=1}^{r-1}
u^i_{[t]},(k^{i\top}*{[t]}k^r*{[t]})
\right).
$$

These equations capture the entire within-chunk effect without explicitly storing full transition matrices for each prefix.

Conceptually:

* $W$ parameterizes how the chunk transforms incoming memory,
* $U$ parameterizes what the chunk writes.

---

# 12. Stack the chunk tensors

Define stacked matrices for chunk $[t]$:

$$
K_{[t]} =
\begin{bmatrix}
(k^1_{[t]})^\top \
\vdots \
(k^C_{[t]})^\top
\end{bmatrix}
\in \mathbb{R}^{C \times d_k},
$$

$$
Q_{[t]} =
\begin{bmatrix}
(q^1_{[t]})^\top \
\vdots \
(q^C_{[t]})^\top
\end{bmatrix}
\in \mathbb{R}^{C \times d_k},
$$

$$
W_{[t]} =
\begin{bmatrix}
(w^1_{[t]})^\top \
\vdots \
(w^C_{[t]})^\top
\end{bmatrix}
\in \mathbb{R}^{C \times d_k},
$$

$$
U_{[t]} =
\begin{bmatrix}
(u^1_{[t]})^\top \
\vdots \
(u^C_{[t]})^\top
\end{bmatrix}
\in \mathbb{R}^{C \times d_v}.
$$

Exact row/column conventions can vary across papers and implementations, but the core point is the same: chunk-local effects are collected into dense matrices amenable to batched linear algebra.

---

# 13. Chunk boundary update in matrix form

At chunk end,

$$
S[t+1] = S[t]P_{[t]} + H_{[t]}.
$$

Using structured forms for $P_{[t]}$ and $H_{[t]}$, one arrives at the hardware-friendly update

$$
S[t+1]
======

S[t] + \bigl(U_{[t]} - W_{[t]}S[t]^\top\bigr)^\top K_{[t]}.
$$

Interpretation:

* $W_{[t]}S[t]^\top$ describes how the chunk interacts with incoming memory,
* subtracting it from $U_{[t]}$ gives the chunk’s net transformed write,
* multiplying by $K_{[t]}$ projects that write into the memory space.

This is much more GPU-friendly than token-by-token recurrence.

---

# 14. Chunk output computation

For each position $r$ in chunk $[t]$,

$$
o^r_{[t]} = S^r_{[t]} q^r_{[t]}.
$$

Stacking all outputs in the chunk gives a matrix formula of the form

$$
O_{[t]}
=======

Q_{[t]}S[t]^\top
+
\bigl(Q_{[t]}K_{[t]}^\top \odot M\bigr)
\bigl(U_{[t]} - W_{[t]}S[t]^\top\bigr),
$$

where:

* $O_{[t]}$ stacks chunk outputs,
* $M$ is a causal lower-triangular mask / coefficient structure,
* $\odot$ is elementwise multiplication.

The important point is not the exact masking convention, but the computational pattern:

* compute dense matrices like $Q_{[t]}K_{[t]}^\top$,
* combine them with chunk-local factors,
* produce all outputs in the chunk together.

That is where most of the parallel training efficiency comes from.

---

# 15. Where the parallelism is, exactly

Chunk-parallel training is **not** the same as full attention-style parallelism over the whole sequence.

Instead:

## 15.1 Parallel inside a chunk

Within one chunk, many computations are expressed as dense matrix multiplies. So the chunk’s outputs and transition effects can be computed in parallel.

## 15.2 Sequential across chunks

But chunk $[t+1]$ still depends on the boundary state from chunk $[t]$:

$$
S[t+1] = S[t]P_{[t]} + H_{[t]}.
$$

So the model still has a chunk-level scan dependency.

In dependency-graph terms:

* naive recurrence depth: $L$,
* chunked recurrence depth: $T = L/C$.

Thus chunking reduces sequential depth by a factor of roughly $C$.

---

# 16. Relation to linear attention

Linear attention usually maintains an additive memory such as

$$
M_t = M_{t-1} + \phi(k_t) v_t^\top,
$$

with output

$$
o_t \approx \phi(q_t)^\top M_t.
$$

That is simpler because the state is just a running sum.

DeltaNet is more expressive because it does not merely add new outer products. It also **edits previous memory** through

$$
I - \beta_t k_t k_t^\top.
$$

That extra expressiveness is why the math is more complicated and why special structured chunk algorithms are needed.

---

# 17. Relation to Gated DeltaNet

Gated DeltaNet keeps the same general recurrent-memory flavor but introduces additional gating / normalization refinements to improve optimization and expressiveness.

The main conceptual points from our discussion remain:

* it is **linear-style recurrent** rather than full quadratic attention,
* **autoregressive inference is sequential** because the recurrent state must be updated token by token,
* **training can still be chunk-parallelized** by extending the same chunkwise decomposition ideas.

So the right mental model is:

* **attention:** quadratic but highly parallel during training/prefill,
* **Gated DeltaNet:** recurrent and linear-style at inference, sequential at decode, but trainable efficiently with chunk-parallel algorithms.

---

# 18. The exact answer to the earlier comparison question

The earlier comparison can be stated precisely as follows.

## 18.1 “Gated DeltaNet is linear, but sequential”

Broadly yes, with an important nuance.

* At **autoregressive inference time**, Gated DeltaNet is naturally sequential over time because

$$
S_t \text{ depends on } S_{t-1}.
$$

* But during **training**, modern implementations do not simply run a full token-by-token scan. They derive chunk-parallel algorithms that recover much of the hardware efficiency of large batched matrix multiplication.

So it is wrong to say “DeltaNet training is purely sequential.” It is better to say:

> DeltaNet / Gated DeltaNet is recurrent and sequential at decode time, but training can be substantially parallelized using chunkwise formulations.

## 18.2 “Attention is quadratic, but parallelizable”

Also broadly yes.

* Full attention computes interactions across pairs of positions, giving roughly

$$
O(L^2)
$$

sequence-length scaling in standard form.

* But those operations are large dense matrix multiplies, which GPUs handle extremely well.

That is why attention often trains very efficiently despite its quadratic scaling.

---

# 19. A compact derivation from delta rule to DeltaNet

Start with vector delta rule:

$$
\Delta w = \eta(y - w^\top x)x.
$$

Lift from vector weights to matrix memory:

$$
\hat v = Sk,
$$

$$
S \leftarrow S + \beta(v - Sk)k^\top.
$$

Expand:

$$
S \leftarrow S + \beta vk^\top - \beta Skk^\top.
$$

Factor:

$$
S \leftarrow S(I - \beta kk^\top) + \beta vk^\top.
$$

Index by time:

$$
S_t = S_{t-1}(I - \beta_t k_t k_t^\top) + \beta_t v_t k_t^\top.
$$

Define output readout:

$$
o_t = S_t q_t.
$$

Then chunk it:

$$
S^r_{[t]} = S[t]P^r_{[t]} + H^r_{[t]}.
$$

Use structured representation:

$$
P^r_{[t]} = I - \sum_{i=1}^r w^i_{[t]}k^{i\top}*{[t]},
\qquad
H^r*{[t]} = \sum_{i=1}^r u^i_{[t]}k^{i\top}_{[t]}.
$$

Get chunk-end update:

$$
S[t+1]
======

S[t] + \bigl(U_{[t]} - W_{[t]}S[t]^\top\bigr)^\top K_{[t]}.
$$

Get chunk outputs:

$$
O_{[t]}
=======

Q_{[t]}S[t]^\top
+
\bigl(Q_{[t]}K_{[t]}^\top \odot M\bigr)
\bigl(U_{[t]} - W_{[t]}S[t]^\top\bigr).
$$

That is the conceptual pipeline from 1960s delta-rule learning to modern chunk-parallel DeltaNet training.

---

# 20. Pseudocode view

```python
# inputs per token: q_t, k_t, v_t, beta_t
# recurrent memory: S

for each chunk [t]:
    # 1. from chunk-local keys/values/gates, construct structured factors
    #    U_[t], W_[t], K_[t], Q_[t]

    # 2. compute all outputs in the chunk together
    O_[t] = Q_[t] @ S.T + ((Q_[t] @ K_[t].T) * M) @ (U_[t] - W_[t] @ S.T)

    # 3. update chunk boundary state
    S = S + (U_[t] - W_[t] @ S.T).T @ K_[t]
```

This is only schematic, but it captures the main training pattern:

* large chunkwise matrix ops inside a chunk,
* recurrent scan only across chunk boundaries.

---

# 21. Practical intuition

A useful way to think about DeltaNet memory is:

* attention stores the past implicitly in a growing KV cache and rereads it,
* DeltaNet stores the past in an evolving fixed-size state and edits that state online.

The transition

$$
I - \beta_t k_t k_t^\top
$$

lets each token partly reshape what memory means for future retrievals.

So DeltaNet behaves less like “just accumulate features” and more like “perform online error-correcting edits to an associative memory.”

That is exactly why the delta-rule ancestry is more than a naming coincidence.

---

# 22. Final summary

## 22.1 Historical thread

* The **delta rule** updates parameters by correcting the current prediction error.
* A matrix-memory version becomes

$$
S \leftarrow S + \beta(v - Sk)k^\top.
$$

* Expanding yields

$$
S \leftarrow S(I - \beta kk^\top) + \beta vk^\top,
$$

which is the core DeltaNet-style recurrence.

## 22.2 Architectural thread

* **Standard attention** is quadratic in sequence length but highly parallelizable.
* **DeltaNet / Gated DeltaNet** uses recurrent fixed-size memory, so decode is sequential, but training can be parallelized chunkwise.

## 22.3 Chunk-parallel training thread

* Split sequence into chunks.
* Write within-chunk state as

$$
S^r_{[t]} = S[t]P^r_{[t]} + H^r_{[t]}.
$$

* Represent $P^r_{[t]}$ and $H^r_{[t]}$ in structured low-rank form.
* Compute chunk outputs and chunk-end updates with dense matrix multiplies.
* Scan only across chunk boundaries.

That is the essence of chunk-parallel DeltaNet training.

---

# 23. Short glossary

* **delta rule**: gradient-based correction proportional to prediction error.
* **associative memory**: a memory that maps keys to values.
* **outer product**: for vectors $a,b$, the matrix $ab^\top$.
* **recurrent state**: a persistent state updated token by token.
* **chunk-parallel**: parallel inside chunks, sequential across chunk boundaries.
* **KV cache**: attention’s stored past keys and values used at autoregressive decoding.

---

# 24. One-sentence answer

DeltaNet can be viewed as a modern sequence-model realization of a matrix-valued delta rule:

$$
S_t = S_{t-1} + \beta_t(v_t - S_{t-1}k_t)k_t^\top,
$$

and chunk-parallel training works by decomposing within-chunk computation into structured matrix forms so that most work becomes batched matmuls while only chunk boundaries remain sequential.

