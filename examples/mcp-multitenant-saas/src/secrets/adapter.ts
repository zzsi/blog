export function getTenantSecret(tenantId: string, key: string) {
  // Stub for a secret manager integration.
  return `${tenantId}:${key}`;
}
