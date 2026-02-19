import { createMcpExpressApp } from "@modelcontextprotocol/sdk/server/express.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { requireBearerAuth } from "@modelcontextprotocol/sdk/server/auth/middleware/bearerAuth.js";
import { createServer } from "./server.js";
import { loadConfig } from "./config.js";
import { createJwtVerifier } from "./auth/jwt_verifier.js";

const config = loadConfig();
const app = createMcpExpressApp();

const postHandler = async (req: any, res: any) => {
  const server = createServer(config.authMode);

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
};

if (config.authMode === "jwt") {
  const verifier = config.authProvider === "oidc_jwks"
    ? createJwtVerifier({
      mode: "oidc_jwks",
      jwksUri: config.oidcJwksUri!,
      issuer: config.jwtIssuer!,
      audience: config.jwtAudience!,
    })
    : createJwtVerifier({
      mode: "shared_secret",
      secret: config.jwtSecret!,
      issuer: config.jwtIssuer,
      audience: config.jwtAudience,
    });

  const jwtMiddleware = requireBearerAuth({
    verifier,
    requiredScopes: [],
  });

  app.post("/mcp", jwtMiddleware, postHandler);
} else {
  app.post("/mcp", postHandler);
}

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
    `MCP Streamable HTTP server listening on http://localhost:${config.mcpPort}/mcp (auth=${config.authMode})\n`,
  );
});
