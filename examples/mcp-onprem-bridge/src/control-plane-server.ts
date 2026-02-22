import { createMcpExpressApp } from "@modelcontextprotocol/sdk/server/express.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import * as z from "zod/v4";
import { requireBearerAuth } from "@modelcontextprotocol/sdk/server/auth/middleware/bearerAuth.js";
import { loadConfig } from "./config/index.js";
import { createJwtVerifier } from "./auth/jwt_verifier.js";
import { BridgeJobStore, createFileBackedBridgeJobStore } from "./workflows/job_store.js";
import { createBridgeHandlers, requireBridgeAgentToken } from "./bridge/http_handlers.js";
import { getBridgeResultTool, queryCustomerDataTool } from "./mcp/tools.js";

const config = loadConfig();
const app = createMcpExpressApp();
const store = config.storageMode === "file"
  ? createFileBackedBridgeJobStore(config.stateFile)
  : new BridgeJobStore();

const verifier = config.authProvider === "oidc_jwks"
  ? createJwtVerifier({ mode: "oidc_jwks", jwksUri: config.oidcJwksUri!, issuer: config.jwtIssuer!, audience: config.jwtAudience! })
  : createJwtVerifier({ mode: "shared_secret", secret: config.jwtSecret!, issuer: config.jwtIssuer, audience: config.jwtAudience });

const mcpAuth = requireBearerAuth({ verifier, requiredScopes: [] });

function createMcpServer() {
  const server = new McpServer({ name: "mcp-onprem-bridge-control-plane", version: "0.1.0" }, { capabilities: { logging: {} } });

  server.registerTool(
    "query_customer_data",
    {
      description: "Queue an on-prem bridge request for customer data",
      inputSchema: {
        customerId: z.string().regex(/^cust_[0-9]+$/),
        resource: z.enum(["invoice", "contract"]),
      },
    },
    async (args, extra) => queryCustomerDataTool(store)(args, extra),
  );

  server.registerTool(
    "get_bridge_result",
    {
      description: "Read result for a queued bridge request",
      inputSchema: {
        requestId: z.string().regex(/^req_[a-zA-Z0-9_]+$/),
      },
    },
    async (args, extra) => getBridgeResultTool(store)(args, extra),
  );

  return server;
}

app.post("/mcp", mcpAuth, async (req: any, res: any) => {
  const server = createMcpServer();
  try {
    const transport = new StreamableHTTPServerTransport({ sessionIdGenerator: undefined });
    await server.connect(transport);
    await transport.handleRequest(req, res, req.body);
    res.on("close", () => {
      transport.close();
      server.close();
    });
  } catch (error) {
    if (!res.headersSent) {
      res.status(500).json({ jsonrpc: "2.0", error: { code: -32603, message: "Internal server error" }, id: null });
    }
    process.stderr.write(`MCP error: ${String(error)}\n`);
  }
});

app.get("/mcp", (_req: any, res: any) => {
  res.status(405).json({ jsonrpc: "2.0", error: { code: -32000, message: "Method not allowed." }, id: null });
});

app.delete("/mcp", (_req: any, res: any) => {
  res.status(405).json({ jsonrpc: "2.0", error: { code: -32000, message: "Method not allowed." }, id: null });
});

const bridgeAuth = requireBridgeAgentToken(config.bridgeAgentToken);
const handlers = createBridgeHandlers(store, config.jobSigningSecret);

app.get("/healthz", (_req: any, res: any) => {
  res.json({ status: "ok" });
});

app.get("/readyz", (_req: any, res: any) => {
  res.json({ status: "ready", authProvider: config.authProvider });
});

app.post("/bridge/jobs/pull", bridgeAuth, handlers.pullJob);
app.post("/bridge/jobs/:jobId/result", bridgeAuth, handlers.postResult);
app.get("/bridge/stats", bridgeAuth, (_req: any, res: any) => {
  res.json(store.getStats());
});

app.listen(config.mcpPort, (error?: Error) => {
  if (error) {
    process.stderr.write(`Failed to start control-plane: ${error.message}\n`);
    process.exit(1);
  }
  process.stderr.write(`Control-plane listening on http://localhost:${config.mcpPort} (mcp=/mcp, bridge=/bridge/*, storage=${config.storageMode})\n`);
});
