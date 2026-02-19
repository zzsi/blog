export type TenantContext = {
  tenantId: string;
  subject: string;
  scopes: string[];
};

export function requireTenantContext(ctx: Partial<TenantContext>): TenantContext {
  if (!ctx.tenantId || !ctx.subject || !ctx.scopes) {
    throw new Error("forbidden: missing tenant context");
  }
  return ctx as TenantContext;
}
