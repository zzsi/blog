import { describe, expect, it } from "vitest";
import { authorize, authorizeTool } from "../../src/policy/deny_by_default";

describe("deny by default", () => {
  it("denies when allowed=false", () => {
    expect(() => authorize(false)).toThrow();
  });

  it("denies when required scope is missing", () => {
    expect(() => authorizeTool("list_audit_events", ["compliance:control:read"])).toThrow(
      "forbidden: missing scope compliance:audit:read",
    );
  });

  it("allows when all required scopes are present", () => {
    expect(() => authorizeTool("get_control_status", ["compliance:control:read"])).not.toThrow();
  });
});
