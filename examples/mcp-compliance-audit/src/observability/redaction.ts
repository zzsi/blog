const SECRET_KEYS = new Set(["authorization", "apiKey", "token", "password"]);

export function redact(input: Record<string, unknown>) {
  const out: Record<string, unknown> = {};
  for (const [k, v] of Object.entries(input)) {
    out[k] = SECRET_KEYS.has(k) ? "[REDACTED]" : v;
  }
  return out;
}
