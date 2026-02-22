import { describe, expect, it } from "vitest";
import { requireTenantScope } from "../../src/middleware/authz";

describe("tenant isolation", () => {
  it("denies cross-tenant access", () => {
    expect(() =>
      requireTenantScope(
        { tenantId: "t1", subject: "user-1", scopes: ["invoices:read"] },
        "invoices:read",
        "t2",
      ),
    ).toThrow();
  });
});
