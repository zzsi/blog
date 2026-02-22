export function logAuthzDecision(entry: Record<string, unknown>) {
  process.stderr.write(`${JSON.stringify({ event: "authz_decision", ...entry })}\n`);
}
