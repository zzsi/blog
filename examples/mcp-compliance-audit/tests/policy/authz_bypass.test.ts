import { describe, expect, it } from "vitest";
import { authorize } from "../../src/policy/deny_by_default";

describe("deny by default", () => {
  it("denies when allowed=false", () => {
    expect(() => authorize(false)).toThrow();
  });
});
