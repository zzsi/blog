import { describe, expect, it } from "vitest";
import { requireTenantContext } from "../../src/middleware/tenant_context";

describe("requireTenantContext", () => {
  it("extracts tenant context from auth info", () => {
    const result = requireTenantContext({
      authInfo: {
        token: "t",
        clientId: "c",
        scopes: ["invoices:read"],
        extra: { tenant_id: "t1" },
      },
    });

    expect(result).toEqual({ tenantId: "t1", subject: "c", scopes: ["invoices:read"] });
  });

  it("throws without tenant claim", () => {
    expect(() =>
      requireTenantContext({
        authInfo: {
          token: "t",
          clientId: "c",
          scopes: ["invoices:read"],
        },
      }),
    ).toThrow();
  });
});
