export function executeRefund(input: {
  requestId: string;
  approved: boolean;
  approverId: string;
}) {
  if (!input.approved) throw new Error("forbidden: request not approved");
  return { requestId: input.requestId, status: "executed", approverId: input.approverId };
}
