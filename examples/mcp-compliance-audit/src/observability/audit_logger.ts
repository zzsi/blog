import { redact } from "./redaction.js";

export function writeAuditLog(entry: Record<string, unknown>) {
  process.stderr.write(`${JSON.stringify({ event: "audit", ...redact(entry) })}\n`);
}
