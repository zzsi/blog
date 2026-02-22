# mcp-compliance-audit

Runnable high-compliance MCP server focused on policy and observability controls.

## What this demo includes

- Streamable HTTP server (primary): `src/server-http.ts`
- stdio server (secondary): `src/server-stdio.ts`
- Compliance tools:
  - `list_audit_events` (returns redacted audit records)
  - `get_control_status` (control evidence with secrets adapter access)
- Deny-by-default scope policy per tool
- Structured audit logs with automatic credential redaction

## Security defaults in this demo

- Deny-by-default authorization matrix
- Scope checks on every tool call
- Centralized secret access adapter with access audit
- Recursive redaction for secret-like keys in logs and payloads

## Quick start

1. Install dependencies:

```bash
npm install
```

2. Configure env:

```bash
export MCP_PORT=3005
export AUTH_MODE=jwt
export AUTH_PROVIDER=shared_secret
export JWT_SECRET='demo-secret'
export STORAGE_MODE=file
export COMPLIANCE_EVENTS_FILE='.demo-data/compliance_events.json'
```

3. Start server:

```bash
npm run seed
npm run dev:http
```

Server endpoint: `http://localhost:3005/mcp`

## Exec demo script

Run a deterministic end-to-end demo:

```bash
./scripts/demo.sh
```

## Simple walkthrough

In another terminal run:

```bash
node --input-type=module <<'EOF2'
import { SignJWT } from "jose";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";

const secret = new TextEncoder().encode("demo-secret");
const token = await new SignJWT({
  scope: "compliance:audit:read compliance:control:read",
  client_id: "compliance-auditor",
})
  .setProtectedHeader({ alg: "HS256" })
  .setSubject("auditor-1")
  .setIssuedAt()
  .setExpirationTime("10m")
  .sign(secret);

const client = new Client({ name: "compliance-demo", version: "0.1.0" });
const transport = new StreamableHTTPClientTransport(new URL("http://localhost:3005/mcp"), {
  requestInit: { headers: { Authorization: `Bearer ${token}` } },
});

await client.connect(transport);

const events = await client.callTool({
  name: "list_audit_events",
  arguments: { tenantId: "t1", limit: 5 },
});
console.log("list_audit_events:", JSON.stringify(events.structuredContent, null, 2));

const control = await client.callTool({
  name: "get_control_status",
  arguments: { controlId: "log_redaction" },
});
console.log("get_control_status:", JSON.stringify(control.structuredContent, null, 2));

await client.close();
EOF2
```

Expected behavior:

- `list_audit_events` returns events with secret fields redacted (e.g., token, authorization).
- `get_control_status` returns control status and a secret reference, not secret values.
- server stderr logs structured `event:"audit"` entries for each tool call.
- seeded compliance events persist across restarts when `STORAGE_MODE=file`.

## Hardened mode (OIDC/JWKS)

```bash
export AUTH_MODE=jwt
export AUTH_PROVIDER=oidc_jwks
export OIDC_JWKS_URI='https://your-idp.example.com/.well-known/jwks.json'
export JWT_ISSUER='https://your-idp.example.com/'
export JWT_AUDIENCE='your-mcp-api-audience'
npm run dev:http
```

## Notes

- This demo supports file-backed seeded events for deterministic, restart-safe demos via `STORAGE_MODE=file`.
- It demonstrates compliance controls; production should add durable storage and retention workflows.
