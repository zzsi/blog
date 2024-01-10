
Continuous deployment is set up so that a push a main triggers publishing to https://zzsi.github.io/blog/.

### Updating the content

The starting point is `index.qmd` and `_quarto.yml`.

Build locally with VSCode quarto plugin: from the command pallete, run "Quarto: Render Project".

Or, with `quarto` CLI:
```
quarto preview --render all # this watches for changes
```

### Set up

Created using [this example](https://github.com/quarto-dev/quarto-actions/blob/main/examples/example-01-basics.md).

Permissions: make sure in settings/actions, under "Workflow Permissions", check "Read and Write permissions".

### TODO

- Practical AI: what does it mean? Why is it different from traditional software engineering (recipe unknown vs. knonw, research involved)? Why is it different from publication-driven research?
- Multimodal AI can be a big driver of business value, as business data (transactions, documents, status changes, classifications, images, videos) is multi-modal.