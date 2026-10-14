# Workflow redesign around AI agents: 2026 cases

Research notes for "How to Customize Agents, and When to Own Them". Collected 2026-10-11.

Purpose: the TL;DR (T.1) claims "the business gains only when the work is redesigned around them." The draft's evidence (2.6) mostly shows gains going missing without redesign. These are concrete cases of what redesign looks like.

Verification legend:
- **Checked by me**: I fetched the source and confirmed the quote or numbers myself.
- **Agent-verified**: a research agent fetched the source and quoted it; I have not re-read it.
- **Self-report**: the deploying company describing its own results.

## Strongest cases

### A. Alibaba Taobao customer service: randomized field experiment

- **Source:** Wang, Zhu, Feng, Lu and Jia, "Agentic AI and Human-in-the-Loop Interventions: Field Experimental Evidence from Alibaba's Customer Service Operations", arXiv 2605.14830, v1 May 14, 2026, v2 June 1, 2026. https://arxiv.org/abs/2605.14830
- **Status:** title, dates and abstract claims checked by me. Sample sizes and effect sizes are agent-verified.
- **Timing caveat:** the paper is from 2026, but the experiment ran in August 2024.
- **Design:** 647 workers and 680,676 chats. The control group of workers resolved every chat. The treated workers "supervised an agentic AI system that resolved AI-eligible chats while continuing to handle AI-ineligible chats." AI-eligible chats were only 5.8% of the sample.
- **Results:**
  - **Speed and repeat contacts:** "AI deployment reduces average chat duration and has limited effects on retrial rates, but substantially lowers ratings for AI-eligible chats" (abstract). The agent reports chat duration −3.2% overall and −16.8% on AI-eligible chats.
  - **Ratings:** customer ratings fell 0.858 points when the agent handled a chat alone (agent-verified).
  - **Escalations:** "human intervention preserves service quality in algorithm-triggered technical escalations" but is "less effective in algorithm-triggered emotional escalations"; "early intervention is essential for sustaining high post-escalation intervention effort" (abstract).
  - **Late handoffs:** when a frustrated customer was handed over late, "chat duration increases by 40.8 percent … the retrial rate rises by 6 percentage points … customer ratings decline by 0.928 points" (agent-verified).
  - **Freed time:** workers "adapted their multitasking workflow to devote greater attention" to the chats the AI could not take (abstract).
- **Use in article:** the best evidence that *where and when a person steps in* is the redesign decision. It also has a measured downside: ratings fall when the agent handles chats alone.

### B. Kim, Kim and Koning, "Mapping AI into Production": 515 startups, preregistered randomized trial

- **Source:** INSEAD Working Paper 2026/20/STR, March 30, 2026. https://ssrn.com/abstract=6513481 (PDF: https://sites.insead.edu/facultyresearch/research/doc.cfm?did=75343)
- **Status:** abstract and numbers checked by me.
- **Design:** "treated firms receive information about how other firms have reorganized production around AI." All firms had the same tools; the only difference was this information.
- **Results:**
  - "treated firms discover more AI use cases, a 44% increase".
  - "Treated firms complete 12% more tasks, are 18% more likely to acquire paying customers, and generate 1.9x higher revenue."
  - "Their demand for external capital investment falls by 39.5% relative to the control group, while their demand for labor remains unchanged."
  - "discovering where and how to deploy AI is a key bottleneck in realizing the gains from this technology."
- **Role changes reported by the firms (agent-verified):** one firm went "from an intent classifier replacing a dispatcher to a payment-reminder engine replacing collections staff—compressing five roles into AI modules". Another "reduced manual inspection by 70%."
- **Caveat:** startups only, in a 3-month accelerator.
- **Use in article:** the strongest *causal* support for T.1. Same tools, but firms told how others had redesigned their work did better.

### C. Choi and Xie, "Human + AI in Accounting": finance operations

- **Source:** Journal of Accounting Research 64(3), June 2026. https://www.gsb.stanford.edu/faculty-research/publications/human-ai-accounting-early-evidence-field
- **Status:** abstract checked by me on 2026-10-12; added to 2.7.
- **Design:** 79 small and mid-sized firms, over 200,000 transactions. Observational, not causal.
- **Quotes:** "systematic reallocation of effort away from routine data entry toward business communication and quality assurance tasks"; "faster month-end closing"; "accountants selectively intervene when AI confidence scores are low."
- **Use in article:** a peer-reviewed example outside software, showing reviewers acting on a confidence signal. This links to §8, where the article discusses confidence signals and escalation.
- **Caveat:** the per-standard-deviation effect sizes seen in search snippets were not checked. Cite only the abstract-level claims.

### D. Salesforce support: self-report

- **Source:** Salesforce newsroom, April 29, 2026. https://www.salesforce.com/news/stories/salesforce-reshaping-workforce-in-age-of-ai/
- **Status:** agent-verified; self-report.
- **Quotes:**
  - "Agentforce was handling 2.6 million customer conversations with a 63% resolution rate and customer satisfaction scores that matched human agents."
  - The company "redeployed hundreds of support engineers into areas of the business that are growing quickly while also managing demand and headcount by not backfilling other roles."
  - Named destinations for those engineers: renewals and success-architect roles.
- **Not verified:** Benioff's "9,000 to 5,000" support headcount figure, which appears only in a podcast.

### E. Allianz "Project Nemo": insurance claims, self-report, 2025

- **Source:** Allianz SE, November 3, 2025. https://www.allianz.com/en/mediacenter/news/articles/251103-when-the-storm-clears-so-should-the-claim-queue.html
- **Status:** agent-verified; self-report. No 2026 update found.
- **Process:** seven agents (planner, cyber, coverage, weather, fraud, payout, audit) hand "a human agent [the] payment decision." The run "takes less than five minutes … until the final human review."
- **Metrics:** "80% reduction in claim processing and settlement time"; claims under AUD 500 went "from several days to one day—or even just hours."
- **Freed time:** "Claims processors can spend less time on routine checks and more time engaging with complex or emotionally sensitive cases."

### F. Supporting cases

- **BNY, 1Q26 investor presentation, April 16, 2026 (self-report, agent-verified):** "~70% of restricted party screening for payments reviewed by AI", "&gt;30% faster resolution"; "&gt;10% of custody settlement transaction status inquiries addressed by AI", "&gt;80% faster investigation"; "~140 digital employees." https://www.bny.com/assets/corporate/documents/pdf/investor-relations/earnings/quarterly-update-presentation-1q-2026.pdf
- **P&amp;G "Cybernetic Teammate", preregistered randomized trial, n=776, NBER w33641, published online June 2026 (agent-verified):** "individuals with AI matched the performance of teams without AI"; "AI breaks down functional silos." Generative AI, not agents. https://www.nber.org/papers/w33641

### G. Stanford Digital Economy Lab, "The Enterprise AI Playbook: Lessons from 51 Successful Deployments" (added 2026-10-12)

- **Source:** Pereira, Graylin and Brynjolfsson, April 2026. https://digitaleconomy.stanford.edu/app/uploads/2026/03/EnterpriseAIPlaybook_PereiraGraylinBrynjolfsson.pdf
- **Status:** checked by me (PDF text).
- **Method and caveats:** interviews with executives, August 2025 to February 2026, across 51 cases at 41 organisations. All companies are anonymised. The report says it "relies primarily on self-reported data" with "potential selection bias toward successful deployments". Case-study pages carry a "DRAFT" watermark.
- **Aggregate findings:**
  - "77% of the hardest challenges were invisible and intangible costs: change management, data quality, and process redesign."
  - "Escalation-based models (AI handles 80%+ autonomously, humans review exceptions) delivered 71% median productivity gains versus 30% for approval models. This may, in part, reflect different types of tasks addressed." Fits §8.
  - "Headcount reduction was the largest outcome in 45% of the deployments", with hiring avoided, redeployment or no reduction in the other 55%.
- **Concrete cases:**
  - **Edtech company:** content production was re-architected "so that subject matter experts became human-in-the-loop reviewers rather than drafters", generating "millions in cost savings". Engineering saved 20 to 30% of time with Copilot and Cursor, and "Savings were used to accelerate the roadmap, not reduce staff." Fits 2.6 (someone has to decide what freed hours are for).
  - **Regional supermarket chain (about 25 stores):** an agent replaced the human buyer and makes purchasing decisions on its own: waste −40%, stockouts −80%, EBITDA margin doubled.
  - **Communications technology company, customer support:** 82% ticket deflection "by redesigning workflows around AI first resolution", support headcount −32%.
  - **Latin American fintech, coding:** "Rather than engineers completing an entire migration task, they could just review the changes, make minor adjustments, then merge their PR."

## Reversals and cautionary cases

### Klarna: moved to a hybrid of AI and human service, still claims savings

- **2025 reversal (secondary reporting):** CX Dive (November 20, 2025) reports Klarna "turned back to human customer service representatives this May." TechCrunch (June 4, 2025) paraphrases the CEO calling human service "a VIP thing."
- **Claims vs costs (Q3 2025 call, via CX Dive):** the AI does the work of "853 full-time agents" and "saved the company $60 million". Yet customer service and operations cost "$50 million … up from $42 million a year ago."
- **2026, primary source (agent-verified):** Q2 2026 press release, August 18, 2026. "Customer service and operations" cost $58M vs $51M a year earlier (+14%), while revenue grew 27%. Q1 2026: $55M vs $51M. https://s205.q4cdn.com/644747736/files/doc_earnings/2026/q2/earnings-result/Q2-26-Klarna-Group-plc-Press-Release.pdf
- **Reading:** service costs are falling relative to revenue but still rising in dollars.

### Commonwealth Bank of Australia: reversed job cuts in 2025, cut chat roles at an outsourcer in 2026

- **2025 (union source and CBA statement, agent-verified):** "Call volumes were in fact increasing and CBA was scrambling … offering staff overtime and directing Team Leaders to answer calls." In a statement reported by the Canberra Times (August 21, 2025), CBA said its assessment "did not adequately consider all relevant business considerations and this error meant the roles were not redundant." Union release via archive: https://web.archive.org/web/2026id_/https://www.fsunion.org.au/win-cba-backflips-on-customer-service-job-cuts-admits-they-got-it-wrong/
- **2026 (secondary):** ACS Information Age, July 30, 2026, citing Bloomberg: "hundreds of chat support roles" cut at the outsourcer Nutun; the chatbot resolves "almost nine in every 10 customer conversations." https://ia.acs.org.au/article/2026/ai-drives-fresh-commbank-job-cuts.html

## Moves that recur across cases

1. **The agent does the routine pass; a person makes the decision that matters.** Allianz (payout), BNY (screening review), Alibaba (escalation), accounting study (low-confidence items).
2. **Freed time goes to the hard cases.** Alibaba (attention shifted to chats the AI could not take), Allianz ("complex or emotionally sensitive cases"), accounting (client communication and QA).
3. **People are redeployed to growth work, and leavers are not replaced.** Salesforce (support engineers into renewals and success roles); startup trial ("labor remains unchanged" while revenue grew).
4. **When the handoff happens matters as much as whether there is one.** Alibaba: late handoffs on frustrated customers did worst.
5. **Cut staff only once demand has been measured.** CBA and Klarna both staffed to a projected deflection rate (the share of contacts the AI would take) and had to reverse.
6. **The gain comes from knowing where to redesign, not from access to the tool.** Startup trial: same tools, different information, different results.

## Fit with the article

- **T.1 / 2.6:** the startup trial gives causal support for "gains only when the work is redesigned." The Alibaba trial shows what redesign decisions look like (who takes which cases, when a person steps in) and that they have measured trade-offs.
- **§8 (escalation):** the Alibaba handoff findings and the accounting study's "intervene when AI confidence scores are low" fit 8.6 and 8.7.
- **11.1 row "Hours saved, but no cost removed":** move 2 (freed time to hard cases) and move 3 (redeploy, don't backfill) are concrete answers to "what to work on."

## Not verified / excluded

- **Salesforce:** Benioff's "9,000 to 5,000" support cut, a podcast claim with no primary source.
- **Klarna:** February 2026 Charter interview (paywalled) and a Bloomberg quote, neither fetched.
- **Choi and Xie:** effect sizes beyond the abstract.
- **JPMorgan:** the "10% operations" cut, from its 2025 investor day, not checked.
- **Allianz:** no 2026 scaling data found.
- **Vendor marketing excluded:** insurance, healthcare-admin and prior-authorization figures (for example Beam and Five Sigma).
