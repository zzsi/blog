# Doc AI Museum Design

## Goal

Turn the post `Lessons from a Decade of Document AI Work` into a museum-like companion experience where readers can:

- understand how document AI stacks changed over time
- interact with representative failure modes from each phase
- try small hands-on labs without requiring local setup
- compare deterministic pipelines with modern multi-model and agentic flows

The museum should feel educational and tactile, not like a product demo.

## Product shape

The experience should have three layers:

1. **Post**
The existing blog post remains the main narrative.

2. **Museum**
Static interactive exhibits hosted on GitHub Pages.

3. **Labs**
Google Colab notebooks for readers who want hands-on training or experimentation.

This split keeps GitHub Pages lightweight while still letting readers run code in Colab.

The museum rooms are **not separate blog posts**. They should be subpages or exhibit pages attached to the same post folder.

## Constraints

### What GitHub Pages can host well

- narrative pages
- images, gifs, diagrams
- JavaScript-based interactivity
- precomputed model outputs
- synthetic examples
- sliders, overlays, toggles, inspectors

### What GitHub Pages cannot host well

- server-side inference
- GPU-backed training
- persistent user state
- secure access to API keys
- document upload workflows involving sensitive data

### What Colab is good for

- toy training runs
- small-scale fine-tuning
- OCR / token / bbox inspection
- threshold and policy experiments
- reproducible notebooks readers can fork

## Design principle

Do **not** try to recreate full production systems. The goal is to help readers *feel* why each phase existed, what it solved, and what broke next.

The museum should prioritize:

- representative examples over broad coverage
- precomputed outputs over live inference
- small toy labs over heavyweight training
- failure analysis over leaderboard chasing

## Museum structure

The main essay is the entry point. It has the summary table, the four phases, and exhibit links at the end of each phase section. Readers enter rooms directly from the post. There is no separate landing page.

### Room 1: Templates, Registration, OCR

Purpose:
- show why early systems worked
- show how brittle they were

Must-have interaction (failure demo):
- slider for rotation / skew / blur / crop offset showing extraction breaking as distortion increases, with image registration on/off

Nice-to-have:
- drag crop boxes over expected fields
- show OCR text for cropped field regions

Reader learns:
- why stable forms were tractable
- how small geometric changes break extraction
- why registration quality mattered so much

Minimal assets:
- 2 to 3 synthetic form templates
- clean scan + noisy scan variants
- precomputed OCR outputs

Colab lab:
- `01_templates_and_registration.ipynb`
- synthetic form generation
- image registration demo
- cropped OCR extraction

### Room 2: ConvNet Detector + OCR

Purpose:
- show the improvement over templates
- show detector/OCR boundary pain

Must-have interaction (failure demo):
- toggle between bad anchor setup and fixed anchor setup showing missed/mangled fields and downstream OCR failures side by side

Nice-to-have:
- threshold slider for detections
- anchor-box visualizer

Reader learns:
- why small / elongated fields were hard
- why anchor design mattered
- why detector errors propagate into OCR

Minimal assets:
- real-estate-style synthetic pages
- field boxes for tiny and elongated fields
- precomputed outputs before and after anchor tuning

Colab lab:
- `02_detector_plus_ocr.ipynb`
- tiny object detection example on synthetic data
- compare default vs tuned anchors
- inspect downstream OCR effect

### Room 3: Transformer Models

Purpose:
- show why the task formulation changed
- show why supervision became easier

Must-have interaction:
- click a field question and highlight predicted answer tokens over OCR words and boxes

Nice-to-have:
- toggle between detector-pipeline view and token-classification view
- inspect inverse labeling from final answer to token labels
- show examples where noisy/wrong human labels make the model appear to fail, then reveal the label was wrong

Reader learns:
- how text + layout + visual cues are combined in one model
- why no box labeling was a big deal
- why label quality became more visible, and why auditing labels matters

Minimal assets:
- OCR token overlays
- answer spans
- examples of imperfect human-entered answers

Colab lab:
- `03_transformer_token_classification.ipynb`
- token classification on OCR words
- inverse labeling demo
- label-noise audit exercise

### Room 4: Foundation Models, Orchestration, and Agentic Flow

Purpose:
- show that stronger models changed architecture, not just accuracy

Must-have interaction (failure demo):
- show a document where a VLM confidently hallucinates a field value, then show how validator disagreement and grounding catch it

Nice-to-have:
- compare OCR-only, VLM, and LLM outputs on the same page
- confidence policy curve for coverage vs error
- side-by-side fixed pipeline vs tool-using flow trace

Reader learns:
- why composed systems still win
- how trust depends on validation and routing
- why “just use the API” is not enough
- what “reversal of control” means
- when tool use helps
- why agentic systems still need hard constraints

Minimal assets:
- precomputed outputs from multiple components
- validator examples
- confidence-policy charts
- tool-call traces

Colab lab:
- `04_foundation_and_agentic_stack.ipynb`
- compare OCR and VLM extraction
- structured output validation
- routing and fallback simulation
- compare fixed order vs model-chosen tool sequence

## Interaction model inside the post

The post itself should remain readable without requiring interaction.

Pattern:

- one short exhibit block per phase
- one `Try in Colab` link per phase
- one `Open the museum room` link per phase if split into separate pages

Example:

```md
::: {.callout-note appearance="simple"}
Try it:
- [Open Museum Room 2](./museum/room2-detectors.html)
- [Open Colab Lab 2](https://colab.research.google.com/...)
:::
```

Place these links **at the end of each phase section**, not in the middle. One callout block per phase. They should feel like optional depth, not interruptions to the essay.

## Data strategy

Start from publicly available documents and add light synthesis for noise and variation.

Base document sources:

- **IRS / government forms** (W-2, 1099, I-9): publicly available, structured, good for template and detector phases
- **Receipt datasets** ([SROIE](https://rrc.cvc.uab.es/?ch=13), [CORD](https://github.com/clovaai/cord)): directly matches the receipt example in the post
- **Synthetic invoices**: generated with varied layouts, no privacy risk, full control over complexity

Light synthesis to apply on top:

- skew, rotation, blur
- compression artifacts, scanner noise
- stamps, handwritten notes
- field shape variation
- multi-page layouts

Avoid:

- real client documents
- anything with privacy risk
- workflows requiring upload of user documents

The museum should reuse the same synthetic-data philosophy described in the post (printing artifacts, scanner noise, paper distortion, stamps, handwriting overlays) but implemented as simple standalone scripts, not production tooling.

## Implementation plan

### Phase 1: Static museum MVP

Deliver:

- one page per room (no separate landing page; the post is the entry point)
- precomputed outputs only
- simple JavaScript interactivity

Tech:

- Quarto pages or static HTML pages under the post folder
- plain JavaScript
- SVG / canvas overlays where needed

### Phase 2: Colab labs

Deliver:

- four notebooks
- synthetic datasets embedded or downloadable
- no credentials required

Notebook constraints:

- target free Colab when possible
- target runtime under 10 minutes per notebook when possible
- 15 minutes max for the core path
- prefer T4-compatible workloads
- no gated weights
- no paid API requirement for the core experience
- useful even if the reader only runs the first few sections

### Phase 3: Tight integration with the post

Deliver:

- inline exhibit links at the end of each phase section
- small screenshots / gifs from each museum room embedded in the post

## File layout proposal

Within `posts/20260331-practical-doc-ai/`:

```text
posts/20260331-practical-doc-ai/
  index.qmd
  docai_museum_design.md
  museum/
    room1-templates.qmd
    room2-detectors.qmd
    room3-transformers.qmd
    room4-foundation-and-agentic.qmd
    assets/
      *.png
      *.json
      *.js
  colab/
    README.md
```

These museum files should be treated as exhibit pages within the same article package, not as separate dated posts in the blog index.

Actual Colab notebooks can live in:

- a dedicated repo for notebooks, or
- `examples/docai-museum/` if you want them versioned here

GitHub Pages should link out to the hosted Colab URLs.

## MVP recommendation

Start smaller than the full vision.

Best first version:

- Room 1 templates
- Room 2 detector + OCR
- Room 3 transformer token classification
- one Colab notebook for each of those three rooms

Why:

- strongest educational value
- directly tied to the historical progression in the post
- can be built mostly with synthetic data
- avoids needing frontier-model APIs in the first release

Then add:

- Room 4 foundation + agentic stack

## Device support

This experience should be **desktop-first**.

- mobile should support reading
- light tapping and image viewing should work on mobile
- detailed overlays, sliders, and Colab labs should be assumed desktop/laptop first

Do not over-optimize the MVP for touch interactions.

## Success criteria

The museum is successful if a reader can walk away with these intuitions:

- why templates worked and why they broke
- why detector + OCR was a step forward and also a pain
- why transformer models changed the task formulation
- why foundation models did not eliminate systems engineering
- why confidence policy and validation matter as much as raw model quality
- why agentic flow changes control, but not responsibility

## Non-goals

- full production training stack
- general document upload service
- enterprise product demo
- benchmarking museum visitors against each other
- recreating every model faithfully

## Recommendation

This is feasible and worth doing if scoped as:

- static museum on GitHub Pages
- Colab for hands-on labs
- precomputed outputs for anything heavy
- synthetic data for most examples

The wrong version is “build a full platform.”

The right version is “build a sequence of small, vivid exhibits that make the bottlenecks tangible.”
