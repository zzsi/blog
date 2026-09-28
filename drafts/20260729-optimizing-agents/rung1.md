# Rung 1: what companies actually do around vendor agents

Research round, 2026-09-28. Tags: **[PRIMARY]** read at source, **[SECONDARY]** coverage only. Three pages returned 403: OpenAI's Codex GA post, Pinterest's Medium post, Bain's 2025 report.

## Practices, ranked by how often they appear in 10 named company reports plus the Microsoft study

This is a count within a sample, not a survey.

| Rank | Practice | Companies | Reported impact |
|---|---|---|---|
| 1 | Internal MCP servers behind a gateway or registry | Stripe, LinkedIn, Pinterest, Spotify, Intercom, Uber, Cloudflare | High. 2026 twist: full tool schemas eat context, so large users expose tools as CLI commands, "code mode" or tool search |
| 2 | Repo instruction files (AGENTS.md, CLAUDE.md, Cursor rules), often generated and kept current by jobs | Stripe, Intercom, Cloudflare, OpenAI; GitHub and Vercel studies | Mixed: strong in vendor evals, null in the independent ETH study |
| 3 | AI code review in CI on every PR | Uber, Cloudflare, Anthropic, OpenAI | Best measured, consistently positive |
| 4 | Governance: central auth, audit, permission policy, cost controls | Uber, Cloudflare, Pinterest, Intercom | Reported as cost and safety, not productivity |
| 5 | Skills and playbooks | LinkedIn, Intercom, Uber, Cloudflare | Large adoption; Vercel finds skills often never get invoked |
| 6 | Telemetry on agent use | Intercom, Uber, LinkedIn, Pinterest | Makes measurement possible |
| 7 | Scheduled jobs that build agent-readable context | Intercom, Cloudflare, Uber, LinkedIn | Anecdotal |
| 8 | Sandboxed or cloud dev environments | Stripe, Cloudflare, Uber | Enabling infrastructure |
| 9 | Enablement: workshops, peer spread, zero-touch setup | Booking.com, Microsoft, Cloudflare | Microsoft: peer exposure is the strongest adoption predictor |
| 10 | Slack or ticket triggers | Stripe, Spotify (both for home-built agents) | No isolated figure |

**The author's two examples hold up.** MCP over internal services is the most common practice; scheduled context-building jobs appear four times.

## Company evidence

- **LinkedIn CAPT**, Jan 27 2026. MCP plus 500+ executable playbooks for coding agents including Copilot; 1,000+ engineers. "Issue triage time has dropped by about 70% in many areas"; data analysis "roughly three times faster." Self-reported, hedged. https://www.linkedin.com/blog/engineering/ai/contextual-agent-playbooks-and-tools-how-linkedin-gave-ai-coding-agents-organizational-context **[PRIMARY]** — the clearest combination of both author examples, with numbers.
- **Uber**, Aug 27 2026. One gateway over "more than 1,000 MCP servers"; loading all schemas cost "approximately 50K-70K tokens" per session, so tools moved to CLI commands and tool search. 3,600+ skills, 30K+ skill executions a day, "more than 70% of pull requests" attributed to agents. Cost controls: live counter, nudges at 50/80/100% of expected spend, compaction at 400K tokens, reasoning effort defaulted to Medium, cost per merged PR tracked. Spend "relatively stabilized since April" while weekly users grew 7x. https://www.uber.com/us/en/blog/efficient-software-factory/ **[PRIMARY]**
- **Uber uReview**, Aug 2025. Reviews 90%+ of ~65,000 weekly diffs; 75% of comments marked useful, 65%+ addressed. https://www.uber.com/us/en/blog/ureview/ **[PRIMARY]**
- **Cloudflare**, Apr 20 2026. AGENTS.md generated for ~3,900 repos from Backstage metadata, sent as merge requests for teams to review. MCP portal: 13 servers, 182+ tools; the GitLab server's 34 tools (~15,000 tokens) collapsed into two code-mode tools. One-command setup, "no API keys exist on user machines," 93% adoption; weekly MRs ~5,600 to 8,700+. https://blog.cloudflare.com/internal-ai-engineering-stack/ **[PRIMARY]** AI reviewer: 131,246 runs on 48,095 MRs, $1.19 average, median 3m39s. https://blog.cloudflare.com/ai-code-review/ **[PRIMARY]**
- **Intercom**, Mar 19 2026. Claude Code as an internal platform: 13 plugins, 100+ skills, hooks. A permission hook classifies Bash commands GREEN/YELLOW/RED from 14 days of transcripts; a read-replica Admin Tools MCP with blocked tables and an audit trail; telemetry to Honeycomb; "a weekly GitHub Action job that fact checks and updates all CLAUDE.md" files; a session-end hook that files issues for gaps. Top users of the production console "weren't engineers." https://ideas.fin.ai/p/how-we-use-claude-code-today-at-intercom **[PRIMARY]** — the fullest public example of governance plus scheduled knowledge upkeep around a vendor agent.
- **Spotify**, Jun 3 2026. Backstage exposed as MCP and CLI. 99%+ weekly use; "76% increase in pull request frequency"; also "76% more PRs to review," and "the bottleneck moves from coding to decision-making." https://engineering.atspotify.com/2026/6/code-with-claude-coding-is-no-longer-the-constraint **[PRIMARY]**
- **Stripe**, Feb 2026. Cursor rules synced into a format Claude Code reads; Toolshed MCP with "nearly 500 MCP tools" (Part 2; Part 1 said 400+). https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2 **[PRIMARY]**
- **Pinterest**. MCP registry as governance: only registered servers in production, JWT, human approval for sensitive operations; ~66,000 invocations and ~7,000 hours saved a month, owner-estimated. https://www.infoq.com/news/2026/04/pinterest-mcp-ecosystem **[SECONDARY]**
- **Anthropic**, Mar 9 2026. PRs with substantive review comments 16% to 54%; "Code output per Anthropic engineer has grown 200% in the last year." https://claude.com/blog/code-review **[PRIMARY, vendor]**
- **OpenAI**, Jul 20 2026. Custom AGENTS.md review rules recovered 98% of required findings vs 58.3% baseline; weekly PR volume "more than doubled since Q4." https://developers.openai.com/blog/custom-code-review-rules-for-codex **[PRIMARY, vendor]**

## Do instruction files work? Mixed

- **Vercel**, Jan 2026: an 8KB docs index in AGENTS.md scored 100% on its evals vs 53% baseline; skills were never invoked in 56% of cases. https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals **[PRIMARY]**
- **ETH Zurich**, arXiv 2602.11988, Feb 2026: context files "do not generally improve task success rates, while increasing inference cost by over 20% on average." https://arxiv.org/abs/2602.11988 **[PRIMARY]**
- **SMU**, arXiv 2601.20404: AGENTS.md associated with 28.64% lower median runtime and 16.58% fewer output tokens at comparable completion. **[SECONDARY]**
- **GitHub**, Nov 2025, from 2,500+ agents.md files: specific persona, exact commands early, code examples, three-tier boundaries (always / ask first / never). https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/ **[PRIMARY]**

**Reading:** the most common rung 1 practice has the weakest independent evidence. Instruction files help most for non-standard conventions, and for cost and speed more than correctness.

## Instruction files and skills across model releases (research round 2026-09-28)

**Verdict on the author's recollection:** the author recalled that Fable needs much simpler CLAUDE.md files and skills. That is **partly right but misattributed**.
- Anthropic's "too prescriptive" guidance is for **Fable 5** (released June 9 2026), and it is about **skills**, not CLAUDE.md.
- For **Fable 5.1** (Sept 1 2026) Anthropic says Fable 5 prompts "should perform well on Claude Fable 5.1 without changes." Only a few narrow removals are listed, such as lines telling the model to hold back progress updates.
- Anthropic's CLAUDE.md advice about model releases is generic and predates Fable.

**The general point is well supported, but almost entirely by vendors:** re-check instruction files and skills at each model generation. **[PRIMARY]** throughout; I checked the quotes marked ✓ against the saved copies.

- **Anthropic**
  - Prompting Claude Fable 5 (docs, undated): "Skills developed for prior models are often too prescriptive for Claude Fable 5 and can degrade output quality. Review and consider removing older instructions if default performance is better." ✓
  - "How Claude Code works in large codebases" (May 14 2026): "CLAUDE.md files that guided Claude through patterns it used to struggle with may either become unnecessary or actively constraining when the next model ships." It recommends "a meaningful configuration review every three to six months, but it's also worth doing one whenever performance feels like it's plateaued after major model releases." ✓
  - Claude Code docs: "Revisit after major model releases." Claude Code v2.1.283 (Sept 25 2026) added `/doctor prompt-audit` "to audit your CLAUDE.md files, skills, agents and commands for prompting patterns written for older models."
  - Prompting best practices, on Opus 4.5 and 4.6: "If your prompts were designed to reduce undertriggering on tools or skills, these models may now overtrigger… Where you might have said 'CRITICAL: You MUST use this tool when...', you can use more normal prompting."
  - Prompting Claude Opus 5: remove explicit verification instructions, because they "cause over-verification." This is a vendor claim with no numbers given.
  - "Improving skill-creator" (Mar 3 2026): "Capability uplift skills may become less necessary as models improve. Evals tell you when that's happened."
  - Cowork guide (Jul 16 2026): "Saved instructions, like Skills and memory files, written for an earlier model often carry corrections that model needed. Carried forward, old corrections can constrain a new model."
- **OpenAI**
  - "Rethinking skills and prompts for GPT-6 Astra" (Sep 11 2026): "overly specific guidance can now hinder results where it previously helped." ✓ And: "Because AGENTS.md applies whenever the model works in your repository, you should frequently revisit each instruction."
  - GPT-5.5 guide: "Begin migration with a fresh baseline instead of carrying over every instruction from an older prompt stack."
  - GPT-5.6 Sol guide, **vendor-internal**: leaner system prompts "improved evaluation scores by roughly 10–15% while reducing total tokens by 41–66% and cost by 33–67%."
- **Google, Gemini 3.5:** "Verbose or complex prompt engineering techniques designed for older models may cause the model to over-analyze."
- **Cursor:** "We spend weeks customizing our harness to a model's strengths and quirks" (Apr 30 2026). Cursor says per-model tuning is the product's job, not the user's.
- **Anthropic's own harness, "Harness design for long-running apps" (Mar 24 2026):** it dropped context resets with Opus 4.5 and the sprint construct with Opus 4.6. The April 23 postmortem: one system-prompt line cost 3% on Opus 4.6 and 4.7 and was reverted. Anthropic now gates model-specific instructions to the targeted model.

**Not always simpler**
- Fable 5.1 needs more prompting for progress updates, and GPT-6 Astra needs a push to keep going.
- The Opus 4.8 and Sonnet 5 guides note "more literal instruction following," so scope must be stated more explicitly.
- Letting a model write its own files is not a fix:
  - ETH: "stronger models do not necessarily generate superior context files."
  - SkillsBench (arXiv 2602.12670): "Self-generated Skills land below the no-Skills baseline on all three configurations."
- Skills that encode team preferences ("encoded preference" skills) are described as durable. It is skills that make up for missing model ability ("capability uplift" skills) that fade.
- SkillsBench, one pair and my comparison: the same skills added +11.1 on Opus 4.7 and +8.4 on Opus 4.8.

**Staleness from codebase change:** in 2,303 agent context files (arXiv 2511.12884), "a majority (59% to 67%) are modified in multiple commits." Deletions appear in only 19 of 100 sampled commits, and the authors see "a meaningful tendency to add new instructions rather than remove existing ones." Anthropic: CLAUDE.md "grows the way any unowned config file does: every team appends its own instructions and nothing gets deleted."

**Not found:**
- no independent before/after measurement of the same CLAUDE.md across a model upgrade;
- no named non-vendor company reporting rewrites with numbers.

**Defensible line for the post:** the major vendors now tell customers to re-check prompts, instruction files and skills at each model generation. Crutches written for an older model, such as forceful wording, step-by-step recipes and verification reminders, can make a newer one over-trigger or over-verify. The evidence is mostly vendor guidance, so the practical rule is a small eval per file or skill, re-run on each new model, deleting what no longer helps.

## Does AI code review work? (research round 2026-09-28)

**Verdict:** AI review works as a cheap first-pass bug finder. It is not a replacement reviewer, and nobody has shown that it reduces defects in production.

**Corrections to what the skeleton said**
- **Spotify's post never mentions an AI reviewer** (checked). Its answer to "76% more PRs to review" is "auto-merging what's safe, focusing review where it matters most." It has also merged more than 2.5 million automated maintenance PRs, "the vast majority auto-merged with no human in the loop." https://engineering.atspotify.com/2026/6/code-with-claude-coding-is-no-longer-the-constraint (Jun 3 2026) **[PRIMARY, checked]**
- **Uber's uReview figures date from Aug 12 2025, not 2026.** "uReview today analyzes over 90% of the weekly ~65,000 diffs." "75% of its comments as useful" counts only engineers who chose to rate comments; "over 65% of its posted comments addressed." Human comments for comparison: "only 51%… addressed in the same changeset." The time savings are estimated from an assumed 10 minutes per commit. https://www.uber.com/blog/ureview/ **[PRIMARY, company, 2025]**

**Company reports** (all self-reported)
- **Cloudflare**, Apr 20 2026: "the average review costs $1.19 and the median is $0.98." That covers 131,246 review runs across 48,095 merge requests. Engineers overrode the reviewer on 0.6% of merge requests. Their own caveat: "This isn't a replacement for human code review, at least not yet with today's models." https://blog.cloudflare.com/ai-code-review/ **[PRIMARY]**
- **Anthropic Code Review**, Mar 9 2026: "Before, 16% of PRs got substantive review comments. Now 54% do." "Less than 1% of findings are marked incorrect." Reviews "generally average $15–25." Also: "Code output per Anthropic engineer has grown 200% in the last year." https://claude.com/blog/code-review **[PRIMARY, checked, vendor on own use]**
- **GitHub Copilot code review**, Mar 5 2026: "more than one in five code reviews on GitHub." It "surfaces actionable feedback" in 71% of reviews and says nothing in the other 29%. No acceptance rate is given. **[PRIMARY]**
- **Cursor Bugbot**, Jan 15 2026: resolution rate rose "from 52% to over 70%." Resolution is judged by an AI at merge time. **[PRIMARY, vendor]**
- **OpenAI Codex review**, Dec 1 2025: "authors address it with a code change in 52.7% of cases." **[PRIMARY, vendor]**
- **Faros AI**, Sep 18 2026: heavy agentic-review use goes with "faster first reviews and lower change failure rates. The findings are correlational." Unreviewed merges rose 76.3%. No effect size is given. **[PRIMARY, analytics vendor]**

**Independent and academic studies: how often AI comments lead to a change**
- **Tuned in-house systems: 39–74%.**
  - Atlassian RovoDev (ICSE'26): 38.70% versus 44.45% for human comments. **[PRIMARY]**
  - Beko: 73.8% (2024). **[PRIMARY]**
  - Google AutoCommenter: about 40% (2024). **[PRIMARY]**
- **Tools on open-source projects: 1–36%.**
  - CodeRabbit on 239 repos: "36.4% were accepted" (arXiv 2607.03316, Jul 2026). **[PRIMARY]**
  - 16 GitHub Actions: 0.9–19.2% versus 60% for human comments (arXiv 2508.18771). **[PRIMARY]**
- **Head to head, human suggestions win.** From 278,790 review conversations: AI suggestions "are adopted into the codebase at a significantly lower rate than suggestions proposed by human reviewers" (full text: 56.5% versus 16.6%). When adopted, they "produce significantly larger increases in code complexity and code size" (arXiv 2603.15911, Mar 2026). **[PRIMARY, abstract checked]**

**Benchmarks:** AI reviewers catch about 15–33% of the issues human reviewers flagged.
- SWE-PRBench: 15–31% across 8 models.
- c-CRAB: Claude Code 32.1%.
- CR-Bench: GPT-5.2 recall 27–33%.
- Precision is understated because the answer keys are incomplete. **[PRIMARY]**

**Review time:** results point both ways, and no randomized trial of an AI reviewer exists.
- Beko: closure time rose from 5h52m to 8h20m.
- Atlassian: median cycle time 30.8% faster (observational).
- 1.02M PRs: faster decisions, "these efficiency gains do not translate into better review quality" (arXiv 2607.13196). **[PRIMARY]**

**Gaps and risks**
- **No controlled study of the effect on production defects.**
- **Security coverage.** At Meta, security is "19.1% in human reviews to just 2.0% in AI reviews" (arXiv 2607.29516). **[PRIMARY]**
- **Manipulation.** Crafted PR metadata got known vulnerabilities past Claude Code and CodeRabbit review in "32/33 (97%) cases" (arXiv 2603.18740). **[PRIMARY]**
- **Self-review.** "31.7% are silently endorsed by the same model that produced them" (arXiv 2605.21537). **[PRIMARY]**
- **Habituation.** Human approval of agent PRs rose while review latency went up 3.5x and inline comments fell 22% (arXiv 2606.22721). **[PRIMARY]**

**Not confirmed:** Martian leaderboard scores; the "80% of PRs without human involvement" claim; the size of Faros's change-failure effect; the method behind Microsoft's 10–20% figure. No 2026 update from Uber, Google or Datadog was found.

**Defensible line:** AI reviewers find some real bugs cheaply, at about $1 to $25 a review, and a good share of their comments lead to changes. That share is lower than for human comments. They catch a minority of what human reviewers flag, and their effect on production defects has not been measured. Use AI review as a first pass that frees people for design and risk, not as the fix for the review bottleneck.

## Enablement

- **Microsoft**, arXiv 2607.01418: first use spread through social networks; an engineer whose skip-level peers mostly used Copilot CLI "had +216% higher odds of trying it." **[PRIMARY]**

## Does value reach the company?

**The gap between individual output and company outcomes is well supported. "Most reported value is individual" has only weak direct evidence.**

- **DX**, 400+ companies, Nov 2024 to Feb 2026: AI usage up 65% on average, median PR throughput up 7.76%; "a 5–15% throughput gain" is typical. https://getdx.com/report/ai-and-engineering-velocity-a-longitudinal-analysis/ **[PRIMARY, exec summary]**
- **Faros 2026 "Acceleration Whiplash"**, 22,000 developers: tasks +33.7%, but incidents per PR +242.7%, median review time 5x, deployments per week −11.7%. https://www.faros.ai/research/ai-acceleration-whiplash **[PRIMARY, unit of analysis unclear]**
- **Stack Overflow 2025**: 69% of agent users say agents raised their productivity; 17.3% say they improved team collaboration. https://survey.stackoverflow.co/2025/ai **[PRIMARY]**
- **Atlassian 2025**, 3,500 respondents: 68% save 10+ hours a week with AI; 50% lose 10+ hours a week to organisational inefficiency. **[PRIMARY]**
- **NBER w34836**, ~6,000 executives, Feb 2026: nine in ten report no impact on employment or productivity over three years. https://www.nber.org/papers/w34836 **[PRIMARY]**
- **NBER w34984**, Mar 2026: "executives' perceived gains exceeded measurable results." **[PRIMARY]**
- **DORA 2025**: AI now positive for throughput and product performance, still negative for delivery stability; "AI … amplifies what's already there." **[PRIMARY]**
- **MIT NANDA 2025**: tools "primarily enhance individual productivity, not P&L performance." Thin method. **[PRIMARY]**
- **METR**: 2025 found a 19% slowdown; the 2026 redesign estimated an 18% speedup with a wide interval and called it "only very weak evidence." Do not cite for the company-level claim. **[PRIMARY]**
- **Humlum & Vestergaard**: the March 2026 revision ("Still Waters, Rapid Currents") no longer states the 3% time-savings figure in its abstract. Cite the May 2025 version for 3%.

**Complication:** 2026 company posts report org-wide PR volume (Spotify +76%, Cloudflare ~5,600 to 8,700 MRs/week, OpenAI more than doubled, Uber 70%+ agent PRs). That is summed output, not business outcomes, and the clearest company-level results come from agents those companies built.
