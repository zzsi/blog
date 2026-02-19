export type AuthMode = "none" | "jwt";
export type AuthProviderMode = "shared_secret" | "oidc_jwks";

export type AppConfig = {
  mcpPort: number;
  authMode: AuthMode;
  authProvider: AuthProviderMode;
  jwtSecret?: string;
  jwtIssuer?: string;
  jwtAudience?: string;
  oidcJwksUri?: string;
};

export function loadConfig(): AppConfig {
  const mcpPort = Number.parseInt(process.env.MCP_PORT ?? "3005", 10);
  const authMode = (process.env.AUTH_MODE ?? "jwt") as AuthMode;
  const authProvider = (process.env.AUTH_PROVIDER ?? "shared_secret") as AuthProviderMode;

  if (!Number.isInteger(mcpPort) || mcpPort < 1 || mcpPort > 65535) {
    throw new Error(`Invalid MCP_PORT: ${process.env.MCP_PORT ?? ""}`);
  }

  if (!(["none", "jwt"] as const).includes(authMode)) {
    throw new Error(`Invalid AUTH_MODE: ${authMode}`);
  }

  if (!(["shared_secret", "oidc_jwks"] as const).includes(authProvider)) {
    throw new Error(`Invalid AUTH_PROVIDER: ${authProvider}`);
  }

  if (authMode === "jwt" && authProvider === "shared_secret" && !process.env.JWT_SECRET) {
    throw new Error("JWT_SECRET is required when AUTH_MODE=jwt and AUTH_PROVIDER=shared_secret");
  }

  if (authMode === "jwt" && authProvider === "oidc_jwks") {
    if (!process.env.OIDC_JWKS_URI) {
      throw new Error("OIDC_JWKS_URI is required when AUTH_PROVIDER=oidc_jwks");
    }
    if (!process.env.JWT_ISSUER || !process.env.JWT_AUDIENCE) {
      throw new Error("JWT_ISSUER and JWT_AUDIENCE are required when AUTH_PROVIDER=oidc_jwks");
    }
  }

  return {
    mcpPort,
    authMode,
    authProvider,
    jwtSecret: process.env.JWT_SECRET,
    jwtIssuer: process.env.JWT_ISSUER,
    jwtAudience: process.env.JWT_AUDIENCE,
    oidcJwksUri: process.env.OIDC_JWKS_URI,
  };
}
