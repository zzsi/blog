import { writeAuditLog } from "../observability/audit_logger.js";

export function getSecret(name: string) {
  const envName = `SECRET_${name.toUpperCase().replace(/[^A-Z0-9]+/g, "_")}`;
  const value = process.env[envName] ?? "demo-placeholder-secret";
  writeAuditLog({ action: "secret_access", secretName: name, envName, value });
  return value;
}
