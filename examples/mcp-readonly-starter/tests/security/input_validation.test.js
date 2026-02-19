import { describe, expect, it } from "vitest";
import { GetInvoiceStatusInput } from "../../src/tools/get_invoice_status";
import { ListOpenInvoicesInput } from "../../src/tools/list_open_invoices";
describe("input schemas", () => {
    it("rejects unknown fields", () => {
        expect(() => GetInvoiceStatusInput.parse({ invoiceId: "inv_123", extra: "x" })).toThrow();
    });
    it("enforces limit bounds", () => {
        expect(() => ListOpenInvoicesInput.parse({ limit: 0 })).toThrow();
        expect(() => ListOpenInvoicesInput.parse({ limit: 101 })).toThrow();
    });
});
