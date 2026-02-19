export function auditWorkflowEvent(entry: Record<string, unknown>) {
  process.stderr.write(`${JSON.stringify({ event: "refund_workflow", ...entry })}\n`);
}
