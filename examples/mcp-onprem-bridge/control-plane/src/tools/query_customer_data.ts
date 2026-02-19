export function queryCustomerData(input: { customerId: string; resource: "invoice" | "contract" }) {
  return {
    requestId: `req_${Date.now()}`,
    status: "queued_for_bridge",
    ...input,
  };
}
