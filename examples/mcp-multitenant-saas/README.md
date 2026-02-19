# mcp-multitenant-saas

Reference layout for a multi-tenant MCP deployment.

Demo dataset: `../mcp-shared/data/invoices.csv`

## Security defaults
- Tenant context from token claims
- Mandatory tenant checks on every tool call
- Per-tenant routing and quotas
