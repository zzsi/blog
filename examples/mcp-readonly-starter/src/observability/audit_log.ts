type AuditEvent = {
  tool: string;
  subject: string;
  scopes: string[];
  params: Record<string, unknown>;
  decision: "allow" | "deny";
  latency_ms: number;
  error?: string;
};

const SECRET_KEYS = new Set(["authorization", "token", "apiKey", "password"]);

function redact(input: Record<string, unknown>): Record<string, unknown> {
  const out: Record<string, unknown> = {};
  for (const [key, value] of Object.entries(input)) {
    out[key] = SECRET_KEYS.has(key) ? "[REDACTED]" : value;
  }
  return out;
}

export function auditToolCall(event: AuditEvent) {
  process.stderr.write(
    `${JSON.stringify({ event: "tool_call", ...event, params: redact(event.params) })}\n`,
  );
}
