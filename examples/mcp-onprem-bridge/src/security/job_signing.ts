import { createHmac, timingSafeEqual } from "node:crypto";

function canonicalize(value: unknown): string {
  if (Array.isArray(value)) return `[${value.map(canonicalize).join(",")}]`;
  if (value && typeof value === "object") {
    const entries = Object.entries(value as Record<string, unknown>).sort(([a], [b]) => a.localeCompare(b));
    return `{${entries.map(([k, v]) => `${JSON.stringify(k)}:${canonicalize(v)}`).join(",")}}`;
  }
  return JSON.stringify(value);
}

export function signPayload(payload: unknown, secret: string): string {
  const data = canonicalize(payload);
  return createHmac("sha256", secret).update(data).digest("hex");
}

export function verifyPayloadSignature(payload: unknown, secret: string, signature: string): boolean {
  const expected = signPayload(payload, secret);
  const a = Buffer.from(expected, "hex");
  const b = Buffer.from(signature, "hex");
  if (a.length !== b.length) return false;
  return timingSafeEqual(a, b);
}
