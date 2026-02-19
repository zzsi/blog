import { redact } from "./redaction";

export function writeAuditLog(entry: Record<string, unknown>) {
  console.log(JSON.stringify({ event: "audit", ...redact(entry) }));
}
