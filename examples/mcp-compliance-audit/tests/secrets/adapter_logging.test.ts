import { afterEach, describe, expect, it } from "vitest";
import { getSecret } from "../../src/secrets/adapter";

describe("secrets adapter logging", () => {
  const originalWrite = process.stderr.write.bind(process.stderr);

  afterEach(() => {
    delete process.env.SECRET_LOG_REDACTION;
    process.stderr.write = originalWrite;
  });

  it("does not log raw secret values", () => {
    process.env.SECRET_LOG_REDACTION = "super-sensitive-value";
    let captured = "";

    process.stderr.write = ((chunk: any) => {
      captured += String(chunk);
      return true;
    }) as typeof process.stderr.write;

    const value = getSecret("log_redaction");
    expect(value).toBe("super-sensitive-value");

    expect(captured).not.toContain("super-sensitive-value");
    expect(captured).toContain("secret_access");
    expect(captured).toContain("keyName");
    expect(captured).toContain("envVar");
    expect(captured).toContain("source");
  });
});
