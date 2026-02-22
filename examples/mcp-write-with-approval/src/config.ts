export type AuthMode = "jwt";
export type AuthProviderMode = "shared_secret" | "oidc_jwks";

export type AppConfig = {
  mcpPort: number;
  authMode: AuthMode;
  authProvider: AuthProviderMode;
  jwtSecret?: string;
  jwtIssuer?: string;
  jwtAudience?: string;
  oidcJwksUri?: string;
  storageMode: "memory" | "file";
  stateFile: string;
};

export function loadConfig(): AppConfig {
  const mcpPort = Number.parseInt(process.env.MCP_PORT ?? "3002", 10);
  const authMode = (process.env.AUTH_MODE ?? "jwt") as AuthMode;
  const authProvider = (process.env.AUTH_PROVIDER ?? "shared_secret") as AuthProviderMode;

  if (authMode !== "jwt") {
    throw new Error("AUTH_MODE must be jwt for this demo");
  }

  if (!["shared_secret", "oidc_jwks"].includes(authProvider)) {
    throw new Error(`Invalid AUTH_PROVIDER: ${authProvider}`);
  }

  if (authProvider === "shared_secret" && !process.env.JWT_SECRET) {
    throw new Error("JWT_SECRET is required when AUTH_PROVIDER=shared_secret");
  }

  if (authProvider === "oidc_jwks") {
    if (!process.env.OIDC_JWKS_URI) {
      throw new Error("OIDC_JWKS_URI is required when AUTH_PROVIDER=oidc_jwks");
    }
    if (!process.env.JWT_ISSUER || !process.env.JWT_AUDIENCE) {
      throw new Error("JWT_ISSUER and JWT_AUDIENCE are required when AUTH_PROVIDER=oidc_jwks");
    }
  }

  const storageMode = (process.env.STORAGE_MODE ?? "memory") as "memory" | "file";
  if (!["memory", "file"].includes(storageMode)) {
    throw new Error(`Invalid STORAGE_MODE: ${storageMode}`);
  }

  const stateFile = process.env.REFUND_STATE_FILE ?? ".demo-data/refund_requests.json";

  return {
    mcpPort,
    authMode,
    authProvider,
    jwtSecret: process.env.JWT_SECRET,
    jwtIssuer: process.env.JWT_ISSUER,
    jwtAudience: process.env.JWT_AUDIENCE,
    oidcJwksUri: process.env.OIDC_JWKS_URI,
    storageMode,
    stateFile,
  };
}
