import { describe, expect, it } from "vitest";
import { requireScope } from "../../src/auth/scope_guard";

describe("requireScope", () => {
  it("allows when scope is present", () => {
    expect(
      requireScope({ authInfo: { token: "t", clientId: "c", scopes: ["invoices:read"] } }, "invoices:read"),
    ).toEqual(["invoices:read"]);
  });

  it("throws when scope is missing", () => {
    expect(() => requireScope({ authInfo: { token: "t", clientId: "c", scopes: [] } }, "invoices:read")).toThrow();
  });
});
