export type AuthProviderMode = "shared_secret" | "oidc_jwks";

export type AppConfig = {
  mcpPort: number;
  authMode: "jwt";
  authProvider: AuthProviderMode;
  jwtSecret?: string;
  jwtIssuer?: string;
  jwtAudience?: string;
  oidcJwksUri?: string;
  bridgeAgentToken: string;
  jobSigningSecret: string;
  controlPlaneUrl: string;
  bridgePollIntervalMs: number;
};

export function loadConfig(): AppConfig {
  const mcpPort = Number.parseInt(process.env.MCP_PORT ?? "3003", 10);
  const authMode = (process.env.AUTH_MODE ?? "jwt") as "jwt";
  const authProvider = (process.env.AUTH_PROVIDER ?? "shared_secret") as AuthProviderMode;

  if (authMode !== "jwt") throw new Error("AUTH_MODE must be jwt");
  if (!["shared_secret", "oidc_jwks"].includes(authProvider)) {
    throw new Error(`Invalid AUTH_PROVIDER: ${authProvider}`);
  }

  if (authProvider === "shared_secret" && !process.env.JWT_SECRET) {
    throw new Error("JWT_SECRET is required when AUTH_PROVIDER=shared_secret");
  }

  if (authProvider === "oidc_jwks") {
    if (!process.env.OIDC_JWKS_URI) throw new Error("OIDC_JWKS_URI is required");
    if (!process.env.JWT_ISSUER || !process.env.JWT_AUDIENCE) {
      throw new Error("JWT_ISSUER and JWT_AUDIENCE are required with oidc_jwks");
    }
  }

  const bridgeAgentToken = process.env.BRIDGE_AGENT_TOKEN ?? "";
  const jobSigningSecret = process.env.JOB_SIGNING_SECRET ?? "";
  if (!bridgeAgentToken) throw new Error("BRIDGE_AGENT_TOKEN is required");
  if (!jobSigningSecret) throw new Error("JOB_SIGNING_SECRET is required");

  return {
    mcpPort,
    authMode,
    authProvider,
    jwtSecret: process.env.JWT_SECRET,
    jwtIssuer: process.env.JWT_ISSUER,
    jwtAudience: process.env.JWT_AUDIENCE,
    oidcJwksUri: process.env.OIDC_JWKS_URI,
    bridgeAgentToken,
    jobSigningSecret,
    controlPlaneUrl: process.env.CONTROL_PLANE_URL ?? `http://localhost:${mcpPort}`,
    bridgePollIntervalMs: Number.parseInt(process.env.BRIDGE_POLL_INTERVAL_MS ?? "2000", 10),
  };
}
