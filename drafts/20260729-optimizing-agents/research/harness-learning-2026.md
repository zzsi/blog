# Harness learning: training a model to revise an agent's harness

Notes for "How to Customize Agents, and When to Own Them". Read 2026-10-12.

- **Paper:** Zhang, Liu, Wang, Tajwar, Arora, Salakhutdinov, Khashabi, Song and Zanette, "Harness Learning Enables Generalizable Test-Time Adaptation", arXiv 2609.35738, v1 September 28, 2026. https://arxiv.org/abs/2609.35738
- **Status:** preprint, not peer reviewed. I read the main text and checked the numbers below against its tables (Tables 9 and 23, Appendix B.1).

## What they did

- The harness is defined as "the executable program that organizes model calls, tool use, and information flow". That matches the article's 1.2 and the Stanford Meta-Harness definition.
- Two models:
  - a **solver**, which answers the questions and stays frozen;
  - a **proposer**, which reads the task description, the current harness code and a report of how it did, and writes a code edit to the harness.
- They train the proposer with RL (GRPO). The reward is the score of the edited harness on a set of scoring questions, plus a small bonus for edits that parse and run.
- At test time both models are frozen. Only the harness code changes, round after round, using feedback from each run.
- Questions are split three ways, all disjoint: feedback questions build the report, scoring questions pick which edit to keep, and held-out questions measure the result.
- **Models:** small ones. On Reasoning Gym, the proposer and solver are both Qwen3.5-4B, with supervised examples from a 35B teacher. On multi-hop QA, a Qwen3-4B proposer revises the harness for a Qwen3-8B solver.
- **Tasks:**
  - Reasoning Gym puzzles (mazes, sudoku, arithmetic and so on), starting from a harness that calls the model once.
  - Multi-hop question answering, starting from an existing two-hop retrieval workflow. They train on HotpotQA and test on MuSiQue and 2WikiMultihopQA.

## Results

1. **Learned revisions transfer to unseen tasks.**
   - On 21 puzzle families the proposer never trained on, the average single revision scored 0.32 before training and 0.62 after SFT plus RL.
   - Over all 26 unseen families, including five hard ones they set aside, the average went from 0.28 to 0.53.
2. **A trained 4B proposer beat its 35B teacher on average,** 0.62 against 0.56. The teacher still did better when you take the best of its eight tries (0.85 against 0.83).
3. **Revising the current best harness beat drawing many independent tries.**
   - On MuSiQue, an unseen QA benchmark, independent revisions averaged 0.15 exact match. The seed harness scored 0.14.
   - Ten rounds of revising the kept harness reached 0.27.
   - With the same 80 proposals, the iterative runs beat even the best of 80 independent ones. The authors note that this "leaves total compute and feedback unmatched".
4. **Training on revision sequences did not reliably beat training on single revisions.** A proposer trained only on one-step edits kept improving harnesses over many rounds anyway.
5. **Training mostly cut broken proposals,** meaning edits that fail to run or score zero. Most of that reduction came from RL; SFT alone left it nearly unchanged.

## Caveats that matter

- **A plain, fixed harness did better than the average learned edit.** The paper's baseline gives the model Python execution for up to five turns, and is the same for every task. On the 21 unseen families it scored 0.69, above the trained proposer's average single revision (0.62). The proposer beats it only when you pick the best of eight edits by held-out score (0.83), and that selection is an oracle, not something you could do in production. The gain therefore depends on selection, and selection depends on a reliable check.
- **Some evaluation families were chosen using earlier results.** For the multi-round tests, six of the extra families were picked partly because the RL proposer had already done well on them (Table 12).
- **The tasks are small:** synthetic puzzles and short QA, run with 4B to 8B models. The authors list long tool-use trajectories as future work.
- **There is a grader with a clean score for every task.** Most business tasks have nothing so neat.

## What the learned edits did

- **Puzzles:** most edits added an interpreter loop, so the model writes code and the runtime executes it. That is the same structure as the fixed baseline that beat the average edit.
- **QA:**
  - The common good edit kept summaries for deciding the next search, but passed the raw retrieved passages to the call that writes the answer.
  - Other edits added a third retrieval hop, or searched again when the draft answer did not appear in the passages.
  - The untrained proposer sometimes collapsed the harness to a single model call or removed the solver entirely.
- **When the proposer was asked to add helper tools,** they often failed at the joins: parsing the question, passing data to and from the tool, or pulling out the answer. Even when the helper's own algorithm was correct, "a generated component contributes only when these interfaces also work."

## Learnings for practitioners

1. **The check does most of the work.** Average proposals were mediocre; kept-if-better and best-of-N selection produced the gains. Without a trustworthy score on held-out work, automated harness tuning has nothing to stand on. This supports 10.3 and 10.6.
2. **Iterate on the current best and keep a change only if it scores higher.** That beat sampling many independent changes for the same number of proposals. The same keep-if-better rule appears in Karpathy's autoresearch (10.1).
3. **Try the boring harness first.** A generic "let the model run code for a few turns" harness was a strong baseline. Measure any tuned harness against it.
4. **Most harness failures happen at the interfaces between components,** not inside them. This matches the Scale AI taxonomy's "a tool wrapper garbles data in transit" (§6 figure).
5. **For one narrow skill, a small model trained on outcomes can match or beat a much larger general model.** This is another 2026 data point for post-training small models (§9), though in a lab setting.
6. **Training the reviser, rather than searching separately for each task, is one answer to the overfitting in 10.3.** The paper tested transfer to unseen tasks directly, which is what the RRSI result says per-task harness evolution lacks.

## Fit with the article

- **Best fit: 10.3,** as the counterpoint to per-task overfitting. Added to 10.3 on 2026-10-12, reworded as: "A 2026 preprint took another route and trained a small model to revise harnesses, and its edits carried over to tasks it never trained on. But its average edit still scored below a plain harness that just lets the model run code. It pulled ahead only when the best edits were picked by score." First draft:

  > "One 2026 preprint trained a small model to revise harnesses, and its edits carried over to tasks it never trained on. But the average edit still scored below a plain harness that just lets the model run code, and the gains came from keeping only the edits that scored higher."

- **Optional, 10.2:** a reference showing self-improvement research that rewrites the harness rather than the weights.
- **Not needed elsewhere.** The article already has Meta-Harness, RRSI and autoresearch for this ground. This paper adds the transfer result and a sober baseline comparison.

## Related 2026 work cited by the paper (not checked)

- Harness-R1 (arXiv 2608.02276): a similar training recipe.
- Meta-Harness (arXiv 2603.28052): already used in the article for the harness definition.
- AutoHarness (arXiv 2603.03329).
- TTHE: Test-time harness evolution (arXiv 2607.08124).
- "Harness Updating Is Not Harness Benefit" (arXiv 2605.30621).
- Whale: joint harness-weight optimisation (arXiv 2609.00196).
- Evo-Bench, on whether language models can improve agent harnesses (arXiv 2608.09096).
