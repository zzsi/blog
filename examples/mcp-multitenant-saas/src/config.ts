export type AuthMode = "jwt";

export type AppConfig = {
  mcpPort: number;
  authMode: AuthMode;
  jwtSecret: string;
  jwtIssuer?: string;
  jwtAudience?: string;
};

export function loadConfig(): AppConfig {
  const mcpPort = Number.parseInt(process.env.MCP_PORT ?? "3001", 10);
  const authMode = (process.env.AUTH_MODE ?? "jwt") as AuthMode;

  if (authMode !== "jwt") {
    throw new Error("AUTH_MODE must be jwt for multitenant demo");
  }

  if (!process.env.JWT_SECRET) {
    throw new Error("JWT_SECRET is required");
  }

  return {
    mcpPort,
    authMode,
    jwtSecret: process.env.JWT_SECRET,
    jwtIssuer: process.env.JWT_ISSUER,
    jwtAudience: process.env.JWT_AUDIENCE,
  };
}
