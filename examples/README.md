# MCP Examples

Runnable MCP scenarios for the blog post: "How to Build and Deploy MCP for Proprietary Data".

## Demo Matrix

| Example | Story | One-command demo | What to expect |
|---|---|---|---|
| `mcp-readonly-starter` | Single-tenant read-only MCP | `cd examples/mcp-readonly-starter && ./scripts/demo.sh` | Returns invoice payload for `inv_10002` |
| `mcp-multitenant-saas` | Tenant isolation and authz | `cd examples/mcp-multitenant-saas && ./scripts/demo.sh` | Tenant-scoped list succeeds; cross-tenant read is denied |
| `mcp-write-with-approval` | Write workflow with approval gate | `cd examples/mcp-write-with-approval && ./scripts/demo.sh` | Execute fails before approval, then succeeds after approval |
| `mcp-onprem-bridge` | Pull-based bridge for on-prem data | `cd examples/mcp-onprem-bridge && ./scripts/demo.sh` | Request is queued, bridge agent runs, result becomes `completed` |
| `mcp-compliance-audit` | Compliance-first policy and observability | `cd examples/mcp-compliance-audit && ./scripts/demo.sh` | Redacted audit records and control status response |
| `optimizer-bench` | Cross-task optimizer comparison (CIFAR-10 + nanochat) | `cd examples/optimizer-bench && ./scripts/run_cifar_all.sh` | Trains six optimizers under one codepath with consistent configs |

## Notes

- Each demo script starts the server(s), runs a deterministic client flow, and exits.
- Demo scripts print service logs to `/tmp/*demo.log` for quick troubleshooting.
- If dependencies are missing in an example, run `npm install` in that example first.
- `optimizer-bench` is Python-based; use its `requirements.txt` setup instructions.
