# The story of "How to Customize Agents, and When to Own Them"

The post's narrative arc as it reads on 2026-10-19, after the opening rewrite. A working note for aligning the story; the post itself is posts/20261016-customize-agents/index.qmd.

## The story

**The hook.** Agents are making headlines: a better fuel-cell catalyst, a solved Erdős problem, a Millennium Prize proof. Yet the off-the-shelf agent you bring to your own work misreads your data and claims success on tasks it has not finished. The difference is that each headline agent ran a strong model inside a system built for its one problem, with a reliable verifier: robots that made and tested the catalysts, a proof checker that verified the proofs. You can build that kind of system around your own agent, but it has many moving parts. Which ones pay off? When should you stop buying and start building, first the agent and then the model? The post follows three layers from the outside in, and asks those two questions at each step. Your own eval, your version of the headline agents' verifier, answers them.

**Act 1: buy.** You start with Claude Code or Codex and connect it: MCP servers, company knowledge, instruction files, review and governance. Then the twist: people get faster, but the business doesn't. Usage rises 65% while throughput rises 8%. The work moved downstream, and the time saved went nowhere. The gains come from redesigning the work, as the randomized startup trial shows. Some companies outgrow the off-the-shelf agent.

**Act 2: build.** To automate a whole process, Stripe and Ramp built their own agents, and owning one gives you control of five parts. The limit is how much of the work you can hand the agent, a trade between silent errors and escalations to a person. Then the act becomes a handbook: how to build it (start simple, eval-driven), whether to use a team of agents (usually not), the five ways it fails, how to prevent failures (most start from a wrong picture of the task), and how to catch them (don't trust the agent's own account, and your checks can be wrong too). Deep in Catching failures comes the worked example: the same agent's best setting moves from 90% coverage to none, depending on what one silent error costs. Security and the Hugging Face incident end the act.

**Act 3: own the model.** Harness changes stop moving your eval. You can host open weights, which few teams do, or train, which is a live debate. Then the author's project: fine-tuned 3B models beat the frontier model on nested-schema document extraction, because "fine-tuning bought the output contract." Then a reference catalog of training methods.

**Epilogue.** Self-improvement is limited by its verifier and overfits, as the author's prompt optimizer did. The lasting asset is your eval. A diagnostic table, then the closing: build the check first.

## Where the story breaks

1. **Act 2's middle tells a different story.** How it fails, Preventing and Catching form a reliability handbook that applies to any agent, off-the-shelf included. For about 40% of the post, the reader loses the buy, build, own question the intro promises to ask at every step.
2. **The decision engine is buried.** Act 2 states its limit early, how much to hand the agent, and the worked example is the answer. But it sits as one item inside Catching failures, after the court cases.
3. **The eval thread is promised but surfaces unevenly.** It appears in Building it and in Act 3's first line. The climax ("the lasting asset is an eval") lands inside the self-improvement section, which is framed as a look ahead rather than as the payoff.
4. **Act 3 resolves, then becomes an appendix.** "So the answer depends on your data, your traffic and your budget" is the resolution. The six paragraphs of training methods after it read as reference material.
5. **The intro and the closing promise different things.** The closing names three takeaways: sort by what you own, set autonomy by error cost, let the eval decide. The intro sets up only the first and third.

## An unannounced protagonist

The author's document-extraction work appears at every stage, always described generically:

- Act 2: token costs and schema compaction.
- The worked example: legal forms.
- Act 3: the fine-tune that beat the frontier model.
- The epilogue: the prompt optimizer that overfit.
- The closing: the list of failures.

If the intro said "I'll follow one kind of work through all three layers," these passages would read as chapters instead of scattered examples.

## Open question

Is this one story, how far to customize (buy, build, own), with reliability as what you must get right before going deeper? Or two stories: where to customize, and how to make agents reliable? The answer decides how Act 2 is reorganized.
