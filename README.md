
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