import type { TenantContext } from "./tenant_context";

export function requireTenantScope(ctx: TenantContext, requiredScope: string, resourceTenantId: string) {
  if (!ctx.scopes.includes(requiredScope)) throw new Error("forbidden: missing scope");
  if (ctx.tenantId !== resourceTenantId) throw new Error("forbidden: cross-tenant access");
}
