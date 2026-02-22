import { describe, expect, it } from "vitest";
import { BridgeJobStore } from "../../src/workflows/job_store";

describe("BridgeJobStore", () => {
  it("creates queued job and returns it for pull", () => {
    const store = new BridgeJobStore();
    const created = store.create({ customerId: "cust_100", resource: "invoice" });
    expect(created.status).toBe("queued");

    const pulled = store.pullNextQueued();
    expect(pulled?.jobId).toBe(created.jobId);
    expect(pulled?.status).toBe("processing");
  });

  it("completes job and exposes by requestId", () => {
    const store = new BridgeJobStore();
    const created = store.create({ customerId: "cust_200", resource: "contract" });
    const pulled = store.pullNextQueued();
    expect(pulled).toBeTruthy();

    const done = store.complete(created.jobId, { ok: true });
    expect(done.status).toBe("completed");

    const byReq = store.getByRequestId(created.requestId);
    expect(byReq?.status).toBe("completed");
    expect(byReq?.result).toEqual({ ok: true });
  });

  it("reuses existing job for same idempotency key", () => {
    const store = new BridgeJobStore();
    const first = store.createOrReuse({
      customerId: "cust_100",
      resource: "invoice",
      idempotencyKey: "same-request-0001",
    });
    const second = store.createOrReuse({
      customerId: "cust_100",
      resource: "invoice",
      idempotencyKey: "same-request-0001",
    });

    expect(first.reused).toBe(false);
    expect(second.reused).toBe(true);
    expect(second.job.jobId).toBe(first.job.jobId);
    expect(second.job.requestId).toBe(first.job.requestId);
  });

  it("returns queue stats", () => {
    const store = new BridgeJobStore();
    const one = store.create({ customerId: "cust_100", resource: "invoice" });
    const two = store.create({ customerId: "cust_200", resource: "contract" });
    expect(one.status).toBe("queued");
    expect(two.status).toBe("queued");

    store.pullNextQueued();
    store.complete(two.jobId, { ok: true });

    const stats = store.getStats();
    expect(stats.totalJobs).toBe(2);
    expect(stats.queued + stats.processing + stats.completed).toBe(2);
  });
});
