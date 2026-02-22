import type { MessageExtraInfo } from "@modelcontextprotocol/sdk/types.js";

export type TenantContext = {
  tenantId: string;
  subject: string;
  scopes: string[];
};

export function requireTenantContext(extra?: MessageExtraInfo): TenantContext {
  const auth = extra?.authInfo;
  const tenantId = typeof auth?.extra?.tenant_id === "string" ? auth.extra.tenant_id : undefined;

  if (!auth?.clientId || !tenantId) {
    throw new Error("forbidden: missing tenant context");
  }

  return {
    tenantId,
    subject: auth.clientId,
    scopes: auth.scopes,
  };
}
