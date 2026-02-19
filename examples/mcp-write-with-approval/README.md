# mcp-write-with-approval

Runnable write-capable MCP workflow with explicit approval gates.

## What this demo includes

- Streamable HTTP server (primary): `src/server-http.ts`
- stdio server (secondary): `src/server-stdio.ts`
- Three-stage tools:
  - `create_refund_request` (intent)
  - `approve_refund_request` (approval)
  - `execute_refund` (side-effect execution)
- Distinct scopes for each stage:
  - `refund:request`
  - `refund:approve`
  - `refund:execute`

## Quick start

1. Install dependencies:

```bash
npm install
```

2. Configure env:

```bash
export AUTH_MODE=jwt
export AUTH_PROVIDER=shared_secret
export JWT_SECRET='demo-secret'
export MCP_PORT=3002
```

3. Run server:

```bash
npm run dev:http
```

Server endpoint: `http://localhost:3002/mcp`

## Exec demo script

Run a deterministic end-to-end demo:

```bash
./scripts/demo.sh
```

## Simple walkthrough

1. Start server with the env above.

2. In another terminal, run:

```bash
node --input-type=module <<'EOF2'
import { SignJWT } from "jose";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";

const secret = new TextEncoder().encode("demo-secret");

async function token(scope, clientId) {
  return await new SignJWT({ scope, client_id: clientId })
    .setProtectedHeader({ alg: "HS256" })
    .setSubject(clientId)
    .setIssuedAt()
    .setExpirationTime("10m")
    .sign(secret);
}

async function call(scope, fn) {
  const client = new Client({ name: "demo-" + scope, version: "0.1.0" });
  const t = await token(scope, "client-" + scope);
  const transport = new StreamableHTTPClientTransport(new URL("http://localhost:3002/mcp"), {
    requestInit: { headers: { Authorization: "Bearer " + t } },
  });
  await client.connect(transport);
  try {
    return await fn(client);
  } finally {
    await client.close();
  }
}

const created = await call("refund:request", (c) =>
  c.callTool({
    name: "create_refund_request",
    arguments: {
      orderId: "ord_demo123",
      amountCents: 99000,
      reason: "Customer reported duplicate charge",
    },
  }),
);

const requestId = created.structuredContent.requestId;
console.log("created:", created.structuredContent);

const denied = await call("refund:execute", (c) =>
  c.callTool({ name: "execute_refund", arguments: { requestId } }),
);
console.log("execute_before_approval:", denied);

const approved = await call("refund:approve", (c) =>
  c.callTool({ name: "approve_refund_request", arguments: { requestId } }),
);
console.log("approved:", approved.structuredContent);

const executed = await call("refund:execute", (c) =>
  c.callTool({ name: "execute_refund", arguments: { requestId } }),
);
console.log("executed:", executed.structuredContent);
EOF2
```

3. Expected behavior:

- `create_refund_request` returns a `requestId` and `pending_approval` status.
- `execute_refund` fails before approval.
- `approve_refund_request` moves request to `approved`.
- `execute_refund` succeeds only after approval.
- server stderr logs each workflow event as `refund_workflow`.

## Hardened mode (OIDC/JWKS)

```bash
export AUTH_MODE=jwt
export AUTH_PROVIDER=oidc_jwks
export OIDC_JWKS_URI='https://your-idp.example.com/.well-known/jwks.json'
export JWT_ISSUER='https://your-idp.example.com/'
export JWT_AUDIENCE='your-mcp-api-audience'
export MCP_PORT=3002
npm run dev:http
```

## Notes

- This demo uses in-memory state for clarity; replace with a durable store in production.
- Keep scope separation strict in production to reduce blast radius.
