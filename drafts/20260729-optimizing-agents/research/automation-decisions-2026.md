# How much to automate: evidence, accountability and one worked case

Working note, 2026-10-20. Research behind the post's "how much to automate end to end" paragraphs (posts/20261016-customize-agents/index.qmd, the two paragraphs that replaced the priced thought experiment). It covers what the outside sources say, a case from the author's own client work, and a framing for when the decision can be made with confidence.

**Confidentiality.** This repo is public. The client case is described generically: no client name, no people, no internal figures. The engagement records stay outside this repo. If the case goes into the post, it is "an invoice-factoring company," with directions of effect rather than exact numbers, and no mention of the model family (the lesson is the decision process, not the model).

---

## 1. Why the priced thought experiment was cut

The earlier draft set autonomy by putting a dollar price on one silent error and reading the best coverage off a curve. Two problems:

1. **Most errors have no price tag.** Should pull-request review be fully automated? There is no number for what one bad merge costs. The pricing frame works only where losses are small, many and countable.
2. **It left out who answers for a mistake.** Organizations often keep a human in the loop because someone has to be accountable, not only to catch errors.

What replaced it: how much to automate depends on how bad a silent mistake could get and on who answers for it.

---

## 2. Outside sources (all checked by fetching the page)

### Spotify, fleet-wide auto-merge (May 2023, before LLM agents)

[Fleet Management at Spotify, Part 3](https://engineering.atspotify.com/2023/05/fleet-management-at-spotify-part-3-fleet-wide-refactoring)

- **What counts as safe:** a change merges on its own only if it passes the repository's tests. If a bad change gets through, "this is a signal to the owner that they should be adding more and better tests to their repo."
- **Who decides:** "We invert control on who decides what is automerged, from the repo owner to the change author."
- **Default:** "A conscious decision was made to treat automerging as something you would have to opt out of if you did not want it, rather than something you need to opt into." About 50 of thousands of repositories opted out.
- **Catching what gets through:** Firewatch "correlate[s] failed backend service deployments or data pipeline executions with potential automerged changes into their repos."
- **Rollout:** "done very slowly," first only for the Java BOM-updating shift, then phase by phase, with components grouped by how critical they are.

**Takeaway.** Safe is defined by a check the repository owner controls. Responsibility is split on purpose (the author decides what auto-merges, the owner answers for the tests). A detector links failures back to the automation so they get caught and undone.

### Spotify, the agent takes over the scripts (Nov 2025)

[Spotify's background coding agent, Part 1](https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1) (Nov 6, 2025). "We replaced deterministic migration scripts with an agent that takes instructions from a prompt. All the surrounding Fleet Management infrastructure — targeting repositories, opening pull requests, getting reviews, and merging into production — remains exactly the same." Teams had merged more than 1,500 of the agent's pull requests.

This is what makes the 2023 auto-merge rules relevant to agents. The 2022 figure (77% of more than 270,000 Fleetshift PRs auto-merged) covers scripted changes only, so it is not used in the post. Neither post says whether the agent's PRs auto-merge or get human review, so don't imply either.

### Spotify, background coding agents (Dec 2025)

[Feedback loops for background coding agents, Part 3](https://engineering.atspotify.com/2025/12/feedback-loops-background-coding-agents-part-3)

- An LLM judge reviews agent sessions and vetoes about a quarter of them. When vetoed, the agent course-corrects about half the time.
- They rank failures from mild to severe: no PR at all, a PR that fails CI, and a PR that passes CI but is wrong. The last is the worst, because nothing flags it.

### Spotify, "coding is no longer the constraint" (June 2026)

[Code with Claude talk write-up](https://engineering.atspotify.com/2026/6/code-with-claude-coding-is-no-longer-the-constraint). Their answer to the growing review load is "auto-merging what's safe, focusing review where it matters most." This is already quoted in the post.

### The moral crumple zone

Madeleine Clare Elish, ["Moral Crumple Zones: Cautionary Tales in Human-Robot Interaction"](https://estsjournal.org/index.php/ests/article/view/260), *Engaging Science, Technology, and Society* (2019). The human operator "bears the brunt of the moral and legal responsibilities when the overall system malfunctions," even with little real control over it. For agents: a reviewer who approves hundreds of agent changes a day without real control is this person.

### Driverless cars: the company answers

- **UK Automated Vehicles Act 2024**, [contents](https://www.legislation.gov.uk/ukpga/2024/10/contents). Section 47: "User-in-charge not liable for manner of driving." The authorized self-driving entity is responsible. *Checked only through the contents page and a summary of it, not the full section text.*
- **California DMV** issues a "Notice of Autonomous Vehicles Noncompliance" (AVIM 2026-02) to the company, since there is no driver to cite. [DMV AV page](https://www.dmv.ca.gov/portal/vehicle-industry-services/autonomous-vehicles/). *Details not read; not used in the post.*
- **Waymo** [safety impact](https://waymo.com/safety/impact/), through June 2026: 271.3 million rider-only miles, 82% fewer injury crashes and 95% fewer serious-injury-or-worse crashes than human benchmarks. These are Waymo's own numbers.

**Takeaway.** When no human is in the loop, the operator takes the liability. It can do that because it has a published record measured over a very large number of miles.

### Users grant autonomy as trust builds

Anthropic, [Measuring agent autonomy](https://www.anthropic.com/research/measuring-agent-autonomy) (Feb 18, 2026). Auto-approve rises from about 20% of sessions for new users to over 40% for experienced ones. Autonomy is granted step by step as people see the agent's record.

### Not verified (blocked or not found)

- The Air Canada chatbot ruling (CanLII and ABA pages returned 403).
- California AB 1777 (leginfo returned 403).
- The selective labels problem (Lakkaraju et al., KDD 2017) and Manski-style partial-identification bounds. Both are standard references for section 4.3, but neither page was fetched this session. Fetch and check before citing.

---

## 3. The worked case: automating invoice purchases

The author's own client project, described generically.

### The decision

An invoice-factoring company buys freight invoices from small carriers and collects from the shipper later. A purchase can't be taken back once it's made, and bad outcomes show up weeks or months afterward: disputes, short payments, chargebacks under recourse, late payment. Before the project, every invoice went through people and a rules engine, and funding took hours.

The automation had one job: decide which invoices to **buy instantly**. Everything else went to the existing human process. The model never rejected an invoice. It could only move an invoice into a fast lane.

### How the decision was made, step by step

1. **Outcomes defined first.** A good outcome means paid in full and on time. Bad outcomes are listed by name: dispute, short pay, chargeback, write-off, late beyond a set number of days. Each is applied the same way to human and machine decisions. This is what let the team compare human + machine against humans alone, rather than ask whether the model was perfect.
2. **History replayed.** The question was "what would have happened had we rolled this out a year earlier?" An audit table recorded every write to the key tables, so each invoice could be scored on the data **as it stood at that moment**, with no information leaking in from later. Outcomes were the ones actually observed, good or bad. Delayed and right-censored outcomes (invoices not yet closed) were handled explicitly.
3. **Several thresholds, each with its exposure.** Several risk thresholds were simulated, from cautious to aggressive. Each one reported its coverage (share of invoices bought instantly), its expected bad-outcome rate and its dollar exposure, compared with the historical rates of the human process on the same invoices. The choice was a trade between precision and coverage, set by agreed tolerances.
4. **Shadow deployment.** The model ran on live traffic and logged its scores and buy recommendations without acting on them. Reviewers studied the disagreements, especially invoices people had rejected that the model scored as safe.
5. **A/B test at 1%.** Leaving shadow mode required approval from the people who answer for credit losses. Invoices were then randomized into treatment (fast lane on) and control (status quo).
6. **Ramp with a pause rule.** The rollout grew a few client groups a week, starting with the most confident few percent of invoices and widening against the agreed tolerance for bad outcomes. It would pause on any unexpected rise in bad outcomes. One real pause closed a gap in an audit workflow before the ramp continued.
7. **Reason codes for the people handling the rest.** Ops asked for reasons on invoices that didn't qualify, because clients need clear steps to fix a submission.

### Who decided

- **The product manager** owned operational decisions.
- **The people who answer for credit losses** steered the rollout and approved each stage (leaving shadow mode, the A/B test, the ramp).

This mirrors Spotify's split: one party sets what is automated, and another answers for the checks and the outcome.

### What happened

- **Faster.** Instantly bought invoices were funded in seconds to minutes instead of hours. That's a better experience for carriers and less work for the call center.
- **Fewer bad outcomes where it acted.** The fast lane's bad-outcome rates were well below the human process.
- **Fewer disputes overall.** In the A/B test, the treatment arm's **overall** dispute rate fell below the control arm's. This was measured across all invoices, not just the fast lane, so it is a causal system-level effect and not selection.
- **Likely mechanism (the author's reading):** automating the safe invoices freed people to spend their attention on the risky ones.
- **What the simulator missed:** the offline replay projected the overall good-outcome rate to be about unchanged, because it held human behavior fixed. Only the experiment could show the second-order effect.

### The limit the replay could not remove: selective labels

The model scores every submitted invoice, including ones people would have rejected, so some invoices it would auto-buy were rejected in history. Outcomes exist only for invoices that were actually bought. For the rejected ones, nobody knows what would have happened. This is the selective labels problem; credit scoring calls it reject inference.

How it was handled:

- **Bounds in the replay.** For each threshold, the replay used a best guess for the rejected invoices it would have auto-bought, plus a best case and a worst case. The worst case treats every one as a bad outcome. History records which invoices people rejected, so the size of this group is known for each threshold. The width of the bounds follows from that size.
- **The A/B test.** The treatment arm actually buys some invoices people would have rejected, so it measures what the replay could only bound.

---

## 4. When can you decide with confidence what to automate, and how much?

The case had most of the conditions below. Most agent deployments have few of them, and saying which ones are missing is more useful than a general caution.

### 4.1 Conditions that make the decision confident

1. **The automation is a fast lane, not a gate.** It takes on the items it is confident about and hands everything else to the existing process. A wrong "not confident" costs nothing beyond the status quo, so you can start narrow and widen.
2. **Each outcome is objective, gets recorded and can be tied to one decision**, even if it arrives late.
3. **The same outcome measure exists for the human-only process.** Most companies already track aggregate business metrics (dispute rates, CSAT, throughput). What's often missing is per-decision correctness for human work. Without it you can't ask "better than people?" on the same items.
4. **History can be replayed faithfully.** Inputs as they stood at the time, decisions and outcomes are all logged, so a simulator can answer "what if we had done this a year ago?"
5. **The worst single loss is small, and losses add up.** Each decision is small and frequent, and errors don't hit all at once, so averages hold. Here the error-price framing does work. Contrast a driverless car, where one failure can be catastrophic and the evidence has to run to hundreds of millions of miles.
6. **The policy can be undone quickly, even if a single action can't.** Buying an invoice can't be undone, but neither can a person's purchase, so reversibility of the act doesn't separate the options. What matters is that raising the threshold sends work back to people within a day. A better test than "is it reversible?": how large is the worst single loss, can it be priced, and how fast can you stop the policy?
7. **Each step of evidence checks the previous one.** The replay predicts, shadow mode checks the prediction on live data, the A/B test measures cause and effect (and the counterfactuals the replay couldn't see), and the ramp carries a stop rule.
8. **An accountable owner signs off at each gate**, with authority over the threshold. Accountability also reaches the customer through reasons for decisions that went the other way.
9. **Success is measured on the whole system.** The decision compares human + machine with human-only on all the work, not the automated slice alone. Second-order effects can go either way: here people refocused and outcomes improved; elsewhere reviewers may grow complacent.

### 4.2 Conditions that undermine it

- The outcome is subjective, or never observed (a summary nobody checks, advice nobody follows up on).
- One failure can be catastrophic, or failures are correlated (a bad prompt change breaks every output at once).
- No per-decision baseline exists for the human process.
- The environment is adversarial or drifting (fraud, gaming of the decision rule). Note that the case's subject-matter experts already flagged bad actors as a risk.
- No one with authority over the threshold will sign for the outcome. Then a human reviewer becomes a moral crumple zone.

### 4.3 Carrying it over to LLM agents

- **Break the agent's work into decisions** and ask the questions above for each one, not for the agent as a whole. A coding agent's "merge this dependency bump" may qualify, while "merge this refactor" may not.
- **Agent outputs are open-ended**, so "outcome" needs a definition: tests pass, the PR is never reverted, the extracted field matches the source, the customer doesn't reopen the ticket. Spotify's ranking (no PR, failing PR, passing-but-wrong PR) is one such definition.
- **Replay is harder but sometimes possible.** Re-run the agent on past tasks whose results are known: merged PRs, closed tickets, documents already reviewed. Point-in-time inputs matter just as much (repo state at the commit, the knowledge base as of that date).
- **Selective labels apply too.** You never see what would have happened to the output you didn't ship. Shadow mode and small randomized rollouts are how you find out.
- **Users already grant autonomy this way, informally.** Anthropic's autonomy data (auto-approve rising with experience) is the individual version of the staged ramp.

---

## 5. Possible use in the post

**Placement.** The "how much to automate end to end" paragraphs. Either replace the Spotify fleet paragraph with this case or follow it. The Spotify paragraph shows "safe" defined by a check plus split responsibility. This case shows the full staged decision and a system-level result.

**Points to carry, in order:**

1. Outcomes defined the same way for human and machine decisions.
2. A replay of history using data as it stood at each moment.
3. The honest gap bounded, then measured by the experiment. The model scores invoices people rejected too, and their outcomes were never observed.
4. Shadow mode, a small randomized test, and a ramp with a pause rule, each stage approved by the people who answer for credit losses.
5. People shifted their attention to riskier invoices, and overall disputes fell.

**Wording constraints:**

- Call it "an invoice-factoring company."
- No name, no exact percentages.
- No model family.
- Keep "the likely mechanism" hedged as the author's reading.

**Open:** whether to show the threshold-versus-exposure trade as a small figure. It would revisit the cut thought experiment, this time with a real decision behind it.
