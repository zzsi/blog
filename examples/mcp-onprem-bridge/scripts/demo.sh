#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

export MCP_PORT="${MCP_PORT:-3003}"
export AUTH_MODE=jwt
export AUTH_PROVIDER=shared_secret
export JWT_SECRET="${JWT_SECRET:-demo-secret}"
export BRIDGE_AGENT_TOKEN="${BRIDGE_AGENT_TOKEN:-bridge-agent-demo-token}"
export JOB_SIGNING_SECRET="${JOB_SIGNING_SECRET:-job-signing-demo-secret}"
export CONTROL_PLANE_URL="${CONTROL_PLANE_URL:-http://localhost:${MCP_PORT}}"

REQUEST_ID_FILE="$(mktemp /tmp/mcp-onprem-request-id.XXXXXX)"
export REQUEST_ID_FILE

npm run dev:control-plane >/tmp/mcp-onprem-control-plane-demo.log 2>&1 &
CONTROL_PID=$!
cleanup() {
  kill "$CONTROL_PID" >/dev/null 2>&1 || true
  rm -f "$REQUEST_ID_FILE" >/dev/null 2>&1 || true
}
trap cleanup EXIT

sleep 2

node --input-type=module <<'EOF2'
import { writeFile } from "node:fs/promises";
import { SignJWT } from "jose";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";

const port = process.env.MCP_PORT ?? "3003";
const secret = new TextEncoder().encode(process.env.JWT_SECRET ?? "demo-secret");
const token = await new SignJWT({ scope: "bridge:request bridge:read", client_id: "onprem-demo-client" })
  .setProtectedHeader({ alg: "HS256" })
  .setSubject("onprem-demo-client")
  .setIssuedAt()
  .setExpirationTime("10m")
  .sign(secret);

const client = new Client({ name: "onprem-demo-client", version: "0.1.0" });
const transport = new StreamableHTTPClientTransport(new URL(`http://localhost:${port}/mcp`), {
  requestInit: { headers: { Authorization: `Bearer ${token}` } },
});
await client.connect(transport);

const queued = await client.callTool({
  name: "query_customer_data",
  arguments: {
    customerId: "cust_100",
    resource: "invoice",
    idempotencyKey: "exec-demo-cust100-001",
  },
});
console.log("queued", JSON.stringify(queued.structuredContent, null, 2));

const requestId = String(queued.structuredContent.requestId);
await writeFile(String(process.env.REQUEST_ID_FILE), requestId, "utf8");

const before = await client.callTool({ name: "get_bridge_result", arguments: { requestId } });
console.log("before_agent", JSON.stringify(before.structuredContent, null, 2));
await client.close();
EOF2

npm run dev:bridge-agent -- --once

node --input-type=module <<'EOF3'
import { readFile } from "node:fs/promises";
import { SignJWT } from "jose";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";

const port = process.env.MCP_PORT ?? "3003";
const secret = new TextEncoder().encode(process.env.JWT_SECRET ?? "demo-secret");
const requestId = (await readFile(String(process.env.REQUEST_ID_FILE), "utf8")).trim();
const token = await new SignJWT({ scope: "bridge:request bridge:read", client_id: "onprem-demo-client" })
  .setProtectedHeader({ alg: "HS256" })
  .setSubject("onprem-demo-client")
  .setIssuedAt()
  .setExpirationTime("10m")
  .sign(secret);

const client = new Client({ name: "onprem-demo-client", version: "0.1.0" });
const transport = new StreamableHTTPClientTransport(new URL(`http://localhost:${port}/mcp`), {
  requestInit: { headers: { Authorization: `Bearer ${token}` } },
});
await client.connect(transport);

const after = await client.callTool({ name: "get_bridge_result", arguments: { requestId } });
console.log("after_agent", JSON.stringify(after.structuredContent, null, 2));
await client.close();
EOF3

echo "Demo complete. Logs: /tmp/mcp-onprem-control-plane-demo.log"
