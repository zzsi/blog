#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

export AUTH_MODE=jwt
export AUTH_PROVIDER=shared_secret
export JWT_SECRET="${JWT_SECRET:-demo-secret}"
export MCP_PORT="${MCP_PORT:-3005}"
export STORAGE_MODE="${STORAGE_MODE:-file}"
export COMPLIANCE_EVENTS_FILE="${COMPLIANCE_EVENTS_FILE:-.demo-data/compliance_events.json}"

npm run seed >/tmp/mcp-compliance-seed.log 2>&1

npm run dev:http >/tmp/mcp-compliance-demo.log 2>&1 &
SERVER_PID=$!
cleanup() {
  kill "$SERVER_PID" >/dev/null 2>&1 || true
}
trap cleanup EXIT

sleep 2

node --input-type=module <<'EOF2'
import { SignJWT } from "jose";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";

const port = process.env.MCP_PORT ?? "3005";
const secret = new TextEncoder().encode(process.env.JWT_SECRET ?? "demo-secret");

const token = await new SignJWT({
  scope: "compliance:audit:read compliance:control:read",
  client_id: "compliance-demo",
})
  .setProtectedHeader({ alg: "HS256" })
  .setSubject("compliance-demo")
  .setIssuedAt()
  .setExpirationTime("10m")
  .sign(secret);

const client = new Client({ name: "compliance-demo-client", version: "0.1.0" });
const transport = new StreamableHTTPClientTransport(new URL(`http://localhost:${port}/mcp`), {
  requestInit: { headers: { Authorization: `Bearer ${token}` } },
});

await client.connect(transport);
const events = await client.callTool({ name: "list_audit_events", arguments: { tenantId: "t1", limit: 5 } });
console.log("list_audit_events", JSON.stringify(events.structuredContent, null, 2));

const control = await client.callTool({ name: "get_control_status", arguments: { controlId: "log_redaction" } });
console.log("get_control_status", JSON.stringify(control.structuredContent, null, 2));
await client.close();
EOF2

echo "Demo complete. Server log: /tmp/mcp-compliance-demo.log"
