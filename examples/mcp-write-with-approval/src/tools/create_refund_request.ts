export function createRefundRequest(input: { orderId: string; amountCents: number; reason: string }) {
  return {
    requestId: `rr_${Date.now()}`,
    status: "pending_approval",
    ...input,
  };
}
