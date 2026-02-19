import { describe, expect, it } from "vitest";
import { signPayload, verifyPayloadSignature } from "../../src/security/job_signing";

describe("job signing", () => {
  it("verifies valid signature", () => {
    const payload = { jobId: "job_1", requestId: "req_1", customerId: "cust_100", resource: "invoice" };
    const secret = "signing-secret";
    const sig = signPayload(payload, secret);
    expect(verifyPayloadSignature(payload, secret, sig)).toBe(true);
  });

  it("rejects modified payload", () => {
    const payload = { jobId: "job_1", result: { x: 1 } };
    const secret = "signing-secret";
    const sig = signPayload(payload, secret);
    expect(verifyPayloadSignature({ jobId: "job_1", result: { x: 2 } }, secret, sig)).toBe(false);
  });
});
