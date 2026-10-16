# Memory and skills: how much the post should say

Notes for "How to Customize Agents, and When to Own Them". Read 2026-10-16.

Two questions came up while reviewing the post against the team deck:

1. Should the post add significant content on agent memory, or is memory already covered by context engineering?
2. Is the post's coverage of skills enough, and do skills belong in layer 1?

## Verdicts

- **Memory: no new section; one paragraph plus a wider label.**
  - Practitioners who coined and spread "context engineering" put memory inside it.
  - Recent surveys split what persists (state, memory) from what goes into each model call (context).
  - So a sixth layer-2 part called "memory and state" is defensible, but not more defensible than folding memory in. Folding in matches the sources the post already uses (LangChain's agent definition, Anthropic).
  - The post's current label is too narrow for either view. It says context engineering is "what the model sees", "assembled for each step". Even Anthropic's definition includes note-taking outside the window. Widen it to cover what the agent keeps between steps and sessions.
- **Skills: enough evidence, but the post never said how a skill differs from an instruction file.** Added to 2.3 on 2026-10-16:
  - the invocation failure (Vercel, 56%);
  - Anthropic's split between skills that fade and skills that last.
- **Skills stay in layer 1.**
  - Writing skills is configuring an off-the-shelf agent through a supported extension point, and they survive model and product upgrades.
  - Building the mechanism that decides when a skill loads is context engineering you own, which is layer 2.
  - Memory splits the same way: turning on a product's memory feature is layer 1, and building your own memory store is layer 2. The September draft had the same ladder: "use-the-memory-feature to build-the-memory-system" (`version20260912.md`).

## Is memory part of context engineering? What the sources say

### Memory folded into context engineering (practitioner usage)

- **Anthropic, "Effective context engineering for AI agents", Sep 29 2025. [PRIMARY ✓]** https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
  - Lists "compaction, structured note-taking, and multi-agent architectures" as its techniques for long horizons.
  - The memory tool "makes it easier to store and consult information outside the context window through a file-based system". It lets agents "build up knowledge bases over time, maintain project state across sessions".
- **LangChain (Lance Martin), "Context engineering for agents", Jul 2 2025. [PRIMARY ✓]** https://blog.langchain.com/context-engineering-for-agents/
  - Sorts the techniques into write, select, compress and isolate. Scratchpads and long-term memories sit under "Write context".
  - "Scratchpads help agents solve a task within a given session … but sometimes agents benefit from remembering things across many sessions!"
- **Manus (Yichao 'Peak' Ji), "Context Engineering for AI Agents: Lessons from Building Manus", Jul 18 2025. [PRIMARY ✓]** https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus
  - "we treat the file system as the ultimate context in Manus: unlimited in size, persistent by nature, and directly operable by the agent itself", "structured, externalized memory".
- **Google, "Context Engineering: Sessions & Memory" whitepaper, Kaggle 5-day agents course, Nov 2025. [SECONDARY]** I saw only course summaries, not the PDF. Its title puts sessions and memory under context engineering.
- **Letta, "Benchmarking AI Agent Memory: Is a Filesystem All You Need?", Aug 12 2025. [PRIMARY ✓]** https://www.letta.com/blog/benchmarking-ai-agent-memory
  - Concludes that "memory is more about how agents manage context than the exact retrieval mechanism used".

### Memory or state as a separate part

- **Survey, "From Question Answering to Task Completion: A Survey on Agent System and Harness Design", arXiv 2606.20683, v1 Jun 14 2026. [PRIMARY ✓, read the relevant sections]** https://arxiv.org/abs/2606.20683
  - Splits the harness into six "runtime responsibilities": observation, context, control, action, state, and verification/governance.
  - The context manager "determines which available information enters the current model call". The "state and artifact store" "persists execution state across steps, sessions, and subtasks", including "memory records".
  - Quote for the post: "Long-horizon agents often fail not because no state is stored, but because the wrong state is preserved, the right state cannot be retrieved, or stale state is treated as current."
  - It cites Meng et al. (Apr 2026), who "formalize the harness as a six-component tuple". A search summary says the tuple includes a separate memory store. **Not read; don't cite.**
- **Google ADK docs, "Conversational Context: Session, State, and Memory". [PRIMARY ✓, live page]** https://google.github.io/adk-docs/sessions/
  - Three separate concepts: Session (one conversation), State (data "within the current conversation") and Memory ("Searchable, Cross-Session Information").
  - All three sit under the heading "Conversational Context", so even this split stays inside context.
- **LangChain, "The anatomy of an agent harness". [PRIMARY ✓]** The post's own source for the agent definition.
  - Has a section of its own, "Memory & Search for Continual Learning": "For memory, the filesystem is again a core primitive. Harnesses support memory file standards like AGENTS.md which get injected into context on agent start."
  - So memory is a named concern, and AGENTS.md counts as memory.
- **Scale AI taxonomy, "Model or Harness? An Interaction-Centric Taxonomy for Localizing Agent Failures", arXiv 2607.28802, Jul 30 2026. [PRIMARY ✓, already in the post]**
  - Abstract: "agent behavior emerges from interactions among models, harnesses, users, tools, memory, and environments."
- **Graphlit (Kirk Marple), "AI Agent Memory Frameworks in 2026: Memory vs. Context", May 20 2026. [PRIMARY ✓, vendor]**
  - Argues "memory and context are related, but they are not the same layer", yet also that "'agent memory' is becoming 'context engineering'". A vendor positioning piece.

### Memory-only surveys (2026), showing memory is a research field of its own

- "Anatomy of Agentic Memory: Taxonomy and Empirical Analysis of Evaluation and System Limitations", arXiv 2602.19320, Feb 22 2026.
  - Benchmarks "underscaled", metrics "misaligned with semantic utility", system costs "frequently overlooked".
- "Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers", arXiv 2603.07670, Mar 8 2026.
  - Memory as a "write–manage–read loop".
- "From Storage to Experience: A Survey on the Evolution of LLM Agent Memory Mechanisms", arXiv 2605.06716, May 7 2026.
  - Calls memory "the architectural cornerstone".
- "Always-On Agents: A Survey of Persistent Memory, State, and Governance in LLM Agents", arXiv 2606.30306, Jun 29 2026.
  - Treats memory together with task ledgers, permissions, credentials and audit records as "persistent state".

All titles and dates checked against the arXiv API.

## Memory evidence usable in the post

- **Databricks, "Memory scaling for AI agents", Apr 10 2026. [PRIMARY ✓]** https://www.databricks.com/blog/memory-scaling-ai-agents
  - "Performance rose from 2.5% to over 50%, surpassing the expert-curated baseline (33.0%) after just 62 log records."
  - "Reasoning steps dropped from ~19 to ~4.3."
  - The memory came from uncurated user conversation logs in a Genie space, filtered by an LLM judge.
- **STALE: Can LLM Agents Know When Their Memories Are No Longer Valid?, arXiv 2605.06527, May 7 2026. [PRIMARY-abs ✓]**
  - 400 conflict scenarios. "even the best evaluated model achieving only 55.2% overall accuracy" (Gemini-3.1-pro).
  - The 55.2% is an average over three probes: noticing that a memory is outdated, rejecting a query that presupposes it, and applying the update. It is **not** a detection rate. Gemini-3.1-pro scored 92% and 69% on noticing, but only 30% and 14% on rejecting a stale premise (Table 2).
  - "most memory frameworks fall below 10%" (mem0 8.3%, A-mem 5.1%). Abstract: models "often accept outdated assumptions embedded in a user's query".
- **Compaction risks.**
  - arXiv 2608.06503 (Aug 6 2026, "preliminary"): compression "can weaken the influence of recent interactions, increasing blocked actions, repeated exploration, and instability across runs."
  - arXiv 2606.23525, Self-Compacting Language Model Agents (Jun 22 2026): fixed-threshold compaction risks "discard of partial results mid-derivation", and a compaction tool alone is "unevenly used".
- **Letta filesystem result (Aug 12 2025, see above).**
  - A gpt-4o-mini agent storing history in files scored 74.0% on LoCoMo, "significantly above Mem0's reported 68.5%".
  - Caveats: a vendor benchmarking a rival, and Mem0 now reports much higher scores (https://mem0.ai/blog/state-of-ai-agent-memory-2026), so the numbers are contested. Cite for the idea (agents use file tools well), not as a ranking.
- **Harvey, context graphs: Niko Grupen (Head of Applied Research), X post, Oct 15 2026. [PRIMARY ✓, read via the fxtwitter API and X syndication]** https://x.com/nikogrupen/status/2110773803592937733
  - Before a task, "an agent first reviews each document in its client matter and builds a graph of relevant entities and their relationships – e.g. parties, dates, draft vs. executed status, which versions belong to the same contract."
  - On Harvey's Legal Agent Bench: "improved rubric pass rate by up to 30% while reducing task cost by up to ~50%".
  - One firm-knowledge task went from 0% of rubric criteria (wrong precedent from raw files) to 75%.
  - Caveats: "up to" figures, Harvey's own benchmark, and a post rather than a write-up ("We'll have more to share soon").
  - Closer to precomputed structured context than to memory across sessions. It fits the post's line that someone has to decide what the agent should know.
- **Harvey Memory, announced Jan 8 2026. [SECONDARY, Legal IT Insider]** https://legaltechnology.com/2026/01/08/harvey-to-build-memory-for-context-retention-across-matters/
  - References past threads within a firm's retention window, scoped to a user, client or matter. An example of buying memory inside a vendor product, which is layer 1.
- **"Context graph" as a term.** Foundation Capital's essay "AI's trillion-dollar opportunity: Context graphs" (Ashu Garg with Jaya Gupta) predates Harvey's post: https://ashugarg.substack.com/p/ais-trillion-dollar-opportunity-context
  - An investor thesis about decision traces, with no outcome data. Don't cite it for results.
- **Karpathy's "LLM wiki" / second brain (2026). [SECONDARY only]**
  - Plain markdown that an LLM writes and maintains. It's the same pattern as the post's one-page memory prompt.
  - I found only press coverage (VentureBeat, MindStudio). Link Karpathy's own post before citing.
- **Author's own setup.** `skeleton.md` lists "scheduled jobs building a knowledge base" as an open author todo. If it produced a result describable without client details, it is the best first-hand anchor.

## Skills: checks for the 2.3 addition

- **Vercel (Jude Gao), "AGENTS.md outperforms skills in our agent evals", Jan 27 2026. [PRIMARY ✓, re-read 2026-10-16]** https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals
  - "In 56% of eval cases, the skill was never invoked. The agent had access to the documentation but didn't use it."
  - Baseline (no docs) 53%; skill with default behaviour 53%, "+0pp".
  - "skills maxed out at 79% even with explicit instructions telling the agent to use them"; the 8KB AGENTS.md docs index reached 100%.
  - "The skill existed, the agent could use it, and the agent chose not to."
- **Anthropic, "Improving skill-creator: Test, measure, and refine Agent Skills", Mar 3 2026. [PRIMARY ✓, re-read 2026-10-16]** https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills
  - "Capability uplift skills help Claude do something the base model either can't do or can't do consistently."
  - "Encoded preference skills document workflows where Claude can already do each piece, but the skill sequences them according to your team's process."
  - "Capability uplift skills may become less necessary as models improve. Evals tell you when that's happened. Encoded preference skills are more durable, but only as valuable as their fidelity to your actual workflow."
- Adoption figures already in `rung1.md`: Uber 3,600+ skills and 30K+ skill executions a day (Aug 27 2026), and Intercom 100+ skills (Mar 19 2026). Not added to the post.

## Knowledge bases and retrieval (read 2026-10-16)

Question: is company knowledge (documents, wikis, playbooks) under-represented? Should layer 1 include "knowledge base engineering"?

**Verdict:**
- Yes, it's under-represented: before this round the post never mentioned retrieval or knowledge bases.
- Add it to layer 1 under a plain name ("Integrations and knowledge"). "Knowledge base engineering" is not a practitioner term.
- Same split as skills and memory:
  - pointing an off-the-shelf agent at your documents through connectors or files is layer 1;
  - building a retrieval pipeline or index into your own harness is layer 2.
- The evidence on agentic search versus an index is mixed. Neither replaces the other.

**Sources:**
- **Anthropic, "Effective context engineering for AI agents", Sep 29 2025. [PRIMARY ✓]**
  - "Claude Code is an agent that employs this hybrid model: CLAUDE.md files are naively dropped into context up front, while primitives like glob and grep allow it to navigate its environment and retrieve files just-in-time, effectively bypassing the issues of stale indexing and complex syntax trees."
  - Also: "we increasingly see teams augmenting these retrieval systems with 'just in time' context strategies".
- **"Deep Agentic Search for Repository-Level Code Question Answering: An Empirical Study", arXiv 2608.01507, Aug 2 2026. [PRIMARY-abs ✓]**
  - On SWE-QA, "Semantic search answered 65.2% of questions correctly against 46.2% for deep agentic search", "at less than half the cost".
  - 41.8% of deep-search failures happened "at the hand-off between the planner and its sub-agent", and were usually silent.
  - Scope: "for read-only questions over a repository that can be indexed".
- **Cursor (Heule, Jia, Jain), "Improving agent with semantic search", Nov 6 2025. [PRIMARY ✓]** https://cursor.com/blog/semsearch
  - "on average 12.5% higher accuracy in answering questions (6.5%–23.5% depending on the model)" over grep alone, plus online A/B tests.
  - A vendor reporting on its own index.
- **"Is Grep All You Need? How Agent Harnesses Reshape Agentic Search", Sen, Kasturi, Lumer, Gulati and Subbiah (all PwC), arXiv 2605.15184, May 14 2026. [PRIMARY ✓, read the results and limitations]**
  - **Setup:** 116 questions from LongMemEval-S (long multi-session chat memory). Grep versus vector retrieval across four harnesses: the authors' own Chronos plus Claude Code, Codex and Gemini CLI. Search results go either inline or into files the model reads separately. GPT-4o grades.
  - **Inline results:** "inline grep exceeds inline vector for every harness–model pair", by margins from 86.2% vs 62.9% (Chronos, Gemini 3.1 Flash-Lite) down to 76.7% vs 75.0% (Claude Code, Opus 4.6).
  - **The harness matters as much as the retriever:** "The same Claude Opus 4.6 backbone reaches 93.1% under Chronos but 76.7% under Claude Code, so changing the harness shifts the ceiling by roughly as much as swapping retrievers within a fixed harness."
  - **How results reach the model matters a lot:** with file-based delivery, "programmatic vector exceeds programmatic grep on five of ten harness–model pairs". Codex with GPT-5.4 "falls from 93.1% under inline grep to 55.2% under programmatic grep".
  - **Authors' own limits:** "our conclusions are tied to long-memory conversational QA … Lexical tools may be disproportionately helpful here because answers often license on verbatim spans"; "We do not claim that grep 'beats' vector in general."
  - **Caveats:** Chronos is the authors' own harness (from their earlier paper), the sample is small (116 questions), and the grader is an LLM.
  - **Use in the post:** not for the knowledge-base paragraph, because the data is chat memory with literal answers. It would back the harness argument in 1.3 or the context-engineering point in layer 2: the same model and data moved from 93.1% to 55.2% depending on how search results were handed to it. Not added; the post already has enough harness-matters evidence.
- **EnterpriseRAG-Bench, arXiv 2605.05253, v1 May 5 2026, by Onyx. [PRIMARY ✓, read Table 6]** https://arxiv.org/abs/2605.05253
  - Synthetic company "Redwood Inference": about 500,000 documents across nine sources (Slack, Gmail, Linear, Google Drive, HubSpot, Fireflies, GitHub, Jira, Confluence), with noise such as misfiled documents, near-duplicates and conflicting information. 500 questions in ten categories.
  - Three baselines, all answering and graded with GPT-5.4. Correctness: BM25 68.8%, a bash agent (grep, find, head, 10-minute budget) 60.6%, vector search (text-embedding-3-large) 51.4%. Completeness: bash agent 61.1%, BM25 56.0%, vector 42.9%.
  - "Vector search underperforms expectations even on semantic questions (32.8% correctness)." The authors suggest embedding models rarely see company codenames, tickets and chat styles.
  - Conflict of interest: Onyx sells a RAG product and "excludes itself from the leaderboard".
  - **Used in 2.3.** This is company knowledge, not code, which makes it the better fit for layer 1.
- **Workspace-Bench 1.0, arXiv 2605.03596, May 5 2026. [PRIMARY-abs ✓]** 20,476 files (up to 20GB) across 5 worker profiles and 388 tasks that need cross-file retrieval. "the best reaches only about 60%, substantially below the human result of 80.7%". Not used; a candidate if the paragraph needs a second number on how hard raw workspaces are.
- **Karpathy, "LLM Wiki" gist, Apr 4 2026. [PRIMARY ✓]** https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
  - "the LLM incrementally builds and maintains a persistent wiki"; "The knowledge is compiled once and then kept current, not re-derived on every query."
  - Contrasts this with RAG, where "the LLM is rediscovering knowledge from scratch on every question".
- **LinkedIn playbooks:** already in the post (2.2).
- **Author's own setup (first-hand, from the author 2026-10-16):** scheduled jobs turn raw documents and records into an organised knowledge base. Agents get to results faster from it than when they search raw documents from scratch. The author also states that it uses fewer tokens; at the author's request (2026-10-16), the post states this directly, without the earlier "not measured" hedge.

## Vendor knowledge-base products (read 2026-10-16)

Verdict: no independent results. Everything below is vendor-run or vendor-commissioned. None of it goes in the post; it's kept here so the question isn't reopened.

- **Glean, "Not all enterprise context is created equal", last updated Feb 12 2026. [PRIMARY ✓, vendor self-evaluation]** https://www.glean.com/blog/enterprise-search-evaluation-2026
  - About 280 queries "mined … from Glean's own internal deployment", run on the same models (Glean on GPT-5.1 vs ChatGPT; Glean vs Claude, both on Sonnet 4.5), blind graded on a five-point preference scale.
  - "when graders had a preference, they picked Glean over ChatGPT 1.9× more often and over Claude 1.6× more often on correctness". Ties are excluded, the queries come from Glean's own deployment, and Glean picked the competitors' connector setups.
  - Mildly interesting for the post's thesis: an index plus a relationship graph beat live connector search on the same model. Too self-interested to cite.
- **Forrester TEI of Glean, commissioned by Glean, Sep 2024. [SECONDARY summary]** 141% ROI over three years and "up to 110 hours per user per year", for a composite organisation built from interviews. Commissioned, modelled and from 2024. Not usable.
- **Atlassian:** a Forrester TEI claiming 428% ROI for Confluence Premium with AI features, commissioned by Atlassian. Not checked further.
- **Slite, "the self-maintaining knowledge base", Jun 10 2026. [PRIMARY changelog]** https://slite.com/changelog/the-self-maintaining-knowledge-base
  - An agent that "detects when documentation has drifted", proposes fixes and routes every change through human approval.
  - A product announcement with no outcome data. It shows that vendors see stale knowledge as a problem, which matches the post's point, but it adds no evidence.
- **Notion AI, Guru, Microsoft 365 Copilot connectors:** marketing pages and reviews only; no published results found.
- **What would count:** an independent comparison of an agent with a curated knowledge base against the same agent searching raw sources, on the same tasks, with cost. None found. EnterpriseRAG-Bench comes closest, but it compares retrieval methods, not curated against raw.

## Two smaller gaps (read 2026-10-16)

- **Skill descriptions decide triggering.** Anthropic, "Improving skill-creator" (Mar 3 2026) [PRIMARY ✓]:
  - "As your skill count grows, description precision becomes critical: too broad and you get false triggers, too narrow and it never fires."
  - "We ran it across our document-creation skills and saw improved triggering on 5 out of 6 public skills."
- **Memory poisoning.** Microsoft AI Red Team, taxonomy v2.0, Jun 4 2026 [PRIMARY ✓, already cited in the post for HitL bypass]:
  - "Memory poisoning via XPIA, where injected instructions seed the agent's persistent memory for later retrieval, requires only a single successful injection, which the agent then propagates across subsequent sessions."
  - "XPIA and memory poisoning were observed at high frequency and frequently combined."
  - v2.0 also adds "Session Context Contamination".

## Done 2026-10-16

- 2.3 split into 2.3 and 2.4. Skills additions: Vercel 56%, and Anthropic's capability-uplift vs encoded-preference split.
- Layer-2 label widened:
  - figure: "Context engineering: what the agent sees and remembers" / "What goes into each step, and what it keeps across sessions";
  - prose: "what the agent sees at each step and what it remembers across sessions (context engineering)".
  - Wording follows common usage: practitioners say "remember" and split short-term from long-term memory.
- Memory paragraph added after the first-hand memory paragraph (review doc 7.3). It cites Databricks, Harvey's context graph ("first look shared on X", "up to"), the harness survey's stale-state line and STALE. Letta was left out: a 2025 vendor-vs-vendor result with contested numbers.
- "Prevention follows from that diagnosis" became "from the diagnosis by Zhao and colleagues", since the new paragraph now sits between them.
- 7.3 opening changed to "Long-term memory can help a lot, but only while it stays current." "The risk is memory that has gone stale" became "Keeping it current is the hard part."
- Layer-1 memory clause added to 2.4, citing Anthropic, "Working with Claude Fable 5 in Claude Cowork", Jul 16 2026 [PRIMARY ✓]: https://claude.com/blog/working-with-claude-fable-5-in-claude-cowork. Full quote: "Saved instructions, like Skills and memory files, written for an earlier model often carry corrections that model needed. Carried forward, old corrections can constrain a new model."
- Applied (review doc 2.3, 2.4, 7.3, decision table, layer-1 figure):
  - 2.3, new knowledge paragraph: Anthropic just-in-time quote, EnterpriseRAG-Bench, the author's first-hand result, LinkedIn, Karpathy.
  - 2.4: skill description and triggering (5 of 6).
  - 7.3: memory poisoning (Microsoft).
  - Decision-table row: "The agent keeps getting your conventions or facts wrong".
  - Layer-1 figure: "Integrations and knowledge" / "MCP servers and connectors to your systems and documents"; "Context the agent loads always or on demand, retested when models change"; alt text updated.
  - Review-doc section 2 renumbered (now 2.1–2.11).
- `fig-failure-fixes.svg` already shows the five failure modes and their fixes. It needs no change: "Context and examples" covers knowledge, skills and memory, and "Unsafe … or is manipulated" covers memory poisoning.

## Open items

- Optional: the layer-1 figure calls instruction files and skills "Standing context the agent reads". Skills load on demand, so "context the agent reads, always or on demand" would be more accurate.
- The deck's Q7 evidence could take the Vercel 56% and skill-creator cards once the user approves.
