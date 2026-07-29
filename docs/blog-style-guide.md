# Blog Style Guide

This blog is about practical AI, engineering, and life. The strongest posts read like notes from an experienced builder: clear thesis, concrete examples, enough technical depth to be useful, and honest discussion of where systems fail.

Use published posts as the primary reference for style. Drafts may contain useful ideas, but they are often less polished and should not set the tone by themselves.

## Topic Fit

Good topics usually fall into one of these lanes:

- Applied AI systems: Document AI, MCP, MLOps, deployment, security, evaluation, and production reliability.
- Model and training practice: optimizers, LLM architectures, video generation, scaling laws, efficient training, and cost-quality tradeoffs.
- Computer vision and multimodal workflows: reproducible demos, model comparisons, sports/media analysis, document understanding, and visual pipelines.
- Agents and automation: coding agents, ML automation, tool use, causal inference agents, and enterprise integration.
- AI in society and life: sustainability, education, career advice, civic access to AI, and policy, grounded in practical consequences.

A topic is a strong fit when it answers at least one of these questions:

- What did I build, test, deploy, or reproduce?
- What changed in the field, and what does it mean for practitioners?
- What bottleneck moved rather than disappeared?
- What should a technical team do differently after reading this?

Avoid posts that are only news summaries, broad hype, or abstract opinion without implementation detail, evidence, or decision guidance.

## Audience

Write for technical builders and AI-adjacent decision makers:

- ML engineers, software engineers, data scientists, founders, consultants, and product-minded technical leaders.
- Readers who know the AI vocabulary but appreciate careful explanations of unfamiliar mechanisms.
- Readers who want practical judgment, not just a literature survey.

Assume the reader is smart but busy. Give them the conclusion early, then make the reasoning defensible.

## Article Shape

Most strong posts should use this structure:

1. State the practical problem or field shift in the opening paragraphs.
2. Give a short thesis: what the post will explain and why it matters.
3. Include a TL;DR, executive summary, or compact decision table for longer posts.
4. Build from mental model to concrete examples.
5. Show evidence: experiments, metrics, code, diagrams, repo links, model numbers, cost estimates, or failure cases.
6. Explain tradeoffs and limits.
7. End with practical guidance: what to try first, when to deviate, what to watch next.

Good recurring section patterns:

- `## TL;DR`
- `## Mental model`
- `## What the business actually needed`
- `## Pattern selection matrix`
- `## What I learned`
- `## If I were starting today`
- `## What this means for the field`
- `## Closing`

Do not overuse numbered sections unless the post is explicitly a survey or playbook. Prefer descriptive headings that tell the reader what the section is doing.

## Voice

The house voice is pragmatic, first-person, and technically grounded.

Prefer:

- "I tried this on a smaller setup..."
- "The bottleneck moved from X to Y."
- "This worked on the demo, but failed when..."
- "In practice, the metric that mattered was..."
- "I would start with..."

Avoid:

- Marketing language.
- Empty futurism.
- Overconfident predictions without caveats.
- Dense academic prose when a practical explanation would work.
- Chatty filler that does not add technical or judgment value.

It is fine to use first person. The best posts make the author visible as someone who has built, debugged, compared, or thought through the system.

## Technical Depth

Aim for enough detail that a motivated reader could reproduce the result or make a better decision.

Use:

- Code snippets for runnable mechanics.
- Tables for tradeoff comparisons, recipes, rollout phases, and model results.
- Diagrams or images when architecture, workflow, or geometry matters.
- Metrics with context: accuracy, mAP, log loss, GPU hours, latency, memory, token count, cost, or operational risk.
- Links to papers, repos, datasets, model cards, and experiment logs.

When covering papers, translate the math into the practical implication. Equations are welcome when they clarify the mechanism, but each equation should earn its place.

When covering production systems, discuss evaluation, failure modes, security, data quality, and human fallback. The recurring thesis is that strong AI systems are composed systems, not magic single-model replacements.

## Formatting Conventions

Use Quarto Markdown consistently:

- YAML front matter with `title`, `date`, and `categories`.
- Add `format.html.toc: true` and `toc-depth: 2` for longer technical posts.
- Use callouts for compact summaries or practical notes.
- Use fenced code blocks with language tags where possible.
- Prefer local assets inside the post directory for images, videos, diagrams, and generated figures.
- Keep image captions concrete. Say what the reader should notice.
- Use tables when comparing patterns, methods, recipes, phases, or results.

Category names should be lowercase unless they are proper nouns. Prefer stable categories such as:

- `ai`
- `llm`
- `computer vision`
- `generative ai`
- `deep learning`
- `ml systems`
- `architecture`
- `security`
- `deployment`
- `optimization`
- `document ai`
- `coding agents`
- `data science`

## Evidence Standard

A post should make clear which claims come from:

- Personal project experience.
- A reproduced demo or experiment.
- A cited paper or benchmark.
- A public model/repo/dataset.
- Inference or opinion.

Do not blur benchmarks with production readiness. A recurring blog theme is that a model can look strong on a clean task and still fail in messy workflows.

For rapidly changing topics, include dates or timeframe markers such as "by early 2026" or "as of this post." This keeps claims auditable later.

## Preferred Endings

Endings should leave the reader with judgment, not just a recap.

Strong endings usually answer:

- What would I do first?
- What is still unsolved?
- Which tradeoff matters most?
- What should readers watch next?

Examples of good closing moves:

- A practical starter recipe.
- A short list of open questions.
- A warning about a common failure mode.
- A sober prediction tied to evidence.

## Editing Checklist

Before publishing, check:

- The opening names a real problem, not just a topic.
- The thesis appears in the first few paragraphs.
- Long posts include a TL;DR, executive summary, or decision table.
- Every major section advances the argument.
- Claims are backed by experience, metrics, citations, or clearly labeled judgment.
- Failure modes and limitations are explicit.
- Code, commands, or repo links are runnable or clearly illustrative.
- Images and tables clarify rather than decorate.
- The conclusion gives practical guidance.
- The title is specific enough to signal the post's value.

