export function auditEvent(entry: Record<string, unknown>) {
  process.stderr.write(`${JSON.stringify({ event: "onprem_bridge", ...entry })}\n`);
}
