# The story of "How to Customize Agents, and When to Own Them"

The post's narrative arc as it reads on 2026-10-21, after the review rounds in the Claude Docs copy. A working note for keeping the story aligned. The full post is posts/20261016-customize-agents/index.qmd, and the 5-minute version, which tells this story in about 1,200 words, is posts/20261016-customize-agents-5min/index.qmd.

## The story

**The hook.** Agents are making headlines: CRESt's fuel-cell catalyst and OpenAI's agents settling Navier–Stokes. Yet the agent you bring to your own work keeps needing steering and says it is done when it is not. The difference is the check: both headline results could be checked automatically, by robots and by Lean, and each agent ran inside a system built around that check. Most business work has no such check, so you customize: context and tools, automated checks where the work allows them, people for the rest. Which customizations pay off, and when do you stop buying and start building? The post sorts the options into three layers, from the outside in.

**Act 1: connect.** You connect Claude Code or Codex to your tools, knowledge and instruction files, and set up review and governance. People get faster, but review becomes the bottleneck, and the business doesn't speed up: usage up 65%, throughput up 7.76%. The gains come from redesigning the work, as the randomized startup trial shows.

**Act 2: build.** To have an agent run part of a process on its own, Stripe and Ramp built their own. Building it covers the three paths and starting simple. Multi-agent setups are a sidebar, usually not worth it. Then reliability, told as one run: before the run (what the agent knows, asking for missing details), during it (wrong beliefs, plans, cost), when it says done (fake evidence, checking the claimed result, a second agent), across many runs (consistency, checks that are wrong) and keeping it secure (manipulation, monitoring, the Hugging Face incident). The Scale AI taxonomy opens the section, with a figure sorting its 41 kinds of failure by where they can be fixed. The act resolves with "Deciding how much to automate": the invoice-factoring case, from an agreed definition of a bad outcome, through replay, to a staged rollout with sign-off.

**Act 3: own the model.** Harness changes stop moving your eval. Hosting open weights comes first, and only a minority of teams do it yet. Whether to train is a long debate; it pays when the right answer is in your proprietary data. The author's extraction project shows fine-tuned 3B models beating the frontier model. A set of questions frames the decision, and the methods follow, matched to the signal you have: examples, an automatic check, or a stronger model.

**Epilogue.** Self-improvement hinges on its verifier: autoresearch works because the eval is read-only, and the author's prompt optimizer overfit. The eval is the lasting asset. "How to decide" gives a table of symptoms and a flowchart, and the closing asks you to decide how you will know the agent got it right before adding the next tool.

## What changed since the 2026-10-19 note

- The decision engine is no longer buried: "Deciding how much to automate" is its own section, built on the invoice-factoring case.
- Act 2's middle was reorganized from three lists (how it fails, preventing, catching) into one run, so it reads as a story rather than a handbook.
- Act 3 now resolves with a set of questions rather than "it depends on your data, your traffic and your budget."
- Cut: the five-mode failure taxonomy, the coverage worked example, the harness-learning example, and the summary paragraph after the flowchart.

## Still open

1. The reliability section still applies to any agent, off-the-shelf included, and it is the longest part of Act 2. The layer question pauses there.
2. The eval thread surfaces in the TL;DR, the reliability section, layer 3 and the closing, but the intro mentions it only once.
3. The 5-minute version follows the full post. When the full post changes, check the short one against it: every number, quote and link in the short version must come from the full post.
