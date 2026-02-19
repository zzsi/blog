#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

export AUTH_MODE=jwt
export AUTH_PROVIDER=shared_secret
export JWT_SECRET="${JWT_SECRET:-demo-secret}"
export MCP_PORT="${MCP_PORT:-3002}"

npm run dev:http >/tmp/mcp-write-approval-demo.log 2>&1 &
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

const port = process.env.MCP_PORT ?? "3002";
const secret = new TextEncoder().encode(process.env.JWT_SECRET ?? "demo-secret");

async function token(scope, clientId) {
  return await new SignJWT({ scope, client_id: clientId })
    .setProtectedHeader({ alg: "HS256" })
    .setSubject(clientId)
    .setIssuedAt()
    .setExpirationTime("10m")
    .sign(secret);
}

async function call(scope, fn) {
  const clientId = `demo-${scope}`;
  const t = await token(scope, clientId);
  const client = new Client({ name: clientId, version: "0.1.0" });
  const transport = new StreamableHTTPClientTransport(new URL(`http://localhost:${port}/mcp`), {
    requestInit: { headers: { Authorization: `Bearer ${t}` } },
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
      orderId: "ord_demo001",
      amountCents: 99000,
      reason: "Duplicate charge",
    },
  }),
);

const requestId = created.structuredContent.requestId;
console.log("created", JSON.stringify(created.structuredContent, null, 2));

const pre = await call("refund:execute", (c) => c.callTool({ name: "execute_refund", arguments: { requestId } }));
console.log("execute_before_approval", JSON.stringify(pre, null, 2));

const approved = await call("refund:approve", (c) => c.callTool({ name: "approve_refund_request", arguments: { requestId } }));
console.log("approved", JSON.stringify(approved.structuredContent, null, 2));

const executed = await call("refund:execute", (c) => c.callTool({ name: "execute_refund", arguments: { requestId } }));
console.log("executed", JSON.stringify(executed.structuredContent, null, 2));
EOF2

echo "Demo complete. Server log: /tmp/mcp-write-approval-demo.log"
