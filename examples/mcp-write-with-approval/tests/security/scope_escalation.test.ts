import { describe, expect, it } from "vitest";
import { EXECUTE_SCOPE, REQUEST_SCOPE, APPROVE_SCOPE } from "../../src/policy/risk_rules";

describe("scope split", () => {
  it("uses distinct scopes for each stage", () => {
    expect(REQUEST_SCOPE).not.toBe(EXECUTE_SCOPE);
    expect(REQUEST_SCOPE).not.toBe(APPROVE_SCOPE);
    expect(APPROVE_SCOPE).not.toBe(EXECUTE_SCOPE);
  });
});
