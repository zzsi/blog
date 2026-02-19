export function logAuthzDecision(entry: Record<string, unknown>) {
  console.log(JSON.stringify({ event: "authz_decision", ...entry }));
}
