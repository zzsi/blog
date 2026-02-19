export function routeTenant(tenantId: string) {
  return { tenantId, database: `db_${tenantId}` };
}
