import { describe, expect, it } from "vitest";
import { redact } from "../../src/observability/redaction";

describe("redaction", () => {
  it("masks credential-like keys", () => {
    expect(redact({ token: "secret", q: "ok" })).toEqual({ token: "[REDACTED]", q: "ok" });
  });

  it("masks nested secret-like keys", () => {
    expect(
      redact({
        metadata: {
          authorization: "Bearer a",
          nested: { apiKey: "abc" },
        },
      }),
    ).toEqual({
      metadata: {
        authorization: "[REDACTED]",
        nested: { apiKey: "[REDACTED]" },
      },
    });
  });
});
