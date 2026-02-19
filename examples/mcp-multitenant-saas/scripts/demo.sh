#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

export AUTH_MODE=jwt
export AUTH_PROVIDER=shared_secret
export JWT_SECRET="${JWT_SECRET:-demo-secret}"
export MCP_PORT="${MCP_PORT:-3001}"

npm run dev:http >/tmp/mcp-multitenant-demo.log 2>&1 &
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

const port = process.env.MCP_PORT ?? "3001";
const secret = new TextEncoder().encode(process.env.JWT_SECRET ?? "demo-secret");

const token = await new SignJWT({ tenant_id: "t1", scope: "invoices:read", client_id: "tenant-demo" })
  .setProtectedHeader({ alg: "HS256" })
  .setSubject("tenant-demo")
  .setIssuedAt()
  .setExpirationTime("10m")
  .sign(secret);

const client = new Client({ name: "multitenant-demo-client", version: "0.1.0" });
const transport = new StreamableHTTPClientTransport(new URL(`http://localhost:${port}/mcp`), {
  requestInit: { headers: { Authorization: `Bearer ${token}` } },
});

await client.connect(transport);
const list = await client.callTool({ name: "list_tenant_open_invoices", arguments: { limit: 3 } });
console.log("list_tenant_open_invoices", JSON.stringify(list.structuredContent, null, 2));

const crossTenant = await client.callTool({ name: "get_tenant_invoice", arguments: { invoiceId: "inv_10029" } });
console.log("get_tenant_invoice_cross_tenant", JSON.stringify(crossTenant, null, 2));

await client.close();
EOF2

echo "Demo complete. Server log: /tmp/mcp-multitenant-demo.log"
