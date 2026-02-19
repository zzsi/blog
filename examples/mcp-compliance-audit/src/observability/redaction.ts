const SECRET_KEY_PATTERN = /(authorization|token|api[_-]?key|password|secret)/i;

export function redactValue(value: unknown): unknown {
  if (Array.isArray(value)) {
    return value.map((item) => redactValue(item));
  }

  if (value && typeof value === "object") {
    return redact(value as Record<string, unknown>);
  }

  return value;
}

export function redact(input: Record<string, unknown>) {
  const out: Record<string, unknown> = {};

  for (const [k, v] of Object.entries(input)) {
    if (SECRET_KEY_PATTERN.test(k)) {
      out[k] = "[REDACTED]";
      continue;
    }
    out[k] = redactValue(v);
  }

  return out;
}
