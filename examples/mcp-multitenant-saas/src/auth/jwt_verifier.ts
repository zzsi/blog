import { jwtVerify } from "jose";
import type { OAuthTokenVerifier } from "@modelcontextprotocol/sdk/server/auth/provider.js";

export type JwtVerifierOptions = {
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

function parseTenantId(payload: Record<string, unknown>): string | undefined {
  if (typeof payload.tenant_id === "string") return payload.tenant_id;
  if (typeof payload.tid === "string") return payload.tid;
  return undefined;
}

export function createJwtVerifier(options: JwtVerifierOptions): OAuthTokenVerifier {
  const key = new TextEncoder().encode(options.secret);

  return {
    async verifyAccessToken(token: string) {
      const { payload } = await jwtVerify(token, key, {
        algorithms: ["HS256"],
        issuer: options.issuer || undefined,
        audience: options.audience || undefined,
      });

      const raw = payload as Record<string, unknown>;
      const subject = typeof raw.sub === "string" ? raw.sub : "unknown";
      const clientId = typeof raw.client_id === "string" ? raw.client_id : subject;
      const tenantId = parseTenantId(raw);

      if (!tenantId) {
        throw new Error("forbidden: tenant_id claim is required");
      }

      return {
        token,
        clientId,
        scopes: parseScopes(raw),
        expiresAt: typeof raw.exp === "number" ? raw.exp : undefined,
        extra: {
          subject,
          tenant_id: tenantId,
        },
      };
    },
  };
}
