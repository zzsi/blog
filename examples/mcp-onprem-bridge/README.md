# mcp-onprem-bridge

Runnable on-prem bridge MCP pattern:

- cloud-hosted control-plane MCP server
- pull-based bridge agent inside customer network
- signed jobs and signed result submission
- basic ops endpoints for health and queue visibility

## What this demo includes

- Control-plane server (Streamable HTTP MCP + bridge API): `src/control-plane-server.ts`
- Bridge agent poller: `src/bridge-agent.ts`
- MCP tools:
  - `query_customer_data` (queue bridge job)
  - `get_bridge_result` (read status/result)
- Ops endpoints:
  - `GET /healthz` (liveness)
  - `GET /readyz` (readiness + auth mode)
  - `GET /bridge/stats` (queue/job counts; requires bridge bearer token)

## Security defaults in this demo

- Pull model (no inbound callback to customer environment)
- Bridge API protected with bearer agent token
- Job payload signed by control-plane (`JOB_SIGNING_SECRET`)
- Result payload signed by bridge agent (`JOB_SIGNING_SECRET`)
- MCP access token required for tool use

## Quick start

1. Install dependencies:

```bash
npm install
```

2. Configure env:

```bash
export MCP_PORT=3003
export AUTH_MODE=jwt
export AUTH_PROVIDER=shared_secret
export JWT_SECRET='demo-secret'
export BRIDGE_AGENT_TOKEN='bridge-agent-demo-token'
export JOB_SIGNING_SECRET='job-signing-demo-secret'
export CONTROL_PLANE_URL='http://localhost:3003'
```

3. Start control-plane:

```bash
npm run dev:control-plane
```

4. In another terminal, run bridge agent once:

```bash
npm run dev:bridge-agent -- --once
```

## Exec demo script

Run a deterministic end-to-end demo:

```bash
./scripts/demo.sh
```

## One-command startup (Docker Compose)

Run both control-plane and bridge-agent:

```bash
docker compose up --build
```

What to expect:

- `control-plane` starts on `http://localhost:3003`.
- `bridge-agent` starts polling automatically and processes queued jobs.

Stop the demo:

```bash
docker compose down
```

## Simple walkthrough

In a separate terminal, run this client script to queue and fetch results:

```bash
node --input-type=module <<'EOF2'
import { SignJWT } from "jose";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";

const secret = new TextEncoder().encode("demo-secret");
const token = await new SignJWT({ scope: "bridge:request bridge:read", client_id: "mcp-client" })
  .setProtectedHeader({ alg: "HS256" })
  .setSubject("mcp-client")
  .setIssuedAt()
  .setExpirationTime("10m")
  .sign(secret);

const client = new Client({ name: "bridge-demo-client", version: "0.1.0" });
const transport = new StreamableHTTPClientTransport(new URL("http://localhost:3003/mcp"), {
  requestInit: { headers: { Authorization: "Bearer " + token } },
});

await client.connect(transport);

const queued = await client.callTool({
  name: "query_customer_data",
  arguments: {
    customerId: "cust_100",
    resource: "invoice",
    idempotencyKey: "demo-cust100-invoice-001"
  },
});
console.log("queued:", queued.structuredContent);

const requestId = queued.structuredContent.requestId;

const first = await client.callTool({ name: "get_bridge_result", arguments: { requestId } });
console.log("first_result_check:", first.structuredContent);

console.log("Run bridge agent now: npm run dev:bridge-agent -- --once");

const second = await client.callTool({ name: "get_bridge_result", arguments: { requestId } });
console.log("second_result_check:", second.structuredContent);

await client.close();
EOF2
```

Expected behavior:

- `query_customer_data` returns `queued_for_bridge` and a `requestId`.
- repeating the same `idempotencyKey` returns `duplicate_request_reused` and the same job/request IDs.
- with `docker compose up`, first result check may already be `completed` because the bridge agent is always running.
- with manual local mode, first result check usually returns `queued` or `processing`, and after running bridge agent once it returns `completed`.

Optional stats check:

```bash
curl -s http://localhost:3003/bridge/stats \
  -H "Authorization: Bearer bridge-agent-demo-token" | jq
```

## Hardened mode (OIDC/JWKS for MCP)

```bash
export AUTH_MODE=jwt
export AUTH_PROVIDER=oidc_jwks
export OIDC_JWKS_URI='https://your-idp.example.com/.well-known/jwks.json'
export JWT_ISSUER='https://your-idp.example.com/'
export JWT_AUDIENCE='your-mcp-api-audience'
npm run dev:control-plane
```

## Notes

- This demo uses in-memory stores; production should use durable queues/stores.
- Bridge agent uses mock data (`src/data/mock_onprem_data.ts`) to emulate customer-local systems.
