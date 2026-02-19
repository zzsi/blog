import { createRemoteJWKSet, jwtVerify } from "jose";
import type { OAuthTokenVerifier } from "@modelcontextprotocol/sdk/server/auth/provider.js";

type SharedSecretOptions = {
  mode: "shared_secret";
  secret: string;
  issuer?: string;
  audience?: string;
};

type OidcJwksOptions = {
  mode: "oidc_jwks";
  jwksUri: string;
  issuer: string;
  audience: string;
};

type Options = SharedSecretOptions | OidcJwksOptions;

function parseScopes(payload: Record<string, unknown>): string[] {
  if (typeof payload.scope === "string") {
    return payload.scope.split(" ").map((s) => s.trim()).filter(Boolean);
  }

  if (Array.isArray(payload.scp)) {
    return payload.scp.filter((v): v is string => typeof v === "string");
  }

  return [];
}

export function createJwtVerifier(options: Options): OAuthTokenVerifier {
  return {
    async verifyAccessToken(token: string) {
      const payload = options.mode === "shared_secret"
        ? (await jwtVerify(token, new TextEncoder().encode(options.secret), {
          algorithms: ["HS256"],
          issuer: options.issuer || undefined,
          audience: options.audience || undefined,
        })).payload
        : (await jwtVerify(token, createRemoteJWKSet(new URL(options.jwksUri)), {
          algorithms: ["RS256", "RS384", "RS512", "ES256", "ES384", "ES512"],
          issuer: options.issuer || undefined,
          audience: options.audience || undefined,
        })).payload;

      const subject = typeof payload.sub === "string" ? payload.sub : "unknown";
      const clientId = typeof payload.client_id === "string" ? payload.client_id : subject;

      return {
        token,
        clientId,
        scopes: parseScopes(payload as Record<string, unknown>),
        expiresAt: typeof payload.exp === "number" ? payload.exp : undefined,
        extra: {
          subject,
        },
      };
    },
  };
}
