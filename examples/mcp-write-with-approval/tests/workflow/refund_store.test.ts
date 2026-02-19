import { describe, expect, it } from "vitest";
import { RefundStore } from "../../src/workflows/approval_queue";

describe("RefundStore", () => {
  it("blocks execution before approval", () => {
    const store = new RefundStore();
    const request = store.create({
      orderId: "ord_1",
      amountCents: 99000,
      reason: "Customer requested refund",
      createdBy: "user-a",
      requiresApproval: true,
    });

    expect(() => store.execute(request.requestId)).toThrow();
  });

  it("allows approve then execute", () => {
    const store = new RefundStore();
    const request = store.create({
      orderId: "ord_2",
      amountCents: 99000,
      reason: "Duplicate charge case",
      createdBy: "user-a",
      requiresApproval: true,
    });

    const approved = store.approve(request.requestId, "approver-1");
    expect(approved.status).toBe("approved");

    const executed = store.execute(request.requestId);
    expect(executed.status).toBe("executed");
  });
});
