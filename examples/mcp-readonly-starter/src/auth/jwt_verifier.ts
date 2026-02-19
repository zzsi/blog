import { jwtVerify } from "jose";
import type { OAuthTokenVerifier } from "@modelcontextprotocol/sdk/server/auth/provider.js";

type Options = {
  secret: string;
  issuer?: string;
  audience?: string;
};

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
  const key = new TextEncoder().encode(options.secret);

  return {
    async verifyAccessToken(token: string) {
      const { payload } = await jwtVerify(token, key, {
        algorithms: ["HS256"],
        issuer: options.issuer || undefined,
        audience: options.audience || undefined,
      });

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
