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
