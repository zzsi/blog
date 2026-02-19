import { describe, expect, it } from "vitest";
import { executeRefund } from "../../src/tools/execute_refund";

describe("approval gate", () => {
  it("blocks execution without approval", () => {
    expect(() => executeRefund({ requestId: "rr_1", approved: false, approverId: "u1" })).toThrow();
  });
});
