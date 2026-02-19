import { createMcpExpressApp } from "@modelcontextprotocol/sdk/server/express.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { requireBearerAuth } from "@modelcontextprotocol/sdk/server/auth/middleware/bearerAuth.js";
import { createJwtVerifier } from "./auth/jwt_verifier.js";
import { loadConfig } from "./config.js";
import { createServer } from "./server.js";

const config = loadConfig();
const app = createMcpExpressApp();

const jwtMiddleware = requireBearerAuth({
  verifier: createJwtVerifier({
    secret: config.jwtSecret,
    issuer: config.jwtIssuer,
    audience: config.jwtAudience,
  }),
  requiredScopes: [],
});

app.post("/mcp", jwtMiddleware, async (req: any, res: any) => {
  const server = createServer();

  try {
    const transport = new StreamableHTTPServerTransport({
      sessionIdGenerator: undefined,
    });

    await server.connect(transport);
    await transport.handleRequest(req, res, req.body);

    res.on("close", () => {
      transport.close();
      server.close();
    });
  } catch (error) {
    if (!res.headersSent) {
      res.status(500).json({
        jsonrpc: "2.0",
        error: { code: -32603, message: "Internal server error" },
        id: null,
      });
    }

    process.stderr.write(`HTTP transport error: ${String(error)}\n`);
  }
});

app.get("/mcp", (_req: any, res: any) => {
  res.status(405).json({
    jsonrpc: "2.0",
    error: { code: -32000, message: "Method not allowed." },
    id: null,
  });
});

app.delete("/mcp", (_req: any, res: any) => {
  res.status(405).json({
    jsonrpc: "2.0",
    error: { code: -32000, message: "Method not allowed." },
    id: null,
  });
});

app.listen(config.mcpPort, (error?: Error) => {
  if (error) {
    process.stderr.write(`Failed to start server: ${error.message}\n`);
    process.exit(1);
  }

  process.stderr.write(
    `MCP multitenant Streamable HTTP server listening on http://localhost:${config.mcpPort}/mcp\n`,
  );
});
