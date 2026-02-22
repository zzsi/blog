export type OnPremResource = "invoice" | "contract";

const INVOICES: Record<string, { invoiceId: string; status: string; amountCents: number }> = {
  cust_100: { invoiceId: "inv_20001", status: "open", amountCents: 15400 },
  cust_200: { invoiceId: "inv_20002", status: "paid", amountCents: 28900 },
};

const CONTRACTS: Record<string, { contractId: string; tier: string; renewalDate: string }> = {
  cust_100: { contractId: "ct_8001", tier: "enterprise", renewalDate: "2026-09-01" },
  cust_200: { contractId: "ct_8002", tier: "business", renewalDate: "2026-05-15" },
};

export function readOnPremResource(customerId: string, resource: OnPremResource) {
  if (resource === "invoice") {
    return INVOICES[customerId] ?? null;
  }
  return CONTRACTS[customerId] ?? null;
}
