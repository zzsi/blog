import { writeAuditLog } from "../observability/audit_logger.js";

export function getSecret(name: string) {
  const envName = `SECRET_${name.toUpperCase().replace(/[^A-Z0-9]+/g, "_")}`;
  const value = process.env[envName] ?? "demo-placeholder-secret";
  // Never log credential material; only log access metadata.
  writeAuditLog({
    action: "secret_access",
    keyName: name,
    envVar: envName,
    source: process.env[envName] ? "env" : "default",
  });
  return value;
}
