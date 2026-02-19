# mcp-readonly-starter

Runnable single-tenant read-only MCP server.

Demo dataset: `../mcp-shared/data/invoices.csv`

## What this demo includes

- Streamable HTTP server (primary): `src/server-http.ts`
- stdio server (secondary, local tooling): `src/server-stdio.ts`
- Tools:
  - `get_invoice_status`
  - `list_open_invoices`
- Optional JWT auth mode for HTTP transport (`AUTH_MODE=jwt`)
- Structured audit logs to stderr

## Quick start

1. Install dependencies:

```bash
npm install
```

2. Run Streamable HTTP server (recommended):

```bash
npm run dev:http
```

The server runs on `http://localhost:3000/mcp` by default.

3. Optional: run stdio transport:

```bash
npm run dev:stdio
```

## Simple walkthrough (no auth)

1. Start server:

```bash
npm run dev:http
```

2. In another terminal, call a tool:

```bash
node --input-type=module <<'EOF'
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";

const client = new Client({ name: "demo-client", version: "0.1.0" });
const transport = new StreamableHTTPClientTransport(new URL("http://localhost:3000/mcp"));
await client.connect(transport);

const result = await client.callTool({
  name: "get_invoice_status",
  arguments: { invoiceId: "inv_10002" },
});

console.log(result.structuredContent);
await client.close();
EOF
```

3. Expected result:

- `structuredContent` contains invoice metadata for `inv_10002`.
- Server stderr includes an audit log entry with `"decision":"allow"`.

## JWT mode for HTTP

1. Configure env vars:

```bash
export AUTH_MODE=jwt
export AUTH_PROVIDER=shared_secret
export JWT_SECRET='replace_with_long_random_secret'
# optional
export JWT_ISSUER='demo-issuer'
export JWT_AUDIENCE='demo-audience'
```

2. Start server:

```bash
npm run dev:http
```

JWTs must include `scope` containing `invoices:read`.

3. Expected behavior:

- With scope `invoices:read`, tool calls succeed.
- Without that scope, tool calls fail and the server logs `"decision":"deny"` with `missing scope invoices:read`.

## Hardened mode (OIDC/JWKS)

For a more realistic production setup, switch token verification from shared secret to OIDC JWKS:

```bash
export AUTH_MODE=jwt
export AUTH_PROVIDER=oidc_jwks
export OIDC_JWKS_URI='https://your-idp.example.com/.well-known/jwks.json'
export JWT_ISSUER='https://your-idp.example.com/'
export JWT_AUDIENCE='your-mcp-api-audience'
npm run dev:http
```

Expected behavior:

- Tokens are validated against your IdP JWKS keys.
- `iss` and `aud` must match `JWT_ISSUER` and `JWT_AUDIENCE`.
- Scope enforcement stays the same (`invoices:read`).

## Notes

- Streamable HTTP is the production-recommended transport for remote MCP servers.
- stdio is useful for local process-spawned integrations.
