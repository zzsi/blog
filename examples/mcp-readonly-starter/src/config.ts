export type AuthMode = "none" | "jwt";

export type AppConfig = {
  mcpPort: number;
  authMode: AuthMode;
  jwtSecret?: string;
  jwtIssuer?: string;
  jwtAudience?: string;
};

export function loadConfig(): AppConfig {
  const mcpPort = Number.parseInt(process.env.MCP_PORT ?? "3000", 10);
  const authMode = (process.env.AUTH_MODE ?? "none") as AuthMode;

  if (!["none", "jwt"].includes(authMode)) {
    throw new Error(`Invalid AUTH_MODE: ${authMode}`);
  }

  if (authMode === "jwt" && !process.env.JWT_SECRET) {
    throw new Error("JWT_SECRET is required when AUTH_MODE=jwt");
  }

  return {
    mcpPort,
    authMode,
    jwtSecret: process.env.JWT_SECRET,
    jwtIssuer: process.env.JWT_ISSUER,
    jwtAudience: process.env.JWT_AUDIENCE,
  };
}
