# mcp-multitenant-saas

Runnable multi-tenant MCP server with Streamable HTTP transport.

Demo dataset: `../mcp-shared/data/invoices.csv`

## What this demo includes

- Streamable HTTP server (primary): `src/server-http.ts`
- stdio server (secondary): `src/server-stdio.ts`
- Tenant-aware tools:
  - `get_tenant_invoice`
  - `list_tenant_open_invoices`
- JWT auth with required claims:
  - `tenant_id` (or `tid`)
  - scope includes `invoices:read`

## Quick start

1. Install dependencies:

```bash
npm install
```

2. Configure env:

```bash
export AUTH_MODE=jwt
export AUTH_PROVIDER=shared_secret
export JWT_SECRET='replace_with_long_random_secret'
export MCP_PORT=3001
export STORAGE_MODE=file
export INVOICES_FILE='.demo-data/invoices_multitenant.json'
```

3. Run server:

```bash
npm run seed
npm run dev:http
```

Server endpoint: `http://localhost:3001/mcp`

## Exec demo script

Run a deterministic end-to-end demo:

```bash
./scripts/demo.sh
```

## Simple walkthrough

1. Start server:

```bash
export AUTH_MODE=jwt
export AUTH_PROVIDER=shared_secret
export JWT_SECRET='demo-secret'
export MCP_PORT=3001
npm run dev:http
```

2. In another terminal, run this client script:

```bash
node --input-type=module <<'EOF'
import { SignJWT } from "jose";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";

const secret = new TextEncoder().encode("demo-secret");
const token = await new SignJWT({
  tenant_id: "t1",
  scope: "invoices:read",
  client_id: "client-t1",
})
  .setProtectedHeader({ alg: "HS256" })
  .setSubject("user-t1")
  .setIssuedAt()
  .setExpirationTime("10m")
  .sign(secret);

const client = new Client({ name: "demo-client", version: "0.1.0" });
const transport = new StreamableHTTPClientTransport(new URL("http://localhost:3001/mcp"), {
  requestInit: { headers: { Authorization: `Bearer ${token}` } },
});
await client.connect(transport);

const list = await client.callTool({
  name: "list_tenant_open_invoices",
  arguments: { limit: 5 },
});
console.log("list_tenant_open_invoices:", JSON.stringify(list.structuredContent, null, 2));

const cross = await client.callTool({
  // `inv_10029` belongs to tenant `t2` in this demo mapping
  name: "get_tenant_invoice",
  arguments: { invoiceId: "inv_10029" },
});
console.log("get_tenant_invoice_cross_tenant:", JSON.stringify(cross, null, 2));

await client.close();
EOF
```

3. Expected results:

- `list_tenant_open_invoices` returns invoices with `"tenant_id": "t1"` only.
- cross-tenant `get_tenant_invoice` returns error content with `forbidden: cross-tenant access`.
- server stderr includes structured `authz_decision` logs.
- seeded tenant-scoped invoice data persists across restarts when `STORAGE_MODE=file`.

## Hardened mode (OIDC/JWKS)

Use your IdP keys and strict issuer/audience checks:

```bash
export AUTH_MODE=jwt
export AUTH_PROVIDER=oidc_jwks
export OIDC_JWKS_URI='https://your-idp.example.com/.well-known/jwks.json'
export JWT_ISSUER='https://your-idp.example.com/'
export JWT_AUDIENCE='your-mcp-api-audience'
export MCP_PORT=3001
npm run dev:http
```

Expected behavior:

- Tokens are verified via remote JWKS.
- `tenant_id` (or `tid`) claim is still required.
- Tenant and scope checks are unchanged (`invoices:read`, cross-tenant denied).

## Notes

- Streamable HTTP is the production-recommended transport for remote MCP servers.
- This demo keeps tenant identity in JWT claims for clarity; production systems should align claims with your IdP standards.
- Demo durability mode uses file-backed seeded data via `STORAGE_MODE=file`.
