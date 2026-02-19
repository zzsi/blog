#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

export AUTH_MODE=jwt
export AUTH_PROVIDER=shared_secret
export JWT_SECRET="${JWT_SECRET:-demo-secret}"
export MCP_PORT="${MCP_PORT:-3000}"

npm run dev:http >/tmp/mcp-readonly-demo.log 2>&1 &
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

const port = process.env.MCP_PORT ?? "3000";
const secret = new TextEncoder().encode(process.env.JWT_SECRET ?? "demo-secret");

const token = await new SignJWT({ scope: "invoices:read", client_id: "readonly-demo" })
  .setProtectedHeader({ alg: "HS256" })
  .setSubject("readonly-demo")
  .setIssuedAt()
  .setExpirationTime("10m")
  .sign(secret);

const client = new Client({ name: "readonly-demo-client", version: "0.1.0" });
const transport = new StreamableHTTPClientTransport(new URL(`http://localhost:${port}/mcp`), {
  requestInit: { headers: { Authorization: `Bearer ${token}` } },
});

await client.connect(transport);
const result = await client.callTool({ name: "get_invoice_status", arguments: { invoiceId: "inv_10002" } });
console.log(JSON.stringify(result.structuredContent, null, 2));
await client.close();
EOF2

echo "Demo complete. Server log: /tmp/mcp-readonly-demo.log"
